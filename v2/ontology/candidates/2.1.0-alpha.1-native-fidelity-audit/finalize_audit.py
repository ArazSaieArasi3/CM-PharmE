"""Build the bounded evidence report and retain the complete 23-item backlog."""
import hashlib,json
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent
def load(name):return json.loads((H/name).read_text())
def write(name,value):(H/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
a=load('actual-specialization-results.json');r=load('native-roundtrip-results.json')
s=load('rule-sensitivity.json');g=load('readonly-guard-results.json');o=load('owl-alignment-results.json');issues=load('open-issues.json')
assert a['actual_specialized_ends']==14 and a['fully_resolved_specializations']==0
assert r['source_elements']==656 and r['readonly_unknown_to_false']==82 and r['guarded_roundtrip_canonical_equal']
assert s['pass']==s['total']==21 and g['pass']==g['total']==4 and r['refusal_pass']==r['refusal_total']==10
assert g['official_parser_pass']==g['official_parser_total']==3 and o['pass']==o['total']==7
assert a['source_sha256']==r['source_sha256']==o['native_sha256']
summary={
 'status':'BOUNDED_NATIVE_AUDIT_COMPLETE_SEMANTIC_GATES_OPEN',
 'date':'2026-10-09','timezone':'Asia/Tehran','prior_head':'bf7e764059eb8f5822017fa067ca17cdc87a0a8c',
 'actual_specialized_ends_audited':14,'actual_specialized_ends_total':14,
 'real_end_audit_coverage_previous_percent':0,'real_end_audit_coverage_percent':100,
 'fully_resolved_specialized_ends':0,'type_conformance_known_pass':10,'type_conformance_unknown':4,
 'context_conformance_known_pass':10,'context_conformance_unknown':4,'upper_bound_unknown_rows':14,
 'real_fragments_examined':7,'real_fragments_legacy_refused':7,
 'owl_declared_specialization_alignment_pass':7,'owl_declared_specialization_alignment_total':7,
 'unknown_readonly_fields':82,'affected_relations':41,'affected_mediations':3,
 'native_roundtrip_elements':656,'events_preserved':13,'situations_preserved':2,'nature_fields_preserved':147,'notes_preserved':25,
 'raw_roundtrip_exact':False,'raw_roundtrip_changes':775,'date_lexical_normalizations':692,'omitted_explicit_null_project_fields':1,
 'guarded_roundtrip_value_equal':True,'rule_cases_pass':21,'rule_cases_total':21,
 'roundtrip_refusal_guards_pass':10,'roundtrip_refusal_guards_total':10,
 'readonly_adapter_controls_pass':4,'readonly_adapter_controls_total':4,
 'legacy_readonly_parser_controls_pass':3,'legacy_readonly_parser_controls_total':3,
 'source_policy_disagreement_families_still_open':4,'source_policy_acceptances':0,
 'basic_legacy_family_sensitivity':'20/20 = 100% (previous immutable package)',
 'full_candidate_detector_runs':0,'full_candidate_detector_target':20,
 'historical_major_gates':'2/5 = 40%','historical_g3_packages':'2/7 = 28.6%',
 'open_issues':issues['count'],'closed_issues':issues['closed_count'],'created_this_execution':0,'closed_this_execution':0,
 'baseline_or_candidate_ontology_modified':False,'official_library_or_archive_modified':False,
 'scientific_gate_closed':False,'pr':305,'pr_state':'open draft','four_domain_removal_or_transfer_finalized':False,
 'limits':[
 'Native serialization preservation is not semantic validation of Event/Situation/nature.',
 'Subsetting checks are bounded native checks, not the official complete UML validator.',
 'All 14 actual specialization rows remain UNKNOWN overall; none approved by test count.',
 'Official in-memory parser still coerces null readOnly; guarded export uses original JSON to restore it.',
 'Four previous detector/source discrepancies remain in #315; serialization drift tracked under #310.',
 'Unchanged OWL/SHACL/HermiT packages were not rerun; only seven-pair axiom alignment was newly checked.',
 'CI evidence is for the explicitly pinned prior head; it is not a success claim for this future commit.'
 ]}
write('summary.json',summary)
old=load('../2.1.0-alpha.1-detector-calibration/continuation-checkpoint.json')
old.update(title='CM-PharmE v2.1 — actual specialization audit and native serialization fidelity',
 previous_checkpoint='../2.1.0-alpha.1-detector-calibration/continuation-checkpoint.json',
 prior_development_head=summary['prior_head'],summary=summary)
updates={
 'P5d':'14/14 ACTUAL ENDS AUDITED: 10 TYPE/CONTEXT PASS, 4 UNKNOWN; ALL 14 UPPER BOUNDS UNKNOWN; 7/7 OWL AXIOM PAIRS ALIGN; NO SEMANTIC ACCEPTANCE',
 'P5c':'NATIVE SERIALIZATION PRESERVES 15 EVENT/SITUATION, 147 NATURE AND 25 NOTES; 82 NULL READONLY COERCIONS GUARDED; FULL SEMANTIC ROUTE REMAINS OPEN',
 'P5e':'BASIC LEGACY SENSITIVITY 20/20; #315 FOUR DIFFERENCES OPEN; REAL FULL CANDIDATE 0/20',
 'P6b':'NEW READONLY LOSS COUNTEREXAMPLE REPRODUCED AND GUARDED; 21 RULE CASES + 10 EXPORT GUARDS + 4 ADAPTER CONTROLS + 3 LEGACY PARSER CONTROLS',
 'P4':'7 ACTUAL SPECIALIZATION PAIRS MATCH OWL AXIOMS; TWO EARLIER EXPERIMENTAL ABOUTNESS ALIGNMENTS AND FULL INTEGRATION REMAIN OPEN'}
for task in old['tasks']:
 if task['id'] in updates:task['status']=updates[task['id']]
assert len(old['tasks'])==23
old['remaining_full_candidate_blockers'].update(specialized_ends_unvalidated_on_actual_candidate=0,
 specialized_ends_audited_but_semantically_unresolved=14,unknown_readonly_ends=82)
old['next_steps_in_order']=[
 'Review the seven actual relation cards: decide six missing specialized mediation multiplicities, their readOnly flags, and the three shared broad parent target/bound policies.',
 'Choose the governing source-policy profile for the four #315 differences, keeping official engine observations intact.',
 'Specify and test Event/Situation identity, participation and temporal constraints on native/OWL representations; scientific acceptance is required before replacing the full-legacy gate with a combined route.',
 'Continue independent atomic requirements, all-domain ownership, registry/regulatory boundaries and scenario coverage; preserve every prior task.',
 'Obtain an actionable W6 diagnostic and successful database pipeline evidence; prior-head steps still empty.',
 'Integrate accepted deltas, run complete validation and human review, then align article/Wiki/Pages and prepare stable diagram/release.'
]
old['source_review_update']={'prior_primary_source_review':'Sales 2014 Tables 38/44/46/51 retained; four differences still open',
 'new_source':'OMG UML 2.5.1 Property subsetting rules and Eclipse UML2 Property API',
 'new_input_risk':'82 readOnly nulls defaulted by installed native parser; no new detector discrepancy is claimed',
 'author_acceptance':False}
write('continuation-checkpoint.json',old)

previous=(H.parent/'2.1.0-alpha.1-detector-calibration/work-status-fa.md').read_text()
table=previous.split('| شناسه |')[1].split('\n## دستاورد')[0]
table='| شناسه |'+table
lines=table.splitlines()
changes={
 'P4':('تطابق هفت رابطهٔ تخصص‌یافته با OWL بررسی و تأیید ساختاری شد','اعمال تصمیم‌های مصوب و هم‌ترازی کامل native/OWL/SHACL؛ دو aboutness آزمایشی نیز باز'),
 'P5d':('هر ۱۴ سر واقعی و هفت قطعه بررسی شد؛ ۱۰ انطباق نوع/زمینه و چهار نامشخص','۱۱ سر بی‌نوع، ۶۶ کاردینالیتی نامشخص، ۱۴ تخصص هنوز حل‌نشده و سیاست readOnly'),
 'P5c':('حفظ ۱۵ Event/Situation، ۱۴۷ nature و ۲۵ Note؛ نگهبان ۸۲ null ساخته و آزموده شد','اعتبارسنجی معنایی رخداد/وضعیت و تصویب مسیر ترکیبی؛ وفاداری serialization کافی نیست'),
 'P6b':('نقص حفظ null کشف شد؛ ۲۱ آزمون قواعد، ۱۰ guard خروجی، چهار کنترل adapter و سه کنترل parser موفق','اصلاح‌های معنایی پس از داوری؛ پذیرش علمی از موفقیت آزمون استنتاج نشود')}
for i,line in enumerate(lines):
 parts=[p.strip() for p in line.split('|')]
 if len(parts)>4 and parts[1] in changes:
  parts[3],parts[4]=changes[parts[1]];lines[i]='| '+' | '.join(parts[1:-1])+' |'
all_issues='| ایشو | عنوان | وضعیت |\n|---|---|---|\n'+'\n'.join(f"| [#{x['number']}]({x['url']}) | {x['title']} | باز |" for x in issues['issues'])
progress='''| شاخص | قبل | اکنون | تغییر |
|---|---:|---:|---:|
| پوشش بررسی مستقیم ۱۴ سر واقعی | ۰/۱۴ = ۰٪ | ۱۴/۱۴ = ۱۰۰٪ | +۱۰۰ واحد درصد |
| تخصص سررابطهٔ کاملاً تعیین‌تکلیف‌شده | ۰/۱۴ | ۰/۱۴ | صفر |
| حساسیت پایهٔ خانواده‌های موتور قدیمی | ۲۰/۲۰ = ۱۰۰٪ | ۲۰/۲۰ = ۱۰۰٪ | صفر |
| اجرای معتبر ۲۰ آشکارساز روی کل مدل | ۰/۲۰ | ۰/۲۰ | صفر |
| دروازه‌های اصلی تاریخی بسته | ۲/۵ = ۴۰٪ | ۲/۵ = ۴۰٪ | صفر |
| بسته‌های اصلی G3 بسته | ۲/۷ = ۲۸٫۶٪ | ۲/۷ = ۲۸٫۶٪ | صفر |

این شاخص‌ها مخرج‌های متفاوت دارند؛ هیچ‌کدام درصد کیفیت علمی کل پروژه نیست. ۳۰ ایشوی باز، ۱۷۰ بسته؛ در این اجرا صفر ایجاد و صفر بسته شد. تمام ۲۳ بند برنامه هنوز کار باقی‌مانده دارند.'''
status='''# وضعیت کامل CM-PharmE v2.1

۲۰۲۶-۱۰-۰۹، Asia/Tehran — ادامه از bf7e764. این گزارش تمام ۲۳ بند قبلی و تمام ایشوهای باز را نگه می‌دارد. تصمیم خروج/انتقال چهار دامنه متوقف است؛ PR305 پیش‌نویس است.

'''+ '\n'.join(lines) + '\n\n## پیشرفت\n\n'+progress+'\n\n## تمام ایشوهای باز\n\n'+all_issues+'''

## اکنون کجا هستیم و گام بعدی

در G3، بین آماده‌سازی شواهد P5 و پذیرش علمی P3/P4 هستیم. بررسی واقعیِ سررابطه‌ها و مهار افت داده انجام شده، اما پذیرش مدل و تبدیل کامل انجام نشده است. کارت‌های هفت رابطه در `decision-cards-fa.md` تصمیم بعدی را مشخص می‌کنند؛ مسیر حفظ معنا و چهار اختلاف منبع در `validation-route-fa.md` آمده است.

گام بعدی: تعیین سیاستِ شش سر تخصص‌یافتهٔ mediation و readOnly آن‌ها، و نوع/کران سه والدِ مشترک گسترده؛ سپس اعمال مصوبات در candidate جدید. هم‌زمان، تکمیل نیازمندی‌های مستقل همهٔ دامنه‌ها و قرارداد هویت/زمان Event/Situation قابل ادامه است. بعد از تعیین منبع حاکم #315 و رفع مانع W6، اعتبارسنجی یکپارچه و مرور انسانی انجام می‌شود. از موفقیت آزمون‌های محدود برای بستن gate استفاده نشده است.

W6 در head مبنا bf7e764 با run 37971912118 و job 113960399377 شکست خورده و پاسخ مراحل خالی است؛ علت قطعی هنوز در دسترس نیست. نتیجهٔ موفق PostgreSQL یا CI ادعا نمی‌شود.
'''
(H/'work-status-fa.md').write_text(status)
readme='''# ممیزی بومیِ روابط واقعی و حفظ اطلاعات

نتیجه: بررسی مستقیم هر ۱۴ سرِ دارای subsetting انجام شد و یک افت اطلاعات قابل بازتولید در parser/serializer شناسایی و با wrapper مهار شد. انتالوژی مبنا، نامزد آزمایشی و کتابخانه‌های رسمی تغییر نکردند؛ این نتیجه پذیرش علمی مدل نیست.

## شواهد همین اجرا

- ۱۴/۱۴ ارجاع معتبر؛ ۱۰/۱۴ انطباق نوع و ۱۰/۱۴ انطباق زمینه برقرار، چهار مورد در هر کدام نامشخص. هر ۱۴ بررسی سقف کاردینالیتی UNKNOWN است. هر هفت قطعهٔ واقعی بدون حدس‌زدن داده‌ها از تبدیل legacy بازماندند.
- جهتِ دو سر، domain/range و subPropertyOf هفت رابطه در OWL با ارجاع بومی متناظر است: ۷/۷. هیچ ادعای هم‌ارزی کاردینالیتی یا منطق کامل از این بررسی به دست نمی‌آید.
- schema/parser رسمی روی کل ۶۵۶ عنصر اجرا شد؛ ۱۳ Event، دو Situation، ۱۴۷ nature و متن هر ۲۵ Note حفظ شد. این حفظِ مقدارهاست و اعتبار معنایی آن‌ها را ثابت نمی‌کند.
- round-trip خام ۷۷۵ تغییر ثبت کرد: ۶۹۲ نرمال‌سازی نوشتاری تاریخ، حذف یک مقدار null متادیتای پروژه، و تبدیل **۸۲ readOnly نامشخص به false** در ۴۱ رابطه. این خروجی نباید بی‌قید جایگزین اصل ورودی شود.
- نگهبان، با نگه‌داشتن گزارش اختلاف و بازگردانی فقط تغییرهای شناخته‌شده از اصل ورودی، برابری همهٔ مقدارهای JSON را برقرار کرد. هر ۱۰ تغییر نامجازِ آزمایشی را رد کرد. خود شیء parser همچنان default دارد؛ تحلیل تصمیم باید JSON اصلی یا خروجی نگهبانی‌شده را بخواند.
- آداپتور سخت‌گیرانه‌تر null readOnly را رد می‌کند. چهار کنترل adapter و سه خوانش parser رسمی موفق بود؛ در یکی، تبدیل null به false توسط parser قدیمی مستقیماً بازتولید شد. ۲۱ شاهد قواعد محدود subsetting نیز نتیجهٔ از پیش تعیین‌شده را دادند.
- شکست اولیهٔ دو کنترل ناشی از سه null دیگرِ fixture بود؛ در `guard-initial-probe.json` حفظ شد. کنترل‌های مصنوعی با Booleanهای صریح ساخته شدند؛ دادهٔ واقعی یا قاعدهٔ رد برای سبزشدن عوض نشد.
- هفت کارت تصمیم و مسیر پیشنهادی اعتبارسنجی ترکیبی تهیه شد. چهار اختلاف #315 حل‌شده یا پذیرفته‌شده محسوب نمی‌شوند؛ هیچ gate یا issue بسته نشد.

## فایل‌های اصلی

- `actual-specialization-results.json`: هر ۱۴ سر، قواعد و موانع هفت قطعه؛ همهٔ annotationهای حذف‌شده از projection در manifest ذکر شده و اصل کامل حفظ است.
- `native-roundtrip-results.json`: ledger تمام تغییرها، hash ورودی و کتابخانه، آزمون‌های حفظ و رد.
- `owl-alignment-results.json`: تطابق هفت جفت واقعی با OWL.
- `readonly-guard-results.json`: ضدنمونهٔ افت null و کنترل‌های native/legacy.
- `decision-cards-fa.md`: تصمیم‌های دامنه‌ای پیشنهادی؛ هیچ کران جدید اعمال نشده است.
- `validation-route-fa.md`: حد ادعا، مسیر Event/Situation/nature و وابستگی #315 به ورودی معتبر.
- `work-status-fa.md` و `continuation-checkpoint.json`: همهٔ ۲۳ کار قبلی و ۳۰ ایشوی باز.

## بازتولید

از پوشهٔ این بسته، با وابستگی‌های نصب‌شدهٔ ثبت‌شده در JSON:

```bash
PYTHONDONTWRITEBYTECODE=1 python run_native_audit.py /path/to/node_modules
PYTHONDONTWRITEBYTECODE=1 python run_readonly_guard.py /path/to/pinned-oled /path/to/ecj-3.39.0.jar
/path/to/rdflib-python check_owl_alignment.py
python finalize_audit.py
```

آرشیو OLED باید دقیقاً commit `42b926f6c2859dc87e49a96b8482eae28d02e7d5` و بدون تغییر tracked باشد. ontouml-js 1.0.0 و schema 1.0.2 استفاده شد؛ hash باینری JS و schema در گزارش هست. ledger منبع اصلی و خروجی نگهبانی‌شده را از شیء تبدیل‌شده در حافظه تفکیک می‌کند. این بسته جایگزین اجرای کامل ۲۰ آشکارساز، تست دامنه، HermiT، SHACL، دادهٔ مستقل یا پذیرش انسانی نیست.

## پیشرفت

'''+progress+'''

جزئیات منبع قواعد در کارت‌های تصمیم آمده است. آمار CI مربوط به head مبناست، نه تأیید commit جدید؛ OWL/SHACL/HermiT قبلی چون فایل مدل تغییر نکرده دوباره اجرا نشدند.
'''
(H/'README-fa.md').write_text(readme)
manifest=[]
for file in sorted(H.iterdir()):
 if file.is_file() and file.name!='file-manifest.json':
  manifest.append({'file':file.name,'bytes':file.stat().st_size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
write('file-manifest.json',{'files':manifest,'count':len(manifest),'self_excluded':True})
print(json.dumps(summary,ensure_ascii=False))
