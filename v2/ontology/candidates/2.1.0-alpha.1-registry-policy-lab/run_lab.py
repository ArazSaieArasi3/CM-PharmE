"""Predeclared source scenarios, malformed-input controls and regression replay."""
import copy,json,sys
from pyshacl import validate
from lab import *
S=shapes();save(S,'proposed-shapes.ttl');save(delta(),'proposed-delta.ttl')
CASES=[];Q=[]
def ids(*v):return ['B2-'+x for x in v]
def check(name,g,want,reqs,polarity,marker=None):
 actual,report,_=validate(g+hierarchy,shacl_graph=base_shapes+S,advanced=True,inference='none')
 details=[{'focus':str(report.value(x,SH.focusNode) or ''),'path':str(report.value(x,SH.resultPath) or ''),'constraint':str(report.value(x,SH.sourceConstraint) or ''),'shape':str(report.value(x,SH.sourceShape) or ''),'component':str(report.value(x,SH.sourceConstraintComponent) or '')} for x in report.subjects(RDF.type,SH.ValidationResult)]
 fixture='fixtures/'+name+'.ttl';save(g,fixture)
 CASES.append({'name':name,'requirements':reqs,'polarity':polarity,'expected_conforms':want,'actual_conforms':bool(actual),'marker':marker,'violations':details,'fixture':fixture,'pass':bool(actual)==want and (marker is None or any(marker in str(d) for d in details))})
def query_case(name,g,operation,args,want,reqs,polarity):
 funcs={'query':query,'approval':approval_answer,'lookup':lookup,'window':window,'applicability':applicability}
 actual=funcs[operation](g,**args);fixture='fixtures/'+name+'.ttl';save(g,fixture)
 Q.append({'name':name,'requirements':reqs,'polarity':polarity,'operation':operation,'args':{k:str(v) if isinstance(v,URIRef) else v for k,v in args.items()},'expected':want,'actual':actual,'fixture':fixture,'pass':actual==want})

reg=registry();listing=registry('listing');org=registry(organization_subject=True);prov=provenance();sub=submission();potential=shortage()
for name,g,reqs in [
 ('registration-positive',reg,ids('RG-01','RG-02','RG-04','RG-07')),
 ('listing-positive',listing,ids('RG-03','RG-04','RG-06')),
 ('organization-self-report-positive',org,ids('RG-07')),
 ('provenance-positive',prov,ids('DS-07','DS-08','DS-09','DS-10')),
 ('submission-positive',sub,ids('RG-08')),
 ('potential-shortage-positive',potential,ids('RP-02'))]:check(name,g,True,reqs,'positive')
for scenario in ['routine','preparedness','crisis']:check(scenario+'-scope-positive',reporting(scenario),True,ids('RP-01','RP-03','RP-04'),'positive')
g=reg+Graph();g.remove((T.mandate,None,None));g.remove((T.conferrer,None,None));check('missing-inherited-authority-grounding',g,False,ids('RG-01'),'negative','MinCountConstraintComponent')

