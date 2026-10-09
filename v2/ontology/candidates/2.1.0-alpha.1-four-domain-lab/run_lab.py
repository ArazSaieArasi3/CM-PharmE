"""Independent scenario witnesses for the review experiment, using real SHACL/OWL engines."""
import json,copy,hashlib,gzip,base64,platform
from pathlib import Path
from tempfile import TemporaryDirectory
from rdflib import Graph,Namespace,RDF,RDFS,OWL,XSD,BNode,Literal
from pyshacl import validate
from owlrl import DeductiveClosure,OWLRL_Semantics
from owlready2 import World,sync_reasoner
from owlready2.base import OwlReadyInconsistentOntologyError
H=Path(__file__).resolve().parent;BASE=H.parent/'2.1.0-alpha.1-g3-p4a-supply-capacity'
C=Namespace('https://w3id.org/cm-pharme/2.1/');L=Namespace('https://w3id.org/cm-pharme/experimental/four-domain/');T=Namespace('urn:cmpe-lab:')
SH=Namespace('http://www.w3.org/ns/shacl#');PFX=f'PREFIX c: <{C}> PREFIX l: <{L}> PREFIX t: <{T}> '
shapes=Graph().parse(H/'combined.shacl.ttl');oldshapes=Graph().parse(BASE/'constraints.ttl');owl=Graph().parse(H/'experimental.owl.ttl')
def graph():
 g=Graph();g.bind('c',C);g.bind('l',L);g.bind('t',T);g.bind('xsd',XSD);return g
def ty(g,s,c):g.add((T[s],RDF.type,C[c]))
def obj(g,s,p,o):g.add((T[s],C[p[2:]] if p.startswith('c:') else L[p],T[o]))
def lit(g,s,p,value,dt=None):g.add((T[s],L[p],Literal(value,datatype=dt)))
def profile(g,s,c,tag):ty(g,s,c);lit(g,s,'profile',tag)
def at(g,s,day):lit(g,s,'atTime',f'2026-10-{day:02}T10:00:00Z',XSD.dateTime)
def clone(g):return graph()+g
def remove(g,s,p):g.remove((T[s],C[p[2:]] if p.startswith('c:') else L[p],None))
def rm():
 g=graph();ty(g,'product','MedicinalProduct');ty(g,'source','SourceRecord')
 profile(g,'scenario','Assertion','risk-scenario');obj(g,'scenario','scenarioProduct','product')
 profile(g,'assessment','RiskAssessmentActivity','risk-assessment');obj(g,'assessment','assessmentScenario','scenario')
 profile(g,'riskResult','Assertion','risk-result');obj(g,'riskResult','resultAssessment','assessment');obj(g,'riskResult','citesSourceRecord','source');at(g,'riskResult',1);lit(g,'riskResult','conclusion','review supply continuity')
 profile(g,'plan','RiskTreatmentPlan','risk-plan');obj(g,'plan','planRiskResult','riskResult')
 return g
def rm_boundary():
 g=rm();profile(g,'assessment2','RiskAssessmentActivity','risk-assessment');obj(g,'assessment2','assessmentScenario','scenario')
 profile(g,'riskResult2','Assertion','risk-result');obj(g,'riskResult2','resultAssessment','assessment2');obj(g,'riskResult2','citesSourceRecord','source');at(g,'riskResult2',2);lit(g,'riskResult2','conclusion','revised assessment')
 profile(g,'review','RiskReviewActivity','risk-review');obj(g,'review','reviewPriorResult','riskResult');obj(g,'review','reviewNewResult','riskResult2');at(g,'review',2)
 profile(g,'action','RiskTreatmentActivity','risk-treatment');obj(g,'action','implementsRiskPlan','plan');at(g,'action',3)
 return g
