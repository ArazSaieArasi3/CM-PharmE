#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Execute the pre-frozen synthetic M1 oracles and bounded formal checks."""
import argparse
import contextlib
import hashlib
import importlib.metadata
import io
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import owlready2
from owlready2.base import OwlReadyInconsistentOntologyError
from rdflib import Graph, OWL, RDF, URIRef
from rdflib.compare import isomorphic

import profile as m1


def roundtrip(graph):
    for fmt in ['turtle','xml','json-ld','nt']:
        reparsed=Graph().parse(data=graph.serialize(format=fmt),format=fmt)
        m1.require(isomorphic(graph,reparsed),'RDF roundtrip differs: '+fmt)


def normalized_rows(data):
    query=(m1.HERE/'query.rq').read_text()
    rows=[]
    for row in data.query(query):
        rows.append([None if value is None else str(value) for value in row])
    return sorted(rows,key=lambda x:json.dumps(x))


def standalone_admission():
    files=['profile.py','profile.ttl','shapes.ttl','query.rq']
    stages={}
    with tempfile.TemporaryDirectory(prefix='cmpe-m1-standalone-') as folder:
        target=Path(folder)
        for name in files:shutil.copyfile(m1.HERE/name,target/name)
        for fixture,expected_code,expected_stage in [('with-run',0,'ADMITTED'),('missing-record-key',1,'SHACL_REJECTED')]:
            path=target/(fixture+'.ttl');shutil.copyfile(m1.HERE/'fixtures'/path.name,path)
            run=subprocess.run([sys.executable,str(target/'profile.py'),'admit',str(path)],
                               cwd=target,capture_output=True,text=True,timeout=60)
            m1.require(run.returncode==expected_code,'Standalone CLI exit differs: '+run.stdout+run.stderr)
            result=json.loads(run.stdout)
            m1.require(result['stage']==expected_stage,'Standalone admission differs')
            stages[fixture]=result['stage']
    return dict(copied_runtime_files=files,stages=stages,historical_source_or_repository_files_copied=False,
                database_or_java_required_for_admission=False,pass_result=True)


