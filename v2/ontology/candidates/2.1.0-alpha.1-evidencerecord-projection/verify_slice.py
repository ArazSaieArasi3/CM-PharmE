#!/usr/bin/env python3
"""Bounded EvidenceRecord projection candidate; original evidence never rewritten."""
import argparse,copy,hashlib,importlib.util,importlib.metadata,json,subprocess,sys,tempfile
from pathlib import Path
from rdflib import Graph,Namespace,RDF,RDFS,OWL,Literal,BNode,XSD
from pyshacl import validate
from owlready2 import World,sync_reasoner
from owlready2.base import OwlReadyInconsistentOntologyError
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];CAND=HERE.parent
CONTRACT_SHA='b35bc67d504418dc283c848d5ed5512c21f924e6541933abf2389cd9c44fa9bc'
ORACLE_SHA='b00e554ba35c80f6c022f6f83650c76436775501defb3de982d3111b6ecedf04'
FREEZE='799cb885a9bb0a65c4d8aad5601b328c91d73a07'
contract=json.loads((HERE/'contract.json').read_text());oracles=json.loads((HERE/'fixed-oracles.json').read_text())
sys.path.insert(0,str(CAND/'2.1.0-alpha.1-derived-participant-lab'))
import run_semantics as legacy
import run_temporal as temporal
from native_specialization import audit
spec=importlib.util.spec_from_file_location('contextclass_predecessor',CAND/'2.1.0-alpha.1-contextclass-projection/verify_slice.py')
predecessor=importlib.util.module_from_spec(spec);spec.loader.exec_module(predecessor)
from build_lab import RELATIONS as ALL_RELATIONS
legacy.RELATIONS=dict(ALL_RELATIONS)
C=legacy.C;T=legacy.T;SH=legacy.SH


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'))
def require(ok,why):
    if not ok:raise ValueError(why)
def frozen():
    require(sha(HERE/'contract.json')==CONTRACT_SHA,'Contract drift');require(sha(HERE/'fixed-oracles.json')==ORACLE_SHA,'Oracle drift')
    for p,d in contract['historical_inputs_sha256'].items():require(sha(ROOT/p)==d,'Historical input drift: '+p)


def build_candidate(base):
    model=copy.deepcopy(base);by={e['id']:e for e in model['elements']}
    for row in contract['patch']:
        require(by[row['id']].get(row['field'])==row['before'],'Patch precondition')
        by[row['id']][row['field']]=row['after']
    return model


def check_delta(base,model):
    require([e['id'] for e in base['elements']]==[e['id'] for e in model['elements']],'Unauthorized native delta')
    expected=build_candidate(base);require(canonical(model)==canonical(expected),'Unauthorized native delta')


def native_checks(base,model,modules,out):
    check_delta(base,model);snapshot=out/'ontouml.json';snapshot.write_text(json.dumps(model,indent=2)+'\n')
    p=subprocess.run(['node',str(HERE/'check_native.cjs'),str(snapshot),str(modules),str(out/'native.json')],capture_output=True,text=True,timeout=90)
    require(p.returncode==0,p.stdout+p.stderr);native=json.loads((out/'native.json').read_text());require(native['versions']==contract['node_versions'],'Node dependency version drift')
    require(native['restored_unknown_readonly']==76 and native['guarded_roundtrip_equal'],'Boolean/nature fidelity drift')
    rows=[row for row in audit(model)['rows'] if row['relation'] in {'rel-evidenceRecord'}]
    require(len(rows)==2 and all(row['overall']=='PASS' for row in rows),'Scoped subsetting failed')
    trials=[]
    for name in oracles['expected_native_refusals']:
        altered=copy.deepcopy(model);d={e['id']:e for e in altered['elements']}
        if name=='projection-turned-primitive':d['rel-evidenceRecord']['stereotype']='mediation'
        elif name=='specialization-dropped':d['end-evidenceRecord-target']['subsettedProperties']=[]
        elif name=='unrelated-unknown-defaulted':d['end-contextClassificationJurisdiction-target']['isReadOnly']=False
        elif name=='element-dropped':altered['elements'].pop()
        elif name=='nature-changed':d['EvidenceSupport']['restrictedTo']=['functional-complex']
        elif name=='primitive-identity-reverted':d['end-evidenceItem-target']['isReadOnly']=False
        try:check_delta(base,altered)
        except ValueError as error:trials.append(dict(id=name,refused=True,reason=str(error)))
        else:raise ValueError('Unauthorized native delta admitted: '+name)
    props=[e for e in model['elements'] if e['type']=='Property']
    inv=dict(elements=len(model['elements']),properties=len(props),unknown_readonly=sum(e.get('isReadOnly') is None for e in props),unknown_cardinality=sum(e.get('cardinality') is None for e in props),untyped_properties=sum(e.get('propertyType') is None for e in props),specialized_properties=sum(bool(e.get('subsettedProperties') or e.get('redefinedProperties')) for e in props))
    require(inv==contract['expected_inventory'],'Candidate inventory mismatch')
    return dict(schema_serialization=native,subsetting_rows=rows,refusal_cases=trials,inventory=inv,permitted_field_changes=len(contract['patch']),candidate_sha256=sha(snapshot))


