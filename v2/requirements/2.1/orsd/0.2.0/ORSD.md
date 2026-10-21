# CM PharmE 2.1 ORSD 0.2.0

Consolidated research specification baseline | 21 October 2026

## Scope of closure

Technical preparation of the document is complete for the declared scope. One author content review remains before freezing 1.0.0. This is not independent expert acceptance or an ontology release.

## Requirements

83 retained tracked rows; 71 functional, 12 quality; eight explicit scoped specializations. Thirteen local refinements stay attached; historical B2-DS-07 remains merged into R-DS-04.

### FR-01 Ecosystem Organization

مدل باید سازمان حقوقی را از تأسیسات فیزیکی متمایز کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S24
Question: کدام سازمان بهره‌بردار کدام تأسیسات است؟
Expected: یک سازمان و دو محل با شناسه مستقل قابل بازیابی باشند.
Positive: یک سازمان و دو محل با شناسه مستقل قابل بازیابی باشند.
Negative: همسان‌سازی سازمان و محل صرفاً به دلیل نام یا نشانی رد شود.
Anchors: Organization, Facility, FacilityOperation
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-02 Ecosystem Organization

مدل باید نقش یک سازمان را در زمینه رابطه مربوط مشخص کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S27
Question: سازمان در این رابطه چه نقشی دارد؟
Expected: نقش با رابطه زمینه‌ای قابل بازیابی باشد.
Positive: نقش با رابطه زمینه‌ای قابل بازیابی باشد.
Negative: نام شرکت به‌تنهایی اثبات نقش یا مسئولیت تلقی نشود.
Anchors: Organization, ManufacturerRole, ImporterRole, WholesaleDistributorRole
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-03 Facility Operations

مدل باید بهره‌برداری از تأسیسات را به سازمان مسئول پیوند دهد.

Disposition: RETAIN_SCOPED_SPECIALIZATION; parent: FR-02
Priority: Must candidate; sources: S27
Question: چه سازمانی این محل را اداره می‌کند؟
Expected: حامل سازمانی و محل تحت بهره‌برداری مشخص باشند.
Positive: حامل سازمانی و محل تحت بهره‌برداری مشخص باشند.
Negative: هم‌مکانی به‌تنهایی به بهره‌برداری تبدیل نشود.
Anchors: FacilityOperation, OperatingOrganizationRole, OperatedFacilityRole
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-04 Facility Operations

مدل باید استفاده از محل تولید را از مسئولیت تولید محصول متمایز کند.

Disposition: RETAIN_SCOPED_SPECIALIZATION; parent: FR-02
Priority: Must candidate; sources: S27
Question: آیا شاهد درباره محل تولید است یا مسئولیت تولید محصول؟
Expected: دو موضوع و روابط مربوط جدا قابل بازیابی باشند.
Positive: دو موضوع و روابط مربوط جدا قابل بازیابی باشند.
Negative: داشتن محل به‌تنهایی مسئولیت هر محصول را نتیجه ندهد.
Anchors: ManufacturingResponsibility, ManufacturingSiteUse, ManufacturingSiteRole
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-05 Regulatory Governance

مدل باید ثبت مؤسسه را به مرجع ثبت و موضوع ثبت متصل کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S26
Question: مرجع ثبت این سازمان یا محل کدام است؟
Expected: مرجع و موضوع ثبت با شاهد مشخص شوند.
Positive: مرجع و موضوع ثبت با شاهد مشخص شوند.
Negative: وجود رکورد بدون حل موضوع، ثبت قطعی موجودیت تلقی نشود.
Anchors: EstablishmentRegistration, RegisteredParty, RegisteringAuthorityRole
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-06 Regulatory Governance

مدل باید مجوز را در قلمرو مقرراتی مربوط تفسیر کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S29
Question: مجوز برای چه طرف و در چه قلمرویی معتبر گزارش شده است؟
Expected: طرف مجاز، مرجع و قلمرو معلوم یا صریحاً نامعلوم باشند.
Positive: طرف مجاز، مرجع و قلمرو معلوم یا صریحاً نامعلوم باشند.
Negative: مجوز یک قلمرو به قلمروی دیگر تعمیم داده نشود.
Anchors: RegulatoryAuthorization, AuthorizedParty, RegulatoryJurisdiction
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-07 Regulatory Governance

مدل باید نظارت مقرراتی را از داشتن مجوز متمایز کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S27
Question: چه مرجعی بر کدام موضوع نظارت دارد؟
Expected: رابطه نظارت مستقل قابل بیان باشد.
Positive: رابطه نظارت مستقل قابل بیان باشد.
Negative: نظارت به‌تنهایی داشتن مجوز یا انطباق را اثبات نکند.
Anchors: RegulatoryOversight, OversightAuthorityRole, GovernedEntity
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-08 Pharmaceutical Product

مدل باید محصول دارویی را از ماده دارویی متمایز کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S32
Question: محصول به کدام مواد فعال مربوط است؟
Expected: محصول و ماده با شناسه و نوع مستقل بازیابی شوند.
Positive: محصول و ماده با شناسه و نوع مستقل بازیابی شوند.
Negative: یکسان بودن نام ماده و محصول سبب ادغام هویت نشود.
Anchors: MedicinalProduct, PharmaceuticalSubstance
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-09 Pharmaceutical Product

مدل باید ارائه یا بسته عرضه‌شده را از محصول متمایز کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S32
Question: هر ارائه به کدام محصول تعلق دارد؟
Expected: دو بسته‌بندی از یک محصول با شناسه جدا نمایش داده شوند.
Positive: دو بسته‌بندی از یک محصول با شناسه جدا نمایش داده شوند.
Negative: دو بسته متفاوت فقط به دلیل محصول مشترک ادغام نشوند.
Anchors: MedicinalProduct, MedicinalProductPresentation, PackageConfiguration
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-10 Pharmaceutical Product

مدل باید قدرت یا غلظت را به موضوع دارویی مناسب نسبت دهد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S32
Question: قدرت یا غلظت این ارائه چیست؟
Expected: مقدار و موضوع قدرت با هم بازیابی شوند.
Positive: مقدار و موضوع قدرت با هم بازیابی شوند.
Negative: قدرت، هویت محصول یا تعداد بسته تلقی نشود.
Anchors: Strength, MedicinalProductPresentation
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-11 Pharmaceutical Product

مدل باید شکل دارویی را به‌صورت مشخصه قابل ارجاع نگه دارد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S32
Question: شکل دارویی این ارائه چیست؟
Expected: شکل دارویی با ارجاع منبع قابل بازیابی باشد.
Positive: شکل دارویی با ارجاع منبع قابل بازیابی باشد.
Negative: شکل دارویی به مسیر مصرف یا ماده فعال تقلیل داده نشود.
Anchors: DosageFormSpecification, MedicinalProductPresentation
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-12 Pharmaceutical Product

مدل باید تخصیص طبقه‌بندی محصول را همراه با نظام طبقه‌بندی نگه دارد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S32
Question: این کد در کدام نظام به چه محصولی تخصیص یافته است؟
Expected: کد، نظام و موضوع تخصیص هم‌زمان بازیابی شوند.
Positive: کد، نظام و موضوع تخصیص هم‌زمان بازیابی شوند.
Negative: کد طبقه‌بندی به‌تنهایی شناسه هویت محصول نشود.
Anchors: ProductClassificationAssignment, ProductClassificationScheme, ClassificationEntry
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-13 Supply Operations

