#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""One isolated copied-W6 integration; historical M1/schema artifacts stay unchanged."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import importlib.util
import json
import platform
import sys
from pathlib import Path

import psycopg
from psycopg.conninfo import conninfo_to_dict, make_conninfo
from psycopg.rows import dict_row
from rdflib import Graph, RDF, Literal

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[5]
FREEZE_COMMIT='44803b489a44b484fa603e6fb4e4c92d50d82641'
FREEZE_SHA256='d0893183e6fc0dbd618e82408629104928572fa602a38b67919110942a230d48'


def require(ok,message):
    if not ok:raise ValueError(message)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def inputs():
    require(digest(HERE/'freeze.json')==FREEZE_SHA256,'Freeze manifest drift')
    freeze=json.loads((HERE/'freeze.json').read_text())
    for p,expected in freeze['files_sha256'].items():
        require(digest(HERE/p)==expected,'Contract/oracle drift: '+p)
    contract=json.loads((HERE/'contract.json').read_text())
    for p,expected in contract['source_sha256'].items():
        require(digest(ROOT/p)==expected,'Pinned source drift: '+p)
    versions={name:importlib.metadata.version(name) for name in contract['pinned_python_dependencies']}
    require(versions==contract['pinned_python_dependencies'],'Dependency version drift')
    legacy=load('cmpe_historical_m1',ROOT/'v2/data/migrations/2.1/0.2.0/verify_m1.py')
    admission=load('cmpe_isolated_m1',ROOT/contract['profile']/'profile.py')
    require(hashlib.sha256(legacy.SOURCE_SQL.encode()).hexdigest()==contract['source_sql_sha256'],'Source SELECT changed')
    require((ROOT/contract['profile']/'query.rq').read_text()==legacy.PAIR_SPARQL,'Historical query changed')
    # Only isolated profile artifacts are loaded, never the historical full P3 TBox/shapes.
    schema=Graph().parse(ROOT/contract['profile']/'profile.ttl')
    shapes=Graph().parse(ROOT/contract['profile']/'shapes.ttl')
    admission.audit_schema(schema);admission.audit_shapes(shapes)
    return contract,json.loads((HERE/'fixed-oracles.json').read_text()),versions,legacy,admission,schema,shapes


def target_guard(url,contract):
    info=conninfo_to_dict(url)
    require(info.get('dbname')==contract['database']['name'],'Only the named isolated fixture database is permitted')
    require(info.get('host') in contract['database']['hosts'],'Only an explicit loopback fixture host is permitted')
    return info


def guard_cases(contract):
    refused=[]
    for name,url in [('default-postgres','dbname=postgres host=localhost'),
                     ('legacy-default','dbname=cmpe host=localhost'),
                     ('nonloopback','dbname=cmpe_m1_core_332 host=example.org')]:
        try:target_guard(url,contract)
        except ValueError:refused.append(dict(id=name,refused=True))
        else:raise ValueError('Unsafe target accepted: '+name)
    target_guard('dbname=cmpe_m1_core_332 host=localhost',contract)
    return refused


