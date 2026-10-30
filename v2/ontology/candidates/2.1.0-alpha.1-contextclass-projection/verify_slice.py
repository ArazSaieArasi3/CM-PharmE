#!/usr/bin/env python3
"""Bounded ContextClass projection candidate; original evidence never rewritten."""
import argparse,copy,hashlib,importlib.util,importlib.metadata,json,subprocess,sys,tempfile
from pathlib import Path
from rdflib import Graph,Namespace,RDF,RDFS,OWL,Literal,BNode,XSD
from pyshacl import validate
from owlready2 import World,sync_reasoner
from owlready2.base import OwlReadyInconsistentOntologyError
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];CAND=HERE.parent
CONTRACT_SHA='4b29818efad75f46ba300c450b36dff5d197271fdebac2ca605ab6393e372ffe'
ORACLE_SHA='5ba8c32d1605455387e6f910b55ed977a4f8ebbd0d0c18f873de4b369f69b988'
FREEZE='be6dd2c67ff2bb33071813a4360790f83d4f5efe'
contract=json.loads((HERE/'contract.json').read_text());oracles=json.loads((HERE/'fixed-oracles.json').read_text())
sys.path.insert(0,str(CAND/'2.1.0-alpha.1-derived-participant-lab'))
import run_semantics as legacy
import run_temporal as temporal
from native_specialization import audit
legacy.RELATIONS={k:v for k,v in legacy.RELATIONS.items() if k!='evidenceRecord'}
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
    require(native['restored_unknown_readonly']==78 and native['guarded_roundtrip_equal'],'Boolean/nature fidelity drift')
    rows=[row for row in audit(model)['rows'] if row['relation'] in {'rel-contextClassificationEntry','rel-contextClassificationProduct'}]
    require(len(rows)==4 and all(row['overall']=='PASS' for row in rows),'Scoped subsetting failed')
    trials=[]
    for name in oracles['expected_native_refusals']:
        altered=copy.deepcopy(model);d={e['id']:e for e in altered['elements']}
        if name=='projection-turned-primitive':d['rel-contextClassificationProduct']['stereotype']='mediation'
        elif name=='specialization-dropped':d['end-contextClassificationEntry-target']['subsettedProperties']=[]
        elif name=='unrelated-unknown-defaulted':d['end-evidenceRecord-target']['isReadOnly']=False
        elif name=='element-dropped':altered['elements'].pop()
        elif name=='nature-changed':d['ContextualMedicineClassificationAssignment']['restrictedTo']=['functional-complex']
        elif name=='primitive-identity-reverted':d['end-classificationEntity-target']['isReadOnly']=False
        try:check_delta(base,altered)
        except ValueError as error:trials.append(dict(id=name,refused=True,reason=str(error)))
        else:raise ValueError('Unauthorized native delta admitted: '+name)
    props=[e for e in model['elements'] if e['type']=='Property']
    inv=dict(elements=len(model['elements']),properties=len(props),unknown_readonly=sum(e.get('isReadOnly') is None for e in props),unknown_cardinality=sum(e.get('cardinality') is None for e in props),untyped_properties=sum(e.get('propertyType') is None for e in props),specialized_properties=sum(bool(e.get('subsettedProperties') or e.get('redefinedProperties')) for e in props))
    require(inv==contract['expected_inventory'],'Candidate inventory mismatch')
    return dict(schema_serialization=native,subsetting_rows=rows,refusal_cases=trials,inventory=inv,permitted_field_changes=len(contract['patch']),candidate_sha256=sha(snapshot))


