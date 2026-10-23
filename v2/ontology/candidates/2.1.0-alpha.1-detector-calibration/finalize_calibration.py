"""Aggregate coverage without promoting basic witnesses to scientific acceptance."""
import json,hashlib,sys
from pathlib import Path
H=Path(__file__).resolve().parent;P=H.parent/'2.1.0-alpha.1-content-event-policy';A=Path(sys.argv[1])
def read(n):return json.loads((H/n).read_text())
def write(n,v):(H/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
x=read('calibration-results.json');b=read('readonly-boundary-results.json');a=read('adapter-results.json');hf=read('homofunc-boundary-results.json');old=json.loads((P/'sensitivity-results.json').read_text())
assert x['paired_cases']==x['paired_cases_pass']==34
assert x['prior_replay_cases']==x['prior_replay_pass']==8
for r in x['prior_replays']:
 before=next(c for c in old['rows'] if c['detector']==r['family'] and c['name']==r['name']);assert before['xmi_sha256']==r['fixture_sha256']
assert a['case_pass']==a['case_total']==3 and a['guard_pass']==a['guard_total']==8
assert b['total']==b['engine_expectation_pass']==4 and b['documentation_matches']==2
assert hf['total']==hf['engine_expectation_pass']==2 and hf['thesis_matches']==1
assert len(x['documentation_discrepancy_probes'])==2
assert all(not q['documentation_expectation_matches'] and q['engine_expectation_pass'] for q in x['documentation_discrepancy_probes'])
families=[]
for f in sorted(list(x['family_pair_status'])+old['families_with_positive_and_negative_probes']):
 new=f in x['family_pair_status'];rows=[r for r in x['rows'] if r['family']==f and r['category']=='paired'] if new else [r for r in x['prior_replays'] if r['family']==f]
 families.append({'family':f,'positive_and_negative_present':True,'passing_paired_cases':len(rows),'fixture_format':'legacy reference XMI (custom JSON manifest)' if new else 'native JSON through prior structural adapter','source_policy_discrepancy_open':f in ['RelComp','WholeOver','RelRig','HomoFunc'],'complete_current_candidate_run':False})
assert len(families)==len(set(r['family'] for r in families))==20
write('coverage-matrix.json',{'scope':'Catalogue-family basic witness coverage; not exhaustive branch/semantic coverage.','catalogue':'https://ontouml.readthedocs.io/en/latest/anti-patterns/index.html','alias_note':'Catalogue MultDep corresponds to archived Java class MultiDepAntipattern.','families':families})
summary={'status':'BASIC_CALIBRATION_COMPLETE_SOURCE_POLICY_REVIEW_REQUIRED','new_families':17,'cumulative_families':20,'catalogue_families':20,'basic_family_coverage_percent':100,'previous_basic_family_coverage_percent':15,'change_percentage_points':85,'new_paired_cases_pass':34,'prior_paired_cases_replayed_pass':8,'boundary_probes':8,'boundary_disagreements_with_literal_documentation':5,'disagreement_rule_families':4,'native_adapter_cases_pass':3,'adapter_rejection_guards_pass':8,'full_candidate_detector_runs':0,'full_candidate_detector_target':20,'scientific_gate_closed':False,'official_archive_modified':False,'baseline_ontology_modified':False,'four_domain_removal_or_transfer_finalized':False,'new_issue':315,'open_issues':30,'closed_issues':170,'closed_this_execution':0,'created_this_execution':1,'historical_major_gates':'2/5 = 40%','historical_g3_packages':'2/7 = 28.6%','limits':['Only basic controlled positive/negative witnesses; no exhaustive correctness claim.','Direct legacy XMI fixtures do not prove modern OntoUML JSON conversion fidelity.','Event/Situation, nature and candidate endpoint/cardinality decisions remain open.','Subsetting/redefinition reference serialization works in toys, not acceptance of 14 actual specialized ends.','SHACL/HermiT ontology tests from the previous immutable package were not rerun because ontology content did not change.']}
write('summary.json',summary)
source_manifest=[]
for f in [r['family'] for r in families]:
 d='GSRig' if f=='GSRig' else f.lower();src=A/'br.ufes.inf.nemo.antipattern/src/br/ufes/inf/nemo/antipattern'/d/(f+'Antipattern.java')
 source_manifest.append({'family':f,'relative_path':str(src.relative_to(A)),'sha256':hashlib.sha256(src.read_bytes()).hexdigest()})
write('official-source-manifest.json',{'repository':'https://github.com/nemo-ufes/ontouml-lightweight-editor','commit':x['archive_commit'],'files':source_manifest,'classes_modified':False,'auxiliary_files':[{'relative_path':str(f.relative_to(A)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in [A/'br.ufes.inf.nemo.antipattern/src/br/ufes/inf/nemo/antipattern/wholeover/WholeOverOccurrence.java',A/'br.ufes.inf.nemo.antipattern/src/br/ufes/inf/nemo/antipattern/overlapping/OverlappingOccurrence.java']]})
write('ci-evidence.json',{'checked_head':'3abb6d2af7579af1b950888a88c8b2e1c03ff8c7','w6_run':37969524157,'job':113952281270,'job_name':'representation-gates','status':'completed','conclusion':'failure','job_steps':[],'root_cause':'NOT EXPOSED by available job-step endpoint','postgresql_pipeline_success_proven':False,'prior_local_contract_tests_retained':True})
print(json.dumps(summary))
