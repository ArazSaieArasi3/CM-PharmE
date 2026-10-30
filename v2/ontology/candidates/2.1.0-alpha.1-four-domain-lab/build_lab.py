"""Build a separate, additive experiment; never modify the baseline candidate."""
import copy,json,hashlib
from pathlib import Path
from rdflib import Graph,Namespace,RDF,RDFS,OWL,XSD,BNode,Literal
from rdflib.collection import Collection
H=Path(__file__).resolve().parent
BASE=H.parent/'2.1.0-alpha.1-g3-p4a-supply-capacity'
C=Namespace('https://w3id.org/cm-pharme/2.1/')
L=Namespace('https://w3id.org/cm-pharme/experimental/four-domain/')
SH=Namespace('http://www.w3.org/ns/shacl#')
NEW={
 'RiskReviewActivity':('RM','An occurrence reviewing an earlier risk assessment/result. It need not repeat the assessment.'),
 'SignalAssessmentActivity':('PV','An occurrence assessing a medicinal safety signal; separate from reporting and from assessment content.'),
 'SystemDeploymentActivity':('DS','An actual installation/deployment of an identified component version in an organizational context. Not an ETL/provenance transformation.')}
# Universal ends are permissive; mandatory fields belong to opted-in admission profiles.
# (local property, source type, target type). Names denote candidate relations, not established project vocabulary.
RELS=[
 ('scenarioProduct','Assertion','MedicinalProduct'),('assessmentScenario','RiskAssessmentActivity','Assertion'),
 ('resultAssessment','Assertion','RiskAssessmentActivity'),('citesSourceRecord','Assertion','SourceRecord'),
 ('planRiskResult','RiskTreatmentPlan','Assertion'),('implementsRiskPlan','RiskTreatmentActivity','RiskTreatmentPlan'),
 ('reviewPriorResult','RiskReviewActivity','Assertion'),('reviewNewResult','RiskReviewActivity','Assertion'),
 ('reportsRecord','AdverseEventReportingActivity','SourceRecord'),('signalProduct','Assertion','MedicinalProduct'),
 ('signalSubstance','Assertion','PharmaceuticalSubstance'),('signalAssessmentTarget','SignalAssessmentActivity','Assertion'),
 ('pvResultSignal','Assertion','Assertion'),('pvResultAssessment','Assertion','SignalAssessmentActivity'),
 ('pvRequirementJurisdiction','PharmacovigilanceRequirement','RegulatoryJurisdiction'),
 ('surveillanceRequirement','PostMarketSurveillanceActivity','PharmacovigilanceRequirement'),
 ('surveillanceSource','PostMarketSurveillanceActivity','SourceRecord'),
 ('serviceCapability','ServiceOfferingSpecification','EnterpriseCapability'),('viewOrganization','BusinessArchitectureView','Organization'),
 ('viewService','BusinessArchitectureView','ServiceOfferingSpecification'),('capabilityRealizedIn','EnterpriseCapability','ManufacturingActivity'),
 ('deploymentComponent','SystemDeploymentActivity','DigitalInformationSystemComponent'),
 ('deploymentOrganization','SystemDeploymentActivity','Organization'),('digitalActivityDeployment','ProvenanceActivity','SystemDeploymentActivity'),
 ('recordDigitalActivity','SourceRecord','ProvenanceActivity'),('digitalServiceComponent','ServiceOfferingSpecification','DigitalInformationSystemComponent'),
 ('digitalServiceActivity','ServiceOfferingSpecification','ProvenanceActivity')]
DATA={'profile':XSD.string,'atTime':XSD.dateTime,'conclusion':XSD.string,'signalStatus':XSD.string,'componentVersion':XSD.string,'causallyEstablished':XSD.boolean}
DISJOINT=[('RiskAssessmentActivity','Assertion'),('RiskReviewActivity','Assertion'),('RiskTreatmentActivity','RiskTreatmentPlan'),
 ('AdverseEventReportingActivity','SourceRecord'),('SignalAssessmentActivity','Assertion'),('BusinessArchitectureView','Organization'),
 ('DigitalInformationSystemComponent','SourceRecord'),('SystemDeploymentActivity','SourceRecord')]