def project(g,names=None):
    out=g+Graph()
    for name,(parent,source,target) in legacy.RELATIONS.items():
        if names is not None and name not in names:continue
        for a,b in list(g.subject_objects(C[parent])):
            if legacy.instance(g,a,C[source]) and legacy.instance(g,b,C[target]):out.add((a,C[name],b))
    return out


def documented():return Graph().parse(ROOT/contract['contract_transition']['fixture'])


def fixture(name):
    g=documented() if name.startswith('documented-') else legacy.evidence(record=name!='nonrecord-evidence')
    if name=='unqualified-record':g.remove((T.item,RDF.type,C.EvidenceSourceRecordRole))
    elif name=='missing-primitive-item':g.remove((T.support,C.evidenceItem,T.item))
    elif name=='shortcut-without-parent':g.remove((T.support,C.evidenceItem,T.item));g.add((T.support,C.evidenceRecord,T.item))
    elif name in {'stale-record','two-record-items'}:
        legacy.types(g,'other','EvidenceItem','EvidenceSourceRecordRole','SourceRecord')
        g.add((T.support,C.evidenceRecord if name=='stale-record' else C.evidenceItem,T.other))
        g.add((T.item,OWL.differentFrom,T.other))
    elif name=='documented-primitive-missing':g.remove((None,C.evidenceItem,None))
    elif name=='documented-role-missing':g.remove((None,RDF.type,C.EvidenceSourceRecordRole))
    elif name=='documented-shortcut-only':
        for a,b in list(g.subject_objects(C.evidenceItem)):g.remove((a,C.evidenceItem,b));g.add((a,C.evidenceRecord,b))
    return g


def details(report):
    return [str(report.value(z,SH.resultPath) or '')+' '+str(report.value(z,SH.sourceConstraint) or '') for z in report.subjects(RDF.type,SH.ValidationResult)]


def check_shacl(out):
    shapes=legacy.base_shapes+legacy.shapes('C');delta=legacy.restrictions('C')
    # The inherited native primitive target is exactly one EvidenceItem. Make
    # this baseline commitment explicit in the bounded OWL projection too.
    for pred in [OWL.minQualifiedCardinality,OWL.maxQualifiedCardinality]:
        b=BNode();delta.add((C.EvidenceSupport,RDFS.subClassOf,b));delta.add((b,RDF.type,OWL.Restriction));delta.add((b,OWL.onProperty,C.evidenceItem));delta.add((b,OWL.onClass,C.EvidenceItem));delta.add((b,pred,Literal(1,datatype=XSD.nonNegativeInteger)))
    shapes.serialize(out/'shapes.ttl',format='turtle');delta.serialize(out/'owl-delta.ttl',format='turtle');rows=[]
    for oracle in oracles['shacl_cases']:
        g=fixture(oracle['id']);data=project(g) if oracle['materialize'] else g+Graph()
        count=sum(1 for _,p,_ in data if p in {C.contextClassificationEntry,C.contextClassificationProduct,C.evidenceRecord})
        ok,report,_=validate(data+legacy.hierarchy,shacl_graph=shapes,inference='none',advanced=True)
        require(bool(ok)==oracle['expected_conforms'] and count==oracle['expected_projection_edges'],('SHACL oracle',oracle['id'],bool(ok),count,details(report)))
        g.serialize(out/(oracle['id']+'.ttl'),format='turtle')
        rows.append(dict(id=oracle['id'],expected_conforms=oracle['expected_conforms'],actual_conforms=bool(ok),projection_edges=count,pass_result=True))
    return rows,shapes,delta


