"""Independent domain counterexamples for three proposals; SHACL and HermiT.
Derivation is a declared operational rule, not an OWL inference completeness claim.
"""
import copy,json,sys,tempfile
from pathlib import Path
from rdflib import Graph,Namespace,RDF,RDFS,OWL,Literal,BNode,XSD,URIRef
from pyshacl import validate
from owlready2 import World,sync_reasoner
from owlready2.base import OwlReadyInconsistentOntologyError
from build_lab import RELATIONS,H,P,write
C=Namespace('https://w3id.org/cm-pharme/2.1/');T=Namespace('urn:cmpe-participant-lab:');SH=Namespace('http://www.w3.org/ns/shacl#')
ont=Graph().parse(P/'experimental.owl.ttl')
base_shapes=Graph().parse(P/'combined.shacl.ttl')
old_policy=H.parent/'2.1.0-alpha.1-content-event-policy'
ont+=Graph().parse(old_policy/'proposed-delta.ttl');base_shapes+=Graph().parse(old_policy/'proposed-shapes.ttl')
hierarchy=Graph()
for a,b in ont.subject_objects(RDFS.subClassOf):
 if isinstance(a,URIRef) and isinstance(b,URIRef):hierarchy.add((a,RDFS.subClassOf,b))

def instance(g,node,cls):
 return any(t==cls or (t,RDFS.subClassOf*'+',cls) in hierarchy for t in g.objects(node,RDF.type))

def materialize(g):
 out=g+Graph()
 for name,(parent,source,target) in RELATIONS.items():
  for a,b in list(g.subject_objects(C[parent])):
   if instance(g,a,C[source]) and instance(g,b,C[target]):out.add((a,C[name],b))
 return out

def shapes(variant):
 s=Graph()
 for i,(name,(parent,source,target)) in enumerate(RELATIONS.items()):
  shape=T[name+'Shape'];prop=T[name+'Cardinality'];s.add((shape,RDF.type,SH.NodeShape));s.add((shape,SH.targetClass,C[source]));s.add((shape,SH.targetSubjectsOf,C[name]));s.add((shape,SH['class'],C[source]));s.add((shape,SH.property,prop));s.add((prop,SH.path,C[name]));s.add((prop,SH['class'],C[target]));s.add((prop,SH.maxCount,Literal(1)))
  minimum=1 if variant=='B' or i==0 or (variant=='A' and i==1) else 0
  s.add((prop,SH.minCount,Literal(minimum)))
  # Exactness covers both missing eligible projections and stale/unsupported edges.
  constraint=T[name+'ExactProjection'];s.add((shape,SH.sparql,constraint));s.add((constraint,SH.message,Literal('Derived typed projection must equal the eligible primitive links.')))
  query=f'''SELECT $this ?value WHERE {{
   {{ $this <{C[parent]}> ?value . $this a/rdfs:subClassOf* <{C[source]}> . ?value a/rdfs:subClassOf* <{C[target]}> . FILTER NOT EXISTS {{ $this <{C[name]}> ?value }} }}
   UNION {{ $this <{C[name]}> ?value . FILTER NOT EXISTS {{ $this <{C[parent]}> ?value . $this a/rdfs:subClassOf* <{C[source]}> . ?value a/rdfs:subClassOf* <{C[target]}> }} }}
  }}'''
  s.add((constraint,SH.select,Literal('PREFIX rdfs: <'+str(RDFS)+'>\n'+query)))
  if variant=='B':
   inverse=T[name+'Inverse'];ip=T[name+'InverseCardinality'];path=BNode()
   s.add((inverse,RDF.type,SH.NodeShape));s.add((inverse,SH.targetClass,C[target]));s.add((inverse,SH.property,ip));s.add((ip,SH.path,path));s.add((path,SH.inversePath,C[name]));s.add((ip,SH.minCount,Literal(1)))
 return s

def restrictions(variant):
 d=Graph()
 for i,(name,(parent,source,target)) in enumerate(RELATIONS.items()):
  minimum=1 if variant=='B' or i==0 or (variant=='A' and i==1) else 0
  for predicate,value in [(OWL.minQualifiedCardinality,minimum),(OWL.maxQualifiedCardinality,1)]:
   b=BNode();d.add((C[source],RDFS.subClassOf,b));d.add((b,RDF.type,OWL.Restriction));d.add((b,OWL.onProperty,C[name]));d.add((b,OWL.onClass,C[target]));d.add((b,predicate,Literal(value,datatype=XSD.nonNegativeInteger)))
 return d

def types(g,n,*classes):
 for cls in classes:g.add((T[n],RDF.type,C[cls]))
