"""Non-regression checks focus on new vocabulary and supported projections."""
from lab import *
PREV=P/'2.1.0-alpha.1-module-contract-lab'
delta=M+Graph().parse(PREV/'pv-group-delta.ttl')+Graph().parse(H/'risk-scope-delta.ttl')
shapes=coh.shapes+S+Graph().parse(PREV/'pv-group-shapes.ttl')+Graph().parse(H/'risk-scope-shapes.ttl')
data=Graph().parse(H/'evidence.ttl')+Graph().parse(H/'risk-scope-data.ttl')+Graph().parse(H/'contract-claims.ttl')+Graph().parse(H/'contract-domain-projection.ttl')
old=Graph().parse(PREV/'combined-positive.ttl');combined=data+old
ok,_,_=validate(combined+coh.hierarchy,shacl_graph=shapes,advanced=True,inference='none');hr=coh.ctx.prev.hermit(coh.full+delta+combined)
old_cases=0;target_intersections=[]
for m in ['RM','PV','BA','DS']:
 contract=json.loads((PREV/'modules'/m/'contract.json').read_text())
 for case in contract['admission_cases']:
  g=Graph().parse(PREV/'modules'/m/case['fixture']);old_cases+=1
  if list(g.triples((None,E.claimMode,None))) or list(g.triples((None,E.profile,None))) or list(g.triples((None,E.scenarioScopeDescription,None))) or list(g.triples((None,E.riskProfile,None))):target_intersections.append(case['id'])
# These are candidate projections and are not added to the real-source graph.
# Their expected failures expose missing evidence instead of filling it in.
profiles=[]
g=graph();g.add((T.launch,RDF.type,C.SystemDeploymentActivity));g.add((T.launch,L.profile,Literal('deployment')));g.add((T.system,RDF.type,C.DigitalInformationSystemComponent));g.add((T.launch,L.deploymentComponent,T.system))
def profile(name,g,expected,missing):
 result=coh.admission(g);profiles.append({'id':name,'expected_conforms':expected,'actual_conforms':result['conforms'],'violations':result['violations'],'unestablished_fields':missing,'pass':result['conforms']==expected});save('projection-'+name+'.ttl',g)
profile('DS-complete-deployment',g,False,['componentVersion: not in source; E2B(R3) is a message standard','deploymentOrganization: launching actor is not automatically technical operator','atTime: day known, exact time and timezone not known'])
g=graph();g.add((T.agreement,RDF.type,C.StrategicPartnershipAgreement));g.add((T.agreement,L.profile,Literal('documented-partnership')))
for org in ['Lonza','Moderna']:
 g.add((T[org],RDF.type,C.Organization));g.add((T[org],RDF.type,C.PartnerOrganizationRole));g.add((T.agreement,C.partnershipParticipant,T[org]))
profile('BA-complete-commitment',g,False,['agreementCommitment: full documented commitment content not extracted','commitment evidence and exact participants not reconstructed as accepted facts'])
g=Graph().parse(H/'risk-scope-data.ttl');g.add((T.riskScenario,L.profile,Literal('risk-scenario')))
profile('RM-original-product-profile',g,False,['scenarioProduct/scenarioFacility/scenarioDependency: family label list is not a single product, facility or dependency; use the separate proposed scope profile'])
result={'historical_fixtures_inspected':old_cases,'new_target_intersections':target_intersections,'interpretation':'Historical 83 fixture files were inspected for new shape targets, not re-executed; prior results are not counted anew. Existing shapes and source packages unchanged.','combined_triples':len(combined),'combined_admission':bool(ok),'combined_reasoner':hr,'profile_fit':profiles,'new_classes':0,'new_domain_information_relations':1,'new_owned_classes':0,'native_changed':False}
result['pass']=bool(ok) and hr['consistent'] and not hr['unsatisfiable_named_classes'] and not target_intersections and all(x['pass'] for x in profiles)
dump('integration-results.json',result);save('combined-positive.ttl',combined)
print(json.dumps({'combined_triples':len(combined),'pass':result['pass'],'historical_inspected':old_cases,'profile_fit':sum(x['pass'] for x in profiles)}),flush=True)
assert result['pass']
