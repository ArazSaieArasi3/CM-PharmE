"""Produce a reproducible checkpoint with every prior task and explicit limits."""
from common import *
import copy,ast,importlib.metadata,owlready2
from datetime import datetime
from zoneinfo import ZoneInfo
def read(n):return json.loads((H/n).read_text())
rr,ndc,rg,tg,fields,repo=[read(n) for n in ['reasoner-results.json','ndc-results.json','regression-results.json','target-results.json','field-audit.json','repository-evidence.json']]
assert (rr['pass'],rr['total'])==(38,38)
assert (ndc['pass'],ndc['total'])==(26,26)
assert (rg['pass'],rg['total'])==(116,116)
assert (tg['reasoner_pass'],tg['reasoner_total'],tg['admission_pass'],tg['admission_total'])==(25,25,27,27)
assert fields['reviewed']==22
for f,meta in [('sources/prov-o-20130430.ttl','sources/prov-source.json'),('sources/ndc-response.json','sources/ndc-source.json')]:
 assert hashlib.sha256((H/f).read_bytes()).hexdigest()==read(meta)['sha256']
native=H.parent/'2.1.0-alpha.1-four-domain-refinement/ontouml-experimental.json'
assert hashlib.sha256(native.read_bytes()).hexdigest()==json.loads((REG/'mapping-audit.json').read_text())['native_source_sha256']
summary={'created_at':datetime.now(ZoneInfo('Asia/Tehran')).isoformat(),'timezone':'Asia/Tehran','prior_head':repo['prior_head'],
 'status':'PROV_TARGET_AND_FIRST_NDC_WITNESSES_TESTED_NOT_ACCEPTED',
 'directional_alignment_axioms':7,'alignment_hermit_pass':38,'alignment_hermit_total':38,
 'raw_direct_hermit_pass':35,'raw_direct_hermit_total':36,'explicit_PROV_adapter_removed_declarations':2,
 'target_scenario_families':7,'target_admission_pass':27,'target_admission_total':27,'target_hermit_pass':25,'target_hermit_total':25,
 'ndc_source_product_rows':5,'ndc_derived_package_records':7,'ndc_abox_triples':227,'ndc_checks_pass':26,'ndc_checks_total':26,
 'old_admission_regression_pass':116,'old_admission_regression_total':116,'old_positive_graphs_combined':45,
 'combined_positive_hermit_consistent':rg['combined_positive_hermit']['consistent'],
 'prior_real_rows':768,'prior_real_triples':39272,'prior_real_nonregression_pass':rg['old_real_sample']['shacl']['conforms'] and rg['old_real_sample']['hermit']['consistent'],
 'prior_real_new_profile_witnesses':0,'previous_profile_fields_reviewed':22,'new_Q_positive_fixture_predicates':18,
 'all_prior_tasks_retained':23,'main_tasks_fully_closed_this_run':0,'bounded_execution_deliverables_completed':3,'bounded_execution_deliverables_total':3,
 'historical_major_gates_closed':2,'historical_major_gates_total':5,'historical_major_gate_percent':40,
 'historical_g3_packages_closed':2,'historical_g3_packages_total':7,'historical_g3_package_percent':28.6,
 'full_candidate_detector_runs':0,'full_candidate_detector_total':20,'C_regression_88_of_89_unresolved':True,
 'native_classes_added':0,'native_relations_added':0,'native_endpoints_changed':0,
 'baseline_ontology_modified':False,'scientific_acceptance':False,'pr':305,'pr_draft':True,
 'four_domain_removal_or_transfer_finalized':False,'open_issues':repo['open_count'],'closed_issues':repo['closed_count'],'issues_closed':0,'issues_created':0,
 'limits':['The raw PROV download fails the selected revision-entailment probe with this OWLAPI/HermiT route. Passing final tests use the explicit two-declaration projection.',
 'No full OWL2 DL profile checker, PROV-CONSTRAINTS, native OntoUML/UFO validity or release readiness is claimed.',
 'Five first-returned API rows are not a representative sample. Seven package records are derived projections of those five rows.',
 'Real NDC coverage excludes establishment-registration, independent approval, ESMP reporting, revision history and actual risk incidents.',
 'Source-qualified target profiles do not materialize world-level causal edges; seven scenarios are fictional.',
 '116/116 admission replay uses asserted graphs and named-class hierarchy, not arbitrary materialized inference graphs; separate C remains 88/89 and unaccepted.',
 'W6 at prior head bdc0a00 still fails with no returned step diagnostics.']}
