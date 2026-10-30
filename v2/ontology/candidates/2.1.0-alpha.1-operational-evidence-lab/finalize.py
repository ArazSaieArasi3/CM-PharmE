"""Evidence readiness, scientific decisions, complete queue and manifest."""
from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
H=Path(__file__).resolve().parent;PREV=H.parent/'2.1.0-alpha.1-module-contract-lab'
def read(name):return json.loads((H/name).read_text())
def dump(name,x):(H/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
contract=read('contract-results.json');contract_extract=read('contract-extraction.json')
results=read('results.json');risk=read('risk-scope-results.json');integ=read('integration-results.json');repo=read('repository-evidence.json')
matrix=[
 ('RM','RiskAssessmentActivity','RM-EMA-2020','Source reports a completed public review; month precision','Company-level assessment inputs, scoring and organization-specific scenario absent'),
 ('RM','RiskReviewActivity','RM-EMA-2020','Source describes revised limits and prior review; mapping proposed','Exact review occurrence/time and formal predecessor/result identity unestablished'),
 ('RM','RiskTreatmentPlan','RM-EMA-2020','Normative control expectations only','No company-specific adopted treatment plan obtained'),
 ('RM','RiskTreatmentActivity','RM-EMA-2020','No execution witness in this selected document','Need actual implemented action and effectiveness evidence'),
 ('PV','AdverseEventReportingActivity','Prior PRAC package; DS-EMA-LIVE','Reporting functionality and documentary safety recommendations','No individual ICSR submission occurrence or message acquired'),
 ('PV','PharmacovigilanceRequirement','Prior reporting-context package; DS-EMA-LIVE','Guidance/requirement descriptions; versioned source context','Current obligation applicability and concrete operational reporting evidence'),
 ('PV','PostMarketSurveillanceActivity','DS-EMA-LIVE','System supports safety analysis; does not prove a specific surveillance occurrence','Actual surveillance process and responsible actor evidence'),
 ('PV','SignalAssessmentActivity','Prior PRAC package','Three documentary recommendations and interpreted signal/result links','Assessment occurrence/time and complete identity binding'),
 ('BA','BusinessArchitectureView','This analytical crosswalk','Authored view, explicitly analyst-created','No claim that an external company published this architecture view'),
 ('BA','ServiceOfferingSpecification','BA-LONZA-2020-05; BA-MODERNA-SEC-2020','Manufacturing scope publicly described','SOW definition inspected in SEC exhibit; actual work orders are missing/redacted'),
 ('BA','EnterpriseCapability','BA-LONZA-2020-05; BA-LONZA-2021-04','Expertise reported; subsequent production separately reported','Capability identity, quantitative capacity and temporal persistence not established'),
 ('BA','PartnerOrganizationRole','BA-LONZA-2020-05; BA-MODERNA-SEC-2020','Two corporate labels in announcement; three legal signatory labels in SEC exhibit','Registry identifiers and contextual participant sets remain unresolved'),
 ('BA','StrategicPartnershipAgreement','BA-LONZA-2020-05; BA-LONZA-2020-07; BA-MODERNA-SEC-2020','Issuer reports plus public redacted executed GLTA; three-party commitment projection tested','Unredacted terms and SOWs absent; SCA/GLTA identity and subset commitments need review'),
 ('DS','DigitalInformationSystemComponent','DS-EMA-LIVE; DS-EMA-TIMELINE','Identified system and supported message standard','System-to-component granularity and software build identifier unestablished'),
 ('DS','SystemDeploymentActivity','DS-EMA-LIVE; DS-EMA-TIMELINE','Official launch report and historical day','Exact instant, build version, technical operator and deployment log absent')]
dump('core-evidence-matrix.json',{'rows':[dict(zip(['domain','concept','sources','supported','remaining'],r)) for r in matrix],'owned_concepts_reviewed':len(matrix),'count_is_not_empirical_coverage':True,'rules':['A document mentioning a concept does not fully instantiate it','Publisher-self-report is distinguished from independent regulator evidence','Every listed gap remains open until its acceptance criterion is met']})
decisions=[
 {'id':'OE-01','topic':'RM family-scoped risk','recommendation':'Keep scenarioScopeDescription as a proposed information relation to a versioned source-defined scope. Reuse the PV scope profile; do not create a fake MedicinalProduct for a family.','evidence':'risk-scope-results.json: 8/8 checks, 2/2 logical expectations','remaining':'Native representation and semantic acceptance; formal scope membership versus lexical source labels.'},
 {'id':'OE-02','topic':'Time precision','recommendation':'Retain day/month/year and time role on documentary claims. Use an interval for a month/year; never manufacture a midnight instant or treat publication date as event date.','evidence':'RM January 2019; DS launch day; BA occurrence upper bounds and planned windows','remaining':'A future accepted temporal model for domain events, separate from this documentary adapter.'},
 {'id':'OE-03','topic':'Plan versus occurrence','recommendation':'Keep planned/required/capability/occurrence reports distinct and query source publication cutoffs. A future target is not observed capacity.','evidence':'Lonza May 2020 plan, July 2020 transfer update, April 2021 production report','remaining':'Redacted/absent work orders, commitment identity, quantities and effectiveness; public executed agreement now examined.'},
 {'id':'OE-04','topic':'DS granularity and version','recommendation':'Preserve launch evidence in the documentary layer until component/build/operator details are known. E2B(R3) is a message format, not componentVersion. Keep the complete deployment profile strict.','evidence':'DS-complete-deployment projection correctly rejected','remaining':'Actual deployment/change record and operator evidence; choose system/component scope explicitly.'},
 {'id':'OE-05','topic':'Registry licence boundary','recommendation':'Use Swissmedic as authority evidence for a facility licence. Do not promote it to product marketing authorization or establishment registration.','evidence':'REG-SWISSMEDIC-2021 and query boundary checks','remaining':'Licence record/identifier, exact issuance date, legal object classification and RG-07.'}]
decisions.append({'id':'OE-06','topic':'BA contract identity and party scope','recommendation':'Keep SCA and GLTA separate; retain made/effective dates and three signature-party identities. Scope commitments to their agreement/SOW. Do not collapse affiliates into corporate labels or apply the exact-set profile universally.','evidence':'Public SEC Exhibit 10.2; contract-results.json: 11/11 checks and 2/2 logical expectations','remaining':'Missing SOWs, redacted clauses, registry identity, debtor/creditor roles and subset/affiliate commitments.'})
for d in decisions:d['status']='PROPOSED_NOT_YET_SCIENTIFICALLY_ACCEPTED';d['execution_owner']='assistant';d['review_owner']='Araz'
dump('decision-dossier.json',{'retention_direction':'ACCEPTED; all four domains retained','decisions':decisions,'proceed_without_waiting':['source and identifier research','scenario expansion','formal validation preparation'],'not_inferred':['full semantic approval','merge/release approval for this draft candidate']})
summary={'created_at':datetime.now(timezone.utc).isoformat(),'base_head':repo['base_head'],'four_domain_direction':'RETAIN_ACCEPTED','source_documents':8,'publisher_families':4,'new_source_extractions':results['source_extractions']+contract_extract['count'],'proposed_ontology_mappings':results['proposed_mappings'],'documentary_checks':[results['passed'],results['total']],'risk_scope_checks':[risk['passed'],risk['total']],'contract_checks':[contract['passed'],contract['total']],'logical_checks':[results['logical_passed']+sum(x['pass'] for x in risk['logical'])+sum(x['pass'] for x in contract['logical'])+int(integ['combined_reasoner']['consistent'] and not integ['combined_reasoner']['unsatisfiable_named_classes']),8],'expected_incomplete_projection_rejections':3,'combined_triples':integ['combined_triples'],'combined_admission':integ['combined_admission'],'historical_fixtures_inspected_not_reexecuted':83,'new_owned_classes':0,'new_domain_information_relations':1,'native_changed':False,'semantic_acceptance':'Retention direction only; six new detailed decisions pending','issues_open':repo['open_count'],'issues_closed':repo['closed_count'],'issues_closed_this_run':0,'progress':{'targeted_RM_BA_DS_documentary_witnesses':[3,3],'portable_modules_prior':[4,4],'historical_gates':[2,5],'G3_packages':[2,7],'full_detector_runs':[0,20],'global_weighted_percent':None}}
dump('summary.json',summary)
checkpoint=json.loads((PREV/'continuation-checkpoint.json').read_text());checkpoint['prior_summary']=checkpoint.pop('summary');checkpoint['summary']=summary
checkpoint.update(title='CM-PharmE v2.1 — operational documentary evidence and scope refinement',date=summary['created_at'],previous_checkpoint='../'+PREV.name+'/continuation-checkpoint.json',prior_development_head=repo['base_head'])
updates={
 'N03':('ماتریس شاهد و شکاف برای تمام ۱۵ مفهوم هستهٔ چهار دامنه تهیه شد','داوری تعریف‌ها و مالکیت جامع سایر دامنه‌ها'),
 'N05':('حفظ چهار دامنه پذیرفته؛ چهار بستهٔ مستقل قبلی محفوظ و برای RM/BA/DS شاهد واقعی مستند افزوده شد','پذیرش جزئیات و تکمیل شواهد عملیاتیِ فاقد شناسه/زمان/تعهد'),
 'N06':('اطلاعیهٔ رسمی Swissmedic دربارهٔ مجوز محل تولید Lonza پیدا و نگاشت شد','شناسه و رکورد مجوز، ثبت مؤسسه، مجوز محصول و داوری RG-07'),
 'N09':('سناریوهای برنامه/وقوع، زمان کم‌دقت، نسخهٔ مجهول، مجوز محل و گروه ریسک اضافه شد','پوشش دادهٔ عملیاتی و سناریوهای مستقل باقی‌مانده'),
 'P3':('شش تصمیم علمی مشخص با پیشنهاد و شاهد آزمون آماده شد','داوری شش تصمیم و صف روابط/C/PROV/RG-07'),
 'P4':('رابط اطلاعاتی محدودهٔ ریسک و پروفایل شواهد OWL/SHACL آزمایشی پیاده شد؛ native ثابت ماند','اعمال تصمیم‌های مصوب و هماهنگی کامل نمایش‌ها'),
 'P6a':('۳۱ کنترل شواهد، ۸ کنترل محدودهٔ ریسک، ۱۱ کنترل قرارداد و ۳ ردِ موردانتظار برای دادهٔ ناکامل موفق شد','نمونه‌های عملیاتی متوازن‌تر'),
 'P6b':('شکاف خانوادهٔ دارویی با استفادهٔ مجدد از پروفایل گروه پوشش داده شد؛ قیود کامل قبلی تضعیف نشد','زمان رویداد، هویت جزء سامانه و تعهد واقعی هنوز نیازمند تصمیم‌اند'),
 'P6c':('۸ سند اولیه، ۴۹ استخراج و ۱۳ نگاشت پیشنهادی ثبت شد؛ چهار خانوادهٔ ناشر؛ قرارداد عمومی دارای امضا نیز بررسی شد','SOWهای واقعی و هویت تعهدها، لاگ استقرار، اجرای اقدام RM، شاهد ESMP و رفع CI/#307'),
 'P6d':('۸ انتظار منطقی موفق؛ گراف ترکیبی شامل شواهد، محدودهٔ ریسک و نگاشت قراردادی سازگار و پذیرفته شد','اعتبارسنجی جامع، ۲۰ آشکارساز و مرور انسانی')}
for task in checkpoint['tasks']:
 if task['id'] in updates:task['current_extension'],task['remaining_fa']=updates[task['id']]
checkpoint['next_steps_in_order']=['Obtain company-level risk treatment/review and effectiveness records; retain public regulatory review separately.','Obtain full contract/commitment identity and deployment/build/operator evidence; resolve DS system/component granularity.','Review six OE decisions, prior ten relation proposals and C/PROV/RG-07; no invented identifiers/timestamps.','Continue real ESMP action and registry/licence identifier evidence; resolve CI and #307.','Align accepted native/OWL/SHACL changes, run full detectors and human G3 review, then documentation/article/diagrams/release.']
dump('continuation-checkpoint.json',checkpoint)
report='''# گزارش شواهد واقعی و کیفیت چهار دامنه

تصمیم حفظ Risk Management، Pharmacovigilance، Business Architecture و Digital Systems پابرجاست. کار اجرایی با دستیار است. این نوبت طراحی را با شواهد تاریخی واقعی سنجیدیم؛ پذیرش کامل علمی یا انتشار اعلام نمی‌شود.

## دستاوردهای تازه

| حوزه | شاهد و نتیجهٔ قابل استفاده | مرز مهم |
|---|---|---|
| RM | سند EMA/603826/2020 بازبینی قبلی و تغییر مبنای حدود ناخالصی از مادهٔ مؤثره به محصول نهایی را گزارش می‌کند؛ پنج نام داخل محدوده و سه نام خارج از آن مشخص‌اند | الزام به کنترل و آزمایش، اجرای اقدام توسط شرکت را اثبات نمی‌کند؛ زمان بازبینی قبلی فقط ماه است |
| BA | سه اطلاعیهٔ Lonza از توافق و برنامهٔ اولیه، تکمیل انتقال فناوری و سپس تولید آغازشده خبر می‌دهند | هدف تولید با ظرفیت تحقق‌یافته برابر نیست؛ سه اطلاعیه از یک خانوادهٔ ناشرند؛ نسخهٔ عمومیِ دارای امضا با حذف برخی بندها در SEC نیز بررسی شد؛ SOWهای واقعی موجود نیست |
| DS | اطلاعیهٔ EMA و خط زمانی رسمی راه‌اندازی EudraVigilance در ۲۲ نوامبر ۲۰۱۷ را پشتیبانی می‌کنند | شمارهٔ build، زمان دقیق و اپراتور فنی معلوم نیست؛ E2B(R3) نسخهٔ نرم‌افزار نیست |
| Registry | اطلاعیهٔ Swissmedic، اعطای مجوز محل تولید Lonza را گزارش می‌کند | شمارهٔ مجوز و روز صدور موجود نیست؛ این شاهد مجوز بازاریابی محصول یا ثبت مؤسسه نیست |
| PV | پروفایل محدودهٔ گروه مواد قبلی حفظ و در RM بازاستفاده شد؛ شاهد سامانهٔ گزارش‌دهی نیز افزوده شد | هنوز دادهٔ ICSR یا وقوع یک ارسال مشخص نداریم |

۸ سند از چهار خانوادهٔ ناشر خوانده شد؛ ۴۹ گزارهٔ مستند و ۱۳ نگاشت صریحاً پیشنهادی ذخیره شد. علاوه بر نگاشت‌های گزاره‌ای، یک تصویر پیشنهادی از قرارداد سه‌طرفه در مدل BA ساخته و آزموده شد. نمونه‌گیری هدفمند است و نمایندگی آماری یا داوری مستقل متخصص محسوب نمی‌شود. گزارش شرکت با شاهد مقام تنظیم‌گر یکسان شمرده نشده است.

## تغییر مدل و آزمون

یک رابطهٔ اطلاعاتی پیشنهادی `scenarioScopeDescription` افزوده شد تا سناریوی ریسک به محدودهٔ نسخه‌دار یک خانواده اشاره کند. مدل گروه مواد PV بازاستفاده شد؛ گروه به محصول یا مادهٔ شیمیایی منفرد تبدیل نشد. هیچ کلاس اختصاصی تازه یا تغییر native اعمال نشد. این رابطه و پروفایل هنوز نیازمند داوری علمی‌اند.

لایهٔ شواهد اکنون برنامه، الزام، قابلیت گزارش‌شده، محتوای ارزیابی، وقوع گزارش‌شده، گزارش مجوز و نگاشت پیشنهادی را متمایز می‌کند. دقت زمانی روز/ماه/سال و نقش زمان حفظ می‌شود. زمان انتشار با زمان وقوع مخلوط نمی‌شود. پاسخ‌ها گزاره‌های سند را گزارش می‌کنند و رابطهٔ جهان واقعی را خودکار ایجاد نمی‌کنند.

- کنترل شواهد و پاسخ‌ها: **۳۱/۳۱**.
- کنترل محدودهٔ ریسک: **۸/۸**.
- کنترل قرارداد عمومی و تصویر پیشنهادی آن: **۱۱/۱۱**.
- انتظارهای منطقی با HermiT: **۸/۸**، شامل ترکیب با دادهٔ مثبت قبلی.
- سه نمونهٔ ناکامل RM/BA/DS مطابق انتظار توسط قراردادهای کامل رد شدند؛ کمبودها ثبت شد.
- گراف ترکیبی **__TRIPLES__ سه‌تایی** پذیرفته و سازگار بود.
- ۸۳ فایل آزمون قبلی از نظر برخورد با هدف قیود تازه بررسی شد؛ صفر برخورد. آن ۸۳ آزمون این بار دوباره اجرا نشده‌اند و به دستاورد تازه جمع نمی‌شوند.

## کیفیت و باقی‌مانده

برای تمام ۱۵ مفهوم هسته، شاهد موجود، نوع پشتیبانی و شکاف باقیمانده در core-evidence-matrix.json آمده است. عدد ۱۵/۱۵ به معنی کامل‌بودن شاهد برای همهٔ مفاهیم نیست. هدف و استقلال اجرایی چهار بسته برقرار است؛ شواهد واقعی اکنون محدودیت‌های عملی آن‌ها را نیز نشان می‌دهد.

شش تصمیم OE-01 تا OE-06 آماده است: محدودهٔ گروه در RM، دقت زمانی، برنامه در برابر وقوع، مرز سامانه/جزء و نسخه در DS، مرز مجوز محل تولید، و هویت قرارداد/طرف‌ها/تعهدها. پیشنهاد فعلی، حفظ لایهٔ شواهد ناقص در کنار قراردادهای سخت‌گیرانهٔ دادهٔ کامل است. برای پرکردن شکاف، شناسه، زمان یا رابطه ساخته نشده است.

منزوی‌های کپی native قبلی همچنان موضوع همان نتیجهٔ ساختاری صفر منزوی‌اند؛ این نوبت native تغییر نکرد و پیشرفت ساختاری دوباره محاسبه نمی‌شود. اعتبار علمی اتصال‌ها هنوز باز است.

## پیشرفت

تهیهٔ حداقل شاهد مستند برای سه دامنهٔ هدف این نوبت: **۳/۳ = ۱۰۰٪ این زیرکار**. این درصد، کامل‌بودن سه انتالوژی نیست. چهار بستهٔ مستقلِ نوبت قبل محفوظ‌اند. دروازه‌های تاریخی **۲/۵ = ۴۰٪** و بسته‌های G3 برابر **۲/۷ = ۲۸٫۶٪** باقی ماندند. اجرای معتبر هر ۲۰ آشکارساز روی کل candidate هنوز **۰/۲۰** است. درصد کلی وزنی پروژه تعریف نشده است.

۳۰ ایشو باز و ۱۷۰ بسته؛ صفر ایشو این نوبت بسته شد. PR305 پیش‌نویس باقی می‌ماند. CI از نوبت قبلی حل‌نشده است؛ آزمون محلی معادل موفقیت CI نیست.

## گام بعدی

۱. رکورد شرکتی ارزیابی/اجرای اقدام ریسک و اثربخشی، متن تعهدات قرارداد و رکورد استقرار/نسخه/اپراتور را دنبال کنیم.
۲. شش تصمیم جدید و صف روابط، C/PROV/RG-07 را داوری کنیم؛ بهترین پیشنهادها در decision-dossier.json آماده‌اند.
۳. شاهد عملیاتی ESMP، شناسهٔ مجوز و ثبت مؤسسه را تکمیل کنیم؛ CI و #307 را حل کنیم.
۴. تغییرات مصوب را در native/OWL/SHACL هماهنگ کنیم و اعتبارسنجی جامع و مرور انسانی G3 را انجام دهیم؛ سپس مقاله، ویکی، Pages، دیاگرام‌ها و انتشار.

پیوند و محل دقیق هر شاهد در sources.json و extractions.json ثبت شده است. فایل کامل منابع آرشیو نشده و هش بایت آن‌ها ادعا نشده است. این نمونه‌ها تاریخی‌اند و مبنای توصیهٔ بالینی یا حکم انطباق حقوقی فعلی نیستند.
'''
report=report.replace('__TRIPLES__',str(integ['combined_triples']))
report+='\n## یافتهٔ تکمیلی BA\n\nنسخهٔ عمومیِ قرارداد دارای امضا در پروندهٔ SEC پیدا شد. سه نام شخصیت حقوقی از بخش امضا استخراج شد؛ تفاوت تاریخ تنظیم و تاریخ اثرگذاری و جدا بودن SCA از GLTA حفظ شد. متن عمومی برخی بندها را حذف کرده و پیوست‌های SOW واقعی در آن موجود نیست. تصویر پیشنهادیِ تعهد مشترک سه‌طرفه با مفاهیم موجود پذیرفته شد؛ افزودن بازیگر خارج از قرارداد یا حذف شاهد رد شد. این موفقیت، قاعدهٔ برابر بودن بازیگران هر تعهد با تمام طرف‌های قرارداد را برای همهٔ قراردادها اثبات نمی‌کند؛ تعهدهای زیرمجموعه‌ای و شرکت‌های وابسته در صف تصمیم باقی ماندند.\n'
(H/'decision-report-fa.md').write_text(report)
work='# فهرست کامل کارها — شواهد واقعی چهار دامنه\n\nهیچ‌یک از ۲۳ کار اصلی کاملاً بسته نشده است. زیرکارهای انجام‌شده و باقی‌مانده به‌صورت جدا ثبت شده‌اند.\n\n| شناسه | کار | انجام‌شده | باقی‌مانده |\n|---|---|---|---|\n'
for t in checkpoint['tasks']:work+='| '+t['id']+' | '+t['task_fa']+' | '+t.get('current_extension','کار قبلی محفوظ؛ پذیرش نهایی باز')+' | '+t.get('remaining_fa',t.get('deliverable_fa','پذیرش نهایی'))+' |\n'
work+='\n## تمام ایشوهای باز\n\n| ایشو | عنوان |\n|---|---|\n'
for i in repo['open_issues']:work+='| [#'+str(i['number'])+']('+i['url']+') | '+i['title']+' |\n'
(H/'work-status-fa.md').write_text(work)
(H/'README.md').write_text('''# CM-PharmE — operational documentary witnesses

Eight primary documents, 49 extracted statements and 13 explicit mapping proposals test the practical boundaries of the retained four-domain design. The source evidence is historical, purposive and documentary; it is not a complete operational dataset or independent expert validation.

Read decision-report-fa.md, work-status-fa.md, core-evidence-matrix.json and decision-dossier.json. The 15-concept matrix deliberately includes unsupported and partially supported concepts. Do not call all 15 empirically covered.

Run from this directory with the preceding experiment packages present:

```sh
python run_lab.py
python run_risk_scope.py
python run_contract.py
python run_integration.py
python finalize.py
```

Python requirements: rdflib 7.6.0, pyshacl 0.30.1, owlready2 0.49; Java 17. These research runners use the full repository model. The previous four standalone exports remain unchanged; this new evidence adapter is not represented as a new standalone release.

New relation: scenarioScopeDescription, information-to-information; scientific approval and native representation pending. Existing complete profiles were not relaxed to make incomplete sources pass. Qualification modes distinguish plans, requirements, capabilities, reported occurrences, assessment content and authorization reports. Date precision and publication cutoffs do not establish current world truth.

The no-materialization countermodel establishes only scoped non-entailments. No full OWL2 DL, UFO/OntoUML conformance, detector-suite execution, semantic acceptance or release closure is claimed.
''')
manifest=[{'path':str(p.relative_to(H)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(H.rglob('*')) if p.is_file() and p.name!='file-manifest.json' and '__pycache__' not in p.parts]
dump('file-manifest.json',{'files':manifest,'count':len(manifest)})
print(json.dumps({'files':len(manifest)+1,'summary':summary}),flush=True)
