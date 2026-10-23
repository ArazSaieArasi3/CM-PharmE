# وضعیت کامل CM-PharmE v2.1 — ادامه از 34d23eb

در G3 هستیم؛ مقایسهٔ گزینه‌ها و آزمون‌های محدود انجام شده، پذیرش علمی و ادغام نهایی باز است. PR305 پیش‌نویس است و تصمیم خروج/انتقال چهار دامنه نهایی نشده است.

| شناسه | کار | انجام‌شده / وضعیت | باقی‌مانده |
|---|---|---|---|
| N01 | منشور هدف و مرز v2.1 | پیش‌نویس آماده | تأیید هدف و مرز نسخه |
| N02 | استخراج مستقل و اتمیک نیازمندی‌ها | ۲۴ بند قبلی محفوظ؛ ۱۶ پیشنهاد مستقل جدید، چهار منبع و هشت هم‌پوشانی مشخص | رفع هم‌پوشانی، تکمیل همهٔ دامنه‌ها و آزمون/پذیرش نیازهای ضروری |
| N03 | بازبینی مأموریت و مالکیت همهٔ دامنه‌ها | مأموریت چهار دامنه بررسی شده | مالکیت و مرز همهٔ دامنه‌ها |
| N04 | ماتریس پوشش جهانی و تحلیل شکاف | باز | ماتریس پوشش و شکاف در زمینه‌های مختلف |
| N05 | طراحی و ارزیابی حداقلی چهار دامنه با بازماندن تصمیم جایگاه نهایی | چهار نمونه، هشت اصلاح و دو قاعدهٔ پیشنهادی هویت آزموده | هویت کامل محتوا، تصویب قواعد و جایگاه نهایی دامنه‌ها |
| N06 | تعیین حد رجیستری | مرز پیشنهادی رکورد/واقعیت/مجوز و هشت بند رجیستری آماده | داوری مرز، نگاشت کامل و شاهد مستقل؛ product approval در مدل موجود حل نشده |
| N07 | تقویت محدود Regulatory Policy | چهار بند محدود ESMP برای نقش/سناریو، بالقوه/واقعی، موضوع و تناوب آماده | تعیین زمینهٔ اعمال، نسخه و زمان؛ آزمون اجرایی اختصاصی و پذیرش |
| N08 | تعیین تکلیف مفاهیم منزوی | ۱۳ منزوی در مبنا؛ ۴ در آزمایش قبلی | توجیه معنایی روابط و تعیین تکلیف چهار مفهوم باقی‌مانده |
| N09 | طراحی سناریوها و مرجع پاسخ آزمون | ۱۶ خانوادهٔ قبلی و آزمون‌های هشت اصلاح اجرا شده | سناریوهای مستقل سایر دامنه‌ها |
| P3 | نهایی‌سازی تصمیم‌های علمی قبلی و جدید | سه گزینه برای سه رابطه مقایسه شد؛ C ترجیح آزمایشی دارد | پذیرش stereotype، readOnly و قرارداد شاهد؛ ۳۹ کارت و پرونده‌های قبلی محفوظ |
| P4 | اعمال تصمیم‌های مصوب در سه نمایش | سه OWL delta و سه SHACL profile آزمایشی، با تعریف materialization آماده | ادغام فقط مصوبات؛ دو aboutness و هم‌ترازی کامل همچنان باز |
| P5d | تکمیل نوع سررابطه‌ها، کاردینالیتی و subsetting | برای شش سر از ۱۴، پیشنهاد اجرایی C و کنترل محدود موفق آماده شد | پذیرش صفر از ۱۴؛ ۱۱ نوع، ۶۶ کران مبنا و سه والد گسترده هنوز تعیین‌تکلیف نشده |
| P5c | پوشش معتبر Event/Situation و nature | ده شاهد هویت زمانی اجرا شد؛ حفظ native قبلی برقرار | هویت کامل Event/Situation و اعتبار معنایی nature؛ پذیرش مسیر ترکیبی |
| P5e | اجرای الگوها و هر ۲۰ ضدالگو | ۱۲ آزمایش RelSpec؛ شش mutation بدشکل با خروجی صفر شناسایی شد | چهار اختلاف #315 و اجرای معتبر کل candidate همچنان ۰/۲۰ |
| P6a | نمونه‌سازی مصنوعی کوچک اما پوشش‌دار | ۲۴ شاهد SHACL جدید، ۱۲ ریزنر و ده trace محدود آماده | پوشش متوازن نیازمندی‌ها و مفاهیم کل پروژه |
| P6b | چرخهٔ اصلاح براساس آزمون | تغییر نتیجهٔ یک رگرسیون تشخیص و با سه شاهد توضیح داده شد؛ شکست اولیه محفوظ | قرارداد شاهد باید داوری شود؛ رگرسیون C هنوز ۸۸/۸۹ |
| P6c | قرارداد منبع و شواهد تجربی مستقل | شواهد پیشین ۷۶۸ ردیف محفوظ؛ W6 در head مبنا دوباره بررسی شد | W6 شکست با steps خالی؛ دادهٔ مستقل برای پروفایل‌های جدید و سایر منابع لازم |
| P6d | اعتبارسنجی یکپارچه و ریزنر | ۱۲/۱۲ HermiT؛ قرارداد قبلی ۸۹/۸۹، پس از C فقط ۸۸/۸۹ | اعتبارسنجی یکپارچه پس از پذیرش و رفع اختلاف قرارداد |
| N10 | تثبیت نهایی نیازمندی‌های آزموده‌شده v2.1 | باز | تثبیت نیازمندی‌های آزموده و پذیرفته‌شده |
| P7 | مرور انسانی و بستن G3 | باز | مرور انسانی و بستن G3 |
| G4 | تطبیق داده، ردیابی، ویکی، Pages و مقاله | باز | هم‌ترازی داده، نگاشت، ویکی، Pages و مقاله |
| G5a | دیاگرام جامع و مرور نهایی نسخهٔ پایدار | باز | دیاگرام جامع نسخهٔ پایدار و مرور نهایی |
| G5b | ممیزی انتشار و release v2.1 | باز | ممیزی انتشار و release v2.1 |

