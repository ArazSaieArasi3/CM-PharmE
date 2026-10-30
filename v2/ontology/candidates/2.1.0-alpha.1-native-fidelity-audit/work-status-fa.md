# وضعیت کامل CM-PharmE v2.1

۲۰۲۶-۱۰-۰۹، Asia/Tehran — ادامه از bf7e764. این گزارش تمام ۲۳ بند قبلی و تمام ایشوهای باز را نگه می‌دارد. تصمیم خروج/انتقال چهار دامنه متوقف است؛ PR305 پیش‌نویس است.

| شناسه | کار | انجام‌شده / وضعیت | باقی‌مانده |
|---|---|---|---|
| N01 | منشور هدف و مرز v2.1 | پیش‌نویس آماده | تأیید هدف و مرز نسخه |
| N02 | استخراج مستقل و اتمیک نیازمندی‌ها | ۲۴ نیازمندی نگاشت‌شده؛ ۸ اصلاح آزموده | تکمیل نیازمندی‌های همهٔ دامنه‌ها و پذیرش علمی |
| N03 | بازبینی مأموریت و مالکیت همهٔ دامنه‌ها | مأموریت چهار دامنه بررسی شده | مالکیت و مرز همهٔ دامنه‌ها |
| N04 | ماتریس پوشش جهانی و تحلیل شکاف | باز | ماتریس پوشش و شکاف در زمینه‌های مختلف |
| N05 | طراحی و ارزیابی حداقلی چهار دامنه با بازماندن تصمیم جایگاه نهایی | چهار نمونه، هشت اصلاح و دو قاعدهٔ پیشنهادی هویت آزموده | هویت کامل محتوا، تصویب قواعد و جایگاه نهایی دامنه‌ها |
| N06 | تعیین حد رجیستری | باز | مرز رجیستری و تفکیک داده/واقعیت/مجوز |
| N07 | تقویت محدود Regulatory Policy | قلمرو PV به‌صورت محدود آزموده | پوشش محدود و مستند Regulatory Policy |
| N08 | تعیین تکلیف مفاهیم منزوی | ۱۳ منزوی در مبنا؛ ۴ در آزمایش قبلی | توجیه معنایی روابط و تعیین تکلیف چهار مفهوم باقی‌مانده |
| N09 | طراحی سناریوها و مرجع پاسخ آزمون | ۱۶ خانوادهٔ قبلی و آزمون‌های هشت اصلاح اجرا شده | سناریوهای مستقل سایر دامنه‌ها |
| P3 | نهایی‌سازی تصمیم‌های علمی قبلی و جدید | ۳۹ کارت رابطه، ۲۰ تفسیر ویژهٔ رخداد/تحقق و ۹ تصمیم هویت آماده شد | تصویب stereotype و کران‌ها؛ ادامهٔ پروندهٔ ۲۹ رابطهٔ قبلی |
| P4 | اعمال تصمیم‌های مصوب در سه نمایش | تطابق هفت رابطهٔ تخصص‌یافته با OWL بررسی و تأیید ساختاری شد | اعمال تصمیم‌های مصوب و هم‌ترازی کامل native/OWL/SHACL؛ دو aboutness آزمایشی نیز باز |
| P5d | تکمیل نوع سررابطه‌ها، کاردینالیتی و subsetting | هر ۱۴ سر واقعی و هفت قطعه بررسی شد؛ ۱۰ انطباق نوع/زمینه و چهار نامشخص | ۱۱ سر بی‌نوع، ۶۶ کاردینالیتی نامشخص، ۱۴ تخصص هنوز حل‌نشده و سیاست readOnly |
| P5c | پوشش معتبر Event/Situation و nature | حفظ ۱۵ Event/Situation، ۱۴۷ nature و ۲۵ Note؛ نگهبان ۸۲ null ساخته و آزموده شد | اعتبارسنجی معنایی رخداد/وضعیت و تصویب مسیر ترکیبی؛ وفاداری serialization کافی نیست |
| P5e | اجرای الگوها و هر ۲۰ ضدالگو | اجرای تاریخی و شاهد مثبت/منفی پایهٔ ۲۰/۲۰ خانواده؛ چهار اختلاف منبع آشکار شد | داوری #315، پوشش شاخه‌های بیشتر و اجرای معتبر روی کل مدل |
| P6a | نمونه‌سازی مصنوعی کوچک اما پوشش‌دار | نمونه‌های محدود چهار دامنه آماده و آزموده | پوشش متوازن همهٔ نیازمندی‌های پروژه |
| P6b | چرخهٔ اصلاح براساس آزمون | نقص حفظ null کشف شد؛ ۲۱ آزمون قواعد، ۱۰ guard خروجی، چهار کنترل adapter و سه کنترل parser موفق | اصلاح‌های معنایی پس از داوری؛ پذیرش علمی از موفقیت آزمون استنتاج نشود |
| P6c | قرارداد منبع و شواهد تجربی مستقل | قرارداد P1 اصلاح؛ ۱۲ آزمون منفی و تبدیل ۷۶۸ ردیف موفق | رفع مانع اجرای W6 CI؛ سایر منابع و دادهٔ مستقل |
| P6d | اعتبارسنجی یکپارچه و ریزنر | ۸ آزمون HermiT برای سیاست جدید موفق؛ شواهد واقعی قبلی محفوظ | اعتبارسنجی کل نسخه پس از ادغام تصمیم‌ها |
| N10 | تثبیت نهایی نیازمندی‌های آزموده‌شده v2.1 | باز | تثبیت نیازمندی‌های آزموده و پذیرفته‌شده |
| P7 | مرور انسانی و بستن G3 | باز | مرور انسانی و بستن G3 |
| G4 | تطبیق داده، ردیابی، ویکی، Pages و مقاله | باز | هم‌ترازی داده، نگاشت، ویکی، Pages و مقاله |
| G5a | دیاگرام جامع و مرور نهایی نسخهٔ پایدار | باز | دیاگرام جامع نسخهٔ پایدار و مرور نهایی |
| G5b | ممیزی انتشار و release v2.1 | باز | ممیزی انتشار و release v2.1 |