مدل باید وابستگی عرضه را با دو طرف وابسته و فراهم‌کننده بیان کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S27
Question: چه موجودیتی به چه فراهم‌کننده‌ای وابسته است؟
Expected: دو طرف وابستگی با منبع و زمینه قابل ردیابی باشند.
Positive: دو طرف وابستگی با منبع و زمینه قابل ردیابی باشند.
Negative: صرف حضور در یک منبع، رابطه تأمین‌کننده و خریدار نسازد.
Anchors: SupplyDependency, DependentEntity, ProviderEntity
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-14 Supply Operations

مدل باید ظرفیت عرضه را به دقیقاً یک حامل واجد شرایط در پروفایل مصوب نسبت دهد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S12
Question: حامل این ظرفیت سازمان است یا تأسیسات؟
Expected: یک مسیر حامل سازمان یا محل پذیرفته شود.
Positive: یک مسیر حامل سازمان یا محل پذیرفته شود.
Negative: نبود حامل یا دو مسیر هم‌زمان در پروفایل XOR رد شود.
Anchors: SupplyCapacity, Organization, Facility
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-15 Supply Operations

مدل باید اندازه‌گیری ظرفیت را از خود ظرفیت متمایز کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S31
Question: کدام مشاهده درباره کدام ظرفیت یا موضوع عرضه است؟
Expected: مشاهده و ظرفیت هویت مستقل داشته باشند.
Positive: مشاهده و ظرفیت هویت مستقل داشته باشند.
Negative: وجود اندازه‌گیری به ایجاد بی‌دلیل یک ظرفیت ذاتی منجر نشود.
Anchors: SupplyCapacity, SupplyCapacityObservationResult
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-16 Supply Resilience

مدل باید وضعیت کمبود دارو را از گزارش آن متمایز کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S31
Question: آیا داده یک وضعیت کمبود را توصیف می‌کند یا فقط گزارشی درباره آن است؟
Expected: شاهد گزارش از موضوع وضعیت تفکیک شود.
Positive: شاهد گزارش از موضوع وضعیت تفکیک شود.
Negative: گزارش بالقوه یا نقل‌قول، وقوع کمبود را به‌تنهایی اثبات نکند.
Anchors: MedicineShortageSituation, SourceRecord, Assertion
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-17 Supply Resilience

مدل باید اثر اختلال بر وابستگی عرضه را به شواهد متصل کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Should candidate; sources: S23
Question: کدام وابستگی تحت اثر این اختلال گزارش شده است؟
Expected: مسیر اثر با موضوع، زمان و شاهد ثبت شود.
Positive: مسیر اثر با موضوع، زمان و شاهد ثبت شود.
Negative: هم‌زمانی دو گزارش به رابطه علّی تبدیل نشود.
Anchors: DisruptionEvent, SupplyDependency
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-18 Supply Resilience

مدل باید بحرانی بودن دارو را به زمینه طبقه‌بندی مقید کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S26
Question: دارو طبق کدام فهرست و در چه زمینه‌ای بحرانی است؟
Expected: فهرست، موضوع و زمینه طبقه‌بندی معلوم باشند.
Positive: فهرست، موضوع و زمینه طبقه‌بندی معلوم باشند.
Negative: بحرانی بودن در یک فهرست به حکم جهانی تبدیل نشود.
Anchors: ContextualMedicineClassificationAssignment, CriticalMedicineClassification
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-19 Supply Resilience

مدل باید ضروری بودن دارو را به زمینه طبقه‌بندی مقید کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S26
Question: دارو طبق کدام فهرست ضروری است؟
Expected: فهرست و نسخه یا تاریخ منبع قابل ارجاع باشند.
Positive: فهرست و نسخه یا تاریخ منبع قابل ارجاع باشند.
Negative: ضروری بودن با بحرانی بودن یکسان فرض نشود.
Anchors: ContextualMedicineClassificationAssignment, EssentialMedicineClassification
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-20 Supply Resilience

مدل باید گزینه جایگزین را نسبت به موضوع مرجع بیان کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Should candidate; sources: S27
Question: کدام دارو در چه زمینه‌ای جایگزین موضوع مرجع گزارش شده است؟
Expected: موضوع مرجع و جایگزین و شاهد قابل بازیابی باشند.
Positive: موضوع مرجع و جایگزین و شاهد قابل بازیابی باشند.
Negative: شباهت نام به معادل درمانی قطعی تبدیل نشود.
Anchors: AlternativeMedicineAssignment, AlternativeMedicinalProductRole, ReferenceProductRole
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-21 Spatiotemporal Context

مدل باید جغرافیای فیزیکی را از قلمرو مقرراتی متمایز کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S29
Question: موقعیت محل چیست و قلمرو حاکم کدام است؟
Expected: موقعیت و قلمرو دو نقش معنایی مجزا داشته باشند.
Positive: موقعیت و قلمرو دو نقش معنایی مجزا داشته باشند.
Negative: نام کشور به‌تنهایی هم‌هویتی جغرافیا و قلمرو نسازد.
Anchors: GeographicFeature, RegulatoryJurisdiction, Facility
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-22 Spatiotemporal Context

مدل باید دقت زمانی شاهد را حفظ کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S19
Question: تاریخ شاهد در حد روز است یا ماه یا سال؟
Expected: نقش تاریخ و دقت آن حفظ شود.
Positive: نقش تاریخ و دقت آن حفظ شود.
Negative: از تاریخ ماهانه یا زمان انتشار، لحظه دقیق رخداد ساخته نشود.
Anchors: TimeInterval, ReportingPeriod
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-23 Ecosystem Observation

مدل باید نتیجه مشاهده را از فعالیت مشاهده متمایز کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S31
Question: چه نتیجه‌ای از کدام فعالیت مشاهده حاصل شده است؟
Expected: هویت رخداد و نتیجه جدا بازیابی شوند.
Positive: هویت رخداد و نتیجه جدا بازیابی شوند.
Negative: نبود نتیجه منتشرشده به نبود رخداد تعبیر نشود.
Anchors: ObservationResult, ObservationActivity
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-24 Market Access

مدل باید مشاهده بازپرداخت یا مصرف را با زمینه آن نگه دارد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Should candidate; sources: S32
Question: این مقدار برای چه موضوع و دوره و جغرافیایی گزارش شده است؟
Expected: موضوع، دوره، منطقه و رکورد منبع همراه مقدار باشند.
Positive: موضوع، دوره، منطقه و رکورد منبع همراه مقدار باشند.
Negative: مصرف تجمیعی به شمار بیماران یکتا یا دسترسی قطعی تبدیل نشود.
Anchors: ReimbursementUtilisationObservationResult, ReportingPeriod, GeographicFeature
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-25 Evidence Traceability

مدل باید زنجیره مجموعه‌داده تا نسخه و رکورد را نگه دارد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S31
Question: این رکورد از کدام نسخه مجموعه‌داده آمده است؟
Expected: هر رکورد پذیرفته‌شده به نسخه منبع قابل ردیابی باشد.
Positive: هر رکورد پذیرفته‌شده به نسخه منبع قابل ردیابی باشد.
Negative: دو نسخه منبع بدون ثبت تفاوت ادغام نشوند.
Anchors: Dataset, DatasetRelease, SourceRecord
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-26 Evidence Traceability

