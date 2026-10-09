"""Entailment by inconsistent negation; non-entailment by a consistent countermodel.
Complete pinned PROV-O with the explicit two-declaration reasoning projection,
including its non-RL union axioms. This is not a raw-import conformance claim.
This does not execute PROV-CONSTRAINTS or establish OntoUML/UFO validity.
"""
from common import *
save('prov-reasoning-projection.ttl',prov)
write('prov-adapter.json',{'source_triples':len(raw_prov),'reasoning_triples':len(prov),
 'removed_triples':[[str(x) for x in triple] for triple in sorted(raw_prov-prov)],'added_triples':[],
 'status':'PROPOSED_EXPLICIT_REASONING_PROJECTION_NOT_AUTHOR_ACCEPTED',
 'retains_every_other_source_triple':True,'imports':list(map(str,raw_prov.objects(None,OWL.imports))),
 'basis':'OWL 2 structural specification section 5.8.1 requires object/data/annotation property IRIs to be disjoint. The downloaded source dual-declares specializationOf and wasRevisionOf.',
 'raw_run':'initial-direct-results.json: 35/36; revision entailment fails with raw source in this parser.',
 'initial_owlready_run':'initial-owlready-results.json: 36/36, but loader explicitly attempted to repair dual property declarations.',
 'limitation':'No complete OWL2 DL profile checker or PROV-CONSTRAINTS validation is claimed. Header metadata including the source revision IRI is retained unchanged.'})
rows=[]
def case(name,g,want,mode='aligned',claim=''):
 theory=full if mode=='aligned' else base+prov if mode=='unaligned' else base
 result=hermit(theory+g);save('reasoner-fixtures/'+name+'.ttl',g)
 row={'name':name,'mode':mode,'claim':claim,'expected_consistent':want,**result,
      'pass':result['consistent']==want and not result['unsatisfiable_named_classes']}
 rows.append(row);print(json.dumps(row),flush=True)
 write('reasoner-results.json',{'cases':rows,'pass':sum(x['pass'] for x in rows),'total':len(rows)})
case('full-prov-and-baseline',graph(),True,'unaligned')
case('full-prov-and-directional-alignment',graph(),True)
for local,external in [(C.SourceRecord,PROV.Entity),(C.Dataset,PROV.Entity),(C.DatasetRelease,PROV.Entity),(C.ProvenanceActivity,PROV.Activity)]:
 name=str(local).split('/')[-1]
 g=graph();typ(g,T.x,local);not_type(g,T.x,external)
 case(name+'-forward-entails',g,False,claim='Negated external membership is inconsistent.')
 g=graph();typ(g,T.x,external);not_type(g,T.x,local)
 case(name+'-reverse-not-entailed',g,True,claim='External membership need not imply local membership.')
for local,external in [(L.recordDigitalActivity,PROV.wasGeneratedBy),(C.generatedAssertion,PROV.generated),(R.activityResponsibleOrganization,PROV.wasAssociatedWith)]:
 name=str(local).split('/')[-1]
 g=graph();g.add((T.x,local,T.y));not_edge(g,T.x,external,T.y)
 case(name+'-forward-entails',g,False)
 g=graph();g.add((T.x,external,T.y));not_edge(g,T.x,local,T.y)
 case(name+'-reverse-not-entailed',g,True)
g=graph();typ(g,T.x,PROV.Agent);not_type(g,T.x,PROV.Entity)
case('Agent-need-not-be-Entity',g,True,claim='Official PROV has no global Agent subclass Entity axiom.')
g=graph();typ(g,T.x,PROV.Agent);typ(g,T.x,PROV.Entity)
case('Agent-may-also-be-Entity',g,True)
g=graph();typ(g,T.x,C.Organization);not_type(g,T.x,PROV.Agent)
case('unassociated-Organization-not-automatically-Agent',g,True)
g=graph();typ(g,T.x,C.Assertion);not_type(g,T.x,PROV.Entity)
case('ungenerated-Assertion-not-automatically-Entity',g,True)
g=graph();g.add((T.x,C.generatedAssertion,T.y));not_type(g,T.y,PROV.Entity)
case('generated-Assertion-Entity-by-range',g,False)
g=graph();g.add((T.x,R.activityResponsibleOrganization,T.y));not_type(g,T.y,PROV.Agent)
case('responsible-Organization-Agent-by-range',g,False)
g=graph();typ(g,T.x,C.SourceRecord);typ(g,T.x,C.ProvenanceActivity)
case('record-activity-collision-unaligned',g,True,'unaligned')
case('record-activity-collision-aligned',g,False,claim='PROV Entity/Activity disjointness makes prior proposal redundant in this import configuration only.')
g=graph();g.add((T.x,L.recordDigitalActivity,T.y));not_edge(g,T.y,PROV.generated,T.x)
case('generation-inverse-entails',g,False)
g=reg.provenance();g.remove((reg.T.record,PROV.wasDerivedFrom,None));not_edge(g,reg.T.record,PROV.wasDerivedFrom,reg.T.previous)
case('revision-entails-derivation',g,False)
g=graph();g.add((T.x,PROV.specializationOf,T.y));not_edge(g,T.x,PROV.alternateOf,T.y)
case('specialization-entails-alternate',g,False)
g=graph();g.add((T.x,PROV.qualifiedRevision,T.q));typ(g,T.q,PROV.Revision);g.add((T.q,PROV.entity,T.y));not_edge(g,T.x,PROV.wasDerivedFrom,T.y)
case('qualified-revision-entails-derivation',g,False)
g=reg.provenance();case('revision-with-distinct-records',g,True)
g=graph();g.add((T.x,PROV.qualifiedGeneration,T.q));typ(g,T.q,PROV.Generation);g.add((T.q,PROV.activity,T.y));not_edge(g,T.x,PROV.wasGeneratedBy,T.y)
case('qualified-generation-chain',g,False)
g=graph();g.add((T.x,PROV.wasGeneratedBy,T.y));not_type(g,T.x,PROV.Generation)
case('generated-record-is-not-reified-Generation',g,True)
for name,g,node in [('registration',reg.registry(),reg.T.fact),('listing',reg.registry('listing'),reg.T.fact),('record',reg.provenance(),reg.T.record)]:
 not_type(g,node,C.RegulatoryAuthorization);case(name+'-no-authorization-entailment',g,True)
g=reg.shortage();not_type(g,reg.T.claim,C.MedicineShortageSituation);case('potential-claim-no-actual-shortage',g,True)
g=graph();g.add((T.x,C.usedSourceArtifact,T.y));typ(g,T.y,PROV.Activity)
case('broad-artifact-parent-allows-Activity-target',g,True)
g.add((C.usedSourceArtifact,RDFS.subPropertyOf,PROV.used))
case('unsafe-global-usage-mapping-rejects-Activity-target',g,False,claim='Stress case exposes new range commitment; not proof this use is intended.')
g=graph();typ(g,T.x,PROV.Activity);g.add((T.x,PROV.startedAtTime,Literal('2026-10-02T00:00:00Z',datatype=XSD.dateTime)));g.add((T.x,PROV.endedAtTime,Literal('2026-10-01T00:00:00Z',datatype=XSD.dateTime)))
case('OWL-does-not-validate-time-order',g,True,claim='Expected limitation: temporal consistency needs a separate constraints checker.')
assert all(x['pass'] for x in rows)
