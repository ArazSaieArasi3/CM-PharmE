"""Bounded source-contract prototypes using CM-PharmE individuals.

All p: terms are an experimental admission/query vocabulary, not native concepts.
Inputs and results describe supplied assertions, not independently verified law.
"""
from pathlib import Path
import json
from rdflib import Graph,Namespace,RDF,RDFS,OWL,XSD,Literal,URIRef,BNode
from rdflib.collection import Collection
H=Path(__file__).resolve().parent
C=Namespace('https://w3id.org/cm-pharme/2.1/')
L=Namespace('https://w3id.org/cm-pharme/experimental/four-domain/')
R=Namespace('https://w3id.org/cm-pharme/experimental/refinement/')
P=Namespace('https://w3id.org/cm-pharme/experimental/registry-policy/')
T=Namespace('urn:cmpe-registry-policy:')
PROV=Namespace('http://www.w3.org/ns/prov#')
SH=Namespace('http://www.w3.org/ns/shacl#')
OLD=H.parent/'2.1.0-alpha.1-four-domain-refinement'
POLICY=H.parent/'2.1.0-alpha.1-content-event-policy'
ontology=Graph().parse(OLD/'experimental.owl.ttl')+Graph().parse(POLICY/'proposed-delta.ttl')
base_shapes=Graph().parse(OLD/'combined.shacl.ttl')+Graph().parse(POLICY/'proposed-shapes.ttl')
hierarchy=Graph()
for a,b in ontology.subject_objects(RDFS.subClassOf):
 if isinstance(a,URIRef) and isinstance(b,URIRef):hierarchy.add((a,RDFS.subClassOf,b))
def write(name,d):(H/name).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def save(g,name):
 f=H/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(g.serialize(format='turtle').rstrip()+'\n')
def graph():
 g=Graph()
 for prefix,ns in [('c',C),('l',L),('r',R),('p',P),('t',T),('prov',PROV),('owl',OWL),('xsd',XSD)]:g.bind(prefix,ns)
 return g
def types(g,n,*classes):
 for c in classes:g.add((n,RDF.type,c))
def value(g,s,p,v,datatype=None):g.add((s,p,Literal(v,datatype=datatype)))
def tag(g,s,name):value(g,s,P.profile,name)

def registry(kind='registration',organization_subject=False):
 g=graph();types(g,T.record,C.SourceRecord);tag(g,T.record,'registry-record')
 types(g,T.release,C.DatasetRelease);g.add((T.release,C.containsSourceRecord,T.record));g.add((T.record,P.release,T.release))
 types(g,T.reporter,C.Organization);g.add((T.record,PROV.wasAttributedTo,T.reporter))
 value(g,T.record,P.recordKind,kind);value(g,T.record,P.externalKey,'SYNTHETIC-001')
 value(g,T.record,P.retrievedAt,'2026-10-01T10:00:00Z',XSD.dateTime)
 value(g,T.record,P.approvalConclusion,'unknown')
 types(g,T.jurisdiction,C.RegulatoryJurisdiction)
 if kind=='registration':
  subject=T.reporter if organization_subject else T.facility
  types(g,subject,C.RegisteredParty,C.RegisteredOrganizationRole if organization_subject else C.RegisteredFacilityRole,C.Organization if organization_subject else C.Facility)
  types(g,T.fact,C.EstablishmentRegistration);types(g,T.authority,C.Organization,C.RegisteringAuthorityRole)
  # Explicit synthetic grounding for the inherited RegulatoryAuthorityRole.
  # This is not a claim about the legal mandate structure of the real FDA.
  types(g,T.mandate,C.RegulatoryMandate);types(g,T.conferrer,C.Organization,C.MandateConferringOrganizationRole)
  g.add((T.mandate,C.regulatoryMandateHolder,T.authority));g.add((T.mandate,C.regulatoryMandateCounterpart,T.conferrer))
  g.add((T.fact,C.registrationEntity,subject));g.add((T.fact,C.registrationAuthority,T.authority));g.add((T.fact,C.registrationJurisdiction,T.jurisdiction))
 else:
  subject=T.presentation;types(g,subject,C.MedicinalProductPresentation,C.ListedPresentationRole)
  types(g,T.product,C.MedicinalProduct);g.add((subject,C.presentationOf,T.product))
  types(g,T.fact,C.MarketListing);types(g,T.reporter,C.ListingResponsibleOrganizationRole)
  g.add((T.fact,C.listingPresentation,subject));g.add((T.fact,C.listingResponsibleOrganization,T.reporter));g.add((T.fact,C.listingJurisdiction,T.jurisdiction))
  value(g,T.record,P.marketingStart,'2026-09-01',XSD.date);value(g,T.record,P.marketingEnd,'2026-11-01',XSD.date)
 g.add((T.record,P.recordSubject,subject));g.add((T.record,P.representsFact,T.fact))
 return g