مدل باید پشتیبانی یک ادعا را به شاهد مشخص متصل کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S31
Question: کدام شاهد از این ادعا پشتیبانی می‌کند؟
Expected: هر پشتیبانی به ادعا و شاهد اشاره کند.
Positive: هر پشتیبانی به ادعا و شاهد اشاره کند.
Negative: استناد کلی به ناشر جای شاهد ادعا ننشیند.
Anchors: EvidenceSupport, SourceRecord, Assertion
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-27 Evidence Traceability

مدل باید یافته کیفیت داده را از واقعیت موضوع متمایز کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Should candidate; sources: S31
Question: کدام نقص در داده یا نگاشت ثبت شده است؟
Expected: نقص، موضوع و منبع ثبت شوند.
Positive: نقص، موضوع و منبع ثبت شوند.
Negative: نبود داده به نقض واقعی یا نبود موجودیت تبدیل نشود.
Anchors: DataQualityFinding, MappingAssertion, SourceRecord
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-28 Entity Identity

مدل باید شناسه را همراه با نظام صادرکننده و موضوع آن نگه دارد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S30
Question: این مقدار در کدام نظام به چه موجودیتی اشاره دارد؟
Expected: مقدار، نظام و موضوع تخصیص هم‌زمان بازیابی شوند.
Positive: مقدار، نظام و موضوع تخصیص هم‌زمان بازیابی شوند.
Negative: برابری رشته در دو نظام سبب هم‌هویتی نشود.
Anchors: IdentifierAssignment, IdentifierScheme, IdentifierValue, IdentifiedEntity
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-29 Entity Identity

مدل باید تطبیق بین منابع را با شاهد و اطمینان صریح نگه دارد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Should candidate; sources: S30
Question: چرا این دو رکورد به یک موجودیت نامزد شده‌اند؟
Expected: دو طرف و شاهد و وضعیت تطبیق موجود باشند.
Positive: دو طرف و شاهد و وضعیت تطبیق موجود باشند.
Negative: تطبیق احتمالی خودکار به owl sameAs قطعی تبدیل نشود.
Anchors: EntityMatchAssertion, MatchConfidence, MappingAssertion
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-30 Regulatory Policy

مدل باید محتوای الزام را از سند حامل آن متمایز کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S31
Question: کدام سند چه الزام قابل اعمالی را بیان می‌کند؟
Expected: رابطه سند و محتوای الزام قابل ردیابی باشد.
Positive: رابطه سند و محتوای الزام قابل ردیابی باشد.
Negative: وجود سند عمومی سبب تعهد همه بازیگران نشود.
Anchors: RegulatoryRequirement, SourceRecord
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-31 Evidence Traceability

مدل باید تعارض ادعاهای منابع را بدون ادغام خودکار حفظ کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Should candidate; sources: S22
Question: کدام منابع درباره یک موضوع ادعاهای متفاوت دارند؟
Expected: دو ادعا و دو انتساب منبع مستقل باقی بمانند.
Positive: دو ادعا و دو انتساب منبع مستقل باقی بمانند.
Negative: اختلاف ادعا با حذف یکی یا منفی‌سازی جهانی حل نشود.
Anchors: Assertion, SourceRecord
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### FR-32 Facility Operations

مدل باید نقش توزیع محل را از نقش توزیع سازمان متمایز کند.

Disposition: RETAIN_SCOPED_SPECIALIZATION; parent: FR-02
Priority: Must candidate; sources: S27
Question: کدام سازمان و کدام محل در توزیع مشارکت دارند؟
Expected: نقش محل و نقش سازمان با زمینه مجزا بیان شوند.
Positive: نقش محل و نقش سازمان با زمینه مجزا بیان شوند.
Negative: مجوز یا نقش سازمان خودکار به همه محل‌های آن منتقل نشود.
Anchors: DistributionSiteRole, WholesaleDistributorRole, DistributionSiteUse
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### R-RM-01 Risk Management

موضوع هر ارزیابی ریسک باید به زمینهٔ دارویی مشخص قابل ردیابی باشد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S08, S17
Question: موضوع این ارزیابی ریسک کدام محصول یا محل یا وابستگی عرضه است؟
Expected: پرسش، محصول/تأسیسات/وابستگی موضوع را برگرداند؛ موضوع نامعلوم به‌عنوان نقص اطلاعات مشخص شود.
Positive: پرسش، محصول/تأسیسات/وابستگی موضوع را برگرداند؛ موضوع نامعلوم به‌عنوان نقص اطلاعات مشخص شود.
Negative: ارزیابی فاقد سناریو یا موضوع مشخص در پروفایل کامل رد شود.
Anchors: assessmentScenario, scenarioProduct
Model comparison: EXPERIMENTAL_ONLY; semantic approval: PENDING_SEMANTIC_REVIEW

### R-RM-02 Risk Management

نتیجهٔ هر ارزیابی باید از رخداد انجام ارزیابی متمایز باشد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S08, S17
Question: رخداد ارزیابی و محتوای نتیجه آن چه شناسه های مستقلی دارند؟
Expected: شناسه نتیجه و رخداد قابل تفکیک باشند؛ نبود نتیجهٔ منتشرشده به معنی نبود رخداد نیست.
Positive: شناسه نتیجه و رخداد قابل تفکیک باشند؛ نبود نتیجهٔ منتشرشده به معنی نبود رخداد نیست.
Negative: همسان سازی رخداد ارزیابی با محتوای نتیجه رد شود.
Anchors: resultAssessment
Model comparison: EXPERIMENTAL_ONLY; semantic approval: PENDING_SEMANTIC_REVIEW

### R-RM-03 Risk Management

مبنای شواهد هر نتیجهٔ ارزیابی باید قابل بازیابی باشد.

Disposition: RETAIN_SCOPED_SPECIALIZATION; parent: FR-26
Priority: Must candidate; sources: S08, S17
Question: کدام رکورد یا ادعا از نتیجه ارزیابی پشتیبانی می کند؟
Expected: نتیجهٔ پذیرفته‌شده در پروفایل داده به حداقل یک SourceRecord/Assertion متصل باشد.
Positive: نتیجهٔ پذیرفته‌شده در پروفایل داده به حداقل یک SourceRecord/Assertion متصل باشد.
Negative: نتیجه فاقد شاهد در پروفایل کامل پذیرفته نشود.
Anchors: citesSourceRecord
Model comparison: EXPERIMENTAL_ONLY; semantic approval: PENDING_SEMANTIC_REVIEW

### R-RM-04 Risk Management

برنامهٔ رسیدگی باید به نتیجهٔ ارزیابی موردنظر متصل باشد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S08, S17
Question: این برنامه رسیدگی به کدام نتیجه ارزیابی پاسخ می دهد؟
Expected: پرسش برنامه فقط ارزیابی‌های تصریح‌شده را برگرداند.
Positive: پرسش برنامه فقط ارزیابی‌های تصریح‌شده را برگرداند.
Negative: برنامه با ارجاع آویزان به نتیجه رد شود.
Anchors: planRiskResult
Model comparison: EXPERIMENTAL_ONLY; semantic approval: PENDING_SEMANTIC_REVIEW

### R-RM-05 Risk Management

