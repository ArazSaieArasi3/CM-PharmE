# CM-PharmE v2.1 — چهار دامنهٔ حداقلی و برنامهٔ ادامه

**وضعیت: طرح قابل بازبینی؛ تصمیم خروج/انتقال چهار دامنه معلق است.** ۹ اکتبر ۲۰۲۶، تهران.

این بسته دستور جدید نویسنده را ثبت می‌کند: Risk Management، Pharmacovigilance، Business Architecture و Digital Systems برای بررسی حفظ می‌شوند. حداقلی‌سازی باید بر نیاز و کارکرد متکی باشد. تصمیم جایگاه هسته/افزونه و کفایت علمی هر دامنه هنوز باز است. هیچ کلاس، رابطه یا قید انتالوژی در این نوبت تغییر نکرده است.

## بازیابی و تصحیح وضعیت

برنامهٔ اصلی از `cm-pharme-v2.1-consolidated-plan-2026-10-09.json` بازیابی شد: **۲۳ ردیف** شامل N01–N10 و کارهای فنی قبلی. این فایل اصلی تحلیل پیشنهادی بود و تصریح می‌کرد که تغییر مخزن یا انتالوژی اعمال نشده است. نسخهٔ این بسته همهٔ ردیف‌ها را با ترتیب اصلی حفظ می‌کند و جهت N05 را مطابق دستور جدید تغییر می‌دهد.