def pv():
 g=graph();ty(g,'medicine','MedicinalProduct');ty(g,'report','SourceRecord');ty(g,'jA','RegulatoryJurisdiction');ty(g,'jB','RegulatoryJurisdiction')
 profile(g,'reporting','AdverseEventReportingActivity','safety-reporting');obj(g,'reporting','reportsRecord','report');at(g,'reporting',1)
 profile(g,'signal','Assertion','safety-signal');obj(g,'signal','signalProduct','medicine');obj(g,'signal','citesSourceRecord','report')
 profile(g,'signalAssessment','SignalAssessmentActivity','signal-assessment');obj(g,'signalAssessment','signalAssessmentTarget','signal')
 profile(g,'signalResult','Assertion','signal-result');obj(g,'signalResult','pvResultSignal','signal');obj(g,'signalResult','pvResultAssessment','signalAssessment');at(g,'signalResult',2);lit(g,'signalResult','signalStatus','under-review')
 profile(g,'pvRule','PharmacovigilanceRequirement','pv-requirement');obj(g,'pvRule','pvRequirementJurisdiction','jA')
 profile(g,'surveillance','PostMarketSurveillanceActivity','pv-surveillance');obj(g,'surveillance','surveillanceRequirement','pvRule');obj(g,'surveillance','surveillanceSource','report')
 return g
def pv_boundary():
 g=pv();remove(g,'signal','signalProduct');ty(g,'substance','PharmaceuticalSubstance');obj(g,'signal','signalSubstance','substance');ty(g,'study','SourceRecord');remove(g,'signal','citesSourceRecord');obj(g,'signal','citesSourceRecord','study')
 profile(g,'reporting2','AdverseEventReportingActivity','safety-reporting');obj(g,'reporting2','reportsRecord','report');at(g,'reporting2',3)
 profile(g,'signalAssessment2','SignalAssessmentActivity','signal-assessment');obj(g,'signalAssessment2','signalAssessmentTarget','signal')
 profile(g,'signalResult2','Assertion','signal-result');obj(g,'signalResult2','pvResultSignal','signal');obj(g,'signalResult2','pvResultAssessment','signalAssessment2');at(g,'signalResult2',3);lit(g,'signalResult2','signalStatus','refuted-at-this-time')
 return g
def ba():
 g=graph();ty(g,'org','Organization');ty(g,'org2','Organization');ty(g,'cap','EnterpriseCapability');obj(g,'cap','c:capabilityBearer','org')
 profile(g,'service','ServiceOfferingSpecification','ba-service');obj(g,'service','serviceCapability','cap')
 profile(g,'view','BusinessArchitectureView','ba-view');obj(g,'view','viewOrganization','org');obj(g,'view','viewService','service')
 profile(g,'agreement','StrategicPartnershipAgreement','ba-partnership')
 for o in ['org','org2']:ty(g,o,'PartnerOrganizationRole');obj(g,'agreement','c:partnershipParticipant',o)
 g.add((T.org,OWL.differentFrom,T.org2));return g
def ba_boundary():
 g=ba();g.remove((T.view,None,None));ty(g,'product','MedicinalProduct');ty(g,'facility','Facility');return g
def ds():
 g=graph();ty(g,'component','DigitalInformationSystemComponent');ty(g,'operator','Organization')
 profile(g,'deployment','SystemDeploymentActivity','deployment');obj(g,'deployment','deploymentComponent','component');obj(g,'deployment','deploymentOrganization','operator');lit(g,'deployment','componentVersion','1.0');at(g,'deployment',1)
 profile(g,'transform','ProvenanceActivity','digital-activity');obj(g,'transform','digitalActivityDeployment','deployment');at(g,'transform',2)
 profile(g,'record','SourceRecord','digital-record');obj(g,'record','recordDigitalActivity','transform')
 profile(g,'digitalService','ServiceOfferingSpecification','digital-service');obj(g,'digitalService','digitalServiceComponent','component');obj(g,'digitalService','digitalServiceActivity','transform')
 return g