وقوع اقدام رسیدگی باید مستقل از وجود برنامه قابل تشخیص باشد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S08, S17
Question: برای کدام برنامه ها اجرای رسیدگی در این مجموعه داده ثبت شده است؟
Expected: وجود برنامه بدون رخداد، اجرای اقدام را نتیجه ندهد.
Positive: وجود برنامه بدون رخداد، اجرای اقدام را نتیجه ندهد.
Negative: از برنامه بدون شاهد اجرا، رخداد رسیدگی یا اثربخشی استنتاج نشود.
Anchors: implementsRiskPlan
Model comparison: EXPERIMENTAL_ONLY; semantic approval: PENDING_SEMANTIC_REVIEW

### R-RM-06 Risk Management

هر بازبینی باید نتیجهٔ پیشین مورد بازبینی را مشخص کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S08, S17
Question: این بازبینی کدام نتیجه پیشین را به کدام نتیجه تازه متصل می کند؟
Expected: زنجیره نسخه/زمان نتیجه‌های قبلی حفظ شود.
Positive: زنجیره نسخه/زمان نتیجه‌های قبلی حفظ شود.
Negative: بازبینی فاقد نتیجه پیشین یا با ترتیب زمانی نامعتبر رد شود.
Anchors: reviewPriorResult, reviewNewResult, atTime
Model comparison: EXPERIMENTAL_ONLY; semantic approval: PENDING_SEMANTIC_REVIEW

### R-PV-01 Pharmacovigilance

اطلاعات گزارش ایمنی باید از رخداد گزارش‌کردن متمایز باشد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S08, S16
Question: کدام رکورد حاوی گزارش است و رخداد گزارش کردن کدام است؟
Expected: بازارسال همان محتوا، رخداد جدید را بدون ادغام خودکار گزارش‌ها ثبت کند.
Positive: بازارسال همان محتوا، رخداد جدید را بدون ادغام خودکار گزارش‌ها ثبت کند.
Negative: همسان سازی حامل گزارش با رخداد گزارش کردن رد شود.
Anchors: reportsRecord
Model comparison: EXPERIMENTAL_ONLY; semantic approval: PENDING_SEMANTIC_REVIEW

### R-PV-02 Pharmacovigilance

موضوع سیگنال باید به محصول یا مادهٔ دارویی مشخص متصل باشد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S08, S16
Question: موضوع این سیگنال کدام محصول یا ماده دارویی است؟
Expected: سیگنال ماده‌ای بدون اجبار ساختن یک برند قابل ثبت باشد.
Positive: سیگنال ماده‌ای بدون اجبار ساختن یک برند قابل ثبت باشد.
Negative: سیگنال فاقد موضوع یا با موضوع ناسازگار در پروفایل کامل رد شود.
Anchors: signalProduct, signalSubstance
Model comparison: EXPERIMENTAL_ONLY; semantic approval: PENDING_SEMANTIC_REVIEW

### R-PV-03 Pharmacovigilance

پشتوانهٔ هر سیگنال باید به منابع آن قابل ردیابی باشد.

Disposition: RETAIN_SCOPED_SPECIALIZATION; parent: FR-26
Priority: Must candidate; sources: S08, S16
Question: کدام منابع از این سیگنال پشتیبانی می کنند؟
Expected: منبع ادعاشده موجود و قابل ارجاع باشد؛ نبود گزارش فردی سیگنال مبتنی بر مطالعه را رد نکند.
Positive: منبع ادعاشده موجود و قابل ارجاع باشد؛ نبود گزارش فردی سیگنال مبتنی بر مطالعه را رد نکند.
Negative: سیگنال فاقد ارجاع شاهد در پروفایل کامل رد شود.
Anchors: citesSourceRecord
Model comparison: EXPERIMENTAL_ONLY; semantic approval: PENDING_SEMANTIC_REVIEW

### R-PV-04 Pharmacovigilance

هر نتیجهٔ ارزیابی باید به سیگنال مورد ارزیابی متصل باشد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S08, S16
Question: این نتیجه به ارزیابی کدام سیگنال تعلق دارد؟
Expected: سیگنال و نتیجهٔ ارزیابی آن شناسه و نوع متمایز داشته باشند.
Positive: سیگنال و نتیجهٔ ارزیابی آن شناسه و نوع متمایز داشته باشند.
Negative: یکی بودن نتیجه با سیگنال یا اختلاف موضوع نتیجه و ارزیابی رد شود.
Anchors: pvResultSignal, pvResultAssessment, signalAssessmentTarget
Model comparison: EXPERIMENTAL_ONLY; semantic approval: PENDING_SEMANTIC_REVIEW

### R-PV-05 Pharmacovigilance

وضعیت نتیجهٔ ارزیابی باید به زمان ارزیابی مقید باشد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S08, S16
Question: وضعیت نتیجه در چه زمان ارزیابی گزارش شده است؟
Expected: نتیجهٔ بازبینی، تاریخچهٔ قبلی را پاک نکند.
Positive: نتیجهٔ بازبینی، تاریخچهٔ قبلی را پاک نکند.
Negative: نتیجه فاقد زمان یا وضعیت لازم در پروفایل کامل رد شود.
Anchors: atTime, signalStatus
Model comparison: EXPERIMENTAL_ONLY; semantic approval: PENDING_SEMANTIC_REVIEW

### R-PV-06 Pharmacovigilance

اعمال الزام فارماکوویژیلانس باید به قلمرو مقرراتی مشخص مقید باشد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S08, S16
Question: این الزام در کدام قلمرو مقرراتی اعمال می شود؟
Expected: الزام منطقه A به‌طور خودکار به منطقه B تعمیم نیابد.
Positive: الزام منطقه A به‌طور خودکار به منطقه B تعمیم نیابد.
Negative: الزام فاقد قلمرو در پروفایل کامل پذیرفته نشود.
Anchors: pvRequirementJurisdiction, surveillanceRequirement
Model comparison: EXPERIMENTAL_ONLY; semantic approval: PENDING_SEMANTIC_REVIEW

### R-BA-01 Business Architecture

هر EnterpriseCapability باید حامل سازمانی مشخص داشته باشد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S08, S14
Question: حامل سازمانی این قابلیت کدام است؟
Expected: حامل با رابطه موجود capabilityBearer قابل بازیابی باشد؛ Mode بی‌حامل در پروفایل کامل رد شود.
Positive: حامل با رابطه موجود capabilityBearer قابل بازیابی باشد؛ Mode بی‌حامل در پروفایل کامل رد شود.
Negative: قابلیت فاقد حامل سازمانی در پروفایل کامل رد شود.
Anchors: capabilityBearer
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### R-BA-02 Business Architecture

وجود قابلیت نباید وقوع فعالیت متناظر را الزام کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S08, S14
Question: کدام قابلیت در گراف بررسی شده فاقد اجرای لجستیک ثبت شده است؟
Expected: در گراف داده مورد آزمون، قابلیت فاقد اجرای ثبت شده بازیابی شود؛ قابلیت دارای اجرای ثبت شده در همان رابطه بازیابی نشود. جداگانه، وجود قابلیت بدون هیچ تحقق در این رابطه با مدل OWL سازگار بماند.
Positive: سازمان دارای قابلیت غیرفعال مجاز باشد.
Negative: وجود قابلیت بدون اجرای ثبت شده باید سازگار بماند؛ اجرای اجباری از قابلیت استنتاج نشود.
Anchors: capabilityRealizedInLogistics
Model comparison: EXPERIMENTAL_ONLY; semantic approval: PENDING_SEMANTIC_REVIEW

