# وضعیت کامل CM-PharmE v2.1 — ادامه از a83471c

در G3 هستیم. بستهٔ نیازمندی و آزمون رجیستری/گزارش‌دهی آماده شد؛ پذیرش علمی، ادغام و مرور انسانی بازند. PR305 پیش‌نویس است؛ خروج/انتقال چهار دامنه نهایی نشده است.

| شناسه | کار | انجام‌شده / وضعیت | باقی‌مانده |
|---|---|---|---|
| N01 | منشور هدف و مرز v2.1 | پیش‌نویس آماده | تأیید هدف و مرز نسخه |
| N02 | استخراج مستقل و اتمیک نیازمندی‌ها | ۱۶/۱۶ بند تطبیق داده شد؛ ۴۰ ردیف ورودی به ۳۹ عنوان کاری ردیابی شد | استخراج همهٔ دامنه‌ها و پذیرش علمی؛ ۳۹ عنوان صرفاً محدودهٔ این دو ورودی است |
| N03 | بازبینی مأموریت و مالکیت همهٔ دامنه‌ها | مأموریت چهار دامنه بررسی شده | مالکیت و مرز همهٔ دامنه‌ها |
| N04 | ماتریس پوشش جهانی و تحلیل شکاف | باز | ماتریس پوشش و شکاف در زمینه‌های مختلف |
| N05 | طراحی و ارزیابی حداقلی چهار دامنه با بازماندن تصمیم جایگاه نهایی | چهار دامنه حفظ شدند؛ شواهد منشأ و تفکیک ادعا/وضعیت تقویت شد | پذیرش طراحی حداقلی و تصمیم جایگاه نهایی چهار دامنه |
| N06 | تعیین حد رجیستری | هشت بند رجیستری، شاهدهای مثبت/منفی و اصلاح خودگزارشی سازمان آماده | دادهٔ واقعی جدید و نگاشت کامل؛ مدل کامل مجوز محصول هنوز باز |
| N07 | تقویت محدود Regulatory Policy | چهار بند گزارش‌دهی با نقش، سناریو، مسیر، موضوع و زمان آزموده شد | مدل مفهومی زمینهٔ اعمال و منبع واقعی اعلان؛ پذیرش علمی |
| N08 | تعیین تکلیف مفاهیم منزوی | ۱۳ منزوی در مبنا؛ ۴ در آزمایش قبلی | توجیه معنایی روابط و تعیین تکلیف چهار مفهوم باقی‌مانده |
| N09 | طراحی سناریوها و مرجع پاسخ آزمون | برای هر ۱۶ بند بسته شاهد مثبت و منفی وجود دارد؛ ۳۸ پاسخ بررسی شد | سناریوهای مستقل سایر دامنه‌ها، خصوصاً دو والد بدون شاهد |
| P3 | نهایی‌سازی تصمیم‌های علمی قبلی و جدید | دو قید هویت و اصلاح RG-07 برای داوری آماده است؛ تصمیم C محفوظ | پذیرش قیدها، C/readOnly و پرونده‌های علمی قبلی |
| P4 | اعمال تصمیم‌های مصوب در سه نمایش | ۱۳ رابطهٔ موجود بازاستفاده شد؛ ۲۲ فیلد آزمایشی و چهار PROV تفکیک شدند | نگاشت رسمی جهت‌دار PROV و انتقال فقط مصوبات به native/OWL/SHACL |
| P5d | تکمیل نوع سررابطه‌ها، کاردینالیتی و subsetting | سه والد در ۴۵ گراف مثبت و نمونهٔ واقعی ممیزی شد؛ ۶۱۴۴ پیوند مشاهده | دو والد بی‌شاهد؛ تعیین دامنه/کران کامل و ۱۱ نوع/۶۶ کران نامشخص قبلی |
| P5c | پوشش معتبر Event/Situation و nature | دو برخورد هویت در OWL قبلی بازتولید و با قید پیشنهادی مهار شد | پذیرش علمی و اعتبارسنجی جامع Event/Situation/nature |
| P5e | اجرای الگوها و هر ۲۰ ضدالگو | ۱۲ آزمایش RelSpec؛ شش mutation بدشکل با خروجی صفر شناسایی شد | چهار اختلاف #315 و اجرای معتبر کل candidate همچنان ۰/۲۰ |
| P6a | نمونه‌سازی مصنوعی کوچک اما پوشش‌دار | پنج پروفایل با ۲۷ SHACL و ۳۸ پاسخ آزموده شد | پوشش متوازن همهٔ نیازهای پروژه |
| P6b | چرخهٔ اصلاح براساس آزمون | دو نقص fixture ناشی از mandate مفقود اصلاح شد؛ شکست اولیه محفوظ | داوری تغییر قرارداد C همچنان ۸۸/۸۹؛ اصلاح‌ها پس از پذیرش |
| P6c | قرارداد منبع و شواهد تجربی مستقل | نمونهٔ واقعی قبلی ۷۶۸ ردیفی عدم پسرفت را گذراند؛ شاهد جدید صفر | دریافت دادهٔ مستقل NDC/ESMP؛ رفع شکست W6 با steps خالی |
| P6d | اعتبارسنجی یکپارچه و ریزنر | ۱۳ HermiT مصنوعی + یک واقعی موفق؛ رگرسیون این بسته ۸۹/۸۹ | اعتبارسنجی یکپارچه پس از ادغام؛ نتیجهٔ C جدا و باز باقی است |
| N10 | تثبیت نهایی نیازمندی‌های آزموده‌شده v2.1 | باز | تثبیت نیازمندی‌های آزموده و پذیرفته‌شده |
| P7 | مرور انسانی و بستن G3 | باز | مرور انسانی و بستن G3 |
| G4 | تطبیق داده، ردیابی، ویکی، Pages و مقاله | باز | هم‌ترازی داده، نگاشت، ویکی، Pages و مقاله |
| G5a | دیاگرام جامع و مرور نهایی نسخهٔ پایدار | باز | دیاگرام جامع نسخهٔ پایدار و مرور نهایی |
| G5b | ممیزی انتشار و release v2.1 | باز | ممیزی انتشار و release v2.1 |

