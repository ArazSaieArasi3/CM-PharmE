# CM PharmE 2.1 Ontology Requirements Specification Document

Document version 0.1.0 | 2026-10-20 | Draft for author and domain review

Baseline commit `09d60136a990d6602438be4085a4d407c9bd5c68`. No ontology release or semantic approval is implied.

83 tracked requirement rows, not 83 independently elicited or semantically nonoverlapping requirements; 13 refinements are attached, not added. Raw discovery and held-out inventories remain separate.

## Purpose

A modular and traceable pharmaceutical ecosystem model for organizations, facilities, products, regulatory relations, supply and evidence. Retain RM, PV, BA and DS as purposeful small ontologies.

## Scope and representations

Core plus reusable evidence, identity, geography and temporal infrastructure. Native OntoUML, OWL/RDF, SHACL/SPARQL and relational projections have distinct contracts. Clinical Care and universal legal compliance remain outside this commitment.

## Users and uses

Regulators, pharmaceutical actors, PV/risk analysts, researchers, data stewards and developers. Principal uses: UC-01/02/03/04/05/07/09/10/15 and bounded UC-16/18.

## Requirements

### FR-01 Ecosystem Organization

مدل باید سازمان حقوقی را از تأسیسات فیزیکی متمایز کند.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S24; uses: UC-01
Question: کدام سازمان بهره‌بردار کدام تأسیسات است؟
Positive: یک سازمان و دو محل با شناسه مستقل قابل بازیابی باشند.
Negative: همسان‌سازی سازمان و محل صرفاً به دلیل نام یا نشانی رد شود.
Anchors: Organization, Facility, FacilityOperation
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-02 Ecosystem Organization

مدل باید نقش یک سازمان را در زمینه رابطه مربوط مشخص کند.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S27; uses: UC-01
Question: سازمان در این رابطه چه نقشی دارد؟
Positive: نقش با رابطه زمینه‌ای قابل بازیابی باشد.
Negative: نام شرکت به‌تنهایی اثبات نقش یا مسئولیت تلقی نشود.
Anchors: Organization, ManufacturerRole, ImporterRole, WholesaleDistributorRole
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-03 Facility Operations

مدل باید بهره‌برداری از تأسیسات را به سازمان مسئول پیوند دهد.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S27; uses: UC-01
Question: چه سازمانی این محل را اداره می‌کند؟
Positive: حامل سازمانی و محل تحت بهره‌برداری مشخص باشند.
Negative: هم‌مکانی به‌تنهایی به بهره‌برداری تبدیل نشود.
Anchors: FacilityOperation, OperatingOrganizationRole, OperatedFacilityRole
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-04 Facility Operations

مدل باید استفاده از محل تولید را از مسئولیت تولید محصول متمایز کند.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S27; uses: UC-01
Question: آیا شاهد درباره محل تولید است یا مسئولیت تولید محصول؟
Positive: دو موضوع و روابط مربوط جدا قابل بازیابی باشند.
Negative: داشتن محل به‌تنهایی مسئولیت هر محصول را نتیجه ندهد.
Anchors: ManufacturingResponsibility, ManufacturingSiteUse, ManufacturingSiteRole
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-05 Regulatory Governance

مدل باید ثبت مؤسسه را به مرجع ثبت و موضوع ثبت متصل کند.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S26; uses: UC-05
Question: مرجع ثبت این سازمان یا محل کدام است؟
Positive: مرجع و موضوع ثبت با شاهد مشخص شوند.
Negative: وجود رکورد بدون حل موضوع، ثبت قطعی موجودیت تلقی نشود.
Anchors: EstablishmentRegistration, RegisteredParty, RegisteringAuthorityRole
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-06 Regulatory Governance

مدل باید مجوز را در قلمرو مقرراتی مربوط تفسیر کند.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S29; uses: UC-05
Question: مجوز برای چه طرف و در چه قلمرویی معتبر گزارش شده است؟
Positive: طرف مجاز، مرجع و قلمرو معلوم یا صریحاً نامعلوم باشند.
Negative: مجوز یک قلمرو به قلمروی دیگر تعمیم داده نشود.
Anchors: RegulatoryAuthorization, AuthorizedParty, RegulatoryJurisdiction
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-07 Regulatory Governance

مدل باید نظارت مقرراتی را از داشتن مجوز متمایز کند.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S27; uses: UC-05
Question: چه مرجعی بر کدام موضوع نظارت دارد؟
Positive: رابطه نظارت مستقل قابل بیان باشد.
Negative: نظارت به‌تنهایی داشتن مجوز یا انطباق را اثبات نکند.
Anchors: RegulatoryOversight, OversightAuthorityRole, GovernedEntity
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-08 Pharmaceutical Product

مدل باید محصول دارویی را از ماده دارویی متمایز کند.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S32; uses: UC-01
Question: محصول به کدام مواد فعال مربوط است؟
Positive: محصول و ماده با شناسه و نوع مستقل بازیابی شوند.
Negative: یکسان بودن نام ماده و محصول سبب ادغام هویت نشود.
Anchors: MedicinalProduct, PharmaceuticalSubstance
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-09 Pharmaceutical Product

مدل باید ارائه یا بسته عرضه‌شده را از محصول متمایز کند.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S32; uses: UC-01
Question: هر ارائه به کدام محصول تعلق دارد؟
Positive: دو بسته‌بندی از یک محصول با شناسه جدا نمایش داده شوند.
Negative: دو بسته متفاوت فقط به دلیل محصول مشترک ادغام نشوند.
Anchors: MedicinalProduct, MedicinalProductPresentation, PackageConfiguration
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-10 Pharmaceutical Product

مدل باید قدرت یا غلظت را به موضوع دارویی مناسب نسبت دهد.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S32; uses: UC-01
Question: قدرت یا غلظت این ارائه چیست؟
Positive: مقدار و موضوع قدرت با هم بازیابی شوند.
Negative: قدرت، هویت محصول یا تعداد بسته تلقی نشود.
Anchors: Strength, MedicinalProductPresentation
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-11 Pharmaceutical Product

مدل باید شکل دارویی را به‌صورت مشخصه قابل ارجاع نگه دارد.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S32; uses: UC-01
Question: شکل دارویی این ارائه چیست؟
Positive: شکل دارویی با ارجاع منبع قابل بازیابی باشد.
Negative: شکل دارویی به مسیر مصرف یا ماده فعال تقلیل داده نشود.
Anchors: DosageFormSpecification, MedicinalProductPresentation
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-12 Pharmaceutical Product

مدل باید تخصیص طبقه‌بندی محصول را همراه با نظام طبقه‌بندی نگه دارد.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S32; uses: UC-01
Question: این کد در کدام نظام به چه محصولی تخصیص یافته است؟
Positive: کد، نظام و موضوع تخصیص هم‌زمان بازیابی شوند.
Negative: کد طبقه‌بندی به‌تنهایی شناسه هویت محصول نشود.
Anchors: ProductClassificationAssignment, ProductClassificationScheme, ClassificationEntry
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-13 Supply Operations

