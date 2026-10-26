#!/usr/bin/env python3
"""Copied-W6 typed capacity bearer, observation separation and rollback checks."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import platform
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

import psycopg
from psycopg.rows import dict_row
from pyshacl import validate
from rdflib import Graph, Literal, Namespace, RDF, OWL
from rdflib.namespace import DCTERMS, XSD
from owlrl import DeductiveClosure, OWLRL_Semantics

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
spec = importlib.util.spec_from_file_location("m4_m3", HERE.parent / "0.4.0/verify_m3.py")
m3 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m3)
m1 = m3.m1
C = Namespace("https://w3id.org/cm-pharme/2.1/")
PROV = Namespace("http://www.w3.org/ns/prov#")
M4 = Namespace("urn:cmpe:rdb-m4:")
ORACLES = json.loads((HERE / "fixed-oracles.json").read_text())
E = ORACLES["expected"]
FIX = json.loads((HERE / "fixtures-spec.json").read_text())
CAPS = FIX["capacities"]
OBS = FIX["observation"]
RUN = "m4-fixture-run:0.5.0"
RELEASE = "m4-fixture-release:0.5.0"
CAP_COLUMNS = ["capacity_id", "projection_version", "bearer_type", "bearer_id", "claim_kind",
               "release_id", "row_number", "source_hash", "run_id", "assertion_id", "evidence_id"]
OBS_COLUMNS = ["observation_id", "facility_id", "reporting_period", "quantity", "source_hash",
               "release_id", "run_id", "assertion_id", "evidence_id"]

CAP_SQL = """
SELECT sc.public_id AS capacity_id, sc.projection_version,
       CASE WHEN sc.organization_id IS NOT NULL THEN 'organization' ELSE 'facility' END AS bearer_type,
       COALESCE(o.public_id,f.public_id) AS bearer_id, sc.claim_kind,
       dr.public_id AS release_id, sr.row_number, sr.source_hash,
       tr.public_id AS run_id, a.public_id AS assertion_id, es.public_id AS evidence_id,
       sr.raw_key
FROM cmpe.supply_capacity_21 sc
LEFT JOIN cmpe.organization o USING (organization_id)
LEFT JOIN cmpe.facility f USING (facility_id)
LEFT JOIN cmpe.source_record sr ON sr.source_record_id=sc.source_record_id
LEFT JOIN cmpe.dataset_release dr USING (dataset_release_id)
LEFT JOIN cmpe.transformation_run tr USING (transformation_run_id)
LEFT JOIN cmpe.assertion a ON a.assertion_id=sc.assertion_id
LEFT JOIN cmpe.evidence_support es ON es.evidence_support_id=sc.evidence_support_id
ORDER BY sc.public_id
"""
OBS_SQL = """
SELECT obs.public_id AS observation_id, f.public_id AS facility_id,
       obs.reporting_period, obs.package_count AS quantity,
       sr.source_hash, dr.public_id AS release_id, tr.public_id AS run_id,
       a.public_id AS assertion_id, es.public_id AS evidence_id, sr.row_number, sr.raw_key