تمام ۲۳ بند هنوز بخشی انجام‌نشده دارند؛ تکمیل یک آزمایش معادل بستن بند نیست.

## پیشرفت با مخرج مشخص

| شاخص | قبل | اکنون | تفسیر |
|---|---:|---:|---|
| سررابطهٔ دارای پیشنهاد اجرایی C در این بسته | ۰/۱۴ | ۶/۱۴ = ۴۲٫۹٪ | افزایش ۴۲٫۹ واحد درصد در این شاخص محدود؛ پذیرش علمی صفر است |
| گزینه‌های برنامه‌ریزی‌شدهٔ همین مقایسه که اجرا شدند | ۰/۳ | ۳/۳ = ۱۰۰٪ | مقایسه تمام؛ تصمیم نهایی باز |
| انتظارهای قبلی حفظ‌شده پس از C | — | ۸۸/۸۹ = ۹۸٫۹٪ | یک تغییر قرارداد؛ gate رگرسیون بسته نشده |
| دروازه‌های اصلی تاریخی بسته | ۲/۵ = ۴۰٪ | ۲/۵ = ۴۰٪ | بدون تغییر |
| بسته‌های اصلی G3 بسته | ۲/۷ = ۲۸٫۶٪ | ۲/۷ = ۲۸٫۶٪ | بدون تغییر |
| آشکارساز اجراشدهٔ معتبر روی کل candidate | ۰/۲۰ | ۰/۲۰ | مانع‌های fidelity/semantics باقی است |

این درصدها مستقل‌اند و درصد کیفیت علمی کل پروژه نیستند. نیازمندی‌های مستقل: ۱۶ پیشنهاد جدید، هشت هم‌پوشانی؛ تعداد یکتای کل هنوز معلوم نیست. هیچ درصد ساختگی برای کل نیازمندی‌ها محاسبه نشده است.

## تمام ایشوهای باز

30 باز، 170 بسته؛ در این اجرا صفر ایجاد و صفر بسته شد.

