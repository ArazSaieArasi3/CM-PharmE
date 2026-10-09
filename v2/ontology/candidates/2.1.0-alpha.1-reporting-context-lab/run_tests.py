"""Predeclared bounded assertions; all negative expectations remain visible."""
from lab import *
import copy
fixtures=Dataset();queries=[];structure=[];logic=[]
def keep(name,g):
 out=fixtures.graph(URIRef('urn:cmpe-context-case:'+name))
 for t in g:out.add(t)
def qcase(name,g,s,c,want,requirement,dimension=None):
 result=evaluate(g,s,c);actual=result['verdict'] if dimension is None else result['dimensions'][dimension]
 queries.append({'name':name,'requirement':requirement,'expected':want,'actual':actual,'result':result,'dimension':dimension,'pass':actual==want});keep(name,g)
def scase(name,g,want,requirement,marker=None):
 r=validate_graph(g);passed=r['conforms']==want and (marker is None or marker in str(r['violations']))
 structure.append({'name':name,'requirement':requirement,'expected':want,**r,'marker':marker,'pass':passed});keep(name,g)
def lcase(name,g,want,requirement):
 r=prev.hermit(full+g);logic.append({'name':name,'requirement':requirement,'expected_consistent':want,**r,'pass':r['consistent']==want and not r['unsatisfiable_named_classes']});keep(name,g)
g,s,c=fixture();qcase('complete-declared-match',g,s,c,'MATCHES_DECLARED_CRITERIA','CTX-01');scase('complete-context-positive',g,True,'CTX-01')
changes=[
 ('wrong-role',c,B.contextRole,Literal('NCA'),'OUTSIDE_DECLARED_SCOPE','CTX-01'),
 ('wrong-route',c,B.contextRoute,Literal('NAP'),'OUTSIDE_DECLARED_SCOPE','CTX-03'),
 ('wrong-scenario',c,B.scenario,Literal('crisis'),'OUTSIDE_DECLARED_SCOPE','CTX-03'),
 ('wrong-submission-kind',c,B.submissionKind,Literal('manufacturing'),'OUTSIDE_DECLARED_SCOPE','CTX-07'),
 ('wrong-jurisdiction',c,B.contextJurisdiction,T.otherJurisdiction,'OUTSIDE_DECLARED_SCOPE','CTX-02'),
 ('missing-role',c,B.contextRole,None,'UNKNOWN','CTX-01'),
 ('missing-actor',c,B.contextActor,None,'UNKNOWN','CTX-01'),
 ('not-in-MAH-portfolio',c,B.portfolioRelationDeclared,Literal(False),'OUTSIDE_DECLARED_SCOPE','CTX-01'),
 ('missing-portfolio',c,B.portfolioRelationDeclared,None,'UNKNOWN','CTX-01'),
 ('missing-product',c,B.contextProduct,None,'UNKNOWN','CTX-05'),
 ('other-product-complete-list',c,B.contextProduct,T.otherProduct,'OUTSIDE_DECLARED_SCOPE','CTX-05'),
 ('missing-action-evidence',s,B.actionEvidence,None,'UNKNOWN','CTX-04'),
 ('launch-is-not-action',s,B.actionEvidenceKind,Literal('platform-launch'),'UNKNOWN','CTX-04'),
 ('guidance-is-not-action',s,B.actionEvidenceKind,Literal('guidance'),'UNKNOWN','CTX-04'),
 ('unannounced-action',s,B.actionState,Literal('not-announced'),'UNKNOWN','CTX-04'),
 ('different-action',c,B.contextAction,T.otherAction,'OUTSIDE_DECLARED_SCOPE','CTX-04'),
 ('missing-end',s,B.effectiveTo,None,'UNKNOWN','CTX-06'),
 ('missing-timezone',c,B.evaluatedAt,Literal('2026-10-10T00:00:00',datatype=XSD.dateTime),'UNKNOWN','CTX-06'),
 ('expired-at-exclusive-end',c,B.evaluatedAt,Literal('2026-11-01T00:00:00Z',datatype=XSD.dateTime),'OUTSIDE_DECLARED_SCOPE','CTX-06'),
 ('inclusive-start',c,B.evaluatedAt,Literal('2026-10-01T00:00:00Z',datatype=XSD.dateTime),'MATCHES_DECLARED_CRITERIA','CTX-06'),
 ('different-rule-version',c,B.contextVersion,Literal('synthetic-v2'),'VERSION_MISMATCH','CTX-06'),
 ('missing-version',c,B.contextVersion,None,'UNKNOWN','CTX-06'),
 ('not-marketed-availability',c,B.marketingStatus,Literal('not-marketed'),'OUTSIDE_DECLARED_SCOPE','CTX-07'),
 ('temporary-unavailability-admitted',c,B.marketingStatus,Literal('temporarily-unavailable'),'MATCHES_DECLARED_CRITERIA','CTX-07'),
 ('unknown-marketing-status',c,B.marketingStatus,None,'UNKNOWN','CTX-07'),
 ('marketing-country-mismatch',c,B.marketingCountry,Literal('FR'),'UNKNOWN','CTX-02'),
 ('reversed-effective-interval',s,B.effectiveTo,Literal('2026-09-01T00:00:00Z',datatype=XSD.dateTime),'INVALID_INPUT','CTX-06')]
