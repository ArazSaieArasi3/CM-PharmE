# وضعیت کامل CM-PharmE v2.1 — ادامه از bdc0a00

در G3 هستیم. این اجرا نگاشت PROV، سناریوهای دو والد و اولین شاهد واقعی NDC را جلو برد. هیچ‌یک از ۲۳ کار اصلی هنوز کاملاً بسته نشده است. PR305 پیش‌نویس است؛ خروج/انتقال چهار دامنه همچنان معلق است.

| شناسه | کار | انجام‌شده / وضعیت | باقی‌مانده |
|---|---|---|---|
| N01 | منشور هدف و مرز v2.1 | پیش‌نویس یا کار قبلی محفوظ؛ پذیرش باز | پاراگراف هدف، ذی‌نفعان، کاربردها، موارد خارج دامنه و حد ادعای جهانی |
| N02 | استخراج مستقل و اتمیک نیازمندی‌ها | ۱۶/۱۶ بند تطبیق داده شد؛ ۴۰ ردیف ورودی به ۳۹ عنوان کاری ردیابی شد | استخراج همهٔ دامنه‌ها و پذیرش علمی؛ ۳۹ عنوان صرفاً محدودهٔ این دو ورودی است |
| N03 | بازبینی مأموریت و مالکیت همهٔ دامنه‌ها | پیش‌نویس یا کار قبلی محفوظ؛ پذیرش باز | مأموریت هر دامنه، نگاشت همهٔ مفاهیم و وابستگی‌های بین‌دامنه‌ای |
| N04 | ماتریس پوشش جهانی و تحلیل شکاف | پیش‌نویس یا کار قبلی محفوظ؛ پذیرش باز | نیازمندی × سناریو × حوزه قضایی × منبع؛ وضعیت پشتیبانی/شکاف/خارج دامنه/تعویق |
| N05 | طراحی و ارزیابی حداقلی چهار دامنه با بازماندن تصمیم جایگاه نهایی | طرح حداقلی Risk Management و Digital Systems با PROV، سناریو و شاهد NDC تقویت شد؛ چهار دامنه حفظ‌اند | پذیرش طراحی و ارزیابی متوازن هر چهار دامنه؛ تصمیم جایگاه نهایی باز |
| N06 | تعیین حد رجیستری | پنج رکورد واقعی NDC به هفت شاهد بسته‌بندی با ردیابی کامل نگاشت شد | نمونهٔ متنوع‌تر، ثبت مؤسسه و شواهد مستقل مجوز؛ مدل کامل محصول باز |
| N07 | تقویت محدود Regulatory Policy | ۲۲ فیلد مثبت قبلی دسته‌بندی شد؛ زمینهٔ اعمال از متادیتای منبع جدا شد | مدل حداقلی زمینهٔ گزارش‌دهی و اعلان واقعی ESMP |
| N08 | تعیین تکلیف مفاهیم منزوی | پیش‌نویس یا کار قبلی محفوظ؛ پذیرش باز | تعیین تکلیف مستند هر ۱۳ منزوی فعلی؛ بررسی نیازمندی‌محور ۸ منزوی چهار دامنه بدون حذف پیش‌فرض. |
| N09 | طراحی سناریوها و مرجع پاسخ آزمون | هفت سناریوی مستقل برای دو والد؛ ۲۷ کنترل شواهد و ۲۵ آزمون منطقی موفق | سناریوهای دیگر دامنه‌ها و شاهد واقعی رخداد/ارزیابی ریسک |
| P3 | نهایی‌سازی تصمیم‌های علمی قبلی و جدید | هفت اصل PROV، تبدیل دو اعلان و گزینه‌های دامنهٔ هدف آمادهٔ داوری است | پذیرش پیشنهادها، C/readOnly، RG-07 و پرونده‌های علمی قبلی |
| P4 | اعمال تصمیم‌های مصوب در سه نمایش | نگاشت جهت‌دار هفت‌اصلی PROV با ۳۸ آزمون آماده؛ native دست‌نخورده | پذیرش و انتقال هماهنگ به native/OWL/SHACL؛ پل carrier/claim/fact |
| P5d | تکمیل نوع سررابطه‌ها، کاردینالیتی و subsetting | گزینهٔ محدودکردن دو والد به SupplyDependency با ضدنمونه رد شد؛ دو جهت child/parent آزموده شد | دامنهٔ هدف و کران جامع؛ ۱۱ نوع، ۶۶ کران و ۱۴ سررابطهٔ تخصصی هنوز باز |
| P5c | پوشش معتبر Event/Situation و nature | تفکیک رکورد/فعالیت در پروفایل PROV آزموده شد؛ قید تکراری در این پیکربندی شناخته شد | اعتبارسنجی جامع Event/Situation و nature؛ پذیرش علمی |
| P5e | اجرای الگوها و هر ۲۰ ضدالگو | ۱۲ آزمایش RelSpec؛ شش mutation بدشکل با خروجی صفر شناسایی شد | چهار اختلاف #315 و اجرای معتبر کل candidate همچنان ۰/۲۰ |
| P6a | نمونه‌سازی مصنوعی کوچک اما پوشش‌دار | ۷ سناریوی هدف، ۳۸ آزمون PROV و کنترل‌های مثبت/منفی دادهٔ واقعی آماده | پوشش متوازن کل پروژه؛ ۳۹ عنوان کاری قبلی هنوز پوشش جهانی نیست |
| P6b | چرخهٔ اصلاح براساس آزمون | تعارض اعلان PROV و استفادهٔ نادرست از helper با شناسهٔ ثابت شناسایی و اصلاح آزمایشی شد؛ شواهد اولیه محفوظ | داوری تبدیل PROV و قرارداد C؛ اصلاح‌های مصوب |
| P6c | قرارداد منبع و شواهد تجربی مستقل | دریافت مستقل پنج رکورد واقعی NDC موفق؛ checksum، زمان و JSON pointer ثبت شد | گسترش نمونه، ESMP، قرارداد #307 و علت شکست W6 |
| P6d | اعتبارسنجی یکپارچه و ریزنر | رگرسیون ۱۱۶/۱۱۶، HermiT ترکیب ۴۵ گراف مثبت و نمونهٔ واقعی قدیم/جدید موفق | پروفایل کامل OWL2 DL/قیود PROV و اعتبارسنجی native و انسانی؛ C جدا باز |
| N10 | تثبیت نهایی نیازمندی‌های آزموده‌شده v2.1 | پیش‌نویس یا کار قبلی محفوظ؛ پذیرش باز | ماتریس نیاز→CQ→مفهوم/رابطه/قید→تست→شاهد→تصمیم |
| P7 | مرور انسانی و بستن G3 | پیش‌نویس یا کار قبلی محفوظ؛ پذیرش باز | بستهٔ تصمیم و شواهد نسخهٔ نامزد پایدار |
| G4 | تطبیق داده، ردیابی، ویکی، Pages و مقاله | پیش‌نویس یا کار قبلی محفوظ؛ پذیرش باز | همگامی نگاشت‌ها و شواهد مستقل، ادعاها و مستندات/مقاله با نسخهٔ مصوب |
| G5a | دیاگرام جامع و مرور نهایی نسخهٔ پایدار | پیش‌نویس یا کار قبلی محفوظ؛ پذیرش باز | دیاگرام جامع OntoUML و نماهای دامنه‌ای پس از تثبیت |
| G5b | ممیزی انتشار و release v2.1 | پیش‌نویس یا کار قبلی محفوظ؛ پذیرش باز | چک‌لیست انتشار، نسخه‌بندی، تغییرات، مجوز، قابلیت بازتولید و آرشیو |