def catalog(url,contract):
    with psycopg.connect(url,row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT current_database() AS db, current_setting(\'server_version_num\')::integer AS pg, postgis_lib_version() AS postgis')
            runtime=dict(cur.fetchone())
            require(runtime['db']==contract['database']['name'],'Connected database identity differs')
            require(runtime['pg']//10000==contract['database']['postgres_major'],'PostgreSQL major differs')
            require(runtime['postgis'].startswith(contract['database']['postgis_series']+'.'),'PostGIS series differs')
            cur.execute("SELECT tablename,indexname,indexdef FROM pg_indexes WHERE schemaname='cmpe' ORDER BY tablename,indexname")
            indexes=[dict(x) for x in cur.fetchall()]
            cur.execute("SELECT viewname,definition FROM pg_views WHERE schemaname='cmpe' ORDER BY viewname")
            views=[dict(x) for x in cur.fetchall()]
            cur.execute("SELECT table_name,column_default FROM information_schema.columns WHERE table_schema='cmpe' AND column_name='ontology_iri' AND column_default IS NOT NULL ORDER BY table_name")
            defaults={x['table_name']:x['column_default'] for x in cur.fetchall()}
            expected={name:"'"+value+"'::text" for name,value in contract['expected_ontology_iri_defaults'].items()}
            require(defaults==expected,'Historical ontology_iri defaults differ')
    payload=json.dumps(dict(indexes=indexes,views=views,defaults=defaults),sort_keys=True,separators=(',',':')).encode()
    return dict(runtime=runtime,indexes=indexes,views=views,ontology_iri_defaults=defaults,sha256=hashlib.sha256(payload).hexdigest())


def read_only_probe(url,oracle):
    with psycopg.connect(url) as conn:
        try:
            with conn.cursor() as cur:cur.execute(oracle['sql'])
        except psycopg.Error as error:
            conn.rollback();require(error.sqlstate==oracle['expected_sqlstate'],'Unexpected write-probe SQLSTATE')
            return dict(refused=True,sqlstate=error.sqlstate,where_false=True)
        else:
            conn.rollback();raise ValueError('Read-only connection allowed a write command')


def query_rows(graph,query,legacy):
    result=graph.query(query)
    rows=[{str(var):row[i] for i,var in enumerate(result.vars)} for row in result]
    return [list(x) for x in legacy.normalize_rows(rows,legacy.COLUMNS)]


def check_case(rows,oracle,legacy,admission,schema,shapes,query,out):
    graph=legacy.build_graph(rows);before=admission.canonical(graph)
    result=admission.admit(graph,schema,shapes)
    require(result['stage']=='ADMITTED','Copied export not admitted: '+json.dumps(result))
    require(result['explicit_target_union_counts']==oracle['expected_focus_counts'],'Actual copied focus counts differ')
    normalized=[list(x) for x in legacy.normalize_rows(rows,legacy.COLUMNS)]
    require(normalized==oracle['expected_query_tuples'],'SQL source tuples differ from pre-frozen fixture golden')
    projected=query_rows(graph,query,legacy)
    require(projected==normalized and len(projected)==oracle['expected_rows'],'SQL/SPARQL pair differs')
    require(len(graph)==oracle['expected_graph_triples'],'Export triple count differs')
    require(sum(x['run_public'] is None for x in rows)==oracle['expected_missing_runs'],'Optional run boundary differs')
    keys={(x['release_public'],int(x['row_number']),x['source_hash']) for x in rows}
    require(len(keys)==len(rows),'Source key collision')
    out.mkdir(parents=True,exist_ok=True)
    formats=[]
    for fmt,suffix in [('turtle','ttl'),('nt','nt'),('xml','rdf'),('json-ld','jsonld')]:
        path=out/('raw-export.'+suffix);graph.serialize(path,format=fmt)
        restored=Graph().parse(path,format=fmt)
        require(admission.canonical(restored)==before,'Raw RDF roundtrip differs: '+fmt)
        require(query_rows(restored,query,legacy)==normalized,'Roundtrip query differs: '+fmt)
        formats.append(fmt)
    logical,excluded=admission.logical_view(graph)
    require(len(excluded)==len(rows) and set(graph)-set(logical)==set(excluded),'Undeclared logical-view loss')
    require(all(p==RDF.value for _,p,_ in excluded),'Non-row data dropped from logical view')
    logical.serialize(out/'logical-view.ttl',format='turtle')
    require(admission.canonical(graph)==before,'Admission/view mutated raw RDF')
    return dict(id=oracle['id'],passed=True,query_rows=len(normalized),normalized_sql=normalized,
                normalized_sparql=projected,normalized_tuple_sha256=hashlib.sha256(legacy.compact(normalized)).hexdigest(),
                graph_triples=len(graph),graph_sha256=hashlib.sha256(before).hexdigest(),admission=result,
                source_keys=len(keys),missing_runs=oracle['expected_missing_runs'],roundtrip_formats=formats,
                logical_view_excluded_row_triples=len(excluded),logical_view_triples=len(logical),raw_rdf_unchanged=True),graph


def optional_case(admin,contract,oracle,legacy,admission,schema,shapes,query,out):
    target=contract['optional_run_target']
    with psycopg.connect(admin,row_factory=dict_row) as conn:
        try:
            with conn.cursor() as cur:
                cur.execute('''SELECT sr.source_record_id,sr.transformation_run_id FROM cmpe.source_record sr
                    JOIN cmpe.dataset_release dr ON dr.dataset_release_id=sr.dataset_release_id
                    JOIN cmpe.dataset d ON d.dataset_id=dr.dataset_id
                    WHERE d.public_id=%s AND dr.public_id=%s AND sr.row_number=%s AND sr.source_hash=%s''',
                    (target['dataset_public'],target['release_public'],target['row_number'],target['source_hash']))
                selected=cur.fetchall();require(len(selected)==1 and selected[0]['transformation_run_id'] is not None,'Optional boundary fixture precondition differs')
                cur.execute('UPDATE cmpe.source_record SET transformation_run_id=NULL WHERE source_record_id=%s',(selected[0]['source_record_id'],))
                require(cur.rowcount==1,'Fixture variation changed more than one row')
                cur.execute(legacy.SOURCE_SQL);rows=[dict(x) for x in cur.fetchall()]
                result,_=check_case(rows,oracle,legacy,admission,schema,shapes,query,out)
        finally:
            conn.rollback()
    result['fixture_transaction']=dict(column='source_record.transformation_run_id',rows_updated=1,rolled_back=True,
                                       durable_fixture_change=False,export_sql='Pinned unchanged SELECT')
    return result


def rejection_cases(graph,oracles,admission,schema,shapes):
    record=sorted(graph.subjects(RDF.type,admission.C.SourceRecord),key=str)[0]
    results=[]
    for oracle in oracles:
        altered=graph+Graph()
        if oracle['id']=='missing-record-type':altered.remove((record,RDF.type,admission.C.SourceRecord))
        elif oracle['id']=='missing-record-key':altered.remove((record,admission.D.identifier,None))
        elif oracle['id']=='hash-key-mismatch':altered.set((record,admission.P.value,Literal('controlled-mismatch')))
        result=admission.admit(altered,schema,shapes)
        require(result['stage']==oracle['stage'],'Export mutation not refused: '+oracle['id'])
        results.append(dict(id=oracle['id'],expected_stage=oracle['stage'],actual_stage=result['stage'],refused=True))
    return results


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database-url',help='Explicit isolated fixture URL; no implicit default is used')
    parser.add_argument('--ingest-report',type=Path)
    parser.add_argument('--output-dir',type=Path,default=ROOT/'build/m1-copied-integration')
    parser.add_argument('--preflight-only',action='store_true')
    args=parser.parse_args()
    contract,oracles,versions,legacy,admission,schema,shapes=inputs();guards=guard_cases(contract)
    if args.preflight_only:
        if args.database_url:target_guard(args.database_url,contract)
        print(json.dumps(dict(passed=True,source_pins=len(contract['source_sha256']),target_guards=guards,
                              database_connected=False,profile_triples=len(schema),shape_triples=len(shapes))))
        return
    require(bool(args.database_url) and args.ingest_report is not None,'Explicit fixture database and ingest receipt are required')
    target_guard(args.database_url,contract)
    ingest=json.loads(args.ingest_report.read_text())
    require(ingest['mode']=='schema-faithful-fixture' and not ingest['full_external_dataset_ingestion'] and not ingest['held_out_used'],'Not the synthetic copied-fixture receipt')
    require(ingest['counts']['source_record']==contract['fixtures']['source_records'],'Fixture source count differs')
    out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    readonly=make_conninfo(args.database_url,options='-c default_transaction_read_only=on -c statement_timeout=60000')
    before=legacy.database_snapshot(readonly);catalog_before=catalog(readonly,contract)
    require(set(before['row_counts'])==set(contract['expected_tables']),'Actual copied tables differ')
    dispositions=legacy.check_dispositions()
    old_before=legacy.run_legacy(readonly,out/'legacy-before')
    require(old_before['pairs_passed']==oracles['expected_legacy_pairs_before'],'Legacy before pair count differs')
    query=(ROOT/contract['profile']/'query.rq').read_text()
    rows=legacy.sql_rows(readonly)
    baseline,graph=check_case(rows,oracles['cases'][0],legacy,admission,schema,shapes,query,out/'baseline')
    refusals=rejection_cases(graph,oracles['expected_refusals'],admission,schema,shapes)
    readonly_probe=read_only_probe(readonly,oracles['read_only_write_probe'])
    optional=optional_case(args.database_url,contract,oracles['cases'][1],legacy,admission,schema,shapes,query,out/'optional-run')
    old_after=legacy.run_legacy(readonly,out/'legacy-after')
    after=legacy.database_snapshot(readonly);catalog_after=catalog(readonly,contract)
    require(before==after,'Copied base rows/column/constraint catalog changed')
    require(catalog_before==catalog_after,'Default IRIs/indexes/views changed')
    require(old_before==old_after and old_after['pairs_passed']==oracles['expected_legacy_pairs_after'],'Legacy KG/query changed')
    inputs()  # Recheck frozen source identity after execution, not just at startup.
    report=dict(schema_version='CMPE-M1CopiedIntegrationResults/0.1.0',passed=True,
        freeze_commit=FREEZE_COMMIT,contract_sha256=digest(HERE/'contract.json'),oracle_sha256=digest(HERE/'fixed-oracles.json'),
        source_commit=contract['source_commit'],profile=contract['profile'],profile_manifest_sha256=digest(ROOT/contract['profile']/'manifest.json'),
        python_versions=versions,database_target=contract['database']['name'],database_before=before,database_after=after,
        software=dict(python=platform.python_version(),psycopg_binary=importlib.metadata.version('psycopg-binary'),
                      libpq_version=psycopg.pq.version(),psycopg_implementation=psycopg.pq.__impl__),
        catalog_before=catalog_before,catalog_after=catalog_after,base_rows_schema_defaults_indexes_views_unchanged=True,
        selected_mapping_ids=contract['selected_mapping_ids'],mapping_dispositions=dispositions,
        legacy_before=old_before,legacy_after=old_after,cases=[baseline,optional],export_mutation_refusals=refusals,
        target_guards=guards,read_only_write_probe=readonly_probe,export_connections_default_read_only=True,
        optional_fixture_update_count=1,optional_fixture_update_rolled_back=True,
        copied_database_executed=True,synthetic_fixture=True,full_external_dataset_ingestion=False,
        full_native_validation_claimed=False,old_m1_or_w6_sources_modified=False,ga_ready=False,
        rollback='Baseline exports use enforced read-only connections. A separate single nullable-FK fixture update was rolled back; all W6 row/schema/default/index/view and legacy KG/query snapshots match.',
        boundary=contract['boundary'])
    (out/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(passed=True,copied_database_executed=True,source_rows=baseline['query_rows'],
                         legacy_pairs_before=4,legacy_pairs_after=4,new_pair_cases=2,focus=baseline['admission']['explicit_target_union_counts'],
                         optional_missing_runs=optional['missing_runs'],rollback_verified=True,ga_ready=False)),flush=True)


if __name__=='__main__':main()