g=reg+Graph();g.set((T.record,P.recordKind,Literal('listing')));check('registration-is-not-listing',g,False,ids('RG-01'),'negative','fact-kind-subject-agreement')
g=reg+Graph();g.set((T.record,P.approvalConclusion,Literal('source-asserted-approved')));check('registration-alone-cannot-support-approval',g,False,ids('RG-02'),'negative','approval-needs-independent-decision')
g=listing+Graph();g.set((T.record,P.approvalConclusion,Literal('source-asserted-approved')));g.add((T.record,P.approvalEvidence,T.record));check('listing-cannot-approve-itself',g,False,ids('RG-03'),'negative','approval-needs-independent-decision')
g=reg+Graph();g.remove((T.record,PROV.wasAttributedTo,None));check('missing-submitting-labeler',g,False,ids('RG-04'),'negative','wasAttributedTo')
g=listing+Graph();g.set((T.record,P.marketingEnd,Literal('2026-08-01',datatype=XSD.date)));check('reversed-marketing-dates',g,False,ids('RG-06'),'negative','marketing-interval-order')
g=reg+Graph();g.add((T.record,OWL.sameAs,T.facility));check('record-subject-alias',g,False,ids('RG-07'),'negative','record-not-subject')
g=sub+Graph();g.add((T.record,OWL.sameAs,T.product));check('payload-product-alias',g,False,ids('RG-08'),'negative','payload-not-product')
g=reporting();g.remove((T.requirement,P.jurisdiction,None));check('missing-jurisdiction',g,False,ids('RP-01'),'negative','jurisdiction')
g=reporting();value(g,T.requirement,P.authorizationRoute,'NAP');check('routine-NAP-overgeneralization',g,False,ids('RP-03'),'negative','routine-scope-guard')
g=reporting('preparedness');g.remove((T.requirement,P.scopedProduct,None));check('action-without-explicit-product-scope',g,False,ids('RP-03'),'negative','action-scope-required')
g=reporting('crisis');g.remove((T.requirement,P.frequency,None));check('missing-action-frequency',g,False,ids('RP-04'),'negative','frequency')
g=potential+Graph();types(g,T.situation,C.MedicineShortageSituation);g.add((T.claim,OWL.sameAs,T.situation));check('potential-claim-is-not-situation',g,False,ids('RP-02'),'negative','claim-not-situation')
g=prov+Graph();g.add((T.record,OWL.sameAs,T.activity));check('record-activity-alias',g,False,ids('DS-07'),'negative','record-not-generating-activity')
g=prov+Graph();g.remove((T.activity,PROV.wasAssociatedWith,None));check('attribution-does-not-replace-activity-association',g,False,ids('DS-08'),'negative','associated-actor-required')
g=prov+Graph();g.remove((T.record,PROV.wasDerivedFrom,None));check('revision-missing-explicit-derivation',g,False,ids('DS-09'),'negative','revision-needs-lineage')
g=prov+Graph();g.add((T.record,OWL.sameAs,T.alias));g.add((T.alias,OWL.sameAs,T.previous));check('revision-alias-chain',g,False,ids('DS-10'),'negative','revision-known-identity-collision')

# Query oracles are literal expectations stated independently of function output.
query_case('registration-subject-query',reg,'query',{'key':'registered-subject'},[[str(T.facility)]],ids('RG-01'),'positive')
query_case('registration-does-not-create-listing-query',reg,'query',{'key':'listed-subject'},[],ids('RG-01'),'negative')
query_case('registration-approval-unknown',reg,'approval',{},'UNKNOWN',ids('RG-02'),'positive')
query_case('NDC-approval-unknown',listing,'approval',{},'UNKNOWN',ids('RG-03'),'positive')
g=listing+Graph();g.add((T.record,P.approvalEvidence,T.record));query_case('listing-self-evidence-insufficient',g,'approval',{},'UNKNOWN',ids('RG-03'),'negative')
g=reg+Graph();types(g,T.decision,C.SourceRecord);value(g,T.decision,P.recordKind,'regulatory-decision');g.add((T.decision,P.recordSubject,T.facility));g.add((T.record,P.approvalEvidence,T.decision))
query_case('independent-decision-available-not-verified',g,'approval',{},'SOURCE_DECISION_AVAILABLE_NOT_VERIFIED',ids('RG-02'),'boundary')
query_case('submitter-is-labeler',listing,'query',{'key':'submitter'},[[str(T.reporter)]],ids('RG-04'),'positive')
query_case('absent-code-is-source-scoped',listing,'lookup',{'key':'NOT-IN-RELEASE'},{'source_result':'NOT_FOUND_IN_RELEASE','approval':'UNKNOWN'},ids('RG-05'),'negative')
query_case('present-code-does-not-establish-approval',listing,'lookup',{'key':'SYNTHETIC-001'},{'source_result':'FOUND','approval':'UNKNOWN'},ids('RG-05'),'positive')
for label,date,expected,polarity in [('before','2026-08-31','OUTSIDE_DECLARED_WINDOW','negative'),('start','2026-09-01','WITHIN_DECLARED_WINDOW','positive'),('end','2026-11-01','OUTSIDE_DECLARED_WINDOW','boundary')]:
 query_case('marketing-window-'+label,listing,'window',{'on_date':date},expected,ids('RG-06'),polarity)