write('summary.json',summary)
checkpoint=copy.deepcopy(json.loads((REG/'continuation-checkpoint.json').read_text()))
updates={
 'N05':('طرح حداقلی Risk Management و Digital Systems با PROV، سناریو و شاهد NDC تقویت شد؛ چهار دامنه حفظ‌اند','پذیرش طراحی و ارزیابی متوازن هر چهار دامنه؛ تصمیم جایگاه نهایی باز'),
 'N06':('پنج رکورد واقعی NDC به هفت شاهد بسته‌بندی با ردیابی کامل نگاشت شد','نمونهٔ متنوع‌تر، ثبت مؤسسه و شواهد مستقل مجوز؛ مدل کامل محصول باز'),
 'N07':('۲۲ فیلد مثبت قبلی دسته‌بندی شد؛ زمینهٔ اعمال از متادیتای منبع جدا شد','مدل حداقلی زمینهٔ گزارش‌دهی و اعلان واقعی ESMP'),
 'N09':('هفت سناریوی مستقل برای دو والد؛ ۲۷ کنترل شواهد و ۲۵ آزمون منطقی موفق','سناریوهای دیگر دامنه‌ها و شاهد واقعی رخداد/ارزیابی ریسک'),
 'P3':('هفت اصل PROV، تبدیل دو اعلان و گزینه‌های دامنهٔ هدف آمادهٔ داوری است','پذیرش پیشنهادها، C/readOnly، RG-07 و پرونده‌های علمی قبلی'),
 'P4':('نگاشت جهت‌دار هفت‌اصلی PROV با ۳۸ آزمون آماده؛ native دست‌نخورده','پذیرش و انتقال هماهنگ به native/OWL/SHACL؛ پل carrier/claim/fact'),
 'P5d':('گزینهٔ محدودکردن دو والد به SupplyDependency با ضدنمونه رد شد؛ دو جهت child/parent آزموده شد','دامنهٔ هدف و کران جامع؛ ۱۱ نوع، ۶۶ کران و ۱۴ سررابطهٔ تخصصی هنوز باز'),
 'P5c':('تفکیک رکورد/فعالیت در پروفایل PROV آزموده شد؛ قید تکراری در این پیکربندی شناخته شد','اعتبارسنجی جامع Event/Situation و nature؛ پذیرش علمی'),
 'P6a':('۷ سناریوی هدف، ۳۸ آزمون PROV و کنترل‌های مثبت/منفی دادهٔ واقعی آماده','پوشش متوازن کل پروژه؛ ۳۹ عنوان کاری قبلی هنوز پوشش جهانی نیست'),
 'P6b':('تعارض اعلان PROV و استفادهٔ نادرست از helper با شناسهٔ ثابت شناسایی و اصلاح آزمایشی شد؛ شواهد اولیه محفوظ','داوری تبدیل PROV و قرارداد C؛ اصلاح‌های مصوب'),
 'P6c':('دریافت مستقل پنج رکورد واقعی NDC موفق؛ checksum، زمان و JSON pointer ثبت شد','گسترش نمونه، ESMP، قرارداد #307 و علت شکست W6'),
 'P6d':('رگرسیون ۱۱۶/۱۱۶، HermiT ترکیب ۴۵ گراف مثبت و نمونهٔ واقعی قدیم/جدید موفق','پروفایل کامل OWL2 DL/قیود PROV و اعتبارسنجی native و انسانی؛ C جدا باز')}
for task in checkpoint['tasks']:
 if task['id'] in updates:task.update(status='BOUNDED_EVIDENCE_READY_NOT_ACCEPTED',current_extension=updates[task['id']][0],remaining_fa=updates[task['id']][1])
assert len(checkpoint['tasks'])==23
checkpoint.update(title='CM-PharmE v2.1 — directional PROV, target scenarios and first live NDC witnesses',previous_checkpoint='../2.1.0-alpha.1-registry-policy-lab/continuation-checkpoint.json',prior_development_head=repo['prior_head'],summary=summary)
checkpoint['source_review_update']={'sources':['pinned W3C PROV-O 20130430 Turtle','OWL2 structural specification 5.8.1','ICH Q9(R1) 2025 corrected document','FDA NDC Directory','openFDA NDC API five-row snapshot'],'new_empirical_records':5,'derived_package_records':7,'author_acceptance':False,'raw_PROV_dual_declaration_conflicts':2}
checkpoint['next_steps_in_order']=[
 'Build and test a minimum contextual reporting-applicability model and the record/claim/fact bridge, using the completed 22-field triage; keep metadata out of unnecessary native domain classes.',
 'Expand NDC sampling by explicit source strata and acquire a versioned real ESMP reporting action; retain package/product dates, source attribution and unknown approval separately.',
 'Prepare author adjudication of the seven PROV alignment axioms, two-declaration reasoning projection, target-policy alternatives, RG-07 and prior C/evidence contract. No generic continuation instruction counts as approval.',
 'After acceptance, integrate native/OWL/SHACL deltas, resolve the 11 untyped ends, 66 unknown cardinalities, 14 specialized ends, four isolates and four #315 discrepancies; run all 20 detectors on a supported full candidate.',
 'Resolve W6 and #307; complete all-domain requirements/ownership, independent evaluation and human G3 review; then align article/Wiki/Pages and stable diagrams and audit release.']