### R-BA-03 Business Architecture

ServiceOfferingSpecification باید به موضوع خدمت دارویی متصل باشد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S08, S14
Question: مشخصات این خدمت به کدام موضوع دارویی مربوط است؟
Expected: حداقل یک قابلیت/فعالیت/محصول مرتبط در پروفایل پذیرفته‌شده مشخص باشد.
Positive: حداقل یک قابلیت/فعالیت/محصول مرتبط در پروفایل پذیرفته‌شده مشخص باشد.
Negative: خدمت فاقد زمینه دارویی در پروفایل کامل رد شود.
Anchors: serviceCapability
Model comparison: EXPERIMENTAL_ONLY; semantic approval: PENDING_SEMANTIC_REVIEW

### R-BA-04 Business Architecture

BusinessArchitectureView باید به شناسه‌های موجودیت‌های اصلی ارجاع دهد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Should candidate; sources: S08, S14
Question: این نمای معماری به کدام موجودیت های اصلی ارجاع می دهد؟
Expected: نمای جدید برای یک سازمان، سازمان دوم ایجاد نکند.
Positive: نمای جدید برای یک سازمان، سازمان دوم ایجاد نکند.
Negative: ارجاع آویزان نمای معماری به سازمان یا خدمت رد شود.
Anchors: viewOrganization, viewService
Model comparison: EXPERIMENTAL_ONLY; semantic approval: PENDING_SEMANTIC_REVIEW

### R-BA-05 Business Architecture

مشارکت در StrategicPartnershipAgreement باید از تعامل اتفاقی متمایز باشد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S08, S14
Question: چه تعهد یا توافقی مشارکت این سازمان ها را توجیه می کند؟
Expected: تعامل بدون شاهد تعهد، خودکار PartnerOrganizationRole نسازد.
Positive: تعامل بدون شاهد تعهد، خودکار PartnerOrganizationRole نسازد.
Negative: همکاری اتفاقی یا سند برنامه بدون تعهد مستند، توافق راهبردی قطعی تلقی نشود.
Anchors: partnershipParticipant
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### R-BA-06 Business Architecture

هویت موجودیت‌های هسته باید مستقل از وجود نمای معماری بماند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Should candidate; sources: S08, S14
Question: آیا هویت سازمان و خدمت بدون وجود نمای معماری محفوظ می ماند؟
Expected: حذف نمای اختیاری، هویت یا طبقه‌بندی اجباری محصول و تأسیسات را تغییر ندهد.
Positive: حذف نمای اختیاری، هویت یا طبقه‌بندی اجباری محصول و تأسیسات را تغییر ندهد.
Negative: حذف نمای معماری سبب حذف یا تغییر هویت موجودیت اصلی نشود.
Anchors: viewOrganization
Model comparison: EXPERIMENTAL_ONLY; semantic approval: PENDING_SEMANTIC_REVIEW

### R-DS-01 Digital Systems

هویت جزء سامانه باید از هویت رکورد تولیدشده متمایز باشد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S08, S15
Question: جزء سامانه و رکورد تولیدشده چه هویت های مستقلی دارند؟
Expected: سامانه و SourceRecord شناسه و نوع قابل تفکیک داشته باشند.
Positive: سامانه و SourceRecord شناسه و نوع قابل تفکیک داشته باشند.
Negative: همسان سازی جزء سامانه با رکورد تولیدشده رد شود.
Anchors: recordDigitalActivity, deploymentComponent
Model comparison: EXPERIMENTAL_ONLY; semantic approval: PENDING_SEMANTIC_REVIEW

### R-DS-02 Digital Systems

نسخه جزء سامانهٔ استفاده‌شده باید قابل بازیابی باشد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Should candidate; sources: S08, S15
Question: کدام نسخه جزء سامانه در این فعالیت استفاده شده است؟
Expected: دو اجرای دارای نسخه‌های مختلف در ردیابی ادغام نشوند.
Positive: دو اجرای دارای نسخه‌های مختلف در ردیابی ادغام نشوند.
Negative: نسخه نامعلوم با مقدار ساختگی تکمیل نشود؛ پروفایل استقرار کامل آن را رد کند.
Anchors: digitalActivityDeployment, componentVersion
Model comparison: EXPERIMENTAL_ONLY; semantic approval: PENDING_SEMANTIC_REVIEW

### R-DS-03 Digital Systems

رابطه پشتیبانی سامانه باید به فعالیت دارویی مشخص متصل باشد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S08, S15
Question: این جزء یا خدمت دیجیتال از کدام فعالیت دارویی پشتیبانی می کند؟
Expected: نام بردن سامانه بدون فعالیت مرتبط، پوشش عملکرد دامنه شمرده نشود.
Positive: نام بردن سامانه بدون فعالیت مرتبط، پوشش عملکرد دامنه شمرده نشود.
Negative: خدمت دیجیتال بدون موضوع فعالیت دارویی، پشتیبانی عملیاتی کامل تلقی نشود.
Anchors: digitalServiceActivity, digitalServiceComponent
Model comparison: EXPERIMENTAL_ONLY; semantic approval: PENDING_SEMANTIC_REVIEW

### R-DS-04 Digital Systems

منشأ رکورد باید از مسیر فعالیت تولیدکننده قابل ردیابی باشد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S08, S15, S21
Question: رکورد از چه فعالیت داده و کدام استقرار تولید شده است؟
Expected: مسیر رکورد→فعالیت→جزء/نسخه و عامل مسئول برای پروفایل کامل قابل پرس‌وجو باشد.
Positive: مسیر رکورد→فعالیت→جزء/نسخه و عامل مسئول برای پروفایل کامل قابل پرس‌وجو باشد.
Negative: فعالیت داده مفقود با رکورد یکسان انگاشته نشود؛ مسیر کامل منشأ کنترل شود.
Anchors: recordDigitalActivity, digitalActivityDeployment, deploymentComponent, deploymentOrganization
Model comparison: EXPERIMENTAL_ONLY; semantic approval: PENDING_SEMANTIC_REVIEW

### R-DS-05 Digital Systems

هر استقرار باید زمان وقوع مشخص داشته باشد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Should candidate; sources: S08, S15
Question: استقرار این نسخه در چه زمان و زمینه ای رخ داده است؟
Expected: تغییر نسخه با رخداد استقرار جدید و حفظ تاریخچه نمایش داده شود.
Positive: تغییر نسخه با رخداد استقرار جدید و حفظ تاریخچه نمایش داده شود.
Negative: تاریخ انتشار اطلاعیه به لحظه دقیق استقرار تبدیل نشود.
Anchors: atTime, componentVersion
Model comparison: EXPERIMENTAL_ONLY; semantic approval: PENDING_SEMANTIC_REVIEW

### R-DS-06 Digital Systems

وجود رکورد دیجیتال نباید به‌تنهایی مجوز مقرراتی ایجاد کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S08, S15
Question: آیا صرف وجود رکورد دیجیتال، مجوز مقرراتی را نتیجه می دهد؟
Expected: رکورد رجیستری بدون شاهد مجوز، RegulatoryAuthorization استنتاج نکند.
Positive: رکورد رجیستری بدون شاهد مجوز، RegulatoryAuthorization استنتاج نکند.
Negative: رکورد یا حضور دیجیتال به تنهایی مجوز مقرراتی ایجاد نکند.
Anchors: recordDigitalActivity
Model comparison: EXPERIMENTAL_ONLY; semantic approval: PENDING_SEMANTIC_REVIEW

