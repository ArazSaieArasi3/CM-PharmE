"""Generate traceability, the continuation checkpoint and reports from results."""
from lab import *
from datetime import timezone
from zoneinfo import ZoneInfo
import platform,importlib.metadata,subprocess
def read(f):return json.loads((H/f).read_text())
t,n,e,r=map(read,['test-results.json','ndc-results.json','esmp-results.json','regression-results.json'])
assert all(t[k]==t[k.replace('_pass','_total')] for k in ['query_pass','shacl_pass','hermit_pass'])
assert all(d['pass']==d['total'] for d in [n,e,r])
assert n['claim_origin_counts']=={'source-extracted':74,'mapping-interpretation':76}
assert r['new_data_with_combined_historical_and_new_shapes']['conforms']
native=H.parent/'2.1.0-alpha.1-four-domain-refinement/ontouml-experimental.json'
native_sha=hashlib.sha256(native.read_bytes()).hexdigest()
assert native_sha=='fef3295149278bdf5a9c446f9699582a565d26fa2f52f76d90f593ba00e20989'
now=datetime.now(ZoneInfo('Asia/Tehran')).isoformat()
reqs=[
 ('CL-01','Separate information carrier, structured claim and context/specification descriptions',['B2-RG-07']),
 ('CL-02','Represent claim content without materializing its described world-level statement',['B2-RG-03','B2-RP-02']),
 ('CL-03','Preserve source denial and conflicting source claims without global truth negation',['B2-RG-07']),
 ('CL-04','Do not turn missing slice evidence into world-level falsity',['B2-RG-05']),
 ('CL-05','Distinguish source field extraction from proposed ontology interpretation',['B2-RG-04','B2-RG-07']),
 ('CTX-01','Qualify context by actor role and declared portfolio',['B2-RP-01']),
 ('CTX-02','Keep jurisdiction, product/presentation and marketing country coherent',['B2-RP-03']),
 ('CTX-03','Select scenario and authorisation-route tokens explicitly',['B2-RP-01','B2-RP-03']),
 ('CTX-04','Require action-specific evidence for non-routine action matching',['B2-RP-03']),
 ('CTX-05','Distinguish complete from incomplete product scope',['B2-RP-03']),
 ('CTX-06','Bind evaluation to a rule version/time and expose action-specific frequency',['B2-RP-04']),
 ('CTX-07','Keep marketing prerequisites specific to submission flow',['B2-RP-03']),
 ('CTX-08','Return bounded match/unknown/error without certifying legal compliance or readiness',['B2-RP-01','B2-RP-02'])]
trace=[]
for id,statement,prior in reqs:
 cases=[{'kind':kind,'test':x['name'],'pass':x['pass']} for kind,key in [('query','queries'),('admission','shacl'),('reasoner','hermit')] for x in t[key] if x['requirement']==id]
 assert cases
 trace.append({'id':id,'statement':statement,'related_prior_ids':prior,'mapping':'PARTIAL_REFINEMENT_NOT_REPLACEMENT','origin':'DESIGN_PROPOSAL_WITH_SOURCE_LINKS','tests':cases,'source_extractions':[x['id'] for x in read('source-evidence.json')['extractions'] if id in x['requirements']],'accepted':False})