def ds_boundary():
 g=ds();ty(g,'operator2','Organization')
 profile(g,'deployment2','SystemDeploymentActivity','deployment');obj(g,'deployment2','deploymentComponent','component');obj(g,'deployment2','deploymentOrganization','operator2');lit(g,'deployment2','componentVersion','2.0');at(g,'deployment2',3)
 profile(g,'transform2','ProvenanceActivity','digital-activity');obj(g,'transform2','digitalActivityDeployment','deployment2');at(g,'transform2',4)
 profile(g,'record2','SourceRecord','digital-record');obj(g,'record2','recordDigitalActivity','transform2');return g
POS={'RM':rm,'PV':pv,'BA':ba,'DS':ds};BOUND={'RM':rm_boundary,'PV':pv_boundary,'BA':ba_boundary,'DS':ds_boundary}
all_results=[];fixtures=H/'fixtures';fixtures.mkdir(exist_ok=True)
def check(module,group,name,g,expected,expected_marker=None):
 conforms,report,_=validate(g,shacl_graph=shapes,advanced=True,inference='none',abort_on_first=False)
 failures=[{'path':str(report.value(r,SH.resultPath) or ''),'constraint':str(report.value(r,SH.sourceConstraint) or ''),'component':str(report.value(r,SH.sourceConstraintComponent) or ''),'focus':str(report.value(r,SH.focusNode) or '')} for r in report.subjects(RDF.type,SH.ValidationResult)]
 marker=expected_marker is None or any(expected_marker in str(x) for x in failures)
 fn=f'{module}-{group}-{name}.ttl';g.serialize(fixtures/fn,format='turtle')
 row={'scenario':f'SC-{module}-{group:02}','name':name,'expected_conforms':expected,'actual_conforms':bool(conforms),'expected_failure_marker':expected_marker,'failure_marker_seen':marker,'violations':failures,'fixture':'fixtures/'+fn,'pass':bool(conforms)==expected and marker};all_results.append(row);return row