### B2-RG-01 Registry

ثبت مؤسسه باید از فهرست‌شدن محصول متمایز بماند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S21
Question: Which subject is registered or listed?
Expected: Facility registration and product listing remain distinct.
Positive: Facility registration and product listing remain distinct.
Negative: Registration alone cannot create a product listing.
Anchors: EstablishmentRegistration, MarketListing, rel-registrationEntity, rel-listingPresentation
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### B2-RG-02 Registry

ثبت مؤسسه نباید به‌تنهایی مجوز محصول را نتیجه دهد.

Disposition: RETAIN_SCOPED_SPECIALIZATION; parent: R-DS-06
Priority: Must candidate; sources: S21
Question: Does registration establish approval?
Expected: Answer unknown without approval evidence.
Positive: Answer unknown without approval evidence.
Negative: Reject registration-to-approval inference.
Anchors: EstablishmentRegistration, RegulatoryAuthorization
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### B2-RG-03 Registry

فهرست‌شدن NDC نباید به‌تنهایی تأیید محصول را نتیجه دهد.

Disposition: RETAIN_SCOPED_SPECIALIZATION; parent: R-DS-06
Priority: Must candidate; sources: S21
Question: What approval evidence supports this product?
Expected: Listed product may have unknown approval.
Positive: Listed product may have unknown approval.
Negative: NDC presence cannot supply approval evidence.
Anchors: IdentifierAssignment, IdentifierScheme, MarketListing, EvidenceSupport
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### B2-RG-04 Registry

اطلاعات تسلیم‌شده به دایرکتوری باید به تسلیم‌کننده منتسب شود.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S21
Question: Who supplied this entry?
Expected: Return submitting labeler.
Positive: Return submitting labeler.
Negative: Do not substitute FDA verification.
Anchors: SourceRecord, Organization, Assertion
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### B2-RG-05 Registry

نبود مدخل در دایرکتوری باید وضعیت نامعلوم را حفظ کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S21
Question: What follows from a missing entry?
Expected: Return not-found within this source.
Positive: Return not-found within this source.
Negative: Do not infer unapproved or nonexistent.
Anchors: SourceRecord, DatasetRelease
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### B2-RG-06 Registry

تاریخ بازاریابی باید از تاریخ دریافت داده متمایز بماند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S21
Question: Was the entry published at the queried time?
Expected: Apply declared source publication conditions.
Positive: Apply declared source publication conditions.
Negative: Do not equate retrieval with marketing start.
Anchors: SourceRecord, DatasetRelease, MarketListing, TimeInterval
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### B2-RP-01 Regulatory Policy

اعمال تعهد گزارش‌دهی باید با نقش مخاطب و سناریو مقید شود.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S21
Question: Who reports under this scenario?
Expected: Return applicable MAH/NCA roles.
Positive: Return applicable MAH/NCA roles.
Negative: Do not generalize one scenario globally.
Anchors: RegulatoryRequirement, Organization, RegulatoryJurisdiction
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### B2-RP-02 Regulatory Policy

گزارش کمبود بالقوه باید از وضعیت کمبود واقعی متمایز بماند.

Disposition: RETAIN_SCOPED_SPECIALIZATION; parent: FR-16
Priority: Must candidate; sources: S21
Question: Is this a forecast or actual shortage?
Expected: Potential report remains an assertion.
Positive: Potential report remains an assertion.
Negative: Forecast alone cannot establish actual shortage.
Anchors: Assertion, MedicineShortageSituation, SourceRecord
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### B2-RP-03 Regulatory Policy

دامنه محصول در گزارش‌دهی باید با سناریوی انتخاب‌شده سازگار باشد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S21
Question: Are CAPs, NAPs or selected medicines in scope?
Expected: Use the scenario-specific scope.
Positive: Use the scenario-specific scope.
Negative: Do not apply routine CAP scope universally.
Anchors: RegulatoryRequirement, MedicinalProduct, ContextualMedicineClassificationAssignment
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### B2-RP-04 Regulatory Policy

تناوب گزارش‌دهی باید به اقدام اعلام‌شده متصل شود.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Should candidate; sources: S21
Question: Which frequency applies to this action?
Expected: Retrieve that action’s frequency.
Positive: Retrieve that action’s frequency.
Negative: Do not hard-code a universal interval.
Anchors: RegulatoryRequirement, ReportingPeriod, TimeInterval
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### B2-DS-08 Digital Systems

انتساب یک رکورد باید از مسئولیت عامل در فعالیت متمایز بماند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S21
Question: Is responsibility attached to artifact or activity?
Expected: Return the qualified relation.
Positive: Return the qualified relation.
Negative: Do not collapse both predicates.
Anchors: SourceRecord, ProvenanceActivity, Organization
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### B2-DS-09 Digital Systems

زنجیره اشتقاق بین مصنوعات داده باید حفظ شود.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S21
Question: Which artifact was this derived from?
Expected: Return predecessor lineage.
Positive: Return predecessor lineage.
Negative: Source absence cannot invent lineage.
Anchors: SourceRecord, Dataset, DatasetRelease
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### B2-DS-10 Digital Systems

بازنگری محتوا نباید به ادغام خودکار هویت نسخه‌ها منجر شود.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Should candidate; sources: S21
Question: Which prior version was revised?
Expected: Keep both versions and revision link.
Positive: Keep both versions and revision link.
Negative: Revision alone must not assert owl:sameAs.
Anchors: SourceRecord, DatasetRelease
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### B2-RG-07 Registry

موضوع ثبت باید از سازمان گزارش‌دهنده متمایز باشد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S21
Question: Which organization reported on which establishment?
Expected: An organizational subject may report on itself; record identity remains separate.
Positive: An organizational subject may report on itself; record identity remains separate.
Negative: Reject record-subject identity collision, including known owl:sameAs aliases.
Anchors: RegisteredFacilityRole, RegisteredOrganizationRole, SourceRecord
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### B2-RG-08 Registry

SPL باید به‌صورت بازنمایی تسلیم‌شده تفسیر شود.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S21
Question: Which submission represents the listed drug?
Expected: Trace submission to represented subject.
Positive: Trace submission to represented subject.
Negative: Do not identify payload with physical product.
Anchors: SourceRecord, MedicinalProduct, Assertion
Model comparison: NATIVE_VOCABULARY_ALL_ANCHORS; semantic approval: PENDING_SEMANTIC_REVIEW

### NFR-01 Cross cutting quality

شناسه‌های مفاهیم و روابط باید در هر نسخه پایدار و تغییرات آن‌ها قابل ردیابی باشد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S28
Question: Quality protocol
Expected: دو اجرای ساخت با ورودی یکسان شناسه‌های یکسان بدهند؛ تغییر هویت در changelog ثبت شود.
Positive: دو اجرای ساخت با ورودی یکسان شناسه‌های یکسان بدهند؛ تغییر هویت در changelog ثبت شود.
Negative: خروجی فاقد این شاهد نباید وضعیت کامل یا پذیرفته بگیرد.
Anchors: 
Model comparison: QUALITY_REVIEW_REQUIRED; semantic approval: PENDING_SEMANTIC_REVIEW