FROM cmpe.observation_result obs
JOIN cmpe.facility f USING (facility_id)
JOIN cmpe.source_record sr USING (source_record_id)
JOIN cmpe.dataset_release dr USING (dataset_release_id)
JOIN cmpe.transformation_run tr USING (transformation_run_id)
JOIN cmpe.assertion a ON a.assertion_id=obs.assertion_id
JOIN cmpe.evidence_support es ON es.source_record_id=sr.source_record_id AND es.assertion_id=a.assertion_id
WHERE obs.observation_kind='supply_capacity'
ORDER BY obs.public_id
"""
PREFIX = """
PREFIX c: <https://w3id.org/cm-pharme/2.1/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
"""
CAP_SPARQL = PREFIX + """
SELECT ?capacity_id ?projection_version ?bearer_type ?bearer_id ?claim_kind
       ?release_id ?row_number ?source_hash ?run_id ?assertion_id ?evidence_id WHERE {
  ?cap a c:SupplyCapacity ; dct:identifier ?capacity_id ; dct:hasVersion ?projection_version ; dct:type ?claim_kind .
  { ?bearer a c:Organization ; c:organizationHasSupplyCapacity ?cap . BIND('organization' AS ?bearer_type) }
  UNION
  { ?bearer a c:Facility ; c:facilityHasSupplyCapacity ?cap . BIND('facility' AS ?bearer_type) }
  ?bearer dct:identifier ?bearer_id .
  OPTIONAL {
    ?cap prov:wasDerivedFrom ?source ; dct:relation ?evidence .
    ?source rdf:value ?row_number ; prov:value ?source_hash ; prov:wasGeneratedBy ?run .
    ?release c:containsSourceRecord ?source ; dct:identifier ?release_id .
    ?run dct:identifier ?run_id .
    ?evidence dct:identifier ?evidence_id ; dct:relation ?assertion .
    ?assertion dct:identifier ?assertion_id .
  }
} ORDER BY ?capacity_id
"""
OBS_SPARQL = PREFIX + """
SELECT ?observation_id ?facility_id ?reporting_period ?quantity ?source_hash
       ?release_id ?run_id ?assertion_id ?evidence_id WHERE {
  ?obs a c:SupplyCapacityObservationResult ; dct:identifier ?observation_id ; dct:relation ?facility, ?evidence ;
       c:validFrom ?date ; c:measureNumericValue ?quantity ; prov:wasDerivedFrom ?source .
  ?facility a c:Facility ; dct:identifier ?facility_id .
  ?source prov:value ?source_hash ; prov:wasGeneratedBy ?run .
  ?release c:containsSourceRecord ?source ; dct:identifier ?release_id .
  ?run dct:identifier ?run_id .
  ?evidence dct:identifier ?evidence_id ; dct:relation ?assertion .
  ?assertion dct:identifier ?assertion_id .
  BIND(SUBSTR(STR(?date),1,10) AS ?reporting_period)
} ORDER BY ?observation_id
"""


def source_row(key):
    raw = dict(FIX["source_records"][key])
    if key == "capacity-assertion":
        raw.update({"subject_public_id": CAPS[0]["bearer_public_id"],
                    "predicate_key": "organizationHasSupplyCapacity", "object_public_id": CAPS[0]["public_id"]})
    else:
        raw.update({"subject_public_id": OBS["facility_public_id"], "predicate_key": "capacity_measurement_fixture",
                    "object_public_id": OBS["public_id"], "observation_kind": OBS["observation_kind"],
                    "reporting_period": OBS["reporting_period"], "package_count": OBS["package_count"], "unit": OBS["unit"]})
    return {"release_id": RELEASE, "run_id": RUN, "source_hash": m1.sha(m1.compact(raw)),
            "row_number": 1 if key == "capacity-assertion" else 2, "raw_key": raw,
            "assertion_id": "m4-fixture-assertion:" + key, "evidence_id": "m4-fixture-evidence:" + key}


def example_rows():
    rows = []
    for cap in CAPS:
        row = {"capacity_id": cap["public_id"], "projection_version": FIX["projection_version"],
               "bearer_type": cap["bearer_type"], "bearer_id": cap["bearer_public_id"], "claim_kind": FIX["claim_kind"]}
        row.update(source_row(cap["source_key"]) if cap["source_key"] else
                   {k: None for k in ["release_id","run_id","source_hash","row_number","raw_key","assertion_id","evidence_id"]})
        rows.append(row)
    observation = {"observation_id":OBS["public_id"],"facility_id":OBS["facility_public_id"],
                   "reporting_period":OBS["reporting_period"],"quantity":Decimal(OBS["package_count"]),
                   **source_row(OBS["source_key"])}
    return rows, [observation]


def typed(g, node, cls, key=None):
    g.add((node, RDF.type, cls))
    if key is not None: g.add((node,DCTERMS.identifier,Literal(key)))


def provenance(g, subject, row, assertion_subject, predicate):
    if row["source_hash"] is None: return
    assert m1.sha(m1.compact(row["raw_key"])) == row["source_hash"]
    source = m1.node("source-record", m1.source_key({"release_public":row["release_id"],
                      "row_number":row["row_number"],"source_hash":row["source_hash"]}))
    release = m1.node("dataset-release",row["release_id"])
    run = m1.node("provenance-activity",row["run_id"])
    assertion = m1.node("assertion",row["assertion_id"])
    evidence = m1.node("evidence-support",row["evidence_id"])
    typed(g,source,C.SourceRecord); typed(g,release,C.DatasetRelease,row["release_id"])
    typed(g,run,C.ProvenanceActivity,row["run_id"]); typed(g,assertion,C.Assertion,row["assertion_id"])
    g.add((source,RDF.value,Literal(row["row_number"],datatype=XSD.integer)))
    g.add((source,PROV.value,Literal(row["source_hash"])))
    g.add((source,DCTERMS.type,Literal("synthetic_fixture")))
    g.add((source,PROV.wasGeneratedBy,run)); g.add((release,C.containsSourceRecord,source))
    g.add((subject,PROV.wasDerivedFrom,source)); g.add((subject,DCTERMS.relation,evidence))
    # Preserve SQL evidence identity without settling the unresolved M025 role type.
    g.add((evidence,DCTERMS.identifier,Literal(row["evidence_id"])))
    g.add((evidence,PROV.wasDerivedFrom,source)); g.add((evidence,DCTERMS.relation,assertion))
    g.add((assertion,RDF.subject,assertion_subject)); g.add((assertion,RDF.predicate,predicate))
    g.add((assertion,RDF.object,subject))


def export(capacities, observations):
    g=Graph()
    for prefix,ns in [("c",C),("dct",DCTERMS),("prov",PROV)]:g.bind(prefix,ns)
    for row in capacities:
        cap=m1.node("supply-capacity",row["capacity_id"])
        bearer=m1.node(row["bearer_type"],row["bearer_id"])
        org=row["bearer_type"]=="organization"
        typed(g,cap,C.SupplyCapacity,row["capacity_id"])
        typed(g,bearer,C.Organization if org else C.Facility,row["bearer_id"])
        primary=C.organizationHasSupplyCapacity if org else C.facilityHasSupplyCapacity
        g.add((bearer,primary,cap)); g.add((cap,DCTERMS.hasVersion,Literal(row["projection_version"])))
        g.add((cap,DCTERMS.type,Literal(row["claim_kind"])))
        provenance(g,cap,row,bearer,primary)
    for row in observations:
        obs=m1.node("observation-result",row["observation_id"])
        facility=m1.node("facility",row["facility_id"])
        typed(g,obs,C.SupplyCapacityObservationResult,row["observation_id"])
        typed(g,facility,C.Facility,row["facility_id"])
        g.add((obs,DCTERMS.type,Literal("synthetic_fixture")));g.add((obs,DCTERMS.relation,facility))
        g.add((obs,C.measureNumericValue,Literal(row["quantity"],datatype=XSD.decimal)))
        g.add((obs,C.measureUnitLabel,Literal(OBS["unit"])))
        g.add((obs,C.validFrom,Literal(str(row["reporting_period"])+"T00:00:00Z",datatype=XSD.dateTime)))
        provenance(g,obs,row,facility,M4.capacity_measurement_fixture)
    typed(g,m1.node("organization",FIX["no_capacity_organization"]),C.Organization,FIX["no_capacity_organization"])
    return g


def minimal(route="organization", capacity=None, bearer=None):
    g=Graph();cap=capacity or m1.node("supply-capacity","m4-minimal")
    b=bearer or m1.node(route,"m4-minimal-bearer")
    typed(g,cap,C.SupplyCapacity);typed(g,b,C.Organization if route=="organization" else C.Facility)
    g.add((b,C.organizationHasSupplyCapacity if route=="organization" else C.facilityHasSupplyCapacity,cap))
    return g,cap,b


def shacl_checks(g, ontology, shapes):
    def check(data):
        ok,report,_=validate(data,shacl_graph=shapes,ont_graph=ontology,inference="none",advanced=True,meta_shacl=True)
        return bool(ok),len(list(report.subjects(RDF.type,Namespace("http://www.w3.org/ns/shacl#").ValidationResult)))
    org,cap,b=minimal();fac,_,_=minimal("facility")
    cases={"positive_export":g,"organization_bearer":org,"facility_bearer_unknown_source":fac}
    bare=Graph();typed(bare,m1.node("organization","bare"),C.Organization);typed(bare,m1.node("facility","bare"),C.Facility)
    cases["no_capacity_required"]=bare
    missing=org-Graph();missing.remove((b,C.organizationHasSupplyCapacity,cap));cases["missing_bearer"]=missing
    dual=org-Graph();other=m1.node("organization","other");typed(dual,other,C.Organization)
    dual.add((other,C.organizationHasSupplyCapacity,cap));cases["two_organization_bearers"]=dual
    both=org-Graph();site=m1.node("facility","other");typed(both,site,C.Facility)
    both.add((site,C.facilityHasSupplyCapacity,cap));cases["both_routes"]=both
    wrong=org-Graph();wrong.remove((b,RDF.type,C.Organization));typed(wrong,b,C.Facility);cases["wrong_bearer_type"]=wrong
    broad=missing-Graph();broad.add((cap,C.capacityBearer,b));cases["broad_only"]=broad
    inverse=missing-Graph();inverse.add((cap,C.capacityOrganizationBearer,b));cases["typed_inverse_only"]=inverse
    obs=org-Graph();obs.remove((cap,RDF.type,C.SupplyCapacity));typed(obs,cap,C.SupplyCapacityObservationResult)
    cases["observation_used_as_mode"]=obs
    collision=org-Graph();typed(collision,cap,C.SupplyCapacityObservationResult);cases["observation_and_mode_collision"]=collision
    fullcap=m1.node("supply-capacity",CAPS[0]["public_id"])
    partial=g-Graph();partial.remove((fullcap,DCTERMS.relation,None));cases["partial_provenance"]=partial
    mismatch=g-Graph();assertion=m1.node("assertion","m4-fixture-assertion:capacity-assertion")
    mismatch.set((assertion,RDF.subject,m1.node("organization",FIX["no_capacity_organization"])));cases["misaligned_assertion"]=mismatch
    observed={};counts={}
    for name,data in cases.items():observed[name],counts[name]=check(data)
    if observed!=E["shacl"]:raise AssertionError(f"Frozen SHACL oracle mismatch: {observed}")
    return {"expected":E["shacl"],"observed":observed,"violation_counts":counts,"all_expected_met":True}


def reasoner_checks(g,ontology):
    org,cap,b=minimal();other=m1.node("organization","other")
    missing=Graph();typed(missing,cap,C.SupplyCapacity)
    dual=org-Graph();typed(dual,other,C.Organization);dual.add((other,C.organizationHasSupplyCapacity,cap))
    distinct=dual-Graph();distinct.add((b,OWL.differentFrom,other))
    both=org-Graph();site=m1.node("facility","other");typed(both,site,C.Facility);both.add((site,C.facilityHasSupplyCapacity,cap))
    wrong=org-Graph();wrong.remove((b,RDF.type,C.Organization));typed(wrong,b,C.Facility)
    collision=org-Graph();typed(collision,cap,C.SupplyCapacityObservationResult)
    no_capacity=Graph()
    for cls,primary in [(C.Organization,C.organizationHasSupplyCapacity),(C.Facility,C.facilityHasSupplyCapacity)]:
        n=m1.node("countermodel-bearer",str(cls).split('/')[-1]);typed(no_capacity,n,cls)
        restriction=m1.node("zero-capacity-restriction",str(primary).split('/')[-1])
        typed(no_capacity,restriction,OWL.Restriction);no_capacity.add((restriction,OWL.onProperty,primary))
        no_capacity.add((restriction,OWL.maxCardinality,Literal(0,datatype=XSD.nonNegativeInteger)))
        no_capacity.add((n,RDF.type,restriction))
    observation=no_capacity-Graph();typed(observation,m1.node("observation-result","only"),C.SupplyCapacityObservationResult)
    cases={"positive":g,"missing_explicit_bearer_open_world":missing,
           "two_organization_iris_without_inequality":dual,"two_distinct_organizations":distinct,
           "organization_and_facility_routes":both,"wrong_typed_bearer":wrong,
           "observation_mode_collision":collision,"observation_without_capacity":observation,
           "eligible_bearers_with_zero_capacities":no_capacity}
    observed={name:m3.consistent(ontology,data) for name,data in cases.items()}
    if observed!=E["hermit"]:raise AssertionError(f"Frozen HermiT oracle mismatch: {observed}")
    primary_pairs={(m1.node(x["bearer_type"],x["bearer_public_id"]),m1.node("supply-capacity",x["public_id"])) for x in CAPS}
    assert not list(g.triples((None,C.capacityBearer,None)))
    inferred=ontology+g;DeductiveClosure(OWLRL_Semantics).expand(inferred)
    pairs={(o,s) for s,_,o in inferred.triples((None,C.capacityBearer,None)) if str(s).startswith(m1.INST)}
    assert pairs==primary_pairs
    obs=m1.node("observation-result",OBS["public_id"])
    assert (obs,RDF.type,C.SupplyCapacity) not in inferred
    only_fac=m1.node("facility",OBS["facility_public_id"])
    assert not list(inferred.triples((only_fac,C.facilityHasSupplyCapacity,None)))
    return {"expected":E["hermit"],"observed":observed,"all_expected_met":True,
            "derived_bearer_pairs":len(pairs),"primary_only_export":True,"observation_did_not_create_mode":True}


def native_check(config):
    native=json.loads((ROOT/config["candidate_native"]).read_text());items={x['id']:x for x in native['elements']}
    assert items['SupplyCapacity']['stereotype']=='mode' and items['SupplyCapacity']['restrictedTo']==['intrinsic-mode']
    for name,kind in [('organizationHasSupplyCapacity','Organization'),('facilityHasSupplyCapacity','Facility')]:
        assert items['rel-'+name]['stereotype']=='characterization'
        assert items['end-'+name+'-source']['propertyType']==kind
        assert items['end-'+name+'-source']['cardinality']=='0..1'
        assert items['end-'+name+'-target']['propertyType']=='SupplyCapacity'
        assert items['end-'+name+'-target']['cardinality']=='0..*'
    assert 'p4a-capacity-xor-note' in items
    return {'intrinsic_mode':True,'two_typed_characterizations':True,'native_xor_note_present':True,
            'boundary':'Native anchors and multiplicities only; full candidate parser/anti-pattern approval remains separate.'}


def query_rows(g,query):
    q=g.query(query)
    return [{str(v):row[i] for i,v in enumerate(q.vars)} for row in q]


def rdf_checks(capacities,observations,out,config):
    g=export(capacities,observations);nt=m1.canonical(g)
    (out/'capacity-21.nt').write_bytes(nt);g.serialize(out/'capacity-21.ttl',format='turtle')
    reparsed=Graph().parse(out/'capacity-21.nt',format='nt');assert m1.canonical(reparsed)==nt
    cap_answers=query_rows(reparsed,CAP_SPARQL);obs_answers=query_rows(reparsed,OBS_SPARQL)
    assert len(cap_answers)==E['capacity_rows'] and len(obs_answers)==E['observation_rows']
    assert sum(str(r['bearer_type'])=='organization' for r in cap_answers)==E['organization_routes']
    assert sum(str(r['bearer_type'])=='facility' for r in cap_answers)==E['facility_routes']
    assert sum(r['source_hash'] is not None for r in cap_answers)==E['capacity_source_routes']
    assert sum(r['source_hash'] is None for r in cap_answers)==E['capacity_unknown_source_routes']
    assert {str(r['capacity_id']) for r in cap_answers}=={x['public_id'] for x in CAPS}
    assert str(obs_answers[0]['observation_id'])==OBS['public_id']
    assert not {str(r['capacity_id']) for r in cap_answers} & {str(r['observation_id']) for r in obs_answers}
    assert not [r for r in cap_answers if str(r['bearer_id'])==OBS['facility_public_id']]
    ontology=Graph().parse(ROOT/config['candidate_ontology'])
    shapes=Graph().parse(ROOT/config['candidate_shapes'])+Graph().parse(HERE/'admission.ttl')
    return {'rdf_roundtrip':True,'graph_sha256':m1.sha(nt),'graph_triples':len(g),
            'capacity_rows':m1.normalize_rows(cap_answers,CAP_COLUMNS),'observation_rows':m1.normalize_rows(obs_answers,OBS_COLUMNS),
            'observation_only_capacity_rows':0,'real_capacity_witnesses':0,'unknown_source_capacity_rows':1,
            'shacl':shacl_checks(g,ontology,shapes),'owl':reasoner_checks(g,ontology),'native':native_check(config)}


def seed(url):
    capacities,observations=example_rows()
    with psycopg.connect(url,row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            for table,key in [('organization','organization_id'),('facility','facility_id'),('dataset','dataset_id'),
                              ('dataset_release','dataset_release_id'),('transformation_run','transformation_run_id'),
                              ('source_record','source_record_id'),('assertion','assertion_id'),('evidence_support','evidence_support_id'),
                              ('observation_result','observation_result_id')]:
                cur.execute(f'SELECT count(*) AS n FROM cmpe.{table} WHERE {key} BETWEEN -321300 AND -321001')
                assert cur.fetchone()['n']==0,'Reserved M4 IDs already used'
            cur.execute((HERE/'migration.sql').read_text())
            cur.execute("INSERT INTO cmpe.organization(organization_id,public_id,preferred_name) VALUES (-321101,%s,'Synthetic Capacity Organization'),(-321102,%s,'Synthetic Organization Without Capacity')",(CAPS[0]['bearer_public_id'],FIX['no_capacity_organization']))
            cur.execute("INSERT INTO cmpe.facility(facility_id,public_id,preferred_name) VALUES (-321201,%s,'Synthetic Capacity Facility'),(-321202,%s,'Synthetic Observation Only Facility')",(CAPS[1]['bearer_public_id'],OBS['facility_public_id']))
            cur.execute("INSERT INTO cmpe.dataset(dataset_id,public_id,title,source_role) VALUES (-321001,'m4-fixture-dataset','Synthetic M4 source records','fixture')")
            cur.execute("INSERT INTO cmpe.dataset_release(dataset_release_id,dataset_id,public_id,release_label) VALUES (-321001,-321001,%s,'synthetic-0.5.0')",(RELEASE,))
            cur.execute("INSERT INTO cmpe.transformation_run(transformation_run_id,public_id,adapter_name,adapter_version,status) VALUES (-321001,%s,'m4-fixture','0.5.0','completed')",(RUN,))
            for i,(key,subject,predicate,object_id) in enumerate([
                ('capacity-assertion',CAPS[0]['bearer_public_id'],'organizationHasSupplyCapacity',CAPS[0]['public_id']),
                ('observation-record',OBS['facility_public_id'],'capacity_measurement_fixture',OBS['public_id'])],1):
                pk=-321000-i;r=source_row(key)
                cur.execute("INSERT INTO cmpe.source_record(source_record_id,dataset_release_id,transformation_run_id,row_number,source_hash,raw_key) VALUES (%s,-321001,-321001,%s,%s,%s::jsonb)",(pk,i,r['source_hash'],json.dumps(r['raw_key'])))
                cur.execute("INSERT INTO cmpe.assertion(assertion_id,public_id,assertion_type,subject_public_id,predicate_key,object_public_id) VALUES (%s,%s,'synthetic_fixture',%s,%s,%s)",(pk,r['assertion_id'],subject,predicate,object_id))
                cur.execute("INSERT INTO cmpe.evidence_support(evidence_support_id,public_id,source_record_id,assertion_id) VALUES (%s,%s,%s,%s)",(pk,r['evidence_id'],pk,pk))
            cur.execute("""INSERT INTO cmpe.observation_result(observation_result_id,public_id,observation_kind,facility_id,reporting_period,package_count,source_record_id,assertion_id)
                VALUES (-321001,%s,'supply_capacity',-321202,%s,%s,-321002,-321002)""",(OBS['public_id'],OBS['reporting_period'],OBS['package_count']))
            insert="""INSERT INTO cmpe.supply_capacity_21(public_id,organization_id,facility_id,claim_kind,source_record_id,assertion_id,evidence_support_id)
                VALUES (%s,%s,%s,%s,%s,%s,%s)"""
            org=(CAPS[0]['public_id'],-321101,None,'synthetic_fixture',-321001,-321001,-321001)
            fac=(CAPS[1]['public_id'],None,-321201,'synthetic_fixture',None,None,None)
            cur.execute(insert,org);cur.execute(insert,fac)
            updates={'missing_bearer':{1:None,2:None},'double_route':{1:-321101,2:-321201},
                     'facility_in_organization_fk':{1:-321201,2:None},'organization_in_facility_fk':{1:None,2:-321101},
                     'duplicate_capacity_public_id':{0:fac[0]},'partial_provenance':{4:-321001},
                     'wrong_source_fk':{4:-999999999,5:-321001,6:-321001},
                     'mismatched_evidence':{1:-321101,2:None,4:-321001,5:-321002,6:-321002},
                     'observation_public_id_as_capacity':{0:OBS['public_id']}}
            rejections={}
            for name,changes in updates.items():
                values=list(fac);values[0]='m4-invalid:'+name
                for index,value in changes.items():values[index]=value
                rejections[name]=m3.rejected(cur,insert,values,E['sql_rejections'][name])
            cur.execute('SELECT count(*) AS n FROM cmpe.supply_capacity_21 WHERE facility_id=-321202')
            assert cur.fetchone()['n']==E['observation_only_capacity_rows']
    return {'capacities':len(capacities),'observations':len(observations),'sql_rejections':rejections,
            'real_capacity_witnesses':0,'negative_explicit_keys_preserve_sequences':True}


def cleanup(url):
    with psycopg.connect(url) as conn:
        with conn.cursor() as cur:
            cur.execute('DROP TABLE cmpe.supply_capacity_21');cur.execute('DROP FUNCTION cmpe.check_supply_capacity_21()')
            for table,key in [('observation_result','observation_result_id'),('evidence_support','evidence_support_id'),
                              ('assertion','assertion_id'),('source_record','source_record_id'),('dataset_release','dataset_release_id'),
                              ('dataset','dataset_id'),('facility','facility_id'),('organization','organization_id'),
                              ('transformation_run','transformation_run_id')]:
                cur.execute(f'DELETE FROM cmpe.{table} WHERE {key} BETWEEN -321300 AND -321001')


def read_rows(url,query):
    with psycopg.connect(url,row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute('SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY')
            cur.execute(query);return [dict(r) for r in cur.fetchall()]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--database-url',default=os.getenv('DATABASE_URL','postgresql://postgres:postgres@localhost:5432/cmpe'))
    ap.add_argument('--output-dir',default='build/v2-21-rdb-m4');ap.add_argument('--offline',action='store_true');args=ap.parse_args()
    out=ROOT/args.output_dir;out.mkdir(parents=True,exist_ok=True)
    config=json.loads((HERE/'scope.json').read_text());m1.pin_inputs(config)
    report={'schema_version':1,'passed':False,'requirements':['FR-14','FR-15'],'model_commit':config['model_commit'],
            'oracle_commit':'e750774db38c9946c9d3abdb4c801c88df271301','database_executed':not args.offline,
            'software':{'python':platform.python_version(),'psycopg':psycopg.__version__,'rdflib':__import__('rdflib').__version__,
                        'pyshacl':__import__('pyshacl').__version__,'owlready2':__import__('owlready2').VERSION},
            'boundary':'Synthetic copied-W6 capacity/measurement prototype only. No Mode from a measurement, no real capacity witness, no universal bearer-capacity existence or full 2.1 scientific/GA acceptance.'}
    if args.offline:
        report['rdf']=rdf_checks(*example_rows(),out,config);report['scope']='OFFLINE_RDF_ONLY_NO_POSTGRESQL_CLAIM'
    else:
        before=m1.database_snapshot(args.database_url);seq_before=m3.sequences(args.database_url)
        legacy_before=m1.run_legacy(args.database_url,out/'before')
        original_observations=read_rows(args.database_url,OBS_SQL)
        assert not original_observations,'M4 needs the isolated baseline fixture with no capacity observation'
        seeded=False
        try:
            report['sql']=seed(args.database_url);seeded=True
            report['legacy_during']=m1.run_legacy(args.database_url,out/'during')
            validation=out/'during/w6-validation.json'
            subprocess.run([sys.executable,str(ROOT/'tools/v2_data/validate_w6.py'),'--database-url',args.database_url,
                            '--kg',str(out/'during/legacy.ttl'),'--report',str(validation)],cwd=ROOT,check=True,capture_output=True,text=True)
            v=json.loads(validation.read_text());assert v['passed'] and v['shacl_conforms']
            capacities=read_rows(args.database_url,CAP_SQL);observations=read_rows(args.database_url,OBS_SQL)
            report['rdf']=rdf_checks(capacities,observations,out,config)
            for key,rows,columns,result in [('q21_04',capacities,CAP_COLUMNS,'capacity_rows'),('q21_05',observations,OBS_COLUMNS,'observation_rows')]:
                normalized=m1.normalize_rows(rows,columns);rdf_rows=report['rdf'][result]
                assert normalized==rdf_rows,(key,normalized,rdf_rows)
                report[key]={'passed':True,'rows':len(normalized),'sql_normalized_sha256':m1.sha(m1.compact(normalized)),
                             'sparql_normalized_sha256':m1.sha(m1.compact(rdf_rows))}
            report['w6_during_validation']={'passed':v['passed'],'shacl_conforms':v['shacl_conforms']}
        finally:
            if seeded:cleanup(args.database_url)
        after=m1.database_snapshot(args.database_url);seq_after=m3.sequences(args.database_url)
        legacy_after=m1.run_legacy(args.database_url,out/'after')
        assert before==after and seq_before==seq_after and legacy_before==legacy_after
        assert read_rows(args.database_url,OBS_SQL)==original_observations
        report.update({'database_before':before,'database_after':after,'sequences_unchanged':True,
                       'legacy_before':legacy_before,'legacy_after':legacy_after,'rollback_restored':True,
                       'legacy_observation_rows_restored':True,'scope':'COPIED_POSTGRESQL_POSTGIS_M4_ONLY'})
    report['passed']=True
    (out/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True,default=str)+'\n')
    print(json.dumps({'passed':True,'scope':report['scope'],'q21_04':report.get('q21_04'),'q21_05':report.get('q21_05'),
                      'shacl':report['rdf']['shacl']['all_expected_met'],'owl':report['rdf']['owl']['all_expected_met']},indent=2))


if __name__=='__main__':main()