مدل باید وابستگی عرضه را با دو طرف وابسته و فراهم‌کننده بیان کند.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S27; uses: UC-02
Question: چه موجودیتی به چه فراهم‌کننده‌ای وابسته است؟
Positive: دو طرف وابستگی با منبع و زمینه قابل ردیابی باشند.
Negative: صرف حضور در یک منبع، رابطه تأمین‌کننده و خریدار نسازد.
Anchors: SupplyDependency, DependentEntity, ProviderEntity
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-14 Supply Operations

مدل باید ظرفیت عرضه را به دقیقاً یک حامل واجد شرایط در پروفایل مصوب نسبت دهد.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S12; uses: UC-02
Question: حامل این ظرفیت سازمان است یا تأسیسات؟
Positive: یک مسیر حامل سازمان یا محل پذیرفته شود.
Negative: نبود حامل یا دو مسیر هم‌زمان در پروفایل XOR رد شود.
Anchors: SupplyCapacity, Organization, Facility
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-15 Supply Operations

مدل باید اندازه‌گیری ظرفیت را از خود ظرفیت متمایز کند.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S31; uses: UC-02
Question: کدام مشاهده درباره کدام ظرفیت یا موضوع عرضه است؟
Positive: مشاهده و ظرفیت هویت مستقل داشته باشند.
Negative: وجود اندازه‌گیری به ایجاد بی‌دلیل یک ظرفیت ذاتی منجر نشود.
Anchors: SupplyCapacity, SupplyCapacityObservationResult
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-16 Supply Resilience

مدل باید وضعیت کمبود دارو را از گزارش آن متمایز کند.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S31; uses: UC-03
Question: آیا داده یک وضعیت کمبود را توصیف می‌کند یا فقط گزارشی درباره آن است؟
Positive: شاهد گزارش از موضوع وضعیت تفکیک شود.
Negative: گزارش بالقوه یا نقل‌قول، وقوع کمبود را به‌تنهایی اثبات نکند.
Anchors: MedicineShortageSituation, SourceRecord, Assertion
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-17 Supply Resilience

مدل باید اثر اختلال بر وابستگی عرضه را به شواهد متصل کند.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Should candidate; acceptance: PENDING_REVIEW
Sources: S23; uses: UC-03
Question: کدام وابستگی تحت اثر این اختلال گزارش شده است؟
Positive: مسیر اثر با موضوع، زمان و شاهد ثبت شود.
Negative: هم‌زمانی دو گزارش به رابطه علّی تبدیل نشود.
Anchors: DisruptionEvent, SupplyDependency
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-18 Supply Resilience

مدل باید بحرانی بودن دارو را به زمینه طبقه‌بندی مقید کند.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S26; uses: UC-02
Question: دارو طبق کدام فهرست و در چه زمینه‌ای بحرانی است؟
Positive: فهرست، موضوع و زمینه طبقه‌بندی معلوم باشند.
Negative: بحرانی بودن در یک فهرست به حکم جهانی تبدیل نشود.
Anchors: ContextualMedicineClassificationAssignment, CriticalMedicineClassification
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-19 Supply Resilience

مدل باید ضروری بودن دارو را به زمینه طبقه‌بندی مقید کند.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S26; uses: UC-08
Question: دارو طبق کدام فهرست ضروری است؟
Positive: فهرست و نسخه یا تاریخ منبع قابل ارجاع باشند.
Negative: ضروری بودن با بحرانی بودن یکسان فرض نشود.
Anchors: ContextualMedicineClassificationAssignment, EssentialMedicineClassification
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-20 Supply Resilience

مدل باید گزینه جایگزین را نسبت به موضوع مرجع بیان کند.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Should candidate; acceptance: PENDING_REVIEW
Sources: S27; uses: UC-03
Question: کدام دارو در چه زمینه‌ای جایگزین موضوع مرجع گزارش شده است؟
Positive: موضوع مرجع و جایگزین و شاهد قابل بازیابی باشند.
Negative: شباهت نام به معادل درمانی قطعی تبدیل نشود.
Anchors: AlternativeMedicineAssignment, AlternativeMedicinalProductRole, ReferenceProductRole
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-21 Spatiotemporal Context

مدل باید جغرافیای فیزیکی را از قلمرو مقرراتی متمایز کند.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S29; uses: UC-01
Question: موقعیت محل چیست و قلمرو حاکم کدام است؟
Positive: موقعیت و قلمرو دو نقش معنایی مجزا داشته باشند.
Negative: نام کشور به‌تنهایی هم‌هویتی جغرافیا و قلمرو نسازد.
Anchors: GeographicFeature, RegulatoryJurisdiction, Facility
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-22 Spatiotemporal Context

مدل باید دقت زمانی شاهد را حفظ کند.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S19; uses: UC-03
Question: تاریخ شاهد در حد روز است یا ماه یا سال؟
Positive: نقش تاریخ و دقت آن حفظ شود.
Negative: از تاریخ ماهانه یا زمان انتشار، لحظه دقیق رخداد ساخته نشود.
Anchors: TimeInterval, ReportingPeriod
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-23 Ecosystem Observation

مدل باید نتیجه مشاهده را از فعالیت مشاهده متمایز کند.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S31; uses: UC-10
Question: چه نتیجه‌ای از کدام فعالیت مشاهده حاصل شده است؟
Positive: هویت رخداد و نتیجه جدا بازیابی شوند.
Negative: نبود نتیجه منتشرشده به نبود رخداد تعبیر نشود.
Anchors: ObservationResult, ObservationActivity
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-24 Market Access

مدل باید مشاهده بازپرداخت یا مصرف را با زمینه آن نگه دارد.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Should candidate; acceptance: PENDING_REVIEW
Sources: S32; uses: UC-09
Question: این مقدار برای چه موضوع و دوره و جغرافیایی گزارش شده است؟
Positive: موضوع، دوره، منطقه و رکورد منبع همراه مقدار باشند.
Negative: مصرف تجمیعی به شمار بیماران یکتا یا دسترسی قطعی تبدیل نشود.
Anchors: ReimbursementUtilisationObservationResult, ReportingPeriod, GeographicFeature
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-25 Evidence Traceability

مدل باید زنجیره مجموعه‌داده تا نسخه و رکورد را نگه دارد.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S31; uses: UC-10
Question: این رکورد از کدام نسخه مجموعه‌داده آمده است؟
Positive: هر رکورد پذیرفته‌شده به نسخه منبع قابل ردیابی باشد.
Negative: دو نسخه منبع بدون ثبت تفاوت ادغام نشوند.
Anchors: Dataset, DatasetRelease, SourceRecord
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-26 Evidence Traceability

مدل باید پشتیبانی یک ادعا را به شاهد مشخص متصل کند.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S31; uses: UC-10
Question: کدام شاهد از این ادعا پشتیبانی می‌کند؟
Positive: هر پشتیبانی به ادعا و شاهد اشاره کند.
Negative: استناد کلی به ناشر جای شاهد ادعا ننشیند.
Anchors: EvidenceSupport, SourceRecord, Assertion
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-27 Evidence Traceability

مدل باید یافته کیفیت داده را از واقعیت موضوع متمایز کند.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Should candidate; acceptance: PENDING_REVIEW
Sources: S31; uses: UC-10
Question: کدام نقص در داده یا نگاشت ثبت شده است؟
Positive: نقص، موضوع و منبع ثبت شوند.
Negative: نبود داده به نقض واقعی یا نبود موجودیت تبدیل نشود.
Anchors: DataQualityFinding, MappingAssertion, SourceRecord
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-28 Entity Identity

