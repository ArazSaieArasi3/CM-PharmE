"""Trace evidence, preserve all 23 work items and keep acceptance gates open."""
import ast,copy,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent
PREV=H.parent/'2.1.0-alpha.1-derived-participant-lab'
def read(p):return json.loads((H/p).read_text())
def write(p,d):(H/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
requirements=read('reconciled-requirements.json');shacl=read('shacl-results.json');queries=read('query-results.json');reasoner=read('reasoner-results.json');regress=read('prior-regression-results.json');real=read('real-regression.json');mapping=read('mapping-audit.json');repo=read('repository-evidence.json')
assert (shacl['pass'],shacl['total'])==(27,27)
assert (queries['pass'],queries['total'])==(38,38)
assert (reasoner['pass'],reasoner['total'])==(13,13)
assert (regress['pass'],regress['total'])==(89,89)
assert real['pass'] and real['new_profile_witnesses']==0
assert requirements['working_heading_count']==39 and requirements['input_rows']==40
assert hashlib.sha256((H.parent/'2.1.0-alpha.1-four-domain-refinement/ontouml-experimental.json').read_bytes()).hexdigest()==mapping['native_source_sha256']
trace=[]
for r in requirements['requirements']:
 s=[x for x in shacl['cases'] if r['id'] in x['requirements']]
 q=[x for x in queries['cases'] if r['id'] in x['requirements']]
 o=[x for x in reasoner['cases'] if r['id'] in x['requirements']]
 polarities={x['polarity'] for x in s+q};assert {'positive','negative'}<=polarities,r['id']
 trace.append({'requirement_id':r['id'],'canonical_requirement_id':r['canonical_requirement_id'],'source_id':r['source_id'],
  'candidate_existing_ids':r['candidate_existing_ids'],'desk_decision':r['desk_decision'],
  'shacl_cases':[x['name'] for x in s],'query_cases':[x['name'] for x in q],'reasoner_cases':[x['name'] for x in o],
  'positive_and_negative_witnesses':True,'bounded_expectations_pass':all(x['pass'] for x in s+q+o),
  'full_requirement_satisfaction_proven':False,'native_implementation_complete':False,'scientific_acceptance':False,
  'remaining_mapping_gap':r['mapping_gap']})
write('traceability.json',{'requirements':trace,'bounded_rows_covered':16,'total_batch_rows':16,'all_project_coverage_claim':False})
summary={
 'date':'2026-10-09','timezone':'Asia/Tehran','prior_head':repo['prior_head'],
 'status':'BOUNDED_REGISTRY_POLICY_PROTOTYPES_TESTED_NOT_ACCEPTED',
 'source_batch_reconciled':16,'source_batch_total':16,'desk_reconciliation_previous_percent':0,'desk_reconciliation_percent':100,
 'input_requirement_rows':40,'working_requirement_headings':39,'refined_existing_headings':1,'retained_new_headings':15,
 'global_requirement_completeness_known':False,'accepted_requirement_count':0,
 'bounded_batch_rows_with_positive_negative_evidence':16,'bounded_batch_evidence_previous_percent':0,'bounded_batch_evidence_percent':100,
 'new_shacl_pass':27,'new_shacl_total':27,'query_pass':38,'query_total':38,
 'hermit_synthetic_pass':13,'hermit_synthetic_total':13,'hermit_with_prior_real_sample_pass':14,'hermit_with_prior_real_sample_total':14,
 'prior_shacl_replay_pass':89,'prior_shacl_replay_total':89,
 'prior_C_expectations_preserved':88,'prior_C_expectations_total':89,'prior_C_contract_change_accepted':False,'C_materialization_applied_in_this_package':False,
 'prior_real_sample_rows':768,'prior_real_sample_triples':real['triples'],'prior_real_sample_nonregression_pass':real['pass'],'new_profile_empirical_witnesses':0,'new_NDC_records_retrieved':0,
 'new_native_classes':0,'new_native_relations':0,'existing_native_relations_reused':13,'experimental_profile_fields_used':22,'external_PROV_predicates_used':4,'new_disjointness_proposals':2,
 'positive_graphs_audited':45,'broad_parents_audited':3,'broad_parents_with_observed_links':1,'observation_subproperty_witness_links':6144,
 'historical_major_gates_closed':2,'historical_major_gates_total':5,'historical_major_gate_percent':40,
 'historical_g3_packages_closed':2,'historical_g3_packages_total':7,'historical_g3_package_percent':28.6,
 'full_candidate_detector_runs':0,'full_candidate_detector_total':20,'scientifically_accepted_specialized_ends':0,'specialized_ends_total':14,
 'all_prior_tasks_retained':23,'open_issues':repo['open_count'],'closed_issues':repo['closed_count'],'issues_created':0,'issues_closed':0,
 'baseline_ontology_modified':False,'scientific_acceptance':False,'pr':305,'pr_draft':True,'four_domain_removal_or_transfer_finalized':False,
 'limits':['39 headings cover only the two reconciled input lists; all-domain extraction is unfinished.',
 'Profile/query controls are synthetic prototypes, not a complete legal compliance or product-approval model.',
 'Native scope is unchanged; four previous isolates and full Event/Situation/nature semantics remain open.',
 'PROV predicates are used without a formal import/alignment; closeMatch is not class equivalence.',
 '89/89 current regression does not resolve the separate unaccepted 88/89 C contract transition.',
 'The old real sample has zero new profile witnesses; its passing result is nonregression only.',
 'W6 prior-head failure still returns no step diagnostics.']}
write('summary.json',summary)
previous=json.loads((PREV/'continuation-checkpoint.json').read_text());checkpoint=copy.deepcopy(previous)
updates={
 'N02':('۱۶/۱۶ بند تطبیق داده شد؛ ۴۰ ردیف ورودی به ۳۹ عنوان کاری ردیابی شد','استخراج همهٔ دامنه‌ها و پذیرش علمی؛ ۳۹ عنوان صرفاً محدودهٔ این دو ورودی است'),
 'N05':('چهار دامنه حفظ شدند؛ شواهد منشأ و تفکیک ادعا/وضعیت تقویت شد','پذیرش طراحی حداقلی و تصمیم جایگاه نهایی چهار دامنه'),
 'N06':('هشت بند رجیستری، شاهدهای مثبت/منفی و اصلاح خودگزارشی سازمان آماده','دادهٔ واقعی جدید و نگاشت کامل؛ مدل کامل مجوز محصول هنوز باز'),
 'N07':('چهار بند گزارش‌دهی با نقش، سناریو، مسیر، موضوع و زمان آزموده شد','مدل مفهومی زمینهٔ اعمال و منبع واقعی اعلان؛ پذیرش علمی'),
 'N09':('برای هر ۱۶ بند بسته شاهد مثبت و منفی وجود دارد؛ ۳۸ پاسخ بررسی شد','سناریوهای مستقل سایر دامنه‌ها، خصوصاً دو والد بدون شاهد'),
 'P3':('دو قید هویت و اصلاح RG-07 برای داوری آماده است؛ تصمیم C محفوظ','پذیرش قیدها، C/readOnly و پرونده‌های علمی قبلی'),
 'P4':('۱۳ رابطهٔ موجود بازاستفاده شد؛ ۲۲ فیلد آزمایشی و چهار PROV تفکیک شدند','نگاشت رسمی جهت‌دار PROV و انتقال فقط مصوبات به native/OWL/SHACL'),
 'P5d':('سه والد در ۴۵ گراف مثبت و نمونهٔ واقعی ممیزی شد؛ ۶۱۴۴ پیوند مشاهده','دو والد بی‌شاهد؛ تعیین دامنه/کران کامل و ۱۱ نوع/۶۶ کران نامشخص قبلی'),
 'P5c':('دو برخورد هویت در OWL قبلی بازتولید و با قید پیشنهادی مهار شد','پذیرش علمی و اعتبارسنجی جامع Event/Situation/nature'),
 'P6a':('پنج پروفایل با ۲۷ SHACL و ۳۸ پاسخ آزموده شد','پوشش متوازن همهٔ نیازهای پروژه'),
 'P6b':('دو نقص fixture ناشی از mandate مفقود اصلاح شد؛ شکست اولیه محفوظ','داوری تغییر قرارداد C همچنان ۸۸/۸۹؛ اصلاح‌ها پس از پذیرش'),
 'P6c':('نمونهٔ واقعی قبلی ۷۶۸ ردیفی عدم پسرفت را گذراند؛ شاهد جدید صفر','دریافت دادهٔ مستقل NDC/ESMP؛ رفع شکست W6 با steps خالی'),
 'P6d':('۱۳ HermiT مصنوعی + یک واقعی موفق؛ رگرسیون این بسته ۸۹/۸۹','اعتبارسنجی یکپارچه پس از ادغام؛ نتیجهٔ C جدا و باز باقی است')}
checkpoint.update(title='CM-PharmE v2.1 — reconciled requirements and registry-policy witnesses',
 previous_checkpoint='../2.1.0-alpha.1-derived-participant-lab/continuation-checkpoint.json',prior_development_head=repo['prior_head'],summary=summary)
for task in checkpoint['tasks']:
 if task['id'] in updates:
  task.update(status='BOUNDED_EVIDENCE_READY_NOT_ACCEPTED',current_extension=updates[task['id']][0],remaining_fa=updates[task['id']][1])
assert len(checkpoint['tasks'])==23
checkpoint['source_review_update']={'sources':['FDA eDRLS','FDA NDC Directory','EMA ESMP','PROV-O 2013','SKOS 2009','openFDA NDC overview'],
 'reconciled_batch_rows':16,'author_acceptance':False,'new_empirical_API_retrieval':'Not accessible; zero new records',
 'new_reproduced_gaps':['SourceRecord/ProvenanceActivity collision allowed by baseline OWL','Assertion/MedicineShortageSituation collision allowed by baseline OWL','closeMatch does not entail PROV class membership']}
checkpoint['next_steps_in_order']=[
 'Prepare and test a pinned, directional PROV alignment without treating closeMatch as equivalence; inspect the 22 profile fields for minimum necessary conceptual mapping.',
 'Write independent target-universe scenarios for disruptionAffects and riskAssessmentConcerns; use the observed Product/Presentation paths without freezing an exhaustive union from one dataset.',
 'Adjudicate the two proposed identity disjointness axioms, refined RG-07 and the separate C/readOnly/evidence-contract decision; author acceptance remains open.',
 'Acquire real registry/reporting source records with release/version provenance; do not count the old 768-row nonregression sample as validation of these profiles.',
 'Resolve #315 and W6, then integrate accepted deltas and execute complete validation plus human review.',
 'Complete all-domain requirements and ownership, freeze tested scope, align article/Wiki/Pages and stable diagrams, then perform release audit.']
write('continuation-checkpoint.json',checkpoint)
tasklines=[]
for line in (PREV/'work-status-fa.md').read_text().splitlines():
 if line.startswith('| ') and line.split('|')[1].strip() in {t['id'] for t in checkpoint['tasks']}:
  cells=[x.strip() for x in line.split('|')[1:-1]]
  if cells[0] in updates:cells[2],cells[3]=updates[cells[0]]
  tasklines.append('| '+' | '.join(cells)+' |')
assert len(tasklines)==23
lines=['# وضعیت کامل CM-PharmE v2.1 — ادامه از a83471c',
 'در G3 هستیم. بستهٔ نیازمندی و آزمون رجیستری/گزارش‌دهی آماده شد؛ پذیرش علمی، ادغام و مرور انسانی بازند. PR305 پیش‌نویس است؛ خروج/انتقال چهار دامنه نهایی نشده است.',
 '| شناسه | کار | انجام‌شده / وضعیت | باقی‌مانده |','|---|---|---|---|',*tasklines,'',
 'تمام ۲۳ کار اصلی هنوز بخش باقی‌مانده دارند. تکمیل آزمایش‌های این اجرا، بستن کل بند یا پذیرش علمی نیست.','',
 '## درصدهای محدود و قابل ممیزی','',
 '| شاخص | قبل | اکنون | تغییر |','|---|---:|---:|---:|',
 '| تطبیق و تصمیم کارشناسی اولیه برای بستهٔ ۱۶بندی | ۰/۱۶ = ۰٪ | ۱۶/۱۶ = ۱۰۰٪ | +۱۰۰ واحد درصد |',
 '| پوشش مثبت/منفی اجراییِ همین ۱۶ بند | ۰/۱۶ = ۰٪ | ۱۶/۱۶ = ۱۰۰٪ | +۱۰۰ واحد درصد |',
 '| دروازه‌های اصلی تاریخی بسته | ۲/۵ = ۴۰٪ | ۲/۵ = ۴۰٪ | صفر |',
 '| بسته‌های اصلی G3 بسته | ۲/۷ = ۲۸٫۶٪ | ۲/۷ = ۲۸٫۶٪ | صفر |',
 '| اجرای معتبر آشکارساز روی کل candidate | ۰/۲۰ | ۰/۲۰ | صفر |','',
 '۳۹ عنوان کاری از ۴۰ ردیف ورودی، معیار پوشش جهانی نیست. دادهٔ جدید مصنوعی است. ۸۹/۸۹ رگرسیون این بسته، نتیجهٔ مستقل C با ۸۸/۸۹ را تغییر نمی‌دهد.','',
 '## تمام ایشوهای باز','',f"{repo['open_count']} باز و {repo['closed_count']} بسته؛ در این اجرا صفر ایجاد و صفر بسته شد.",'',
 '| ایشو | عنوان | وضعیت |','|---|---|---|']
for issue in repo['open_issues']:lines.append(f"| [#{issue['number']}]({issue['url']}) | {issue['title']} | باز |")
lines+=['','## گام بعدی دقیق','',
 'نگاشت جهت‌دار و پین‌شدهٔ PROV و سناریوهای مستقل دو والد بی‌شاهد را آماده و آزمایش کنیم. هم‌زمان، دو قید هویت جدید، اصلاح خودگزارشی RG-07 و تغییر قرارداد C برای داوری علمی آماده‌اند.',
 'پس از آن: ادغام مصوبات، دادهٔ واقعی جدید و اعتبارسنجی جامع. W6 در head مبنا a83471c، run 37979023406 و job 113984503975 شکست خورده و steps خالی است؛ علت قطعی تعیین نشده است.','',
 'موفقیت نمونهٔ واقعی قبلی: ۷۶۸ ردیف، ۳۹۲۷۲ سه‌تایی، SHACL و HermiT موفق؛ شاهد پروفایل جدید صفر. این نتیجه صرفاً عدم پسرفت است.']
(H/'work-status-fa.md').write_text('\n\n'.join(lines[:2])+'\n\n'+'\n'.join(lines[2:])+'\n')
for f in H.rglob('*.ttl'):f.write_text(f.read_text().rstrip()+'\n')
for f in H.glob('*.py'):ast.parse(f.read_text())
for f in H.rglob('*.json'):json.loads(f.read_text())
files=[{'path':str(f.relative_to(H)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(H.rglob('*')) if f.is_file() and f.name!='file-manifest.json']
write('file-manifest.json',{'scope':'All package files except this manifest','files':files})
print(json.dumps({'files':len(files)+1,'tasks':23,'batch_rows_with_bounded_positive_negative_evidence':len(trace),'working_headings':39,'gate_acceptances':0}))