تمام ۲۳ کار اصلی هنوز بخش باقی‌مانده دارند. تکمیل آزمایش‌های این اجرا، بستن کل بند یا پذیرش علمی نیست.

## درصدهای محدود و قابل ممیزی

| شاخص | قبل | اکنون | تغییر |
|---|---:|---:|---:|
| تطبیق و تصمیم کارشناسی اولیه برای بستهٔ ۱۶بندی | ۰/۱۶ = ۰٪ | ۱۶/۱۶ = ۱۰۰٪ | +۱۰۰ واحد درصد |
| پوشش مثبت/منفی اجراییِ همین ۱۶ بند | ۰/۱۶ = ۰٪ | ۱۶/۱۶ = ۱۰۰٪ | +۱۰۰ واحد درصد |
| دروازه‌های اصلی تاریخی بسته | ۲/۵ = ۴۰٪ | ۲/۵ = ۴۰٪ | صفر |
| بسته‌های اصلی G3 بسته | ۲/۷ = ۲۸٫۶٪ | ۲/۷ = ۲۸٫۶٪ | صفر |
| اجرای معتبر آشکارساز روی کل candidate | ۰/۲۰ | ۰/۲۰ | صفر |

۳۹ عنوان کاری از ۴۰ ردیف ورودی، معیار پوشش جهانی نیست. دادهٔ جدید مصنوعی است. ۸۹/۸۹ رگرسیون این بسته، نتیجهٔ مستقل C با ۸۸/۸۹ را تغییر نمی‌دهد.

## تمام ایشوهای باز

30 باز و 170 بسته؛ در این اجرا صفر ایجاد و صفر بسته شد.

| ایشو | عنوان | وضعیت |
|---|---|---|
| [#315](https://github.com/ArazSaieArasi3/CM-PharmE/issues/315) | [V2.1][P5e] Adjudicate four archived-detector/source discrepancies before full validation | باز |
| [#314](https://github.com/ArazSaieArasi3/CM-PharmE/issues/314) | [V2.1][N05-DS] Design and test minimum viable Digital Systems module | باز |
| [#312](https://github.com/ArazSaieArasi3/CM-PharmE/issues/312) | [V2.1][N05-PV] Design and test minimum viable Pharmacovigilance module | باز |
| [#313](https://github.com/ArazSaieArasi3/CM-PharmE/issues/313) | [V2.1][N05-BA] Design and test minimum viable Business Architecture module | باز |
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

## گام بعدی دقیق

نگاشت جهت‌دار و پین‌شدهٔ PROV و سناریوهای مستقل دو والد بی‌شاهد را آماده و آزمایش کنیم. هم‌زمان، دو قید هویت جدید، اصلاح خودگزارشی RG-07 و تغییر قرارداد C برای داوری علمی آماده‌اند.
پس از آن: ادغام مصوبات، دادهٔ واقعی جدید و اعتبارسنجی جامع. W6 در head مبنا a83471c، run 37979023406 و job 113984503975 شکست خورده و steps خالی است؛ علت قطعی تعیین نشده است.

موفقیت نمونهٔ واقعی قبلی: ۷۶۸ ردیف، ۳۹۲۷۲ سه‌تایی، SHACL و HermiT موفق؛ شاهد پروفایل جدید صفر. این نتیجه صرفاً عدم پسرفت است.