مدل باید شناسه را همراه با نظام صادرکننده و موضوع آن نگه دارد.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S30; uses: UC-04
Question: این مقدار در کدام نظام به چه موجودیتی اشاره دارد؟
Positive: مقدار، نظام و موضوع تخصیص هم‌زمان بازیابی شوند.
Negative: برابری رشته در دو نظام سبب هم‌هویتی نشود.
Anchors: IdentifierAssignment, IdentifierScheme, IdentifierValue, IdentifiedEntity
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-29 Entity Identity

مدل باید تطبیق بین منابع را با شاهد و اطمینان صریح نگه دارد.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Should candidate; acceptance: PENDING_REVIEW
Sources: S30; uses: UC-04
Question: چرا این دو رکورد به یک موجودیت نامزد شده‌اند؟
Positive: دو طرف و شاهد و وضعیت تطبیق موجود باشند.
Negative: تطبیق احتمالی خودکار به owl sameAs قطعی تبدیل نشود.
Anchors: EntityMatchAssertion, MatchConfidence, MappingAssertion
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-30 Regulatory Policy

مدل باید محتوای الزام را از سند حامل آن متمایز کند.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S31; uses: UC-16
Question: کدام سند چه الزام قابل اعمالی را بیان می‌کند؟
Positive: رابطه سند و محتوای الزام قابل ردیابی باشد.
Negative: وجود سند عمومی سبب تعهد همه بازیگران نشود.
Anchors: RegulatoryRequirement, SourceRecord
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-31 Evidence Traceability

مدل باید تعارض ادعاهای منابع را بدون ادغام خودکار حفظ کند.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Should candidate; acceptance: PENDING_REVIEW
Sources: S22; uses: UC-10
Question: کدام منابع درباره یک موضوع ادعاهای متفاوت دارند؟
Positive: دو ادعا و دو انتساب منبع مستقل باقی بمانند.
Negative: اختلاف ادعا با حذف یکی یا منفی‌سازی جهانی حل نشود.
Anchors: Assertion, SourceRecord
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### FR-32 Facility Operations

مدل باید نقش توزیع محل را از نقش توزیع سازمان متمایز کند.

Origin: SOURCE_INFORMED_NEW_SPECIFICATION; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S27; uses: UC-05
Question: کدام سازمان و کدام محل در توزیع مشارکت دارند؟
Positive: نقش محل و نقش سازمان با زمینه مجزا بیان شوند.
Negative: مجوز یا نقش سازمان خودکار به همه محل‌های آن منتقل نشود.
Anchors: DistributionSiteRole, WholesaleDistributorRole, DistributionSiteUse
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.

### R-RM-01 Risk Management

موضوع هر ارزیابی ریسک باید به زمینهٔ دارویی مشخص قابل ردیابی باشد.

Origin: IMPORTED_SOURCE_INFORMED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S08, S17; uses: UC-03
Question: موضوع این ارزیابی ریسک کدام محصول یا محل یا وابستگی عرضه است؟
Positive: پرسش، محصول/تأسیسات/وابستگی موضوع را برگرداند؛ موضوع نامعلوم به‌عنوان نقص اطلاعات مشخص شود.
Negative: ارزیابی فاقد سناریو یا موضوع مشخص در پروفایل کامل رد شود.
Anchors: assessmentScenario, scenarioProduct
Comparison: EXPERIMENTAL_ONLY
Limit: Product path tested; facility and supply-dependency scenario paths remain unimplemented.

### R-RM-02 Risk Management

نتیجهٔ هر ارزیابی باید از رخداد انجام ارزیابی متمایز باشد.

Origin: IMPORTED_SOURCE_INFORMED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S08, S17; uses: UC-03
Question: رخداد ارزیابی و محتوای نتیجه آن چه شناسه های مستقلی دارند؟
Positive: شناسه نتیجه و رخداد قابل تفکیک باشند؛ نبود نتیجهٔ منتشرشده به معنی نبود رخداد نیست.
Negative: همسان سازی رخداد ارزیابی با محتوای نتیجه رد شود.
Anchors: resultAssessment
Comparison: EXPERIMENTAL_ONLY
Limit: Event/content collision rejected; unpublished-result identity cases need an independent witness.

### R-RM-03 Risk Management

مبنای شواهد هر نتیجهٔ ارزیابی باید قابل بازیابی باشد.

Origin: IMPORTED_SOURCE_INFORMED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S08, S17; uses: UC-03
Question: کدام رکورد یا ادعا از نتیجه ارزیابی پشتیبانی می کند؟
Positive: نتیجهٔ پذیرفته‌شده در پروفایل داده به حداقل یک SourceRecord/Assertion متصل باشد.
Negative: نتیجه فاقد شاهد در پروفایل کامل پذیرفته نشود.
Anchors: citesSourceRecord
Comparison: EXPERIMENTAL_ONLY
Limit: Recoverable citation is tested, not evidential strength or qualified EvidenceSupport.

### R-RM-04 Risk Management

برنامهٔ رسیدگی باید به نتیجهٔ ارزیابی موردنظر متصل باشد.

Origin: IMPORTED_SOURCE_INFORMED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S08, S17; uses: UC-03
Question: این برنامه رسیدگی به کدام نتیجه ارزیابی پاسخ می دهد؟
Positive: پرسش برنامه فقط ارزیابی‌های تصریح‌شده را برگرداند.
Negative: برنامه با ارجاع آویزان به نتیجه رد شود.
Anchors: planRiskResult
Comparison: EXPERIMENTAL_ONLY
Limit: Typed explicit references tested; target Assertion need not yet satisfy the risk-result profile.

### R-RM-05 Risk Management

وقوع اقدام رسیدگی باید مستقل از وجود برنامه قابل تشخیص باشد.

Origin: IMPORTED_SOURCE_INFORMED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S08, S17; uses: UC-03
Question: برای کدام برنامه ها اجرای رسیدگی در این مجموعه داده ثبت شده است؟
Positive: وجود برنامه بدون رخداد، اجرای اقدام را نتیجه ندهد.
Negative: از برنامه بدون شاهد اجرا، رخداد رسیدگی یا اثربخشی استنتاج نشود.
Anchors: implementsRiskPlan
Comparison: EXPERIMENTAL_ONLY
Limit: HermiT countermodel permits a plan with zero executions; actual execution still requires evidence.

### R-RM-06 Risk Management

هر بازبینی باید نتیجهٔ پیشین مورد بازبینی را مشخص کند.

Origin: IMPORTED_SOURCE_INFORMED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S08, S17; uses: UC-03
Question: این بازبینی کدام نتیجه پیشین را به کدام نتیجه تازه متصل می کند؟
Positive: زنجیره نسخه/زمان نتیجه‌های قبلی حفظ شود.
Negative: بازبینی فاقد نتیجه پیشین یا با ترتیب زمانی نامعتبر رد شود.
Anchors: reviewPriorResult, reviewNewResult, atTime
Comparison: EXPERIMENTAL_ONLY
Limit: Two-result time ordering tested; full revision identity and review-author provenance remain open.