def fixture(name):
    g=legacy.classification(substance=name=='context-substance',context=name not in {'generic-product','generic-stale-shortcut'})
    if name=='unqualified-product':g.remove((T.entity,RDF.type,C.ClassifiedMedicinalProductRole))
    elif name=='missing-entry':g.remove((T.assignment,C.classificationEntry,T.entry))
    elif name=='stale-product':
        legacy.types(g,'other','ClassifiedEntity','ClassifiedMedicinalProductRole','MedicinalProduct');g.add((T.assignment,C.contextClassificationProduct,T.other))
    elif name=='shortcut-without-parent':g.remove((T.assignment,C.classificationEntity,T.entity));g.add((T.assignment,C.contextClassificationProduct,T.entity))
    elif name=='context-subclass':g.remove((T.assignment,RDF.type,C.ContextualMedicineClassificationAssignment));g.add((T.assignment,RDF.type,C.EssentialMedicineClassification))
    elif name=='generic-stale-shortcut':g.add((T.assignment,C.contextClassificationProduct,T.entity))
    elif name=='two-distinct-products':
        legacy.types(g,'other','ClassifiedEntity','ClassifiedMedicinalProductRole','MedicinalProduct');g.add((T.assignment,C.classificationEntity,T.other));g.add((T.entity,OWL.differentFrom,T.other))
    elif name=='unqualified-entry':g.remove((T.entry,RDF.type,C.AppliedClassificationEntryRole))
    return g


def check_shacl(out):
    shapes=legacy.base_shapes+legacy.shapes('C');delta=legacy.restrictions('C');shapes.serialize(out/'shapes.ttl',format='turtle');delta.serialize(out/'owl-delta.ttl',format='turtle')
    rows=[]
    for oracle in oracles['shacl_cases']:
        g=fixture(oracle['id']);data=legacy.materialize(g) if oracle['materialize'] else g+Graph()
        count=sum(1 for _,p,_ in data if p in {C.contextClassificationEntry,C.contextClassificationProduct})
        ok,report,_=validate(data+legacy.hierarchy,shacl_graph=shapes,inference='none',advanced=True)
        require(bool(ok)==oracle['expected_conforms'] and count==oracle['expected_projection_edges'],('SHACL oracle',oracle['id'],bool(ok),count))
        g.serialize(out/(oracle['id']+'.ttl'),format='turtle')
        rows.append(dict(id=oracle['id'],expected_conforms=oracle['expected_conforms'],actual_conforms=bool(ok),projection_edges=count,pass_result=True))
    return rows,shapes,delta


def regression(shapes):
    rows=[]
    for folder,filename in [('2.1.0-alpha.1-four-domain-lab','shacl-results.json'),('2.1.0-alpha.1-four-domain-refinement','refinement-shacl-results.json'),('2.1.0-alpha.1-content-event-policy','shacl-results.json')]:
        prior=json.loads((CAND/folder/filename).read_text());prior=prior['cases'] if isinstance(prior,dict) else prior
        for case in prior:
            data=Graph().parse(CAND/folder/case['fixture'])
            before,_,_=validate(data+legacy.hierarchy,shacl_graph=legacy.base_shapes,inference='none',advanced=True)
            projected=legacy.materialize(data)
            after,report,_=validate(projected+legacy.hierarchy,shacl_graph=shapes,inference='none',advanced=True)
            marker=case.get('expected_failure_marker',case.get('expected_marker'))
            details=[str(report.value(z,SH.resultPath) or '')+' '+str(report.value(z,SH.sourceConstraint) or '') for z in report.subjects(RDF.type,SH.ValidationResult)]
            ok=bool(before)==case['expected_conforms'] and bool(after)==case['expected_conforms'] and (marker is None or any(marker in s for s in details))
            require(ok,('Historical expectation changed',case['name'],before,after,marker,details))
            added=set(projected)-set(data);require(not any(p==C.evidenceRecord for _,p,_ in added),'EvidenceRecord was materialized')
            rows.append(dict(id=folder+'/'+case['name'],expected_conforms=case['expected_conforms'],baseline_conforms=bool(before),candidate_conforms=bool(after),marker=marker,pass_result=True,triples_added=len(added)))
    require(len(rows)==oracles['historical_shacl_rows'],'Historical row count');return rows