for m,f in POS.items():check(m,1,'positive',f(),True)
for m,f in BOUND.items():check(m,2,'boundary',f(),True)
# Independent negative witnesses, fixed before executing the shapes.
NEG=[
 ('RM','missing-scenario-topic',rm,lambda g:remove(g,'scenario','scenarioProduct'),'scenarioProduct'),
 ('RM','missing-evidence',rm,lambda g:remove(g,'riskResult','citesSourceRecord'),'citesSourceRecord'),
 ('RM','dangling-plan-result',rm,lambda g:(remove(g,'plan','planRiskResult'),obj(g,'plan','planRiskResult','unknown')),'planRiskResult'),
 ('RM','result-is-assessment',rm,lambda g:ty(g,'riskResult','RiskAssessmentActivity'),'distinct-RiskAssessmentActivity'),
 ('RM','missing-review-predecessor',rm_boundary,lambda g:remove(g,'review','reviewPriorResult'),'reviewPriorResult'),
 ('RM','backdated-revision',rm_boundary,lambda g:(remove(g,'riskResult2','atTime'),at(g,'riskResult2',1)),'review-time-order'),
 ('RM','dangling-executed-plan',rm_boundary,lambda g:(remove(g,'action','implementsRiskPlan'),obj(g,'action','implementsRiskPlan','unknown')),'implementsRiskPlan'),
 ('PV','missing-target',pv,lambda g:remove(g,'signal','signalProduct'),'signal-target-required'),
 ('PV','missing-signal-source',pv,lambda g:remove(g,'signal','citesSourceRecord'),'citesSourceRecord'),
 ('PV','dangling-signal',pv,lambda g:(remove(g,'signalResult','pvResultSignal'),obj(g,'signalResult','pvResultSignal','unknown')),'pvResultSignal'),
 ('PV','missing-result-time',pv,lambda g:remove(g,'signalResult','atTime'),'atTime'),
 ('PV','missing-jurisdiction',pv,lambda g:remove(g,'pvRule','pvRequirementJurisdiction'),'pvRequirementJurisdiction'),
 ('PV','reporting-is-record',pv,lambda g:ty(g,'reporting','SourceRecord'),'distinct-AdverseEventReportingActivity'),
 ('PV','signal-is-own-result',pv,lambda g:(remove(g,'signalResult','pvResultSignal'),obj(g,'signalResult','pvResultSignal','signalResult')),'signal-result-distinct'),
 ('PV','signal-result-alias',pv,lambda g:g.add((T.signal,OWL.sameAs,T.signalResult)),'signal-result-distinct'),
 ('PV','result-assessment-target-disagreement',pv,lambda g:(ty(g,'otherSignal','Assertion'),remove(g,'signalAssessment','signalAssessmentTarget'),obj(g,'signalAssessment','signalAssessmentTarget','otherSignal')),'signal-result-agreement'),
 ('BA','missing-capability-bearer',ba,lambda g:remove(g,'cap','c:capabilityBearer'),'capabilityBearer'),
 ('BA','service-without-capability',ba,lambda g:remove(g,'service','serviceCapability'),'serviceCapability'),
 ('BA','view-is-organization',ba,lambda g:ty(g,'view','Organization'),'distinct-BusinessArchitectureView'),
 ('BA','untyped-view-reference',ba,lambda g:(remove(g,'view','viewOrganization'),obj(g,'view','viewOrganization','unknown')),'viewOrganization'),
 ('BA','one-partner-only',ba,lambda g:g.remove((T.agreement,C.partnershipParticipant,T.org2)),'partnershipParticipant'),
 ('BA','known-partner-aliases',ba,lambda g:g.add((T.org,OWL.sameAs,T.org2)),'partners-not-known-aliases'),
 ('DS','missing-version',ds,lambda g:remove(g,'deployment','componentVersion'),'componentVersion'),
 ('DS','missing-generating-activity',ds,lambda g:remove(g,'record','recordDigitalActivity'),'recordDigitalActivity'),
 ('DS','record-is-component',ds,lambda g:ty(g,'record','DigitalInformationSystemComponent'),'distinct-SourceRecord'),
 ('DS','missing-deployment-time',ds,lambda g:remove(g,'deployment','atTime'),'atTime'),
 ('DS','deployment-after-use',ds,lambda g:(remove(g,'deployment','atTime'),at(g,'deployment',3)),'deployment-before-use'),
 ('DS','service-without-supported-activity',ds,lambda g:remove(g,'digitalService','digitalServiceActivity'),'digitalServiceActivity')]