### R-PV-01 Pharmacovigilance

اطلاعات گزارش ایمنی باید از رخداد گزارش‌کردن متمایز باشد.

Origin: IMPORTED_SOURCE_INFORMED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S08, S16; uses: UC-07
Question: کدام رکورد حاوی گزارش است و رخداد گزارش کردن کدام است؟
Positive: بازارسال همان محتوا، رخداد جدید را بدون ادغام خودکار گزارش‌ها ثبت کند.
Negative: همسان سازی حامل گزارش با رخداد گزارش کردن رد شود.
Anchors: reportsRecord
Comparison: EXPERIMENTAL_ONLY
Limit: Repeated reporting of one carrier tested; content identity across different report carriers is unresolved.

### R-PV-02 Pharmacovigilance

موضوع سیگنال باید به محصول یا مادهٔ دارویی مشخص متصل باشد.

Origin: IMPORTED_SOURCE_INFORMED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S08, S16; uses: UC-07
Question: موضوع این سیگنال کدام محصول یا ماده دارویی است؟
Positive: سیگنال ماده‌ای بدون اجبار ساختن یک برند قابل ثبت باشد.
Negative: سیگنال فاقد موضوع یا با موضوع ناسازگار در پروفایل کامل رد شود.
Anchors: signalProduct, signalSubstance
Comparison: EXPERIMENTAL_ONLY
Limit: Both product and substance paths tested; no brand requirement introduced.

### R-PV-03 Pharmacovigilance

پشتوانهٔ هر سیگنال باید به منابع آن قابل ردیابی باشد.

Origin: IMPORTED_SOURCE_INFORMED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S08, S16; uses: UC-07
Question: کدام منابع از این سیگنال پشتیبانی می کنند؟
Positive: منبع ادعاشده موجود و قابل ارجاع باشد؛ نبود گزارش فردی سیگنال مبتنی بر مطالعه را رد نکند.
Negative: سیگنال فاقد ارجاع شاهد در پروفایل کامل رد شود.
Anchors: citesSourceRecord
Comparison: EXPERIMENTAL_ONLY
Limit: Study-source reference works without an individual report; citation is not established causal evidence.

### R-PV-04 Pharmacovigilance

هر نتیجهٔ ارزیابی باید به سیگنال مورد ارزیابی متصل باشد.

Origin: IMPORTED_SOURCE_INFORMED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S08, S16; uses: UC-07
Question: این نتیجه به ارزیابی کدام سیگنال تعلق دارد؟
Positive: سیگنال و نتیجهٔ ارزیابی آن شناسه و نوع متمایز داشته باشند.
Negative: یکی بودن نتیجه با سیگنال یا اختلاف موضوع نتیجه و ارزیابی رد شود.
Anchors: pvResultSignal, pvResultAssessment, signalAssessmentTarget
Comparison: EXPERIMENTAL_ONLY
Limit: Distinct identifiers and assessment-target agreement tested; both contents remain Assertion, with profile-level distinctions only.

### R-PV-05 Pharmacovigilance

وضعیت نتیجهٔ ارزیابی باید به زمان ارزیابی مقید باشد.

Origin: IMPORTED_SOURCE_INFORMED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S08, S16; uses: UC-07
Question: وضعیت نتیجه در چه زمان ارزیابی گزارش شده است؟
Positive: نتیجهٔ بازبینی، تاریخچهٔ قبلی را پاک نکند.
Negative: نتیجه فاقد زمان یا وضعیت لازم در پروفایل کامل رد شود.
Anchors: atTime, signalStatus
Comparison: EXPERIMENTAL_ONLY
Limit: Two timed results preserved; authority responsible for an assessment and controlled status vocabulary remain open.

### R-PV-06 Pharmacovigilance

اعمال الزام فارماکوویژیلانس باید به قلمرو مقرراتی مشخص مقید باشد.

Origin: IMPORTED_SOURCE_INFORMED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S08, S16; uses: UC-07
Question: این الزام در کدام قلمرو مقرراتی اعمال می شود؟
Positive: الزام منطقه A به‌طور خودکار به منطقه B تعمیم نیابد.
Negative: الزام فاقد قلمرو در پروفایل کامل پذیرفته نشود.
Anchors: pvRequirementJurisdiction, surveillanceRequirement
Comparison: EXPERIMENTAL_ONLY
Limit: Explicit jurisdiction linkage and non-propagation tested; actual legal applicability/compliance is not inferred.

### R-BA-01 Business Architecture

هر EnterpriseCapability باید حامل سازمانی مشخص داشته باشد.

Origin: IMPORTED_SOURCE_INFORMED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S08, S14; uses: UC-18
Question: حامل سازمانی این قابلیت کدام است؟
Positive: حامل با رابطه موجود capabilityBearer قابل بازیابی باشد؛ Mode بی‌حامل در پروفایل کامل رد شود.
Negative: قابلیت فاقد حامل سازمانی در پروفایل کامل رد شود.
Anchors: capabilityBearer
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: Reuses the existing intrinsic Mode bearer relation; this does not adjudicate every capability identity condition.

### R-BA-02 Business Architecture

وجود قابلیت نباید وقوع فعالیت متناظر را الزام کند.

Origin: IMPORTED_SOURCE_INFORMED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S08, S14; uses: UC-18
Question: آیا سازمان می تواند قابلیت داشته باشد ولی اجرای آن در داده ثبت نشده باشد؟
Positive: سازمان دارای قابلیت غیرفعال مجاز باشد.
Negative: وجود قابلیت بدون اجرای ثبت شده باید سازگار بماند؛ اجرای اجباری از قابلیت استنتاج نشود.
Anchors: capabilityRealizedIn
Comparison: UNRESOLVED_MAPPING
Limit: Consistent zero-exercise countermodel tested; realization only targets ManufacturingActivity in this experiment.

### R-BA-03 Business Architecture

ServiceOfferingSpecification باید به موضوع خدمت دارویی متصل باشد.

Origin: IMPORTED_SOURCE_INFORMED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S08, S14; uses: UC-18
Question: مشخصات این خدمت به کدام موضوع دارویی مربوط است؟
Positive: حداقل یک قابلیت/فعالیت/محصول مرتبط در پروفایل پذیرفته‌شده مشخص باشد.
Negative: خدمت فاقد زمینه دارویی در پروفایل کامل رد شود.
Anchors: serviceCapability
Comparison: EXPERIMENTAL_ONLY
Limit: Capability dependency tested; a generic capability does not yet establish a pharmaceutical service context.

### R-BA-04 Business Architecture

BusinessArchitectureView باید به شناسه‌های موجودیت‌های اصلی ارجاع دهد.

Origin: IMPORTED_SOURCE_INFORMED_PROPOSAL; priority: Should candidate; acceptance: PENDING_REVIEW
Sources: S08, S14; uses: UC-18
Question: این نمای معماری به کدام موجودیت های اصلی ارجاع می دهد؟
Positive: نمای جدید برای یک سازمان، سازمان دوم ایجاد نکند.
Negative: ارجاع آویزان نمای معماری به سازمان یا خدمت رد شود.
Anchors: viewOrganization, viewService
Comparison: EXPERIMENTAL_ONLY
Limit: Reuses organization identifiers; no automatic new organization follows from creating a view.

