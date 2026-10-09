"""Real source statements, explicit mapping proposals, and fixed boundary oracles."""
from lab import *
sources=json.loads((H/'sources.json').read_text())['sources'];g=graph();rows=[]
for src in sources:
 n=T[src['id']];g.add((n,RDF.type,C.SourceRecord));g.add((n,B.sourceURL,Literal(src['url'],datatype=XSD.anyURI)))
 for p,v in [('sourceID',src['id']),('sourceDateKind',src['date_kind'])]+([('sourceDate',src['source_date'])] if src['source_date'] else []):g.add((n,E[p],Literal(v)))
def fact(id,src,subject,predicate,obj,mode,loc,time='UNKNOWN',precision='unspecified',role='not-established'):
 add(g,id,src,subject,E[predicate],obj,mode,loc,time,precision,role)
 rows.append({'id':id,'source':src,'subject':subject,'predicate':predicate,'object':obj,'mode':mode,'locator':loc,'time':time,'precision':precision,'time_role':role})
# RM: report of a completed review and changed content, not invented company action.
fact('rm-review','RM-EMA-2020','sartan-review','reviewConcluded','true','reported-occurrence','p1 para5','2019-01','month','assessment-period')
fact('rm-prior-scope','RM-EMA-2020','sartan-prior-result','limitBasis','active-ingredient','assessment-content','p1 para2')
fact('rm-new-scope','RM-EMA-2020','sartan-revised-result','limitBasis','finished-product','assessment-content','p1 para2')
fact('rm-control-required','RM-EMA-2020','manufacturers','controlStrategy','prevent-or-limit-impurities','required','p1 para3')
fact('rm-testing-required','RM-EMA-2020','manufacturers','riskEvaluationAndTesting','required','required','p1 para3')
for i,label in enumerate(['candesartan','irbesartan','losartan','olmesartan','valsartan'],1):fact('rm-included-'+str(i),'RM-EMA-2020','sartan-review','includedLabel',label,'assessment-content','p1 More about the medicine')
for i,label in enumerate(['azilsartan','eprosartan','telmisartan'],1):fact('rm-excluded-'+str(i),'RM-EMA-2020','sartan-review','excludedLabel',label,'assessment-content','p2 para1')
# BA: plans and later reports have different modes and publication cutoffs.
fact('ba-agreement','BA-LONZA-2020-05','collaboration','agreementAnnounced','strategic-collaboration','reported-occurrence','announcement para1','2020-05-01','day','event-date')
for label in ['Lonza','Moderna']:fact('ba-party-'+label,'BA-LONZA-2020-05','collaboration','namedParty',label,'assessment-content','announcement para1')
fact('ba-term','BA-LONZA-2020-05','collaboration','statedTermYears','10','assessment-content','announcement para1')
fact('ba-service','BA-LONZA-2020-05','collaboration','manufacturingTarget','mRNA-1273','planned','announcement para2')
fact('ba-transfer-plan','BA-LONZA-2020-05','technology-transfer','transferBegins','true','planned','announcement para2','2020-06','month','planned-window')
fact('ba-batch-plan','BA-LONZA-2020-05','initial-batches','manufactured','true','planned','announcement para2','2020-07','month','planned-window')
fact('ba-capability','BA-LONZA-2020-05','Lonza','expertise','scaling-manufacture','reported-capability','paragraph on experience')
fact('ba-transfer-complete','BA-LONZA-2020-07','technology-transfer','transferCompleted','true','reported-occurrence','collaboration progress paragraph','2020-07-24','day','event-upper-bound')
fact('ba-batch-still-plan','BA-LONZA-2020-07','initial-batches','delivered','true','planned','collaboration progress paragraph','2020-07','month','planned-window')
fact('ba-existing-visp','BA-LONZA-2021-04','existing-Visp-lines','installedCount','3','reported-occurrence','paragraph beginning In May 2020','2021-04-29','day','event-upper-bound')
fact('ba-existing-portsmouth','BA-LONZA-2021-04','existing-Portsmouth-lines','installedCount','1','reported-occurrence','paragraph beginning In May 2020','2021-04-29','day','event-upper-bound')
fact('ba-production','BA-LONZA-2021-04','Visp-production','commenced','true','reported-occurrence','paragraph beginning In May 2020','2021-04-29','day','event-upper-bound')
fact('ba-new-lines-plan','BA-LONZA-2021-04','additional-Visp-lines','operationalCount','3','planned','paragraph on expected operationalization','2022','year','planned-window')
g.add((T['ba-new-lines-plan'],E.timeQualifier,Literal('earlier-part-of-year; no exact subinterval established')))
rows[-1]['source_time_qualifier']='earlier-part-of-year; no exact subinterval established'
# DS: neither publication/update date nor E2B(R3) is a build version.
fact('ds-launch','DS-EMA-LIVE','EudraVigilance-launch','launched','true','reported-occurrence','opening English paragraph')
fact('ds-launch-date','DS-EMA-TIMELINE','EudraVigilance-launch','launched','true','reported-occurrence','timeline item10','2017-11-22','day','event-date')
fact('ds-standard','DS-EMA-TIMELINE','EudraVigilance','messageStandard','ICH-E2B-R3','reported-capability','timeline item10')
fact('ds-launching-actor','DS-EMA-LIVE','EudraVigilance-launch','launchingOrganization','EMA','reported-occurrence','opening English paragraph')
fact('ds-reporting-function','DS-EMA-LIVE','EudraVigilance','supportsFunction','safety-reporting-and-analysis','reported-capability','opening English paragraph and benefits')
# Registry evidence advances a separate gap without pretending a licence ID was read.
fact('reg-grant','REG-SWISSMEDIC-2021','Visp-establishment-licence','granted','true','authorization-report','opening paragraph','2021-03-15','day','event-upper-bound')
fact('reg-authority','REG-SWISSMEDIC-2021','Visp-establishment-licence','grantingAuthority','Swissmedic','authorization-report','opening paragraph')
fact('reg-holder','REG-SWISSMEDIC-2021','Visp-establishment-licence','namedHolder','Lonza','authorization-report','opening paragraph')
fact('reg-scope','REG-SWISSMEDIC-2021','Visp-establishment-licence','scope','manufacture-active-substance-for-Moderna','authorization-report','second paragraph')
# Explicit proposed mappings to existing model vocabulary, not asserted world facts.
maps=[
 ('RM','sartan-review',RDF.type,C.RiskAssessmentActivity,'RM-EMA-2020'),
 ('RM','sartan-revision',RDF.type,C.RiskReviewActivity,'RM-EMA-2020'),
 ('RM','sartan-revision',L.reviewPriorResult,T['sartan-prior-result'],'RM-EMA-2020'),
 ('RM','sartan-revision',L.reviewNewResult,T['sartan-revised-result'],'RM-EMA-2020'),
 ('BA','collaboration',RDF.type,C.StrategicPartnershipAgreement,'BA-LONZA-2020-05'),
 ('BA','collaboration',C.partnershipParticipant,T.Lonza,'BA-LONZA-2020-05'),
 ('BA','collaboration',C.partnershipParticipant,T.Moderna,'BA-LONZA-2020-05'),
 ('BA','Lonza',RDF.type,C.PartnerOrganizationRole,'BA-LONZA-2020-05'),
 ('BA','Moderna',RDF.type,C.PartnerOrganizationRole,'BA-LONZA-2020-05'),
 ('BA','manufacturing-capability',RDF.type,C.EnterpriseCapability,'BA-LONZA-2020-05'),
 ('BA','manufacturing-capability',C.capabilityBearer,T.Lonza,'BA-LONZA-2020-05'),
 ('DS','EudraVigilance-launch',RDF.type,C.SystemDeploymentActivity,'DS-EMA-LIVE'),
 ('DS','EudraVigilance',RDF.type,C.DigitalInformationSystemComponent,'DS-EMA-LIVE')]
