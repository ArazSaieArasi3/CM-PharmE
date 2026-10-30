"""Reuse the source-qualified group profile for a real family-scoped risk review.

Add a distinct opt-in information profile. Do not weaken the existing complete
product/facility/dependency scenario profiles or invent a medicinal product.
"""
from lab import *
PREV=P/'2.1.0-alpha.1-module-contract-lab'
G=Namespace('https://w3id.org/cm-pharme/experimental/source-group/')
delta=graph();delta.add((E.scenarioScopeDescription,RDF.type,OWL.ObjectProperty));delta.add((E.scenarioScopeDescription,RDFS.domain,C.Assertion));delta.add((E.scenarioScopeDescription,RDFS.range,C.Assertion))
shapes=graph();root=E.SourceScopedRiskScenarioShape;shapes.add((root,RDF.type,SH.NodeShape));shapes.add((root,SH.targetSubjectsOf,E.scenarioScopeDescription));shapes.add((root,SH['class'],C.Assertion))
target=BNode();shapes.add((root,SH.target,target));shapes.add((target,RDF.type,SH.SPARQLTarget));shapes.add((target,SH.select,Literal('SELECT ?this WHERE { ?this <'+str(E.riskProfile)+'> "source-scoped-risk-scenario" }')))
n=BNode();shapes.add((root,SH.property,n));shapes.add((n,SH.path,E.scenarioScopeDescription));shapes.add((n,SH.minCount,Literal(1)));shapes.add((n,SH.maxCount,Literal(1)));shapes.add((n,SH.node,G['source-group-scopeShape']))
groupdelta=Graph().parse(PREV/'pv-group-delta.ttl');groupshapes=Graph().parse(PREV/'pv-group-shapes.ttl')
g=graph();source=T['RM-EMA-2020'];g.add((source,RDF.type,C.SourceRecord));g.add((source,E.sourceID,Literal('RM-EMA-2020')))
g.add((T.riskScenario,RDF.type,C.Assertion));g.add((T.riskScenario,E.scenarioScopeDescription,T.riskScope));g.add((T.riskScenario,B.evidencePointer,Literal('RM-EMA-2020#p1 More about the medicine')))
g.add((T.riskScenario,E.riskProfile,Literal('source-scoped-risk-scenario')))
g.add((T.riskScope,RDF.type,C.Assertion));g.add((T.riskScope,G.profile,Literal('source-group-scope')));g.add((T.riskScope,G.scopeVersion,Literal('EMA-603826-2020-sartan-review-scope')));g.add((T.riskScope,G.sourceLabel,Literal('sartan-review-included-labels')));g.add((T.riskScope,G.scopeSource,source))
labels=['candesartan','irbesartan','losartan','olmesartan','valsartan']
for i,label in enumerate(labels,1):
 n=T['risk-entry-'+str(i)];g.add((T.riskScope,G.scopeEntry,n));g.add((n,RDF.type,C.Assertion));g.add((n,G.profile,Literal('source-group-entry')));g.add((n,G.entrySource,source));g.add((n,G.entryOrdinal,Literal(i)))
 for p,v in [('scopeVersion','EMA-603826-2020-sartan-review-scope'),('sourceLabel',label),('evidencePointer','EMA/603826/2020#page=1'),('labelKindProposal','unqualified-name')]:g.add((n,G[p],Literal(v)))
save('risk-scope-data.ttl',g);save('risk-scope-delta.ttl',delta);save('risk-scope-shapes.ttl',shapes)
checks=[];ds=Dataset()
def admission_case(name,z,want):
 ok,_,_=validate(z+coh.hierarchy,shacl_graph=coh.shapes+groupshapes+shapes,advanced=True,inference='none');checks.append({'id':name,'kind':'admission','actual':bool(ok),'expected':want,'pass':bool(ok)==want});ds.graph(URIRef('urn:cmpe-risk-scope:'+name)).__iadd__(z)
admission_case('source-family-without-fake-product',g,True)
z=g+Graph();z.remove((T.riskScenario,E.scenarioScopeDescription,None));admission_case('missing-required-scope-link',z,False)
for name,mut in [('missing-scope-source',lambda z:z.remove((T.riskScope,G.scopeSource,None))),('wrong-entry-version',lambda z:(z.remove((T['risk-entry-1'],G.scopeVersion,None)),z.add((T['risk-entry-1'],G.scopeVersion,Literal('wrong'))))),('scope-is-carrier',lambda z:z.add((T.riskScope,RDF.type,C.SourceRecord))),('missing-member-label',lambda z:z.remove((T['risk-entry-1'],G.sourceLabel,None)))]:
 z=g+Graph();mut(z);admission_case(name,z,False)
q=f'SELECT ?label WHERE {{ <{T.riskScenario}> <{E.scenarioScopeDescription}>/<{G.scopeEntry}> ?entry . ?entry <{G.sourceLabel}> ?label }} ORDER BY ?label'
actual=[str(row[0]) for row in g.query(q)];checks.append({'id':'five-included-source-labels','kind':'query','query':q,'actual':actual,'expected':sorted(labels),'pass':actual==sorted(labels)})
checks.append({'id':'excluded-label-not-promoted','kind':'query','actual':'telmisartan' in actual,'expected':False,'pass':'telmisartan' not in actual})
logical=[]
for name,z in [('full-positive',g),('scope-not-single-product-countermodel',g+Graph())]:
 if 'countermodel' in name:
  coh.ctx.prev.not_type(z,T.riskScope,C.MedicinalProduct);coh.ctx.prev.not_type(z,T.riskScope,C.PharmaceuticalSubstance)
 r=coh.ctx.prev.hermit(coh.full+M+groupdelta+delta+z);logical.append({'id':name,**r,'pass':r['consistent'] and not r['unsatisfiable_named_classes']})
save('risk-scope-fixtures.trig',ds);dump('risk-scope-results.json',{'checks':checks,'passed':sum(x['pass'] for x in checks),'total':len(checks),'logical':logical,'relation_proposal':'scenarioScopeDescription','new_owned_classes':0,'native_change':False,'semantic_acceptance':False})
print(json.dumps({'risk_scope_checks':sum(x['pass'] for x in checks),'total':len(checks),'logical':sum(x['pass'] for x in logical)}),flush=True)
assert all(x['pass'] for x in checks+logical)
