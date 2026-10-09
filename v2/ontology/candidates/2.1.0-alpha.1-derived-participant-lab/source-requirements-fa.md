# بستهٔ نیازمندی‌های مستقل رجیستری، سیاست مقرراتی و منشأ داده

۱۶ پیشنهاد از چهار منبع اصلی؛ هر بند پرسش شایستگی، معیار مثبت/منفی و نگاشت اولیه دارد. این‌ها طراحی پیشنهادی‌اند؛ اجرای حقوقی یا انطباق با استاندارد ادعا نمی‌شود.

۲۴ نیازمندی قبلی حفظ شده است. به دلیل هم‌پوشانی، جمع ۴۰ نیازمندی یکتا گزارش نمی‌شود. آزمون اجرایی اختصاصی این ۱۶ بند و پذیرش آن‌ها هنوز صفر است.

| شناسه | دامنه | نیاز پیشنهادی | شکاف | هم‌پوشانی قبلی |
|---|---|---|---|---|
| B2-RG-01 | Registry | Keep establishment registration separate from drug listing. | Record-to-fact mapping unresolved. | تطابق مستقیم یافت نشد |
| B2-RG-02 | Registry | Registration must not imply product approval. | Existing authorizationParty targets organizations/facilities; product approval representation unresolved. | R-DS-06 |
| B2-RG-03 | Registry | NDC listing must not imply approval. | Approval evidence path unresolved. | R-DS-06 |
| B2-RG-04 | Registry | Attribute submitted directory information to its labeler. | Submitter attribution differs from listing responsibility. | تطابق مستقیم یافت نشد |
| B2-RG-05 | Registry | Directory absence must preserve uncertainty. | Query absence policy required. | تطابق مستقیم یافت نشد |
| B2-RG-06 | Registry | Distinguish marketing dates from retrieval dates. | Bitemporal source profile needed. | تطابق مستقیم یافت نشد |
| B2-RP-01 | Regulatory Policy | Qualify reporting obligations by actor role and scenario. | Scenario applicability path absent. | R-PV-06 |
| B2-RP-02 | Regulatory Policy | Separate potential-shortage reports from actual shortage situations. | Potential/actual assessment policy needed. | تطابق مستقیم یافت نشد |
| B2-RP-03 | Regulatory Policy | Constrain reporting product scope to the selected scenario. | Authorization route and scenario membership unresolved. | تطابق مستقیم یافت نشد |
| B2-RP-04 | Regulatory Policy | Bind reporting frequency to the announced action. | Trigger/version/time linkage unresolved. | تطابق مستقیم یافت نشد |
| B2-DS-07 | Digital Systems | Distinguish a generated record from its generating activity. | Generic provenance alignment pending. | R-DS-01, R-DS-04 |
| B2-DS-08 | Digital Systems | Distinguish entity attribution from activity association. | Agent typing and responsibility mapping pending. | تطابق مستقیم یافت نشد |
| B2-DS-09 | Digital Systems | Retain derivation lineage between data artifacts. | Derivation relation not mapped. | R-DS-04 |
| B2-DS-10 | Digital Systems | Represent revision lineage without automatic identity merging. | Revision identity policy unresolved. | R-RM-06, R-DS-02 |
| B2-RG-07 | Registry | Keep registration entity, reporting organization and source record distinct. | Subject resolution policy required. | R-DS-01 |
| B2-RG-08 | Registry | Treat SPL as a submission representation. | Payload/carrier/claim mapping unresolved. | R-DS-01 |

مشخصات کامل، پرسش‌ها، معیارها و نشانی دقیق منابع در `source-requirements.json` است.
پیشنهاد مرز N06: رجیستری، هویت منبع/شناسه/رکورد و وضعیت ثبت داده را مدیریت کند؛ ادعای مجوز، تعهد یا وضعیت واقعی از مسیر شواهد و مفاهیم تخصصی آن دامنه بیان شود. نبود داده «نامعلوم» بماند.
پیشنهاد N07: RegulatoryRequirement با زمینهٔ اعمال شامل قلمرو، نقش مخاطب، سناریو، موضوع، زمان و نسخهٔ منبع پیوند بخورد. فعلاً ایجاد کلاس تازه، قانون انطباق عمومی یا پیوند اجباری به تمام محصولات تصویب نشده است.
شکاف تازه: RegulatoryAuthorization موجود به AuthorizedParty سازمان/تأسیسات وصل می‌شود؛ این مسیر به‌تنهایی مدل مجوز محصول نیست. افزودن معنای product approval به آن بدون تصمیم علمی مجاز شمرده نشده است.
گام بعد: رفع هم‌پوشانی، انتخاب نیازهای ضروری نسخه، سپس ساخت شاهد مستقل و آزمون عدم‌استنتاج برای ۱۶ بند. چهار دامنهٔ محل بحث حفظ می‌شوند؛ جایگاه نهایی هنوز باز است.