for i,(domain,subject,predicate,obj,src) in enumerate(maps):add(g,'map-'+str(i),src,subject,predicate,obj,'mapping-proposal','proposed-model-crosswalk')
dump('extractions.json',{'rows':rows,'count':len(rows),'selection':'documentary statements; classified modes and ontology mappings are analyst interpretations','mapping_count':len(maps)})
dump('mapping-proposals.json',{'mappings':[{'domain':m,'subject':s,'predicate':str(p),'object':str(o),'source':src,'accepted':False} for m,s,p,o,src in maps],'warnings':['A strategic collaboration announcement is not the full executed contract','System-wide EudraVigilance to component-class mapping needs granularity review','Public regulatory review is not a company risk register or treatment effectiveness study']})
save('evidence.ttl',g);save('proposed-delta.ttl',M);save('proposed-shapes.ttl',S)
checks=[];fixtures=Dataset()
def check(name,actual,expected,kind):checks.append({'id':name,'kind':kind,'actual':actual,'expected':expected,'pass':actual==expected})
def admit(name,z,want):fixtures.graph(URIRef('urn:cmpe-witness-case:'+name)).__iadd__(z);check(name,admission(z)['conforms'],want,'admission')
admit('real-documentary-witnesses',g,True)
for name,mut in [
 ('missing-mode',lambda z:z.remove((T['ds-launch'],E.claimMode,None))),
 ('bad-mode',lambda z:(z.remove((T['ds-launch'],E.claimMode,None)),z.add((T['ds-launch'],E.claimMode,Literal('occurred-for-sure'))))),
 ('missing-precision',lambda z:z.remove((T['rm-review'],E.timePrecision,None))),
 ('invalid-month',lambda z:(z.remove((T['rm-review'],E.timeLexical,None)),z.add((T['rm-review'],E.timeLexical,Literal('2019-13'))))),
 ('invalid-day',lambda z:(z.remove((T['ds-launch-date'],E.timeLexical,None)),z.add((T['ds-launch-date'],E.timeLexical,Literal('2017-02-30'))))),
 ('planned-as-event-time',lambda z:(z.remove((T['ba-batch-plan'],E.timeRole,None)),z.add((T['ba-batch-plan'],E.timeRole,Literal('event-date'))))),
 ('mapping-as-extraction',lambda z:(z.remove((T['map-0'],B.claimOrigin,None)),z.add((T['map-0'],B.claimOrigin,Literal('source-extracted'))))),
 ('untraceable-claim',lambda z:z.remove((T['RM-EMA-2020'],E.sourceID,None))),
 ('unknown-time-as-day',lambda z:(z.remove((T['ds-launch'],E.timePrecision,None)),z.add((T['ds-launch'],E.timePrecision,Literal('day'))))),
 ('bad-source-date',lambda z:(z.remove((T['RM-EMA-2020'],E.sourceDate,None)),z.add((T['RM-EMA-2020'],E.sourceDate,Literal('2020-99-01'))))),
 ('claim-carrier-collision',lambda z:z.add((T['ds-launch'],RDF.type,C.SourceRecord)))]:
 z=g+Graph();mut(z);admit(name,z,False)
