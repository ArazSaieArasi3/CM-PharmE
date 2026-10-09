"""Preserve original tasks and make semantic decisions and remaining work inspectable."""
import json,hashlib,collections
from pathlib import Path
H=Path(__file__).resolve().parent;OLD=H.parent/'2.1.0-alpha.1-four-domain-lab'
def read(p):return json.loads(p.read_text())
def write(name,x):(H/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
for p in H.rglob('*.ttl'):p.write_text(p.read_text().rstrip()+'\n')
manifest=read(H/'model-manifest.json')
assert all(hashlib.sha256((OLD/name).read_bytes()).hexdigest()==sha for name,sha in manifest['old_package_sha256'].items())
groups={
 'content-aboutness':('Content refers to a domain entity. Preserve the Assertion/reality distinction; not a comparison of qualities.', 'specialize an existing aboutness relation where available', 'scenarioProduct signalProduct signalSubstance scenarioFacility scenarioDependency'),
 'content-reference':('An informational object references another content object; this is not their identity or a constitutive social dependency.', 'review content identity and local reference profile', 'planRiskResult pvResultSignal viewOrganization viewService carrierClaim agreementCommitment commitmentActor'),
 'event-content':('An occurrence has a content object as its topic/input/output. Event and content must retain distinct identity.', 'event participation/input/output policy in P5c', 'assessmentScenario resultAssessment reviewPriorResult reviewNewResult reportsRecord signalAssessmentTarget pvResultAssessment surveillanceRequirement surveillanceSource'),
 'evidence-citation':('A citation is recoverable provenance; it does not by itself instantiate qualified evidential support.', 'keep citation weak; reuse EvidenceSupport when support is actually asserted', 'citesSourceRecord'),
 'scoped-applicability':('A requirement is scoped to jurisdiction; the reference does not establish legal applicability or compliance.', 'document scope without a universal compliance rule', 'pvRequirementJurisdiction'),
 'service-specification':('A specification describes an offered service/context or supporting means; its existence does not imply actual execution.', 'retain specification/occurrence distinction and pharmaceutical context', 'serviceCapability digitalServiceComponent digitalServiceActivity serviceProduct serviceFacility'),
 'capability-manifestation':('A capability is intrinsic to its organization; actual realization is a distinct event and not required merely by possession.', 'manifestation/event modeling review; do not use characterization between Mode and event', 'capabilityRealizedIn'),
 'event-participation':('A component, organization, product or facility participates in or is context for an occurrence. No social relator is justified merely by this link.', 'typed event participation policy; preserve responsibility versus deployment distinction', 'deploymentComponent deploymentOrganization assessmentOrganization activityResponsibleOrganization manufacturingProduct manufacturingFacility'),
 'event-dependency':('Two occurrences are linked by use/support/plan enactment; temporal and intentional semantics need explicit review.', 'do not assume event mereology or causal necessity from an operational support link', 'digitalActivityDeployment supportsManufacturing implementsRiskPlan'),
 'record-generation':('A source carrier is produced in a transformation occurrence; representation and producing event remain distinct.', 'qualified PROV-compatible generation candidate; no automatic agent identity', 'recordDigitalActivity')
}
old=read(OLD/'model-manifest.json')['new_relations'];new=manifest['relations'];lookup={r['name']:r for r in old+new};trace=read(OLD/'requirement-traceability.json')['requirements']
rows=[]
for fam,(meaning,proposal,names) in groups.items():
 for name in names.split():
  assert name in lookup,name
  r=lookup[name];req=[q['id'] for q in trace if name in q['candidate_properties']]
  if r.get('requirement'):req.append(r['requirement'])
  if name=='surveillanceSource':req.append('X-PV-SURVEILLANCE')
  rows.append({'relation':name,'source':r['source'],'target':r['target'],'semantic_family':fam,'meaning':meaning,'recommended_next_decision':proposal,'requirement_ids':req,
   'stereotype_verdict':'PENDING — no forced generic formal/material/mediation label','current_universal_bounds':'0..* both ends; not an approved final multiplicity','local_bounds_location':'model-manifest.json profiles and original laboratory profiles','author_acceptance':False})
assert len(rows)==len(lookup)==39 and len({r['relation'] for r in rows})==39
assert all(r['requirement_ids'] for r in rows)
write('relation-semantic-review.json',{'status':'PROPOSALS_WITH_RATIONALE_NOT_APPROVAL','relations':rows,'families':dict(collections.Counter(r['semantic_family'] for r in rows)),
 'reused_native_mediations':['evidenceAssertion','evidenceRecord','partnershipParticipant'],'new_mediations_claimed':0,
 'sources':['https://ontouml.readthedocs.io/en/latest/relationships/formal/index.html','https://ontouml.readthedocs.io/en/latest/relationships/mediation/index.html','https://ontouml.readthedocs.io/en/latest/relationships/material/index.html'],
 'important':'Formal in the cited OntoUML documentation is comparative; arbitrary aboutness, provenance and event links must not receive that label merely to fill null stereotypes.'})
plan=read(OLD/'continuation-checkpoint.json');plan['title']='CM-PharmE v2.1 — checkpoint after eight four-domain refinements and P1 contract repair';plan['experiment']='v2/ontology/candidates/'+H.name
plan['execution_note']='Prior baseline and laboratory preserved. Eight gap-specific contracts implemented and tested; twelve associations and no classes added. P1 source contract repaired with bounded replay; GitHub W6 CI failed before any recorded step and full database execution remains unverified.'
for t in plan['tasks']:
 if t['id']=='N05':t['status']='FOUR_DOMAINS_RETAINED_FOR_REVIEW_EIGHT_GAPS_OPERATIONALIZED'
 if t['id']=='P3':t['current_extension']='39 experimental relations now have semantic-family/rationale review proposals; no final stereotype decisions. Prior 29-relation backlog preserved.'
 if t['id']=='P6c':t['current_extension']='P1 filename/metadata/header contract repaired; 12 negative checks and 768-row replay pass. Full W6 database CI failed before recorded steps; #307 stays open. Other empirical sources remain open.'
 if t['id']=='P6b':t['current_extension']='Eight original gap areas refined with 37 new SHACL cases plus all 39 prior cases passing.'
plan['exact_next']={'task':'P3/P5 semantic and representation alignment','items':['Review informational content/proposition profile boundaries against structural BinOver candidates; a complete report-content model is still absent.','Adjudicate 39 experimental relations with event/participation/nature policy; align native, OWL and SHACL.','Resolve W6 CI execution failure or run PostgreSQL/PostGIS in an available independent environment; close #307 only after acceptance.','Continue full 20-pattern adapter, independent data and P7 human evaluation.']}
plan['next_action_fa']='بررسی نتیجهٔ CI قرارداد منبع و سپس تعیین تکلیف هویت محتوای اطلاعاتی و سیاست روابط رخدادها برای هم‌ترازی سه نمایش.'
plan['progress_current']={'this_refinement_contracts':'8/8 have passing bounded tests; none author-accepted','original_requirement_trace_records':'24/24 preserved; no scientific closure inferred','closed_major_gates':'2/5 = 40% unchanged','closed_G3_packages':'2/7 = 28.6% unchanged','new_semantic_gates_closed':0}
plan['reporting_rule_fa']='در هر اجرا: دستاورد، کارهای انجام‌شده، فهرست تمام کارهای باز، شمار ایشوهای باز/بسته و بسته‌شدهٔ همان اجرا، گام مستقیم بعدی و درصد با مخرج روشن گزارش شود.'
write('continuation-checkpoint.json',plan)
statuses={
 'N01':('پیش‌نویس آماده','تأیید هدف و مرز نسخه'),
 'N02':('۲۴ نیازمندی نگاشت‌شده؛ ۸ اصلاح آزموده','تکمیل نیازمندی‌های همهٔ دامنه‌ها و پذیرش علمی'),
 'N03':('مأموریت چهار دامنه بررسی شده','مالکیت و مرز همهٔ دامنه‌ها'),
 'N04':('باز','ماتریس پوشش و شکاف در زمینه‌های مختلف'),
 'N05':('چهار نمونه و هشت اصلاح اجرا شده','هویت محتوا، داوری روابط و جایگاه نهایی دامنه‌ها'),
 'N06':('باز','مرز رجیستری و تفکیک داده/واقعیت/مجوز'),
 'N07':('قلمرو PV به‌صورت محدود آزموده','پوشش محدود و مستند Regulatory Policy'),
 'N08':('۱۳ منزوی در مبنا؛ ۴ در آزمایش قبلی','توجیه معنایی روابط و تعیین تکلیف چهار مفهوم باقی‌مانده'),
 'N09':('۱۶ خانوادهٔ قبلی و آزمون‌های هشت اصلاح اجرا شده','سناریوهای مستقل سایر دامنه‌ها'),
 'P3':('برای ۳۹ رابطهٔ آزمایشی دلیل و پیشنهاد ثبت شد','تصویب stereotype و کران‌ها؛ ادامهٔ پروندهٔ ۲۹ رابطهٔ قبلی'),
 'P4':('مدل اجرایی مستقل ساخته شد','اعمال تصمیم‌های مصوب و هم‌ترازی native/OWL/SHACL'),
 'P5d':('رابطه‌های آزمایشی دو سر نوع‌دار دارند','۱۱ سر بی‌نوع، ۶۶ کران نامشخص و ۱۴ سر تخصص‌یافتهٔ قبلی'),
 'P5c':('موانع رخداد و nature شناسایی شده','نگاشت معتبر به adapter و آزمون حفظ معنا'),
 'P5e':('پیش‌فیلتر اجرا؛ نمونهٔ BinOver قبلاً اجرا شده','اجرای کامل و معتبر هر ۲۰ ضدالگو'),
 'P6a':('نمونه‌های محدود چهار دامنه آماده و آزموده','پوشش متوازن همهٔ نیازمندی‌های پروژه'),
 'P6b':('هشت اصلاح و ۳۷ آزمون جدید؛ ۳۹ آزمون بازگشت موفق','چرخهٔ اصلاح بعد از داوری علمی و کشف موارد جدید'),
 'P6c':('قرارداد P1 اصلاح؛ ۱۲ آزمون منفی و تبدیل ۷۶۸ ردیف موفق','رفع مانع اجرای W6 CI؛ سایر منابع و دادهٔ مستقل'),
 'P6d':('۸ آزمون جدید HermiT و بازگشت نمونهٔ واقعی موفق','اعتبارسنجی کل نسخه پس از ادغام تصمیم‌ها'),
 'N10':('باز','تثبیت نیازمندی‌های آزموده و پذیرفته‌شده'),
 'P7':('باز','مرور انسانی و بستن G3'),
 'G4':('باز','هم‌ترازی داده، نگاشت، ویکی، Pages و مقاله'),
 'G5a':('باز','دیاگرام جامع نسخهٔ پایدار و مرور نهایی'),
 'G5b':('باز','ممیزی انتشار و release v2.1')}
lines=['# وضعیت کامل کارهای CM-PharmE v2.1','',
 '۲۰۲۶-۱۰-۰۹ — این جدول میان «اجرای فنی محدود» و «بسته‌شدن علمی کار» تفاوت می‌گذارد. برنامهٔ ۲۳‌بندی حذف یا کوتاه نشده است.','',
 '| شناسه | کار | انجام‌شده / وضعیت | باقی‌مانده |','|---|---|---|---|']
for t in plan['tasks']:
 done,left=statuses[t['id']];lines.append(f"| {t['id']} | {t['task_fa']} | {done} | {left} |")
lines+=['','## پیشرفت این اجرا','',
 'هشت اصلاح محدود: ۸/۸ دارای شاهد و آزمون مطابق انتظار؛ ۳۷/۳۷ SHACL جدید، ۳۹/۳۹ بازگشت قبلی، ۸/۸ پرسش، ۸/۸ HermiT. قرارداد منبع: ۱۲/۱۲ آزمون منفی، تبدیل ۷۶۸ ردیف و خروجی دقیقاً برابر قبلی.','',
 'دروازه‌های اصلی بسته‌شده: ۲/۵ = ۴۰٪؛ زیرگام‌های G3 بسته‌شده: ۲/۷ = ۲۸٫۶٪؛ هر دو بدون تغییر. این اعداد درصد کیفیت یا برآورد کل تلاش نیستند.','',
 'گام مستقیم بعدی: سیاست هویت محتوای اطلاعاتی و روابط رخدادها را برای P3/P5 تعیین تکلیف کنیم؛ هم‌زمان علت توقف CI را مشخص کنیم یا اجرای PostgreSQL/PostGIS را در محیط مناسب انجام دهیم. #307 تا آن زمان باز است.']
if (H/'open-issues.json').exists():
 snapshot=read(H/'open-issues.json');lines+=['','## تمام ایشوهای باز','',f"باز: {snapshot['open_count']}؛ بسته: {snapshot['closed_count']}؛ بسته‌شده در این اجرا: {snapshot['closed_this_run']}. PRها در این شمارش نیستند.",'','| ایشو | عنوان | وضعیت |','|---|---|---|']
 for issue in snapshot['open_issues']:
  num=issue['number'];lines.append(f"| [#{num}](https://github.com/ArazSaieArasi3/CM-PharmE/issues/{num}) | {issue['title']} | باز |")
(H/'work-status-fa.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'old_package_preserved':True,'relation_proposals':len(rows),'tasks_preserved':len(plan['tasks'])}))
