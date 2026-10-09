from lab import *
topology=build_native();tests=[];logic=[];queries=[];ds=Dataset();positive=graph()
def keep(name,g):
 for t in g:ds.graph(URIRef('urn:coherence-case:'+name)).add(t)
def check(name,g,want,marker=None):
 r=admission(g);passed=r['conforms']==want and (marker is None or marker in str(r['violations']));tests.append({'name':name,'expected':want,**r,'marker':marker,'pass':passed});keep(name,g)
def reason(name,g,want=True,allowed_empty=()):
 r=ctx.prev.hermit(full+g)
 empty={x.rsplit('/',1)[-1].rsplit(':',1)[-1] for x in r['unsatisfiable_named_classes']}
 logic.append({'name':name,'expected_consistent':want,'expected_deliberately_empty_classes':list(allowed_empty),**r,'pass':r['consistent']==want and empty==set(allowed_empty)})
def query(name,actual,want):queries.append({'name':name,'actual':actual,'expected':want,'pass':actual==want})
for tag in PROFILES:
 g,n=fixture(tag);check(tag+'-positive',g,True);positive+=g
 for p in PROFILES[tag]['fields']:
  x=g+Graph();x.remove((n,D[p],None));check(tag+'-missing-'+p,x,False,p)
  x=g+Graph();o=x.value(n,D[p]);x.remove((o,RDF.type,None));check(tag+'-untyped-'+p,x,False,p)
 query(tag+'-retrievable-fields',sum(bool(list(g.objects(n,D[p]))) for p in PROFILES[tag]['fields']),len(PROFILES[tag]['fields']))
g,n=fixture('stockout');x=g+Graph();ctx.prev.not_type(x,n,C.MedicineShortageSituation);reason('local-stockout-does-not-imply-medicine-shortage',x)
g,n=fixture('procurement');ctx.prev.not_type(g,n,C.RiskTreatmentActivity);reason('procurement-does-not-imply-risk-treatment',g)
g,n=fixture('requirement');ctx.prev.not_type(g,n,C.RegulatoryAuthorization);reason('requirement-does-not-imply-authorization',g)
g,n=fixture('logistics');ctx.prev.not_type(g,n,C.ManufacturingActivity);reason('logistics-does-not-imply-manufacturing',g)
reason('combined-new-positive-fixtures',positive)
# Narrow logistics capability/service example; an ordinary outsourcing claim
# does not license StrategicPartnershipAgreement or PartnerOrganizationRole.
ba,_=fixture('capability-logistics');cap=T['capability-logistics'];org=T.bearer
for n,c in [(T.view,C.BusinessArchitectureView),(T.service,C.ServiceOfferingSpecification),(T.customer,C.Organization),(T.product,C.MedicinalProduct),(T.contractCarrier,C.SourceRecord)]:typ(ba,n,c)
ba.add((T.service,L.serviceCapability,cap));ba.add((T.service,R.serviceProduct,T.product));ba.add((T.view,L.viewOrganization,org));ba.add((T.view,L.viewService,T.service))
ctx.claim(ba,T.contractClaim,T.contractCarrier,org,D.outsourcingCounterparty,T.customer,origin='synthetic',pointer='synthetic:GDP-chapter-7-outsourcing-example')
check('BA-outsourced-logistics-service',ba,True)
query('BA-service-capability-bearer',str(ba.value(ba.value(T.service,L.serviceCapability),C.capabilityBearer)),str(org))
query('BA-no-strategic-agreement-asserted',len(list(ba.subjects(RDF.type,C.StrategicPartnershipAgreement))),0)
z=ba+Graph();z.add((C.StrategicPartnershipAgreement,RDFS.subClassOf,OWL.Nothing));ctx.prev.not_type(z,org,C.PartnerOrganizationRole);ctx.prev.not_type(z,T.customer,C.PartnerOrganizationRole);reason('outsourcing-with-no-strategic-partnership-countermodel',z,allowed_empty=['StrategicPartnershipAgreement','PartnerOrganizationRole'])
# Existing DS profile plus the new logistics interface, without forcing manufacturing.
base=H.parent/'2.1.0-alpha.1-four-domain-lab'
digital=Graph().parse(base/'fixtures/DS-1-positive.ttl');oldT=Namespace('urn:cmpe-lab:');logistics,_=fixture('logistics');digital+=logistics;digital.add((oldT.transform,D.profile,Literal('digital-logistics')));digital.add((oldT.transform,D.supportsLogistics,T.logistics))
check('DS-logistics-provenance',digital,True);z=digital+Graph();ctx.prev.not_type(z,oldT.transform,C.DistributionLogisticsActivity);reason('digital-transformation-is-not-physical-logistics',z)
query('DS-record-to-logistics-path',str(digital.value(digital.value(oldT.record,L.recordDigitalActivity),D.supportsLogistics)),str(T.logistics))
# Every original module still has an executable positive fixture. No count of
# passed fixtures is presented as proof that all its requirements are complete.
for module in ['RM','PV','BA','DS']:
 g=Graph().parse(base/('fixtures/'+module+'-1-positive.ttl'));check(module+'-original-positive-replay',g,True)
 if module=='RM':
  z=g+Graph();z.add((C.RiskTreatmentActivity,RDFS.subClassOf,OWL.Nothing));reason('RM-plan-does-not-require-execution',z,allowed_empty=['RiskTreatmentActivity'])
positive+=ba+digital
save('positive-abox.ttl',positive);save('fixtures.trig',ds)
write('test-results.json',{'admission':tests,'reasoner':logic,'queries':queries,'admission_pass':sum(x['pass'] for x in tests),'admission_total':len(tests),'reasoner_pass':sum(x['pass'] for x in logic),'reasoner_total':len(logic),'query_pass':sum(x['pass'] for x in queries),'query_total':len(queries),'limits':['New fixture data are synthetic. No statement of full native/UFO validity.','Ten optional native relations have pending stereotypes and universal bounds; profile min-counts are conditional data contracts.']})
print(json.dumps({'admission':str(sum(x['pass'] for x in tests))+'/'+str(len(tests)),'reasoner':str(sum(x['pass'] for x in logic))+'/'+str(len(logic)),'queries':str(sum(x['pass'] for x in queries))+'/'+str(len(queries)),'isolates_before':topology['prior_experiment']['isolates'],'isolates_after':topology['new_experiment']['isolates']}),flush=True)
assert all(x['pass'] for x in tests+logic+queries)