# Explicit witnesses are identified by a profile, so deleting mode cannot evade targeting.
queries=[
 ('risk-review-reported','sartan-review','reviewConcluded','true','reported-occurrence',None,'SOURCE_REPORTED_OCCURRENCE'),
 ('requirement-not-execution','manufacturers','riskEvaluationAndTesting','required','reported-occurrence',None,'NOT_REPORTED_IN_SELECTED_MODE'),
 ('requirement-preserved','manufacturers','riskEvaluationAndTesting','required','required',None,'SOURCE_REPORTED_REQUIRED'),
 ('batch-plan-preserved','initial-batches','manufactured','true','planned','2020-05-01','SOURCE_REPORTED_PLANNED'),
 ('batch-plan-not-occurrence','initial-batches','manufactured','true','reported-occurrence',None,'NOT_REPORTED_IN_SELECTED_MODE'),
 ('transfer-complete-after-update','technology-transfer','transferCompleted','true','reported-occurrence','2020-07-24','SOURCE_REPORTED_OCCURRENCE'),
 ('no-future-report-leak','technology-transfer','transferCompleted','true','reported-occurrence','2020-05-01','NOT_REPORTED_IN_SELECTED_MODE'),
 ('production-commenced','Visp-production','commenced','true','reported-occurrence','2021-04-29','SOURCE_REPORTED_OCCURRENCE'),
 ('additional-lines-remain-plan','additional-Visp-lines','operationalCount','3','reported-occurrence',None,'NOT_REPORTED_IN_SELECTED_MODE'),
 ('launch-has-documentary-evidence','EudraVigilance-launch','launched','true','reported-occurrence',None,'SOURCE_REPORTED_OCCURRENCE'),
 ('build-version-not-invented','EudraVigilance','softwareBuild','ICH-E2B-R3','reported-occurrence',None,'NOT_REPORTED_IN_SELECTED_MODE'),
 ('standard-is-supported','EudraVigilance','messageStandard','ICH-E2B-R3','reported-capability',None,'SOURCE_REPORTED_CAPABILITY'),
 ('licence-report','Visp-establishment-licence','granted','true','authorization-report',None,'SOURCE_REPORTED_AUTHORIZATION_REPORT'),
 ('licence-not-marketing-approval','Visp-establishment-licence','productMarketingAuthorization','true','authorization-report',None,'NOT_REPORTED_IN_SELECTED_MODE')]