def uri(p):return C[p[2:]] if p.startswith('c:') else L[p]
g=Graph();g.bind('cmpe',C);g.bind('lab',L);g.bind('owl',OWL);g.bind('rdfs',RDFS);g.bind('xsd',XSD)
g.add((L.ontology,RDF.type,OWL.Ontology));g.add((L.ontology,RDFS.comment,Literal('Review experiment only. No release or full OntoUML conformance claim.')))
for n,(_,definition) in NEW.items():g.add((C[n],RDF.type,OWL.Class));g.add((C[n],RDFS.comment,Literal(definition)))
for p,s,t in RELS:g.add((L[p],RDF.type,OWL.ObjectProperty));g.add((L[p],RDFS.domain,C[s]));g.add((L[p],RDFS.range,C[t]))
for p,dt in DATA.items():g.add((L[p],RDF.type,OWL.DatatypeProperty));g.add((L[p],RDFS.range,dt))
for s,t in DISJOINT:g.add((C[s],OWL.disjointWith,C[t]))
g.add((L.viewOrganization,RDFS.subPropertyOf,C.baViewRepresents))
g.add((L.causallyEstablished,RDF.type,OWL.FunctionalProperty))
g.serialize(H/'delta.ttl',format='turtle')
base=Graph().parse(BASE/'active.ttl');(base+g).serialize(H/'experimental.owl.ttl',format='turtle')
# Native projection: keep every original element byte-value; append typed relations and three Events.
n=json.loads((BASE/'ontouml.json').read_text());es=n['elements'];by={e['id']:e for e in es};root=next(e for e in es if e['type']=='Package')
for ident,(domain,definition) in NEW.items():
 e=copy.deepcopy(by['RiskAssessmentActivity']);e.update(id=ident,name={'en':ident},description={'en':definition},created='2026-10-09',modified=None,properties=[],stereotype='event',restrictedTo=['event'])
 es.append(e);root['contents'].append(ident)
template_rel=next(e for e in es if e['type']=='BinaryRelation');template_end=next(e for e in es if e['type']=='Property')
for name,s,t in RELS:
 rid='lab-rel-'+name;props=[]
 for side,cls in [('source',s),('target',t)]:
  eid='lab-end-'+name+'-'+side;e=copy.deepcopy(template_end);e.update(id=eid,name={'en':eid},propertyType=cls,cardinality='0..*',subsettedProperties=[],redefinedProperties=[],description={'en':'Permissive relation end. Conditional admission requirements are in laboratory SHACL profiles, not universal mandatory participation.'});es.append(e);props.append(eid)
 e=copy.deepcopy(template_rel);e.update(id=rid,name={'en':name},properties=props,stereotype=None,description={'en':'Experimental typed association. OntoUML association stereotype requires P3 adjudication; null is explicit, not a validation certificate.'});es.append(e);root['contents'].append(rid)
n['id']='cm-pharme-four-domain-laboratory';n['name']={'en':'CM-PharmE four-domain experiment'};n['modified']='2026-10-09'
(H/'ontouml-experimental.json').write_text(json.dumps(n,ensure_ascii=False,indent=2)+'\n')
sh=Graph();sh.bind('sh',SH);sh.bind('lab',L);sh.bind('cmpe',C);sh.bind('xsd',XSD)
profiles={}
def profile(tag,cls,fields):
 shape=L['shape-'+tag];profiles[tag]={'type':cls,'fields':fields};sh.add((shape,RDF.type,SH.NodeShape));sh.add((shape,SH['class'],C[cls]))
 target=BNode();sh.add((shape,SH.target,target));sh.add((target,RDF.type,SH.SPARQLTarget));sh.add((target,SH.select,Literal(f'SELECT ?this WHERE {{ ?this <{L.profile}> "{tag}" . }}')))
 for p,typ,mi,ma in fields:
  ps=L['field-'+tag+'-'+p.replace(':','-')];sh.add((shape,SH.property,ps));sh.add((ps,SH.path,uri(p)));sh.add((ps,SH.minCount,Literal(mi)))
  if ma is not None:sh.add((ps,SH.maxCount,Literal(ma)))
  sh.add((ps,SH.datatype if typ.startswith('xsd:') else SH['class'],XSD[typ[4:]] if typ.startswith('xsd:') else C[typ]))
 return shape
