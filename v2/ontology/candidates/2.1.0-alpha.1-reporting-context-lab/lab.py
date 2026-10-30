"""Source-bound reporting/claim laboratory. No baseline or native edits.

The three proposed classes are information descriptions, not activities, legal
authorizations or world-level facts. Tokens remain an interface vocabulary.
"""
from pathlib import Path
import importlib.util,sys,json,hashlib
from datetime import datetime
from rdflib import Graph,Dataset,Namespace,URIRef,BNode,Literal,RDF,RDFS,OWL,XSD
from rdflib.collection import Collection
from pyshacl import validate
H=Path(__file__).resolve().parent
PREV=H.parent/'2.1.0-alpha.1-prov-target-lab'
s=importlib.util.spec_from_file_location('previous_prov_lab',PREV/'common.py');prev=importlib.util.module_from_spec(s);s.loader.exec_module(prev)
C,R,P,PROV,SH=prev.C,prev.R,prev.P,prev.PROV,prev.SH
B=Namespace('https://w3id.org/cm-pharme/experimental/reporting-context/')
T=Namespace('urn:cmpe-context:')
def write(name,data):(H/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def graph():
 g=Graph()
 for n,v in [('c',C),('r',R),('b',B),('t',T),('prov',PROV),('xsd',XSD),('owl',OWL)]:g.bind(n,v)
 return g
def value(g,n,p,v,dt=None):g.add((n,p,Literal(v,datatype=dt)))
def typ(g,n,c):g.add((n,RDF.type,c))
def model():
 g=graph()
 for cls,parent in [(B.StructuredClaim,C.Assertion),(B.ReportingContextDescription,C.Assertion),(B.ReportingScopeSpecification,C.RegulatoryRequirement)]:
  typ(g,cls,OWL.Class);g.add((cls,RDFS.subClassOf,parent))
  g.add((cls,OWL.disjointWith,C.SourceRecord))
 # Data/description relationships have no axiom that asserts described relations.
 for p,domain,range_ in [
  (B.claimSubject,B.StructuredClaim,None),(B.objectResource,B.StructuredClaim,None),
  (B.specificationSource,B.ReportingScopeSpecification,C.SourceRecord),
  (B.contextActor,B.ReportingContextDescription,C.Organization),
  (B.contextProduct,B.ReportingContextDescription,C.MedicinalProduct),
  (B.contextPresentation,B.ReportingContextDescription,C.MedicinalProductPresentation),
  (B.contextJurisdiction,B.ReportingContextDescription,C.RegulatoryJurisdiction),
  (B.scopeJurisdiction,B.ReportingScopeSpecification,C.RegulatoryJurisdiction),
  (B.scopedProduct,B.ReportingScopeSpecification,C.MedicinalProduct),
  (B.contextAction,B.ReportingContextDescription,None),
  (B.actionReference,B.ReportingScopeSpecification,None),
  (B.actionEvidence,B.ReportingScopeSpecification,C.SourceRecord)]:
  typ(g,p,OWL.ObjectProperty);g.add((p,RDFS.domain,domain))
  if range_ is not None:g.add((p,RDFS.range,range_))
 for name,domain,range_ in [
  ('predicateIRI',B.StructuredClaim,XSD.anyURI),('objectValue',B.StructuredClaim,None),('polarity',B.StructuredClaim,XSD.string),('claimOrigin',B.StructuredClaim,XSD.string),
  ('specificationVersion',B.ReportingScopeSpecification,XSD.string),('contextVersion',B.ReportingContextDescription,XSD.string),
  ('allowedRole',B.ReportingScopeSpecification,XSD.string),('allowedRoute',B.ReportingScopeSpecification,XSD.string),
  ('scenario',None,XSD.string),('submissionKind',None,XSD.string),('contextRole',B.ReportingContextDescription,XSD.string),
  ('contextRoute',B.ReportingContextDescription,XSD.string),('contextCountry',B.ReportingContextDescription,XSD.string),
  ('portfolioRelationDeclared',B.ReportingContextDescription,XSD.boolean),
  ('scopeMode',B.ReportingScopeSpecification,XSD.string),('scopeComplete',B.ReportingScopeSpecification,XSD.boolean),
  ('actionState',B.ReportingScopeSpecification,XSD.string),('actionEvidenceKind',B.ReportingScopeSpecification,XSD.string),
  ('effectiveFrom',B.ReportingScopeSpecification,XSD.dateTime),('effectiveTo',B.ReportingScopeSpecification,XSD.dateTime),
  ('evaluatedAt',B.ReportingContextDescription,XSD.dateTime),('reportingFrequency',B.ReportingScopeSpecification,XSD.string),
  ('marketingPolicy',B.ReportingScopeSpecification,XSD.string),('marketingStatus',B.ReportingContextDescription,XSD.string),
  ('marketingCountry',B.ReportingContextDescription,XSD.string),
  ('evidencePointer',None,XSD.string),('sourceURL',None,XSD.anyURI),('sourceSHA256',None,XSD.string)]:
  p=B[name];typ(g,p,OWL.DatatypeProperty)
  if domain is not None:g.add((p,RDFS.domain,domain))
  if range_ is not None:g.add((p,RDFS.range,range_))
 return g
M=model();full=prev.full+M
def shapes():
 g=graph();g.bind('sh',SH)
 def node(cls):n=B[str(cls).split('/')[-1]+'Shape'];typ(g,n,SH.NodeShape);g.add((n,SH.targetClass,cls));return n
 def field(n,p,lo=0,hi=1,dt=None,cls=None,choices=None,kind=None):
  b=BNode();g.add((n,SH.property,b));g.add((b,SH.path,p));g.add((b,SH.minCount,Literal(lo)))
  if hi is not None:g.add((b,SH.maxCount,Literal(hi)))
  if dt:g.add((b,SH.datatype,dt))
  if cls:g.add((b,SH['class'],cls))
  if kind:g.add((b,SH.nodeKind,kind))
  if choices:
   h=BNode();Collection(g,h,[Literal(x) for x in choices]);g.add((b,SH['in'],h))
 def rule(n,name,body):
  q=B[name];g.add((n,SH.sparql,q));g.add((q,SH.message,Literal(name)));g.add((q,SH.select,Literal('PREFIX b: <'+str(B)+'> PREFIX r: <'+str(R)+'> PREFIX owl: <'+str(OWL)+'> SELECT $this WHERE { '+body+' }')))
 n=node(B.StructuredClaim)
 field(n,B.claimSubject,1,kind=SH.IRI);field(n,B.predicateIRI,1,dt=XSD.anyURI);field(n,B.objectResource,kind=SH.IRI);field(n,B.objectValue,kind=SH.Literal)
 field(n,B.polarity,1,choices=['positive','negative']);field(n,B.evidencePointer,1,dt=XSD.string)
 field(n,B.claimOrigin,1,choices=['source-extracted','mapping-interpretation','synthetic'])
 inv=BNode();g.add((inv,SH.inversePath,R.carrierClaim));field(n,inv,1,None,cls=C.SourceRecord)
 rule(n,'one-object-kind','{ FILTER NOT EXISTS { $this b:objectResource ?r } FILTER NOT EXISTS { $this b:objectValue ?v } } UNION { $this b:objectResource ?r ; b:objectValue ?v }')
 rule(n,'claim-not-carrier','?record r:carrierClaim $this . $this (owl:sameAs|^owl:sameAs)* ?record .')
 n=node(B.ReportingScopeSpecification)
 field(n,B.specificationSource,1,cls=C.SourceRecord);field(n,B.specificationVersion,1,dt=XSD.string)
 for p in [B.allowedRole,B.allowedRoute]:field(n,p,1,None,dt=XSD.string)
 field(n,B.scenario,1,choices=['routine','preparedness','crisis']);field(n,B.submissionKind,1,dt=XSD.string)
 field(n,B.scopeJurisdiction,1,cls=C.RegulatoryJurisdiction)
 field(n,B.scopeMode,1,choices=['all-declared-route-products','enumerated']);field(n,B.scopedProduct,0,None,cls=C.MedicinalProduct)
 field(n,B.scopeComplete,0,dt=XSD.boolean)
 field(n,B.actionReference);field(n,B.actionEvidence,0,cls=C.SourceRecord)
 field(n,B.actionState,0,choices=['announced','not-announced','unknown'])
 field(n,B.actionEvidenceKind,0,choices=['action-announcement','platform-launch','guidance','unknown'])
 for p in [B.effectiveFrom,B.effectiveTo]:field(n,p,0,dt=XSD.dateTime)
 field(n,B.marketingPolicy,1,choices=['require-marketed-status','not-a-condition','unknown'])
 field(n,B.reportingFrequency,0,dt=XSD.string)
 n=node(B.ReportingContextDescription)
 for p,cls in [(B.contextActor,C.Organization),(B.contextProduct,C.MedicinalProduct),(B.contextPresentation,C.MedicinalProductPresentation),(B.contextJurisdiction,C.RegulatoryJurisdiction)]:field(n,p,0,cls=cls)
 for p in [B.contextVersion,B.contextRole,B.contextRoute,B.contextCountry,B.scenario,B.submissionKind,B.marketingStatus,B.marketingCountry]:field(n,p,0,dt=XSD.string)
 field(n,B.contextAction);field(n,B.portfolioRelationDeclared,0,dt=XSD.boolean);field(n,B.evaluatedAt,0,dt=XSD.dateTime)
 rule(n,'presentation-product-agreement','$this b:contextPresentation ?p ; b:contextProduct ?product . ?p <'+str(C.presentationOf)+'> ?other . FILTER(?other != ?product)')
 return g
S=shapes()
def validate_graph(g):
 hierarchy=prev.reg.hierarchy+Graph()
 for a,b in M.subject_objects(RDFS.subClassOf):hierarchy.add((a,RDFS.subClassOf,b))
 ok,r,_=validate(g+hierarchy,shacl_graph=S,advanced=True,inference='none')
 return {'conforms':bool(ok),'violations':[{'path':str(r.value(x,SH.resultPath) or ''),'constraint':str(r.value(x,SH.sourceConstraint) or ''),'component':str(r.value(x,SH.sourceConstraintComponent) or '')} for x in r.subjects(RDF.type,SH.ValidationResult)]}
def fixture(scenario='preparedness',kind='availability'):
 g=graph();sp=T.spec;ctx=T.context
 for n,c in [(sp,B.ReportingScopeSpecification),(ctx,B.ReportingContextDescription),(T.document,C.SourceRecord),(T.notice,C.SourceRecord),(T.org,C.Organization),(T.product,C.MedicinalProduct),(T.presentation,C.MedicinalProductPresentation),(T.jurisdiction,C.RegulatoryJurisdiction)]:typ(g,n,c)
 g.add((T.presentation,C.presentationOf,T.product))
 for p,o in [(B.specificationSource,T.document),(B.scopeJurisdiction,T.jurisdiction),(B.scopedProduct,T.product),(B.actionReference,T.action),(B.actionEvidence,T.notice)]:g.add((sp,p,o))
 for p,o in [(B.contextActor,T.org),(B.contextProduct,T.product),(B.contextPresentation,T.presentation),(B.contextJurisdiction,T.jurisdiction),(B.contextAction,T.action)]:g.add((ctx,p,o))
 for p,v in [(B.specificationVersion,'synthetic-v1'),(B.allowedRole,'MAH'),(B.allowedRoute,'CAP'),(B.scenario,scenario),(B.submissionKind,kind),(B.scopeMode,'enumerated'),(B.actionState,'announced'),(B.actionEvidenceKind,'action-announcement'),(B.marketingPolicy,'require-marketed-status' if kind in ['availability','routine-shortage'] else 'not-a-condition'),(B.reportingFrequency,'synthetic-weekly')]:value(g,sp,p,v)
 value(g,sp,B.scopeComplete,True);value(g,sp,B.effectiveFrom,'2026-10-01T00:00:00Z',XSD.dateTime);value(g,sp,B.effectiveTo,'2026-11-01T00:00:00Z',XSD.dateTime)
 for p,v in [(B.contextVersion,'synthetic-v1'),(B.contextRole,'MAH'),(B.contextRoute,'CAP'),(B.contextCountry,'DE'),(B.scenario,scenario),(B.submissionKind,kind),(B.marketingStatus,'marketed'),(B.marketingCountry,'DE')]:value(g,ctx,p,v)
 value(g,ctx,B.portfolioRelationDeclared,True);value(g,ctx,B.evaluatedAt,'2026-10-10T00:00:00Z',XSD.dateTime)
 return g,sp,ctx
def evaluate(g,sp,ctx):
 if (sp,RDF.type,B.ReportingScopeSpecification) not in g or (ctx,RDF.type,B.ReportingContextDescription) not in g:return {'verdict':'INVALID_INPUT','dimensions':{'identifier':'MISSING_TYPED_INPUT'}}
 if not validate_graph(g)['conforms']:return {'verdict':'INVALID_INPUT','dimensions':{}}
 one=lambda n,p:g.value(n,p);dims={}
 def equal(name,a,b):dims[name]='UNKNOWN' if a is None or b is None else 'MATCH' if a==b else 'OUTSIDE'
 def member(name,v,vs):dims[name]='UNKNOWN' if v is None or not vs else 'MATCH' if v in vs else 'OUTSIDE'
 equal('version',one(ctx,B.contextVersion),one(sp,B.specificationVersion))
 if dims['version']=='OUTSIDE':return {'verdict':'VERSION_MISMATCH','dimensions':dims}
 equal('scenario',one(ctx,B.scenario),one(sp,B.scenario));equal('submission',one(ctx,B.submissionKind),one(sp,B.submissionKind))
 equal('jurisdiction',one(ctx,B.contextJurisdiction),one(sp,B.scopeJurisdiction))
 member('role',one(ctx,B.contextRole),list(g.objects(sp,B.allowedRole)));member('route',one(ctx,B.contextRoute),list(g.objects(sp,B.allowedRoute)))
 dims['actor']='MATCH' if one(ctx,B.contextActor) is not None else 'UNKNOWN'
 if str(one(ctx,B.contextRole))=='MAH':equal('portfolio',one(ctx,B.portfolioRelationDeclared),Literal(True))
 else:dims['portfolio']='NOT_REQUIRED' if str(one(ctx,B.contextRole))=='NCA' else 'UNKNOWN'
 product=one(ctx,B.contextProduct);mode=str(one(sp,B.scopeMode));listed=list(g.objects(sp,B.scopedProduct))
 dims['product']='UNKNOWN' if product is None else 'MATCH' if mode=='all-declared-route-products' or product in listed else 'OUTSIDE' if one(sp,B.scopeComplete)==Literal(True) else 'UNKNOWN'
 if str(one(sp,B.scenario))=='routine':dims['action']='NOT_REQUIRED'
 else:
  ref=one(sp,B.actionReference);evidence=one(sp,B.actionEvidence)
  dims['action']='UNKNOWN'
  if ref is not None and one(ctx,B.contextAction) is not None and ref!=one(ctx,B.contextAction):dims['action']='OUTSIDE'
  elif ref is not None and ref==one(ctx,B.contextAction) and evidence is not None and str(one(sp,B.actionEvidenceKind))=='action-announcement' and str(one(sp,B.actionState))=='announced':dims['action']='MATCH'
 start,end,at=[one(n,p) for n,p in [(sp,B.effectiveFrom),(sp,B.effectiveTo),(ctx,B.evaluatedAt)]]
 dims['time']='UNKNOWN'
 if all(x is not None for x in [start,end,at]):
  dates=[x.toPython() for x in [start,end,at]]
  if all(isinstance(x,datetime) and x.tzinfo is not None for x in dates):
   if dates[1]<=dates[0]:return {'verdict':'INVALID_INPUT','dimensions':{'time':'REVERSED_INTERVAL'}}
   dims['time']='MATCH' if dates[0]<=dates[2]<dates[1] else 'OUTSIDE'
 policy=str(one(sp,B.marketingPolicy))
 if policy=='not-a-condition':dims['marketing']='NOT_REQUIRED'
 elif policy=='require-marketed-status':
  country=one(ctx,B.contextCountry);scountry=one(ctx,B.marketingCountry);status=str(one(ctx,B.marketingStatus) or '')
  dims['marketing']='UNKNOWN' if country is None or scountry!=country or not status else 'MATCH' if status in ['marketed','temporarily-unavailable'] else 'OUTSIDE' if status in ['not-marketed','never-marketed'] else 'UNKNOWN'
 else:dims['marketing']='UNKNOWN'
 verdict='OUTSIDE_DECLARED_SCOPE' if 'OUTSIDE' in dims.values() else 'UNKNOWN' if 'UNKNOWN' in dims.values() else 'MATCHES_DECLARED_CRITERIA'
 return {'verdict':verdict,'dimensions':dims,'frequency':str(one(sp,B.reportingFrequency) or 'UNKNOWN'),'legal_compliance':'NOT_ASSESSED','operational_readiness':'NOT_ASSESSED'}
def claim(g,n,record,subject,predicate,obj,polarity='positive',pointer='synthetic:/claim',origin='synthetic'):
 typ(g,n,B.StructuredClaim);typ(g,record,C.SourceRecord);g.add((record,R.carrierClaim,n));g.add((n,B.claimSubject,subject))
 value(g,n,B.predicateIRI,str(predicate),XSD.anyURI);g.add((n,B.objectValue if isinstance(obj,Literal) else B.objectResource,obj));value(g,n,B.polarity,polarity);value(g,n,B.evidencePointer,pointer)
 value(g,n,B.claimOrigin,origin)
def claim_answer(g,subject,predicate,obj):
 if not validate_graph(g)['conforms']:return {'status':'INVALID_INPUT','claims':[]}
 found=[]
 for n in g.subjects(B.claimSubject,subject):
  if g.value(n,B.predicateIRI)!=Literal(str(predicate),datatype=XSD.anyURI):continue
  if (n,B.objectValue if isinstance(obj,Literal) else B.objectResource,obj) in g:found.append((str(n),str(g.value(n,B.polarity))))
 polarities={p for _,p in found}
 status='CONFLICTING_SOURCE_CLAIMS' if len(polarities)>1 else 'SOURCE_REPORTED' if polarities=={'positive'} else 'SOURCE_DENIED' if polarities=={'negative'} else 'NOT_REPORTED_IN_SLICE'
 origins={str(g.value(URIRef(n),B.claimOrigin)) for n,_ in found}
 if origins=={'mapping-interpretation'}:status='CONFLICTING_MAPPING_PROPOSALS' if len(polarities)>1 else 'MAPPING_PROPOSED'
 elif 'mapping-interpretation' in origins:status='MIXED_EVIDENCE_ORIGINS'
 return {'status':status,'claims':sorted(n for n,_ in found),'origins':sorted(origins),'polarities':sorted(polarities),'world_fact_inferred':False}