| ایشو | عنوان | وضعیت |
|---|---|---|
| [#315](https://github.com/ArazSaieArasi3/CM-PharmE/issues/315) | [V2.1][P5e] Adjudicate four archived-detector/source discrepancies before full validation | باز |
| [#314](https://github.com/ArazSaieArasi3/CM-PharmE/issues/314) | [V2.1][N05-DS] Design and test minimum viable Digital Systems module | باز |
| [#313](https://github.com/ArazSaieArasi3/CM-PharmE/issues/313) | [V2.1][N05-BA] Design and test minimum viable Business Architecture module | باز |
| [#312](https://github.com/ArazSaieArasi3/CM-PharmE/issues/312) | [V2.1][N05-PV] Design and test minimum viable Pharmacovigilance module | باز |
| [#311](https://github.com/ArazSaieArasi3/CM-PharmE/issues/311) | [V2.1][N05-RM] Design and test minimum viable Risk Management module | باز |
| [#310](https://github.com/ArazSaieArasi3/CM-PharmE/issues/310) | [V2.1][P5b] Bridge native OntoUML JSON to a verified full 20-antipattern detector | باز |
| [#307](https://github.com/ArazSaieArasi3/CM-PharmE/issues/307) | [V2.1][Data] Reconcile NHIF P1 Zenodo file contract with published record | باز |
| [#306](https://github.com/ArazSaieArasi3/CM-PharmE/issues/306) | [V2.1][OntoUML] Resolve pattern triggers and run native validation before release | باز |
| [#244](https://github.com/ArazSaieArasi3/CM-PharmE/issues/244) | [WIKI-33] Final integration, republication and documentation-excellence acceptance audit | باز |
| [#243](https://github.com/ArazSaieArasi3/CM-PharmE/issues/243) | [WIKI-32][BLOCKED][CROSS-REPO] Extract reusable Research/Ontology Documentation Profile into OGCM-RF | باز |
| [#241](https://github.com/ArazSaieArasi3/CM-PharmE/issues/241) | [WIKI-30] Freeze quantitative and qualitative Wiki quality rubrics and perform before/after scoring | باز |
| [#240](https://github.com/ArazSaieArasi3/CM-PharmE/issues/240) | [WIKI-29] Perform page-by-page editorial quality and natural technical prose review | باز |
| [#239](https://github.com/ArazSaieArasi3/CM-PharmE/issues/239) | [WIKI-28] Add tutorials and reproducible how-to paths for using CM-PharmE | باز |
| [#238](https://github.com/ArazSaieArasi3/CM-PharmE/issues/238) | [WIKI-27] Refactor evaluation, supported-claim and reproducibility documentation for readers | باز |
| [#228](https://github.com/ArazSaieArasi3/CM-PharmE/issues/228) | [WIKI-17 EPIC] Elevate CM-PharmE Wiki to a reader-centered research and ontology documentation portal | باز |
| [#214](https://github.com/ArazSaieArasi3/CM-PharmE/issues/214) | [WIKI-12][BLOCKED] Freeze final CM-PharmE 2.0 Wiki for manuscript/research release | باز |
| [#213](https://github.com/ArazSaieArasi3/CM-PharmE/issues/213) | [WIKI-11][BLOCKED] Refresh V2 Wiki after human ontology review and semantic stabilization | باز |
| [#212](https://github.com/ArazSaieArasi3/CM-PharmE/issues/212) | [WIKI-10][BLOCKED] Refresh V2 Wiki after W8 / Gate G stabilization | باز |
| [#211](https://github.com/ArazSaieArasi3/CM-PharmE/issues/211) | [WIKI-09] Maintain CM-PharmE 2.0 as stable-to-date evolving documentation | باز |
| [#202](https://github.com/ArazSaieArasi3/CM-PharmE/issues/202) | [WIKI EPIC] Build complete versioned CM-PharmE Wiki | باز |
| [#173](https://github.com/ArazSaieArasi3/CM-PharmE/issues/173) | [V2][HORP Pilot] Instantiate human ontology review control layer | باز |
| [#171](https://github.com/ArazSaieArasi3/CM-PharmE/issues/171) | [V2-PAPER] Build integrated CM-PharmE 2.0 Manuscript Draft 0 | باز |
| [#170](https://github.com/ArazSaieArasi3/CM-PharmE/issues/170) | [V2-083][W8] Evaluate the demonstrator through representative tasks | باز |
| [#159](https://github.com/ArazSaieArasi3/CM-PharmE/issues/159) | [V2][Human Review] Build concept provenance and V1→V2 evidence mapping matrix | باز |
| [#103](https://github.com/ArazSaieArasi3/CM-PharmE/issues/103) | [W7 META] Prospective evaluation evidence register | باز |
| [#98](https://github.com/ArazSaieArasi3/CM-PharmE/issues/98) | [V2-071][W7] Conduct prospective structured expert evaluation | باز |
| [#24](https://github.com/ArazSaieArasi3/CM-PharmE/issues/24) | [V2 PROGRAM] CM-PharmE 2.0 research roadmap and decision gates | باز |
| [#23](https://github.com/ArazSaieArasi3/CM-PharmE/issues/23) | [V2-PAPER EPIC] Co-develop the Q1/Q2 manuscript and reproducible research release | باز |
| [#22](https://github.com/ArazSaieArasi3/CM-PharmE/issues/22) | [V2-W8 EPIC] Global Pharmaceutical Ecosystem Observatory and application demonstrators | باز |
| [#21](https://github.com/ArazSaieArasi3/CM-PharmE/issues/21) | [V2-W7 EPIC] Prospective multi-family ontology evaluation | باز |

## گام بعد

داوری پیشنهاد C، readOnly والدها و تغییر قرارداد شاهد، سپس ادغام مصوبات در candidate جدید. کار مستقلِ قابل ادامه: رفع هم‌پوشانی ۱۶ نیاز پیشنهادی و ساخت شاهدهای رجیستری/سیاست مقرراتی، همراه با تعیین سه والد گسترده و مسیر Event/Situation.
W6 در head مبنا 34d23eb با run 37974371243 و job 113968787703 شکست خورده و steps خالی است. ۲۲ اجرای ثبت‌شدهٔ همان head شکست دارند؛ علت قطعی مشخص نشده است. موفقیت CI یا PostgreSQL گزارش نمی‌شود.