### R-BA-05 Business Architecture

مشارکت در StrategicPartnershipAgreement باید از تعامل اتفاقی متمایز باشد.

Origin: IMPORTED_SOURCE_INFORMED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S08, S14; uses: UC-18
Question: چه تعهد یا توافقی مشارکت این سازمان ها را توجیه می کند؟
Positive: تعامل بدون شاهد تعهد، خودکار PartnerOrganizationRole نسازد.
Negative: همکاری اتفاقی یا سند برنامه بدون تعهد مستند، توافق راهبردی قطعی تلقی نشود.
Anchors: partnershipParticipant
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: Only participant admission tested. Commitment evidence and casual-interaction-without-partner inference remain unimplemented.

### R-BA-06 Business Architecture

هویت موجودیت‌های هسته باید مستقل از وجود نمای معماری بماند.

Origin: IMPORTED_SOURCE_INFORMED_PROPOSAL; priority: Should candidate; acceptance: PENDING_REVIEW
Sources: S08, S14; uses: UC-18
Question: آیا هویت سازمان و خدمت بدون وجود نمای معماری محفوظ می ماند؟
Positive: حذف نمای اختیاری، هویت یا طبقه‌بندی اجباری محصول و تأسیسات را تغییر ندهد.
Negative: حذف نمای معماری سبب حذف یا تغییر هویت موجودیت اصلی نشود.
Anchors: viewOrganization
Comparison: EXPERIMENTAL_ONLY
Limit: Fixture without a view keeps explicit product/facility types; no full identity or deletion semantics proof.

### R-DS-01 Digital Systems

هویت جزء سامانه باید از هویت رکورد تولیدشده متمایز باشد.

Origin: IMPORTED_SOURCE_INFORMED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S08, S15; uses: UC-15
Question: جزء سامانه و رکورد تولیدشده چه هویت های مستقلی دارند؟
Positive: سامانه و SourceRecord شناسه و نوع قابل تفکیک داشته باشند.
Negative: همسان سازی جزء سامانه با رکورد تولیدشده رد شود.
Anchors: recordDigitalActivity, deploymentComponent
Comparison: EXPERIMENTAL_ONLY
Limit: Explicit record/component identity collision rejected; software artifact versus agent modeling remains open.

### R-DS-02 Digital Systems

نسخه جزء سامانهٔ استفاده‌شده باید قابل بازیابی باشد.

Origin: IMPORTED_SOURCE_INFORMED_PROPOSAL; priority: Should candidate; acceptance: PENDING_REVIEW
Sources: S08, S15; uses: UC-15
Question: کدام نسخه جزء سامانه در این فعالیت استفاده شده است؟
Positive: دو اجرای دارای نسخه‌های مختلف در ردیابی ادغام نشوند.
Negative: نسخه نامعلوم با مقدار ساختگی تکمیل نشود؛ پروفایل استقرار کامل آن را رد کند.
Anchors: digitalActivityDeployment, componentVersion
Comparison: EXPERIMENTAL_ONLY
Limit: Two deployments/versions preserve the first record trace; version identity is a local string, not a complete version model.

### R-DS-03 Digital Systems

رابطه پشتیبانی سامانه باید به فعالیت دارویی مشخص متصل باشد.

Origin: IMPORTED_SOURCE_INFORMED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S08, S15; uses: UC-15
Question: این جزء یا خدمت دیجیتال از کدام فعالیت دارویی پشتیبانی می کند؟
Positive: نام بردن سامانه بدون فعالیت مرتبط، پوشش عملکرد دامنه شمرده نشود.
Negative: خدمت دیجیتال بدون موضوع فعالیت دارویی، پشتیبانی عملیاتی کامل تلقی نشود.
Anchors: digitalServiceActivity, digitalServiceComponent
Comparison: EXPERIMENTAL_ONLY
Limit: Only ingestion/transformation ProvenanceActivity is supported; pharmaceutical business-activity grounding is still missing.

### R-DS-04 Digital Systems

منشأ رکورد باید از مسیر فعالیت تولیدکننده قابل ردیابی باشد.

Origin: IMPORTED_SOURCE_INFORMED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S08, S15, S21; uses: UC-15
Question: رکورد از چه فعالیت داده و کدام استقرار تولید شده است؟
Positive: مسیر رکورد→فعالیت→جزء/نسخه و عامل مسئول برای پروفایل کامل قابل پرس‌وجو باشد.
Negative: فعالیت داده مفقود با رکورد یکسان انگاشته نشود؛ مسیر کامل منشأ کنترل شود.
Anchors: recordDigitalActivity, digitalActivityDeployment, deploymentComponent, deploymentOrganization
Comparison: EXPERIMENTAL_ONLY
Limit: Record/activity/component/operator path queried; deployment organization is not automatically the responsible actor for every transformation.

### R-DS-05 Digital Systems

هر استقرار باید زمان وقوع مشخص داشته باشد.

Origin: IMPORTED_SOURCE_INFORMED_PROPOSAL; priority: Should candidate; acceptance: PENDING_REVIEW
Sources: S08, S15; uses: UC-15
Question: استقرار این نسخه در چه زمان و زمینه ای رخ داده است؟
Positive: تغییر نسخه با رخداد استقرار جدید و حفظ تاریخچه نمایش داده شود.
Negative: تاریخ انتشار اطلاعیه به لحظه دقیق استقرار تبدیل نشود.
Anchors: atTime, componentVersion
Comparison: EXPERIMENTAL_ONLY
Limit: Timestamped upgrade history tested; validity intervals, overlapping deployments and rollback policy remain open.

### R-DS-06 Digital Systems

وجود رکورد دیجیتال نباید به‌تنهایی مجوز مقرراتی ایجاد کند.

Origin: IMPORTED_SOURCE_INFORMED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S08, S15; uses: UC-15
Question: آیا صرف وجود رکورد دیجیتال، مجوز مقرراتی را نتیجه می دهد؟
Positive: رکورد رجیستری بدون شاهد مجوز، RegulatoryAuthorization استنتاج نکند.
Negative: رکورد یا حضور دیجیتال به تنهایی مجوز مقرراتی ایجاد نکند.
Anchors: recordDigitalActivity
Comparison: EXPERIMENTAL_ONLY
Limit: A consistent model with no RegulatoryAuthorization shows the scoped non-entailment; no registry or compliance completeness claim.

### B2-RG-01 Registry

ثبت مؤسسه باید از فهرست‌شدن محصول متمایز بماند.

Origin: IMPORTED_SOURCE_DERIVED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S21; uses: UC-05
Question: Which subject is registered or listed?
Positive: Facility registration and product listing remain distinct.
Negative: Registration alone cannot create a product listing.
Anchors: EstablishmentRegistration, MarketListing, rel-registrationEntity, rel-listingPresentation
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: Record-to-fact mapping unresolved.

### B2-RG-02 Registry

ثبت مؤسسه نباید به‌تنهایی مجوز محصول را نتیجه دهد.

