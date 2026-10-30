# وضعیت کامل CM-PharmE v2.1 — بستهٔ زمینهٔ گزارش‌دهی

در G3 هستیم. خروج/انتقال چهار دامنه معلق است. PR305 پیش‌نویس و مرور علمی باز است. این اجرا هیچ‌یک از ۲۳ کار اصلی را به‌طور کامل نبست.

| شناسه | کار | انجام‌شده | باقی‌مانده |
|---|---|---|---|
| N01 | منشور هدف و مرز v2.1 | کار قبلی محفوظ؛ پذیرش نهایی باز | پاراگراف هدف، ذی‌نفعان، کاربردها، موارد خارج دامنه و حد ادعای جهانی |
| N02 | استخراج مستقل و اتمیک نیازمندی‌ها | ۱۳ پالایش محلی CL/CTX با آزمون و پیوند به نیازهای قبلی ثبت شد؛ به ۳۹ عنوان قبلی جمع زده نشده است | استخراج مستقل تمام دامنه‌ها و پذیرش ماتریس جامع |
| N03 | بازبینی مأموریت و مالکیت همهٔ دامنه‌ها | کار قبلی محفوظ؛ پذیرش نهایی باز | مأموریت هر دامنه، نگاشت همهٔ مفاهیم و وابستگی‌های بین‌دامنه‌ای |
| N04 | ماتریس پوشش جهانی و تحلیل شکاف | کار قبلی محفوظ؛ پذیرش نهایی باز | نیازمندی × سناریو × حوزه قضایی × منبع؛ وضعیت پشتیبانی/شکاف/خارج دامنه/تعویق |
| N05 | طراحی و ارزیابی حداقلی چهار دامنه با بازماندن تصمیم جایگاه نهایی | پل رکورد/ادعا و زمینهٔ گزارش‌دهی، بخش اطلاعاتی طرح چهار دامنه را تقویت کرد؛ هر چهار دامنه حفظ‌اند | ارزیابی متوازن و پذیرش مأموریت/مرز هر چهار دامنه؛ PV و BA هنوز نیازمند تکمیل‌اند |
| N06 | تعیین حد رجیستری | ۱۵ رکورد NDC، ۱۹ بسته‌بندی، ۷۴ استخراج مستقیم و ۷۶ تفسیر پیشنهادی؛ ۷۲ کنترل موفق | شاهد ثبت مؤسسه، مدرک مستقل مجوز، داوری هویت و مسئولیت ثبت RG-07 |
| N07 | تقویت محدود Regulatory Policy | مدل حداقلی زمینه، پنج پروفایل راهنمای ESMP نسخهٔ ۱٫۴ و ۱۶ کنترل موفق | اعلان واقعی اقدام با دامنهٔ محصول، زمان و تناوب؛ دادهٔ واقعی گزارش‌دهی و پذیرش مدل |
| N08 | تعیین تکلیف مفاهیم منزوی | مدل پایه ۱۳ منزوی داشت؛ نمونهٔ اصلاح‌شده همچنان چهار منزوی دارد؛ این اجرا native را تغییر نداد | DistributionLogisticsActivity، ProcurementActivity، RegulatoryRequirement و StockoutSituation نیازمند تصمیم مستندند |
| N09 | طراحی سناریوها و مرجع پاسخ آزمون | آزمون‌های زمینه، تعارض ادعا و تمایز استخراج/تفسیر به خانواده‌های قبلی افزوده شد | سناریوهای مستقل سایر دامنه‌ها و دادهٔ واقعی ریسک/ایمنی |
| P3 | نهایی‌سازی تصمیم‌های علمی قبلی و جدید | پروندهٔ سه زیرکلاس توصیفی و سه عدم‌اشتراک پیشنهادی با حدود ادعا آماده شد | پذیرش پل ادعا، زمینه، PROV و تبدیل دو اعلان؛ RG-07 و C همچنان باز |
| P4 | اعمال تصمیم‌های مصوب در سه نمایش | سه زیرکلاس و قراردادهای OWL/SHACL در بستهٔ آزمایشی جدا پیاده شد؛ native تغییر نکرد | پذیرش و یکپارچه‌سازی هماهنگ native/OWL/SHACL |
| P5d | تکمیل نوع سررابطه‌ها، کاردینالیتی و subsetting | گزینهٔ محدودکردن دو والد به SupplyDependency با ضدنمونه رد شد؛ دو جهت child/parent آزموده شد | دامنهٔ هدف و کران جامع؛ ۱۱ نوع، ۶۶ کران و ۱۴ سررابطهٔ تخصصی هنوز باز |
| P5c | پوشش معتبر Event/Situation و nature | تفکیک رکورد/فعالیت در پروفایل PROV آزموده شد؛ قید تکراری در این پیکربندی شناخته شد | اعتبارسنجی جامع Event/Situation و nature؛ پذیرش علمی |
| P5e | اجرای الگوها و هر ۲۰ ضدالگو | ۱۲ آزمایش RelSpec؛ شش mutation بدشکل با خروجی صفر شناسایی شد | چهار اختلاف #315 و اجرای معتبر کل candidate همچنان ۰/۲۰ |
| P6a | نمونه‌سازی مصنوعی کوچک اما پوشش‌دار | ۴۳ پرس‌وجو، ۱۴ آزمون SHACL و ۱۲ آزمون منطقی موفق؛ شاهدهای ناموفق مورد انتظار محفوظ | پوشش متوازن کل دامنه‌ها و سناریوهای خارج از نمونهٔ حاضر |
| P6b | چرخهٔ اصلاح براساس آزمون | نوع تاریخ ناسازگار با HermiT اصلاح شد؛ رشتهٔ اصلی حفظ و تاریخ جدا اعتبارسنجی شد؛ منشأ تفسیر/استخراج صریح شد | قرارداد C، تبدیل PROV و اصلاح‌های نیازمند پذیرش علمی |
| P6c | قرارداد منبع و شواهد تجربی مستقل | ۱۰ رکورد NDC جدید نسبت به نمونهٔ قبلی؛ راهنمای رسمی ESMP منبع‌دار؛ خطاهای دریافت اولیه محفوظ | اعلان/گزارش عملیاتی ESMP، ثبت مؤسسه/مجوز، قرارداد #307 و علت قطعی W6 |
| P6d | اعتبارسنجی یکپارچه و ریزنر | رگرسیون ۱۱۶/۱۱۶، ترکیب ۴۵ گراف مثبت با دادهٔ جدید و بازآزمایی ۷۶۸ رکورد قبلی موفق | اعتبارسنجی کامل native/UFO و OWL2 DL، آشکارسازهای ۲۰گانه و مرور انسانی |
| N10 | تثبیت نهایی نیازمندی‌های آزموده‌شده v2.1 | ردیابی محلی نیاز→تست→شاهد برای ۱۳ پالایش ثبت شد | تثبیت و پذیرش ماتریس سراسری؛ پوشش محلی با پوشش کامل برابر نیست |
| P7 | مرور انسانی و بستن G3 | کار قبلی محفوظ؛ پذیرش نهایی باز | بستهٔ تصمیم و شواهد نسخهٔ نامزد پایدار |
| G4 | تطبیق داده، ردیابی، ویکی، Pages و مقاله | کار قبلی محفوظ؛ پذیرش نهایی باز | همگامی نگاشت‌ها و شواهد مستقل، ادعاها و مستندات/مقاله با نسخهٔ مصوب |
| G5a | دیاگرام جامع و مرور نهایی نسخهٔ پایدار | کار قبلی محفوظ؛ پذیرش نهایی باز | دیاگرام جامع OntoUML و نماهای دامنه‌ای پس از تثبیت |
| G5b | ممیزی انتشار و release v2.1 | کار قبلی محفوظ؛ پذیرش نهایی باز | چک‌لیست انتشار، نسخه‌بندی، تغییرات، مجوز، قابلیت بازتولید و آرشیو |

