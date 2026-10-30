"""Public redacted executed-agreement witness and explicit BA candidate projection."""
from lab import *
URL='https://www.sec.gov/Archives/edgar/data/1682852/000168285220000023/lonzamodernagltafullye.htm'
source='BA-MODERNA-SEC-2020';g=graph();record=T[source];g.add((record,RDF.type,C.SourceRecord));g.add((record,E.sourceID,Literal(source)));g.add((record,E.sourceDateKind,Literal('filing-date-not-extracted')));g.add((record,B.sourceURL,Literal(URL,datatype=XSD.anyURI)))
facts=[
 ('made','GLTA','statedMadeDate','2020-09-04','assessment-content','opening paragraph'),
 ('effective','GLTA','statedEffectiveDate','2020-05-01','assessment-content','opening paragraph'),
 ('prior-date','SCA','statedAgreementDate','2020-04-30','assessment-content','recital C'),
 ('supersedes','GLTA','supersedesNamedAgreement','SCA','assessment-content','Entire Agreement; Amendments'),
 ('party-moderna','GLTA','signatureParty','ModernaTX, Inc.','assessment-content','signature block'),
 ('party-sales','GLTA','signatureParty','Lonza Sales Ltd.','assessment-content','signature block'),
 ('party-lonza','GLTA','signatureParty','Lonza Ltd.','assessment-content','signature block'),
 ('signed','GLTA','executionSignaturesShown','true','reported-occurrence','signature block'),
 ('work-order','contract-parties','prepareAgreedWorkOrderBeforeWork','required','required','Statement of Work subsection'),
 ('sow-scope','SOW','specifies','service-scope-timetable-fees','assessment-content','definition Statement of Work'),
 ('affiliates','affiliates','mayExecuteSOW','subject-to-agreement','assessment-content','Affiliates subsection'),
 ('missing-sow','appendices-A1-A3','availability','to-be-attached','assessment-content','appendices A-1 A-2 A-3'),
 ('redacted-template','appendix-B','availability','redacted','assessment-content','appendix B')]
for id,subject,predicate,obj,mode,loc in facts:add(g,'sec-'+id,source,subject,E[predicate],obj,mode,loc)
save('contract-claims.ttl',g)
dump('contract-extraction.json',{'source_id':source,'url':URL,'publisher':'Moderna filing hosted by SEC; SEC hosting is not independent endorsement','document':'Exhibit 10.2 Global Long Term Agreement','facts':[dict(zip(['id','subject','predicate','object','mode','locator'],x)) for x in facts],'count':len(facts),'public_redacted_executed_text':True,'full_unredacted_contract_available':False,'identity_note':'Opening paragraph renders Lonza Ss Ltd.; signature block and filing exhibit index use Lonza Sales Ltd. Preserve this discrepancy; labels are not registry-resolved legal identifiers.','limits':['No reconstruction of redacted content or missing work orders','SCA and GLTA kept separate; no owl:sameAs link','Made date, effective date and filing/publication time are distinct','Three signatory organizations are not collapsed into the two corporate labels of the press release']})
# Candidate domain projection: uses existing concepts and relations; not accepted
# world facts or an assertion that every future work order has all three actors.
projection=graph();agreement=T.GLTA;commitment=T.workOrderCommitment
projection.add((agreement,RDF.type,C.StrategicPartnershipAgreement))
for tag in ['ba-partnership','documented-partnership']:projection.add((agreement,L.profile,Literal(tag)))
projection.add((agreement,R.agreementCommitment,commitment))
for cls in [C.Assertion,C.SupportedAssertionRole]:projection.add((commitment,RDF.type,cls))
projection.add((commitment,L.profile,Literal('commitment-assertion')));projection.add((commitment,R.commitmentText,Literal('The parties are to agree a work order before the specified work.')))
parties=[T.ModernaTX,T.LonzaSales,T.LonzaLtd]
for org in parties:
 for cls in [C.Organization,C.PartnerOrganizationRole]:projection.add((org,RDF.type,cls))
 projection.add((agreement,C.partnershipParticipant,org));projection.add((commitment,R.commitmentActor,org))