def formal(profile,oracles,out):
    rows=[]
    for oracle in oracles['reasoner_cases']:
        name=oracle['id'];graph=profile+Graph()
        if name=='with-run':graph+=Graph().parse(m1.HERE/'fixtures/with-run.ttl')
        elif name=='missing-record-key-open-world':graph+=Graph().parse(m1.HERE/'fixtures/missing-record-key.ttl')
        elif name=='cross-kind-alias-not-global-owl-disjointness':graph+=Graph().parse(m1.HERE/'fixtures/cross-kind-alias.ttl')
        elif name=='explicit-owl-nothing-control':graph.add((URIRef('https://example.org/inconsistent-control'),RDF.type,OWL.Nothing))
        before=graph
        graph,excluded=m1.logical_view(before)
        m1.require(set(before)-set(graph)==set(excluded) and all(p==RDF.value for _,p,_ in excluded),
                   'Undeclared logical-view information loss')
        path=out/(name+'.rdf');graph.serialize(path,format='xml')
        world=owlready2.World();capture=io.StringIO()
        try:
            world.get_ontology(path.resolve().as_uri()).load()
            with contextlib.redirect_stderr(capture):
                owlready2.sync_reasoner(world,debug=1)
            consistent=True
            unsat=sorted(x.iri for x in world.inconsistent_classes() if x.iri!=str(OWL.Nothing))
        except OwlReadyInconsistentOntologyError:
            consistent=False;unsat=[]
        finally:
            world.close()
        (out/(name+'.log')).write_text(capture.getvalue())
        m1.require(consistent==oracle['expected_consistent'] and not unsat,'HermiT oracle failed: '+name)
        rows.append(dict(id=name,expected_consistent=oracle['expected_consistent'],actual_consistent=consistent,
                         unsatisfiable_named_classes=unsat,input_canonical_sha256=hashlib.sha256(m1.canonical(graph)).hexdigest(),
                         rdf_value_rows_excluded_from_owl_view=len(excluded),full_rdf_input_changed=False,pass_result=True))
    # Check the serialization/profile explicitly; logical consistency alone does not prove OWL 2 DL.
    helper=m1.ROOT/'tools/v2_ontology/CheckOWL2DL.java'
    jars=sorted((Path(owlready2.__path__[0])/'pellet').glob('*.jar'))
    checked=[]
    for name in ['schema-only','with-run']:
        command=['java','-cp',':'.join(map(str,jars)),str(helper),str(out/(name+'.rdf'))]
        run=subprocess.run(command,capture_output=True,text=True,timeout=90)
        (out/(name+'-owlapi-profile.txt')).write_text(run.stdout+'\n'+run.stderr)
        m1.require(run.returncode==0 and all(x in run.stdout for x in ['IN_OWL2_DL=true','CONSISTENT=true','UNSAT_CLASSES=0']),
                   'OWLAPI/Pellet profile check failed: '+run.stdout+run.stderr)
        checked.append(name)
    return rows,dict(engine='OWLAPI 3.4.3 / Pellet bundled with Owlready2 0.49',in_owl2_dl=True,
                     checked_views=checked,consistent=True,unsatisfiable_named_classes=0,helper_sha256=m1.sha(helper),
                     raw_rdf_export_dl_conformance_claimed=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,default=m1.ROOT/'build/m1-provenance-profile')
    args=parser.parse_args();out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    contract=m1.frozen();oracles=json.loads((m1.HERE/'fixed-oracles.json').read_text())
    versions={k:importlib.metadata.version(k) for k in contract['direct_python_dependencies']}
    m1.require(versions==contract['direct_python_dependencies'],'Dependency versions differ')
    profile=Graph().parse(m1.HERE/'profile.ttl');shapes=Graph().parse(m1.HERE/'shapes.ttl')
    m1.require(isomorphic(profile,m1.build_schema(contract)),'Committed schema differs from exact selected source')
    m1.require(isomorphic(shapes,m1.build_shapes()),'Committed shapes differ from the declared build')
    manifest=json.loads((m1.HERE/'manifest.json').read_text())
    for name,expected in manifest['artifacts_sha256'].items():
        m1.require(m1.sha(m1.HERE/name)==expected,'Artifact manifest drift: '+name)
    roundtrip(profile);roundtrip(shapes)
    cases=[]
    for oracle in oracles['cases']:
        data=Graph().parse(m1.HERE/oracle['fixture']);before=m1.canonical(data)
        result=m1.admit(data,profile,shapes)
        m1.require(result['stage']==oracle['expected_stage'],'Admission stage differs: '+oracle['id']+' '+json.dumps(result))
        m1.require(result['shacl_conforms']==oracle['expected_shacl_conforms'],'SHACL oracle differs: '+oracle['id'])
        rows=None
        if result['admitted']:
            rows=normalized_rows(data)
            m1.require(len(rows)==oracle['expected_query_rows'] and rows==oracle['expected_query_tuples'],
                       'Frozen query tuples differ: '+oracle['id'])
            m1.require(all(result['explicit_target_union_counts'][n]>0 for n in m1.CLASSES[:3]),'Vacuous admitted scope')
        m1.require(before==m1.canonical(data),'Validation mutated fixture: '+oracle['id'])
        roundtrip(data)
        cases.append(dict(id=oracle['id'],expected_stage=oracle['expected_stage'],**result,
                          query_tuples=rows,roundtrip_formats=4,pass_result=True))
    m1.require(len(cases)==oracles['case_count']==24,'Missing oracle case')
    # Two guards against the original isolation/zero-target failure classes.
    controls=[]
    broken=shapes+Graph();broken.remove((m1.S.SourceRecordShape,m1.SH.targetClass,None))
    try:m1.audit_shapes(broken)
    except ValueError:controls.append(dict(id='target-removal',refused=True))
    else:raise ValueError('Missing target accepted')
    broken=profile+Graph();broken.add((URIRef(str(m1.S)),OWL.imports,URIRef('https://example.org/whole-experimental-ontology')))
    try:m1.audit_schema(broken)
    except ValueError:controls.append(dict(id='implicit-full-source-import',refused=True))
    else:raise ValueError('Implicit import accepted')
    print(json.dumps(dict(admission_cases=len(cases),admitted=sum(x['admitted'] for x in cases),guards=len(controls))),flush=True)
    portable=standalone_admission()
    formal_dir=out/'formal';formal_dir.mkdir(exist_ok=True)
    hermit,owlapi=formal(profile,oracles,formal_dir)
    m1.frozen()
    report=dict(schema_version='CMPE-M1ProvenanceResults/0.1.0',passed=True,
                contract_freeze_commit=m1.FREEZE_COMMIT,contract_sha256=m1.sha(m1.HERE/'contract.json'),
                oracle_sha256=m1.sha(m1.HERE/'fixed-oracles.json'),manifest=manifest,
                python_versions=versions,java=subprocess.run(['java','-version'],capture_output=True,text=True).stderr,
                admission_cases=cases,guard_controls=controls,hermit_cases=hermit,owlapi_profile=owlapi,
                standalone_admission=portable,
                profile_roundtrip_formats=4,fixture_roundtrips=len(cases)*4,
                copied_database_executed=False,old_m1_modified=False,
                full_native_validation_claimed=False,ga_ready=False,
                boundary='Isolated six-term profile on pre-frozen synthetic witnesses; local admission is not universal OWL cardinality or complete source/identifier semantics. Copied-W6 integration remains a separate packet.')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,admission_cases=len(cases),hermit_cases=len(hermit),owl2_dl=True,
                          guard_controls=len(controls),copied_database_executed=False,ga_ready=False)),flush=True)


if __name__=='__main__':main()