Origin: IMPORTED_SOURCE_DERIVED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S21; uses: UC-05
Question: Does registration establish approval?
Positive: Answer unknown without approval evidence.
Negative: Reject registration-to-approval inference.
Anchors: EstablishmentRegistration, RegulatoryAuthorization
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: Existing authorizationParty targets organizations/facilities; product approval representation unresolved.

### B2-RG-03 Registry

فهرست‌شدن NDC نباید به‌تنهایی تأیید محصول را نتیجه دهد.

Origin: IMPORTED_SOURCE_DERIVED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S21; uses: UC-05
Question: What approval evidence supports this product?
Positive: Listed product may have unknown approval.
Negative: NDC presence cannot supply approval evidence.
Anchors: IdentifierAssignment, IdentifierScheme, MarketListing, EvidenceSupport
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: Approval evidence path unresolved.

### B2-RG-04 Registry

اطلاعات تسلیم‌شده به دایرکتوری باید به تسلیم‌کننده منتسب شود.

Origin: IMPORTED_SOURCE_DERIVED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S21; uses: UC-05
Question: Who supplied this entry?
Positive: Return submitting labeler.
Negative: Do not substitute FDA verification.
Anchors: SourceRecord, Organization, Assertion
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: Submitter attribution differs from listing responsibility.

### B2-RG-05 Registry

نبود مدخل در دایرکتوری باید وضعیت نامعلوم را حفظ کند.

Origin: IMPORTED_SOURCE_DERIVED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S21; uses: UC-05
Question: What follows from a missing entry?
Positive: Return not-found within this source.
Negative: Do not infer unapproved or nonexistent.
Anchors: SourceRecord, DatasetRelease
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: Query absence policy required.

### B2-RG-06 Registry

تاریخ بازاریابی باید از تاریخ دریافت داده متمایز بماند.

Origin: IMPORTED_SOURCE_DERIVED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S21; uses: UC-05
Question: Was the entry published at the queried time?
Positive: Apply declared source publication conditions.
Negative: Do not equate retrieval with marketing start.
Anchors: SourceRecord, DatasetRelease, MarketListing, TimeInterval
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: Bitemporal source profile needed.

### B2-RP-01 Regulatory Policy

اعمال تعهد گزارش‌دهی باید با نقش مخاطب و سناریو مقید شود.

Origin: IMPORTED_SOURCE_DERIVED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S21; uses: UC-16
Question: Who reports under this scenario?
Positive: Return applicable MAH/NCA roles.
Negative: Do not generalize one scenario globally.
Anchors: RegulatoryRequirement, Organization, RegulatoryJurisdiction
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: Scenario applicability path absent.

### B2-RP-02 Regulatory Policy

گزارش کمبود بالقوه باید از وضعیت کمبود واقعی متمایز بماند.

Origin: IMPORTED_SOURCE_DERIVED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S21; uses: UC-16
Question: Is this a forecast or actual shortage?
Positive: Potential report remains an assertion.
Negative: Forecast alone cannot establish actual shortage.
Anchors: Assertion, MedicineShortageSituation, SourceRecord
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: Potential/actual assessment policy needed.

### B2-RP-03 Regulatory Policy

دامنه محصول در گزارش‌دهی باید با سناریوی انتخاب‌شده سازگار باشد.

Origin: IMPORTED_SOURCE_DERIVED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S21; uses: UC-16
Question: Are CAPs, NAPs or selected medicines in scope?
Positive: Use the scenario-specific scope.
Negative: Do not apply routine CAP scope universally.
Anchors: RegulatoryRequirement, MedicinalProduct, ContextualMedicineClassificationAssignment
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: Authorization route and scenario membership unresolved.

### B2-RP-04 Regulatory Policy

تناوب گزارش‌دهی باید به اقدام اعلام‌شده متصل شود.

Origin: IMPORTED_SOURCE_DERIVED_PROPOSAL; priority: Should candidate; acceptance: PENDING_REVIEW
Sources: S21; uses: UC-16
Question: Which frequency applies to this action?
Positive: Retrieve that action’s frequency.
Negative: Do not hard-code a universal interval.
Anchors: RegulatoryRequirement, ReportingPeriod, TimeInterval
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: Trigger/version/time linkage unresolved.

### B2-DS-08 Digital Systems

انتساب یک رکورد باید از مسئولیت عامل در فعالیت متمایز بماند.

Origin: IMPORTED_SOURCE_DERIVED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S21; uses: UC-15
Question: Is responsibility attached to artifact or activity?
Positive: Return the qualified relation.
Negative: Do not collapse both predicates.
Anchors: SourceRecord, ProvenanceActivity, Organization
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: Agent typing and responsibility mapping pending.

### B2-DS-09 Digital Systems

زنجیره اشتقاق بین مصنوعات داده باید حفظ شود.

Origin: IMPORTED_SOURCE_DERIVED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S21; uses: UC-15
Question: Which artifact was this derived from?
Positive: Return predecessor lineage.
Negative: Source absence cannot invent lineage.
Anchors: SourceRecord, Dataset, DatasetRelease
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: Derivation relation not mapped.

### B2-DS-10 Digital Systems

بازنگری محتوا نباید به ادغام خودکار هویت نسخه‌ها منجر شود.

Origin: IMPORTED_SOURCE_DERIVED_PROPOSAL; priority: Should candidate; acceptance: PENDING_REVIEW
Sources: S21; uses: UC-15
Question: Which prior version was revised?
Positive: Keep both versions and revision link.
Negative: Revision alone must not assert owl:sameAs.
Anchors: SourceRecord, DatasetRelease
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: Revision identity policy unresolved.

### B2-RG-07 Registry

موضوع ثبت باید از سازمان گزارش‌دهنده متمایز باشد.

Origin: IMPORTED_SOURCE_DERIVED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S21; uses: UC-05
Question: Which organization reported on which establishment?
Positive: An organizational subject may report on itself; record identity remains separate.
Negative: Reject record-subject identity collision, including known owl:sameAs aliases.
Anchors: RegisteredFacilityRole, RegisteredOrganizationRole, SourceRecord
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: Subject resolution policy required.

### B2-RG-08 Registry

SPL باید به‌صورت بازنمایی تسلیم‌شده تفسیر شود.

Origin: IMPORTED_SOURCE_DERIVED_PROPOSAL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S21; uses: UC-05
Question: Which submission represents the listed drug?
Positive: Trace submission to represented subject.
Negative: Do not identify payload with physical product.
Anchors: SourceRecord, MedicinalProduct, Assertion
Comparison: NATIVE_VOCABULARY_ALL_ANCHORS
Limit: Payload/carrier/claim mapping unresolved.

### NFR-01 Cross cutting quality

شناسه‌های مفاهیم و روابط باید در هر نسخه پایدار و تغییرات آن‌ها قابل ردیابی باشد.

Origin: NEW_QUALITY_SPECIFICATION_FROM_PROJECT_PROTOCOL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S28; uses: UC-15
Question: Quality acceptance check
Positive: دو اجرای ساخت با ورودی یکسان شناسه‌های یکسان بدهند؛ تغییر هویت در changelog ثبت شود.
Negative: خروجی فاقد این شاهد نباید وضعیت کامل یا پذیرفته بگیرد.
Anchors: 
Comparison: QUALITY_REVIEW_REQUIRED
Limit: نیاز کیفیتی است؛ وجود کلاس معیار ارزیابی آن نیست.