### NFR-02 Cross cutting quality

هر ماژول باید مأموریت و مرز مالکیت واژگان مشخص داشته باشد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S13
Question: Quality protocol
Expected: قرارداد ورودی و خروجی و owned و imported ثبت شود؛ ارجاع شکسته رد شود.
Positive: قرارداد ورودی و خروجی و owned و imported ثبت شود؛ ارجاع شکسته رد شود.
Negative: خروجی فاقد این شاهد نباید وضعیت کامل یا پذیرفته بگیرد.
Anchors: 
Model comparison: QUALITY_REVIEW_REQUIRED; semantic approval: PENDING_SEMANTIC_REVIEW

### NFR-03 Cross cutting quality

نگاشت OntoUML و OWL و قیود داده باید تفاوت معنای هر نمایش را حفظ کند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S18
Question: Quality protocol
Expected: تبدیل فاقد نگاشت معتبر با گزارش خطا متوقف شود؛ معنای گمشده صریح ثبت شود.
Positive: تبدیل فاقد نگاشت معتبر با گزارش خطا متوقف شود؛ معنای گمشده صریح ثبت شود.
Negative: خروجی فاقد این شاهد نباید وضعیت کامل یا پذیرفته بگیرد.
Anchors: 
Model comparison: QUALITY_REVIEW_REQUIRED; semantic approval: PENDING_SEMANTIC_REVIEW

### NFR-04 Cross cutting quality

سازگاری و ناتهی‌پذیری کلاس‌های مصوب باید با ریزنر کنترل شود.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S12
Question: Quality protocol
Expected: ریزنر و نسخه و ورودی ثبت شود؛ تناقض تزریق‌شده تشخیص داده شود.
Positive: ریزنر و نسخه و ورودی ثبت شود؛ تناقض تزریق‌شده تشخیص داده شود.
Negative: خروجی فاقد این شاهد نباید وضعیت کامل یا پذیرفته بگیرد.
Anchors: 
Model comparison: QUALITY_REVIEW_REQUIRED; semantic approval: PENDING_SEMANTIC_REVIEW

### NFR-05 Cross cutting quality

قیود پذیرش داده باید روی نمونه‌های مثبت و منفی سنجیده شوند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S01
Question: Quality protocol
Expected: داده معتبر پذیرفته و نقص هدفمند رد شود؛ معیار موردانتظار پیش از اجرا ثبت شود.
Positive: داده معتبر پذیرفته و نقص هدفمند رد شود؛ معیار موردانتظار پیش از اجرا ثبت شود.
Negative: خروجی فاقد این شاهد نباید وضعیت کامل یا پذیرفته بگیرد.
Anchors: 
Model comparison: QUALITY_REVIEW_REQUIRED; semantic approval: PENDING_SEMANTIC_REVIEW

### NFR-06 Cross cutting quality

الگوها و ضدالگوها باید با دامنه کاربرد و محدودیت ابزار گزارش شوند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S18
Question: Quality protocol
Expected: اجرای مدل کامل از toy جدا باشد؛ اختلاف منبع و ابزار با تصمیم ثبت شود.
Positive: اجرای مدل کامل از toy جدا باشد؛ اختلاف منبع و ابزار با تصمیم ثبت شود.
Negative: خروجی فاقد این شاهد نباید وضعیت کامل یا پذیرفته بگیرد.
Anchors: 
Model comparison: QUALITY_REVIEW_REQUIRED; semantic approval: PENDING_SEMANTIC_REVIEW

### NFR-07 Cross cutting quality

پرسش‌های هم‌معنا در SQL و SPARQL باید روی ورودی ثابت مقایسه شوند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Should candidate; sources: S05
Question: Quality protocol
Expected: پاسخ مرتب و نرمال‌شده یکسان باشد؛ اختلاف join و null و هویت تحلیل شود.
Positive: پاسخ مرتب و نرمال‌شده یکسان باشد؛ اختلاف join و null و هویت تحلیل شود.
Negative: خروجی فاقد این شاهد نباید وضعیت کامل یا پذیرفته بگیرد.
Anchors: 
Model comparison: QUALITY_REVIEW_REQUIRED; semantic approval: PENDING_SEMANTIC_REVIEW

### NFR-08 Cross cutting quality

ساخت نتایج باید از ورودی نسخه‌دار قابل بازتولید باشد.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S06
Question: Quality protocol
Expected: manifest شامل hash و دستور ساخت و نسخه وابستگی باشد؛ اجرای CI جدا ثبت شود.
Positive: manifest شامل hash و دستور ساخت و نسخه وابستگی باشد؛ اجرای CI جدا ثبت شود.
Negative: خروجی فاقد این شاهد نباید وضعیت کامل یا پذیرفته بگیرد.
Anchors: 
Model comparison: QUALITY_REVIEW_REQUIRED; semantic approval: PENDING_SEMANTIC_REVIEW

### NFR-09 Cross cutting quality

منابع ارزیابی مستقل باید از منابع کشف تمیز داده شوند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S26
Question: Quality protocol
Expected: منبع held out در بازسازی این نسخه برای توجیه پذیرش مفهوم مصرف نشود؛ مصرف بعدی با برچسب ثبت شود.
Positive: منبع held out در بازسازی این نسخه برای توجیه پذیرش مفهوم مصرف نشود؛ مصرف بعدی با برچسب ثبت شود.
Negative: خروجی فاقد این شاهد نباید وضعیت کامل یا پذیرفته بگیرد.
Anchors: 
Model comparison: QUALITY_REVIEW_REQUIRED; semantic approval: PENDING_SEMANTIC_REVIEW

### NFR-10 Cross cutting quality

پوشش چندقلمرویی باید با مخرج و حدود تعمیم صریح گزارش شود.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Should candidate; sources: S24
Question: Quality protocol
Expected: قلمروهای بررسی‌شده و پشتیبانی‌نشده حفظ شوند؛ نمونه محدود جهانی نامیده نشود.
Positive: قلمروهای بررسی‌شده و پشتیبانی‌نشده حفظ شوند؛ نمونه محدود جهانی نامیده نشود.
Negative: خروجی فاقد این شاهد نباید وضعیت کامل یا پذیرفته بگیرد.
Anchors: 
Model comparison: QUALITY_REVIEW_REQUIRED; semantic approval: PENDING_SEMANTIC_REVIEW

### NFR-11 Cross cutting quality

ادعاهای روایی مقاله باید به نتیجه و نسخه شواهد متصل باشند.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S04
Question: Quality protocol
Expected: عدد و claim در مقاله با artifact تطبیق داده شود؛ شاهد قدیمی به نتیجه نسخه جدید تبدیل نشود.
Positive: عدد و claim در مقاله با artifact تطبیق داده شود؛ شاهد قدیمی به نتیجه نسخه جدید تبدیل نشود.
Negative: خروجی فاقد این شاهد نباید وضعیت کامل یا پذیرفته بگیرد.
Anchors: 
Model comparison: QUALITY_REVIEW_REQUIRED; semantic approval: PENDING_SEMANTIC_REVIEW

### NFR-12 Cross cutting quality

پذیرش معنایی باید از موفقیت محاسباتی جدا ثبت شود.

