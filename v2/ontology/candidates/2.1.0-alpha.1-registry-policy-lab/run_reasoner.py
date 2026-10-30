"""HermiT countermodels for selected existing and proposed semantics.

Source-specific p: admission/query rules are NOT thereby proven in OWL.
The full PROV ontology is not imported and no PROV conformance is claimed.
"""
import tempfile,sys
from owlready2 import World,sync_reasoner
from owlready2.base import OwlReadyInconsistentOntologyError
from lab import *
ONLY=set(sys.argv[1:])
ROWS=json.loads((H/'reasoner-results.json').read_text())['cases'] if ONLY else []
def not_type(g,subject,cls):
 b=BNode();g.add((b,OWL.complementOf,cls));g.add((subject,RDF.type,b))
def reason(name,g,proposed,want,reqs):
 if ONLY and name not in ONLY:return
 merged=ontology+g+(delta() if proposed else Graph())
 save(g,'reasoner-fixtures/'+name+'.ttl')
 with tempfile.TemporaryDirectory() as td:
  f=Path(td)/'model.rdf';merged.serialize(f,format='xml');world=World();world.get_ontology(f.as_uri()).load()
  try:
   sync_reasoner(world,debug=0);actual=True;unsat=[x.iri for x in world.inconsistent_classes() if x.iri!=str(OWL.Nothing)]
  except OwlReadyInconsistentOntologyError:actual=False;unsat=[]
  finally:world.close()
 row={'name':name,'proposed_disjointness':proposed,'requirements':reqs,'expected_consistent':want,'actual_consistent':actual,'unsatisfiable_named_classes':unsat,'fixture':'reasoner-fixtures/'+name+'.ttl','pass':actual==want and not unsat}
 ROWS[:]=[r for r in ROWS if r['name']!=name];ROWS.append(row);print(json.dumps(row),flush=True)
def req(*s):return ['B2-'+x for x in s]
reason('baseline-tbox-coherent',graph(),False,True,[])
reason('proposed-tbox-coherent',graph(),True,True,[])
g=registry();not_type(g,T.fact,C.RegulatoryAuthorization);reason('registration-fact-not-authorization-countermodel',g,True,True,req('RG-02'))
g=registry('listing');not_type(g,T.fact,C.RegulatoryAuthorization);reason('listing-fact-not-authorization-countermodel',g,True,True,req('RG-03'))
g=registry();not_type(g,T.record,C.RegulatoryAuthorization);reason('source-record-not-authorization-countermodel',g,True,True,req('RG-02','RG-03'))
g=shortage();not_type(g,T.claim,C.MedicineShortageSituation);reason('potential-claim-not-actual-situation-countermodel',g,True,True,req('RP-02'))
g=provenance();g.add((T.record,OWL.sameAs,T.activity))
reason('record-activity-alias-baseline',g,False,True,req('DS-07'))
reason('record-activity-alias-proposal',g,True,False,req('DS-07'))
g=shortage();types(g,T.claim,C.MedicineShortageSituation)
reason('claim-situation-collision-baseline',g,False,True,req('RP-02'))
reason('claim-situation-collision-proposal',g,True,False,req('RP-02'))
reason('revision-with-explicit-distinct-versions',provenance(),True,True,req('DS-10'))
g=graph();types(g,T.record,C.SourceRecord);g.add((PROV.Entity,RDF.type,OWL.Class));not_type(g,T.record,PROV.Entity)
reason('closeMatch-does-not-entail-PROV-Entity',g,False,True,req('DS-07','DS-08','DS-09','DS-10'))
g=graph()
for prefix,part in [('registry',registry()),('listing',registry('listing')),('provenance',provenance()),('reporting',reporting('crisis')),('shortage',shortage()),('submission',submission())]:
 def remap(x):return URIRef(str(T)+prefix+'-'+str(x)[len(str(T)):]) if isinstance(x,URIRef) and str(x).startswith(str(T)) else x
 for a,b,c in part:g.add((remap(a),b,remap(c)))
reason('combined-positive-witness',g,True,True,[])
write('reasoner-results.json',{'cases':ROWS,'pass':sum(r['pass'] for r in ROWS),'total':len(ROWS),
 'scope':'Named-individual countermodels and two proposed disjointness axioms; no full OntoUML/PROV/legal applicability proof.',
 'product_approval_limit':'Registration/listing facts need not be RegulatoryAuthorization instances. A complete medicinal-product approval model is still absent, so these cases do not prove all product-approval semantics.'})
assert all(r['pass'] for r in ROWS)
