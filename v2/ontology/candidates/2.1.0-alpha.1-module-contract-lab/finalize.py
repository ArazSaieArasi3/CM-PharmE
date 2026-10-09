"""Summarize measured evidence and preserve the complete work queue."""
from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
H=Path(__file__).resolve().parent;OLD=H.parent/'2.1.0-alpha.1-domain-coherence-lab'
def dump(name,data):(H/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def read(name):return json.loads((H/name).read_text())
catalog=read('module-catalog.json');results={m:read('modules/'+m+'/results.json') for m in ['RM','PV','BA','DS']}
counts={key:[sum(r['counts'][key][i] for r in results.values()) for i in [0,1]] for key in ['admission','queries','reasoner','source_scope_lookups']}
summary={'status':'BOUNDED_STANDALONE_MODULES_READY_FOR_SCIENTIFIC_REVIEW','direction':'FOUR_DOMAINS_RETAINED_BY_USER_DECISION','modules':catalog,'counts':counts,'integration':read('integration-results.json')['integrated'],'full_fixture_comparison':[read('integration-results.json')['passed'],read('integration-results.json')['total']],'pv_group_checks':[read('pv-group-results.json')['passed'],read('pv-group-results.json')['total']],'progress':{'portable_modules':[4,4],'historical_gates':[2,5],'G3_main_packages':[2,7],'full_detector_suite':[0,20],'global_weighted_percentage':None},'new_scientific_acceptance':'Retention/design direction only','native_unchanged':True,'merge_performed':False,'issue_closed_count':0,'limits':['Historical fixture replays are not new independent empirical evidence','Source-group checks overlap portable PV checks and must not be added as independent coverage','The current exports are signature projections, not formally certified locality modules','29 DS interface classes include the PROV dependency closure; only two classes are counted as owned','No full OntoUML/UFO or OWL2 DL conformance claim; relation stereotypes and cardinalities remain under review']}
dump('summary.json',summary)
contracts={
'RM':{'input':'A scoped medicinal product, facility or supply dependency; a documentary source; assessment and optional review occurrences.','output':'Traceable assessment content, a treatment plan, separately evidenced treatment execution, and predecessor/successor review content.','flow':'scenario → assessment → result/evidence → plan; execution references the plan; review connects prior/new results.','questions':['What product, facility or dependency is assessed, and which source supports the result?','Which plans have no recorded execution in this dataset?','Which review changed which result and conclusion?'],'definitions':{'RiskAssessmentActivity':'An occurrence assessing a scoped risk scenario; distinct from its result content.','RiskTreatmentActivity':'An occurrence executing a risk treatment plan; the plan alone does not establish this occurrence.','RiskTreatmentPlan':'An information artifact specifying a proposed treatment response to an assessment result.','RiskReviewActivity':'An occurrence reviewing earlier assessment content and connecting it with new content.'},'remaining':'Real independent risk assessment/review evidence, treatment effectiveness, agreed temporal semantics and review of event/content boundaries.'},
'PV':{'input':'A safety report or other documentary source, a product/substance or versioned source-defined group scope, and optionally an attributed assessment occurrence.','output':'Traceable signal content and assessment-result content; source statements separated from proposed mappings and actual events.','flow':'source record → reported content → safety signal → assessment → result; a documentary scope points to versioned lexical entries.','questions':['Which target and source are associated with a signal?','How do successive assessment results differ, and who is attributed as assessor?','Which jurisdiction/requirement supports surveillance?','Which labels are listed in this exact source scope, and which qualifiers remain unknown?'],'definitions':{'AdverseEventReportingActivity':'An occurrence reporting safety-related content through a record; it is not the record or a clinical adverse event.','PharmacovigilanceRequirement':'An information object specifying a pharmacovigilance requirement in its applicability context.','PostMarketSurveillanceActivity':'An occurrence conducting post-market surveillance under an identified requirement using identified sources.','SignalAssessmentActivity':'An occurrence assessing a safety signal; distinct from reporting and assessment-result content.'},'remaining':'Actual assessment/time evidence, an ICSR contract, canonical chemical identity mapping, legal applicability/version review and native representation of accepted information profiles.'},
'BA':{'input':'Organizations, a pharmaceutical service specification, a borne capability, and documentary partnership commitments when actually supported.','output':'An analytical architecture view linking organizations, service specifications, capabilities and evidenced collaboration commitments.','flow':'view → organization/service → capability → bearer; strategic agreement → participants/commitment/evidence.','questions':['Who bears a capability, including a capability with no recorded exercise?','Which medicinal product or facility gives the service a pharmaceutical scope?','What commitments and documentary evidence support a strategic agreement?'],'definitions':{'BusinessArchitectureView':'An information artifact representing selected organizational and service relationships for an analytical purpose.','ServiceOfferingSpecification':'An information artifact specifying a service offering; distinct from execution of that service.','EnterpriseCapability':'A capability borne by an organization; its presence does not imply an execution or a quantity of supply capacity.','PartnerOrganizationRole':'A contextual organization role grounded in a strategic partnership agreement.','StrategicPartnershipAgreement':'A proposed relator grounding participants and commitments; the agreement document is a separate source record.'},'remaining':'Independent real contract evidence and adjudication of agreement/commitment/document identity; not every outsourcing arrangement is a strategic partnership.'},
'DS':{'input':'An identified digital component, versioned deployment and organization, a data activity and generated record, plus a supported pharmaceutical operation.','output':'A trace from a record to the digital activity, deployment/version, operator and separately attributed activity responsibility.','flow':'record → data activity → deployment → component/version/operator; data activity → supported manufacturing/logistics.','questions':['Which component version and deployment produced this record?','Which organization operated deployment, and which was responsible for processing?','Which pharmaceutical manufacturing or logistics activity was supported?'],'definitions':{'DigitalInformationSystemComponent':'An identifiable software/information-system component used in a deployment; distinct from a generated record.','SystemDeploymentActivity':'An actual occurrence deploying an identified component version in an organizational context; distinct from transformation of data.'},'remaining':'Independent real deployment/agent evidence, version identity, delegation and responsibility, and adjudication of the inherited PROV projection.'}}
ownership={iri:m for m in contracts for iri in read('modules/'+m+'/contract.json')['owned_classes']}
for m,detail in contracts.items():
 contract=read('modules/'+m+'/contract.json');contract['purpose_contract']=detail
 contract['interface_ownership']={iri:ownership.get(iri,'PROV standard' if 'www.w3.org/ns/prov#' in iri else 'CM-PharmE shared/other-domain interface; final ownership review pending') for iri in contract['imported_interface_classes']}
 dump('modules/'+m+'/contract.json',contract)
 text='# '+contract['name']+' — purposeful minimum viable ontology\n\n'+contract['mission_fa']+'\n\nStatus: retention direction accepted by user; detailed model remains a review proposal.\n\n## Purpose and boundary\n\nInput: '+detail['input']+'\n\nOutput: '+detail['output']+'\n\nWorkflow: '+detail['flow']+'\n\n## Owned concepts (working definitions)\n\n| Concept | Working definition |\n|---|---|\n'
 for name,definition in detail['definitions'].items():text+='| '+name+' | '+definition+' |\n'
 text+='\nThese are proposed working definitions. Imported interface classes are separately listed in contract.json and are not added to the owned count.\n\n## Competency questions\n\n'+'\n'.join('- '+x for x in detail['questions'])+'\n\n## Excluded scope\n\n'+'\n'.join('- '+x for x in contract['excluded_scope'])+'\n\n## Independent execution\n\nCopy this directory anywhere. With Java 17 installed, install requirements.txt and run `python runner.py`. The runner reads only this directory; it does not load sibling labs or fetch ontology imports. All selected dependencies are flattened into ontology.ttl.\n\nMeasured results: '+str(results[m]['counts'])+'. The source-group lookups in PV are documentary/proposed-mapping answers, not patient or legal advice.\n\n## Limits and remaining work\n\n'+detail['remaining']+'\n\nSelected-signature projection, not a formally certified locality module. See omissions.json. Full and local admission behavior was compared only on the listed fixtures. SHACL opt-in required fields are not universal OWL cardinalities. Native OntoUML module exports and full semantic acceptance are not claimed.\n'
 (H/'modules'/m/'README.md').write_text(text)
checkpoint=json.loads((OLD/'continuation-checkpoint.json').read_text());checkpoint.update(title='CM-PharmE v2.1 — purposeful standalone module contracts',date=datetime.now(timezone.utc).isoformat(),previous_checkpoint='../'+OLD.name+'/continuation-checkpoint.json',prior_development_head='3ad341f24aa52b2faba624b6c39a9df67250abbb',decision_hold='Superseded for design direction: user accepts retaining all four domains as purposeful small ontologies.',scientific_acceptance='Retention direction accepted; detailed semantics and release remain pending.')
updates={
'N03':('چهار قرارداد هدف، ورودی/خروجی، تعریف هسته، مرز و وابستگی با اجرای مستقل ثبت شد','مالکیت جامع همهٔ دامنه‌ها و داوری تعریف‌های پیشنهادی'),
'N05':('جهت حفظ چهار دامنه با تأیید کاربر ثبت شد؛ چهار بستهٔ مستقل آزموده شد','شواهد عملیاتی مستقل و تأیید جزئیات چهار مدل'),
'N09':('۲۸ مدخل گروه مواد، ۱۵ آزمون جست‌وجوی مقید و سه پرس‌وجوی تازه PV افزوده شد','پوشش متوازن شواهد واقعی سایر دامنه‌ها و هویت شیمیایی معتبر'),
'P4':('مدل گروه مواد در OWL/SHACL آزمایشی و بستهٔ مستقل PV پیاده شد','بازنمایی native پس از پذیرش علمی؛ سایر نمایش‌ها هنوز کاملاً هماهنگ نشده‌اند'),
'P6a':('۸۳ آزمون داده و ۲۳ پرس‌وجو در چهار بستهٔ مستقل موفق؛ ۷۲ آزمون داده بازاجرای شواهد قبلی است','پوشش سناریوهای مستقل باقی‌مانده'),
'P6b':('نقص انتقال shapeهای نام‌دار و فقدان قید تمایز توصیف/حامل پیدا و اصلاح شد؛ شکست‌های اولیه محفوظ','تصمیم‌های C/PROV و اصلاح‌های معنایی مصوب'),
'P6c':('پاورقی ۴ سند رسمی PRAC بازخوانی شد؛ ۲۸ مدخل نسخه‌دار استخراج شد','دادهٔ عملیاتی ESMP و شواهد RM/BA/DS، CI و #307'),
'P6d':('۸۳/۸۳ نتیجهٔ پذیرش مستقل و کامل برابر؛ ۱۴/۱۴ آزمون منطقی مستقل و ترکیب ۴۷۷ سه‌تایی سازگار','۲۰ آشکارساز، اعتبارسنجی جامع و مرور انسانی')}
for task in checkpoint['tasks']:
 if task['id'] in updates:task['current_extension'],task['remaining_fa']=updates[task['id']]
 if task['id']=='N05':task['task_fa']='حفظ و طراحی چهار انتالوژی کوچک هدفمند';task['status']='RETENTION_DIRECTION_ACCEPTED_MODELS_PENDING_REVIEW'
checkpoint['prior_summary']=checkpoint.pop('summary');checkpoint['summary']=summary
checkpoint['timezone']='Etc/UTC'
checkpoint['next_steps_in_order']=[
 'Obtain independent real RM review, BA agreement and DS deployment witnesses; preserve documentary versus operational evidence.',
 'Adjudicate relation stereotypes/cardinalities and C/PROV/RG-07; acceptance of retention does not accept these details.',
 'Extend PV from versioned source-label scope to reviewed chemical identity and an ICSR contract; obtain real ESMP action evidence.',
 'Resolve CI evidence and #307; complete establishment/approval source contracts.',
 'After semantic adjudication align native/OWL/SHACL, execute full detectors and human G3 review, then update manuscript/Wiki/Pages, diagrams and release.']
for task in checkpoint['tasks']:
 if task['id']=='N05':task['deliverable_fa']='چهار قرارداد هدف، روابط، وابستگی‌ها و آزمون مستقل؛ حفظ دامنه‌ها پذیرفته شده و جزئیات مدل باز است.'
checkpoint['reporting_rule_fa']=checkpoint['reporting_rule_fa'].replace('\\u200c','‌')
dump('continuation-checkpoint.json',checkpoint)
report='''# گزارش پیشرفت — چهار انتالوژی کوچک هدفمند

**تصمیم جاری: حفظ هر چهار دامنه و توسعهٔ مستقل آن‌ها پذیرفته شد.** این تأیید، جایگزین حالت تعلیق تصمیم خروج/انتقال در جهت طراحی است؛ پذیرش همهٔ جزئیات روابط یا انتشار نیست. اجرای کار با دستیار است و لازم نیست کار فنی از ابتدا به کاربر منتقل شود.

چهار بستهٔ مستقل با هدف، ورودی/خروجی، مفاهیم هسته، وابستگی‌های مشخص، پرسش‌های کاربردی و نمونه‌های مثبت/منفی ساخته شد. هر بسته از پوشه‌ای موقت خارج از مخزن اجرا شد. اجزای مشترک واردشده به شمار مفاهیم اختصاصی دامنه افزوده نشده‌اند.

| دامنه | هدف عملی | کلاس اختصاصی / رابط واردشده | آزمون داده | پرس‌وجو | آزمون منطقی |
|---|---|---|---|---|---|
| RM | سناریو، ارزیابی، برنامه، اجرای مستقل و بازبینی ریسک دارویی | ۴ / ۸ | ۱۴/۱۴ | ۴/۴ | ۳/۳ |
| PV | شاهد ایمنی، سیگنال، نتیجه و محدودهٔ نسخه‌دار گروه مواد | ۴ / ۸ | ۳۵/۳۵ | ۹/۹ | ۵/۵ |
| BA | خدمت و قابلیت دارویی، نمای تحلیلی و تعهد همکاری | ۵ / ۱۱ | ۱۷/۱۷ | ۵/۵ | ۳/۳ |
| DS | جزء سامانه، استقرار/نسخه و منشأ دادهٔ عملیات دارویی | ۲ / ۲۹ | ۱۷/۱۷ | ۵/۵ | ۳/۳ |

وابستگی بیشتر DS عمدتاً از بستهٔ PROV می‌آید؛ هستهٔ دوکلاسه به‌تنهایی «۲۹ کلاس متعلق به DS» محسوب نمی‌شود. کوچک‌بودن باید با کارکرد مشخص و وابستگی روشن سنجیده شود، نه با افزایش صوری تعداد کلاس.

۸۳/۸۳ آزمون داده، ۲۳/۲۳ پرس‌وجو و ۱۴/۱۴ انتظار منطقی در اجرای مستقل موفق بود. ۱۵/۱۵ آزمون بررسی محدودهٔ مواد نیز موفق بود. نتیجهٔ همان ۸۳ آزمون داده با مدل کامل مقایسه و برابر شد. گراف مشترک مثبت شامل ۴۷۷ سه‌تایی در هر دو پیکربندی مستقل/کامل پذیرفته و با HermiT سازگار بود. ۷۲ آزمون داده و ۲۰ پرس‌وجو بازاجرای آزمون‌های قبلی‌اند و شواهد تجربی تازه محسوب نمی‌شوند.

## دستاورد PV

پاورقی ۴ صفحهٔ ۶ سند EMA/PRAC/183502/2026 پس از رفع خطای موقت ۴۲۹ بازخوانی شد. ۲۸ مدخل به‌صورت نام‌های مستند در یک محدودهٔ وابسته به نسخه ذخیره شد. نام ترکیب، نام ساده و نام مقید به فرمولاسیون تفکیک شد. هیچ گروهی به‌اجبار یک PharmaceuticalSubstance نشد. پیوند سیگنال به این محدوده تفسیر پیشنهادی است و با ادعای استخراج‌شده از سند یکسان نیست.

در آزمون اولیه مشخص شد مدل، یکی‌شدن توصیف محدوده با سند حامل را منع نمی‌کند. قید محدود به این واژگان و آزمون‌های مثبت/منفی اضافه شد. شکست اولیه محفوظ است. بررسی عددی مقدار/مسیر فقط تحت نگاشت پیشنهادی و با مبنای مقدار صریح انجام می‌شود؛ مقدار مجهول یا واحد نامعلوم نتیجهٔ نامعلوم دارد. این مدل دربارهٔ هویت شیمیایی نهایی، دوز بیمار یا انطباق حقوقی حکم نمی‌دهد.

## منزوی‌ها و انسجام

صفر منزوی و یک مؤلفه در کپی آزمایشی قبلی برقرار بود؛ این اجرا دوباره آن دستاورد را محاسبه نمی‌کند و native را تغییر نداد. هسته‌های چهار دامنه پیش از رفع چهار منزوی باقیمانده هم صفر منزوی داشتند. اکنون استقلال اجرایی و حفظ رفتار در آزمون‌های مشخص اثبات قوی‌تری دارد، اما انسجام معنایی کامل همچنان نیازمند داوری و شاهد واقعی است.

## جایگاه و درصد پیشرفت

- بسته‌های مستقل قابل اجرا و آزموده‌شده: **۴/۴ = ۱۰۰٪ این خروجی محدود**؛ این درصدِ تکمیل علمی چهار دامنه نیست.
- تصمیم جهت حفظ چهار دامنه: **یک تصمیم پذیرفته‌شده**؛ جزئیات مدل‌ها باز است.
- دروازه‌های تاریخی پروژه: **۲/۵ = ۴۰٪**؛ بدون تغییر.
- بسته‌های اصلی G3: **۲/۷ = ۲۸٫۶٪**؛ بدون تغییر.
- اجرای معتبر هر ۲۰ آشکارساز روی کل candidate: **۰/۲۰**.
- درصد کلی وزنی پروژه هنوز تعریف نشده؛ درصد ساختگی ارائه نمی‌شود.

## گام بعدی

۱. گردآوری و نگاشت شاهد عملیاتی مستقل برای بازبینی ریسک RM، قرارداد خدمت/تعهد BA و استقرار/مسئولیت DS؛ راهنما به‌تنهایی وقوع واقعی را اثبات نمی‌کند.
۲. پروندهٔ تصمیم رابطه‌به‌رابطه برای ۱۰ پیشنهاد قبلی و صف C/PROV/RG-07؛ تفکیک کران عمومی از الزام پروفایل داده.
۳. تکمیل مرز ICSR/هویت مواد در PV و شواهد اقدام واقعی ESMP؛ قرارداد ثبت مؤسسه و مدرک مستقل مجوز.
۴. تعیین تکلیف ۱۱ سررابطهٔ بی‌نوع، ۶۶ کران نامعلوم، ۱۴ تخصص و ۸۹ رابطهٔ بدون stereotype در کپی فعلی؛ اجرای معتبر ۲۰ آشکارساز و مرور انسانی G3.
۵. همگامی نسخهٔ مصوب با native/OWL/SHACL، مقاله، ویکی، Pages و دیاگرام‌ها؛ سپس ممیزی انتشار.

PR #305 همچنان draft است و merge نشد. ۳۰ ایشو باز و ۱۷۰ بسته بازبینی شد؛ هیچ ایشویی در این اجرا بسته نشد. CI آخرین head بررسی‌شده ۲۲ شکست داشت. دو job بررسی‌شده مرحله و runner ثبت‌شده نداشتند؛ علت قطعی از دسترسی موجود قابل اثبات نبود. موفقیت آزمون‌های محلی به معنی رفع CI نیست.

## حدود ادعا

این بسته‌ها برش رابطِ مبتنی بر امضای انتخاب‌شده‌اند؛ اثبات استخراج ماژول locality یا حفظ همهٔ استنتاج‌ها ارائه نشده است. حذف‌های مرزی در omissions.json ثبت شده‌اند. بازنمایی native مستقل، صحت جامع UFO/OntoUML، انطباق کامل OWL2 DL یا پذیرش معنایی نهایی ادعا نشده است. نتایج بستهٔ PV با آزمون‌های گروه مواد هم‌پوشانی دارند و برای ساخت درصد بیشتر جمع زده نمی‌شوند.

منابع: [سند رسمی PRAC](https://www.ema.europa.eu/en/documents/prac-recommendation/prac-recommendations-signals-adopted-31-august-3-september-2026-prac-meeting_en.pdf)، [OWL 2، ساختار و imports](https://www.w3.org/TR/owl2-syntax/#Imports). هش PDF از بازیابی قبلی نگه داشته شد؛ این نوبت متن دوباره خوانده شد ولی هش بایت‌ها دوباره محاسبه نشد.
'''
(H/'decision-report-fa.md').write_text(report)
work='# وضعیت کامل ۲۳ کار — پس از بسته‌های مستقل\n\nدر G3 هستیم. هیچ‌یک از ۲۳ بستهٔ اصلی کاملاً بسته نشده؛ جهت حفظ چهار دامنه پذیرفته شده و زیرکارهای آزموده‌شده در جدول مشخص‌اند.\n\n| شناسه | کار | انجام‌شده / آخرین دستاورد | باقی‌مانده |\n|---|---|---|---|\n'
for t in checkpoint['tasks']:work+='| '+t['id']+' | '+t['task_fa']+' | '+t.get('current_extension','کار قبلی محفوظ؛ پذیرش نهایی باز')+' | '+t.get('remaining_fa',t.get('deliverable_fa','پذیرش نهایی'))+' |\n'
evidence=read('repository-evidence.json');work+='\n## همهٔ ۳۰ ایشوی باز\n\n| ایشو | عنوان |\n|---|---|\n'
for issue in evidence['open_issues']:work+='| [#'+str(issue['number'])+']('+issue['url']+') | '+issue['title']+' |\n'
work+='\n## شاخص‌ها\n\n۴/۴ بستهٔ مستقل آزموده‌شده؛ ۲/۵ دروازهٔ تاریخی؛ ۲/۷ بستهٔ اصلی G3؛ ۰/۲۰ اجرای کامل آشکارسازها. درصد کلی وزنی تعریف نشده است. ۳۰ ایشو باز، ۱۷۰ بسته و صفر بسته‌شده در این نوبت. برای حدود ادعا و گام بعدی decision-report-fa.md را ببینید.\n'
(H/'work-status-fa.md').write_text(work)
(H/'README.md').write_text('''# CM-PharmE — purposeful standalone module contracts

User direction: retain Risk Management, Pharmacovigilance, Business Architecture and Digital Systems as purposeful small ontologies. Detailed scientific acceptance and release remain pending.

Read decision-report-fa.md and work-status-fa.md for the current decision, measured progress and complete work queue. Each modules/RM, PV, BA, DS directory is independently runnable and includes a purpose contract, owned versus imported vocabulary, flattened OWL, opt-in SHACL, fixed queries, fixtures and results.

Rebuild from the repository with the pinned Python requirements and Java 17:

```sh
python build_pv_group.py
python build_modules.py
python run_standalone.py
python run_integration.py
python finalize.py
```

Rebuild scripts read earlier immutable experiment packages. Exported module runners read only their own directory. Initial extraction failure (named property shapes omitted) and initial PV failure (scope/carrier identity not excluded) are retained with final passing results.

This is a bounded signature projection and fixture comparison, not formal locality extraction or complete logical equivalence. Native OntoUML remains unchanged; no gate or issue is closed. Do not sum overlapping PV checks as independent empirical evidence.
''')
# Preserve literal whitespace from imported PROV comments. If Turtle's long
# literal layout triggers whitespace checks, use N-Triples (also valid Turtle)
# rather than trimming the literal content. Verify RDF graph identity.
from rdflib import Graph
from rdflib.compare import isomorphic
for path in H.rglob('*.ttl'):
 original=Graph().parse(path);text=path.read_text()
 if any(line.endswith((' ','\t')) for line in text.splitlines()):text=original.serialize(format='nt')
 text=text.rstrip()+'\n';assert isomorphic(original,Graph().parse(data=text,format='turtle'));path.write_text(text)
for path in H.rglob('*.trig'):path.write_text(path.read_text().rstrip()+'\n')
manifest=[{'path':str(p.relative_to(H)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(H.rglob('*')) if p.is_file() and p.name!='file-manifest.json' and '__pycache__' not in p.parts]
dump('file-manifest.json',{'files':manifest,'count':len(manifest)})
print(json.dumps({'counts':counts,'files':len(manifest)+1,'all_tasks':len(checkpoint['tasks'])}),flush=True)