## درصدها با مخرج مشخص

| شاخص | پیش از اجرا | اکنون | تغییر |
|---|---:|---:|---:|
| چهار خروجی محدود: پل ادعا، زمینه، شواهد NDC/راهنما، رگرسیون و گزارش | ۰/۴ | ۴/۴ = ۱۰۰٪ | +۱۰۰ واحد درصد در همین بسته |
| دروازه‌های تاریخی | ۲/۵ = ۴۰٪ | ۲/۵ = ۴۰٪ | صفر |
| بسته‌های اصلی G3 | ۲/۷ = ۲۸٫۶٪ | ۲/۷ = ۲۸٫۶٪ | صفر |
| اجرای معتبر آشکارسازها روی کل candidate | ۰/۲۰ | ۰/۲۰ | صفر |

این چهار خروجی شامل دریافت اعلان واقعی ESMP نیست. درصد کلی وزنی پروژه تعریف نشده؛ درصد موفقیت تست‌ها درصد پیشرفت پروژه نیست.

## همهٔ ایشوهای باز

30 باز، 170 بسته؛ در این اجرا صفر بسته شد.

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

## گام‌های بعدی

1. Obtain a complete action-specific ESMP notice or authorised anonymised submission; map actor/product/country/action/version/time/frequency without inventing unavailable values.
2. Develop the establishment-registration and independent-approval source contracts, preserving entity identity and the distinction between labeler attribution and listing responsibility.
3. Extend independently sourced PV and BA scenarios and reconcile all-domain ownership and requirement gaps.
4. Adjudicate the three description subclasses, claim-origin contract, source/fact migration, seven PROV mappings, two-declaration projection, RG-07, target policies and C. Generic continuation is not scientific acceptance.
5. After accepted decisions, align native/OWL/SHACL and resolve 11 untyped ends, 66 unknown cardinalities, 14 specialised ends, four isolates and four detector discrepancies; run all 20 detectors.
6. Resolve W6 and #307, complete human G3 review, then align data/article/Wiki/Pages, diagrams and release audit.

W6 در کامیت مبنای 894c207: run 37986934737 / job 114011149463 ناموفق؛ steps خالی و logs_url تهی؛ علت قطعی مشخص نشده است. تمام ۲۲ اجرای مشاهده‌شده در همان head ناموفق‌اند. این گزارش دربارهٔ CI کامیت بعدی ادعایی ندارد.