## درصدهای با مخرج مشخص

| شاخص | پیش از اجرا | اکنون | تغییر |
|---|---:|---:|---:|
| سه خروجی اجرایی همین نوبت: PROV، دو والد، اولین NDC | ۰/۳ | ۳/۳ = ۱۰۰٪ | +۱۰۰ واحد درصد در همین بسته |
| بررسی اولیهٔ فیلدهای مثبت قبلی | ۰/۲۲ | ۲۲/۲۲ = ۱۰۰٪ | +۱۰۰ واحد درصد؛ بدون پذیرش علمی |
| دروازه‌های اصلی تاریخی | ۲/۵ = ۴۰٪ | ۲/۵ = ۴۰٪ | صفر |
| بسته‌های اصلی G3 | ۲/۷ = ۲۸٫۶٪ | ۲/۷ = ۲۸٫۶٪ | صفر |
| اجرای معتبر ۲۰ آشکارساز روی کل candidate | ۰/۲۰ | ۰/۲۰ | صفر |

عدد ۱۰۰٪ مربوط به خروجی محدود همین اجراست، نه کل انتالوژی یا مقاله. درصد کلی وزنی پروژه تعریف و تصویب نشده؛ عددی برای آن ساخته نشده است.

## تمام ایشوهای باز

30 باز و 170 بسته؛ در این اجرا صفر ایجاد و صفر بسته شد.