def contextclass_replay(shapes):
    rows=[]
    for oracle in predecessor.oracles['shacl_cases']:
        data=predecessor.fixture(oracle['id']);data=project(data) if oracle['materialize'] else data+Graph()
        count=sum(1 for _,p,_ in data if p in {C.contextClassificationEntry,C.contextClassificationProduct})
        ok,report,_=validate(data+legacy.hierarchy,shacl_graph=shapes,inference='none',advanced=True)
        require(bool(ok)==oracle['expected_conforms'] and count==oracle['expected_projection_edges'],('ContextClass changed',oracle['id']))
        rows.append(dict(id=oracle['id'],expected_conforms=oracle['expected_conforms'],actual_conforms=bool(ok),projection_edges=count,pass_result=True))
    require(len(rows)==oracles['expected_contextclass_shacl_rows'],'ContextClass count');return rows


def regression(shapes):
    all_rules=legacy.RELATIONS;legacy.RELATIONS={k:v for k,v in all_rules.items() if k!='evidenceRecord'}
    before_shapes=legacy.base_shapes+legacy.shapes('C');legacy.RELATIONS=all_rules
    rows=[];transitions=[]
    for folder,filename in [('2.1.0-alpha.1-four-domain-lab','shacl-results.json'),('2.1.0-alpha.1-four-domain-refinement','refinement-shacl-results.json'),('2.1.0-alpha.1-content-event-policy','shacl-results.json')]:
        prior=json.loads((CAND/folder/filename).read_text());prior=prior['cases'] if isinstance(prior,dict) else prior
        for case in prior:
            path=CAND/folder/case['fixture'];data=Graph().parse(path)
            previous=project(data,{'contextClassificationEntry','contextClassificationProduct'})
            before,b_report,_=validate(previous+legacy.hierarchy,shacl_graph=before_shapes,inference='none',advanced=True)
            projected=project(data);after,a_report,_=validate(projected+legacy.hierarchy,shacl_graph=shapes,inference='none',advanced=True)
            marker=case.get('expected_failure_marker',case.get('expected_marker'))
            baseline_pass=bool(before)==case['expected_conforms'] and (marker is None or any(marker in x for x in details(b_report)))
            is_transition=path.resolve()==(ROOT/contract['contract_transition']['fixture']).resolve()
            prospective_expected=contract['contract_transition']['prospective_expected'] if is_transition else case['expected_conforms']
            prospective_marker=None if is_transition else marker
            prospective_pass=bool(after)==prospective_expected and (prospective_marker is None or any(prospective_marker in x for x in details(a_report)))
            original_match=bool(after)==case['expected_conforms'] and (marker is None or any(marker in x for x in details(a_report)))
            require(baseline_pass and prospective_pass,('Witness contract failure',case['name'],before,after,is_transition,details(a_report)))
            if is_transition:
                require(case['expected_conforms']==contract['contract_transition']['historical_expected'] and not original_match,'Transition drift')
                transitions.append(dict(contract_id=contract['contract_transition']['id'],fixture=str(path.relative_to(ROOT)),historical_expected=case['expected_conforms'],prospective_expected=prospective_expected,actual=bool(after),triples_added=len(projected)-len(previous)))
            rows.append(dict(id=folder+'/'+case['name'],historical_expected=case['expected_conforms'],before_conforms=bool(before),before_pass=baseline_pass,after_conforms=bool(after),historical_oracle_matches=original_match,prospective_expected=prospective_expected,prospective_pass=prospective_pass,explicit_transition=is_transition,original_marker=marker,triples_added=len(projected)-len(previous)))
    require(len(rows)==oracles['historical_shacl_rows'] and sum(x['before_pass'] for x in rows)==oracles['expected_before_pass'],'Before count')
    require(sum(x['historical_oracle_matches'] for x in rows)==oracles['expected_original_after_matches'],'Original result changed')
    require(sum(x['prospective_pass'] for x in rows)==oracles['expected_prospective_pass'] and len(transitions)==oracles['expected_contract_transitions'],'Prospective count')
    return rows,transitions


