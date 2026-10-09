"""Build a truthful continuation checkpoint without promoting experimental gates."""
import copy,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent
# RDFLib emits an extra final blank line; normalize only package artifacts.
for f in H.rglob('*.ttl'):f.write_text(f.read_text().rstrip()+'\n')
def read(name):return json.loads((H/name).read_text())
def write(name,d):(H/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
prior=read('../2.1.0-alpha.1-native-fidelity-audit/continuation-checkpoint.json')
repo=read('repository-evidence.json');native=read('native-alternatives.json');legacy=read('legacy-results.json')
shacl=read('shacl-results.json');reg=read('prior-regression-results.json');reasoner=read('reasoner-results.json');temporal=read('temporal-results.json');req=read('source-requirements.json')
assert len(prior['tasks'])==23
assert (shacl['pass'],shacl['total'])==(24,24)
assert (reg['baseline_pass'],reg['pass'],reg['total'])==(89,88,89)
assert reg['known_contract_change_characterized'] and not reg['contract_change_accepted']
assert (reasoner['pass'],reasoner['total'])==(12,12)
assert (legacy['ocl_pass'],legacy['relspec_pass'])==(9,12)
assert (temporal['pass'],temporal['total'])==(10,10)
assert len(req['requirements'])==16 and sum(bool(x['related_prior_requirement_ids']) for x in req['requirements'])==8
assert native['source_sha256']==hashlib.sha256((H.parent/'2.1.0-alpha.1-four-domain-refinement/ontouml-experimental.json').read_bytes()).hexdigest()
summary={
 'date':'2026-10-09','timezone':'Asia/Tehran','prior_head':repo['prior_head'],
 'status':'ALTERNATIVES_COMPARED_ONE_UNACCEPTED_REGRESSION_CONTRACT_CHANGE',
 'native_schema_parser_variants_pass':3,'native_schema_parser_variants_total':3,
 'bounded_subsetting_comparisons_pass':18,'bounded_subsetting_comparisons_total':18,
 'specialized_ends_with_executable_C_proposal':6,'specialized_ends_total':14,
 'C_proposal_end_coverage_previous_percent':0,'C_proposal_end_coverage_percent':round(600/14,1),
 'scientifically_accepted_specialized_ends':0,
 'official_ocl_expected_observations_pass':9,'official_ocl_fragment_runs':9,
 'official_ocl_rules_selected':3,'official_complete_validator_run':False,
 'relspec_expected_observations_pass':12,'relspec_runs':12,'zero_relspec_malformed_native_controls':6,
 'new_shacl_pass':24,'new_shacl_total':24,'original_baseline_replay_pass':89,
 'C_prior_expectations_preserved':88,'C_prior_expectations_total':89,
 'regression_gate':reg['regression_gate'],'known_contract_change_accepted':False,
 'hermit_pass':12,'hermit_total':12,'temporal_pass':10,'temporal_total':10,
 'source_requirement_proposals':16,'primary_requirement_sources':4,'requirements_partial_overlap_rows':8,
 'prior_requirement_rows':24,'unique_project_requirement_total':None,'new_requirements_accepted':0,
 'historical_major_gates_closed':2,'historical_major_gates_total':5,'historical_major_gate_percent':40,
 'historical_g3_packages_closed':2,'historical_g3_packages_total':7,'historical_g3_package_percent':28.6,
 'full_candidate_detector_runs':0,'full_candidate_detector_total':20,'prior_source_policy_differences_open':4,
 'open_issues':repo['open_count'],'closed_issues':repo['closed_count'],'issues_created':0,'issues_closed':0,
 'new_native_classes':0,'new_native_relations':0,'original_ontology_files_modified':False,
 'four_domain_removal_or_transfer_finalized':False,'scientific_acceptance':False,'pr_draft':True,
 'limits':['Three selected OCL rules and structural fragments do not validate all modern nature or Event/Situation semantics.',
 'C uses explicitly typed roles and named subclass paths, not complete OWL inference.',
 'C OWL delta does not encode the full operational projection or temporal immutability.',
 'One old negative becomes positive under C; original expectation and failure are preserved.',
 'Requirement proposals are source-based designs, not accepted or fully implemented requirements.',
 'W6 prior-head failure still has no returned step diagnostics; no CI/database success claimed.']}
write('summary.json',summary)
changes={
 'N02':('۲۴ بند قبلی محفوظ؛ ۱۶ پیشنهاد مستقل جدید، چهار منبع و هشت هم‌پوشانی مشخص','رفع هم‌پوشانی، تکمیل همهٔ دامنه‌ها و آزمون/پذیرش نیازهای ضروری'),
 'N06':('مرز پیشنهادی رکورد/واقعیت/مجوز و هشت بند رجیستری آماده','داوری مرز، نگاشت کامل و شاهد مستقل؛ product approval در مدل موجود حل نشده'),
 'N07':('چهار بند محدود ESMP برای نقش/سناریو، بالقوه/واقعی، موضوع و تناوب آماده','تعیین زمینهٔ اعمال، نسخه و زمان؛ آزمون اجرایی اختصاصی و پذیرش'),
 'P3':('سه گزینه برای سه رابطه مقایسه شد؛ C ترجیح آزمایشی دارد','پذیرش stereotype، readOnly و قرارداد شاهد؛ ۳۹ کارت و پرونده‌های قبلی محفوظ'),
 'P4':('سه OWL delta و سه SHACL profile آزمایشی، با تعریف materialization آماده','ادغام فقط مصوبات؛ دو aboutness و هم‌ترازی کامل همچنان باز'),
 'P5d':('برای شش سر از ۱۴، پیشنهاد اجرایی C و کنترل محدود موفق آماده شد','پذیرش صفر از ۱۴؛ ۱۱ نوع، ۶۶ کران مبنا و سه والد گسترده هنوز تعیین‌تکلیف نشده'),
 'P5c':('ده شاهد هویت زمانی اجرا شد؛ حفظ native قبلی برقرار','هویت کامل Event/Situation و اعتبار معنایی nature؛ پذیرش مسیر ترکیبی'),
 'P5e':('۱۲ آزمایش RelSpec؛ شش mutation بدشکل با خروجی صفر شناسایی شد','چهار اختلاف #315 و اجرای معتبر کل candidate همچنان ۰/۲۰'),
 'P6a':('۲۴ شاهد SHACL جدید، ۱۲ ریزنر و ده trace محدود آماده','پوشش متوازن نیازمندی‌ها و مفاهیم کل پروژه'),
 'P6b':('تغییر نتیجهٔ یک رگرسیون تشخیص و با سه شاهد توضیح داده شد؛ شکست اولیه محفوظ','قرارداد شاهد باید داوری شود؛ رگرسیون C هنوز ۸۸/۸۹'),
 'P6c':('شواهد پیشین ۷۶۸ ردیف محفوظ؛ W6 در head مبنا دوباره بررسی شد','W6 شکست با steps خالی؛ دادهٔ مستقل برای پروفایل‌های جدید و سایر منابع لازم'),
 'P6d':('۱۲/۱۲ HermiT؛ قرارداد قبلی ۸۹/۸۹، پس از C فقط ۸۸/۸۹','اعتبارسنجی یکپارچه پس از پذیرش و رفع اختلاف قرارداد')
}
checkpoint=copy.deepcopy(prior)
checkpoint.update(title='CM-PharmE v2.1 — participant alternatives, temporal probes and independent requirements',
 previous_checkpoint='../2.1.0-alpha.1-native-fidelity-audit/continuation-checkpoint.json',
 prior_development_head=repo['prior_head'],summary=summary)
for task in checkpoint['tasks']:
 if task['id'] in changes:
  done,left=changes[task['id']];task.update(status='EXPERIMENTAL_PROGRESS_NOT_ACCEPTED',current_extension=done,remaining_fa=left)
checkpoint['next_steps_in_order']=[
 'Adjudicate C derived associations, role-typing policy, primitive mediation readOnly, and the documented-partnership contract transition using decision-report-fa.md.',
 'Deduplicate the 16 source-based proposals against the prior 24; implement independent positive/negative witnesses for selected registry/regulatory/provenance requirements.',
 'Resolve three broad parent relation target/cardinality policies and the remaining four specialization relations without inventing an Entity supertype only for conversion.',
 'Adjudicate four #315 source-profile differences and establish faithful Event/Situation/nature validation; full-candidate 20-detector run remains blocked.',
 'Obtain actionable W6 diagnostics and a successful database pipeline; maintain empirical/source-contract limits.',
 'Integrate accepted changes, validate all representations, complete human review, then align article/Wiki/Pages, stable diagram and release.']
checkpoint['source_review_update']={'primary_sources':['FDA DRLS','FDA NDC Directory','EMA ESMP','W3C PROV-O','Guizzardi & Zamborlini SLE2012 PDF','pinned RefOntoUML Ecore'],
 'author_acceptance':False,'new_source_profile_mismatch':'Previous optional mediation proposal conflicts with three selected pinned archival constraints.',
 'prior_detector_source_disagreements':4}
write('continuation-checkpoint.json',checkpoint)
old=(H.parent/'2.1.0-alpha.1-native-fidelity-audit/work-status-fa.md').read_text()
tasklines=[]
for line in old.splitlines():
 if line.startswith('| ') and line.split('|')[1].strip() in {t['id'] for t in prior['tasks']}:
  cells=[x.strip() for x in line.split('|')[1:-1]]
  if cells[0] in changes:cells[2],cells[3]=changes[cells[0]]
  tasklines.append('| '+' | '.join(cells)+' |')
assert len(tasklines)==23
lines=['# وضعیت کامل CM-PharmE v2.1 — ادامه از 34d23eb',
 'در G3 هستیم؛ مقایسهٔ گزینه‌ها و آزمون‌های محدود انجام شده، پذیرش علمی و ادغام نهایی باز است. PR305 پیش‌نویس است و تصمیم خروج/انتقال چهار دامنه نهایی نشده است.',
 '| شناسه | کار | انجام‌شده / وضعیت | باقی‌مانده |','|---|---|---|---|',*tasklines,'',
 'تمام ۲۳ بند هنوز بخشی انجام‌نشده دارند؛ تکمیل یک آزمایش معادل بستن بند نیست.','',
 '## پیشرفت با مخرج مشخص','',
 '| شاخص | قبل | اکنون | تفسیر |','|---|---:|---:|---|',
 '| سررابطهٔ دارای پیشنهاد اجرایی C در این بسته | ۰/۱۴ | ۶/۱۴ = ۴۲٫۹٪ | افزایش ۴۲٫۹ واحد درصد در این شاخص محدود؛ پذیرش علمی صفر است |',
 '| گزینه‌های برنامه‌ریزی‌شدهٔ همین مقایسه که اجرا شدند | ۰/۳ | ۳/۳ = ۱۰۰٪ | مقایسه تمام؛ تصمیم نهایی باز |',
 '| انتظارهای قبلی حفظ‌شده پس از C | — | ۸۸/۸۹ = ۹۸٫۹٪ | یک تغییر قرارداد؛ gate رگرسیون بسته نشده |',
 '| دروازه‌های اصلی تاریخی بسته | ۲/۵ = ۴۰٪ | ۲/۵ = ۴۰٪ | بدون تغییر |',
 '| بسته‌های اصلی G3 بسته | ۲/۷ = ۲۸٫۶٪ | ۲/۷ = ۲۸٫۶٪ | بدون تغییر |',
 '| آشکارساز اجراشدهٔ معتبر روی کل candidate | ۰/۲۰ | ۰/۲۰ | مانع‌های fidelity/semantics باقی است |','',
 'این درصدها مستقل‌اند و درصد کیفیت علمی کل پروژه نیستند. نیازمندی‌های مستقل: ۱۶ پیشنهاد جدید، هشت هم‌پوشانی؛ تعداد یکتای کل هنوز معلوم نیست. هیچ درصد ساختگی برای کل نیازمندی‌ها محاسبه نشده است.','',
 '## تمام ایشوهای باز','',f"{repo['open_count']} باز، {repo['closed_count']} بسته؛ در این اجرا صفر ایجاد و صفر بسته شد.",'',
 '| ایشو | عنوان | وضعیت |','|---|---|---|']
for i in repo['open_issues']:lines.append(f"| [#{i['number']}]({i['url']}) | {i['title']} | باز |")
lines+=['','## گام بعد','',
 'داوری پیشنهاد C، readOnly والدها و تغییر قرارداد شاهد، سپس ادغام مصوبات در candidate جدید. کار مستقلِ قابل ادامه: رفع هم‌پوشانی ۱۶ نیاز پیشنهادی و ساخت شاهدهای رجیستری/سیاست مقرراتی، همراه با تعیین سه والد گسترده و مسیر Event/Situation.',
 'W6 در head مبنا 34d23eb با run 37974371243 و job 113968787703 شکست خورده و steps خالی است. ۲۲ اجرای ثبت‌شدهٔ همان head شکست دارند؛ علت قطعی مشخص نشده است. موفقیت CI یا PostgreSQL گزارش نمی‌شود.']
(H/'work-status-fa.md').write_text('\n\n'.join(lines[:2])+'\n\n'+'\n'.join(lines[2:])+'\n')
files=[]
for f in sorted(H.rglob('*')):
 if f.is_file() and f.name!='file-manifest.json':files.append({'path':str(f.relative_to(H)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
write('file-manifest.json',{'scope':'All package files except this self-referential manifest','files':files})
print(json.dumps({'files':len(files)+1,'tasks':23,'open_issues':repo['open_count'],'regression_gate':reg['regression_gate'],'proposals_accepted':0}))