for name,node,p,obj,want,req in changes:
 x=g+Graph();x.remove((node,p,None))
 if obj is not None:x.add((node,p,obj))
 if obj==T.otherJurisdiction:typ(x,obj,C.RegulatoryJurisdiction)
 if obj==T.otherProduct:
  typ(x,obj,C.MedicinalProduct);x.remove((c,B.contextPresentation,None))
 qcase(name,x,s,c,want,req)
x=g+Graph();x.set((c,B.contextProduct,T.otherProduct));typ(x,T.otherProduct,C.MedicinalProduct);x.remove((c,B.contextPresentation,None));x.set((s,B.scopeComplete,Literal(False)))
qcase('other-product-incomplete-list',x,s,c,'UNKNOWN','CTX-05')
x=g+Graph();x.set((s,B.allowedRole,Literal('NCA')));x.set((c,B.contextRole,Literal('NCA')));x.remove((c,B.portfolioRelationDeclared,None))
qcase('NCA-does-not-need-MAH-portfolio',x,s,c,'MATCHES_DECLARED_CRITERIA','CTX-01')
for kind in ['manufacturing','alternative-therapies']:
 x,sp,ctx=fixture(kind=kind);x.remove((ctx,B.marketingStatus,None));qcase(kind+'-independent-of-marketing',x,sp,ctx,'MATCHES_DECLARED_CRITERIA','CTX-07')
x,sp,ctx=fixture('routine','routine-shortage');x.remove((sp,B.actionEvidence,None));x.remove((sp,B.actionState,None));qcase('routine-no-action-notice-required',x,sp,ctx,'MATCHES_DECLARED_CRITERIA','CTX-04')
qcase('unknown-record-selector-rejected',g,T.nonexistent,c,'INVALID_INPUT','CTX-08')
x=g+Graph();x.set((s,B.reportingFrequency,Literal('synthetic-monthly')))
r=evaluate(x,s,c);queries.append({'name':'frequency-not-hardcoded','requirement':'CTX-06','expected':'synthetic-monthly','actual':r['frequency'],'pass':r['frequency']=='synthetic-monthly'});keep('frequency-not-hardcoded',x)
x=g+Graph();x.add((c,B.contextRole,Literal('NCA')));scase('ambiguous-context-role',x,False,'CTX-01','MaxCountConstraintComponent')
x=g+Graph();x.set((s,B.specificationSource,T.missingSource));scase('untyped-source-reference',x,False,'CTX-08','ClassConstraintComponent')
x=g+Graph();x.set((c,B.contextProduct,T.otherProduct));typ(x,T.otherProduct,C.MedicinalProduct);scase('presentation-product-mismatch',x,False,'CTX-02','presentation-product-agreement')
a=graph();claim(a,T.claim,T.record,T.listing,C.listingPresentation,T.presentation)
scase('structured-claim-positive',a,True,'CL-01')
for name,p,o in [('literal-subject',B.claimSubject,Literal('not-an-iri')),('literal-resource-object',B.objectResource,Literal('not-an-iri'))]:
 x=a+Graph();x.set((T.claim,p,o));scase(name,x,False,'CL-02','NodeKindConstraintComponent')
x=a+Graph();x.remove((T.claim,B.objectResource,None));x.add((T.claim,B.objectValue,T.wrongLiteral));scase('resource-in-literal-slot',x,False,'CL-02','NodeKindConstraintComponent')
x=a+Graph();x.add((T.claim,OWL.sameAs,T.record));scase('claim-carrier-alias',x,False,'CL-01','claim-not-carrier')
x=a+Graph();x.add((T.claim,B.objectValue,Literal('extra')));scase('resource-and-literal-object',x,False,'CL-02','one-object-kind')
x=a+Graph();x.remove((T.claim,B.objectResource,None));scase('no-claim-object',x,False,'CL-02','one-object-kind')
x=a+Graph();x.remove((T.record,R.carrierClaim,None));scase('claim-without-carrier',x,False,'CL-04','MinCountConstraintComponent')
x=a+Graph();x.set((T.claim,B.predicateIRI,Literal(str(C.listingPresentation))));scase('predicate-is-not-anyURI',x,False,'CL-02','DatatypeConstraintComponent')
x=a+Graph();claim(x,T.counterclaim,T.otherRecord,T.listing,C.listingPresentation,T.presentation,polarity='negative')
for name,inp,sub,pred,obj,want,req in [
 ('positive-source-claim',a,T.listing,C.listingPresentation,T.presentation,'SOURCE_REPORTED','CL-02'),
 ('conflicting-source-claims',x,T.listing,C.listingPresentation,T.presentation,'CONFLICTING_SOURCE_CLAIMS','CL-03'),
 ('absent-is-not-false',a,T.otherListing,C.listingPresentation,T.presentation,'NOT_REPORTED_IN_SLICE','CL-04')]:
 actual=claim_answer(inp,sub,pred,obj);queries.append({'name':name,'requirement':req,'expected':want,'actual':actual['status'],'pass':actual['status']==want});keep(name,inp)