| ایشو | عنوان |
|---|---|
| [#315](https://github.com/ArazSaieArasi3/CM-PharmE/issues/315) | [V2.1][P5e] Adjudicate four archived-detector/source discrepancies before full validation |
| [#314](https://github.com/ArazSaieArasi3/CM-PharmE/issues/314) | [V2.1][N05-DS] Design and test minimum viable Digital Systems module |
| [#312](https://github.com/ArazSaieArasi3/CM-PharmE/issues/312) | [V2.1][N05-PV] Design and test minimum viable Pharmacovigilance module |
| [#313](https://github.com/ArazSaieArasi3/CM-PharmE/issues/313) | [V2.1][N05-BA] Design and test minimum viable Business Architecture module |
| [#311](https://github.com/ArazSaieArasi3/CM-PharmE/issues/311) | [V2.1][N05-RM] Design and test minimum viable Risk Management module |
| [#310](https://github.com/ArazSaieArasi3/CM-PharmE/issues/310) | [V2.1][P5b] Bridge native OntoUML JSON to a verified full 20-antipattern detector |
| [#307](https://github.com/ArazSaieArasi3/CM-PharmE/issues/307) | [V2.1][Data] Reconcile NHIF P1 Zenodo file contract with published record |
| [#306](https://github.com/ArazSaieArasi3/CM-PharmE/issues/306) | [V2.1][OntoUML] Resolve pattern triggers and run native validation before release |
| [#244](https://github.com/ArazSaieArasi3/CM-PharmE/issues/244) | [WIKI-33] Final integration, republication and documentation-excellence acceptance audit |
| [#243](https://github.com/ArazSaieArasi3/CM-PharmE/issues/243) | [WIKI-32][BLOCKED][CROSS-REPO] Extract reusable Research/Ontology Documentation Profile into OGCM-RF |
| [#241](https://github.com/ArazSaieArasi3/CM-PharmE/issues/241) | [WIKI-30] Freeze quantitative and qualitative Wiki quality rubrics and perform before/after scoring |
| [#240](https://github.com/ArazSaieArasi3/CM-PharmE/issues/240) | [WIKI-29] Perform page-by-page editorial quality and natural technical prose review |
| [#239](https://github.com/ArazSaieArasi3/CM-PharmE/issues/239) | [WIKI-28] Add tutorials and reproducible how-to paths for using CM-PharmE |
| [#238](https://github.com/ArazSaieArasi3/CM-PharmE/issues/238) | [WIKI-27] Refactor evaluation, supported-claim and reproducibility documentation for readers |
| [#228](https://github.com/ArazSaieArasi3/CM-PharmE/issues/228) | [WIKI-17 EPIC] Elevate CM-PharmE Wiki to a reader-centered research and ontology documentation portal |
| [#214](https://github.com/ArazSaieArasi3/CM-PharmE/issues/214) | [WIKI-12][BLOCKED] Freeze final CM-PharmE 2.0 Wiki for manuscript/research release |
| [#213](https://github.com/ArazSaieArasi3/CM-PharmE/issues/213) | [WIKI-11][BLOCKED] Refresh V2 Wiki after human ontology review and semantic stabilization |
| [#212](https://github.com/ArazSaieArasi3/CM-PharmE/issues/212) | [WIKI-10][BLOCKED] Refresh V2 Wiki after W8 / Gate G stabilization |
| [#211](https://github.com/ArazSaieArasi3/CM-PharmE/issues/211) | [WIKI-09] Maintain CM-PharmE 2.0 as stable-to-date evolving documentation |
| [#202](https://github.com/ArazSaieArasi3/CM-PharmE/issues/202) | [WIKI EPIC] Build complete versioned CM-PharmE Wiki |
| [#173](https://github.com/ArazSaieArasi3/CM-PharmE/issues/173) | [V2][HORP Pilot] Instantiate human ontology review control layer |
| [#171](https://github.com/ArazSaieArasi3/CM-PharmE/issues/171) | [V2-PAPER] Build integrated CM-PharmE 2.0 Manuscript Draft 0 |
| [#170](https://github.com/ArazSaieArasi3/CM-PharmE/issues/170) | [V2-083][W8] Evaluate the demonstrator through representative tasks |
| [#159](https://github.com/ArazSaieArasi3/CM-PharmE/issues/159) | [V2][Human Review] Build concept provenance and V1→V2 evidence mapping matrix |
| [#103](https://github.com/ArazSaieArasi3/CM-PharmE/issues/103) | [W7 META] Prospective evaluation evidence register |
| [#98](https://github.com/ArazSaieArasi3/CM-PharmE/issues/98) | [V2-071][W7] Conduct prospective structured expert evaluation |
| [#24](https://github.com/ArazSaieArasi3/CM-PharmE/issues/24) | [V2 PROGRAM] CM-PharmE 2.0 research roadmap and decision gates |
| [#23](https://github.com/ArazSaieArasi3/CM-PharmE/issues/23) | [V2-PAPER EPIC] Co-develop the Q1/Q2 manuscript and reproducible research release |
| [#22](https://github.com/ArazSaieArasi3/CM-PharmE/issues/22) | [V2-W8 EPIC] Global Pharmaceutical Ecosystem Observatory and application demonstrators |
| [#21](https://github.com/ArazSaieArasi3/CM-PharmE/issues/21) | [V2-W7 EPIC] Prospective multi-family ontology evaluation |

## گام بعدی

- Build and test a minimum contextual reporting-applicability model and the record/claim/fact bridge, using the completed 22-field triage; keep metadata out of unnecessary native domain classes.
- Expand NDC sampling by explicit source strata and acquire a versioned real ESMP reporting action; retain package/product dates, source attribution and unknown approval separately.
- Prepare author adjudication of the seven PROV alignment axioms, two-declaration reasoning projection, target-policy alternatives, RG-07 and prior C/evidence contract. No generic continuation instruction counts as approval.
- After acceptance, integrate native/OWL/SHACL deltas, resolve the 11 untyped ends, 66 unknown cardinalities, 14 specialized ends, four isolates and four #315 discrepancies; run all 20 detectors on a supported full candidate.
- Resolve W6 and #307; complete all-domain requirements/ownership, independent evaluation and human G3 review; then align article/Wiki/Pages and stable diagrams and audit release.

W6 در head مبنای bdc0a00: run 37984390144 و job 114002601320، شکست با steps خالی و logs_url تهی. علت قطعی مشخص نشده؛ موفقیت محلی جایگزین CI نیست.