## پیشرفت

| شاخص | قبل | اکنون | تغییر |
|---|---:|---:|---:|
| پوشش بررسی مستقیم ۱۴ سر واقعی | ۰/۱۴ = ۰٪ | ۱۴/۱۴ = ۱۰۰٪ | +۱۰۰ واحد درصد |
| تخصص سررابطهٔ کاملاً تعیین‌تکلیف‌شده | ۰/۱۴ | ۰/۱۴ | صفر |
| حساسیت پایهٔ خانواده‌های موتور قدیمی | ۲۰/۲۰ = ۱۰۰٪ | ۲۰/۲۰ = ۱۰۰٪ | صفر |
| اجرای معتبر ۲۰ آشکارساز روی کل مدل | ۰/۲۰ | ۰/۲۰ | صفر |
| دروازه‌های اصلی تاریخی بسته | ۲/۵ = ۴۰٪ | ۲/۵ = ۴۰٪ | صفر |
| بسته‌های اصلی G3 بسته | ۲/۷ = ۲۸٫۶٪ | ۲/۷ = ۲۸٫۶٪ | صفر |

این شاخص‌ها مخرج‌های متفاوت دارند؛ هیچ‌کدام درصد کیفیت علمی کل پروژه نیست. ۳۰ ایشوی باز، ۱۷۰ بسته؛ در این اجرا صفر ایجاد و صفر بسته شد. تمام ۲۳ بند برنامه هنوز کار باقی‌مانده دارند.

## تمام ایشوهای باز

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

## اکنون کجا هستیم و گام بعدی

در G3، بین آماده‌سازی شواهد P5 و پذیرش علمی P3/P4 هستیم. بررسی واقعیِ سررابطه‌ها و مهار افت داده انجام شده، اما پذیرش مدل و تبدیل کامل انجام نشده است. کارت‌های هفت رابطه در `decision-cards-fa.md` تصمیم بعدی را مشخص می‌کنند؛ مسیر حفظ معنا و چهار اختلاف منبع در `validation-route-fa.md` آمده است.

گام بعدی: تعیین سیاستِ شش سر تخصص‌یافتهٔ mediation و readOnly آن‌ها، و نوع/کران سه والدِ مشترک گسترده؛ سپس اعمال مصوبات در candidate جدید. هم‌زمان، تکمیل نیازمندی‌های مستقل همهٔ دامنه‌ها و قرارداد هویت/زمان Event/Situation قابل ادامه است. بعد از تعیین منبع حاکم #315 و رفع مانع W6، اعتبارسنجی یکپارچه و مرور انسانی انجام می‌شود. از موفقیت آزمون‌های محدود برای بستن gate استفاده نشده است.

W6 در head مبنا bf7e764 با run 37971912118 و job 113960399377 شکست خورده و پاسخ مراحل خالی است؛ علت قطعی هنوز در دسترس نیست. نتیجهٔ موفق PostgreSQL یا CI ادعا نمی‌شود.
