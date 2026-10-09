"""Check seven actual declared specialization pairs against the unchanged OWL graph.
Structural axiom alignment only: no new OWL consistency/entailment claim.
"""
import hashlib,json
from pathlib import Path
from rdflib import Graph,Namespace,RDFS
H=Path(__file__).resolve().parent
N=H.parent/'2.1.0-alpha.1-four-domain-refinement/ontouml-experimental.json'
O=N.with_name('experimental.owl.ttl')
m=json.loads(N.read_text());d={e['id']:e for e in m['elements']}
owners={p:r for r in d.values() if r['type']=='BinaryRelation' for p in r['properties']}
g=Graph().parse(O);C=Namespace('https://w3id.org/cm-pharme/2.1/');rows=[]
for r in d.values():
    if r['type']!='BinaryRelation' or not any(d[p].get('subsettedProperties') for p in r['properties']):continue
    targets=[d[p].get('subsettedProperties',[]) for p in r['properties']]
    assert all(len(v)==1 for v in targets)
    parent=owners[targets[0][0]];assert parent==owners[targets[1][0]]
    assert targets[0][0]==parent['properties'][0] and targets[1][0]==parent['properties'][1]
    name=r['name']['en'];pn=parent['name']['en'];ends=[d[p]['propertyType'] for p in r['properties']]
    checks={'native_end_orientation_agrees':True,
            'owl_subproperty_present':(C[name],RDFS.subPropertyOf,C[pn]) in g,
            'domain_matches':set(g.objects(C[name],RDFS.domain))=={C[ends[0]]},
            'range_matches':set(g.objects(C[name],RDFS.range))=={C[ends[1]]}}
    rows.append({'relation':r['id'],'parent_relation':parent['id'],'owl_property':str(C[name]),
                 'owl_parent_property':str(C[pn]),'checks':checks,'pass':all(checks.values())})
result={'scope':'Seven already-declared paired end specializations and their OWL domain/range/subPropertyOf axioms only. No cardinality equivalence, full-model equivalence, reasoner execution, or scientific acceptance.',
    'native_sha256':hashlib.sha256(N.read_bytes()).hexdigest(),'owl_sha256':hashlib.sha256(O.read_bytes()).hexdigest(),
    'rows':rows,'pass':sum(r['pass'] for r in rows),'total':len(rows)}
(H/'owl-alignment-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'}));assert result['pass']==result['total']==7
