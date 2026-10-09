"""Isolated proposed content-identity policy; does not edit baseline or native stereotypes."""
import json,hashlib
from pathlib import Path
from tempfile import TemporaryDirectory
from rdflib import Graph,Namespace,RDF,OWL,BNode,Literal
from pyshacl import validate
from owlready2 import World,sync_reasoner
from owlready2.base import OwlReadyInconsistentOntologyError
H=Path(__file__).resolve().parent;P=H.parent/'2.1.0-alpha.1-four-domain-refinement';O=H.parent/'2.1.0-alpha.1-four-domain-lab'
C=Namespace('https://w3id.org/cm-pharme/2.1/');L=Namespace('https://w3id.org/cm-pharme/experimental/four-domain/');R=Namespace('https://w3id.org/cm-pharme/experimental/refinement/');T=Namespace('urn:cmpe-policy:');SH=Namespace('http://www.w3.org/ns/shacl#')
def dump(n,x):(H/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
# Global to use of this experimental predicate; independent of opt-in profile tags.
delta=Graph();delta.add((L.pvResultSignal,RDF.type,OWL.IrreflexiveProperty));delta.add((R.carrierClaim,RDF.type,OWL.IrreflexiveProperty));delta.serialize(H/'proposed-delta.ttl',format='turtle')
s=Graph();shape=T.ResultSignalIdentityShape;s.add((shape,RDF.type,SH.NodeShape));s.add((shape,SH.targetSubjectsOf,L.pvResultSignal));constraint=T.NoSelfOrSameAsChain;s.add((shape,SH.sparql,constraint));s.add((constraint,SH.message,Literal('An assessment result must differ from its target signal, including explicitly stated sameAs aliases.')))
s.add((constraint,SH.select,Literal('''SELECT $this ?value WHERE {
 $this <https://w3id.org/cm-pharme/experimental/four-domain/pvResultSignal> ?value .
 $this (<http://www.w3.org/2002/07/owl#sameAs>|^<http://www.w3.org/2002/07/owl#sameAs>)* ?value .
}''')));s.serialize(H/'proposed-shapes.ttl',format='turtle')
carrier_shape=T.CarrierClaimIdentityShape;carrier_constraint=T.CarrierNotOwnClaim
s.add((carrier_shape,RDF.type,SH.NodeShape));s.add((carrier_shape,SH.targetSubjectsOf,R.carrierClaim));s.add((carrier_shape,SH.sparql,carrier_constraint));s.add((carrier_constraint,SH.message,Literal('A carrier must differ from its carried claim, including explicit sameAs aliases.')))
s.add((carrier_constraint,SH.select,Literal('SELECT $this ?value WHERE { $this <'+str(R.carrierClaim)+'> ?value . $this (<'+str(OWL.sameAs)+'>|^<'+str(OWL.sameAs)+'>)* ?value . }')))
s.serialize(H/'proposed-shapes.ttl',format='turtle')
shapes=Graph().parse(P/'combined.shacl.ttl')+s;ont=Graph().parse(P/'experimental.owl.ttl')+delta
(H/'fixtures').mkdir(exist_ok=True)
checks=[]
def graph(edges):
 g=Graph()
 for a,p,b in edges:g.add((T[a],p,T[b]))
 return g
def check(name,g,expected):
 ok,report,_=validate(g,shacl_graph=shapes,advanced=True,inference='none')
 violations=[str(report.value(x,SH.sourceConstraint)) for x in report.subjects(RDF.type,SH.ValidationResult)]
 path='fixtures/'+name+'.ttl';g.serialize(H/path,format='turtle')
 checks.append({'name':name,'expected_conforms':expected,'actual_conforms':bool(ok),'violation_constraints':violations,'fixture':path,'pass':bool(ok)==expected and (expected or str(constraint) in violations or str(carrier_constraint) in violations)})
 return g
E=[('result',L.pvResultSignal,'signal')]
check('untagged-distinct-result',graph(E),True)
check('untagged-self',graph([('result',L.pvResultSignal,'result')]),False)
check('direct-alias',graph(E+[('result',OWL.sameAs,'signal')]),False)
check('reverse-alias',graph(E+[('signal',OWL.sameAs,'result')]),False)
check('mixed-three-link-alias',graph(E+[('result',OWL.sameAs,'a'),('b',OWL.sameAs,'a'),('b',OWL.sameAs,'signal')]),False)
check('unrelated-alias',graph(E+[('x',OWL.sameAs,'y')]),True)
check('shared-signal-two-assessments',graph(E+[('result2',L.pvResultSignal,'signal')]),True)
check('cross-context-content-reuse',graph(E+[('signal',L.pvResultSignal,'result')]),True)
g=graph(E);g.add((T.result,R.claimText,Literal('same lexical string')));g.add((T.signal,R.claimText,Literal('same lexical string')));check('same-text-does-not-merge-claims',g,True)
check('carrier-self-without-tag',graph([('record',R.carrierClaim,'record')]),False)
check('carrier-alias-chain',graph([('record',R.carrierClaim,'claim'),('record',OWL.sameAs,'alias'),('claim',OWL.sameAs,'alias')]),False)
check('distinct-carrier-and-claim',graph([('record',R.carrierClaim,'claim')]),True)
check('two-carriers-same-claim',graph([('record',R.carrierClaim,'claim'),('copy',R.carrierClaim,'claim')]),True)
# Replay every prior SHACL expectation, preserving its marker check.
reg=[]
prior=json.loads((O/'shacl-results.json').read_text())['cases']+json.loads((P/'refinement-shacl-results.json').read_text())
for i,c in enumerate(prior):
 src=O if i<39 else P;g=Graph().parse(src/c['fixture']);ok,r,_=validate(g,shacl_graph=shapes,advanced=True,inference='none');marker=c.get('expected_failure_marker',c.get('expected_marker'))
 details=[{'path':str(r.value(x,SH.resultPath) or ''),'constraint':str(r.value(x,SH.sourceConstraint) or ''),'focus':str(r.value(x,SH.focusNode) or '')} for x in r.subjects(RDF.type,SH.ValidationResult)]
 reg.append({'name':c['name'],'source':str(src.name)+'/'+c['fixture'],'expected_conforms':c['expected_conforms'],'actual_conforms':bool(ok),'marker':marker,'pass':bool(ok)==c['expected_conforms'] and (marker is None or any(marker in str(x) for x in details))})
dump('shacl-results.json',checks);dump('regression-results.json',reg)
print(json.dumps({'new_shacl':sum(x['pass'] for x in checks),'total':len(checks),'regression_pass':sum(x['pass'] for x in reg),'regression_total':len(reg)}),flush=True)
rr=[]
def reason(name,g,expected=True):
 with TemporaryDirectory() as td:
  p=Path(td)/'model.rdf';(ont+g).serialize(p,format='xml');w=World();w.get_ontology(p.as_uri()).load()
  try:sync_reasoner(w,debug=0);actual=True;unsat=[str(c.iri) for c in w.inconsistent_classes() if c.iri!=str(OWL.Nothing)]
  except OwlReadyInconsistentOntologyError:actual=False;unsat=[]
  finally:w.close()
 row={'name':name,'expected_consistent':expected,'actual_consistent':actual,'unsatisfiable_named_classes':unsat,'pass':actual==expected and not unsat};rr.append(row);print(json.dumps(row),flush=True)
reason('proposed-tbox-coherence',Graph())
reason('self-is-inconsistent',graph([('result',L.pvResultSignal,'result')]),False)
reason('sameAs-chain-is-inconsistent',graph(E+[('result',OWL.sameAs,'a'),('a',OWL.sameAs,'signal')]),False)
reason('two-assessments-can-share-signal',graph(E+[('result2',L.pvResultSignal,'signal'),('result',OWL.differentFrom,'result2')]))
reason('cross-context-reuse-not-globally-disjoint',graph(E+[('signal',L.pvResultSignal,'result')]))
g=graph([('record',R.carrierClaim,'claim'),('record2',R.carrierClaim,'claim2'),('record',OWL.differentFrom,'record2'),('claim',OWL.differentFrom,'claim2')]);
for n in ['record','record2']:g.add((T[n],R.caseIdentifier,Literal('SYNTHETIC-SAME-ID')))
for n in ['claim','claim2']:g.add((T[n],R.claimText,Literal('same lexical string')))
reason('same-case-and-text-do-not-require-identity',g)
reason('record-cannot-be-its-claim',graph([('record',R.carrierClaim,'record')]),False)
reason('previous-combined-witness',Graph().parse(P/'combined-positive.ttl'))
dump('reasoner-results.json',rr)
summary={'status':'ISOLATED_PROPOSAL_NOT_AUTHOR_APPROVED','new_classes':0,'new_relations':0,'new_owl_axioms':2,'new_shapes':2,'new_shacl_cases':len(checks),'new_shacl_pass':sum(x['pass'] for x in checks),'prior_regression_cases':len(reg),'prior_regression_pass':sum(x['pass'] for x in reg),'reasoner_cases':len(rr),'reasoner_pass':sum(x['pass'] for x in rr),'all_pass':all(x['pass'] for x in checks+reg+rr),'native_stereotypes_approved':False,'baseline_changed':False,'full_ontology_validation':False,'hashes':{n:hashlib.sha256((H/n).read_bytes()).hexdigest() for n in ['proposed-delta.ttl','proposed-shapes.ttl']},'parent_hashes':{n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ['experimental.owl.ttl','combined.shacl.ttl','ontouml-experimental.json']}}
dump('policy-results.json',summary)
assert summary['all_pass'],summary