for m,name,base,mutation,marker in NEG:g=base();mutation(g);check(m,3,name,g,False,marker)
# Fixed CQ result oracles are not generated from the shape definitions.
QUERIES=[
 ('RM',1,'SELECT ?scenario ?assessment ?product ?evidence WHERE { t:riskResult l:resultAssessment ?assessment ; l:citesSourceRecord ?evidence . ?assessment l:assessmentScenario ?scenario . ?scenario l:scenarioProduct ?product }',[['urn:cmpe-lab:scenario','urn:cmpe-lab:assessment','urn:cmpe-lab:product','urn:cmpe-lab:source']]),
 ('RM',2,'SELECT ?plan WHERE { ?plan l:planRiskResult t:riskResult . FILTER NOT EXISTS { ?a l:implementsRiskPlan ?plan } }',[['urn:cmpe-lab:plan']]),
 ('RM',3,'SELECT ?old ?new ?source ?conclusion WHERE { t:review l:reviewPriorResult ?old ; l:reviewNewResult ?new . ?new l:citesSourceRecord ?source ; l:conclusion ?conclusion }',[['urn:cmpe-lab:riskResult','urn:cmpe-lab:riskResult2','urn:cmpe-lab:source','revised assessment']]),
 ('PV',1,'SELECT ?target ?source WHERE { t:signal l:signalSubstance ?target ; l:citesSourceRecord ?source }',[['urn:cmpe-lab:substance','urn:cmpe-lab:study']]),
 ('PV',2,'SELECT ?assessment ?status ?time WHERE { ?r l:pvResultSignal t:signal ; l:pvResultAssessment ?assessment ; l:signalStatus ?status ; l:atTime ?time }',[['urn:cmpe-lab:signalAssessment','under-review','2026-10-02T10:00:00+00:00'],['urn:cmpe-lab:signalAssessment2','refuted-at-this-time','2026-10-03T10:00:00+00:00']]),
 ('PV',3,'SELECT ?activity ?requirement ?jurisdiction WHERE { ?activity l:surveillanceRequirement ?requirement . ?requirement l:pvRequirementJurisdiction ?jurisdiction }',[['urn:cmpe-lab:surveillance','urn:cmpe-lab:pvRule','urn:cmpe-lab:jA']]),
 ('BA',1,'SELECT ?org WHERE { t:cap c:capabilityBearer ?org . FILTER NOT EXISTS { t:cap l:capabilityRealizedIn ?x } }',[['urn:cmpe-lab:org']]),
 ('BA',2,'SELECT ?cap WHERE { t:service l:serviceCapability ?cap }',[['urn:cmpe-lab:cap']]),
 ('BA',3,'SELECT ?artifact ?org WHERE { { ?artifact a c:BusinessArchitectureView ; l:viewOrganization ?org } UNION { ?artifact a c:StrategicPartnershipAgreement ; c:partnershipParticipant ?org } }',[['urn:cmpe-lab:view','urn:cmpe-lab:org'],['urn:cmpe-lab:agreement','urn:cmpe-lab:org'],['urn:cmpe-lab:agreement','urn:cmpe-lab:org2']]),
 ('DS',1,'SELECT ?component ?version WHERE { t:record l:recordDigitalActivity/l:digitalActivityDeployment ?d . ?d l:deploymentComponent ?component ; l:componentVersion ?version }',[['urn:cmpe-lab:component','1.0']]),
 ('DS',2,'SELECT ?activity ?component ?operator WHERE { t:record l:recordDigitalActivity ?activity . ?activity l:digitalActivityDeployment ?deployment . ?deployment l:deploymentComponent ?component ; l:deploymentOrganization ?operator }',[['urn:cmpe-lab:transform','urn:cmpe-lab:component','urn:cmpe-lab:operator']]),
 ('DS',3,'SELECT ?org ?version ?time WHERE { ?d l:deploymentOrganization ?org ; l:componentVersion ?version ; l:atTime ?time }',[['urn:cmpe-lab:operator','1.0','2026-10-01T10:00:00+00:00'],['urn:cmpe-lab:operator2','2.0','2026-10-03T10:00:00+00:00']])]
qr=[]
for m,num,q,expected in QUERIES:
 g=BOUND[m]() if (m,num) in [('RM',3),('PV',1),('PV',2),('DS',1),('DS',2),('DS',3)] else POS[m]()
 actual=sorted([[str(v) for v in row] for row in g.query(PFX+q)])
 qr.append({'id':f'CQ-{m}-{num:02}','query':PFX+q,'expected':sorted(expected),'actual':actual,'pass':actual==sorted(expected)})
(H/'cq-results.json').write_text(json.dumps(qr,indent=2)+'\n')
# Bounded rule-closure checks. These are not full OWL-DL non-entailment proofs.
ne=[]
for m in POS:
 g=owl+POS[m]();DeductiveClosure(OWLRL_Semantics).expand(g)
 if m=='RM':ok=not list(g.triples((None,L.implementsRiskPlan,T.plan))) and (T.scenario,RDF.type,C.DisruptionEvent) not in g
 if m=='PV':ok=(T.signal,L.causallyEstablished,Literal(True)) not in g and (T.pvRule,L.pvRequirementJurisdiction,T.jB) not in g
 if m=='BA':ok=not list(g.triples((T.cap,L.capabilityRealizedIn,None))) and (T.service,RDF.type,C.ManufacturingActivity) not in g
 if m=='DS':ok=not list(g.subjects(RDF.type,C.RegulatoryAuthorization)) and (T.record,RDF.type,C.DigitalInformationSystemComponent) not in g
 ne.append({'scenario':f'SC-{m}-04','method':'OWL-RL closure: bounded unwanted-triple absence','pass':ok})