write('continuation-checkpoint.json',checkpoint)
lines=['# وضعیت کامل CM-PharmE v2.1 — ادامه از bdc0a00','',
 'در G3 هستیم. این اجرا نگاشت PROV، سناریوهای دو والد و اولین شاهد واقعی NDC را جلو برد. هیچ‌یک از ۲۳ کار اصلی هنوز کاملاً بسته نشده است. PR305 پیش‌نویس است؛ خروج/انتقال چهار دامنه همچنان معلق است.','',
 '| شناسه | کار | انجام‌شده / وضعیت | باقی‌مانده |','|---|---|---|---|']
for t in checkpoint['tasks']:lines.append('| '+t['id']+' | '+t['task_fa']+' | '+t.get('current_extension','پیش‌نویس یا کار قبلی محفوظ؛ پذیرش باز')+' | '+t.get('remaining_fa',t['deliverable_fa'])+' |')
lines += ['', '## درصدهای با مخرج مشخص','',
 '| شاخص | پیش از اجرا | اکنون | تغییر |','|---|---:|---:|---:|',
 '| سه خروجی اجرایی همین نوبت: PROV، دو والد، اولین NDC | ۰/۳ | ۳/۳ = ۱۰۰٪ | +۱۰۰ واحد درصد در همین بسته |',
 '| بررسی اولیهٔ فیلدهای مثبت قبلی | ۰/۲۲ | ۲۲/۲۲ = ۱۰۰٪ | +۱۰۰ واحد درصد؛ بدون پذیرش علمی |',
 '| دروازه‌های اصلی تاریخی | ۲/۵ = ۴۰٪ | ۲/۵ = ۴۰٪ | صفر |',
 '| بسته‌های اصلی G3 | ۲/۷ = ۲۸٫۶٪ | ۲/۷ = ۲۸٫۶٪ | صفر |',
 '| اجرای معتبر ۲۰ آشکارساز روی کل candidate | ۰/۲۰ | ۰/۲۰ | صفر |','',
 'عدد ۱۰۰٪ مربوط به خروجی محدود همین اجراست، نه کل انتالوژی یا مقاله. درصد کلی وزنی پروژه تعریف و تصویب نشده؛ عددی برای آن ساخته نشده است.','',
 '## تمام ایشوهای باز','',f"{repo['open_count']} باز و {repo['closed_count']} بسته؛ در این اجرا صفر ایجاد و صفر بسته شد.",'', '| ایشو | عنوان |','|---|---|']
lines += ['| [#'+str(x['number'])+']('+x['url']+') | '+x['title']+' |' for x in repo['open_issues']]
lines+=['','## گام بعدی','',*['- '+s for s in checkpoint['next_steps_in_order']], '',
 'W6 در head مبنای bdc0a00: run 37984390144 و job 114002601320، شکست با steps خالی و logs_url تهی. علت قطعی مشخص نشده؛ موفقیت محلی جایگزین CI نیست.']
(H/'work-status-fa.md').write_text('\n'.join(lines)+'\n')
runtime={'python_packages':{x:importlib.metadata.version(x) for x in ['rdflib','pyshacl','owlready2']},'java_version':subprocess.run(['java','-version'],capture_output=True,text=True).stderr.strip(),'hermit_classpath':_HERMIT_CLASSPATH if '_HERMIT_CLASSPATH' in globals() else 'owlready2.reasoning._HERMIT_CLASSPATH','test_scripts':['run_reasoner.py','run_targets.py','run_ndc.py','run_regression.py','audit_fields.py']}
runtime['hermit_jar_sha256']=hashlib.sha256((Path(owlready2.__file__).parent/'hermit/HermiT.jar').read_bytes()).hexdigest()
runtime['whitespace_preservation_exceptions']={'sources/prov-o-20130430.ttl':'Exact vendor byte snapshot, including literal whitespace and final blank line. SHA256 enforced.','prov-reasoning-projection.ttl':'Preserves vendor annotation literal values, including trailing whitespace inside multiline literals; only the two declared adapter triples differ.'}
write('runtime.json',runtime)
for f in H.glob('*.py'):ast.parse(f.read_text())
manifest={str(p.relative_to(H)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(H.rglob('*')) if p.is_file() and p.name!='file-manifest.json' and '__pycache__' not in p.parts}
write('file-manifest.json',{'algorithm':'sha256','files':manifest,'count':len(manifest),'self_excluded':True})
print(json.dumps({'summary':summary,'manifest_files':len(manifest)},ensure_ascii=False),flush=True)