g=listing+Graph();g.set((T.record,P.retrievedAt,Literal('2026-09-01T00:00:00Z',datatype=XSD.dateTime)));check('coincident-marketing-and-retrieval-allowed',g,True,ids('RG-06'),'boundary')
g=listing+Graph();g.remove((T.record,P.marketingEnd,None));query_case('undeclared-marketing-end-is-unknown',g,'window',{'on_date':'2026-10-01'},'UNKNOWN',ids('RG-06'),'boundary')
query_case('self-report-organizational-subject',org,'query',{'key':'registered-subject'},[[str(T.reporter)]],ids('RG-07'),'positive')
query_case('payload-to-product',sub,'query',{'key':'represented-product'},[[str(T.product)]],ids('RG-08'),'positive')
query_case('potential-report-status',potential,'query',{'key':'source-asserted-shortage'},[['potential']],ids('RP-02'),'positive')
query_case('potential-report-no-actual-instance',potential,'query',{'key':'actual-shortage-instances'},[],ids('RP-02'),'negative')

MATRIX=[
 ('routine-MAH-CAP','routine',{'role':'MAH','route':'CAP'},'APPLICABLE_IN_PROFILE',['RP-01','RP-03'],'positive'),
 ('routine-NCA-excluded','routine',{'role':'NCA','route':'CAP'},'NOT_APPLICABLE_IN_PROFILE',['RP-01'],'negative'),
 ('routine-NAP-excluded','routine',{'role':'MAH','route':'NAP'},'NOT_APPLICABLE_IN_PROFILE',['RP-03'],'negative'),
 ('preparedness-NCA-NAP','preparedness',{'role':'NCA','route':'NAP'},'APPLICABLE_IN_PROFILE',['RP-01','RP-03'],'positive'),
 ('crisis-MAH-NAP','crisis',{'role':'MAH','route':'NAP'},'APPLICABLE_IN_PROFILE',['RP-03'],'positive'),
 ('unselected-product','crisis',{'role':'MAH','route':'CAP','product':T.otherProduct},'NOT_APPLICABLE_IN_PROFILE',['RP-03'],'negative'),
 ('wrong-jurisdiction','crisis',{'role':'MAH','route':'CAP','jurisdiction':T.otherJurisdiction},'NOT_APPLICABLE_IN_PROFILE',['RP-01'],'negative'),
 ('unknown-role','routine',{'role':None,'route':'CAP'},'UNKNOWN',['RP-01'],'boundary'),
 ('unknown-route','routine',{'role':'MAH','route':None},'UNKNOWN',['RP-03'],'boundary'),
 ('expired-scope','crisis',{'role':'MAH','route':'CAP','at':'2026-11-01T00:00:00Z'},'NOT_APPLICABLE_IN_PROFILE',['RP-04'],'negative'),
 ('wrong-scenario','routine',{'role':'MAH','route':'CAP','scenario':'crisis'},'NOT_APPLICABLE_IN_PROFILE',['RP-01'],'negative')]
