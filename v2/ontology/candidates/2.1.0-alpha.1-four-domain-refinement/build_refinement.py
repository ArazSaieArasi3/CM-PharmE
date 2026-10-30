"""Add scoped refinements to the frozen prior laboratory, not the release candidate."""
import json,copy,hashlib
from pathlib import Path
from rdflib import Graph,Namespace,RDF,RDFS,OWL,XSD,BNode,Literal
H=Path(__file__).resolve().parent;OLD=H.parent/'2.1.0-alpha.1-four-domain-lab'
C=Namespace('https://w3id.org/cm-pharme/2.1/');L=Namespace('https://w3id.org/cm-pharme/experimental/four-domain/');R=Namespace('https://w3id.org/cm-pharme/experimental/refinement/');SH=Namespace('http://www.w3.org/ns/shacl#')
RELS=[('scenarioFacility','Assertion','Facility','X-RM-CONTEXT'),('scenarioDependency','Assertion','SupplyDependency','X-RM-CONTEXT'),
 ('carrierClaim','SourceRecord','Assertion','X-PV-CARRIER'),('assessmentOrganization','SignalAssessmentActivity','Organization','X-PV-ACTOR'),
 ('serviceProduct','ServiceOfferingSpecification','MedicinalProduct','X-BA-SERVICE'),('serviceFacility','ServiceOfferingSpecification','Facility','X-BA-SERVICE'),
 ('agreementCommitment','StrategicPartnershipAgreement','Assertion','X-BA-COMMITMENT'),('commitmentActor','Assertion','Organization','X-BA-COMMITMENT'),
 ('supportsManufacturing','ProvenanceActivity','ManufacturingActivity','X-DS-PHARMA'),('manufacturingProduct','ManufacturingActivity','MedicinalProduct','X-DS-PHARMA'),
 ('manufacturingFacility','ManufacturingActivity','Facility','X-DS-PHARMA'),('activityResponsibleOrganization','ProvenanceActivity','Organization','X-DS-RESPONSIBILITY')]
DATA=['caseIdentifier','caseIdentifierScheme','claimText','commitmentText']
g=Graph();g.bind('c',C);g.bind('l',L);g.bind('r',R);g.bind('owl',OWL)
for p,s,t,req in RELS:g.add((R[p],RDF.type,OWL.ObjectProperty));g.add((R[p],RDFS.domain,C[s]));g.add((R[p],RDFS.range,C[t]))
for p in DATA:g.add((R[p],RDF.type,OWL.DatatypeProperty));g.add((R[p],RDFS.range,XSD.string))
g.add((L.scenarioProduct,RDFS.subPropertyOf,C.assertionAboutProduct));g.add((L.signalProduct,RDFS.subPropertyOf,C.assertionAboutProduct))
g.serialize(H/'delta.ttl',format='turtle');(Graph().parse(OLD/'experimental.owl.ttl')+g).serialize(H/'experimental.owl.ttl',format='turtle')
sh=Graph().parse(OLD/'combined.shacl.ttl');sh.bind('r',R)
profiles={}
def uri(p):return {'c':C,'l':L,'r':R}[p[0]][p[2:]]
def shape(tag,cls,fields):
 s=R['shape-'+tag];sh.add((s,RDF.type,SH.NodeShape));sh.add((s,SH['class'],C[cls]));profiles[tag]={'type':cls,'fields':fields}
 t=BNode();sh.add((s,SH.target,t));sh.add((t,RDF.type,SH.SPARQLTarget));sh.add((t,SH.select,Literal(f'SELECT ?this WHERE {{ ?this <{L.profile}> "{tag}" }}')))
 for p,typ,mi,ma in fields:
  ps=R['field-'+tag+'-'+p[2:]];sh.add((s,SH.property,ps));sh.add((ps,SH.path,uri(p)));sh.add((ps,SH.minCount,Literal(mi)))
  if ma is not None:sh.add((ps,SH.maxCount,Literal(ma)))
  sh.add((ps,SH.datatype if typ.startswith('xsd:') else SH['class'],XSD[typ[4:]] if typ.startswith('xsd:') else C[typ]))
 return s
def constraint(s,name,msg,query):
 n=R[name];sh.add((s,SH.sparql,n));sh.add((n,RDF.type,SH.SPARQLConstraint));sh.add((n,SH.message,Literal(msg)));sh.add((n,SH.select,Literal(query)))