def reporting(scenario='routine'):
 g=graph();types(g,T.requirement,C.RegulatoryRequirement);tag(g,T.requirement,'reporting-scope')
 types(g,T.jurisdiction,C.RegulatoryJurisdiction);g.add((T.requirement,P.jurisdiction,T.jurisdiction))
 value(g,T.requirement,P.scenario,scenario);value(g,T.requirement,P.sourceVersion,'synthetic-guidance-snapshot-1')
 value(g,T.requirement,C.validFrom,'2026-10-01T00:00:00Z',XSD.dateTime)
 value(g,T.requirement,C.validTo,'2026-11-01T00:00:00Z',XSD.dateTime)
 for role in (['MAH'] if scenario=='routine' else ['MAH','NCA']):value(g,T.requirement,P.actorRole,role)
 for route in (['CAP'] if scenario=='routine' else ['CAP','NAP']):value(g,T.requirement,P.authorizationRoute,route)
 value(g,T.requirement,P.frequency,'awareness-and-new-information' if scenario=='routine' else 'synthetic-action-specific-frequency')
 if scenario!='routine':
  types(g,T.product,C.MedicinalProduct);g.add((T.requirement,P.scopedProduct,T.product))
  value(g,T.requirement,P.scopeComplete,True);value(g,T.requirement,P.actionAnnounced,True)
 return g

def provenance():
 g=graph();types(g,T.record,C.SourceRecord);types(g,T.activity,C.ProvenanceActivity)
 types(g,T.author,C.Organization);types(g,T.operator,C.Organization)
 tag(g,T.record,'provenance-record');g.add((T.record,L.recordDigitalActivity,T.activity))
 g.add((T.record,PROV.wasAttributedTo,T.author));g.add((T.activity,PROV.wasAssociatedWith,T.operator))
 value(g,T.record,P.version,'2');types(g,T.previous,C.SourceRecord);value(g,T.previous,P.version,'1')
 g.add((T.record,PROV.wasRevisionOf,T.previous));g.add((T.record,PROV.wasDerivedFrom,T.previous))
 g.add((T.record,OWL.differentFrom,T.previous));return g

def shortage():
 g=graph();types(g,T.claim,C.Assertion);tag(g,T.claim,'shortage-claim')
 types(g,T.product,C.MedicinalProduct);g.add((T.claim,C.assertionAboutProduct,T.product))
 value(g,T.claim,P.shortageStatus,'potential');return g

def submission():
 g=provenance();tag(g,T.record,'submission-record');types(g,T.claim,C.Assertion);types(g,T.product,C.MedicinalProduct)
 g.add((T.record,R.carrierClaim,T.claim));g.add((T.claim,C.assertionAboutProduct,T.product));value(g,T.record,P.payloadFormat,'SPL')
 return g

