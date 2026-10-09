"""Audit review-package traceability and recompute baseline topology; no semantic certification."""
import json, hashlib
from pathlib import Path
from collections import Counter
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BASE=ROOT/'v2/ontology/candidates/2.1.0-alpha.1-g3-p4a-supply-capacity'
d=json.loads((HERE/'domain-dossier.json').read_text())
p=json.loads((HERE/'continuation-plan.json').read_text())
es=json.loads((BASE/'ontouml.json').read_text())['elements']; by={e['id']:e for e in es}
classes={e['id'] for e in es if e['type']=='Class' and e.get('stereotype')!='datatype'}
assert len(classes)==138
adj={x:set() for x in classes}; typed=0
for e in es:
    pair=[]
    if e['type']=='Generalization':pair=[e['general'],e['specific']]
    if e['type']=='BinaryRelation':
        pair=[by[k].get('propertyType') for k in e['properties']]
        if all(x in classes for x in pair):typed+=1
    if len(pair)==2 and all(x in classes for x in pair):
        a,b=pair;adj[a].add(b);adj[b].add(a)
isolates=sorted(x for x,ns in adj.items() if not ns)
remaining=set(classes); components=[]
while remaining:
    todo=[remaining.pop()]; seen=set(todo)
    while todo:
        x=todo.pop()
        for y in adj[x]-seen:seen.add(y);remaining.discard(y);todo.append(y)
    components.append(seen)
all_existing=[];reqs=[];cqs=[];scenarios=[];rels=[];proposed=[];source_ids={s['id'] for s in d['sources']}
module_counts=[]
for m in d['modules']:
    existing=m['retained_existing_ids']; assert all(x in classes for x in existing)
    interface_vocabulary={e['id'] for e in es if e['type']=='Class'}
    assert all(x in interface_vocabulary for x in m['interfaces']), (m['id'],set(m['interfaces'])-interface_vocabulary)
    assert set(m['source_ids'])<=source_ids
    qids={q['id'] for q in m['competency_questions']}
    rids={r['id'] for r in m['requirements']}
    for r in m['requirements']:
        assert set(r['competency_questions'])<=qids
        assert r['positive_witness'] and r['negative_or_boundary_witness'],r['id']
        assert r['test_result']=='NOT_EXECUTED'
    for s in m['scenarios']:assert set(s['requirement_ids'])<=rids
    assert {s['kind'] for s in m['scenarios']}=={'positive','boundary','negative','non_entailment'}
    assert not ({x['id'] for x in m['proposed_concepts']} & classes)
    all_existing+=existing;reqs+=m['requirements'];cqs+=m['competency_questions'];scenarios+=m['scenarios'];rels+=m['relation_designs'];proposed+=m['proposed_concepts']
    module_counts.append({'domain':m['name'],'existing':len(existing),'isolates':sorted(set(existing)&set(isolates)),'candidate_slots':len(existing)+len(m['proposed_concepts']),'proposed_new_slots':len(m['proposed_concepts'])})
for collection in [reqs,cqs,scenarios,rels,proposed]:assert len({x['id'] for x in collection})==len(collection)
assert len(set(all_existing))==12
expected=['N01','N02','N03','N04','N05','N06','N07','N08','N09','P3','P4','P5d','P5c','P5e','P6a','P6b','P6c','P6d','N10','P7','G4','G5a','G5b']
assert [x['id'] for x in p['tasks']]==expected
assert p['user_decision']['status']=='CONFIRMED_USER_DIRECTION'
assert len(reqs)==24 and len(cqs)==12 and len(scenarios)==16
assert len(isolates)==13 and len(components)==14 and max(map(len,components))==125
result={'status':'PASS_PACKAGE_INTEGRITY_AND_BASELINE_TOPOLOGY_ONLY','semantic_tests_run':False,'as_of':'2026-10-09','baseline_commit':d['baseline_commit'],'baseline_sha256':{x:hashlib.sha256((BASE/x).read_bytes()).hexdigest() for x in ['ontouml.json','active.ttl','constraints.ttl']},'native_elements':len(es),'native_types':dict(Counter(e['type'] for e in es)),'named_classes':len(classes),'fully_typed_named_class_relations':typed,'undirected_unique_edges':sum(map(len,adj.values()))//2,'components':len(components),'largest_component':max(map(len,components)),'isolates':isolates,'module_counts':module_counts,'requirements':len(reqs),'competency_questions':len(cqs),'designed_scenarios':len(scenarios),'proposed_relation_designs':len(rels),'proposed_new_concept_slots':len(proposed),'preserved_work_items':len(p['tasks']),'source_records':len(d['sources']),'limits':['No official OntoUML detector or reasoner rerun in this documentation turn.','Scenario designs have not executed.','Candidate concept counts are not accepted ontology changes.','Source-informed proposed requirements are not universal regulatory requirements.']}
(HERE/'audit-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
