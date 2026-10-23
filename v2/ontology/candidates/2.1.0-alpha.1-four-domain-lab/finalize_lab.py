"""Trace the original requirements without silently broadening test claims."""
import json,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent
ROOT=H.parents[3]
DOS=ROOT/'v2/research/w4/minimum-viable-domains-2026-10-09'
BASE=H.parent/'2.1.0-alpha.1-g3-p4a-supply-capacity'
for path in H.rglob('*.ttl'):
 path.write_text(path.read_text().rstrip()+'\n')
def read(p):return json.loads(p.read_text())
def write(name,value):(H/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
# Each row is a manual mapping of an existing requirement, not generated acceptance.
# properties; profiles; particular witnesses; remaining coverage/semantic limitation
M={
'RM':[
('assessmentScenario scenarioProduct','risk-assessment risk-scenario','missing-scenario-topic','Product path tested; facility and supply-dependency scenario paths remain unimplemented.'),
('resultAssessment','risk-result','result-is-assessment','Event/content collision rejected; unpublished-result identity cases need an independent witness.'),
('citesSourceRecord','risk-result','missing-evidence','Recoverable citation is tested, not evidential strength or qualified EvidenceSupport.'),
('planRiskResult','risk-plan','dangling-plan-result','Typed explicit references tested; target Assertion need not yet satisfy the risk-result profile.'),
('implementsRiskPlan','risk-treatment','dangling-executed-plan','HermiT countermodel permits a plan with zero executions; actual execution still requires evidence.'),
('reviewPriorResult reviewNewResult atTime','risk-review','missing-review-predecessor backdated-revision','Two-result time ordering tested; full revision identity and review-author provenance remain open.')],
'PV':[
('reportsRecord','safety-reporting','reporting-is-record','Repeated reporting of one carrier tested; content identity across different report carriers is unresolved.'),
('signalProduct signalSubstance','safety-signal','missing-target','Both product and substance paths tested; no brand requirement introduced.'),
('citesSourceRecord','safety-signal','missing-signal-source','Study-source reference works without an individual report; citation is not established causal evidence.'),
('pvResultSignal pvResultAssessment signalAssessmentTarget','signal-result signal-assessment','dangling-signal signal-is-own-result signal-result-alias result-assessment-target-disagreement','Distinct identifiers and assessment-target agreement tested; both contents remain Assertion, with profile-level distinctions only.'),
('atTime signalStatus','signal-result','missing-result-time','Two timed results preserved; authority responsible for an assessment and controlled status vocabulary remain open.'),
('pvRequirementJurisdiction surveillanceRequirement','pv-requirement pv-surveillance','missing-jurisdiction','Explicit jurisdiction linkage and non-propagation tested; actual legal applicability/compliance is not inferred.')],
'BA':[
('c:capabilityBearer','ba-service','missing-capability-bearer','Reuses the existing intrinsic Mode bearer relation; this does not adjudicate every capability identity condition.'),
('capabilityRealizedIn','ba-service','positive','Consistent zero-exercise countermodel tested; realization only targets ManufacturingActivity in this experiment.'),
('serviceCapability','ba-service','service-without-capability','Capability dependency tested; a generic capability does not yet establish a pharmaceutical service context.'),
('viewOrganization viewService','ba-view','view-is-organization untyped-view-reference','Reuses organization identifiers; no automatic new organization follows from creating a view.'),
('c:partnershipParticipant','ba-partnership','one-partner-only known-partner-aliases','Only participant admission tested. Commitment evidence and casual-interaction-without-partner inference remain unimplemented.'),
('viewOrganization','ba-view','boundary','Fixture without a view keeps explicit product/facility types; no full identity or deletion semantics proof.')],
'DS':[
('recordDigitalActivity deploymentComponent','digital-record deployment','record-is-component','Explicit record/component identity collision rejected; software artifact versus agent modeling remains open.'),
('digitalActivityDeployment componentVersion','digital-activity deployment','missing-version','Two deployments/versions preserve the first record trace; version identity is a local string, not a complete version model.'),
('digitalServiceActivity digitalServiceComponent','digital-service','service-without-supported-activity','Only ingestion/transformation ProvenanceActivity is supported; pharmaceutical business-activity grounding is still missing.'),
('recordDigitalActivity digitalActivityDeployment deploymentComponent deploymentOrganization','digital-record digital-activity deployment','missing-generating-activity','Record/activity/component/operator path queried; deployment organization is not automatically the responsible actor for every transformation.'),
('atTime componentVersion','deployment digital-activity','missing-deployment-time deployment-after-use','Timestamped upgrade history tested; validity intervals, overlapping deployments and rollback policy remain open.'),
('recordDigitalActivity','digital-record','positive','A consistent model with no RegulatoryAuthorization shows the scoped non-entailment; no registry or compliance completeness claim.')]
}
dossier=read(DOS/'domain-dossier.json');sh=read(H/'shacl-results.json');cq=read(H/'cq-results.json');reason=read(H/'reasoner-results.json')
rows=[]
for module in dossier['modules']:
 m=module['id']
 for req,mapping in zip(module['requirements'],M[m]):
  props,profiles,names,limit=mapping
  cases=[x for x in sh['cases'] if x['scenario'].startswith('SC-'+m+'-') and x['name'] in set(names.split()+['positive','boundary'])]
  qs=[x for x in cq if x['id'] in req['competency_questions']]
  rs=[x['name'] for x in reason['cases'] if x['name'].startswith(m+'-')]
  rows.append({'id':req['id'],'statement_fa':req['atomic_statement_fa'],'original_acceptance_fa':req['acceptance_criterion_fa'],
   'source_ids':req['evidence_sources'],'competency_question_ids':req['competency_questions'],'candidate_properties':props.split(),
   'admission_profiles':profiles.split(),'fixture_paths':[x['fixture'] for x in cases],
   'bounded_case_expectations_pass':bool(cases) and all(x['pass'] for x in cases),'query_expectations_pass':bool(qs) and all(x['pass'] for x in qs),
   'related_module_reasoner_cases':rs,'coverage_limit':limit,'status':'MAPPED_WITH_BOUNDED_EVIDENCE_NOT_ACCEPTED','author_acceptance':False})
assert len(rows)==24 and len({r['id'] for r in rows})==24
for row in rows:
 for p in row['fixture_paths']:assert (H/p).is_file(),p
write('requirement-traceability.json',{'requirements':rows,'mapped_count':24,'accepted_count':0,
 'meaning':'24/24 trace records, not 24/24 proven requirements. Every row retains an explicit limitation.'})

def structure(path):
 n=read(path);by={x['id']:x for x in n['elements']};cl={k:v for k,v in by.items() if v['type']=='Class' and v['stereotype']!='datatype'}
 adj={c:set() for c in cl};edges=set();typed=0;null_ends=0;null_cards=0;special=0;unclassified=0
 for e in by.values():
  ends=None
  if e['type']=='Generalization':ends=[e['general'],e['specific']]
  if e['type']=='BinaryRelation':
   ps=[by[p] for p in e['properties']];ends=[p['propertyType'] for p in ps]
   typed+=all(x in cl for x in ends);null_ends+=sum(p['propertyType'] is None for p in ps)
   null_cards+=sum(p['cardinality'] is None for p in ps);special+=sum(bool(p.get('subsettedProperties') or p.get('redefinedProperties')) for p in ps)
   unclassified+=e['stereotype'] is None
  if ends and all(x in cl for x in ends):
   a,b=ends;adj[a].add(b);adj[b].add(a);edges.add(tuple(sorted((a,b))))
 unseen=set(cl);components=[]
 while unseen:
  todo=[min(unseen)];seen=set()
  while todo:
   x=todo.pop()
   if x not in seen:seen.add(x);todo.extend(adj[x]-seen)
  unseen-=seen;components.append(sorted(seen))
 return {'elements':len(by),'named_classes':len(cl),'binary_relations':sum(e['type']=='BinaryRelation' for e in by.values()),
  'typed_named_relations':typed,'unique_undirected_edges':len(edges),'components':len(components),'largest_component':max(map(len,components)),
  'isolates':sorted(k for k,v in adj.items() if not v),'isolate_count':sum(not v for v in adj.values()),
  'untyped_ends':null_ends,'unknown_cardinality_ends':null_cards,'specialized_ends':special,'relations_without_stereotype':unclassified,
  'event_situation_classes':sum(e['type']=='Class' and e['stereotype'] in ['event','situation'] for e in by.values()),
  'nature_restrictions':sum(e['type']=='Class' and bool(e.get('restrictedTo')) for e in by.values())}
a=structure(BASE/'ontouml.json');b=structure(H/'ontouml-experimental.json')
manifest=read(H/'model-manifest.json')
assert all(hashlib.sha256((BASE/n).read_bytes()).hexdigest()==v for n,v in manifest['baseline_sha256'].items())
old={x['id']:x for x in read(BASE/'ontouml.json')['elements']};new={x['id']:x for x in read(H/'ontouml-experimental.json')['elements']}
unchanged=all(v==new[k] for k,v in old.items() if v['type']!='Package')
assert unchanged
write('structural-comparison.json',{'baseline':a,'experiment':b,'baseline_files_unchanged':True,'existing_nonpackage_native_elements_unchanged':unchanged,
 'connected_former_isolates':sorted(set(a['isolates'])-set(b['isolates'])),
 'meaning':'Undirected topology only, not semantic quality. The experiment is separate; current candidate retains its original topology.',
 'detector_limit':'Not a full detector run. Three new Event classes and 27 unclassified relations add scientific/adapter work.'})

queue=[]
for r in manifest['new_relations']:
 queue.append({**r,'decision':'OPEN','questions':['What ontological dependence/truthmaker justifies this association?','Reuse or specialize an existing relation instead?','What multiplicities hold universally, as distinct from local profile admission?','How are event participation or content-aboutness preserved in native/OWL/SHACL and the detector adapter?'],
  'requirement_ids':[x['id'] for x in rows if r['name'] in x['candidate_properties']]})
write('relation-review-queue.json',{'status':'P3_REVIEW_INPUT_NOT_ADJUDICATED','count':len(queue),'relations':queue})

plan=read(DOS/'continuation-plan.json')
plan['title']='CM-PharmE v2.1 — continuation checkpoint after four-domain executable experiment'
plan['execution_note']='Separate executable review experiment added. Baseline candidate and previous scientific dispositions unchanged; no final domain removal or gate closure.'
plan['experiment']='v2/ontology/candidates/'+H.name
for t in plan['tasks']:
 if t['id']=='N05':t['status']='HOLD_RETAIN_FOUR_EXECUTABLE_REVIEW_PROTOTYPES'
 if t['id']=='N09':t['status']='FOUR_DOMAIN_16_FAMILIES_EXECUTED_REMAINING_PROJECT_SCOPE_OPEN'
 if t['id']=='P3':t['current_extension']='27 experimental relation decisions added; prior relation review backlog remains.'
 if t['id'] in ['P4','P6a','P6b','P6d']:t['current_extension']='Bounded four-domain experiment executed; no full package closure.'
plan['exact_next']={'task':'N05/P3 semantic refinement','items':['Resolve report-carrier versus content identity and shared Assertion profile boundaries.','Ground BA service and DS activity in pharmaceutical context; add partnership commitment/casual-interaction witness.','Adjudicate 27 relation stereotypes, identity/dependence and native/OWL/SHACL alignment.','Then continue P5c/P5d/P5e full 20-pattern detector adaptation and independent data coverage.']}
plan['next_action_fa']='رفع شکاف‌های هویت و زمینهٔ دارویی چهار نمونه و داوری روابط P3، پیش از ادغام در مدل نامزد.'
plan['progress_current']={'four_domain_scenario_families':'16/16 bounded executions','requirement_trace_records':'24/24; acceptance 0/24',
 'closed_major_gates':'2/5 = 40% unchanged','closed_G3_packages':'2/7 = 28.6% unchanged','newly_closed_release_gates':0,
 'caution':'Execution coverage is not scientific acceptance, total effort progress, empirical coverage or ontology quality.'}
write('continuation-checkpoint.json',plan)
print(json.dumps({'trace_records':len(rows),'baseline_isolates':a['isolate_count'],'experimental_isolates':b['isolate_count'], 'baseline_preserved':unchanged,'relation_decisions_open':len(queue)}))