for name,scenario,args,want,reqs,polarity in MATRIX:query_case(name,reporting(scenario),'applicability',args,want,ids(*reqs),polarity)
g=reporting('crisis');g.remove((T.requirement,P.scopeComplete,None));query_case('incomplete-scope-not-negative',g,'applicability',{'role':'MAH','route':'CAP','product':T.otherProduct},'UNKNOWN',ids('RP-03'),'boundary')
g=reporting('crisis');g.remove((T.requirement,P.actionAnnounced,None));query_case('unannounced-action-unknown',g,'applicability',{'role':'MAH','route':'CAP'},'UNKNOWN',ids('RP-01'),'boundary')
g=reporting();g.set((T.requirement,C.validFrom,Literal('2026-10-01T00:00:00',datatype=XSD.dateTime)));query_case('timezone-not-assumed',g,'applicability',{'role':'MAH','route':'CAP'},'UNKNOWN',ids('RP-04'),'boundary')
query_case('action-frequency-query',reporting('crisis'),'query',{'key':'frequency'},[['synthetic-action-specific-frequency']],ids('RP-04'),'positive')
g=reporting('crisis');g.set((T.requirement,P.frequency,Literal('synthetic-revised-frequency')));query_case('frequency-not-hardcoded',g,'query',{'key':'frequency'},[['synthetic-revised-frequency']],ids('RP-04'),'negative')
for name,key,want,req in [('generation-query','generation',[[str(T.activity)]],'DS-07'),('two-responsibilities-query','attribution-and-association',[[str(T.author),str(T.operator)]],'DS-08'),('derivation-query','derivation',[[str(T.previous)]],'DS-09'),('revision-query','revision',[[str(T.previous)]],'DS-10')]:query_case(name,prov,'query',{'key':key},want,ids(req),'positive')
g=prov+Graph();g.remove((T.record,PROV.wasDerivedFrom,None));query_case('missing-lineage-not-invented',g,'query',{'key':'derivation'},[],ids('DS-09'),'negative')

write('shacl-results.json',{'cases':CASES,'pass':sum(c['pass'] for c in CASES),'total':len(CASES)})
write('query-results.json',{'cases':Q,'pass':sum(c['pass'] for c in Q),'total':len(Q),'queries':QUERIES,'semantic_limit':'Absence in SPARQL results is not global OWL non-entailment; selected HermiT countermodels are separate.'})
print(json.dumps({'shacl':f"{sum(c['pass'] for c in CASES)}/{len(CASES)}",'queries':f"{sum(c['pass'] for c in Q)}/{len(Q)}"}),flush=True)
bad=[c for c in CASES+Q if not c['pass']]
if bad:print(json.dumps(bad,ensure_ascii=False,indent=2),flush=True);raise SystemExit(1)

# Profiles are opt-in. Replay actual historical witnesses, preserving expectations.
if '--no-regression' not in sys.argv:
 prior=[];first=H.parent/'2.1.0-alpha.1-four-domain-lab'
 prior.extend((first,c) for c in json.loads((first/'shacl-results.json').read_text())['cases'])
 prior.extend((OLD,c) for c in json.loads((OLD/'refinement-shacl-results.json').read_text()))
 prior.extend((POLICY,c) for c in json.loads((POLICY/'shacl-results.json').read_text()))
 regress=[]
 for folder,c in prior:
  g=Graph().parse(folder/c['fixture']);ok,report,_=validate(g+hierarchy,shacl_graph=base_shapes+S,advanced=True,inference='none')
  marker=c.get('expected_failure_marker',c.get('expected_marker'))
  details=[str(report.value(x,SH.resultPath) or '')+' '+str(report.value(x,SH.sourceConstraint) or '') for x in report.subjects(RDF.type,SH.ValidationResult)]
  regress.append({'source':folder.name+'/'+c['fixture'],'expected':c['expected_conforms'],'actual':bool(ok),'marker':marker,'pass':bool(ok)==c['expected_conforms'] and (marker is None or any(marker in x for x in details))})
 write('prior-regression-results.json',{'cases':regress,'pass':sum(c['pass'] for c in regress),'total':len(regress),'C_materialization_applied':False,'C_regression_change_still_unaccepted':True})
 print(json.dumps({'historical_regression':f"{sum(c['pass'] for c in regress)}/{len(regress)}"}),flush=True)
 assert all(c['pass'] for c in regress)