neg=graph();claim(neg,T.denial,T.otherRecord,T.listing,C.listingPresentation,T.presentation,'negative');ans=claim_answer(neg,T.listing,C.listingPresentation,T.presentation)
queries.append({'name':'negative-source-claim','requirement':'CL-03','expected':'SOURCE_DENIED','actual':ans['status'],'pass':ans['status']=='SOURCE_DENIED'});keep('negative-source-claim',neg)
for name,origins,polarities,want in [
 ('mapping-is-not-source-extraction',['mapping-interpretation'],['positive'],'MAPPING_PROPOSED'),
 ('conflicting-mapping-proposals',['mapping-interpretation','mapping-interpretation'],['positive','negative'],'CONFLICTING_MAPPING_PROPOSALS'),
 ('mixed-origin-answer',['source-extracted','mapping-interpretation'],['positive','positive'],'MIXED_EVIDENCE_ORIGINS'),
 ('direct-source-extraction',['source-extracted'],['positive'],'SOURCE_REPORTED')]:
 z=graph()
 for i,(origin,polarity) in enumerate(zip(origins,polarities)):claim(z,T['origin-claim-'+str(i)],T['origin-record-'+str(i)],T.listing,C.listingPresentation,T.presentation,polarity,origin=origin)
 ans=claim_answer(z,T.listing,C.listingPresentation,T.presentation);queries.append({'name':name,'requirement':'CL-05','expected':want,'actual':ans['status'],'pass':ans['status']==want});keep(name,z)
z=a+Graph();z.remove((T.claim,B.claimOrigin,None));scase('missing-claim-origin',z,False,'CL-05','MinCountConstraintComponent')
lcase('combined-proposed-tbox',graph(),True,'CTX-08')
lcase('complete-synthetic-context',g,True,'CTX-01')
z=a+Graph();prev.not_edge(z,T.listing,C.listingPresentation,T.presentation);lcase('claim-does-not-assert-relation',z,True,'CL-02')
z=a+Graph();prev.not_type(z,T.listing,C.MarketListing);lcase('claim-does-not-create-listing',z,True,'CL-02')
z=graph();claim(z,T.claim,T.record,T.x,RDF.type,C.RegulatoryAuthorization);prev.not_type(z,T.x,C.RegulatoryAuthorization);lcase('type-claim-does-not-create-authorization',z,True,'CL-02')
lcase('conflicting-claims-remain-logically-consistent',x,True,'CL-03')
z=a+Graph();z.add((T.claim,OWL.sameAs,T.record));lcase('claim-carrier-identity-collision',z,False,'CL-01')
z=neg+Graph();z.add((T.listing,C.listingPresentation,T.presentation));lcase('source-denial-is-not-negative-world-assertion',z,True,'CL-03')
z=g+Graph();prev.not_type(z,T.context,C.MedicineShortageSituation);lcase('context-description-not-shortage-fact',z,True,'CTX-08')
z=g+Graph();prev.not_type(z,T.org,C.AuthorizedOrganizationRole);lcase('scope-match-no-authorization',z,True,'CTX-08')
z=g+Graph();typ(z,T.spec,C.SourceRecord);lcase('specification-is-not-source-carrier',z,False,'CL-01')
z=graph();typ(z,T.context,B.ReportingContextDescription);prev.not_type(z,T.context,C.Assertion);lcase('context-is-an-assertion-description',z,False,'CTX-08')
M.serialize(H/'proposed-model.ttl',format='turtle');S.serialize(H/'proposed-shapes.ttl',format='turtle');fixtures.serialize(H/'test-fixtures.trig',format='trig')
out={'queries':queries,'query_pass':sum(r['pass'] for r in queries),'query_total':len(queries),'shacl':structure,'shacl_pass':sum(r['pass'] for r in structure),'shacl_total':len(structure),'hermit':logic,'hermit_pass':sum(r['pass'] for r in logic),'hermit_total':len(logic),'world_fact_materialization':False,'scientific_acceptance':False}
write('test-results.json',out);print(json.dumps({k:v for k,v in out.items() if k.endswith(('_pass','_total'))}),flush=True)
assert all(r['pass'] for r in queries+structure+logic)