answers=[]
for name,subject,predicate,obj,mode,asof,want in queries:
 result=answer(g,T[subject],E[predicate],Literal(obj),mode,asof);check(name,result['status'],want,'query');answers.append({'id':name,'question':{'subject':subject,'predicate':predicate,'object':obj,'mode':mode,'source_cutoff':asof},'answer':result})
check('mapping-remains-proposal',answer(g,T['sartan-review'],RDF.type,C.RiskAssessmentActivity,'mapping-proposal')['status'],'MAPPING_PROPOSED','query')
check('month-retains-range',[x.isoformat() for x in time_interval('2019-01','month')],['2019-01-01','2019-01-31'],'time')
check('day-precision',[x.isoformat() for x in time_interval('2017-11-22','day')],['2017-11-22','2017-11-22'],'time')
check('year-not-invented-quarter',[x.isoformat() for x in time_interval('2022','year')],['2022-01-01','2022-12-31'],'time')
z=g+Graph();add(z,'synthetic-conflict','DS-EMA-TIMELINE','EudraVigilance-launch',E.launched,'true','reported-occurrence','synthetic-test-not-real-source',polarity='negative')
check('explicit-conflict-visible',answer(z,T['EudraVigilance-launch'],E.launched,Literal('true'))['status'],'SOURCE_CONFLICT','query')
logical=[]
for name,z,want in [('full-positive',g,True),('no-materialized-mapping',g+Graph(),True),('claim-source-identity-collision',g+Graph(),False)]:
 if name=='no-materialized-mapping':
  for _,subject,predicate,obj,_ in maps:
   if predicate==RDF.type:coh.ctx.prev.not_type(z,T[subject],obj)
   else:coh.ctx.prev.not_edge(z,T[subject],predicate,obj)
 if name=='claim-source-identity-collision':z.add((T['ds-launch'],RDF.type,C.SourceRecord))
 r=coh.ctx.prev.hermit(coh.full+M+z);logical.append({'id':name,**r,'expected':want,'pass':r['consistent']==want and not r['unsatisfiable_named_classes']})
save('fixtures.trig',fixtures);dump('answers.json',answers);dump('results.json',{'checks':checks,'passed':sum(x['pass'] for x in checks),'total':len(checks),'logical':logical,'logical_passed':sum(x['pass'] for x in logical),'source_count':len(sources),'source_extractions':len(rows),'proposed_mappings':len(maps)})
print(json.dumps({'passed':sum(x['pass'] for x in checks),'total':len(checks),'logical':sum(x['pass'] for x in logical),'failures':[x for x in checks if not x['pass']]}),flush=True)
assert all(x['pass'] for x in checks+logical)