write('requirements-traceability.json',{'status':'13 local refinements, not 13 additional globally independent requirements','requirements':trace,'limits':['Presence of a linked test is not exhaustive requirement coverage.','NCA actor handling is synthetic design evidence; the real guide used here addresses MAHs.','No registration/approval/SPL requirement is declared complete.']})
runtime={'created_at':now,'python':platform.python_version(),'packages':{x:importlib.metadata.version(x) for x in ['rdflib','pyshacl','owlready2','owlrl']},'java':subprocess.run(['java','-version'],capture_output=True,text=True).stderr,'reasoner':'Direct HermiT CLI via the previous package; explicit two-declaration PROV projection retained','native_sha256':native_sha,'dependencies':['../2.1.0-alpha.1-prov-target-lab/common.py','../2.1.0-alpha.1-registry-policy-lab/lab.py'],'network_required_for_replaying_pinned_NDC':False,'full_OWL2_DL_profile_checker_run':False}
write('runtime.json',runtime)
repo=read('repository-evidence.json')
summary={'created_at':now,'prior_head':repo['head'],'status':'REPORTING_CONTEXT_AND_CLAIM_BRIDGE_TESTED_NOT_ACCEPTED','query_pass':t['query_pass'],'query_total':t['query_total'],'shacl_pass':t['shacl_pass'],'shacl_total':t['shacl_total'],'hermit_pass':t['hermit_pass'],'hermit_total':t['hermit_total'],'ndc_unique_products':n['unique_source_product_ids'],'ndc_prior_overlap':n['prior_sample_overlap'],'ndc_new_products':n['new_unique_product_ids_beyond_prior'],'ndc_packages':n['package_projections'],'ndc_claims':n['structured_claims'],'claim_origin_counts':n['claim_origin_counts'],'ndc_checks_pass':n['pass'],'ndc_checks_total':n['total'],'esmp_guidance_profiles':e['profiles'],'esmp_checks_pass':e['pass'],'esmp_checks_total':e['total'],'esmp_real_action_announcements':0,'esmp_operational_submissions':0,'admission_regression_pass':r['pass'],'admission_regression_total':r['total'],'historical_positive_fixtures_combined':45,'historical_real_rows':768,'historical_real_triples':39272,'new_data_combined_shapes_conform':True,'bounded_deliverables_completed':4,'bounded_deliverables_total':4,'historical_major_gates_closed':2,'historical_major_gates_total':5,'historical_major_gate_percent':40,'historical_g3_packages_closed':2,'historical_g3_packages_total':7,'historical_g3_package_percent':28.6,'full_candidate_detector_runs':0,'full_candidate_detector_total':20,'all_prior_tasks_retained':23,'main_tasks_fully_closed_this_run':0,'open_issues':repo['open_issues'],'closed_issues':repo['closed_issues'],'issues_closed':0,'native_classes_added':0,'native_relations_added':0,'native_endpoints_changed':0,'baseline_modified':False,'scientific_acceptance':False,'pr':305,'pr_draft':True,'four_domain_removal_or_transfer_finalized':False}
write('summary.json',summary)
checkpoint=json.loads((PREV/'continuation-checkpoint.json').read_text())
checkpoint.update({'title':'CM-PharmE v2.1 — reporting context and source-qualified claim bridge','date':now,'previous_checkpoint':'../2.1.0-alpha.1-prov-target-lab/continuation-checkpoint.json','prior_development_head':repo['head'],'summary':summary,'active_issues':[x['number'] for x in repo['issues']]})
updates={
 'N02':('۱۳ پالایش محلی CL/CTX با آزمون و پیوند به نیازهای قبلی ثبت شد؛ به ۳۹ عنوان قبلی جمع زده نشده است','استخراج مستقل تمام دامنه‌ها و پذیرش ماتریس جامع'),
 'N05':('پل رکورد/ادعا و زمینهٔ گزارش‌دهی، بخش اطلاعاتی طرح چهار دامنه را تقویت کرد؛ هر چهار دامنه حفظ‌اند','ارزیابی متوازن و پذیرش مأموریت/مرز هر چهار دامنه؛ PV و BA هنوز نیازمند تکمیل‌اند'),
 'N06':('۱۵ رکورد NDC، ۱۹ بسته‌بندی، ۷۴ استخراج مستقیم و ۷۶ تفسیر پیشنهادی؛ ۷۲ کنترل موفق','شاهد ثبت مؤسسه، مدرک مستقل مجوز، داوری هویت و مسئولیت ثبت RG-07'),
 'N07':('مدل حداقلی زمینه، پنج پروفایل راهنمای ESMP نسخهٔ ۱٫۴ و ۱۶ کنترل موفق','اعلان واقعی اقدام با دامنهٔ محصول، زمان و تناوب؛ دادهٔ واقعی گزارش‌دهی و پذیرش مدل'),
 'N08':('مدل پایه ۱۳ منزوی داشت؛ نمونهٔ اصلاح‌شده همچنان چهار منزوی دارد؛ این اجرا native را تغییر نداد','DistributionLogisticsActivity، ProcurementActivity، RegulatoryRequirement و StockoutSituation نیازمند تصمیم مستندند'),
 'N09':('آزمون‌های زمینه، تعارض ادعا و تمایز استخراج/تفسیر به خانواده‌های قبلی افزوده شد','سناریوهای مستقل سایر دامنه‌ها و دادهٔ واقعی ریسک/ایمنی'),
 'P3':('پروندهٔ سه زیرکلاس توصیفی و سه عدم‌اشتراک پیشنهادی با حدود ادعا آماده شد','پذیرش پل ادعا، زمینه، PROV و تبدیل دو اعلان؛ RG-07 و C همچنان باز'),
 'P4':('سه زیرکلاس و قراردادهای OWL/SHACL در بستهٔ آزمایشی جدا پیاده شد؛ native تغییر نکرد','پذیرش و یکپارچه‌سازی هماهنگ native/OWL/SHACL'),
 'P6a':('۴۳ پرس‌وجو، ۱۴ آزمون SHACL و ۱۲ آزمون منطقی موفق؛ شاهدهای ناموفق مورد انتظار محفوظ','پوشش متوازن کل دامنه‌ها و سناریوهای خارج از نمونهٔ حاضر'),
 'P6b':('نوع تاریخ ناسازگار با HermiT اصلاح شد؛ رشتهٔ اصلی حفظ و تاریخ جدا اعتبارسنجی شد؛ منشأ تفسیر/استخراج صریح شد','قرارداد C، تبدیل PROV و اصلاح‌های نیازمند پذیرش علمی'),
 'P6c':('۱۰ رکورد NDC جدید نسبت به نمونهٔ قبلی؛ راهنمای رسمی ESMP منبع‌دار؛ خطاهای دریافت اولیه محفوظ','اعلان/گزارش عملیاتی ESMP، ثبت مؤسسه/مجوز، قرارداد #307 و علت قطعی W6'),
 'P6d':('رگرسیون ۱۱۶/۱۱۶، ترکیب ۴۵ گراف مثبت با دادهٔ جدید و بازآزمایی ۷۶۸ رکورد قبلی موفق','اعتبارسنجی کامل native/UFO و OWL2 DL، آشکارسازهای ۲۰گانه و مرور انسانی'),
 'N10':('ردیابی محلی نیاز→تست→شاهد برای ۱۳ پالایش ثبت شد','تثبیت و پذیرش ماتریس سراسری؛ پوشش محلی با پوشش کامل برابر نیست')}