shacl_summary={'cases':all_results,'case_count':len(all_results),'pass_count':sum(r['pass'] for r in all_results),'cq_count':len(qr),'cq_pass':sum(r['pass'] for r in qr),'rule_closure':ne}
(H/'shacl-results.json').write_text(json.dumps(shacl_summary,indent=2)+'\n')
print(json.dumps({'shacl':f"{shacl_summary['pass_count']}/{len(all_results)}",'cqs':f"{sum(r['pass'] for r in qr)}/12",'rule_closure':ne}),flush=True)
# Verify the independent module witnesses together.
combined=graph()
for f in BOUND.values():combined+=f()
check('ALL',1,'combined-domains',combined,True)
combined.serialize(H/'combined-positive.ttl',format='turtle')
def reason(name,data,expected=True,coherence=False,extra=None):
 with TemporaryDirectory() as td:
  path=Path(td)/'x.rdf';(owl+data+(extra or Graph())).serialize(path,format='xml');w=World();w.get_ontology(path.as_uri()).load()
  try:
   sync_reasoner(w,debug=0);consistent=True;unsat=[str(c.iri) for c in w.inconsistent_classes() if c.iri!=str(OWL.Nothing)] if coherence else []
  except OwlReadyInconsistentOntologyError:consistent=False;unsat=[]
  finally:w.close()
 row={'name':name,'expected_consistent':expected,'actual_consistent':consistent,'unsatisfiable_named_classes':unsat,'pass':consistent==expected and not unsat};print(json.dumps(row),flush=True);return row
rr=[]
rr.append(reason('experimental-tbox-coherence',graph(),True,True))
rr.append(reason('all-four-modules-positive',combined,True,True))
for m,(s,cls) in {'RM':('riskResult','RiskAssessmentActivity'),'PV':('reporting','SourceRecord'),'BA':('view','Organization'),'DS':('record','DigitalInformationSystemComponent')}.items():
 g=POS[m]();ty(g,s,cls);rr.append(reason(m+'-identity-collision',g,False))
# Explicit countermodels for absence of unwanted existence/type implications.
def max_zero(subject,prop,inverse=False):
 x=Graph();r=BNode();p=prop
 if inverse:p=BNode();x.add((p,OWL.inverseOf,prop))
 x.add((T[subject],RDF.type,r));x.add((r,RDF.type,OWL.Restriction));x.add((r,OWL.onProperty,p));x.add((r,OWL.maxCardinality,Literal(0,datatype=XSD.nonNegativeInteger)));return x