### NFR-02 Cross cutting quality

هر ماژول باید مأموریت و مرز مالکیت واژگان مشخص داشته باشد.

Origin: NEW_QUALITY_SPECIFICATION_FROM_PROJECT_PROTOCOL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S13; uses: UC-15
Question: Quality acceptance check
Positive: قرارداد ورودی و خروجی و owned و imported ثبت شود؛ ارجاع شکسته رد شود.
Negative: خروجی فاقد این شاهد نباید وضعیت کامل یا پذیرفته بگیرد.
Anchors: 
Comparison: QUALITY_REVIEW_REQUIRED
Limit: نیاز کیفیتی است؛ وجود کلاس معیار ارزیابی آن نیست.

### NFR-03 Cross cutting quality

نگاشت OntoUML و OWL و قیود داده باید تفاوت معنای هر نمایش را حفظ کند.

Origin: NEW_QUALITY_SPECIFICATION_FROM_PROJECT_PROTOCOL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S18; uses: UC-15
Question: Quality acceptance check
Positive: تبدیل فاقد نگاشت معتبر با گزارش خطا متوقف شود؛ معنای گمشده صریح ثبت شود.
Negative: خروجی فاقد این شاهد نباید وضعیت کامل یا پذیرفته بگیرد.
Anchors: 
Comparison: QUALITY_REVIEW_REQUIRED
Limit: نیاز کیفیتی است؛ وجود کلاس معیار ارزیابی آن نیست.

### NFR-04 Cross cutting quality

سازگاری و ناتهی‌پذیری کلاس‌های مصوب باید با ریزنر کنترل شود.

Origin: NEW_QUALITY_SPECIFICATION_FROM_PROJECT_PROTOCOL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S12; uses: UC-15
Question: Quality acceptance check
Positive: ریزنر و نسخه و ورودی ثبت شود؛ تناقض تزریق‌شده تشخیص داده شود.
Negative: خروجی فاقد این شاهد نباید وضعیت کامل یا پذیرفته بگیرد.
Anchors: 
Comparison: QUALITY_REVIEW_REQUIRED
Limit: نیاز کیفیتی است؛ وجود کلاس معیار ارزیابی آن نیست.

### NFR-05 Cross cutting quality

قیود پذیرش داده باید روی نمونه‌های مثبت و منفی سنجیده شوند.

Origin: NEW_QUALITY_SPECIFICATION_FROM_PROJECT_PROTOCOL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S01; uses: UC-15
Question: Quality acceptance check
Positive: داده معتبر پذیرفته و نقص هدفمند رد شود؛ معیار موردانتظار پیش از اجرا ثبت شود.
Negative: خروجی فاقد این شاهد نباید وضعیت کامل یا پذیرفته بگیرد.
Anchors: 
Comparison: QUALITY_REVIEW_REQUIRED
Limit: نیاز کیفیتی است؛ وجود کلاس معیار ارزیابی آن نیست.

### NFR-06 Cross cutting quality

الگوها و ضدالگوها باید با دامنه کاربرد و محدودیت ابزار گزارش شوند.

Origin: NEW_QUALITY_SPECIFICATION_FROM_PROJECT_PROTOCOL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S18; uses: UC-15
Question: Quality acceptance check
Positive: اجرای مدل کامل از toy جدا باشد؛ اختلاف منبع و ابزار با تصمیم ثبت شود.
Negative: خروجی فاقد این شاهد نباید وضعیت کامل یا پذیرفته بگیرد.
Anchors: 
Comparison: QUALITY_REVIEW_REQUIRED
Limit: نیاز کیفیتی است؛ وجود کلاس معیار ارزیابی آن نیست.

### NFR-07 Cross cutting quality

پرسش‌های هم‌معنا در SQL و SPARQL باید روی ورودی ثابت مقایسه شوند.

Origin: NEW_QUALITY_SPECIFICATION_FROM_PROJECT_PROTOCOL; priority: Should candidate; acceptance: PENDING_REVIEW
Sources: S05; uses: UC-15
Question: Quality acceptance check
Positive: پاسخ مرتب و نرمال‌شده یکسان باشد؛ اختلاف join و null و هویت تحلیل شود.
Negative: خروجی فاقد این شاهد نباید وضعیت کامل یا پذیرفته بگیرد.
Anchors: 
Comparison: QUALITY_REVIEW_REQUIRED
Limit: نیاز کیفیتی است؛ وجود کلاس معیار ارزیابی آن نیست.

### NFR-08 Cross cutting quality

ساخت نتایج باید از ورودی نسخه‌دار قابل بازتولید باشد.

Origin: NEW_QUALITY_SPECIFICATION_FROM_PROJECT_PROTOCOL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S06; uses: UC-15
Question: Quality acceptance check
Positive: manifest شامل hash و دستور ساخت و نسخه وابستگی باشد؛ اجرای CI جدا ثبت شود.
Negative: خروجی فاقد این شاهد نباید وضعیت کامل یا پذیرفته بگیرد.
Anchors: 
Comparison: QUALITY_REVIEW_REQUIRED
Limit: نیاز کیفیتی است؛ وجود کلاس معیار ارزیابی آن نیست.

### NFR-09 Cross cutting quality

منابع ارزیابی مستقل باید از منابع کشف تمیز داده شوند.

Origin: NEW_QUALITY_SPECIFICATION_FROM_PROJECT_PROTOCOL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S26; uses: UC-15
Question: Quality acceptance check
Positive: منبع held out در بازسازی این نسخه برای توجیه پذیرش مفهوم مصرف نشود؛ مصرف بعدی با برچسب ثبت شود.
Negative: خروجی فاقد این شاهد نباید وضعیت کامل یا پذیرفته بگیرد.
Anchors: 
Comparison: QUALITY_REVIEW_REQUIRED
Limit: نیاز کیفیتی است؛ وجود کلاس معیار ارزیابی آن نیست.

### NFR-10 Cross cutting quality

پوشش چندقلمرویی باید با مخرج و حدود تعمیم صریح گزارش شود.

Origin: NEW_QUALITY_SPECIFICATION_FROM_PROJECT_PROTOCOL; priority: Should candidate; acceptance: PENDING_REVIEW
Sources: S24; uses: UC-15
Question: Quality acceptance check
Positive: قلمروهای بررسی‌شده و پشتیبانی‌نشده حفظ شوند؛ نمونه محدود جهانی نامیده نشود.
Negative: خروجی فاقد این شاهد نباید وضعیت کامل یا پذیرفته بگیرد.
Anchors: 
Comparison: QUALITY_REVIEW_REQUIRED
Limit: نیاز کیفیتی است؛ وجود کلاس معیار ارزیابی آن نیست.

### NFR-11 Cross cutting quality

ادعاهای روایی مقاله باید به نتیجه و نسخه شواهد متصل باشند.

Origin: NEW_QUALITY_SPECIFICATION_FROM_PROJECT_PROTOCOL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S04; uses: UC-15
Question: Quality acceptance check
Positive: عدد و claim در مقاله با artifact تطبیق داده شود؛ شاهد قدیمی به نتیجه نسخه جدید تبدیل نشود.
Negative: خروجی فاقد این شاهد نباید وضعیت کامل یا پذیرفته بگیرد.
Anchors: 
Comparison: QUALITY_REVIEW_REQUIRED
Limit: نیاز کیفیتی است؛ وجود کلاس معیار ارزیابی آن نیست.