# Broaden the opted-in scenario topic contract: one of three typed contexts, not product-only.
sh.set((L['field-risk-scenario-scenarioProduct'],SH.minCount,Literal(0)))
rs=shape('risk-scenario','Assertion',[('r:scenarioFacility','Facility',0,None),('r:scenarioDependency','SupplyDependency',0,None)])
constraint(rs,'scenarioProduct-or-context-required','A product, facility or dependency context is required.',f'SELECT $this WHERE {{ FILTER NOT EXISTS {{ $this <{L.scenarioProduct}> ?p }} FILTER NOT EXISTS {{ $this <{R.scenarioFacility}> ?f }} FILTER NOT EXISTS {{ $this <{R.scenarioDependency}> ?d }} }}')
rc=shape('report-carrier','SourceRecord',[('r:carrierClaim','Assertion',1,None),('r:caseIdentifier','xsd:string',1,1),('r:caseIdentifierScheme','xsd:string',1,1)])
shape('report-claim','Assertion',[('r:claimText','xsd:string',1,1)])
constraint(rc,'carrier-not-claim','A carrier is not its own carried claim or a known alias of that claim.',f'SELECT $this WHERE {{ $this <{R.carrierClaim}> ?c . FILTER($this = ?c || EXISTS {{ $this <{OWL.sameAs}> ?c }} || EXISTS {{ ?c <{OWL.sameAs}> $this }}) }}')
shape('attributed-signal-assessment','SignalAssessmentActivity',[('r:assessmentOrganization','Organization',1,None)])
svc=shape('pharma-service','ServiceOfferingSpecification',[('l:serviceCapability','EnterpriseCapability',1,None),('r:serviceProduct','MedicinalProduct',0,None),('r:serviceFacility','Facility',0,None)])
constraint(svc,'pharma-service-context','A pharmaceutical service needs a product or facility context.',f'SELECT $this WHERE {{ FILTER NOT EXISTS {{ $this <{R.serviceProduct}> ?p }} FILTER NOT EXISTS {{ $this <{R.serviceFacility}> ?f }} }}')
agreement=shape('documented-partnership','StrategicPartnershipAgreement',[('r:agreementCommitment','Assertion',1,None)])
shape('commitment-assertion','Assertion',[('r:commitmentActor','Organization',2,None),('r:commitmentText','xsd:string',1,1)])
constraint(agreement,'commitment-evidence-required','Commitment requires the existing EvidenceSupport/SourceRecord pattern.',f'SELECT $this WHERE {{ $this <{R.agreementCommitment}> ?c . FILTER NOT EXISTS {{ ?e a <{C.EvidenceSupport}> ; <{C.evidenceAssertion}> ?c ; <{C.evidenceRecord}> ?s . ?c a <{C.SupportedAssertionRole}> . ?s a <{C.SourceRecord}> , <{C.EvidenceSourceRecordRole}> . }} }}')
constraint(agreement,'commitment-participant-agreement','The commitment actor set and agreement participant set must agree in this bounded admission profile.',f'SELECT $this WHERE {{ $this <{R.agreementCommitment}> ?c . {{ ?c <{R.commitmentActor}> ?org . FILTER NOT EXISTS {{ $this <{C.partnershipParticipant}> ?org }} }} UNION {{ $this <{C.partnershipParticipant}> ?org . FILTER NOT EXISTS {{ ?c <{R.commitmentActor}> ?org }} }} }}')
shape('manufacturing-context','ManufacturingActivity',[('r:manufacturingProduct','MedicinalProduct',1,None),('r:manufacturingFacility','Facility',1,None)])
dig=shape('manufacturing-data-activity','ProvenanceActivity',[('r:supportsManufacturing','ManufacturingActivity',1,None),('r:activityResponsibleOrganization','Organization',1,None)])
# Linked objects are validated even if their tag was accidentally omitted.
sh.add((R['field-manufacturing-data-activity-supportsManufacturing'],SH.node,R['shape-manufacturing-context']))
sh.add((R['field-report-carrier-carrierClaim'],SH.node,R['shape-report-claim']))
sh.add((R['field-documented-partnership-agreementCommitment'],SH.node,R['shape-commitment-assertion']))
digital=shape('manufacturing-digital-service','ServiceOfferingSpecification',[('l:digitalServiceActivity','ProvenanceActivity',1,None)])
sh.add((R['field-manufacturing-digital-service-digitalServiceActivity'],SH.node,R['shape-manufacturing-data-activity']))
constraint(digital,'service-component-agreement','Every supported activity deployment component must be listed as a service component.',f'SELECT $this WHERE {{ $this <{L.digitalServiceActivity}> ?a . ?a <{L.digitalActivityDeployment}>/<{L.deploymentComponent}> ?c . FILTER NOT EXISTS {{ $this <{L.digitalServiceComponent}> ?c }} }}')
sh.serialize(H/'combined.shacl.ttl',format='turtle')
n=json.loads((OLD/'ontouml-experimental.json').read_text());es=n['elements'];by={e['id']:e for e in es};root=next(e for e in es if e['type']=='Package')
for name,s,t,req in RELS:
 rid='refine-rel-'+name;props=[]
 for side,cls in [('source',s),('target',t)]:
  e=copy.deepcopy(by['lab-end-scenarioProduct-'+side]);e.update(id='refine-end-'+name+'-'+side,name={'en':name+'-'+side},propertyType=cls,cardinality='0..*');es.append(e);props.append(e['id'])
 e=copy.deepcopy(by['lab-rel-scenarioProduct']);e.update(id=rid,name={'en':name},properties=props,description={'en':req+'; review association, no approved OntoUML stereotype.'});es.append(e);root['contents'].append(rid)
n['id']='cm-pharme-four-domain-refinement';n['name']={'en':'CM-PharmE four-domain refinement experiment'}
(H/'ontouml-experimental.json').write_text(json.dumps(n,ensure_ascii=False,indent=2)+'\n')
manifest={'status':'EXPERIMENT_NOT_RELEASE','baseline_commit':'17b5d12e160033f3a1bd814bc580e4fb81fb753e','new_classes':0,'additional_relations':len(RELS),'total_experimental_relation_decisions':27+len(RELS),'profiles':profiles,'relations':[{'name':p,'source':s,'target':t,'requirement':r,'native_stereotype':None,'bounds':'0..*; local admission is separate'} for p,s,t,r in RELS],
 'old_package_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OLD.iterdir() if p.is_file()},
 'reuse':['EvidenceSupport, SupportedAssertionRole, EvidenceSourceRecordRole and their existing mediation relations','assertionAboutProduct as superproperty for the two content-specific product links','No caseIdentifier owl:hasKey or inverse-functional carrierClaim'],
 'limits':['Report claim is a proposition, not complete report content','Profile constraints are not universal OntoUML identity axioms','Native/OWL/SHACL alignment and 39 relation stereotypes need adjudication']}
(H/'model-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'new_classes':0,'additional_relations':len(RELS),'native_elements':len(es)}))
