"""Compare exported admission contracts with the full experimental model.

Tests bounded fixture preservation, never arbitrary entailment preservation.
"""
from pathlib import Path
import importlib.util,json
from rdflib import Graph,RDF,Namespace
from pyshacl import validate
H=Path(__file__).resolve().parent;P=H.parent
s=importlib.util.spec_from_file_location('coh',P/'2.1.0-alpha.1-domain-coherence-lab/lab.py');lab=importlib.util.module_from_spec(s);s.loader.exec_module(lab)
delta=Graph().parse(H/'pv-group-delta.ttl');extra=Graph().parse(H/'pv-group-shapes.ttl');shapes=lab.shapes+extra
rows=[];positive=Graph();export_schema=Graph();export_shapes=Graph();export_hier=Graph()
for m in ['RM','PV','BA','DS']:
 d=H/'modules'/m;contract=json.loads((d/'contract.json').read_text());local=json.loads((d/'results.json').read_text());by={x['id']:x for x in local['admission']}
 export_schema+=Graph().parse(d/'ontology.ttl');export_shapes+=Graph().parse(d/'shapes.ttl');export_hier+=Graph().parse(d/'hierarchy.ttl')
 for case in contract['admission_cases']:
  g=Graph().parse(d/case['fixture']);ok,_,_=validate(g+lab.hierarchy,shacl_graph=shapes,advanced=True,inference='none')
  passed=bool(ok)==by[case['id']]['conforms']==case['expected']
  rows.append({'module':m,'id':case['id'],'full_conforms':bool(ok),'local_conforms':by[case['id']]['conforms'],'expected':case['expected'],'pass':passed})
  if case['expected']:positive+=g
 print(json.dumps({'module':m,'compared':len(contract['admission_cases']),'passed':sum(x['pass'] for x in rows if x['module']==m)}),flush=True)
ok,_,_=validate(positive+lab.hierarchy,shacl_graph=shapes,advanced=True,inference='none')
local_ok,_,_=validate(positive+export_hier,shacl_graph=export_shapes,advanced=True,inference='none')
full_logical=lab.ctx.prev.hermit(lab.full+delta+positive)
local_logical=lab.ctx.prev.hermit(export_schema+positive)
integrated={'positive_triples':len(positive),'full_admission':bool(ok),'export_union_admission':bool(local_ok),'full_reasoner':full_logical,'export_union_reasoner':local_logical}
integrated['pass']=bool(ok) and bool(local_ok) and all(r['consistent'] and not r['unsatisfiable_named_classes'] for r in [full_logical,local_logical])
(H/'integration-results.json').write_text(json.dumps({'fixture_comparisons':rows,'passed':sum(x['pass'] for x in rows),'total':len(rows),'integrated':integrated,'interpretation':'Only these fixtures compared. No claim of logical equivalence, formal locality, full OWL2 DL conformance or semantic acceptance.'},indent=2)+'\n')
positive.serialize(H/'combined-positive.ttl',format='turtle')
print(json.dumps(integrated),flush=True)
assert all(x['pass'] for x in rows) and integrated['pass']