### NFR-12 Cross cutting quality

پذیرش معنایی باید از موفقیت محاسباتی جدا ثبت شود.

Origin: NEW_QUALITY_SPECIFICATION_FROM_PROJECT_PROTOCOL; priority: Must candidate; acceptance: PENDING_REVIEW
Sources: S33; uses: UC-15
Question: Quality acceptance check
Positive: مرورکننده و تصمیم و دلیل ثبت شوند؛ تست سبز به تأیید خودکار متخصص تبدیل نشود.
Negative: خروجی فاقد این شاهد نباید وضعیت کامل یا پذیرفته بگیرد.
Anchors: 
Comparison: QUALITY_REVIEW_REQUIRED
Limit: نیاز کیفیتی است؛ وجود کلاس معیار ارزیابی آن نیست.

## Preglossary

- **Organization**: سازمان با هویت حقوقی یا نهادی؛ محل فیزیکی نیست.
- **Facility**: محل فیزیکی فعالیت؛ از سازمان بهره‌بردار متمایز است.
- **Role**: نقش زمینه‌مند با وابستگی به رابطه مربوط.
- **Relator**: مبنای رابطه میان مشارکت‌کنندگان؛ با سند حامل آن یکی نیست.
- **MedicinalProduct**: محصول دارویی با هویت مستقل از ماده و بسته عرضه.
- **PharmaceuticalSubstance**: ماده دارویی؛ رابطه آن با محصول باید صریح باشد.
- **MedicinalProductPresentation**: ارائه مشخص محصول با مشخصات عرضه و بسته.
- **RegulatoryJurisdiction**: قلمرو اعمال اختیار یا الزام مقرراتی.
- **SourceRecord**: رکورد منبع؛ حامل اطلاعات و متمایز از ادعای موضوعی.
- **Assertion**: محتوای ادعا در پروفایل پذیرفته‌شده؛ معادل خودکار حقیقت جهانی نیست.
- **EvidenceSupport**: پیوند واجد شرایط میان شاهد و ادعای پشتیبانی‌شده.
- **ObservationActivity**: رخداد مشاهده؛ از نتیجه مشاهده مستقل است.
- **ObservationResult**: محتوای نتیجه مشاهده با موضوع و زمینه قابل ردیابی.
- **SupplyCapacity**: قابلیت عرضه متعلق به حامل؛ مقدار مشاهده‌شده خود آن نیست.
- **SupplyDependency**: وابستگی با طرف وابسته و فراهم‌کننده و زمینه.
- **MedicineShortageSituation**: وضعیت کمبود؛ با رکورد یا ادعای کمبود یکی نیست.
- **RiskTreatmentPlan**: محتوای برنامه رسیدگی؛ وجود آن به معنی اجرا نیست.
- **Safety signal**: محتوای سیگنال ایمنی در پروفایل آزمایشی؛ اثبات رابطه علّی نیست.
- **EnterpriseCapability**: قابلیت سازمانی؛ فعالیت تحقق آن مستقل است.
- **SystemDeploymentActivity**: رخداد پیشنهادی استقرار نسخه جزء سامانه؛ با تبدیل داده یکی نیست.
- **IdentifierAssignment**: تخصیص مقدار شناسه در یک نظام به یک موجودیت.
- **EntityMatchAssertion**: ادعای تطبیق با شاهد و اطمینان؛ الزاماً هم‌هویتی قطعی نیست.
- **Core**: تمایزهای ضروری برای کاربردهای اصلی و قابل استفاده در ماژول‌ها.
- **Held out**: خانواده منبع محفوظ برای ارزیابی مستقل از کشف همان نسخه.

## Assessment

{
  "requirement_rows": 83,
  "functional_rows": 71,
  "nonfunctional_rows": 12,
  "new_core_rows": 32,
  "imported_canonical_rows": 39,
  "attached_local_refinements": 13,
  "historical_discovery_rows": 97,
  "historical_heldout_rows": 51,
  "author_accepted_rows": 0,
  "comparison_counts": {
    "NATIVE_VOCABULARY_ALL_ANCHORS": 49,
    "EXPERIMENTAL_ONLY": 21,
    "UNRESOLVED_MAPPING": 1,
    "QUALITY_REVIEW_REQUIRED": 12
  },
  "native_named_classes": 138,
  "native_datatypes": 6,
  "native_elements": 536,
  "experimental_elements": 686
}

Identifier availability is not semantic coverage. Historical tests were not rerun.

## Improvements

- P0 مرز و هم‌پوشانی نیازها: داوری FR عمومی در برابر B2 و R تخصصی؛ ثبت parent و specialization پیش از ادعای تعداد یکتا.
- P0 معنای روابط و قیود: بستن تصمیم‌های علمی و نوع سررابطه و کاردینالیتی و subsetting؛ خودکارکردن تطبیق همه نمایش‌ها.
- P0 هویت رکورد و محتوا و موضوع: تصمیم RG-07 و CL درباره حامل و ادعا و گزارش‌دهنده؛ آزمون مثبت و منفی مستقل.
- P0 Event و Situation و ابزار: حفظ uncertainty و طبیعت مفاهیم؛ داوری چهار اختلاف آشکارساز پیش از تأیید کل مدل.
- P1 شواهد چهار ماژول: داده واقعی اجرای رسیدگی و اثر آن، سفارش کار و تعهد، نسخه و اپراتور استقرار؛ شاهد مفقود نامعلوم بماند.
- P1 قلمرو و زمان: تصمیم درباره دقت روز و ماه و سال و انواع تاریخ؛ عضویت رسمی در محدوده گروه از برچسب منبع جدا شود.
- P1 CQ مستقل نسخه جدید: برای هر نیاز Must پذیرفته‌شده، oracle ثابت و داده مثبت و مرزی و ناقض ساخته و اجرا شود.
- P1 تعمیم و held out: پوشش ۹۷ و ۵۱ ردیف تاریخی نسبت به نسخه جدید جدا بازبینی شود؛ استفاده از held out برای طراحی جدید افشا شود.
- P1 مرور انسانی: نیازها و تعاریف و نمونه‌ها توسط نویسنده و متخصص دامنه بازبینی شوند؛ اختلاف نظر حفظ شود.
- P2 مقاله و دیاگرام و انتشار: مقاله ۲ اکتبر، نمودار، Wiki و Pages پس از تثبیت همگام شوند؛ هدف BioMedInformatics و مغایرت سربرگ اصلاح شود.

## Method reference

{"title": "How to Write and Use the Ontology Requirements Specification Document", "authors": "M. C. Suarez-Figueroa, A. Gomez-Perez, B. Villazon-Terrazas", "year": 2009, "doi": "10.1007/978-3-642-05151-7_16", "url": "https://oa.upm.es/5474/"}

## Reproduction

Run `python build.py` to regenerate canonical JSON, CSV, Markdown and DOCX. Run `python validate.py` for schema, hashes, references and historical module query replays. Render DOCX with the documents skill renderer; copy its PDF into this directory.
