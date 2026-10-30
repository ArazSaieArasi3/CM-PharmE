"""Fixed witnesses for the eight declared refinement contracts plus prior regressions."""
import json,gzip,base64,hashlib
from pathlib import Path
from tempfile import TemporaryDirectory
from rdflib import Graph,Namespace,RDF,OWL,XSD,BNode,Literal
from pyshacl import validate
from owlready2 import World,sync_reasoner
from owlready2.base import OwlReadyInconsistentOntologyError
H=Path(__file__).resolve().parent;OLD=H.parent/'2.1.0-alpha.1-four-domain-lab'
C=Namespace('https://w3id.org/cm-pharme/2.1/');L=Namespace('https://w3id.org/cm-pharme/experimental/four-domain/');R=Namespace('https://w3id.org/cm-pharme/experimental/refinement/');T=Namespace('urn:cmpe-lab:');SH=Namespace('http://www.w3.org/ns/shacl#')
shapes=Graph().parse(H/'combined.shacl.ttl');owl=Graph().parse(H/'experimental.owl.ttl');(H/'fixtures').mkdir(exist_ok=True)
def dump(name,x):(H/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def base(m,bound=False):return Graph().parse(OLD/'fixtures'/f'{m}-{2 if bound else 1}-{"boundary" if bound else "positive"}.ttl')
def ty(g,s,*classes):
 for c in classes:g.add((T[s],RDF.type,C[c]))
def obj(g,s,p,o):g.add((T[s],p,T[o]))
def lit(g,s,p,v):g.add((T[s],p,Literal(v)))
def tag(g,s,t):lit(g,s,L.profile,t)
def rm(which='product'):
 g=base('RM')
 if which!='product':g.remove((T.scenario,L.scenarioProduct,None))
 if which=='facility':ty(g,'riskFacility','Facility');obj(g,'scenario',R.scenarioFacility,'riskFacility')
 if which=='dependency':
  ty(g,'dependency','SupplyDependency');ty(g,'dependent','DependentEntity');ty(g,'provider','ProviderEntity')
  obj(g,'dependency',C.dependencyDependent,'dependent');obj(g,'dependency',C.dependencyProvider,'provider');obj(g,'scenario',R.scenarioDependency,'dependency')
 return g
def carrier(changed=False):
 g=base('PV');tag(g,'reportedClaim','report-claim');ty(g,'reportedClaim','Assertion');lit(g,'reportedClaim',R.claimText,'A source reports a suspected event; causation is unestablished.')
 for record,claim in [('report','reportedClaim'),('reportCopy','updatedClaim' if changed else 'reportedClaim')]:
  ty(g,record,'SourceRecord');tag(g,record,'report-carrier');obj(g,record,R.carrierClaim,claim);lit(g,record,R.caseIdentifier,'SYNTHETIC-CASE-1');lit(g,record,R.caseIdentifierScheme,'synthetic-local-case-id-not-E2B-conformance')
 if changed:ty(g,'updatedClaim','Assertion');tag(g,'updatedClaim','report-claim');lit(g,'updatedClaim',R.claimText,'Follow-up changes the reported clinical claim.');g.add((T.reportedClaim,OWL.differentFrom,T.updatedClaim))
 g.add((T.report,OWL.differentFrom,T.reportCopy))
 ty(g,'copyReporting','AdverseEventReportingActivity');tag(g,'copyReporting','safety-reporting');obj(g,'copyReporting',L.reportsRecord,'reportCopy');g.add((T.copyReporting,L.atTime,Literal('2026-10-03T10:00:00Z',datatype=XSD.dateTime)))
 return g
def actor(two=False):
 g=base('PV',two)
 for activity,org in [('signalAssessment','assessorA')]+([('signalAssessment2','assessorB')] if two else []):
  tag(g,activity,'attributed-signal-assessment');ty(g,org,'Organization');obj(g,activity,R.assessmentOrganization,org)
 return g
def service(facility=False):
 g=base('BA');tag(g,'service','pharma-service');ty(g,'serviceProduct','MedicinalProduct');ty(g,'serviceFacility','Facility')
 obj(g,'service',R.serviceFacility if facility else R.serviceProduct,'serviceFacility' if facility else 'serviceProduct');return g
def commitment():
 g=base('BA');tag(g,'agreement','documented-partnership');obj(g,'agreement',R.agreementCommitment,'commitment')
 ty(g,'commitment','Assertion','SupportedAssertionRole');tag(g,'commitment','commitment-assertion');lit(g,'commitment',R.commitmentText,'Synthetic organizations commit to the stated joint service.')
 for o in ['org','org2']:obj(g,'commitment',R.commitmentActor,o)
 ty(g,'commitmentRecord','SourceRecord','EvidenceSourceRecordRole','EvidenceItem');ty(g,'commitmentEvidence','EvidenceSupport')
 obj(g,'commitmentEvidence',C.evidenceAssertion,'commitment');obj(g,'commitmentEvidence',C.evidenceRecord,'commitmentRecord');obj(g,'commitmentEvidence',C.evidenceItem,'commitmentRecord');return g
def casual():
 g=Graph();ty(g,'contactRecord','SourceRecord');ty(g,'contactClaim','Assertion');ty(g,'org','Organization');ty(g,'org2','Organization')
 obj(g,'contactRecord',R.carrierClaim,'contactClaim');lit(g,'contactClaim',R.claimText,'Two organizations met; no agreement is asserted.');return g
def digital(two=False):
 g=base('DS',two);ty(g,'manufacturing','ManufacturingActivity');tag(g,'manufacturing','manufacturing-context');ty(g,'manufacturedProduct','MedicinalProduct');ty(g,'manufacturingSite','Facility')
 obj(g,'manufacturing',R.manufacturingProduct,'manufacturedProduct');obj(g,'manufacturing',R.manufacturingFacility,'manufacturingSite')
 ty(g,'processor','Organization');g.add((T.processor,OWL.differentFrom,T.operator))
 for a in ['transform']+(['transform2'] if two else []):
  tag(g,a,'manufacturing-data-activity');obj(g,a,R.supportsManufacturing,'manufacturing');obj(g,a,R.activityResponsibleOrganization,'processor')
 tag(g,'digitalService','manufacturing-digital-service');return g
def surveillance(study=False):return base('PV',study)
CASES=[]
def check(req,name,g,expected,marker=None,fixture=None):
 conforms,report,_=validate(g,shacl_graph=shapes,advanced=True,inference='none')
 violations=[{'path':str(report.value(x,SH.resultPath) or ''),'constraint':str(report.value(x,SH.sourceConstraint) or ''),'focus':str(report.value(x,SH.focusNode) or '')} for x in report.subjects(RDF.type,SH.ValidationResult)]
 good=bool(conforms)==expected and (marker is None or any(marker in str(v) for v in violations))
 fn=f'fixtures/{req}-{name}.ttl' if fixture is None else fixture
 if fixture is None:g.serialize(H/fn,format='turtle')
 CASES.append({'requirement':req,'name':name,'expected_conforms':expected,'actual_conforms':bool(conforms),'expected_marker':marker,'violations':violations,'fixture':fn,'pass':good})
POS={'X-RM-CONTEXT':lambda:rm(),'X-PV-CARRIER':carrier,'X-PV-ACTOR':actor,'X-BA-SERVICE':service,'X-BA-COMMITMENT':commitment,'X-DS-PHARMA':digital,'X-DS-RESPONSIBILITY':digital,'X-PV-SURVEILLANCE':surveillance}
BOUND={'X-RM-CONTEXT':lambda:rm('facility'),'X-PV-CARRIER':lambda:carrier(True),'X-PV-ACTOR':lambda:actor(True),'X-BA-SERVICE':lambda:service(True),'X-BA-COMMITMENT':casual,'X-DS-PHARMA':lambda:digital(True),'X-DS-RESPONSIBILITY':lambda:digital(True),'X-PV-SURVEILLANCE':lambda:surveillance(True)}
for req,f in POS.items():check(req,'positive',f(),True)
for req,f in BOUND.items():check(req,'boundary',f(),True)
check('X-RM-CONTEXT','dependency-boundary',rm('dependency'),True)
NEG=[
 ('X-RM-CONTEXT','missing-context',lambda:rm('none'),lambda g:None,'scenarioProduct-or-context-required'),
 ('X-RM-CONTEXT','untyped-facility',lambda:rm('facility'),lambda g:g.remove((T.riskFacility,RDF.type,None)),'scenarioFacility'),
 ('X-PV-CARRIER','missing-claim',carrier,lambda g:g.remove((T.report,R.carrierClaim,None)),'carrierClaim'),
 ('X-PV-CARRIER','missing-claim-content',carrier,lambda g:g.remove((T.reportedClaim,R.claimText,None)),'carrierClaim'),
 ('X-PV-CARRIER','carrier-as-claim',carrier,lambda g:(ty(g,'report','Assertion'),g.remove((T.report,R.carrierClaim,None)),obj(g,'report',R.carrierClaim,'report')),'carrier-not-claim'),
 ('X-PV-ACTOR','missing-actor',actor,lambda g:g.remove((T.signalAssessment,R.assessmentOrganization,None)),'assessmentOrganization'),
 ('X-PV-ACTOR','untyped-actor',actor,lambda g:g.remove((T.assessorA,RDF.type,None)),'assessmentOrganization'),
 ('X-BA-SERVICE','missing-pharma-context',service,lambda g:g.remove((T.service,R.serviceProduct,None)),'pharma-service-context'),
 ('X-BA-SERVICE','untyped-product',service,lambda g:g.remove((T.serviceProduct,RDF.type,None)),'serviceProduct'),
 ('X-BA-COMMITMENT','missing-commitment',commitment,lambda g:g.remove((T.agreement,R.agreementCommitment,None)),'agreementCommitment'),
 ('X-BA-COMMITMENT','missing-source-evidence',commitment,lambda g:g.remove((T.commitmentEvidence,C.evidenceRecord,None)),'commitment-evidence-required'),
 ('X-BA-COMMITMENT','outside-actor',commitment,lambda g:(ty(g,'outsider','Organization'),obj(g,'commitment',R.commitmentActor,'outsider')),'commitment-participant-agreement'),
 ('X-DS-PHARMA','missing-manufacturing',digital,lambda g:g.remove((T.transform,R.supportsManufacturing,None)),'supportsManufacturing'),
 ('X-DS-PHARMA','missing-manufactured-product',digital,lambda g:g.remove((T.manufacturing,R.manufacturingProduct,None)),'manufacturingProduct'),
 ('X-DS-PHARMA','service-component-disagreement',digital,lambda g:(g.remove((T.digitalService,L.digitalServiceComponent,None)),ty(g,'otherComponent','DigitalInformationSystemComponent'),obj(g,'digitalService',L.digitalServiceComponent,'otherComponent')),'service-component-agreement'),
 ('X-DS-RESPONSIBILITY','missing-responsibility',digital,lambda g:g.remove((T.transform,R.activityResponsibleOrganization,None)),'activityResponsibleOrganization'),
 ('X-DS-RESPONSIBILITY','untyped-responsible-actor',digital,lambda g:g.remove((T.processor,RDF.type,None)),'activityResponsibleOrganization'),
 ('X-PV-SURVEILLANCE','missing-source',surveillance,lambda g:g.remove((T.surveillance,L.surveillanceSource,None)),'surveillanceSource'),
 ('X-PV-SURVEILLANCE','untyped-source',surveillance,lambda g:g.remove((T.report,RDF.type,C.SourceRecord)),'surveillanceSource')]
for req,name,f,mutation,marker in NEG:g=f();mutation(g);check(req,name,g,False,marker)
dump('refinement-shacl-results.json',CASES)
# All 39 previous fixture expectations are replayed with the refined shapes.
REG=[]
for old in json.loads((OLD/'shacl-results.json').read_text())['cases']:
 g=Graph().parse(OLD/old['fixture']);check('PREVIOUS',old['name'],g,old['expected_conforms'],old['expected_failure_marker'],str(Path('../'+OLD.name)/old['fixture']));REG.append(CASES.pop())
dump('prior-regression-results.json',REG)
print(json.dumps({'new_shacl':sum(x['pass'] for x in CASES),'new_total':len(CASES),'prior_regression':sum(x['pass'] for x in REG),'prior_total':len(REG)}),flush=True)

PFX=f'PREFIX c: <{C}> PREFIX l: <{L}> PREFIX r: <{R}> PREFIX t: <{T}> '
QUERIES=[
 ('X-RM-CONTEXT',lambda:rm('facility'),'SELECT ?facility WHERE { t:assessment l:assessmentScenario/r:scenarioFacility ?facility }',[['urn:cmpe-lab:riskFacility']]),
 ('X-PV-CARRIER',lambda:carrier(True),'SELECT ?record ?case ?claim WHERE { ?record r:caseIdentifier ?case ; r:carrierClaim ?claim }',[['urn:cmpe-lab:report','SYNTHETIC-CASE-1','urn:cmpe-lab:reportedClaim'],['urn:cmpe-lab:reportCopy','SYNTHETIC-CASE-1','urn:cmpe-lab:updatedClaim']]),
 ('X-PV-ACTOR',lambda:actor(True),'SELECT ?org ?status ?time WHERE { ?result l:pvResultAssessment/r:assessmentOrganization ?org ; l:signalStatus ?status ; l:atTime ?time }',[['urn:cmpe-lab:assessorA','under-review','2026-10-02T10:00:00+00:00'],['urn:cmpe-lab:assessorB','refuted-at-this-time','2026-10-03T10:00:00+00:00']]),
 ('X-BA-SERVICE',service,'SELECT ?product ?capability WHERE { t:service r:serviceProduct ?product ; l:serviceCapability ?capability }',[['urn:cmpe-lab:serviceProduct','urn:cmpe-lab:cap']]),
 ('X-BA-COMMITMENT',commitment,'SELECT ?org ?source WHERE { t:agreement r:agreementCommitment ?claim . ?claim r:commitmentActor ?org . ?e c:evidenceAssertion ?claim ; c:evidenceRecord ?source }',[['urn:cmpe-lab:org','urn:cmpe-lab:commitmentRecord'],['urn:cmpe-lab:org2','urn:cmpe-lab:commitmentRecord']]),
 ('X-DS-PHARMA',digital,'SELECT ?manufacturing ?product ?facility WHERE { t:transform r:supportsManufacturing ?manufacturing . ?manufacturing r:manufacturingProduct ?product ; r:manufacturingFacility ?facility }',[['urn:cmpe-lab:manufacturing','urn:cmpe-lab:manufacturedProduct','urn:cmpe-lab:manufacturingSite']]),
 ('X-DS-RESPONSIBILITY',digital,'SELECT ?responsible ?operator WHERE { t:transform r:activityResponsibleOrganization ?responsible ; l:digitalActivityDeployment/l:deploymentOrganization ?operator }',[['urn:cmpe-lab:processor','urn:cmpe-lab:operator']]),
 ('X-PV-SURVEILLANCE',surveillance,'SELECT ?source ?requirement WHERE { t:surveillance l:surveillanceSource ?source ; l:surveillanceRequirement ?requirement }',[['urn:cmpe-lab:report','urn:cmpe-lab:pvRule']])]
Q=[]
for req,f,q,expected in QUERIES:
 actual=sorted([[str(v) for v in row] for row in f().query(PFX+q)]);Q.append({'requirement':req,'query':PFX+q,'expected':sorted(expected),'actual':actual,'pass':actual==sorted(expected)})
dump('cq-results.json',Q)

RR=[]
def reason(name,data,consistent=True,coherence=False):
 with TemporaryDirectory() as td:
  p=Path(td)/'model.rdf';(owl+data).serialize(p,format='xml');w=World();w.get_ontology(p.as_uri()).load()
  try:sync_reasoner(w,debug=0);actual=True;unsat=[str(c.iri) for c in w.inconsistent_classes() if c.iri!=str(OWL.Nothing)] if coherence else []
  except OwlReadyInconsistentOntologyError:actual=False;unsat=[]
  finally:w.close()
 row={'name':name,'expected_consistent':consistent,'actual_consistent':actual,'unsatisfiable_named_classes':unsat,'pass':actual==consistent and not unsat};RR.append(row);print(json.dumps(row),flush=True)
combined=Graph()
for f in POS.values():combined+=f()
combined.serialize(H/'combined-positive.ttl',format='turtle');check('COMBINED','all-refinements',combined,True)
reason('refined-tbox-coherence',Graph(),True,True);reason('combined-refinements',combined,True,True)
reason('same-case-distinct-carriers-and-updated-claims',carrier(True))
g=casual();n=BNode();g.add((n,OWL.complementOf,C.PartnerOrganizationRole));g.add((T.org,RDF.type,n));g.add((T.org2,RDF.type,n));reason('casual-contact-with-no-partner-role-countermodel',g)
reason('responsible-organization-different-from-deployer',digital())
g=actor();n=BNode();g.add((n,OWL.complementOf,C.RegulatoryAuthorityRole));g.add((T.assessorA,RDF.type,n));reason('assessor-not-necessarily-regulator-countermodel',g)
# Deliberately corrupt a known identity separation to exercise the reasoner.
g=digital();ty(g,'record','DigitalInformationSystemComponent');reason('record-component-collision',g,False)
encoded=H.parent/'2.1.0-alpha.1-g3-3-d-real-source-migration/real-source-abox.nt.gz.b64'
raw=gzip.decompress(base64.b64decode(encoded.read_text()));real=Graph().parse(data=raw.decode(),format='nt')
conforms,report,_=validate(real,shacl_graph=shapes,advanced=True,inference='none');reason('existing-real-sample-regression',real,True,True)
REAL={'rows':768,'triples':len(real),'sha256':hashlib.sha256(raw).hexdigest(),'shacl_conforms':bool(conforms),'violations':len(list(report.subjects(RDF.type,SH.ValidationResult))),'new_profile_witnesses':0,'scope':'nonregression only'}
dump('real-regression.json',REAL);dump('reasoner-results.json',RR);dump('refinement-shacl-results.json',CASES)
contracts=json.loads((H/'contracts.json').read_text())['requirements'];trace=[]
for r in contracts:
 cases=[c for c in CASES if c['requirement']==r['id']];query=next(q for q in Q if q['requirement']==r['id'])
 trace.append({'id':r['id'],'parent_requirements':r['parent_requirements'],'source_ids':r['source_ids'],'fixture_paths':[x['fixture'] for x in cases],'case_count':len(cases),'test_expectations_pass':all(c['pass'] for c in cases) and query['pass'],'scientific_acceptance':False})
dump('traceability.json',trace)
summary={'status':'BOUNDED_REFINEMENT_NOT_RELEASE','refinement_contracts':8,'contracts_with_passing_witnesses':sum(x['test_expectations_pass'] for x in trace),'new_shacl_cases':len(CASES),'new_shacl_pass':sum(x['pass'] for x in CASES),'prior_shacl_cases':len(REG),'prior_shacl_pass':sum(x['pass'] for x in REG),'new_cq_cases':len(Q),'new_cq_pass':sum(x['pass'] for x in Q),'reasoner_cases':len(RR),'reasoner_pass':sum(x['pass'] for x in RR),'all_executed_expectations_pass':all(x['pass'] for x in CASES+REG+Q+RR) and bool(conforms),'new_scientific_acceptance':False,'full_antipattern_run':False}
dump('summary.json',summary);print(json.dumps(summary),flush=True)
if not summary['all_executed_expectations_pass']:raise SystemExit(1)