مبنای مخزن: `71a8615d7e89b2ee735ca21be4e6f49683816555`، شاخه `v2/connectivity-audit-2-1-candidate`، [PR #305](https://github.com/ArazSaieArasi3/CM-PharmE/pull/305)، [گیت #306](https://github.com/ArazSaieArasi3/CM-PharmE/issues/306). پروندهٔ SupplyCapacity در #309 بسته شده است.

| دستهٔ تحلیل قبلی | یافتهٔ بازیابی و تطبیق‌شده | ادامه |
|---|---|---|
| هدف و مرز | مدل مرجع ماژولار؛ ادعای جهانی باید محدود به شواهد باشد | منشور N01 زیر برای بازبینی آماده است |
| نیازمندی و پوشش | نیاز منبع‌دار، بازسازی از مدل و پیشنهاد جدید تفکیک شوند | ۲۴ نیاز پیشنهادی فقط برای چهار دامنه؛ استخراج جامع هنوز باز |
| سازمان‌دهی دامنه‌ها | ۱۷ عنوان؛ ۱۶ دامنه دارای عنصر؛ تخصیص ۶۰ عنصر افزوده هنوز پیشنهادی | N03، بازبینی مالکیت و روابط همه دامنه‌ها |
| مرز رجیستری و مقررات | ثبت حقوقی، رکورد منبع و سامانه متمایزند؛ سند/الزام/اعمال باید ردیابی شوند | N06 و N07 محفوظ |
| اتصال مدل | ۱۳۸ کلاس نام‌دار، ۶ نوع داده؛ ۱۳ منزوی، ۱۴ مؤلفه، بزرگ‌ترین مؤلفه ۱۲۵ کلاس | این اعداد در این نوبت از فایل native بازشماری شد |
| نقش و وابستگی | دو Mode قبلاً intrinsic-mode شده‌اند؛ P4a برای SupplyCapacity مسیر حامل را تکمیل کرده است | پاسخ بازیابی قبلی که هر دو را همچنان نامشخص می‌دانست، قدیمی بود |
| داوری روابط | ۲۹ ردیف رابطه، ۱۰ پرسش ImpAbs، ۱۹ سیاست RepRel باقی؛ خانواده‌ها همپوشان‌اند | P3 و P5d محفوظ |
| ابزار آنتی‌پترن | P5b اجرای واقعی BinOver را روی سه نمونه کوچک آزموده؛ اجرای کامل ۲۰ مورد انجام نشده | P5c/P5d/P5e و #310 باز |
| مانع تبدیل ابزار | ۱۲ Event/Situation، ۱۴۴ nature restriction، ۱۱ سر بی‌نوع، ۶۶ کاردینالیتی نامشخص و ۱۴ سر تخصص‌یافته | نگاشت نباید معنا را بی‌صدا حذف کند |
| داده واقعی | ۷۶۸ ردیف NHIF، ۳۹٬۲۷۲ RDF؛ SHACL بدون خطا و HermiT سازگار در گزارش قبلی | آزمون این نوبت تکرار نشده؛ نمونه غیرتصادفی و ناممثل کل منبع است |
| ارزیابی و انتشار | قرارداد منبع #307، داده مستقل، بازبینی انسانی و تطبیق مقاله/ویکی باز | G4 و G5 محفوظ |

## N01 — منشور پیشنهادی اصلاح‌شده

هدف پیشنهادی CM-PharmE v2.1، مدل مفهومی مرجع و ماژولار برای پیوند سازمان‌ها و نقش‌ها، محصولات و تأسیسات، ثبت و مجوز و نظارت، عرضه و دسترسی و وابستگی‌های تأمین با شواهد زمان‌مند و قلمرومند است. چهار دامنه ریسک، فارماکوویژیلانس، معماری کسب‌وکار و سامانه‌های دیجیتال در وضعیت حفظ برای بررسی‌اند تا با نیازمندی و روابط موجه، سهم حداقلی و قابل ارزیابی در کل مدل داشته باشند. استقلال از کشور هدف طراحی است؛ اعتبار در همه کشورها ادعای اثبات‌شده نیست.

ذی‌نفعان پیشنهادی: پژوهشگران انتالوژی، تحلیلگران اکوسیستم دارویی، متولیان داده و رگولاتوری، و سازمان‌های مشارکت‌کننده. کاربردها: شناسایی بازیگر و مسئولیت، تمایز مجوز و عمل، ردیابی عرضه و شواهد، و تحلیل محدود ایمنی، ریسک، قابلیت و پشتیبانی دیجیتال. جزئیات درمان بیمار، موتور جامع حقوقی، ریسک عمومی بنگاه و معماری کامل نرم‌افزار در این طرح گسترش داده نمی‌شوند. این محدودیت، حذف خود چهار دامنه نیست.

استقلال دامنه به معنی داشتن هدف، مالکیت معنا و رابط مشخص است؛ به معنی نداشتن وابستگی به Product، Organization یا Evidence نیست. تصمیم پیشین W4 دربارهٔ Business Architecture به‌عنوان نمای تحلیلی اختیاری حفظ شده و این بسته آن را به اصل هویت‌دهی هسته تبدیل نمی‌کند.

## طرح‌های حداقلی پیشنهادی

منابع رسمی از اهمیت حوزه‌ها پشتیبانی می‌کنند؛ کلاس‌ها، روابط و پروفایل‌های زیر **پیشنهاد طراحی ما** هستند و مستقیماً از استانداردها الزام نشده‌اند. کامل‌بودن یا کمینه‌بودن ریاضی این مجموعه هنوز اثبات نشده است.

| دامنه | مفاهیم موجود | منزوی فعلی | جایگاه مفهومی طرح اولیه | هدف |
|---|---:|---:|---:|---|
| Risk Management | 3 | 2 | 6 | ارزیابی و پیگیری ریسک کیفیت و تداوم عرضهٔ دارو در زمینهٔ محصول، تأسیسات و وابستگی تأمین. |
| Pharmacovigilance | 3 | 3 | 7 | پیوند شواهد ایمنی دارو به گزارش‌دهی، سیگنال، ارزیابی و تصمیم قابل ردیابی. |
| Business Architecture | 5 | 2 | 5 | توضیح اینکه سازمان چگونه با قابلیت، خدمت و تعهد همکاری در اکوسیستم دارویی مشارکت می‌کند. |
| Digital Systems | 1 | 1 | 3 | ردیابی پشتیبانی سامانه‌های دیجیتال از فعالیت‌ها و شواهد دارویی، همراه نسخه و استقرار. |

اعداد طرح اولیه شامل ۱۲ مفهوم موجود و ۹ جایگاه پیشنهادی‌اند. جایگاه پیشنهادی ممکن است با مفهوم موجود، تخصص‌یافتگی، قید یا پروفایل داده پوشش یابد؛ در آن صورت کلاس جدید اضافه نمی‌شود. شمار مفاهیم مشترک در دامنه مالک فقط یک‌بار محاسبه می‌شود.

### Risk Management

ارزیابی و پیگیری ریسک کیفیت و تداوم عرضهٔ دارو در زمینهٔ محصول، تأسیسات و وابستگی تأمین.

**حفظ موجود:** `RiskAssessmentActivity`, `RiskTreatmentActivity`, `RiskTreatmentPlan`

| جایگاه پیشنهادی | معنای کاری | وضعیت دسته‌بندی |
|---|---|---|
| `RiskScenarioSpecification` | A documented possible harmful circumstance and consequence; not an occurred disruption. | information content; identity review pending |
| `RiskAssessmentResult` | A contextual assessment conclusion; reuse ObservationResult/Assertion if their definitions suffice. | information result; reuse before adding a class |
| `RiskReviewActivity` | An occurrence reviewing prior assessment or treatment evidence. | event candidate |

**رابط‌ها:** `MedicinalProduct`, `Facility`, `SupplyDependency`, `DisruptionEvent`, `ObservationResult`, `SourceRecord`, `Organization`, `TimeInterval`

**پرسش‌های صلاحیت:**

- **CQ-RM-01** — چه ریسک مستندی دربارهٔ کدام محصول یا وابستگی، با چه ارزیابی‌ای وجود دارد؟
- **CQ-RM-02** — برای نتیجهٔ ارزیابی چه برنامه‌ای وجود دارد و کدام اقدام واقعاً اجرا شده است؟
- **CQ-RM-03** — بازبینی بعدی با چه شواهدی نتیجهٔ قبلی را تغییر داده است؟

| نیاز پیشنهادی | الزام اتمیک | معیار پذیرش |
|---|---|---|
| R-RM-01 | موضوع هر ارزیابی ریسک باید به زمینهٔ دارویی مشخص قابل ردیابی باشد. | پرسش، محصول/تأسیسات/وابستگی موضوع را برگرداند؛ موضوع نامعلوم به‌عنوان نقص اطلاعات مشخص شود. |
| R-RM-02 | نتیجهٔ هر ارزیابی باید از رخداد انجام ارزیابی متمایز باشد. | شناسه نتیجه و رخداد قابل تفکیک باشند؛ نبود نتیجهٔ منتشرشده به معنی نبود رخداد نیست. |
| R-RM-03 | مبنای شواهد هر نتیجهٔ ارزیابی باید قابل بازیابی باشد. | نتیجهٔ پذیرفته‌شده در پروفایل داده به حداقل یک SourceRecord/Assertion متصل باشد. |
| R-RM-04 | برنامهٔ رسیدگی باید به نتیجهٔ ارزیابی موردنظر متصل باشد. | پرسش برنامه فقط ارزیابی‌های تصریح‌شده را برگرداند. |
| R-RM-05 | وقوع اقدام رسیدگی باید مستقل از وجود برنامه قابل تشخیص باشد. | وجود برنامه بدون رخداد، اجرای اقدام را نتیجه ندهد. |
| R-RM-06 | هر بازبینی باید نتیجهٔ پیشین مورد بازبینی را مشخص کند. | زنجیره نسخه/زمان نتیجه‌های قبلی حفظ شود. |

**روابط و قیود اولیه:**

- RD-RM-01: RiskAssessmentActivity موضوع RiskScenarioSpecification را بررسی می‌کند. At least one declared scenario for an admitted assessment record; incomplete evidence is not OWL inconsistency.
- RD-RM-02: RiskScenarioSpecification دربارهٔ MedicinalProduct/Facility/SupplyDependency است. Use typed aboutness routes; do not resurrect deferred AssetAtRisk/Vulnerability automatically.
- RD-RM-03: ارزیابی، RiskAssessmentResult تولید می‌کند و نتیجه به SourceRecord ارجاع دارد. Completed admitted result: one generating assessment and >=1 evidence record; not a universal claim that all assessments complete.
- RD-RM-04: RiskTreatmentPlan نتیجه را مبنا قرار می‌دهد؛ RiskTreatmentActivity اجرای برنامه را ثبت می‌کند. Plan can exist with 0 execution occurrences; ad hoc activity must not force an invented plan.
- RD-RM-05: RiskReviewActivity نتیجه پیشین را بازبینی می‌کند. A review may produce a revised result; preserve original evidence and timestamp.

| سناریوی طراحی‌شده | ورودی | انتظار مستقل از مدل |
|---|---|---|
| SC-RM-01 / positive | ارزیابی وابستگی تأمین X با شاهد E، نتیجه R و برنامه P ثبت می‌شود؛ هنوز اقدامی رخ نداده است. | X/E/R/P بازیابی شوند؛ اقدام اجراشده صفر؛ رخداد و نتیجه یکی نشوند. |
| SC-RM-02 / boundary | بازبینی دوم در زمان t2 نتیجه R را با شاهد جدید اصلاح می‌کند؛ نتیجه t1 باقی است. | هر دو نتیجه با ترتیب زمانی و پیوند بازبینی حفظ شوند. |
| SC-RM-03 / negative | نتیجه آماده پذیرش فاقد موضوع یا شاهد است؛ برنامه به ارزیابی ناموجود اشاره دارد. | پروفایل پذیرش، نقص ارجاع/شواهد را رد کند؛ نوع نقص گزارش شود. |
| SC-RM-04 / non_entailment | تنها سناریوی ریسک و برنامهٔ پیشگیری موجود است. | وقوع اختلال، اجرای درمان یا کاهش واقعی ریسک استنتاج نشود. |

تصمیم‌های باز: Result versus ObservationResult reuse؛ Scenario identity versus actual Situation؛ Meaning and jurisdiction of risk acceptance.

منابع: S1, S6. سناریوهای این بخش طراحی شده‌اند و هنوز اجرا نشده‌اند.

### Pharmacovigilance

پیوند شواهد ایمنی دارو به گزارش‌دهی، سیگنال، ارزیابی و تصمیم قابل ردیابی.

**حفظ موجود:** `AdverseEventReportingActivity`, `PharmacovigilanceRequirement`, `PostMarketSurveillanceActivity`

| جایگاه پیشنهادی | معنای کاری | وضعیت دسته‌بندی |
|---|---|---|
| `SafetyReport` | Versioned safety information submitted/referenced by a reporting occurrence; not the adverse event itself. | information content; may reuse a SourceRecord profile |
| `SafetySignal` | Information warranting investigation of a possible medicine-event association. | information content; not an actual event |
| `SignalAssessmentActivity` | An occurrence evaluating a safety signal. | event candidate |
| `SignalAssessmentResult` | Versioned assessment conclusion with provenance and scoped status. | information result; reuse Assertion/ObservationResult if appropriate |

**رابط‌ها:** `MedicinalProduct`, `PharmaceuticalSubstance`, `SourceRecord`, `EvidenceSupport`, `Organization`, `RegulatoryRequirement`, `RegulatoryJurisdiction`, `TimeInterval`

**پرسش‌های صلاحیت:**

- **CQ-PV-01** — کدام گزارش یا منبع از سیگنال مربوط به کدام دارو یا ماده پشتیبانی می‌کند؟
- **CQ-PV-02** — وضعیت ارزیابی سیگنال در زمان و مرجع معین چیست؟
- **CQ-PV-03** — کدام الزام پایش در این قلمرو اعمال می‌شود و چه فعالیتی آن را پوشش می‌دهد؟

| نیاز پیشنهادی | الزام اتمیک | معیار پذیرش |
|---|---|---|
| R-PV-01 | اطلاعات گزارش ایمنی باید از رخداد گزارش‌کردن متمایز باشد. | بازارسال همان محتوا، رخداد جدید را بدون ادغام خودکار گزارش‌ها ثبت کند. |
| R-PV-02 | موضوع سیگنال باید به محصول یا مادهٔ دارویی مشخص متصل باشد. | سیگنال ماده‌ای بدون اجبار ساختن یک برند قابل ثبت باشد. |
| R-PV-03 | پشتوانهٔ هر سیگنال باید به منابع آن قابل ردیابی باشد. | منبع ادعاشده موجود و قابل ارجاع باشد؛ نبود گزارش فردی سیگنال مبتنی بر مطالعه را رد نکند. |
| R-PV-04 | هر نتیجهٔ ارزیابی باید به سیگنال مورد ارزیابی متصل باشد. | سیگنال و نتیجهٔ ارزیابی آن شناسه و نوع متمایز داشته باشند. |
| R-PV-05 | وضعیت نتیجهٔ ارزیابی باید به زمان ارزیابی مقید باشد. | نتیجهٔ بازبینی، تاریخچهٔ قبلی را پاک نکند. |
| R-PV-06 | اعمال الزام فارماکوویژیلانس باید به قلمرو مقرراتی مشخص مقید باشد. | الزام منطقه A به‌طور خودکار به منطقه B تعمیم نیابد. |

**روابط و قیود اولیه:**

- RD-PV-01: AdverseEventReportingActivity گزارش SafetyReport را ارسال می‌کند. One or more reports per admitted reporting occurrence; same report may have multiple transmissions.
- RD-PV-02: SafetySignal دربارهٔ MedicinalProduct یا PharmaceuticalSubstance است. >=1 explicit target in admitted profile; typed routes permit substance-level signals.
- RD-PV-03: SafetySignal به SourceRecord/EvidenceSupport متصل است. >=1 evidence item for accepted signal record; spontaneous report is not the only permitted source.
- RD-PV-04: SignalAssessmentActivity نتیجه SignalAssessmentResult دربارهٔ سیگنال تولید می‌کند. Result has an identified assessment and temporal context; no one-result-ever uniqueness policy.
- RD-PV-05: PharmacovigilanceRequirement با RegulatoryRequirement هم‌تراز و به قلمرو مربوط می‌شود. Subclass/reuse and applicability constraints pending N07; avoid a duplicate normative-content identity.
- RD-PV-06: PostMarketSurveillanceActivity شواهد مرتبط با موضوع دارویی را تولید/استفاده می‌کند. No mandatory patient individual; law-specific obligations remain separate from actual activity.

| سناریوی طراحی‌شده | ورودی | انتظار مستقل از مدل |
|---|---|---|
| SC-PV-01 / positive | گزارش RP درباره محصول P در رخداد T ارسال و با شاهد E به سیگنال S وصل می‌شود؛ ارزیابی A نتیجه R در t1 می‌دهد. الزام پایش فقط در قلمرو A مستند است. | محتوا، ارسال، سیگنال و نتیجه به‌تفکیک بازیابی شوند. الزام با همان قلمرو برگردد. |
| SC-PV-02 / boundary | سیگنال مربوط به یک ماده از مطالعه و نه گزارش فردی آمده؛ دو ارزیابی در t1 و t2 دارد. | سیگنال معتبرِ داده‌ای با منبع مطالعه پذیرفته و هر دو نتیجه حفظ شوند. |
| SC-PV-03 / negative | رکورد پذیرش‌شده موضوع سیگنال ندارد یا نتیجه به سیگنال ناموجود اشاره دارد؛ الزام A به B منتسب شده است. | نقص ارجاع رد و انتساب بی‌شاهد قلمرو متوقف شود. |
| SC-PV-04 / non_entailment | یک سیگنال مشکوک ثبت شده و الزام گزارش‌دهی فقط برای قلمرو A مستند است. | علیت قطعی، ایمنی قطعی یا الزام در B استنتاج نشود. |

تصمیم‌های باز: Report content versus SourceRecord carrier؛ Signal statuses as contextual claims, not rigid kinds؛ PharmacovigilanceRequirement specialization of RegulatoryRequirement.

منابع: S2, S3, S6. سناریوهای این بخش طراحی شده‌اند و هنوز اجرا نشده‌اند.

### Business Architecture

توضیح اینکه سازمان چگونه با قابلیت، خدمت و تعهد همکاری در اکوسیستم دارویی مشارکت می‌کند.

**حفظ موجود:** `BusinessArchitectureView`, `ServiceOfferingSpecification`, `EnterpriseCapability`, `PartnerOrganizationRole`, `StrategicPartnershipAgreement`

در این طرح اولیه افزودن کلاس جدید لازم دیده نشده؛ بهبود تعریف و روابط همان پنج مفهوم در اولویت است.

**رابط‌ها:** `Organization`, `ManufacturingActivity`, `DistributionLogisticsActivity`, `MedicinalProduct`, `SourceRecord`, `TimeInterval`

**پرسش‌های صلاحیت:**

- **CQ-BA-01** — سازمان چه قابلیتی دارد و آن قابلیت از چه فعالیت واقع‌شده‌ای متمایز است؟
- **CQ-BA-02** — خدمت عرضه‌شده به کدام قابلیت یا فعالیت دارویی متکی است؟
- **CQ-BA-03** — نمای معماری و تعهد همکاری به کدام موجودیت‌های اصلی اشاره می‌کنند؟

| نیاز پیشنهادی | الزام اتمیک | معیار پذیرش |
|---|---|---|
| R-BA-01 | هر EnterpriseCapability باید حامل سازمانی مشخص داشته باشد. | حامل با رابطه موجود capabilityBearer قابل بازیابی باشد؛ Mode بی‌حامل در پروفایل کامل رد شود. |
| R-BA-02 | وجود قابلیت نباید وقوع فعالیت متناظر را الزام کند. | سازمان دارای قابلیت غیرفعال مجاز باشد. |
| R-BA-03 | ServiceOfferingSpecification باید به موضوع خدمت دارویی متصل باشد. | حداقل یک قابلیت/فعالیت/محصول مرتبط در پروفایل پذیرفته‌شده مشخص باشد. |
| R-BA-04 | BusinessArchitectureView باید به شناسه‌های موجودیت‌های اصلی ارجاع دهد. | نمای جدید برای یک سازمان، سازمان دوم ایجاد نکند. |
| R-BA-05 | مشارکت در StrategicPartnershipAgreement باید از تعامل اتفاقی متمایز باشد. | تعامل بدون شاهد تعهد، خودکار PartnerOrganizationRole نسازد. |
| R-BA-06 | هویت موجودیت‌های هسته باید مستقل از وجود نمای معماری بماند. | حذف نمای اختیاری، هویت یا طبقه‌بندی اجباری محصول و تأسیسات را تغییر ندهد. |

**روابط و قیود اولیه:**

- RD-BA-01: EnterpriseCapability حامل Organization دارد. Existing native capabilityBearer is retained; cardinality and inverse characterization orientation reviewed in P3/P5d, no silent replacement.
- RD-BA-02: ServiceOfferingSpecification به قابلیت/فعالیت/محصول دارویی ارجاع می‌دهد. Typed aboutness routes; specification is not actual service execution.
- RD-BA-03: BusinessArchitectureView موجودیت‌های اصلی را بازنمایی می‌کند. Refine existing untyped baViewRepresents with justified typed routes; no mandatory reverse dependency.
- RD-BA-04: StrategicPartnershipAgreement نقش‌های PartnerOrganizationRole را زمینه‌مند می‌کند. Existing mediation retained; >=2 distinct organizations needs identity and temporal evidence, not just two IRIs.

| سناریوی طراحی‌شده | ورودی | انتظار مستقل از مدل |
|---|---|---|
| SC-BA-01 / positive | سازمان O قابلیت C دارد؛ خدمت S به C اشاره و نمای V همان O را بازنمایی می‌کند. O و سازمان متمایز O2 با شاهد توافق A مشارکت راهبردی دارند. | شناسه O مشترک بماند و C/S/V قابل ردیابی باشند. دو نقش شریک به همان توافق و دو سازمان متمایز متصل باشند. |
| SC-BA-02 / boundary | O در بازه t هیچ تولیدی انجام نداده ولی قابلیت C همچنان برقرار است؛ V حذف می‌شود. | وجود C و هویت O/P مستقل از تولید و V حفظ شوند. |
| SC-BA-03 / negative | نمای V سازمان O را کپی می‌کند یا توافق فقط یک سازمان را با دو شناسه تکراری شریک معرفی می‌کند. | تکرار هویت یا ناکافی‌بودن طرف‌های متمایز تشخیص داده شود. |
| SC-BA-04 / non_entailment | خدمت فقط توصیف شده و دو سازمان یک مبادله داشته‌اند. | وقوع خدمت، تحقق قابلیت یا وجود توافق راهبردی استنتاج نشود. |

تصمیم‌های باز: Service specification target types؛ Evidence for distinct partners and repeated agreements؛ View information identity; preserve prior W4 optional-view decision.

منابع: S4, S5, S7. سناریوهای این بخش طراحی شده‌اند و هنوز اجرا نشده‌اند.

### Digital Systems

ردیابی پشتیبانی سامانه‌های دیجیتال از فعالیت‌ها و شواهد دارویی، همراه نسخه و استقرار.

**حفظ موجود:** `DigitalInformationSystemComponent`

| جایگاه پیشنهادی | معنای کاری | وضعیت دسته‌بندی |
|---|---|---|
| `SystemDeploymentActivity` | An actual deployment occurrence of a component/version in an organizational context. | event candidate; check reuse of ProvenanceActivity |
| `DigitalServiceSpecification` | A description of a digital service supporting a pharmaceutical task. | information content; assess ServiceOfferingSpecification reuse |

**رابط‌ها:** `Organization`, `SourceRecord`, `DatasetRelease`, `ProvenanceActivity`, `ObservationActivity`, `TimeInterval`, `ServiceOfferingSpecification`

**پرسش‌های صلاحیت:**

- **CQ-DS-01** — کدام جزء و نسخه سامانه از فعالیت دارویی پشتیبانی کرده است؟
- **CQ-DS-02** — رکورد از کدام فعالیت و سامانه به دست آمده است؟
- **CQ-DS-03** — کدام سازمان و در چه زمانی نسخه سامانه را مستقر کرده است؟

| نیاز پیشنهادی | الزام اتمیک | معیار پذیرش |
|---|---|---|
| R-DS-01 | هویت جزء سامانه باید از هویت رکورد تولیدشده متمایز باشد. | سامانه و SourceRecord شناسه و نوع قابل تفکیک داشته باشند. |
| R-DS-02 | نسخه جزء سامانهٔ استفاده‌شده باید قابل بازیابی باشد. | دو اجرای دارای نسخه‌های مختلف در ردیابی ادغام نشوند. |
| R-DS-03 | رابطه پشتیبانی سامانه باید به فعالیت دارویی مشخص متصل باشد. | نام بردن سامانه بدون فعالیت مرتبط، پوشش عملکرد دامنه شمرده نشود. |
| R-DS-04 | منشأ رکورد باید از مسیر فعالیت تولیدکننده قابل ردیابی باشد. | مسیر رکورد→فعالیت→جزء/نسخه و عامل مسئول برای پروفایل کامل قابل پرس‌وجو باشد. |
| R-DS-05 | هر استقرار باید زمان وقوع مشخص داشته باشد. | تغییر نسخه با رخداد استقرار جدید و حفظ تاریخچه نمایش داده شود. |
| R-DS-06 | وجود رکورد دیجیتال نباید به‌تنهایی مجوز مقرراتی ایجاد کند. | رکورد رجیستری بدون شاهد مجوز، RegulatoryAuthorization استنتاج نکند. |

**روابط و قیود اولیه:**

- RD-DS-01: SystemDeploymentActivity جزء/نسخه و سازمان زمینه را مشخص می‌کند. At least one identified component/version and organizational context for admitted deployment evidence; shared hosting is allowed.
- RD-DS-02: DigitalInformationSystemComponent از فعالیت مشخص پشتیبانی می‌کند. Support/use relation differs from executing agent; no component→prov:SoftwareAgent equivalence without agency evidence.
- RD-DS-03: ProvenanceActivity/ObservationActivity، SourceRecord یا DatasetRelease را تولید می‌کند. Reuse existing provenance where definitions match; preserve generation and responsibility as separate relations.
- RD-DS-04: DigitalServiceSpecification فعالیت دارویی پشتیبانی‌شده را توصیف می‌کند. Existing ServiceOfferingSpecification may suffice; a class addition is not mandatory for domain acceptance.

| سناریوی طراحی‌شده | ورودی | انتظار مستقل از مدل |
|---|---|---|
| SC-DS-01 / positive | سامانه C نسخه v1 در فعالیت A استفاده شده و رکورد R تولید شده؛ استقرار در t1 با سازمان O مستند است. R رکورد رجیستری است و شاهد مجوز ارائه نشده است. | مسیر R/A/C/v1/O/t1 بازیابی و سامانه با رکورد یکی نشود. رکورد قابل بازیابی باشد و وضعیت مجوز نامعلوم بماند. |
| SC-DS-02 / boundary | C به v2 ارتقا یافته؛ R قدیمی همچنان حاصل v1 است و چند سازمان از C استفاده می‌کنند. | ردیابی تاریخی و اشتراک سامانه بدون بازنویسی منشأ قدیمی حفظ شود. |
| SC-DS-03 / negative | رکورد کامل ادعا شده ولی نسخه یا فعالیت تولیدکننده مفقود است؛ رکورد عین سامانه معرفی شده است. | خطای کامل‌بودن داده و اختلاط هویت در پروفایل پذیرش رد شود. |
| SC-DS-04 / non_entailment | نام محصول در رکورد رجیستری دیجیتال آمده و هیچ شاهد مجوز ارائه نشده است. | ثبت داده به معنی ثبت حقوقی، مجوز یا انطباق کامل تلقی نشود. |

تصمیم‌های باز: Software component identity across versions؛ Deployment event versus state/record؛ Reuse service specification and provenance before adding types.

منابع: S5, S6. سناریوهای این بخش طراحی شده‌اند و هنوز اجرا نشده‌اند.

## معیار پذیرش دامنه حداقلی

1. هر مفهوم یک نیاز و دست‌کم یک CQ ضروری را پشتیبانی کند؛ مفهوم تزئینی پذیرفته نیست.
2. رابط‌های بین‌دامنه‌ای نوع‌دار، دارای تعریف، شاهد و کاردینالیتی موجه باشند؛ لینک برای زیبایی گراف کافی نیست.
3. هر نیاز الزامی شاهد مثبت و مرزی/منفی و نتیجهٔ آزمون قابل بازتولید داشته باشد.
4. تمایز هویت، رخداد، وضعیت، محتوا و شاهد حفظ شود؛ طبقه‌بندی OntoUML برای موارد جدید باید مستقل بررسی شود.
5. آزمون حذف/بازاستفاده انجام شود: اگر حذف کلاس پیشنهادی یا استفاده از کلاس موجود، CQ را بدون از دست‌رفتن معنا پاسخ می‌دهد، افزودن کلاس توجیه ندارد.
6. پروفایل پذیرش بسته با قیود جهانی OWL خلط نشود؛ شاهد مفقود در داده باز، الزاماً ناسازگاری واقعیت نیست.
7. مفیدبودن کل مدل با سناریوی مشترک ارزیابی شود: شاهد کیفیت/عرضه → ارزیابی ریسک → برنامه و اقدام؛ شاهد ایمنی → سیگنال و ارزیابی؛ سازمان/قابلیت/همکاری → فعالیت دارویی؛ سامانه/نسخه → فعالیت و منشأ رکورد. اتصال این زنجیره‌ها باید شاهد داشته باشد.
8. حفظ شمار کم مفاهیم معیار کفایت نیست؛ پذیرش بر پاسخ‌گویی، نبود تعارض، پوشش شواهد و بازبینی متخصص استوار است.

## برنامهٔ جامع حفظ‌شده

| ترتیب | شناسه | کار | وضعیت این نوبت |
|---:|---|---|---|
| 1 | N01 | منشور هدف و مرز v2.1 | DRAFT_PREPARED_NOT_ACCEPTED |
| 2 | N02 | استخراج مستقل و اتمیک نیازمندی‌ها | PARTIAL_DRAFT_FOUR_DOMAINS_ONLY |
| 3 | N03 | بازبینی مأموریت و مالکیت همهٔ دامنه‌ها | PARTIAL_DRAFT_FOUR_DOMAINS_ONLY |
| 4 | N04 | ماتریس پوشش جهانی و تحلیل شکاف | PROPOSED_PENDING_DECISION |
| 5 | N05 | طراحی و ارزیابی حداقلی چهار دامنه با بازماندن تصمیم جایگاه نهایی | PARTIAL_DRAFT_FOUR_DOMAINS_ONLY |
| 6 | N06 | تعیین حد رجیستری | PROPOSED_PENDING_DECISION |
| 7 | N07 | تقویت محدود Regulatory Policy | PROPOSED_PENDING_DECISION |
| 8 | N08 | تعیین تکلیف مفاهیم منزوی | PROPOSED_PENDING_DECISION |
| 9 | N09 | طراحی سناریوها و مرجع پاسخ آزمون | PARTIAL_DRAFT_FOUR_DOMAINS_ONLY |
| 10 | P3 | نهایی‌سازی تصمیم‌های علمی قبلی و جدید | PROPOSED_PENDING_DECISION |
| 11 | P4 | اعمال تصمیم‌های مصوب در سه نمایش | PROPOSED_PENDING_DECISION |
| 12 | P5d | تکمیل نوع سررابطه‌ها، کاردینالیتی و subsetting | PROPOSED_PENDING_DECISION |
| 13 | P5c | پوشش معتبر Event/Situation و nature | PROPOSED_PENDING_DECISION |
| 14 | P5e | اجرای الگوها و هر ۲۰ ضدالگو | PROPOSED_PENDING_DECISION |
| 15 | P6a | نمونه‌سازی مصنوعی کوچک اما پوشش‌دار | PROPOSED_PENDING_DECISION |
| 16 | P6b | چرخهٔ اصلاح براساس آزمون | PROPOSED_PENDING_DECISION |
| 17 | P6c | قرارداد منبع و شواهد تجربی مستقل | PROPOSED_PENDING_DECISION |
| 18 | P6d | اعتبارسنجی یکپارچه و ریزنر | PROPOSED_PENDING_DECISION |
| 19 | N10 | تثبیت نهایی نیازمندی‌های آزموده‌شده v2.1 | PROPOSED_PENDING_DECISION |
| 20 | P7 | مرور انسانی و بستن G3 | PROPOSED_PENDING_DECISION |
| 21 | G4 | تطبیق داده، ردیابی، ویکی، Pages و مقاله | PROPOSED_PENDING_DECISION |
| 22 | G5a | دیاگرام جامع و مرور نهایی نسخهٔ پایدار | PROPOSED_PENDING_DECISION |
| 23 | G5b | ممیزی انتشار و release v2.1 | PROPOSED_PENDING_DECISION |

اجرای جزئی N02/N03/N05/N09 برای چهار دامنه، به معنی تکمیل آن‌ها برای کل انتالوژی نیست. N01 نیز هنوز منشور پیشنهادی قابل بازبینی است.

## پیشرفت و اعتبار نتایج

- آماده‌سازی چهار پرونده: **۴/۴ = ۱۰۰٪**؛ این فقط پوشش طراحی اولیه است.
- نیازهای پیشنهادی دارای CQ و شاهد طراحی‌شده مثبت و مرزی/منفی: **۲۴/۲۴ = ۱۰۰٪**؛ اجرای معنایی **۰/۱۶ سناریو**.
- برنامهٔ قدیمی: **۲/۵ گیت اصلی = ۴۰٪** و **۲/۷ بسته G3 = ۲۸٫۶٪**؛ در این نوبت هیچ گیت جدید بسته نشد.
- برنامهٔ تازهٔ ۲۳ردیفی: **۰/۲۳ پذیرش نهایی**؛ پیش‌نویس N01 و کار جزئی چهار دامنه برای N02/N03/N05/N09 آماده شده است. این معیار، پیشرفت تاریخی را صفر نمی‌کند.
- وضعیت هنگام بررسی مخزن، پیش از افزودن پرونده پیگیری جدید: **۲۵ issue باز و ۱۷۰ بسته**، بدون احتساب PR. نسبت بسته‌ها ۸۷٫۲٪ است و درصد پیشرفت علمی یا آمادگی انتشار نیست.
- بازشماری واقعی گراف و کنترل ارجاعات بسته در `audit-results.json` ثبت شده؛ آزمون‌های دلیل‌آور و آنتی‌پترن در این نوبت تکرار نشده‌اند.

**گام بعدی اجرایی:** تکمیل نگاشت نیازمندی به ۱۲ مفهوم موجود و روابط پیشنهادی چهار دامنه، بررسی بازاستفاده ۹ جایگاه مفهومی پیشنهادی، تعیین هویت/وابستگی/کاردینالیتی و اجرای ۱۶ سناریوی طراحی‌شده در کاندید مستقل؛ هم‌زمان استخراج نیازهای دیگر دامنه‌ها.

## فایل‌ها

- [domain-dossier.json](domain-dossier.json): چهار قرارداد دامنه، ۲۴ نیاز، ۱۲ CQ، ۱۹ طرح رابطه و ۱۶ سناریو.
- [continuation-plan.json](continuation-plan.json): هر ۲۳ ردیف پیشین همراه تصمیم جدید و حدود پیشرفت.
- [audit_package.py](audit_package.py): کنترل شناسه‌ها، ردیابی و بازشماری گراف مبنا.
- [audit-results.json](audit-results.json): نتیجهٔ واقعی کنترل بسته؛ گواهی صحت علمی نیست.

## منابع و حدود استفاده

- **S1** [ICH Q9(R1), final Step 4, 2023](https://database.ich.org/sites/default/files/ICH_Q9%28R1%29_Guideline_Step4_2023_0126_0.pdf). Sections 4.3–4.6, 6.1. Pharmaceutical quality risk assessment, control and review, including availability risks from quality/manufacturing issues. Does not prescribe the proposed ontology classes.
- **S2** [WHO Pharmacovigilance](https://www.who.int/teams/regulation-prequalification/regulation-and-safety/pharmacovigilance/). What is Pharmacovigilance?. Medicine-safety monitoring is a legitimate pharmaceutical ecosystem concern.
- **S3** [EMA GVP Module IX Rev.1, final](https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-good-pharmacovigilance-practices-gvp-module-ix-signal-management-rev-1_en.pdf). IX.A.1.1, pp.4–6; IX.B; IX.C.8. Reports, signals, assessment and recorded dispositions are distinct. EU procedures are jurisdiction-specific; signal status is not proof of causation.
- **S4** [The Open Group ArchiMate overview](https://www.opengroup.org/archimate-forum/archimate-overview). About the ArchiMate Modeling Language. Cross-domain analysis of processes, organizational structures, information flows and IT. Not an OntoUML stereotype mapping.
- **S5** [The Open Group ArchiMate 101](https://archimate-community.pages.opengroup.org/workgroups/archimate-101/). Business Layer Elements; Application Layer Elements. Distinguishes business behavior, applications and data; supports analytical interfaces.
- **S6** [W3C PROV-O Recommendation](https://www.w3.org/TR/prov-o/). Section 3.1 Starting Point Terms; qualified relations. Reusable provenance for entities, activities and responsible agents; no mandatory equivalence between a software artifact and a software agent.
- **S7** [OntoUML Characterization documentation](https://ontouml.readthedocs.io/en/latest/relationships/characterization/index.html). Definition. Mode and Quality bearer dependence; generic constraints do not settle each proposed domain-specific stereotype.

منابع در ۹ اکتبر ۲۰۲۶ بررسی شدند. شواهد چندقلمرویی و داده مستقل برای N04/P6c هنوز لازم است. منبع EMA چارچوب اروپا را توصیف می‌کند و تعمیم حقوقی آن به جهان مجاز نیست.

## پیگیری ثبت‌شده

- RM: [#311](https://github.com/ArazSaieArasi3/CM-PharmE/issues/311)
- PV: [#312](https://github.com/ArazSaieArasi3/CM-PharmE/issues/312)
- BA: [#313](https://github.com/ArazSaieArasi3/CM-PharmE/issues/313)
- DS: [#314](https://github.com/ArazSaieArasi3/CM-PharmE/issues/314)

پس از ثبت این چهار کار: **۲۹ issue باز و ۱۷۰ بسته**؛ در این نوبت صفر issue بسته شد.