rr.append(reason('RM-plan-with-zero-executions-countermodel',rm(),True,extra=max_zero('plan',L.implementsRiskPlan,True)))
rr.append(reason('BA-capability-with-zero-exercises-countermodel',ba(),True,extra=max_zero('cap',L.capabilityRealizedIn)))
g=pv();lit(g,'signal','causallyEstablished',False,XSD.boolean);rr.append(reason('PV-signal-without-established-causality-countermodel',g))
x=Graph();x.add((C.RegulatoryAuthorization,OWL.equivalentClass,OWL.Nothing));rr.append(reason('DS-record-with-no-authorization-in-model-countermodel',ds(),True,extra=x))
# Empty authorization class is deliberate only in this countermodel, not a coherence test.
empty_jur=Graph();neg=BNode();empty_jur.add((neg,RDF.type,OWL.NegativePropertyAssertion));empty_jur.add((neg,OWL.sourceIndividual,T.pvRule));empty_jur.add((neg,OWL.assertionProperty,L.pvRequirementJurisdiction));empty_jur.add((neg,OWL.targetIndividual,T.jB));empty_jur.add((T.jA,OWL.differentFrom,T.jB));rr.append(reason('PV-jurisdiction-B-not-implied-countermodel',pv(),True,extra=empty_jur))
(H/'reasoner-results.json').write_text(json.dumps({'engine':'HermiT bundled with Owlready2 0.49','cases':rr,'pass_count':sum(r['pass'] for r in rr),'case_count':len(rr),'countermodel_note':'Consistency of added negations/max-zero establishes the scoped non-entailment only; it does not validate causality or a regulatory rule.'},indent=2)+'\n')
# Real-data nonregression uses existing bounded published sample, not new empirical domain support.
encoded=H.parent/'2.1.0-alpha.1-g3-3-d-real-source-migration/real-source-abox.nt.gz.b64'
raw=gzip.decompress(base64.b64decode(encoded.read_text()));real=Graph().parse(data=raw.decode(),format='nt');assert len(real)==39272
old=validate(real,shacl_graph=oldshapes,advanced=True,inference='none')[0]
new,report,_=validate(real,shacl_graph=shapes,advanced=True,inference='none')
real_result={'triples':len(real),'sample_rows':768,'source_sha256':hashlib.sha256(raw).hexdigest(),'old_shapes_conform':bool(old),'experimental_shapes_conform':bool(new),'violations':len(list(report.subjects(RDF.type,SH.ValidationResult))),'experimental_profile_nodes':len(set(real.subjects(L.profile,None))),'meaning':'Nonregression only; this sample supplies no new witness for the four experimental profiles.'}
real_result['reasoner']=reason('existing-NHIF-ABox-with-experiment',real,True,True)
(H/'real-regression.json').write_text(json.dumps(real_result,indent=2)+'\n')
# One pre-existing positive and a corrupt capacity witness protect a concrete prior change.
cap=graph();ty(cap,'capacity','SupplyCapacity');ty(cap,'capacityOrg','Organization');obj(cap,'capacityOrg','c:organizationHasSupplyCapacity','capacity')
check('REG',1,'typed-capacity-preserved',cap,True)
cap.remove((T.capacityOrg,C.organizationHasSupplyCapacity,T.capacity));check('REG',3,'bearer-free-capacity-rejected',cap,False)
scenario=[]
for m in POS:
 for k in [1,2,3,4]:
  cases=[x for x in all_results if x['scenario']==f'SC-{m}-{k:02}'] if k<4 else [x for x in ne if x['scenario']==f'SC-{m}-04']
  scenario.append({'id':f'SC-{m}-{k:02}','executed_subcases':len(cases),'pass':bool(cases) and all(x['pass'] for x in cases),'coverage':'bounded operationalization; remaining semantic limits in report'})
summary={'status':'BOUNDED_EXPERIMENT_ONLY','versions':{'python':platform.python_version(),'rdflib':__import__('rdflib').__version__,'pyshacl':__import__('pyshacl').__version__,'owlready2':__import__('owlready2').VERSION},'shacl_cases':len(all_results),'shacl_pass':sum(x['pass'] for x in all_results),'cq_cases':len(qr),'cq_pass':sum(x['pass'] for x in qr),'reasoner_cases':len(rr)+1,'reasoner_pass':sum(x['pass'] for x in rr)+int(real_result['reasoner']['pass']),'scenario_families':scenario,'scenario_family_pass':sum(x['pass'] for x in scenario),'real_sample_regression':real_result,'full_official_antipattern_detector_run':False,'new_scientific_approval':False,'release_gate_closed':False}
summary['all_executed_expectations_pass']=all(x['pass'] for x in all_results+qr+rr+ne) and bool(new) and real_result['reasoner']['pass']
(H/'shacl-results.json').write_text(json.dumps({'cases':all_results,'case_count':len(all_results),'pass_count':sum(x['pass'] for x in all_results),'rule_closure':ne},indent=2)+'\n')
(H/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ['scenario_families','real_sample_regression']}),flush=True)
if not summary['all_executed_expectations_pass']:raise SystemExit(1)