for row in checkpoint['tasks']:
 if row['id'] in updates:row['current_extension'],row['remaining_fa']=updates[row['id']];row['status']='BOUNDED_EVIDENCE_READY_NOT_ACCEPTED'
assert len(checkpoint['tasks'])==23
checkpoint['next_steps_in_order']=[
 'Obtain a complete action-specific ESMP notice or authorised anonymised submission; map actor/product/country/action/version/time/frequency without inventing unavailable values.',
 'Develop the establishment-registration and independent-approval source contracts, preserving entity identity and the distinction between labeler attribution and listing responsibility.',
 'Extend independently sourced PV and BA scenarios and reconcile all-domain ownership and requirement gaps.',
 'Adjudicate the three description subclasses, claim-origin contract, source/fact migration, seven PROV mappings, two-declaration projection, RG-07, target policies and C. Generic continuation is not scientific acceptance.',
 'After accepted decisions, align native/OWL/SHACL and resolve 11 untyped ends, 66 unknown cardinalities, 14 specialised ends, four isolates and four detector discrepancies; run all 20 detectors.',
 'Resolve W6 and #307, complete human G3 review, then align data/article/Wiki/Pages, diagrams and release audit.']
checkpoint['source_review_update']={'guidance':'EMA MAH guide 1.4, 2026-04-28, six paraphrased extractions with printed-page locators','ndc':'Five predeclared purposive strata, 15 distinct rows; not representative','real_action_notice':'Not retrieved; no assertion that no such notice exists'}
write('continuation-checkpoint.json',checkpoint)
rows=['# وضعیت کامل CM-PharmE v2.1 — بستهٔ زمینهٔ گزارش‌دهی','','در G3 هستیم. خروج/انتقال چهار دامنه معلق است. PR305 پیش‌نویس و مرور علمی باز است. این اجرا هیچ‌یک از ۲۳ کار اصلی را به‌طور کامل نبست.','','| شناسه | کار | انجام‌شده | باقی‌مانده |','|---|---|---|---|']
for task in checkpoint['tasks']:rows.append('| '+ ' | '.join([task['id'],task['task_fa'],task.get('current_extension','کار قبلی محفوظ؛ پذیرش نهایی باز'),task.get('remaining_fa',task['deliverable_fa'])]).replace('\n',' ')+' |')
rows+=['','## درصدها با مخرج مشخص','','| شاخص | پیش از اجرا | اکنون | تغییر |','|---|---:|---:|---:|','| چهار خروجی محدود: پل ادعا، زمینه، شواهد NDC/راهنما، رگرسیون و گزارش | ۰/۴ | ۴/۴ = ۱۰۰٪ | +۱۰۰ واحد درصد در همین بسته |','| دروازه‌های تاریخی | ۲/۵ = ۴۰٪ | ۲/۵ = ۴۰٪ | صفر |','| بسته‌های اصلی G3 | ۲/۷ = ۲۸٫۶٪ | ۲/۷ = ۲۸٫۶٪ | صفر |','| اجرای معتبر آشکارسازها روی کل candidate | ۰/۲۰ | ۰/۲۰ | صفر |','','این چهار خروجی شامل دریافت اعلان واقعی ESMP نیست. درصد کلی وزنی پروژه تعریف نشده؛ درصد موفقیت تست‌ها درصد پیشرفت پروژه نیست.','','## همهٔ ایشوهای باز','',f"{repo['open_issues']} باز، {repo['closed_issues']} بسته؛ در این اجرا صفر بسته شد.",'','| ایشو | عنوان |','|---|---|']
rows += [f"| [#{x['number']}]({x['url']}) | {x['title']} |" for x in repo['issues']]
rows += ['','## گام‌های بعدی','']+[f'{i}. {x}' for i,x in enumerate(checkpoint['next_steps_in_order'],1)]
rows += ['','W6 در کامیت مبنای 894c207: run 37986934737 / job 114011149463 ناموفق؛ steps خالی و logs_url تهی؛ علت قطعی مشخص نشده است. تمام ۲۲ اجرای مشاهده‌شده در همان head ناموفق‌اند. این گزارش دربارهٔ CI کامیت بعدی ادعایی ندارد.','']
(H/'work-status-fa.md').write_text('\n'.join(rows))
report=f'''# گزارش تصمیم و شواهد — پل ادعا و زمینهٔ گزارش‌دهی

ادامه از `894c207`. تصمیم حذف/انتقال Risk Management، Pharmacovigilance، Business Architecture و Digital Systems همچنان معلق است. این بسته آزمایشی است و پذیرش علمی یا انتشار محسوب نمی‌شود.

## دستاورد

سه زیرکلاس پیشنهادی `StructuredClaim`، `ReportingContextDescription` و `ReportingScopeSpecification` ساخته شد. دو مورد اول زیرمجموعهٔ `Assertion` و سومی زیرمجموعهٔ `RegulatoryRequirement` است. هر سه در این پیشنهاد از `SourceRecord` جدا هستند. انتساب stereotype و اعتبار هستی‌شناختی native هنوز داوری نشده است.

ادعا، موضوع/محمول/مفعول، جهت مثبت/منفی، منشأ و مسیر شاهد دارد. محمول به‌صورت literal از نوع anyURI ذخیره می‌شود و triple توصیف‌شده خودکار ساخته نمی‌شود. این الگو پیشنهادِ توصیف محتواست؛ اثبات نهایی ماهیت UFO یا مناسب‌ترین مدل proposition نیست.

تمایز تازهٔ منشأ، استخراج فیلد منبع را از تفسیر مدل‌ساز و نمونهٔ مصنوعی جدا می‌کند. پاسخ `MAPPING_PROPOSED` به معنای گزارهٔ صریح منبع نیست. ادعاهای متعارض می‌توانند با هم نمایش داده شوند، بدون آنکه واقعیت بیرونی متناقض اعلام شود. نبود ادعا نیز صرفاً نبود شاهد در برش داده است.

زمینه، نقش، بازیگر، محصول/بسته‌بندی، کشور، حوزه، سناریو، مسیر، نسخه، بازه و اقدام را جدا نگه می‌دارد. خروجی‌ها تطبیق معیارهای اعلام‌شده، بیرون بودن از همان معیارها، نامعلوم، خطای ورودی یا اختلاف نسخه هستند. هیچ خروجی به‌تنهایی تأیید تکلیف قانونی، وقوع کمبود، مجوز محصول یا آمادگی عملیاتی نیست. تطبیق زمان پایان را انحصاری می‌گیرد؛ این قرارداد آزمایشی است، نه قاعدهٔ عمومی حقوقی. نبود تاریخ پایان می‌تواند پاسخ نامعلوم تولید کند؛ مدل دورهٔ باز هنوز کامل نیست.

## نتیجهٔ آزمون‌ها

| خانواده | نتیجه | دامنه |
|---|---:|---|
| پرس‌وجوی ادعا و زمینه | {t['query_pass']}/{t['query_total']} | مثبت، منفی، نامعلوم، تعارض و منشأ |
| قرارداد SHACL جدید | {t['shacl_pass']}/{t['shacl_total']} | شاهد مثبت و رد ورودی معیوب |
| HermiT جدید | {t['hermit_pass']}/{t['hermit_total']} | سازگاری و ضدمدل‌های محدود |
| نگاشت NDC | {n['pass']}/{n['total']} | منبع، تاریخ، پاسخ و عدم استنتاج واقعیت |
| پروفایل راهنمای ESMP | {e['pass']}/{e['total']} | پنج پروفایل با زمینه‌های صریحاً مصنوعی |
| رگرسیون قراردادهای قبلی | {r['pass']}/{r['total']} | inference=none و سلسله‌مراتب نام‌دار |

ترکیب ۴۵ نمونهٔ مثبت قبلی، زمینهٔ مصنوعی، NDC جدید و راهنمای ESMP با HermiT سازگار است؛ افزودن دو پیشنهاد عدم‌اشتراک قبلی هم آن را ناسازگار نکرد. قراردادهای قبلی و جدید روی دادهٔ جدید نیز موفق‌اند. نمونهٔ قبلی ۷۶۸ ردیفی/۳۹۲۷۲ triple دوباره آزموده شد؛ برای پروفایل ادعای جدید شاهد ندارد. این‌ها گواه پوشش کامل OntoUML/UFO، OWL2 DL، PROV-CONSTRAINTS یا ۲۰ آشکارساز نیستند. قرارداد C با نتیجهٔ تاریخی ۸۸/۸۹ همچنان جدا و حل‌نشده است.

## شواهد واقعی و حدودشان

NDC: پنج گروه از پیش تعیین‌شده، هرکدام سه نتیجه؛ ۱۵ شناسهٔ محصول متمایز، ۱۹ بسته‌بندی. پنج محصول با نمونهٔ قبلی مشترک و ۱۰ محصول جدید است. نمونه هدفمند و سهمیه‌ای است و نمایندهٔ آماری جامعه نیست. از ۱۵۰ گزاره، ۷۴ مورد استخراج فیلد و ۷۶ مورد تفسیر پیشنهادی نگاشت‌اند. نوع ثبت، نقش listed و مسئولیت ثبت جزء تفسیرهای پیشنهادشده‌اند؛ labeler به‌تنهایی تکلیف مسئولیت حقوقی ثبت را نهایی نمی‌کند. هویت محصول/سازمان در اینجا مرجع منبعی و نگاشت آزمایشی است. نتایج واقعیت ثبت، مجوز مستقل یا ثبت مؤسسه را تأیید نمی‌کنند.

ESMP: یک راهنمای رسمی نسخهٔ ۱٫۴ مورخ ۲۸ آوریل ۲۰۲۶، شش استخراج دستی و پنج پروفایل نگاشت شد. شناسهٔ اقدام، فهرست کامل محصولات و زمان‌بندی واقعی ساخته نشده است؛ زمینه‌های آزمایش مصنوعی‌اند و پاسخ فعال‌بودن واقعی نامعلوم باقی ماند. جست‌وجو به اعلان کامل اقدام یا گزارش عملیاتی نرسید؛ این به معنای نبود آنها نیست. URL، نسخه و checksum ثبت شده، اما PDF کامل در مخزن آرشیو نشده است. جزئیات منبع در `source-evidence.json` و `sources/esmp-guide-manifest.json` است. [راهنمای EMA]({read('source-evidence.json')['source']['url']}) و [مستندات openFDA](https://open.fda.gov/apis/drug/ndc/).

## اصلاح‌های کشف‌شده

- پرس‌وجوی نخست NDC با فیلد `.exact` به خطا رسید؛ درخواست اصلاح و دستهٔ واقعی هر پاسخ بررسی شد. شواهد خطا در sources محفوظ است.
- `xsd:date` در HermiT این پیکربندی پشتیبانی نشد. تاریخ اصلی JSON به صورت رشتهٔ YYYYMMDD حفظ و اعتبار تقویمی آن جدا بررسی شد؛ زمان یا منطقهٔ زمانی اختراع نشد. خطای اولیه ثبت شده است. تاریخ محصول فقط یک‌بار در هر ردیف استخراج می‌شود؛ تاریخ بسته‌بندی جداست.
- کنترل نوع گره برای موضوع/مفعول و برچسب منشأ اجباری اضافه شد. محتوای منبع و استنباط مدل‌ساز دیگر یک پاسخ یکسان ندارند.

## پروندهٔ تصمیم باز

پذیرش سه زیرکلاس و عدم‌اشتراک‌ها، معنای Assertion/RegulatoryRequirement، هویت claim در نسخه‌ها، چندموضوعی بودن گزاره‌ها، بازه‌های باز زمانی، اعتماد به شواهد، هم‌ارزی شناسه‌ها، جایگاه metadata و انتقال به native هنوز باز است. گراف قبلی NDC که واقعیت‌های ثبت را مستقیم تصویر می‌کرد دست‌نخورده مانده؛ این بسته مقصد پیشنهادی مهاجرت است و هیچ داده‌ای بی‌صدا جایگزین نشده است. تصمیم RG-07، نگاشت PROV و تبدیل دو اعلان و قرارداد C نیز پذیرش ندارند.

native هیچ کلاس/رابطه/سررابطهٔ تازه‌ای نگرفت. ۱۱ نوع نامعلوم، ۶۶ کران نامعلوم، ۱۴ سررابطهٔ تخصصی و چهار منزوی نمونهٔ اصلاح‌شده باقی است. موجودی پایهٔ ۱۳ منزوی با چهار منزوی نسخهٔ اصلاح‌شده یک شاخص یکسان نیست.

در G3 هستیم؛ پیشرفت دروازه‌های تاریخی ۲/۵ یا ۴۰٪ و بسته‌های اصلی G3 برابر ۲/۷ یا ۲۸٫۶٪ است. چهار خروجی محدود این اجرا آماده شد، ولی هیچ‌یک از ۲۳ کار اصلی یا ۳۰ ایشوی باز بسته نشد. همهٔ کارها و گام‌های بعد در `work-status-fa.md` آمده است.
'''
(H/'decision-report-fa.md').write_text(report)
(H/'README.md').write_text('''# Reporting-context and claim-bridge proposal laboratory

Isolated successor to `2.1.0-alpha.1-prov-target-lab`; no native or baseline mutation.

Run with Python 3 and Java 17, using versions in `runtime.json`, from this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python run_tests.py
PYTHONDONTWRITEBYTECODE=1 python run_esmp.py
PYTHONDONTWRITEBYTECODE=1 python run_real_data.py
PYTHONDONTWRITEBYTECODE=1 python run_regression.py
PYTHONDONTWRITEBYTECODE=1 python finalize.py
```

The previous labs are runtime dependencies. Replays use pinned source JSON, not new API results. Reruns regenerate graphs with non-stable blank-node labels and timestamps, so byte identity is not expected for generated artifacts; semantic results should match. Source snapshot hashes must match. HermiT receives RDF/XML verified graph-isomorphic to input, with the earlier explicitly documented PROV projection.

The five EMA profiles are manual design interpretations of official guidance. Contexts are synthetic. No real action announcement or operational submission is present. The PDF is URL/hash pinned but not archived here. NDC sampling is purposive, 15 source products with 5 overlapping the prior sample, 19 package projections. 74 direct field claims and 76 mapping interpretations are kept distinct; no described listing/authorization fact is materialized. Native identity, full OWL2-DL/UFO validity, legal compliance and release readiness are not established.

See `decision-report-fa.md`, `work-status-fa.md`, `requirements-traceability.json`, `continuation-checkpoint.json` and machine-readable results. Historical C 88/89 and scientific acceptance remain open. PR305 stays draft; the four domain disposition decisions stay on hold.
''')
for p in list(H.glob('*.ttl'))+list(H.glob('*.trig')):p.write_text(p.read_text().rstrip('\n')+'\n')
files=[p for p in H.rglob('*') if p.is_file() and p.name!='file-manifest.json' and '__pycache__' not in p.parts]
write('file-manifest.json',{'files':[{'path':str(p.relative_to(H)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)],'self_excluded':True})
print(json.dumps({'summary':summary,'manifest_files':len(files)},ensure_ascii=False))