def classification(substance=False,context=True):
 g=Graph();types(g,'assignment','ProductClassificationAssignment')
 if context:types(g,'assignment','ContextualMedicineClassificationAssignment')
 types(g,'entry','ClassificationEntry','AppliedClassificationEntryRole')
 types(g,'entity','ClassifiedEntity',*(['PharmaceuticalSubstance','ClassifiedPharmaceuticalSubstanceRole'] if substance else ['MedicinalProduct','ClassifiedMedicinalProductRole']))
 g.add((T.assignment,C.classificationEntity,T.entity));g.add((T.assignment,C.classificationEntry,T.entry))
 return g
def evidence(record=True):
 g=Graph();types(g,'support','EvidenceSupport');types(g,'claim','Assertion','SupportedAssertionRole');types(g,'item','EvidenceItem')
 if record:types(g,'item','SourceRecord','EvidenceSourceRecordRole')
 else:
  types(g,'item','Dataset');b=BNode();g.add((b,OWL.complementOf,C.SourceRecord));g.add((T.item,RDF.type,b))
 g.add((T.support,C.evidenceItem,T.item));g.add((T.support,C.evidenceAssertion,T.claim));return g

def main():
 S={k:shapes(k) for k in ['A','B','C']};D={k:restrictions(k) for k in ['A','B','C']}
 for k in S:S[k].serialize(H/('proposal-'+k+'.shacl.ttl'),format='turtle');D[k].serialize(H/('proposal-'+k+'.owl-delta.ttl'),format='turtle')
 fixtures={
  'context-product':classification(), 'context-substance':classification(True),
  'generic-product-no-context':classification(context=False),
  'record-evidence':evidence(), 'nonrecord-evidence':evidence(False)}
 expected={'context-product':{'A':True,'B':True,'C':True},'context-substance':{'A':False,'B':False,'C':True},
 'generic-product-no-context':{'A':True,'B':False,'C':True},'record-evidence':{'A':True,'B':True,'C':True},
 'nonrecord-evidence':{'A':True,'B':False,'C':True}}
 checks=[]
 def check(name,g,k,want,derive=True,marker=None):
  x=materialize(g) if derive else g+Graph();ok,report,_=validate(x+hierarchy,shacl_graph=base_shapes+S[k],inference='none',advanced=True)
  details=[{'path':str(report.value(z,SH.resultPath) or ''),'constraint':str(report.value(z,SH.sourceConstraint) or ''),'shape':str(report.value(z,SH.sourceShape) or '')} for z in report.subjects(RDF.type,SH.ValidationResult)]
  file='fixtures/'+name+'.ttl';(H/'fixtures').mkdir(exist_ok=True);g.serialize(H/file,format='turtle')
  checks.append({'name':name,'variant':k,'materialized':derive,'expected':want,'actual':bool(ok),'marker':marker,
    'details':details,'pass':bool(ok)==want and (marker is None or any(marker in str(z) for z in details)),'fixture':file})
 for name,g in fixtures.items():
  for k in S:check(name,g,k,expected[name][k])
 check('missing-entry',fixtures['context-product']-Graph().add((T.assignment,C.classificationEntry,T.entry)),'C',False,marker='classificationEntry')
 stale=materialize(classification());types(stale,'other','ClassifiedEntity','ClassifiedMedicinalProductRole','MedicinalProduct');stale.add((T.assignment,C.contextClassificationProduct,T.other));check('stale-product-projection',stale,'C',False,marker='contextClassificationProduct')
 stale=materialize(evidence());types(stale,'other','EvidenceItem','EvidenceSourceRecordRole','SourceRecord');stale.add((T.support,C.evidenceRecord,T.other));check('stale-record-projection',stale,'C',False,marker='evidenceRecord')
 check('eligible-product-projection-missing-before-materialization',classification(),'C',False,derive=False,marker='ExactProjection')
 check('eligible-record-projection-missing-before-materialization',evidence(),'C',False,derive=False,marker='ExactProjection')
 only=evidence();only.remove((T.support,C.evidenceItem,T.item));only.add((T.support,C.evidenceRecord,T.item));check('shortcut-does-not-invent-parent-fact',only,'C',False,marker='evidenceItem')
 # The old negative contains a primitive link to an explicitly typed record.
 # Its only missing assertion is the redundant shortcut. Preserve its historical
 # expectation below and expose the proposed contract transition independently.
 migration=Graph().parse(P/'fixtures/X-BA-COMMITMENT-missing-source-evidence.ttl')
 check('documented-partnership-primitive-record-suffices',migration,'C',True)
 no_fact=migration+Graph();no_fact.remove((None,C.evidenceItem,None))
 check('documented-partnership-primitive-evidence-absent',no_fact,'C',False,marker='commitment-evidence-required')
 no_role=migration+Graph();no_role.remove((None,RDF.type,C.EvidenceSourceRecordRole))
 check('documented-partnership-unqualified-record-not-derived',no_role,'C',False,marker='commitment-evidence-required')
 # Replay all 89 previous bounded SHACL witnesses after explicit proposed derivation.
 prior=[];L=H.parent/'2.1.0-alpha.1-four-domain-lab'
 old=json.loads((L/'shacl-results.json').read_text())['cases']
 prior.extend((L,x) for x in old);prior.extend((P,x) for x in json.loads((P/'refinement-shacl-results.json').read_text()))
 prior.extend((old_policy,x) for x in json.loads((old_policy/'shacl-results.json').read_text()))
 replay=[]
 for folder,c in prior:
  original=Graph().parse(folder/c['fixture']);data=materialize(original)
  baseline_ok,_,_=validate(original+hierarchy,shacl_graph=base_shapes,inference='none',advanced=True)
  ok,report,_=validate(data+hierarchy,shacl_graph=base_shapes+S['C'],inference='none',advanced=True)
  marker=c.get('expected_failure_marker',c.get('expected_marker'))
  details=[{'path':str(report.value(z,SH.resultPath) or ''),'constraint':str(report.value(z,SH.sourceConstraint) or '')} for z in report.subjects(RDF.type,SH.ValidationResult)]
  replay.append({'name':c['name'],'source':folder.name+'/'+c['fixture'],'expected':c['expected_conforms'],'actual':bool(ok),'marker':marker,
   'baseline_actual':bool(baseline_ok),'baseline_pass':bool(baseline_ok)==c['expected_conforms'],
   'details':details,'triples_added':len(data)-len(original),'pass':bool(ok)==c['expected_conforms'] and (marker is None or any(marker in str(z) for z in details))})
 write('shacl-results.json',{'cases':checks,'pass':sum(c['pass'] for c in checks),'total':len(checks)})
 known='2.1.0-alpha.1-four-domain-refinement/fixtures/X-BA-COMMITMENT-missing-source-evidence.ttl'
 failures=[c for c in replay if not c['pass']]
 characterized=len(failures)==1 and failures[0]['source']==known and failures[0]['actual'] is True and failures[0]['triples_added']==1
 write('prior-regression-results.json',{'cases':replay,'pass':sum(c['pass'] for c in replay),'total':len(replay),'materialization_applied':True,
  'baseline_pass':sum(c['baseline_pass'] for c in replay),'known_contract_change_characterized':characterized,
  'contract_change_accepted':False,'regression_gate':'BLOCKED_PENDING_SEMANTIC_DECISION'})
 print(json.dumps({'shacl_pass':sum(c['pass'] for c in checks),'shacl_total':len(checks),'replay_pass':sum(c['pass'] for c in replay),'replay_total':len(replay)}),flush=True)
 assert all(c['pass'] for c in checks) and all(c['baseline_pass'] for c in replay) and characterized
 if '--shacl-only' in sys.argv:return
 rr=[]
 def reason(name,g,k,want):
  merged=ont+g+(D[k] if k else Graph())
  with tempfile.TemporaryDirectory() as td:
   f=Path(td)/'model.rdf';merged.serialize(f,format='xml');w=World();w.get_ontology(f.as_uri()).load()
   try:sync_reasoner(w,debug=0);actual=True;unsat=[c.iri for c in w.inconsistent_classes() if c.iri!=str(OWL.Nothing)]
   except OwlReadyInconsistentOntologyError:actual=False;unsat=[]
   finally:w.close()
  row={'name':name,'variant':k or 'BASELINE','expected_consistent':want,'actual_consistent':actual,'unsatisfiable_named_classes':unsat,'pass':actual==want and not unsat};rr.append(row);print(json.dumps(row),flush=True)
 reason('C-tbox-coherent',Graph(),'C',True)
 for name in ['context-substance','nonrecord-evidence']:
  for k,want in [(None,True),('B',False),('C',True)]:reason(name,materialize(fixtures[name]),k,want)
 missing=Graph();types(missing,'assignment','ContextualMedicineClassificationAssignment')
 reason('missing-data-is-not-OWL-inconsistency',missing,'C',True)
 b=BNode();missing.add((T.assignment,RDF.type,b));missing.add((b,RDF.type,OWL.Restriction));missing.add((b,OWL.onProperty,C.contextClassificationEntry));missing.add((b,OWL.maxCardinality,Literal(0,datatype=XSD.nonNegativeInteger)))
 reason('explicit-zero-contradicts-required-entry',missing,'C',False)
 two=materialize(classification());types(two,'other','MedicinalProduct','ClassifiedMedicinalProductRole');two.add((T.assignment,C.contextClassificationProduct,T.other))
 reason('different-IRIs-do-not-prove-distinct-products',two,'C',True)
 two.add((T.entity,OWL.differentFrom,T.other));reason('two-explicitly-distinct-products-inconsistent',two,'C',False)
 reason('prior-combined-witness',materialize(Graph().parse(P/'combined-positive.ttl')),'C',True)
 write('reasoner-results.json',{'cases':rr,'pass':sum(x['pass'] for x in rr),'total':len(rr)})
 assert all(c['pass'] for c in checks+rr)

if __name__=='__main__':main()