PREFIX='PREFIX p: <'+str(P)+'> PREFIX c: <'+str(C)+'> PREFIX l: <'+str(L)+'> PREFIX r: <'+str(R)+'> PREFIX prov: <'+str(PROV)+'> PREFIX owl: <'+str(OWL)+'>\n'
def shapes():
 s=graph();s.bind('sh',SH)
 def node(name,cls):
  n=P['shape-'+name];s.add((n,RDF.type,SH.NodeShape));s.add((n,SH['class'],cls));t=BNode();s.add((n,SH.target,t));s.add((t,RDF.type,SH.SPARQLTarget));s.add((t,SH.select,Literal(PREFIX+'SELECT ?this WHERE { ?this p:profile "'+name+'" }')));return n
 def field(n,p,minimum=1,maximum=1,cls=None,datatype=None,choices=None):
  f=BNode();s.add((n,SH.property,f));s.add((f,SH.path,p));s.add((f,SH.minCount,Literal(minimum)))
  if maximum is not None:s.add((f,SH.maxCount,Literal(maximum)))
  if cls:s.add((f,SH['class'],cls))
  if datatype:s.add((f,SH.datatype,datatype))
  if choices is not None:
   head=BNode();Collection(s,head,[Literal(x) for x in choices]);s.add((f,SH['in'],head))
 def rule(n,name,body):
  q=P[name];s.add((n,SH.sparql,q));s.add((q,SH.message,Literal(name)));s.add((q,SH.select,Literal(PREFIX+'SELECT $this WHERE { '+body+' }')))
 n=node('registry-record',C.SourceRecord)
 field(n,P.recordKind,choices=['registration','listing']);field(n,P.recordSubject);field(n,P.representsFact)
 field(n,P.release,cls=C.DatasetRelease);field(n,PROV.wasAttributedTo,cls=C.Organization)
 field(n,P.externalKey,datatype=XSD.string);field(n,P.retrievedAt,datatype=XSD.dateTime)
 field(n,P.approvalConclusion,choices=['unknown','source-asserted-approved','source-asserted-not-approved'])
 field(n,P.marketingStart,0,datatype=XSD.date);field(n,P.marketingEnd,0,datatype=XSD.date)
 rule(n,'record-not-subject','$this p:recordSubject ?x . $this (owl:sameAs|^owl:sameAs)* ?x .')
 rule(n,'record-not-fact','$this p:representsFact ?x . $this (owl:sameAs|^owl:sameAs)* ?x .')
 rule(n,'fact-kind-subject-agreement','{ $this p:recordKind "registration" ; p:recordSubject ?x ; p:representsFact ?f . FILTER NOT EXISTS { ?f a c:EstablishmentRegistration ; c:registrationEntity ?x } } UNION { $this p:recordKind "listing" ; p:recordSubject ?x ; p:representsFact ?f . FILTER NOT EXISTS { ?f a c:MarketListing ; c:listingPresentation ?x } }')
 rule(n,'approval-needs-independent-decision','$this p:approvalConclusion ?status ; p:recordSubject ?subject . FILTER(?status != "unknown") FILTER NOT EXISTS { $this p:approvalEvidence ?e . ?e a c:SourceRecord ; p:recordKind "regulatory-decision" ; p:recordSubject ?subject . FILTER(?e != $this) FILTER NOT EXISTS { $this (owl:sameAs|^owl:sameAs)+ ?e } }')
 rule(n,'marketing-interval-order','$this p:marketingStart ?s ; p:marketingEnd ?e . FILTER(?s >= ?e)')
 n=node('reporting-scope',C.RegulatoryRequirement)
 field(n,P.jurisdiction,cls=C.RegulatoryJurisdiction);field(n,P.scenario,choices=['routine','preparedness','crisis'])
 field(n,P.sourceVersion,datatype=XSD.string);field(n,C.validFrom,datatype=XSD.dateTime);field(n,C.validTo,datatype=XSD.dateTime)
 field(n,P.actorRole,maximum=None,choices=['MAH','NCA']);field(n,P.authorizationRoute,maximum=None,choices=['CAP','NAP'])
 field(n,P.frequency,datatype=XSD.string)
 rule(n,'scope-time-order','$this c:validFrom ?s ; c:validTo ?e . FILTER(?s >= ?e)')
 rule(n,'routine-scope-guard','$this p:scenario "routine" . { $this p:actorRole ?r . FILTER(?r != "MAH") } UNION { $this p:authorizationRoute ?r . FILTER(?r != "CAP") }')
 rule(n,'action-scope-required','$this p:scenario ?s . FILTER(?s != "routine") FILTER NOT EXISTS { $this p:actionAnnounced true ; p:scopeComplete true ; p:scopedProduct ?product . ?product a c:MedicinalProduct }')
 n=node('shortage-claim',C.Assertion);field(n,P.shortageStatus,choices=['potential','reported-actual']);field(n,C.assertionAboutProduct,cls=C.MedicinalProduct)
 rule(n,'claim-not-situation','$this (owl:sameAs|^owl:sameAs)* ?s . ?s a c:MedicineShortageSituation .')
 n=node('provenance-record',C.SourceRecord);field(n,L.recordDigitalActivity,cls=C.ProvenanceActivity);field(n,PROV.wasAttributedTo,cls=C.Organization)
 field(n,P.version,datatype=XSD.string)
 rule(n,'record-not-generating-activity','$this l:recordDigitalActivity ?a . $this (owl:sameAs|^owl:sameAs)* ?a .')
 rule(n,'associated-actor-required','$this l:recordDigitalActivity ?a . FILTER NOT EXISTS { ?a prov:wasAssociatedWith ?actor . ?actor a c:Organization }')
 rule(n,'revision-needs-lineage','$this prov:wasRevisionOf ?old . FILTER NOT EXISTS { $this prov:wasDerivedFrom ?old . ?old a c:SourceRecord ; p:version ?version }')
 rule(n,'revision-known-identity-collision','$this prov:wasRevisionOf ?old . $this (owl:sameAs|^owl:sameAs)* ?old .')
 n=node('submission-record',C.SourceRecord);field(n,R.carrierClaim,cls=C.Assertion);field(n,P.payloadFormat,choices=['SPL'])
 rule(n,'submission-subject-required','$this r:carrierClaim ?claim . FILTER NOT EXISTS { ?claim c:assertionAboutProduct ?product . ?product a c:MedicinalProduct }')
 rule(n,'payload-not-product','$this r:carrierClaim/c:assertionAboutProduct ?p . $this (owl:sameAs|^owl:sameAs)* ?p .')
 return s