def reason(delta,out):
    rows=[]
    for oracle in oracles['hermit_cases']:
        name=oracle['id'];g=Graph()
        if name in {'missing-data-open-world','explicit-zero-evidence-item'}:
            legacy.types(g,'support','EvidenceSupport')
            if name=='explicit-zero-evidence-item':
                b=BNode();g.add((T.support,RDF.type,b));g.add((b,RDF.type,OWL.Restriction));g.add((b,OWL.onProperty,C.evidenceItem));g.add((b,OWL.maxCardinality,Literal(0,datatype=XSD.nonNegativeInteger)))
        elif name=='nonrecord-item':g=project(legacy.evidence(record=False))
        elif name=='documented-primitive-suffices':g=project(documented())
        else:
            g=project(legacy.evidence());legacy.types(g,'other','EvidenceItem','EvidenceSourceRecordRole','SourceRecord');g.add((T.support,C.evidenceRecord,T.other))
            if name=='two-explicitly-distinct-records':g.add((T.item,OWL.differentFrom,T.other))
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'model.rdf';(legacy.ont+g+delta).serialize(p,format='xml');w=World();w.get_ontology(p.as_uri()).load()
            try:sync_reasoner(w,debug=0);consistent=True;unsat=[x.iri for x in w.inconsistent_classes() if x.iri!=str(OWL.Nothing)]
            except OwlReadyInconsistentOntologyError:consistent=False;unsat=[]
            finally:w.close()
        require(consistent==oracle['expected_consistent'] and not unsat,('HermiT oracle',name,consistent,unsat))
        rows.append(dict(id=name,expected_consistent=oracle['expected_consistent'],actual_consistent=consistent,unsatisfiable_named_classes=unsat,pass_result=True))
    return rows


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--node-modules',required=True,type=Path);ap.add_argument('--output-dir',default='build/evidencerecord-projection');args=ap.parse_args();out=ROOT/args.output_dir;out.mkdir(parents=True,exist_ok=True)
    frozen();versions={name:importlib.metadata.version(name) for name in contract['python_versions']};require(versions==contract['python_versions'],'Python dependency version drift')
    base=json.loads((ROOT/contract['baseline_path']).read_text());model=build_candidate(base)
    native=native_checks(base,model,args.node_modules.resolve(),out)
    require(sha(HERE/'ontouml.json')==native['candidate_sha256'],'Committed candidate differs from generated delta')
    cases,shapes,delta=check_shacl(out);print(json.dumps(dict(native=True,shacl=len(cases))),flush=True)
    context_rows=contextclass_replay(shapes);history,transitions=regression(shapes);print(json.dumps(dict(historical=len(history),original_after_matches=sum(x['historical_oracle_matches'] for x in history),prospective_pass=sum(x['prospective_pass'] for x in history))),flush=True)
    traces=[]
    for oracle in oracles['temporal_cases']:
        actual=temporal.inspect(oracle['input']);require(actual==oracle['expected'],('Temporal oracle',oracle['id'],actual));traces.append(dict(id=oracle['id'],expected=oracle['expected'],actual=actual,pass_result=True))
    rr=reason(delta,out);frozen()
    report=dict(schema_version=1,profile=contract['profile'],oracle_freeze_commit=FREEZE,contract_sha256=CONTRACT_SHA,oracle_sha256=ORACLE_SHA,passed=True,baseline_sha256=contract['baseline_sha256'],python_dependencies=versions,committed_candidate_matches_generated=True,native=native,shacl_cases=cases,historical_shacl_rows=history,contract_transitions=transitions,contextclass_shacl_rows=context_rows,temporal_cases=traces,hermit_cases=rr,historical_inputs_unchanged=True,evidenceRecord_migration_included=True,prospective_contract=contract['prospective_contract'],full_antipattern_execution=False,independent_scientific_acceptance=False,claim_boundary='EvidenceRecord typed projection and explicit support-identity policy on the ContextClass candidate; historical 88/89 comparison preserved, one prospective witness transition versioned; bounded checks only, no independent scientific acceptance or complete validator.')
    (out/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(passed=True,shacl=len(cases),historical=len(history),temporal=len(traces),hermit=len(rr),native_refusals=len(native['refusal_cases']),inventory=native['inventory'])),flush=True)


if __name__=='__main__':main()