def query_constraint(shape,ident,message,query):
 sc=L[ident];sh.add((shape,SH.sparql,sc));sh.add((sc,RDF.type,SH.SPARQLConstraint));sh.add((sc,SH.message,Literal(message)));sh.add((sc,SH.select,Literal(query)))
def same_node_guard(shape,a,b):
 query_constraint(shape,'distinct-'+a+'-'+b,'Content and real-world bearer/occurrence must not be the same node.',f'SELECT $this WHERE {{ $this a <{C[a]}> , <{C[b]}> . }}')
profile('risk-scenario','Assertion',[('scenarioProduct','MedicinalProduct',1,None)])
profile('risk-assessment','RiskAssessmentActivity',[('assessmentScenario','Assertion',1,None)])
rr=profile('risk-result','Assertion',[('resultAssessment','RiskAssessmentActivity',1,1),('citesSourceRecord','SourceRecord',1,None),('atTime','xsd:dateTime',1,1),('conclusion','xsd:string',1,1)])
same_node_guard(rr,'RiskAssessmentActivity','Assertion')
profile('risk-plan','RiskTreatmentPlan',[('planRiskResult','Assertion',1,None)])
profile('risk-treatment','RiskTreatmentActivity',[('implementsRiskPlan','RiskTreatmentPlan',1,None),('atTime','xsd:dateTime',1,1)])
rv=profile('risk-review','RiskReviewActivity',[('reviewPriorResult','Assertion',1,None),('reviewNewResult','Assertion',1,None),('atTime','xsd:dateTime',1,1)])
query_constraint(rv,'review-time-order','New result must not predate the prior result.',f'SELECT $this WHERE {{ $this <{L.reviewPriorResult}> ?old ; <{L.reviewNewResult}> ?new . ?old <{L.atTime}> ?a . ?new <{L.atTime}> ?b . FILTER(?b <= ?a) }}')
rp=profile('safety-reporting','AdverseEventReportingActivity',[('reportsRecord','SourceRecord',1,None),('atTime','xsd:dateTime',1,1)]);same_node_guard(rp,'AdverseEventReportingActivity','SourceRecord')
sg=profile('safety-signal','Assertion',[('signalProduct','MedicinalProduct',0,None),('signalSubstance','PharmaceuticalSubstance',0,None),('citesSourceRecord','SourceRecord',1,None)])
query_constraint(sg,'signal-target-required','A signal must name a product or substance.',f'SELECT $this WHERE {{ FILTER NOT EXISTS {{ $this <{L.signalProduct}> ?p }} FILTER NOT EXISTS {{ $this <{L.signalSubstance}> ?s }} }}')
profile('signal-assessment','SignalAssessmentActivity',[('signalAssessmentTarget','Assertion',1,None)])
sr=profile('signal-result','Assertion',[('pvResultSignal','Assertion',1,1),('pvResultAssessment','SignalAssessmentActivity',1,1),('atTime','xsd:dateTime',1,1),('signalStatus','xsd:string',1,1)])
same_node_guard(sr,'SignalAssessmentActivity','Assertion')
query_constraint(sr,'signal-result-distinct','An assessment result must not be its own assessed signal or a known alias of it.',f'SELECT $this WHERE {{ $this <{L.pvResultSignal}> ?s . FILTER($this = ?s || EXISTS {{ $this <{OWL.sameAs}> ?s }} || EXISTS {{ ?s <{OWL.sameAs}> $this }}) }}')
query_constraint(sr,'signal-result-agreement','The recorded result and producing assessment must refer to the same signal.',f'SELECT $this WHERE {{ $this <{L.pvResultSignal}> ?s ; <{L.pvResultAssessment}> ?a . FILTER NOT EXISTS {{ ?a <{L.signalAssessmentTarget}> ?s }} }}')
profile('pv-requirement','PharmacovigilanceRequirement',[('pvRequirementJurisdiction','RegulatoryJurisdiction',1,None)])
profile('pv-surveillance','PostMarketSurveillanceActivity',[('surveillanceRequirement','PharmacovigilanceRequirement',1,None),('surveillanceSource','SourceRecord',1,None)])
profile('ba-service','ServiceOfferingSpecification',[('serviceCapability','EnterpriseCapability',1,None)])
bv=profile('ba-view','BusinessArchitectureView',[('viewOrganization','Organization',1,None),('viewService','ServiceOfferingSpecification',0,None)]);same_node_guard(bv,'BusinessArchitectureView','Organization')
bp=profile('ba-partnership','StrategicPartnershipAgreement',[('c:partnershipParticipant','PartnerOrganizationRole',2,None)])
query_constraint(bp,'partners-not-known-aliases','Two known aliases do not establish two distinct organizations.',f'SELECT DISTINCT $this WHERE {{ $this <{C.partnershipParticipant}> ?a, ?b . ?a <{OWL.sameAs}> ?b . FILTER(?a != ?b) }}')
dep=profile('deployment','SystemDeploymentActivity',[('deploymentComponent','DigitalInformationSystemComponent',1,1),('deploymentOrganization','Organization',1,None),('componentVersion','xsd:string',1,1),('atTime','xsd:dateTime',1,1)])
da=profile('digital-activity','ProvenanceActivity',[('digitalActivityDeployment','SystemDeploymentActivity',1,1),('atTime','xsd:dateTime',1,1)])
query_constraint(da,'deployment-before-use','A deployment must not postdate its use.',f'SELECT $this WHERE {{ $this <{L.digitalActivityDeployment}> ?d ; <{L.atTime}> ?t . ?d <{L.atTime}> ?dt . FILTER(?dt > ?t) }}')
rec=profile('digital-record','SourceRecord',[('recordDigitalActivity','ProvenanceActivity',1,1)]);same_node_guard(rec,'SourceRecord','DigitalInformationSystemComponent')
profile('digital-service','ServiceOfferingSpecification',[('digitalServiceComponent','DigitalInformationSystemComponent',1,None),('digitalServiceActivity','ProvenanceActivity',1,None)])
sh.serialize(H/'profiles.shacl.ttl',format='turtle')
(Graph().parse(BASE/'constraints.ttl')+sh).serialize(H/'combined.shacl.ttl',format='turtle')
manifest={'status':'EXPERIMENT_NOT_RELEASE','baseline_commit':'a99ea1dc5a88f07d92f2ede08ce365c0a7f258a3','baseline_sha256':{x:hashlib.sha256((BASE/x).read_bytes()).hexdigest() for x in ['ontouml.json','active.ttl','constraints.ttl']},'new_classes':NEW,'new_relations':[{'name':p,'source':s,'target':t,'native_stereotype':'PENDING_P3','native_bounds':'0..* at both ends; profile restrictions are conditional'} for p,s,t in RELS],'profiles':profiles,'new_native_elements':len(es)-536,'native_total_elements':len(es),'new_datatype_fields':list(DATA),'native_projection_limits':['The six experimental admission/provenance fields are not new conceptual datatypes; their profile constraints are in SHACL only.','Eight OWL disjointness experiments are not yet reflected as native generalization sets.','Association stereotypes are unresolved; native schema/parser pass cannot close P3/P5.'],'reuse_decisions':{
 'RiskScenarioSpecification':'Assertion profile representing a scenario proposition; not an occurred Situation.',
 'RiskAssessmentResult':'Assertion profile; use ObservationResult only when a measured result is actually evidenced.',
 'SafetyReport':'SourceRecord report-carrier profile; identity of information content across distinct carriers remains open.',
 'SafetySignal':'Assertion profile for an evidential hypothesis; not an actual adverse event.',
 'SignalAssessmentResult':'Assertion profile with time/status and producing event.',
 'DigitalServiceSpecification':'Existing ServiceOfferingSpecification; DS imports the BA service specification interface.',
 'RiskReviewActivity':'New Event candidate; a review is not always a full reassessment.',
 'SignalAssessmentActivity':'New Event candidate; do not equate assessment with reporting or restrict all assessments to post-market surveillance.',
 'SystemDeploymentActivity':'New Event candidate; W3 defines ProvenanceActivity for transformation/ingestion, not arbitrary deployment.'}}
(H/'model-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'native_elements':len(es),'new_classes':len(NEW),'relations':len(RELS),'profiles':len(profiles)}))