def delta():
 d=graph();d.add((C.SourceRecord,OWL.disjointWith,C.ProvenanceActivity));d.add((C.Assertion,OWL.disjointWith,C.MedicineShortageSituation));return d

# These queries do not derive verified approval or actual shortage from a record.
QUERIES={
 'registered-subject':'SELECT ?subject WHERE { ?f a c:EstablishmentRegistration ; c:registrationEntity ?subject }',
 'listed-subject':'SELECT ?subject WHERE { ?f a c:MarketListing ; c:listingPresentation ?subject }',
 'submitter':'SELECT ?actor WHERE { t:record prov:wasAttributedTo ?actor }',
 'generation':'SELECT ?activity WHERE { t:record l:recordDigitalActivity ?activity }',
 'attribution-and-association':'SELECT ?author ?operator WHERE { t:record prov:wasAttributedTo ?author ; l:recordDigitalActivity ?a . ?a prov:wasAssociatedWith ?operator }',
 'derivation':'SELECT ?source WHERE { t:record prov:wasDerivedFrom ?source }',
 'revision':'SELECT ?source WHERE { t:record prov:wasRevisionOf ?source }',
 'represented-product':'SELECT ?product WHERE { t:record r:carrierClaim/c:assertionAboutProduct ?product }',
 'source-asserted-shortage':'SELECT ?status WHERE { t:claim p:shortageStatus ?status }',
 'actual-shortage-instances':'SELECT ?s WHERE { ?s a c:MedicineShortageSituation }',
 'frequency':'SELECT ?f WHERE { t:requirement p:frequency ?f }'
}
def query(g,key):return sorted([list(map(str,row)) for row in g.query(PREFIX+'PREFIX t: <'+str(T)+'>\n'+QUERIES[key])])
def approval_answer(g):
 q='ASK { t:record p:approvalEvidence ?e ; p:recordSubject ?subject . ?e a c:SourceRecord ; p:recordKind "regulatory-decision" ; p:recordSubject ?subject . FILTER(?e != t:record) FILTER NOT EXISTS { t:record (owl:sameAs|^owl:sameAs)+ ?e } }'
 known=bool(g.query(PREFIX+'PREFIX t: <'+str(T)+'>\n'+q))
 return 'SOURCE_DECISION_AVAILABLE_NOT_VERIFIED' if known else 'UNKNOWN'
def lookup(g,key):
 # No global negative conclusion follows from missing membership in this release.
 found=any((T.release,C.containsSourceRecord,r) in g for r in g.subjects(P.externalKey,Literal(key)))
 return {'source_result':'FOUND' if found else 'NOT_FOUND_IN_RELEASE','approval':'UNKNOWN'}
def window(g,on_date):
 from datetime import date
 start=g.value(T.record,P.marketingStart);end=g.value(T.record,P.marketingEnd)
 if start is None or end is None:return 'UNKNOWN'
 d=date.fromisoformat(on_date)
 return 'WITHIN_DECLARED_WINDOW' if start.toPython()<=d<end.toPython() else 'OUTSIDE_DECLARED_WINDOW'
def applicability(g,role,route,product=T.product,jurisdiction=T.jurisdiction,at='2026-10-10T00:00:00Z',scenario=None):
 from datetime import datetime
 def one(p):return g.value(T.requirement,p)
 roles=list(g.objects(T.requirement,P.actorRole));routes=list(g.objects(T.requirement,P.authorizationRoute))
 if any(x is None for x in [role,route,product,jurisdiction,at,one(P.jurisdiction),one(P.scenario),one(C.validFrom),one(C.validTo)]):return 'UNKNOWN'
 if not roles or not routes:return 'UNKNOWN'
 if scenario is not None and str(one(P.scenario))!=scenario:return 'NOT_APPLICABLE_IN_PROFILE'
 if jurisdiction!=one(P.jurisdiction) or Literal(role) not in roles or Literal(route) not in routes:return 'NOT_APPLICABLE_IN_PROFILE'
 moment=datetime.fromisoformat(at.replace('Z','+00:00'))
 # xsd:dateTime can legally omit a timezone; do not invent one for comparison.
 if any(d.tzinfo is None for d in [moment,one(C.validFrom).toPython(),one(C.validTo).toPython()]):return 'UNKNOWN'
 if not one(C.validFrom).toPython()<=moment<one(C.validTo).toPython():return 'NOT_APPLICABLE_IN_PROFILE'
 if str(one(P.scenario))!='routine':
  if one(P.actionAnnounced)!=Literal(True):return 'UNKNOWN'
  if (T.requirement,P.scopedProduct,product) not in g:
   return 'NOT_APPLICABLE_IN_PROFILE' if one(P.scopeComplete)==Literal(True) else 'UNKNOWN'
 return 'APPLICABLE_IN_PROFILE'