for cls in [C.SourceRecord,C.EvidenceSourceRecordRole,C.EvidenceItem]:projection.add((record,RDF.type,cls))
projection.add((record,B.sourceURL,Literal(URL,datatype=XSD.anyURI)))
projection.add((T.contractEvidence,RDF.type,C.EvidenceSupport))
for p,o in [(C.evidenceAssertion,commitment),(C.evidenceRecord,record),(C.evidenceItem,record)]:projection.add((T.contractEvidence,p,o))
save('contract-domain-projection.ttl',projection)
checks=[];ds=Dataset()
def check(name,actual,expected,kind):checks.append({'id':name,'actual':actual,'expected':expected,'kind':kind,'pass':actual==expected})
check('documentary-claims-admitted',admission(g)['conforms'],True,'admission')
def admit(name,z,want):check(name,coh.admission(z)['conforms'],want,'projection');ds.graph(URIRef('urn:cmpe-contract:'+name)).__iadd__(z)
admit('three-party-projected-commitment',projection,True)
for name,mut in [('missing-source-evidence',lambda z:z.remove((T.contractEvidence,C.evidenceRecord,None))),('outsider-added',lambda z:(z.add((T.outsider,RDF.type,C.Organization)),z.add((commitment,R.commitmentActor,T.outsider)))),('collapsed-party-set',lambda z:z.remove((agreement,C.partnershipParticipant,T.LonzaSales))),('document-as-agreement',lambda z:(z.remove((T.contractEvidence,C.evidenceRecord,None)),z.add((T.contractEvidence,C.evidenceRecord,agreement))))]:
 z=projection+Graph();mut(z);admit(name,z,False)
check('three-signatory-labels',len([x for x in facts if x[2]=='signatureParty']),3,'query')
check('made-differs-from-effective',facts[0][3]!=facts[1][3],True,'query')
check('missing-work-orders-not-invented',answer(g,T['appendices-A1-A3'],E.availability,Literal('to-be-attached'),'assessment-content')['status'],'SOURCE_REPORTED_ASSESSMENT_CONTENT','query')
check('required-work-order-not-proved-executed',answer(g,T['contract-parties'],E.prepareAgreedWorkOrderBeforeWork,Literal('required'),'reported-occurrence')['status'],'NOT_REPORTED_IN_SELECTED_MODE','query')
q=f'SELECT ?org WHERE {{ <{agreement}> <{C.partnershipParticipant}> ?org }} ORDER BY ?org'
actual=[str(r[0]) for r in projection.query(q)];check('projected-three-party-query',actual,sorted(map(str,parties)),'query')
logical=[]
for name,z,want in [('projected-contract-consistent',projection+g,True),('agreement-is-not-source',projection+g,True)]:
 if name=='agreement-is-not-source':coh.ctx.prev.not_type(z,agreement,C.SourceRecord)
 r=coh.ctx.prev.hermit(coh.full+M+z);logical.append({'id':name,**r,'pass':r['consistent']==want and not r['unsatisfiable_named_classes']})
save('contract-fixtures.trig',ds);dump('contract-results.json',{'checks':checks,'passed':sum(x['pass'] for x in checks),'total':len(checks),'logical':logical,'projection_status':'PROPOSED_MAPPING_USING_EXISTING_MODEL; NOT_SCIENTIFICALLY_ACCEPTED','future_gap':'The exact-participant-set bounded profile does not yet model an affiliate-only SOW or subset commitments. Do not generalize this all-party witness to every contractual obligation.'})
print(json.dumps({'contract_checks':sum(x['pass'] for x in checks),'total':len(checks),'logical':sum(x['pass'] for x in logical)}),flush=True)
assert all(x['pass'] for x in checks+logical)
