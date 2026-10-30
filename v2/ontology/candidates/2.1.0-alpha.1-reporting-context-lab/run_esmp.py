"""Versioned official guidance witnesses, NOT operational ESMP submissions/actions."""
from lab import *
meta=json.loads((H/'sources/esmp-guide-manifest.json').read_text())
g=graph();source=B['EMA-guide-1.4-'+meta['sha256'][:12]];typ(g,source,C.SourceRecord)
value(g,source,B.sourceURL,meta['url'],XSD.anyURI);value(g,source,B.sourceSHA256,meta['sha256'])
jur=B['EU-EEA-declared'];typ(g,jur,C.RegulatoryJurisdiction)
evidence=[
 {'id':'E01','pages':[35],'rule':'A specific preparedness action or crisis determines its own product scope and reporting start; generic guidance is not an action announcement.','requirements':['CTX-04','CTX-05']},
 {'id':'E02','pages':[35,51],'rule':'Availability templates require marketed or temporarily unavailable status for the relevant product/presentation and country.','requirements':['CTX-02','CTX-07']},
 {'id':'E03','pages':[35],'rule':'Manufacturing and alternative-therapy forms are generated independently of marketing status.','requirements':['CTX-07']},
 {'id':'E04','pages':[49],'rule':'Submission frequency is specified for the particular crisis or preparedness action.','requirements':['CTX-06']},
 {'id':'E05','pages':[19,24],'rule':'Routine CAP shortage templates use the marketing status of the presentation in the specific country.','requirements':['CTX-02','CTX-07']},
 {'id':'E06','pages':[7,35],'rule':'Product-master-data completeness and account/access prerequisites remain separate from matching the bounded scope criteria.','requirements':['CTX-08']}
]
specs=[]
for name,scenario,kind,policy,routes,pages in [
 ('routine-cap','routine','routine-shortage','require-marketed-status',['CAP'],[19,24]),
 ('preparedness-availability','preparedness','availability','require-marketed-status',['CAP','NAP'],[35,51]),
 ('preparedness-manufacturing','preparedness','manufacturing','not-a-condition',['CAP','NAP'],[35]),
 ('preparedness-alternatives','preparedness','alternative-therapies','not-a-condition',['CAP','NAP'],[35]),
 ('crisis-availability','crisis','availability','require-marketed-status',['CAP','NAP'],[35,51])]:
 sp=B['EMA-'+name+'-1.4'];typ(g,sp,B.ReportingScopeSpecification);g.add((sp,B.specificationSource,source));g.add((sp,B.scopeJurisdiction,jur))
 for p,v in [(B.specificationVersion,'EMA-MAH-1.4-2026-04-28'),(B.allowedRole,'MAH'),(B.scenario,scenario),(B.submissionKind,kind),(B.marketingPolicy,policy),(B.scopeMode,'all-declared-route-products' if scenario=='routine' else 'enumerated')]:value(g,sp,p,v)
 for route in routes:value(g,sp,B.allowedRoute,route)
 value(g,sp,B.evidencePointer,'EMA guide v1.4 pp. '+','.join(map(str,pages)))
 # No invented action IRI, announcement, complete product list or validity end.
 if scenario!='routine':value(g,sp,B.scopeComplete,False);value(g,sp,B.actionState,'unknown');value(g,sp,B.actionEvidenceKind,'guidance')
 specs.append({'id':str(sp),'scenario':scenario,'kind':kind,'marketing_policy':policy,'pages':pages})
sh=validate_graph(g);hr=prev.hermit(full+g)
checks=[{'name':'official-guidance-profiles-shacl','pass':sh['conforms']},{'name':'official-guidance-hermit','pass':hr['consistent'] and not hr['unsatisfiable_named_classes']}]
outcomes=[];tests=Dataset()
for row in specs:
 sp=URIRef(row['id']);x=g+Graph();synthetic,_,ctx=fixture(row['scenario'],row['kind'])
 for s,p,o in synthetic:
  if s==ctx or s in [T.org,T.product,T.presentation,T.jurisdiction]:x.add((s,p,o))
 x.set((ctx,B.contextVersion,Literal('EMA-MAH-1.4-2026-04-28')));x.set((ctx,B.contextJurisdiction,jur));x.remove((ctx,B.contextAction,None))
 result=evaluate(x,sp,ctx);checks.append({'name':row['kind']+'-'+row['scenario']+'-unknown-activation-or-time','pass':result['verdict']=='UNKNOWN','result':result})
 outcomes.append({'scope':row['id'],'context_origin':'SYNTHETIC_NOT_REAL_SUBMISSION','result':result})
 t=tests.graph(URIRef('urn:esmp-guidance-test:'+row['scenario']+'-'+row['kind']))
 for triple in x:t.add(triple)
 if row['scenario']!='routine':checks.append({'name':row['id']+'-does-not-fabricate-action','pass':result['dimensions']['action']=='UNKNOWN'})
 checks.append({'name':row['id']+'-marketing-policy','pass':result['dimensions']['marketing']==('MATCH' if row['marketing_policy']=='require-marketed-status' else 'NOT_REQUIRED')})
g.serialize(H/'esmp-guidance.ttl',format='turtle');tests.serialize(H/'esmp-test-contexts.trig',format='trig')
write('source-evidence.json',{'source':meta,'extractions':evidence,'status':'MANUAL_SOURCE_TRACED_DESIGN_EXTRACTION_NOT_INDEPENDENT_EXPERT_VALIDATION','profiles':specs,'real_operational_ESMP_submissions':0,'real_action_announcements_retrieved':0,'search_limit':'Targeted searches on ema.europa.eu found versioned guidance, platform launch notices and descriptions of preparedness monitoring. No complete action-specific notice with product scope/start/frequency was retrieved. This does not prove none exists.'})
out={'profiles':len(specs),'source_extractions':len(evidence),'real_guidance_documents':1,'real_action_announcements':0,'operational_submissions':0,'shacl':sh,'hermit':hr,'checks':checks,'pass':sum(x['pass'] for x in checks),'total':len(checks),'outcomes':outcomes,'limit':'Real documentary evidence plus explicitly synthetic query contexts. No actual reporting obligation, account readiness or legal compliance determination.'}
write('esmp-results.json',out);print(json.dumps({k:out[k] for k in ['profiles','source_extractions','pass','total']}),flush=True)
assert all(x['pass'] for x in checks)