Disposition: RETAIN_DISTINCT_OBLIGATION; parent: none
Priority: Must candidate; sources: S33
Question: Quality protocol
Expected: مرورکننده و تصمیم و دلیل ثبت شوند؛ تست سبز به تأیید خودکار متخصص تبدیل نشود.
Positive: مرورکننده و تصمیم و دلیل ثبت شوند؛ تست سبز به تأیید خودکار متخصص تبدیل نشود.
Negative: خروجی فاقد این شاهد نباید وضعیت کامل یا پذیرفته بگیرد.
Anchors: 
Model comparison: QUALITY_REVIEW_REQUIRED; semantic approval: PENDING_SEMANTIC_REVIEW

## Overlap decisions

- OV-01 FR-02, FR-03, FR-04, FR-32: نقش زمینه‌ای قاعده عمومی است؛ بهره‌برداری، مسئولیت تولید و نقش توزیع موضوع و معیار مستقل دارند. FR-03 و FR-04 و FR-32 تخصص‌های کاربردی FR-02 هستند.
- OV-02 FR-05, B2-RG-01: FR-05 پیوند مرجع و موضوع ثبت را می‌خواهد؛ B2-RG-01 مرز ثبت مؤسسه و فهرست محصول را کنترل می‌کند. هیچ‌یک دیگری را پوشش کامل نمی‌دهد.
- OV-03 R-DS-06, B2-RG-02, B2-RG-03: عدم ایجاد مجوز از رکورد دیجیتال قاعده عمومی است؛ ثبت مؤسسه و NDC دو شاهد و محرک متفاوت برای آزمون همان مرز هستند. دو بند B2 تخصص‌های R-DS-06 هستند.
- OV-04 FR-06, B2-RG-02, B2-RG-03: قلمرو اعتبار مجوز با منع نتیجه‌گیری مجوز از ثبت یا فهرست تفاوت دارد؛ حفظ هر سه بند لازم است.
- OV-05 FR-16, B2-RP-02: مرز کلی وضعیت و گزارش در FR-16 ثبت می‌شود؛ گزارش کمبود بالقوه یک مورد تخصصی است که نباید کمبود واقعی ایجاد کند.
- OV-06 FR-22, B2-RG-06: دقت زمانی روز و ماه و سال با نقش تاریخ بازاریابی و دریافت داده تفاوت دارد؛ این دو بعد مستقل نگه داشته می‌شوند.
- OV-07 FR-25, R-DS-04, B2-DS-09: عضویت رکورد در نسخه مجموعه داده، تولید رکورد از فعالیت دیجیتال و اشتقاق مصنوعات سه مسیر ردیابی متفاوت‌اند؛ در یک شناسه ادغام نمی‌شوند.
- OV-08 FR-26, R-RM-03, R-PV-03: قاعده عمومی پشتیبانی ادعا و دو کاربرد ریسک و ایمنی حفظ می‌شوند. استناد ساده به منبع، تحقق خودکار EvidenceSupport واجد شرایط نیست؛ وضعیت مدل برای هر مسیر جدا ارزیابی می‌شود.
- OV-09 FR-30, B2-RP-01, R-PV-06: تفکیک محتوا از سند، مخاطب و سناریوی اعمال، و قلمرو الزام ایمنی سه معیار متفاوت‌اند و باید جدا آزموده شوند.
- OV-10 FR-31: CL-03 پالایش محلی برای تعارض ادعاهای منبع است و به FR-31 پیوند می‌خورد؛ شمار نیازها را افزایش نمی‌دهد.
- OV-11 B2-DS-10, R-RM-06: نسخه‌بندی محتوای داده به ادغام هویت منجر نمی‌شود؛ رخداد بازبینی ریسک موضوع و زمان و نتایج قبلی و جدید دارد. دو سطح با شناسه مستقل حفظ می‌شوند.
- OV-12 B2-DS-08, R-DS-04: انتساب رکورد به عامل با ارتباط فعالیت تولیدکننده تفاوت دارد؛ تولیدکننده و مسئولیت و انتساب نباید یک رابطه شوند.
- OV-13 NFR-01, FR-28: NFR-01 پایداری شناسه عناصر خود انتالوژی است؛ FR-28 تخصیص شناسه دامنه به موجودیت واقعی است. مشابهت واژه شناسه دلیل تکراری‌بودن نیست.
- OV-14 NFR-03, NFR-07: حفظ معنا در تبدیل نمایش‌ها شرط مدل است؛ برابری پاسخ SQL و SPARQL یک ارزیابی رفتاری مستقل دارد.
- OV-15 FR-14, FR-15: قید حامل ظرفیت با تمایز خود ظرفیت از مشاهده اندازه‌گیری آن یکسان نیست؛ یکی جایگزین دیگری نمی‌شود.
- OV-16 FR-18, FR-19: بحرانی بودن و ضروری بودن دو نظام و تصمیم زمینه‌ای متفاوت‌اند؛ دو بند با دو فهرست شاهد حفظ می‌شوند.
- OV-17 FR-01, R-DS-01: هر دو مرز هویت را حفظ می‌کنند ولی موضوع سازمان و محل با جزء سامانه و رکورد متفاوت است؛ شاهد و خطای ناقض متفاوت دارند.
- OV-18 R-DS-02, R-DS-05: شناسه نسخه و زمان استقرار دو فیلد با نقش مستقل‌اند. زمان وقوع از نام نسخه یا تاریخ انتشار استنتاج نمی‌شود.
- OV-19 R-BA-01, FR-14: قابلیت سازمانی و ظرفیت عرضه الزاماً همان مفهوم نیستند؛ قید حامل در هر پروفایل با دامنه خود نگه داشته می‌شود.
- OV-20 FR-23, R-RM-02: مشاهده و ارزیابی ریسک هر دو به تمایز رخداد و نتیجه نیاز دارند؛ بدون اثبات زیرنوع‌بودن ارزیابی ریسک از مشاهده، رابطه subsumption بین این دو نیاز ادعا نمی‌شود.
- OV-21 FR-05, B2-RG-07: وجود رابطه ثبت و حل هویت موضوع ثبت در برابر گزارش‌دهنده دو معیار مستقل‌اند؛ هر دو حفظ می‌شوند.
- OV-22 FR-21, FR-06: تمایز هستی‌شناختی جغرافیا و قلمرو با قید قلمرو یک مجوز متفاوت است.
- OV-23 R-DS-04: B2-DS-07 در R-DS-04 ادغام قبلی شده است؛ به عنوان alias تاریخی حفظ می‌شود و شناسه مستقل فعال ندارد.
- OV-24 NFR-05: الزام آزمون مثبت و منفی یک قاعده کیفیت برای پروتکل ارزیابی است؛ وجود معیار پذیرش در نیازهای کارکردی آن را تکراری نمی‌کند.

## Targeted verification

{
  "document_checks": [
    22,
    22
  ],
  "new_query_cases": [
    7,
    7
  ],
  "new_reasoner_cases": [
    3,
    3
  ],
  "BA_admission": [
    17,
    17
  ],
  "historical_query_replays": [
    23,
    23
  ]
}

47 other functional contracts have no new standalone acceptance execution in this package. No semantic approval is inferred.

## Next action

One author review of purpose, scope, priorities and any concrete missing need, then freeze document 1.0.0. Broader ontology verification and expert evaluation continue separately.