def reason(delta,out):
    rows=[]
    for oracle in oracles['hermit_cases']:
        name=oracle['id'];g=Graph()
        if name in {'missing-data-open-world','explicit-zero-required-entry'}:
            legacy.types(g,'assignment','ContextualMedicineClassificationAssignment')
            if name=='explicit-zero-required-entry':
                b=BNode();g.add((T.assignment,RDF.type,b));g.add((b,RDF.type,OWL.Restriction));g.add((b,OWL.onProperty,C.contextClassificationEntry));g.add((b,OWL.maxCardinality,Literal(0,datatype=XSD.nonNegativeInteger)))
        else:
            g=legacy.materialize(legacy.classification());legacy.types(g,'other','MedicinalProduct','ClassifiedMedicinalProductRole');g.add((T.assignment,C.contextClassificationProduct,T.other))
            if name=='two-explicitly-distinct-products':g.add((T.entity,OWL.differentFrom,T.other))
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'model.rdf';(legacy.ont+g+delta).serialize(p,format='xml');w=World();w.get_ontology(p.as_uri()).load()
            try:sync_reasoner(w,debug=0);consistent=True;unsat=[x.iri for x in w.inconsistent_classes() if x.iri!=str(OWL.Nothing)]
            except OwlReadyInconsistentOntologyError:consistent=False;unsat=[]
            finally:w.close()
        require(consistent==oracle['expected_consistent'] and not unsat,('HermiT oracle',name,consistent,unsat))
        rows.append(dict(id=name,expected_consistent=oracle['expected_consistent'],actual_consistent=consistent,unsatisfiable_named_classes=unsat,pass_result=True))
    return rows


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--node-modules',required=True,type=Path);ap.add_argument('--output-dir',default='build/contextclass-projection');args=ap.parse_args();out=ROOT/args.output_dir;out.mkdir(parents=True,exist_ok=True)
    frozen();versions={name:importlib.metadata.version(name) for name in contract['python_versions']};require(versions==contract['python_versions'],'Python dependency version drift')
    base=json.loads((ROOT/contract['baseline_path']).read_text());model=build_candidate(base)
    native=native_checks(base,model,args.node_modules.resolve(),out)
    require(sha(HERE/'ontouml.json')==native['candidate_sha256'],'Committed candidate differs from generated delta')
    cases,shapes,delta=check_shacl(out);print(json.dumps(dict(native=True,shacl=len(cases))),flush=True)
    history=regression(shapes);print(json.dumps(dict(historical=len(history))),flush=True)
    traces=[]
    for oracle in oracles['temporal_cases']:
        actual=temporal.inspect(oracle['input']);require(actual==oracle['expected'],('Temporal oracle',oracle['id'],actual));traces.append(dict(id=oracle['id'],expected=oracle['expected'],actual=actual,pass_result=True))
    rr=reason(delta,out);frozen()
    report=dict(schema_version=1,profile=contract['profile'],oracle_freeze_commit=FREEZE,contract_sha256=CONTRACT_SHA,oracle_sha256=ORACLE_SHA,passed=True,baseline_sha256=contract['baseline_sha256'],python_dependencies=versions,committed_candidate_matches_generated=True,native=native,shacl_cases=cases,historical_shacl_rows=history,temporal_cases=traces,hermit_cases=rr,historical_inputs_unchanged=True,evidenceRecord_migration_included=False,full_antipattern_execution=False,independent_scientific_acceptance=False,claim_boundary='Two ContextClass typed projections and explicit assignment-identity policy in a separate native candidate; closed-world/OWL/temporal checks are bounded; all historical packages and the P3 baseline remain unchanged.')
    (out/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(passed=True,shacl=len(cases),historical=len(history),temporal=len(traces),hermit=len(rr),native_refusals=len(native['refusal_cases']),inventory=native['inventory'])),flush=True)


if __name__=='__main__':main()
