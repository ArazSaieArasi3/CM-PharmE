import json, csv, hashlib, pathlib, re, collections, subprocess, shutil
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
import rdflib

HERE=pathlib.Path(__file__).resolve().parent
ROOT=next((p for p in [HERE,*HERE.parents] if (p/'v2/ontology/candidates').exists()),HERE/'cm-pharme')
C=ROOT/'v2/ontology/candidates'
BASE='09d60136a990d6602438be4085a4d407c9bd5c68'
OUT=ROOT/'v2/requirements/2.1/orsd/0.1.0'
OUT.mkdir(parents=True,exist_ok=True)
def read(p): return json.loads((ROOT/p).read_text())
def cand(p): return json.loads((C/p).read_text())
native=cand('2.1.0-alpha.1-g3-p4a-supply-capacity/ontouml.json')
experimental=cand('2.1.0-alpha.1-domain-coherence-lab/ontouml-experimental.json')
native_ids={x['id'] for x in native['elements']}
exp_ids={x['id'] for x in experimental['elements']}
graph=rdflib.Graph().parse(C/'2.1.0-alpha.1-g3-p4a-supply-capacity/active.ttl')
native_terms={str(x).rsplit('/',1)[-1].rsplit('#',1)[-1] for t in graph for x in t if isinstance(x,rdflib.URIRef)}
exp_terms=set()
for m in ['RM','PV','BA','DS']:
 d=cand(f'2.1.0-alpha.1-module-contract-lab/modules/{m}/contract.json')
 exp_terms|={v.rsplit('/',1)[-1].rsplit('#',1)[-1] for k in ['owned_classes','imported_interface_classes','properties'] for v in d[k]}

# These requirements are newly specified from the independent needs and admission
# evidence. They are review proposals, not retrospectively claimed elicitation.
core='''01|Ecosystem Organization|مدل باید سازمان حقوقی را از تأسیسات فیزیکی متمایز کند.|کدام سازمان بهره‌بردار کدام تأسیسات است؟|Organization Facility FacilityOperation|یک سازمان و دو محل با شناسه مستقل قابل بازیابی باشند.|همسان‌سازی سازمان و محل صرفاً به دلیل نام یا نشانی رد شود.|UC-01|v2/research/w1/stakeholder-needs.md
02|Ecosystem Organization|مدل باید نقش یک سازمان را در زمینه رابطه مربوط مشخص کند.|سازمان در این رابطه چه نقشی دارد؟|Organization ManufacturerRole ImporterRole WholesaleDistributorRole|نقش با رابطه زمینه‌ای قابل بازیابی باشد.|نام شرکت به‌تنهایی اثبات نقش یا مسئولیت تلقی نشود.|UC-01|v2/research/w3/candidate-relations-events.md
03|Facility Operations|مدل باید بهره‌برداری از تأسیسات را به سازمان مسئول پیوند دهد.|چه سازمانی این محل را اداره می‌کند؟|FacilityOperation OperatingOrganizationRole OperatedFacilityRole|حامل سازمانی و محل تحت بهره‌برداری مشخص باشند.|هم‌مکانی به‌تنهایی به بهره‌برداری تبدیل نشود.|UC-01|v2/research/w3/candidate-relations-events.md
04|Facility Operations|مدل باید استفاده از محل تولید را از مسئولیت تولید محصول متمایز کند.|آیا شاهد درباره محل تولید است یا مسئولیت تولید محصول؟|ManufacturingResponsibility ManufacturingSiteUse ManufacturingSiteRole|دو موضوع و روابط مربوط جدا قابل بازیابی باشند.|داشتن محل به‌تنهایی مسئولیت هر محصول را نتیجه ندهد.|UC-01|v2/research/w3/candidate-relations-events.md
05|Regulatory Governance|مدل باید ثبت مؤسسه را به مرجع ثبت و موضوع ثبت متصل کند.|مرجع ثبت این سازمان یا محل کدام است؟|EstablishmentRegistration RegisteredParty RegisteringAuthorityRole|مرجع و موضوع ثبت با شاهد مشخص شوند.|وجود رکورد بدون حل موضوع، ثبت قطعی موجودیت تلقی نشود.|UC-05|v2/research/w2/operational-source-registry.md
06|Regulatory Governance|مدل باید مجوز را در قلمرو مقرراتی مربوط تفسیر کند.|مجوز برای چه طرف و در چه قلمرویی معتبر گزارش شده است؟|RegulatoryAuthorization AuthorizedParty RegulatoryJurisdiction|طرف مجاز، مرجع و قلمرو معلوم یا صریحاً نامعلوم باشند.|مجوز یک قلمرو به قلمروی دیگر تعمیم داده نشود.|UC-05|v2/research/w3/geospatial-temporal-jurisdiction.md
07|Regulatory Governance|مدل باید نظارت مقرراتی را از داشتن مجوز متمایز کند.|چه مرجعی بر کدام موضوع نظارت دارد؟|RegulatoryOversight OversightAuthorityRole GovernedEntity|رابطه نظارت مستقل قابل بیان باشد.|نظارت به‌تنهایی داشتن مجوز یا انطباق را اثبات نکند.|UC-05|v2/research/w3/candidate-relations-events.md
08|Pharmaceutical Product|مدل باید محصول دارویی را از ماده دارویی متمایز کند.|محصول به کدام مواد فعال مربوط است؟|MedicinalProduct PharmaceuticalSubstance|محصول و ماده با شناسه و نوع مستقل بازیابی شوند.|یکسان بودن نام ماده و محصول سبب ادغام هویت نشود.|UC-01|v2/research/w3/source-schema-concept-extraction.md
09|Pharmaceutical Product|مدل باید ارائه یا بسته عرضه‌شده را از محصول متمایز کند.|هر ارائه به کدام محصول تعلق دارد؟|MedicinalProduct MedicinalProductPresentation PackageConfiguration|دو بسته‌بندی از یک محصول با شناسه جدا نمایش داده شوند.|دو بسته متفاوت فقط به دلیل محصول مشترک ادغام نشوند.|UC-01|v2/research/w3/source-schema-concept-extraction.md
10|Pharmaceutical Product|مدل باید قدرت یا غلظت را به موضوع دارویی مناسب نسبت دهد.|قدرت یا غلظت این ارائه چیست؟|Strength MedicinalProductPresentation|مقدار و موضوع قدرت با هم بازیابی شوند.|قدرت، هویت محصول یا تعداد بسته تلقی نشود.|UC-01|v2/research/w3/source-schema-concept-extraction.md
11|Pharmaceutical Product|مدل باید شکل دارویی را به‌صورت مشخصه قابل ارجاع نگه دارد.|شکل دارویی این ارائه چیست؟|DosageFormSpecification MedicinalProductPresentation|شکل دارویی با ارجاع منبع قابل بازیابی باشد.|شکل دارویی به مسیر مصرف یا ماده فعال تقلیل داده نشود.|UC-01|v2/research/w3/source-schema-concept-extraction.md
12|Pharmaceutical Product|مدل باید تخصیص طبقه‌بندی محصول را همراه با نظام طبقه‌بندی نگه دارد.|این کد در کدام نظام به چه محصولی تخصیص یافته است؟|ProductClassificationAssignment ProductClassificationScheme ClassificationEntry|کد، نظام و موضوع تخصیص هم‌زمان بازیابی شوند.|کد طبقه‌بندی به‌تنهایی شناسه هویت محصول نشود.|UC-01|v2/research/w3/source-schema-concept-extraction.md
13|Supply Operations|مدل باید وابستگی عرضه را با دو طرف وابسته و فراهم‌کننده بیان کند.|چه موجودیتی به چه فراهم‌کننده‌ای وابسته است؟|SupplyDependency DependentEntity ProviderEntity|دو طرف وابستگی با منبع و زمینه قابل ردیابی باشند.|صرف حضور در یک منبع، رابطه تأمین‌کننده و خریدار نسازد.|UC-02|v2/research/w3/candidate-relations-events.md
14|Supply Operations|مدل باید ظرفیت عرضه را به دقیقاً یک حامل واجد شرایط در پروفایل مصوب نسبت دهد.|حامل این ظرفیت سازمان است یا تأسیسات؟|SupplyCapacity Organization Facility|یک مسیر حامل سازمان یا محل پذیرفته شود.|نبود حامل یا دو مسیر هم‌زمان در پروفایل XOR رد شود.|UC-02|v2/ontology/candidates/2.1.0-alpha.1-g3-p4a-supply-capacity/README-fa.md
15|Supply Operations|مدل باید اندازه‌گیری ظرفیت را از خود ظرفیت متمایز کند.|کدام مشاهده درباره کدام ظرفیت یا موضوع عرضه است؟|SupplyCapacity SupplyCapacityObservationResult|مشاهده و ظرفیت هویت مستقل داشته باشند.|وجود اندازه‌گیری به ایجاد بی‌دلیل یک ظرفیت ذاتی منجر نشود.|UC-02|v2/research/w3/provenance-evidence-observation.md
16|Supply Resilience|مدل باید وضعیت کمبود دارو را از گزارش آن متمایز کند.|آیا داده یک وضعیت کمبود را توصیف می‌کند یا فقط گزارشی درباره آن است؟|MedicineShortageSituation SourceRecord Assertion|شاهد گزارش از موضوع وضعیت تفکیک شود.|گزارش بالقوه یا نقل‌قول، وقوع کمبود را به‌تنهایی اثبات نکند.|UC-03|v2/research/w3/provenance-evidence-observation.md
17|Supply Resilience|مدل باید اثر اختلال بر وابستگی عرضه را به شواهد متصل کند.|کدام وابستگی تحت اثر این اختلال گزارش شده است؟|DisruptionEvent SupplyDependency|مسیر اثر با موضوع، زمان و شاهد ثبت شود.|هم‌زمانی دو گزارش به رابطه علّی تبدیل نشود.|UC-03|v2/research/w1/geospatial-resilience-risk.md
18|Supply Resilience|مدل باید بحرانی بودن دارو را به زمینه طبقه‌بندی مقید کند.|دارو طبق کدام فهرست و در چه زمینه‌ای بحرانی است؟|ContextualMedicineClassificationAssignment CriticalMedicineClassification|فهرست، موضوع و زمینه طبقه‌بندی معلوم باشند.|بحرانی بودن در یک فهرست به حکم جهانی تبدیل نشود.|UC-02|v2/research/w2/operational-source-registry.md
19|Supply Resilience|مدل باید ضروری بودن دارو را به زمینه طبقه‌بندی مقید کند.|دارو طبق کدام فهرست ضروری است؟|ContextualMedicineClassificationAssignment EssentialMedicineClassification|فهرست و نسخه یا تاریخ منبع قابل ارجاع باشند.|ضروری بودن با بحرانی بودن یکسان فرض نشود.|UC-08|v2/research/w2/operational-source-registry.md
20|Supply Resilience|مدل باید گزینه جایگزین را نسبت به موضوع مرجع بیان کند.|کدام دارو در چه زمینه‌ای جایگزین موضوع مرجع گزارش شده است؟|AlternativeMedicineAssignment AlternativeMedicinalProductRole ReferenceProductRole|موضوع مرجع و جایگزین و شاهد قابل بازیابی باشند.|شباهت نام به معادل درمانی قطعی تبدیل نشود.|UC-03|v2/research/w3/candidate-relations-events.md
21|Spatiotemporal Context|مدل باید جغرافیای فیزیکی را از قلمرو مقرراتی متمایز کند.|موقعیت محل چیست و قلمرو حاکم کدام است؟|GeographicFeature RegulatoryJurisdiction Facility|موقعیت و قلمرو دو نقش معنایی مجزا داشته باشند.|نام کشور به‌تنهایی هم‌هویتی جغرافیا و قلمرو نسازد.|UC-01|v2/research/w3/geospatial-temporal-jurisdiction.md
22|Spatiotemporal Context|مدل باید دقت زمانی شاهد را حفظ کند.|تاریخ شاهد در حد روز است یا ماه یا سال؟|TimeInterval ReportingPeriod|نقش تاریخ و دقت آن حفظ شود.|از تاریخ ماهانه یا زمان انتشار، لحظه دقیق رخداد ساخته نشود.|UC-03|v2/ontology/candidates/2.1.0-alpha.1-operational-evidence-lab/decision-dossier.json
23|Ecosystem Observation|مدل باید نتیجه مشاهده را از فعالیت مشاهده متمایز کند.|چه نتیجه‌ای از کدام فعالیت مشاهده حاصل شده است؟|ObservationResult ObservationActivity|هویت رخداد و نتیجه جدا بازیابی شوند.|نبود نتیجه منتشرشده به نبود رخداد تعبیر نشود.|UC-10|v2/research/w3/provenance-evidence-observation.md
24|Market Access|مدل باید مشاهده بازپرداخت یا مصرف را با زمینه آن نگه دارد.|این مقدار برای چه موضوع و دوره و جغرافیایی گزارش شده است؟|ReimbursementUtilisationObservationResult ReportingPeriod GeographicFeature|موضوع، دوره، منطقه و رکورد منبع همراه مقدار باشند.|مصرف تجمیعی به شمار بیماران یکتا یا دسترسی قطعی تبدیل نشود.|UC-09|v2/research/w3/source-schema-concept-extraction.md
25|Evidence Traceability|مدل باید زنجیره مجموعه‌داده تا نسخه و رکورد را نگه دارد.|این رکورد از کدام نسخه مجموعه‌داده آمده است؟|Dataset DatasetRelease SourceRecord|هر رکورد پذیرفته‌شده به نسخه منبع قابل ردیابی باشد.|دو نسخه منبع بدون ثبت تفاوت ادغام نشوند.|UC-10|v2/research/w3/provenance-evidence-observation.md
26|Evidence Traceability|مدل باید پشتیبانی یک ادعا را به شاهد مشخص متصل کند.|کدام شاهد از این ادعا پشتیبانی می‌کند؟|EvidenceSupport SourceRecord Assertion|هر پشتیبانی به ادعا و شاهد اشاره کند.|استناد کلی به ناشر جای شاهد ادعا ننشیند.|UC-10|v2/research/w3/provenance-evidence-observation.md
27|Evidence Traceability|مدل باید یافته کیفیت داده را از واقعیت موضوع متمایز کند.|کدام نقص در داده یا نگاشت ثبت شده است؟|DataQualityFinding MappingAssertion SourceRecord|نقص، موضوع و منبع ثبت شوند.|نبود داده به نقض واقعی یا نبود موجودیت تبدیل نشود.|UC-10|v2/research/w3/provenance-evidence-observation.md
28|Entity Identity|مدل باید شناسه را همراه با نظام صادرکننده و موضوع آن نگه دارد.|این مقدار در کدام نظام به چه موجودیتی اشاره دارد؟|IdentifierAssignment IdentifierScheme IdentifierValue IdentifiedEntity|مقدار، نظام و موضوع تخصیص هم‌زمان بازیابی شوند.|برابری رشته در دو نظام سبب هم‌هویتی نشود.|UC-04|v2/research/w3/identifiers-entity-resolution.md
29|Entity Identity|مدل باید تطبیق بین منابع را با شاهد و اطمینان صریح نگه دارد.|چرا این دو رکورد به یک موجودیت نامزد شده‌اند؟|EntityMatchAssertion MatchConfidence MappingAssertion|دو طرف و شاهد و وضعیت تطبیق موجود باشند.|تطبیق احتمالی خودکار به owl sameAs قطعی تبدیل نشود.|UC-04|v2/research/w3/identifiers-entity-resolution.md
30|Regulatory Policy|مدل باید محتوای الزام را از سند حامل آن متمایز کند.|کدام سند چه الزام قابل اعمالی را بیان می‌کند؟|RegulatoryRequirement SourceRecord|رابطه سند و محتوای الزام قابل ردیابی باشد.|وجود سند عمومی سبب تعهد همه بازیگران نشود.|UC-16|v2/research/w3/provenance-evidence-observation.md
31|Evidence Traceability|مدل باید تعارض ادعاهای منابع را بدون ادغام خودکار حفظ کند.|کدام منابع درباره یک موضوع ادعاهای متفاوت دارند؟|Assertion SourceRecord|دو ادعا و دو انتساب منبع مستقل باقی بمانند.|اختلاف ادعا با حذف یکی یا منفی‌سازی جهانی حل نشود.|UC-10|v2/ontology/candidates/2.1.0-alpha.1-reporting-context-lab/requirements-traceability.json
32|Facility Operations|مدل باید نقش توزیع محل را از نقش توزیع سازمان متمایز کند.|کدام سازمان و کدام محل در توزیع مشارکت دارند؟|DistributionSiteRole WholesaleDistributorRole DistributionSiteUse|نقش محل و نقش سازمان با زمینه مجزا بیان شوند.|مجوز یا نقش سازمان خودکار به همه محل‌های آن منتقل نشود.|UC-05|v2/research/w3/candidate-relations-events.md'''

req=[]
for line in core.splitlines():
 k,domain,statement,cq,anchors,pos,neg,uc,src=line.split('|')
 if not (ROOT/src).exists() and k=='14': src='v2/ontology/candidates/2.1.0-alpha.1-g3-p4a-supply-capacity/validation-results.json'
 req.append(dict(id='FR-'+k,kind='functional',domain=domain,statement_fa=statement,origin='SOURCE_INFORMED_NEW_SPECIFICATION',priority='Must candidate',use_cases=[uc],source_paths=[src],source_row_ids=[],cq_id='CQ-FR-'+k,cq=cq,expected_answer=pos,positive_acceptance=pos,negative_acceptance=neg,anchors=anchors.split(),evidence_status='ANCHOR_AUDIT_ONLY',acceptance_status='PENDING_REVIEW',coverage_limit='وجود واژگان، اثبات پوشش کامل معنایی نیست؛ آزمون مستقل اختصاصی این بند هنوز اجرا نشده است.'))

prior=cand('2.1.0-alpha.1-four-domain-lab/requirement-traceability.json')
reconciled=cand('2.1.0-alpha.1-registry-policy-lab/reconciled-requirements.json')
source_new={x['id']:x for x in reconciled['requirements']}
prior_by={x['id']:x for x in prior['requirements']}
fa_new={
'B2-RG-01':'ثبت مؤسسه باید از فهرست‌شدن محصول متمایز بماند.',
'B2-RG-02':'ثبت مؤسسه نباید به‌تنهایی مجوز محصول را نتیجه دهد.',
'B2-RG-03':'فهرست‌شدن NDC نباید به‌تنهایی تأیید محصول را نتیجه دهد.',
'B2-RG-04':'اطلاعات تسلیم‌شده به دایرکتوری باید به تسلیم‌کننده منتسب شود.',
'B2-RG-05':'نبود مدخل در دایرکتوری باید وضعیت نامعلوم را حفظ کند.',
'B2-RG-06':'تاریخ بازاریابی باید از تاریخ دریافت داده متمایز بماند.',
'B2-RP-01':'اعمال تعهد گزارش‌دهی باید با نقش مخاطب و سناریو مقید شود.',
'B2-RP-02':'گزارش کمبود بالقوه باید از وضعیت کمبود واقعی متمایز بماند.',
'B2-RP-03':'دامنه محصول در گزارش‌دهی باید با سناریوی انتخاب‌شده سازگار باشد.',
'B2-RP-04':'تناوب گزارش‌دهی باید به اقدام اعلام‌شده متصل شود.',
'B2-DS-08':'انتساب یک رکورد باید از مسئولیت عامل در فعالیت متمایز بماند.',
'B2-DS-09':'زنجیره اشتقاق بین مصنوعات داده باید حفظ شود.',
'B2-DS-10':'بازنگری محتوا نباید به ادغام خودکار هویت نسخه‌ها منجر شود.',
'B2-RG-07':'موضوع ثبت باید از سازمان گزارش‌دهنده متمایز باشد.',
'B2-RG-08':'SPL باید به‌صورت بازنمایی تسلیم‌شده تفسیر شود.'}
module_cqs={}
questions={
'R-RM-01':'موضوع این ارزیابی ریسک کدام محصول یا محل یا وابستگی عرضه است؟',
'R-RM-02':'رخداد ارزیابی و محتوای نتیجه آن چه شناسه های مستقلی دارند؟',
'R-RM-03':'کدام رکورد یا ادعا از نتیجه ارزیابی پشتیبانی می کند؟',
'R-RM-04':'این برنامه رسیدگی به کدام نتیجه ارزیابی پاسخ می دهد؟',
'R-RM-05':'برای کدام برنامه ها اجرای رسیدگی در این مجموعه داده ثبت شده است؟',
'R-RM-06':'این بازبینی کدام نتیجه پیشین را به کدام نتیجه تازه متصل می کند؟',
'R-PV-01':'کدام رکورد حاوی گزارش است و رخداد گزارش کردن کدام است؟',
'R-PV-02':'موضوع این سیگنال کدام محصول یا ماده دارویی است؟',
'R-PV-03':'کدام منابع از این سیگنال پشتیبانی می کنند؟',
'R-PV-04':'این نتیجه به ارزیابی کدام سیگنال تعلق دارد؟',
'R-PV-05':'وضعیت نتیجه در چه زمان ارزیابی گزارش شده است؟',
'R-PV-06':'این الزام در کدام قلمرو مقرراتی اعمال می شود؟',
'R-BA-01':'حامل سازمانی این قابلیت کدام است؟',
'R-BA-02':'آیا سازمان می تواند قابلیت داشته باشد ولی اجرای آن در داده ثبت نشده باشد؟',
'R-BA-03':'مشخصات این خدمت به کدام موضوع دارویی مربوط است؟',
'R-BA-04':'این نمای معماری به کدام موجودیت های اصلی ارجاع می دهد؟',
'R-BA-05':'چه تعهد یا توافقی مشارکت این سازمان ها را توجیه می کند؟',
'R-BA-06':'آیا هویت سازمان و خدمت بدون وجود نمای معماری محفوظ می ماند؟',
'R-DS-01':'جزء سامانه و رکورد تولیدشده چه هویت های مستقلی دارند؟',
'R-DS-02':'کدام نسخه جزء سامانه در این فعالیت استفاده شده است؟',
'R-DS-03':'این جزء یا خدمت دیجیتال از کدام فعالیت دارویی پشتیبانی می کند؟',
'R-DS-04':'رکورد از چه فعالیت داده و کدام استقرار تولید شده است؟',
'R-DS-05':'استقرار این نسخه در چه زمان و زمینه ای رخ داده است؟',
'R-DS-06':'آیا صرف وجود رکورد دیجیتال، مجوز مقرراتی را نتیجه می دهد؟'}
for m in ['RM','PV','BA','DS']:
 d=cand(f'2.1.0-alpha.1-module-contract-lab/modules/{m}/contract.json')
 for q in d['queries']: module_cqs[q['id']]=q
 for rid in [x['id'] for x in prior['requirements'] if x['id'].startswith('R-'+m)]:
  x=prior_by[rid]
  req.append(dict(id=rid,kind='functional',domain={'RM':'Risk Management','PV':'Pharmacovigilance','BA':'Business Architecture','DS':'Digital Systems'}[m],statement_fa=x['statement_fa'],origin='IMPORTED_SOURCE_INFORMED_PROPOSAL',priority='Must candidate',use_cases=[{'RM':'UC-03','PV':'UC-07','BA':'UC-18','DS':'UC-15'}[m]],source_paths=['v2/ontology/candidates/2.1.0-alpha.1-four-domain-lab/requirement-traceability.json',f'v2/ontology/candidates/2.1.0-alpha.1-module-contract-lab/modules/{m}/contract.json'],source_row_ids=[rid],cq_id='CQ-'+rid,cq=questions[rid],expected_answer=x['original_acceptance_fa'],positive_acceptance=x['original_acceptance_fa'],negative_acceptance='نمونه ناقض همین تمایز یا زمینه باید مطابق قرارداد بند رد شود؛ عدم وجود سه‌تایی به‌تنهایی اثبات محال‌بودن نیست.',anchors=[z.split(':')[-1] for z in x['candidate_properties']],original_cq_ids=x['competency_question_ids'],fixture_paths=x['fixture_paths'],evidence_status='HISTORICAL_BOUNDED_TESTS',acceptance_status='PENDING_REVIEW',coverage_limit=x['coverage_limit']))
for h in reconciled['canonical_proposal_headings']:
 if h['id'] in prior_by: continue
 x=source_new[h['id']]
 req.append(dict(id=x['id'],kind='functional',domain=x['domain'],statement_fa=fa_new[x['id']],statement_en=x['statement'],origin='IMPORTED_SOURCE_DERIVED_PROPOSAL',priority='Must candidate',use_cases=['UC-05' if 'RG' in x['id'] else 'UC-16' if 'RP' in x['id'] else 'UC-15'],source_paths=['v2/ontology/candidates/2.1.0-alpha.1-registry-policy-lab/reconciled-requirements.json'],source_row_ids=h['source_row_ids'],primary_source_id=x['source_id'],cq_id='CQ-'+x['id'],cq=x['competency_question'],expected_answer=x['positive_acceptance'],positive_acceptance=x['positive_acceptance'],negative_acceptance=x['negative_acceptance'],anchors=x['candidate_existing_ids'],related_prior_ids=x['related_prior_requirement_ids'],evidence_status='HISTORICAL_EXPERIMENTAL_PROFILE',acceptance_status='PENDING_REVIEW',coverage_limit=x.get('mapping_gap','Semantic/native review pending.')))

nfr='''01|شناسه‌های مفاهیم و روابط باید در هر نسخه پایدار و تغییرات آن‌ها قابل ردیابی باشد.|دو اجرای ساخت با ورودی یکسان شناسه‌های یکسان بدهند؛ تغییر هویت در changelog ثبت شود.|v2/research/w3/concept-admission-protocol.md
02|هر ماژول باید مأموریت و مرز مالکیت واژگان مشخص داشته باشد.|قرارداد ورودی و خروجی و owned و imported ثبت شود؛ ارجاع شکسته رد شود.|v2/ontology/candidates/2.1.0-alpha.1-module-contract-lab/module-catalog.json
03|نگاشت OntoUML و OWL و قیود داده باید تفاوت معنای هر نمایش را حفظ کند.|تبدیل فاقد نگاشت معتبر با گزارش خطا متوقف شود؛ معنای گمشده صریح ثبت شود.|v2/ontology/candidates/2.1.0-alpha.1-native-fidelity-audit/summary.json
04|سازگاری و ناتهی‌پذیری کلاس‌های مصوب باید با ریزنر کنترل شود.|ریزنر و نسخه و ورودی ثبت شود؛ تناقض تزریق‌شده تشخیص داده شود.|v2/ontology/candidates/2.1.0-alpha.1-g3-p4a-supply-capacity/validation-results.json
05|قیود پذیرش داده باید روی نمونه‌های مثبت و منفی سنجیده شوند.|داده معتبر پذیرفته و نقص هدفمند رد شود؛ معیار موردانتظار پیش از اجرا ثبت شود.|v2/evaluation/protocol/e4-competency-questions.json
06|الگوها و ضدالگوها باید با دامنه کاربرد و محدودیت ابزار گزارش شوند.|اجرای مدل کامل از toy جدا باشد؛ اختلاف منبع و ابزار با تصمیم ثبت شود.|v2/ontology/candidates/2.1.0-alpha.1-native-fidelity-audit/summary.json
07|پرسش‌های هم‌معنا در SQL و SPARQL باید روی ورودی ثابت مقایسه شوند.|پاسخ مرتب و نرمال‌شده یکسان باشد؛ اختلاف join و null و هویت تحلیل شود.|v2/manuscript/w7-e10-representation-consistency-evidence.md
08|ساخت نتایج باید از ورودی نسخه‌دار قابل بازتولید باشد.|manifest شامل hash و دستور ساخت و نسخه وابستگی باشد؛ اجرای CI جدا ثبت شود.|v2/manuscript/w7-e13-reproducibility-evidence.md
09|منابع ارزیابی مستقل باید از منابع کشف تمیز داده شوند.|منبع held out در بازسازی این نسخه برای توجیه پذیرش مفهوم مصرف نشود؛ مصرف بعدی با برچسب ثبت شود.|v2/research/w2/operational-source-registry.md
10|پوشش چندقلمرویی باید با مخرج و حدود تعمیم صریح گزارش شود.|قلمروهای بررسی‌شده و پشتیبانی‌نشده حفظ شوند؛ نمونه محدود جهانی نامیده نشود.|v2/research/w1/stakeholder-needs.md
11|ادعاهای روایی مقاله باید به نتیجه و نسخه شواهد متصل باشند.|عدد و claim در مقاله با artifact تطبیق داده شود؛ شاهد قدیمی به نتیجه نسخه جدید تبدیل نشود.|v2/manuscript/evidence-ledger.md
12|پذیرش معنایی باید از موفقیت محاسباتی جدا ثبت شود.|مرورکننده و تصمیم و دلیل ثبت شوند؛ تست سبز به تأیید خودکار متخصص تبدیل نشود.|v2/research/w4/HUMAN-REVIEW-README.md'''
for line in nfr.splitlines():
 k,statement,ac,src=line.split('|')
 req.append(dict(id='NFR-'+k,kind='nonfunctional',domain='Cross cutting quality',statement_fa=statement,origin='NEW_QUALITY_SPECIFICATION_FROM_PROJECT_PROTOCOL',priority='Must candidate',use_cases=['UC-15'],source_paths=[src],source_row_ids=[],cq_id=None,cq=None,expected_answer=ac,positive_acceptance=ac,negative_acceptance='خروجی فاقد این شاهد نباید وضعیت کامل یا پذیرفته بگیرد.',anchors=[],evidence_status='PROTOCOL_OR_HISTORICAL_REPORT_ONLY',acceptance_status='PENDING_REVIEW',coverage_limit='نیاز کیفیتی است؛ وجود کلاس معیار ارزیابی آن نیست.'))

refinements=cand('2.1.0-alpha.1-reporting-context-lab/requirements-traceability.json')['requirements']
negative_checks={
'R-RM-01':'ارزیابی فاقد سناریو یا موضوع مشخص در پروفایل کامل رد شود.',
'R-RM-02':'همسان سازی رخداد ارزیابی با محتوای نتیجه رد شود.',
'R-RM-03':'نتیجه فاقد شاهد در پروفایل کامل پذیرفته نشود.',
'R-RM-04':'برنامه با ارجاع آویزان به نتیجه رد شود.',
'R-RM-05':'از برنامه بدون شاهد اجرا، رخداد رسیدگی یا اثربخشی استنتاج نشود.',
'R-RM-06':'بازبینی فاقد نتیجه پیشین یا با ترتیب زمانی نامعتبر رد شود.',
'R-PV-01':'همسان سازی حامل گزارش با رخداد گزارش کردن رد شود.',
'R-PV-02':'سیگنال فاقد موضوع یا با موضوع ناسازگار در پروفایل کامل رد شود.',
'R-PV-03':'سیگنال فاقد ارجاع شاهد در پروفایل کامل رد شود.',
'R-PV-04':'یکی بودن نتیجه با سیگنال یا اختلاف موضوع نتیجه و ارزیابی رد شود.',
'R-PV-05':'نتیجه فاقد زمان یا وضعیت لازم در پروفایل کامل رد شود.',
'R-PV-06':'الزام فاقد قلمرو در پروفایل کامل پذیرفته نشود.',
'R-BA-01':'قابلیت فاقد حامل سازمانی در پروفایل کامل رد شود.',
'R-BA-02':'وجود قابلیت بدون اجرای ثبت شده باید سازگار بماند؛ اجرای اجباری از قابلیت استنتاج نشود.',
'R-BA-03':'خدمت فاقد زمینه دارویی در پروفایل کامل رد شود.',
'R-BA-04':'ارجاع آویزان نمای معماری به سازمان یا خدمت رد شود.',
'R-BA-05':'همکاری اتفاقی یا سند برنامه بدون تعهد مستند، توافق راهبردی قطعی تلقی نشود.',
'R-BA-06':'حذف نمای معماری سبب حذف یا تغییر هویت موجودیت اصلی نشود.',
'R-DS-01':'همسان سازی جزء سامانه با رکورد تولیدشده رد شود.',
'R-DS-02':'نسخه نامعلوم با مقدار ساختگی تکمیل نشود؛ پروفایل استقرار کامل آن را رد کند.',
'R-DS-03':'خدمت دیجیتال بدون موضوع فعالیت دارویی، پشتیبانی عملیاتی کامل تلقی نشود.',
'R-DS-04':'فعالیت داده مفقود با رکورد یکسان انگاشته نشود؛ مسیر کامل منشأ کنترل شود.',
'R-DS-05':'تاریخ انتشار اطلاعیه به لحظه دقیق استقرار تبدیل نشود.',
'R-DS-06':'رکورد یا حضور دیجیتال به تنهایی مجوز مقرراتی ایجاد نکند.'}
should_ids={'FR-17','FR-20','FR-24','FR-27','FR-29','FR-31','R-BA-04','R-BA-06','R-DS-02','R-DS-05','B2-RP-04','B2-DS-10','NFR-07','NFR-10'}
for x in req:
 if x['id']=='R-DS-04':
  x['source_row_ids']=['R-DS-04','B2-DS-07']
  x['source_paths'].append('v2/ontology/candidates/2.1.0-alpha.1-registry-policy-lab/reconciled-requirements.json')
 if x['id'] in negative_checks:x['negative_acceptance']=negative_checks[x['id']]
 if x['id'] in should_ids:x['priority']='Should candidate'
 a=x['anchors']; x['native_anchors_present']=[v for v in a if v in native_ids or v in native_terms]
 x['experimental_anchors_present']=[v for v in a if v in exp_ids or v in exp_terms]
 x['anchors_unresolved']=[v for v in a if v not in native_ids and v not in native_terms and v not in exp_ids and v not in exp_terms]
 x['comparison_status']='QUALITY_REVIEW_REQUIRED' if x['kind']=='nonfunctional' else 'NATIVE_VOCABULARY_ALL_ANCHORS' if len(x['native_anchors_present'])==len(a) else 'NATIVE_VOCABULARY_PARTIAL' if x['native_anchors_present'] else 'EXPERIMENTAL_ONLY' if x['experimental_anchors_present'] else 'UNRESOLVED_MAPPING'
 x['related_refinement_ids']=[z['id'] for z in refinements if x['id'] in z.get('related_prior_ids',[])]
 x['comparison_limit']='Lexical/identifier reference availability only. Not semantic coverage, constraint conformance or author approval.'

source_paths={p for x in req for p in x['source_paths']}
source_paths|={'v2/research/w1/use-case-catalog.md','v2/research/w2/operational-source-registry.md','v2/evaluation/protocol/e7-source-semantic-coverage.csv','v2/evaluation/protocol/e8-heldout-requirements.csv','v2/ontology/candidates/2.1.0-alpha.1-g3-p4a-supply-capacity/ontouml.json','v2/ontology/candidates/2.1.0-alpha.1-g3-p4a-supply-capacity/active.ttl','v2/ontology/candidates/2.1.0-alpha.1-domain-coherence-lab/ontouml-experimental.json','v2/ontology/candidates/2.1.0-alpha.1-reporting-context-lab/requirements-traceability.json','v2/ontology/candidates/2.1.0-alpha.1-operational-evidence-lab/summary.json','v2/ontology/candidates/2.1.0-alpha.1-operational-evidence-lab/decision-dossier.json','v2/ontology/candidates/2.1.0-alpha.1-g3-3-f-review-handoff/domain-inventory.json'}
sources=[]
for i,p in enumerate(sorted(source_paths),1):
 assert (ROOT/p).exists(),p
 pinned=subprocess.check_output(['git','-C',str(ROOT),'show',BASE+':'+p])
 assert pinned==(ROOT/p).read_bytes(),'Source differs from the pinned baseline: '+p
 sources.append(dict(id=f'S{i:02}',path=p,sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),url=f'https://github.com/ArazSaieArasi3/CM-PharmE/blob/{BASE}/{p}',fresh_execution=False))
source_id={s['path']:s['id'] for s in sources}
for x in req:x['source_ids']=[source_id[p] for p in x['source_paths']]
raw_discovery=list(csv.DictReader((ROOT/'v2/evaluation/protocol/e7-source-semantic-coverage.csv').open()))
raw_holdout=list(csv.DictReader((ROOT/'v2/evaluation/protocol/e8-heldout-requirements.csv').open()))
metrics=dict(requirement_rows=len(req),functional_rows=sum(x['kind']=='functional' for x in req),nonfunctional_rows=sum(x['kind']=='nonfunctional' for x in req),new_core_rows=32,imported_canonical_rows=39,attached_local_refinements=len(refinements),historical_discovery_rows=len(raw_discovery),historical_heldout_rows=len(raw_holdout),author_accepted_rows=0,comparison_counts=dict(collections.Counter(x['comparison_status'] for x in req)),native_named_classes=sum(x['type']=='Class' and x.get('stereotype')!='datatype' for x in native['elements']),native_datatypes=sum(x['type']=='Class' and x.get('stereotype')=='datatype' for x in native['elements']),native_elements=len(native['elements']),experimental_elements=len(experimental['elements']))
data=dict(schema_version='1.0',document_id='CMPE-21-ORSD',document_version='0.1.0',ontology_target='2.1 candidate',date='2026-10-20',status='DRAFT_FOR_AUTHOR_AND_DOMAIN_REVIEW',baseline_commit=BASE,approved_direction='Retain RM PV BA DS as purposeful small ontologies; detailed semantics pending',method_reference=dict(title='How to Write and Use the Ontology Requirements Specification Document',authors='M. C. Suarez-Figueroa, A. Gomez-Perez, B. Villazon-Terrazas',year=2009,doi='10.1007/978-3-642-05151-7_16',url='https://oa.upm.es/5474/'),counting_policy='83 tracked requirement rows, not 83 independently elicited or semantically nonoverlapping requirements; 13 refinements are attached, not added. Raw discovery and held-out inventories remain separate.',metrics=metrics,requirements=req,refinements=refinements,sources=sources,primary_source_registry=reconciled['sources'],historical_module_queries=module_cqs,historical_source_inventories=dict(discovery=raw_discovery,held_out=raw_holdout),comparison_method='New identifier availability audit against pinned native and portable-module signatures; historical tests are not rerun and not interpreted as full acceptance.')
(OUT/'requirements.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
(OUT/'sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2))
(OUT/'comparison.json').write_text(json.dumps(dict(baseline_commit=BASE,metrics=metrics,method=data['comparison_method'],requirements=[{k:x[k] for k in ['id','comparison_status','native_anchors_present','experimental_anchors_present','anchors_unresolved','acceptance_status']} for x in req]),ensure_ascii=False,indent=2))
with (OUT/'traceability.csv').open('w',newline='',encoding='utf-8-sig') as f:
 cols=['id','kind','domain','statement_fa','origin','priority','source_ids','cq_id','comparison_status','native_anchors_present','experimental_anchors_present','anchors_unresolved','acceptance_status']
 w=csv.DictWriter(f,fieldnames=cols);w.writeheader()
 for x in req:w.writerow({k:'; '.join(x[k]) if isinstance(x[k],list) else x[k] for k in cols})

DOC=Document();sec=DOC.sections[0];sec.page_width=Inches(8.5);sec.page_height=Inches(11);sec.top_margin=sec.bottom_margin=Inches(.7);sec.left_margin=sec.right_margin=Inches(.7)
for border in list(DOC.styles.element.iter(qn('w:pBdr'))):border.getparent().remove(border)
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Heading 3']:
 st=DOC.styles[name];st.font.name='Vazirmatn';st.font.color.rgb=RGBColor(0,0,0);st.font.size=Pt(11 if name=='Normal' else 23 if name=='Title' else 15 if name=='Heading 1' else 12)
 st.element.get_or_add_rPr().append(OxmlElement('w:rtl'))
 st.paragraph_format.space_after=Pt(6);st.paragraph_format.line_spacing=1.15
 rfonts=st.element.get_or_add_rPr().get_or_add_rFonts()
 for a in ['ascii','hAnsi','eastAsia','cs']:rfonts.set(qn('w:'+a),'Vazirmatn')
def rtl(p,on=True):
 p.alignment=WD_ALIGN_PARAGRAPH.RIGHT if on else WD_ALIGN_PARAGRAPH.LEFT
 pr=p._p.get_or_add_pPr();e=OxmlElement('w:bidi');e.set(qn('w:val'),'1' if on else '0');pr.append(e)
 if on:pr.find(qn('w:jc')).set(qn('w:val'),'start')
 for r in p.runs:
  r.font.name='Vazirmatn';rp=r._r.get_or_add_rPr();el=OxmlElement('w:rtl');el.set(qn('w:val'),'1' if on else '0');rp.append(el)
 return p
def para(t='',bold=False,english=False):
 p=DOC.add_paragraph();p.add_run(t).bold=bold;return rtl(p,not english)
def heading(t,level=1):return rtl(DOC.add_heading(t,level))
def table(headers,rows,widths=None):
 t=DOC.add_table(rows=1,cols=len(headers));t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
 pr=t._tbl.tblPr;bd=OxmlElement('w:bidiVisual');pr.append(bd)
 borders=OxmlElement('w:tblBorders')
 for side in ['top','left','bottom','right','insideH','insideV']:
  z=OxmlElement('w:'+side);z.set(qn('w:val'),'single');z.set(qn('w:sz'),'4');z.set(qn('w:color'),'D9D9D9');borders.append(z)
 pr.append(borders)
 for j,h in enumerate(headers):t.rows[0].cells[j].text=h
 repeat=OxmlElement('w:tblHeader');t.rows[0]._tr.get_or_add_trPr().append(repeat)
 for row in rows:
  c=t.add_row().cells
  for j,v in enumerate(row):c[j].text=str(v)
 for i,row in enumerate(t.rows):
  row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
  for j,cell in enumerate(row.cells):
   if widths:cell.width=Inches(widths[j])
   cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'DCE6EF' if i==0 else 'F5F7F9' if i%2==0 else 'FFFFFF');cell._tc.get_or_add_tcPr().append(sh)
   marg=OxmlElement('w:tcMar')
   for a in ['top','bottom','left','right']:
    z=OxmlElement('w:'+a);z.set(qn('w:w'),'90');z.set(qn('w:type'),'dxa');marg.append(z)
   cell._tc.get_or_add_tcPr().append(marg)
   for p in cell.paragraphs:
    rtl(p);p.paragraph_format.space_after=Pt(3);p.paragraph_format.line_spacing=1.08
    for r in p.runs:r.font.size=Pt(9.5);r.bold=i==0
 return t

DOC.core_properties.title='CM PharmE 2.1 Ontology Requirements Specification Document'
DOC.core_properties.subject='ORSD 0.1.0 and candidate comparison'
DOC.core_properties.author='CM-PharmE Research Project'
rtl(DOC.add_paragraph('سند مشخصات نیازمندی های انتالوژی',style='Title'))
rtl(DOC.add_paragraph('CM PharmE 2.1',style='Subtitle'))
para('Ontology Requirements Specification Document',english=True)
para('نسخه سند 0.1.0   |   ۲۰ اکتبر ۲۰۲۶   |   وضعیت پیشنهادی برای مرور علمی',bold=True)
para('این سند نیازمندی‌های انتالوژی اکوسیستم دارویی CM-PharmE را برای مسیر 2.1 مشخص می‌کند. هدف آن فراهم‌کردن مبنای قابل بازبینی برای تصمیم‌های مدل‌سازی، پرسش‌های شایستگی و ارزیابی است. نسخه حاضر شواهد موجود را تجمیع می‌کند و نیازهای تازه را صریحاً برچسب می‌زند. پذیرش جهت حفظ چهار ماژول، به معنی پذیرش همه جزئیات آن‌ها نیست.')
table(['مشخصه','مقدار'],[['شناسه سند','CMPE-21-ORSD'],['نسخه سند','0.1.0'],['نسخه انتالوژی هدف','کاندید 2.1 و بسته‌های آزمایشی تفکیک‌شده'],['مبنای مقایسه','PR 305 و commit ثبت‌شده در شناسنامه منابع'],['مرجع روش','Suarez Figueroa et al 2009'],['پذیرش نویسنده و متخصص دامنه','در انتظار مرور؛ هیچ تأیید جدیدی از آزمون‌ها استنتاج نشده است']], [1.9,5.1])
heading('راهنمای استفاده')
para('بخش‌های ۱ تا ۷ متن اصلی ORSD را تشکیل می‌دهند. بخش ۸ نتیجه مقایسه با مدل و پیشنهادهای بهبود است. بخش‌های ۹ تا ۱۱ معیار پذیرش، نسخه‌بندی و منابع را مشخص می‌کنند. جدول ردیابی و داده ماشین‌خوان کنار این سند نگهداری می‌شوند.')
para('تعداد ردیف‌ها: ۸۳ شامل ۷۱ نیاز کارکردی و ۱۲ نیاز کیفیتی. این عدد شمار ردیف‌های قابل پیگیری است و ادعای ۸۳ نیاز مستقل یا تأییدشده ندارد. ۱۳ پالایش محلی ضمیمه‌اند و به این عدد افزوده نشده‌اند. ۹۷ ردیف کشف و ۵۱ ردیف held out تاریخی نیز جدا حفظ شده‌اند.')
heading('۱ هدف انتالوژی')
para('هدف CM-PharmE 2.1 فراهم‌کردن مدل مفهومی مرجع، ماژولار و قابل ردیابی برای سازمان‌ها و نقش‌های آن‌ها، تأسیسات، محصولات و مواد دارویی، ثبت و مجوز و نظارت، و شواهد مربوط به عرضه، دسترسی و وابستگی‌هاست. مدل باید پاسخ درباره بازیگر، مسئولیت، موضوع، قلمرو، زمان و شاهد را بدون از بین بردن تمایزهای هویتی ممکن کند.')
para('چهار حوزه Risk Management، Pharmacovigilance، Business Architecture و Digital Systems در قالب ماژول‌های کوچک و هدفمند حفظ می‌شوند. این تصمیم مسیر طراحی را تثبیت می‌کند؛ مرز دقیق مالکیت، قیود و ادعاهای تجربی هر ماژول همچنان نیازمند مرور است.')
heading('۲ دامنه و مرز')
para('هسته شامل بازیگران و محل‌ها، محصول و ارائه، روابط مقرراتی و عرضه است. زیرساخت مشترک شامل جغرافیا و زمان، شناسه و تطبیق، مشاهده، ادعا، شاهد و منشأ داده است. گسترش‌ها فقط در حد نیازهای مشخص وارد می‌شوند. قابلیت استفاده در چند قلمرو هدف طراحی است و با جامعیت جهانی برابر نیست.')
domains=cand('2.1.0-alpha.1-g3-3-f-review-handoff/domain-inventory.json')['domains']
missions=['سازمان و نقش‌های وابسته به زمینه','بهره‌برداری و استفاده از تأسیسات','ثبت و مجوز و نظارت','ماده و محصول و ارائه و طبقه‌بندی','مسئولیت و وابستگی و ظرفیت عرضه','فعالیت مشاهده و نتیجه آن','جغرافیا و قلمرو و زمان','ادعا و منبع و شاهد و نگاشت','شناسه و تخصیص و تطبیق','الزام و زمینه اعمال آن','بحرانی بودن و کمبود و اختلال و جایگزین','مشاهده بازپرداخت و مصرف','ارزیابی و برنامه و اقدام و بازبینی ریسک','گزارش و سیگنال و ارزیابی ایمنی','قابلیت و خدمت و نمای معماری و توافق','جزء سامانه و استقرار و فعالیت داده','مرز بالینی برای کار آینده']
table(['دامنه','مأموریت','مرز نسخه'],[[d['domain'],missions[i],'تعویق؛ بدون الزام جدید در این سند' if d['domain']=='Clinical Care' else 'چهار ماژول هدفمند با جزئیات باز' if i in [12,13,14,15] else 'در دامنه با ردیابی و قیود زمینه‌ای'] for i,d in enumerate(domains)],[2,3.4,1.6])
para('موارد خارج از تعهد این نسخه: مدل جامع مراقبت بیمار، تشخیص و توصیه درمانی، استنتاج علی از گزارش عارضه، همه فرایندهای ریسک سازمانی، موتور جامع انطباق حقوقی، شبکه کامل جهانی محموله و تأمین، و اثبات اثرگذاری عملیاتی یا برتری پیش‌بینی. Clinical Care و منابع ارزیابی مستقل برای پرکردن مصنوعی پوشش وارد هسته نمی‌شوند.')
heading('۳ زبان پیاده سازی و نمایش ها')
table(['نمایش','کارکرد','مرز معنا'],[['OntoUML','تعیین نوع مفاهیم و روابط و هویت و وابستگی','نمای مرجع مفهومی؛ نگاشت به ابزار قدیمی باید فقدان معنا را گزارش کند'],['OWL 2 و RDF','واژگان رسمی و استنتاج با معنای جهان باز','هم‌نامی و نبود داده معادل هم‌هویتی یا نفی نیست'],['SHACL و پرسش های SPARQL','پذیرش داده تحت پروفایل و قرارداد پاسخ','معنای اعتبارسنجی داده با سازگاری OWL یکسان نیست'],['پایگاه رابطه ای و SQL','ذخیره و بازیابی و مقایسه پرسش‌ها','نگاشت رابطه‌ای جایگزین معنا و اعتبار OntoUML نیست'],['JSON و CSV و Markdown','ردیابی و نسخه‌بندی و قابلیت بازبینی','سند و مدل نسخه مستقل اما پیوند مبنا دارند']],[1.5,2.5,3])
heading('۴ کاربران مورد نظر')
table(['کاربر','نیاز اصلی','حد استفاده'],[['رگولاتور و مرجع سلامت','شناخت بازیگران و وضعیت ثبت و عرضه و شواهد','تصمیم حقوقی خودکار ادعا نمی‌شود'],['دارنده مجوز و تولیدکننده و توزیع کننده','موضوع محصول و محل و مسئولیت و گزارش‌دهی','هر رابطه نیازمند شاهد و زمینه است'],['تیم ایمنی و تحلیلگر ریسک','پیوند گزارش و ارزیابی و اقدام و بازبینی','گزارش به معنی علیت یا اثربخشی نیست'],['پژوهشگر و متولی داده','ادغام منابع با حفظ هویت و منشأ','تطبیق احتمالی از هویت قطعی جداست'],['معمار و توسعه دهنده','استفاده مجدد از واژگان و نگاشت‌ها','قرارداد رابط و پروفایل اجرا رعایت شود']],[2,2.8,2.2])
para('این فهرست از اسناد نیازهای پروژه بازسازی و تجمیع شده است؛ به معنی مصاحبه یا توافق تازه با نمایندگان این گروه‌ها نیست. مرور ذی‌نفعان و متخصصان بخشی از برنامه پذیرش است.')
heading('۵ کاربردهای مورد نظر')
table(['کاربرد','خروجی مورد انتظار','وضعیت'],[['UC-01 نقشه بازیگر و محل','بازیگر و نقش و محل و قلمرو با شاهد','نمایش اصلی پژوهش'],['UC-02 و UC-03 عرضه و تاب آوری','وابستگی، بحرانی بودن، اختلال و گزینه جایگزین','در حد داده و سناریوی پذیرفته‌شده'],['UC-04 هویت بین منابع','تخصیص شناسه و تطبیق مستند','زیرساخت مشترک'],['UC-05 مرور مقرراتی','تمایز ثبت و فهرست و مجوز و نظارت','بدون صدور حکم حقوقی'],['UC-07 شواهد ایمنی','گزارش و سیگنال و نتیجه و منشأ','ماژول هدفمند'],['UC-09 مشاهده دسترسی بازار','مقدار با موضوع و دوره و منطقه','مشاهده تجمیعی'],['UC-10 جستجوی مبتنی بر شاهد','پاسخ همراه با منبع و ادعا','کاربرد مشترک'],['UC-15 برابری پرسش ها','مقایسه SQL و SPARQL روی ورودی ثابت','ارزیابی پژوهشی'],['UC-16 و UC-18','پروفایل گزارش‌دهی و مرور اکوسیستم','بخش‌های انتخابی؛ محصول عملیاتی تأیید نشده']],[2.2,3,1.8])
para('UC-06 مربوط به شبکه کارآزمایی، در مخزن تاریخی منبع ارزیابی مستقل است. UC-11 تا UC-14 و UC-17 عمدتاً فرصت آینده هستند. ثبت آن‌ها در کاتالوگ کاربرد به معنی تعهد این نسخه به مدل‌سازی یا اجرای کامل نیست.')
heading('۶ نیازمندی های انتالوژی')
para('اولویت Must candidate یعنی بند برای تصمیم انتشار نامزد الزام است؛ پذیرش آن هنوز انجام نشده است. Should candidate نیاز مطلوب و قابل تعویق با دلیل است. اولویت ها پیشنهاد این سند هستند. برچسب منبع‌مطلع نشان می‌دهد بند با استناد به نیاز و شواهد تدوین شده، اما الزاماً نقل مستقیم یا اجماع ذی‌نفع نیست. هر تغییر به بند باید با دلیل و اثر بر CQ و مدل ثبت شود.')
para('برای هر بند یک پرسش ارزیابی و معیار مثبت و منفی ثبت شده است. پرسش‌های بازنویسی‌شده این سند قرارداد اجرایی تازه محسوب نمی‌شوند. شناسه و متن پرسش‌های اجرایی قدیمی در requirements.json محفوظ‌اند و باید پس از پذیرش به قراردادهای نسخه جدید نگاشت شوند.')
origin_fa={'SOURCE_INFORMED_NEW_SPECIFICATION':'تدوین جدید با اتکا به نیاز و منبع','IMPORTED_SOURCE_INFORMED_PROPOSAL':'پیشنهاد قبلی منبع‌مطلع','IMPORTED_SOURCE_DERIVED_PROPOSAL':'پیشنهاد قبلی مستخرج از منبع','NEW_QUALITY_SPECIFICATION_FROM_PROJECT_PROTOCOL':'نیاز کیفیتی پیشنهادی از پروتکل پروژه'}
status_fa={'NATIVE_VOCABULARY_ALL_ANCHORS':'تمام ارجاعات در واژگان native موجود','NATIVE_VOCABULARY_PARTIAL':'بخشی از ارجاعات در native موجود','EXPERIMENTAL_ONLY':'ارجاع موجود فقط در بسته آزمایشی','UNRESOLVED_MAPPING':'نگاشت شناسه نیازمند حل','QUALITY_REVIEW_REQUIRED':'نیازمند ارزیابی کیفیتی'}
for title,predicate in [('۶ ۱ نیازهای هسته و زیرساخت',lambda x:x['id'].startswith('FR-')),('۶ ۲ نیازهای چهار ماژول هدفمند',lambda x:x['id'].startswith('R-')),('۶ ۳ نیازهای رجیستری و سیاست و منشأ',lambda x:x['id'].startswith('B2-')),('۶ ۴ نیازهای غیرکارکردی و کیفیتی',lambda x:x['kind']=='nonfunctional')]:
 heading(title,2)
 for x in filter(predicate,req):
  heading(x['id']+'   '+x['domain'],3)
  para(x['statement_fa'],bold=True)
  para('منشأ: '+origin_fa[x['origin']]+'؛ منابع: '+', '.join(x['source_ids'])+'؛ کاربرد: '+', '.join(x['use_cases'])+'؛ اولویت: '+x['priority'])
  if x['cq']:para('پرسش '+x['cq_id']+': '+x['cq'])
  para('معیار مثبت: '+x['positive_acceptance'])
  para('معیار منفی: '+x['negative_acceptance'])
  if x['anchors']:para('ارجاع مدل: '+', '.join(x['anchors']),english=True)
  para('مقایسه: '+status_fa[x['comparison_status']]+'؛ پذیرش معنایی: باز. '+x['coverage_limit'])
heading('۶ ۵ پالایش های محلی و رفع هم پوشانی',2)
para('سیزده ردیف CL و CTX در کاتالوگ قدیمی پالایش محلی هستند و نیاز مستقل جدید شمرده نمی‌شوند. ادغام B2-DS-07 در R-DS-04 حفظ شده است. FR-05 با B2-RG-01، FR-16 با B2-RP-02، FR-22 با B2-RG-06، FR-25 و FR-26 با R-DS-04 و FR-31 با CL-03 هم‌پوشانی دارند؛ رابطه عمومی و تخصص زمینه‌ای باید در مرور بعدی داوری شود، نه اینکه بی‌دلیل حذف یا مستقل شمرده شود.')
table(['شناسه پالایش','بیان ثبت شده','نیازهای مرتبط'],[[x['id'],x['statement'],', '.join(x.get('related_prior_ids',[]))] for x in refinements],[.8,4.2,2])
heading('۷ پیش واژه نامه')
glossary=[('Organization','سازمان با هویت حقوقی یا نهادی؛ محل فیزیکی نیست.'),('Facility','محل فیزیکی فعالیت؛ از سازمان بهره‌بردار متمایز است.'),('Role','نقش زمینه‌مند با وابستگی به رابطه مربوط.'),('Relator','مبنای رابطه میان مشارکت‌کنندگان؛ با سند حامل آن یکی نیست.'),('MedicinalProduct','محصول دارویی با هویت مستقل از ماده و بسته عرضه.'),('PharmaceuticalSubstance','ماده دارویی؛ رابطه آن با محصول باید صریح باشد.'),('MedicinalProductPresentation','ارائه مشخص محصول با مشخصات عرضه و بسته.'),('RegulatoryJurisdiction','قلمرو اعمال اختیار یا الزام مقرراتی.'),('SourceRecord','رکورد منبع؛ حامل اطلاعات و متمایز از ادعای موضوعی.'),('Assertion','محتوای ادعا در پروفایل پذیرفته‌شده؛ معادل خودکار حقیقت جهانی نیست.'),('EvidenceSupport','پیوند واجد شرایط میان شاهد و ادعای پشتیبانی‌شده.'),('ObservationActivity','رخداد مشاهده؛ از نتیجه مشاهده مستقل است.'),('ObservationResult','محتوای نتیجه مشاهده با موضوع و زمینه قابل ردیابی.'),('SupplyCapacity','قابلیت عرضه متعلق به حامل؛ مقدار مشاهده‌شده خود آن نیست.'),('SupplyDependency','وابستگی با طرف وابسته و فراهم‌کننده و زمینه.'),('MedicineShortageSituation','وضعیت کمبود؛ با رکورد یا ادعای کمبود یکی نیست.'),('RiskTreatmentPlan','محتوای برنامه رسیدگی؛ وجود آن به معنی اجرا نیست.'),('Safety signal','محتوای سیگنال ایمنی در پروفایل آزمایشی؛ اثبات رابطه علّی نیست.'),('EnterpriseCapability','قابلیت سازمانی؛ فعالیت تحقق آن مستقل است.'),('SystemDeploymentActivity','رخداد پیشنهادی استقرار نسخه جزء سامانه؛ با تبدیل داده یکی نیست.'),('IdentifierAssignment','تخصیص مقدار شناسه در یک نظام به یک موجودیت.'),('EntityMatchAssertion','ادعای تطبیق با شاهد و اطمینان؛ الزاماً هم‌هویتی قطعی نیست.'),('Core','تمایزهای ضروری برای کاربردهای اصلی و قابل استفاده در ماژول‌ها.'),('Held out','خانواده منبع محفوظ برای ارزیابی مستقل از کشف همان نسخه.')]
table(['اصطلاح','تعریف کاری'],glossary,[2.2,4.8])
para('این پیش‌واژه‌نامه برای مشخص‌کردن نیازهاست. تثبیت تعریف و stereotype هر مفهوم، تصمیم مرحله مدل‌سازی و مرور علمی است. فهرست کامل شناسه‌های native در پرونده مبنا نگهداری می‌شود.')
heading('۸ ارزیابی سند و مقایسه با کاندید 2.1')
para('دو لایه جدا بررسی شدند: مدل native ظرفیت عرضه با ۱۳۸ کلاس نام‌دار و ۶ datatype، و نسخه‌های آزمایشی چهار دامنه و پروفایل‌های گزارش و منشأ. مبنا به commit مشخص مقید است؛ وجود چند فایل candidate به معنی ادغام یا پذیرش نهایی آن‌ها نیست.')
table(['شاخص تازه بررسی شده','نتیجه','تفسیر'],[['بخش های اصلی مرجع ORSD','۷ از ۷ موجود','کامل‌بودن ساختار، نه کفایت علمی همه نیازها'],['ردیف های نیازمندی',len(req),'۳۲ جدید هسته، ۳۹ واردشده، ۱۲ کیفیتی'],['پذیرش نهایی نیازها','۰','تأیید جدیدی جعل یا از تست استنتاج نشده'],['پالایش محلی',len(refinements),'در شمار ردیف نیاز مستقل جمع نشده'],['منابع فایل نسخه دار',len(sources),'وجود و SHA256 در اجرای فعلی کنترل شد'],['فهرست تاریخی کشف و held out',f'{len(raw_discovery)} / {len(raw_holdout)}','جدا حفظ شدند؛ نتایج تاریخی به v2.1 تعمیم نیافتند']],[2.7,1.1,3.2])
table(['حالت مقایسه ارجاعات','تعداد ردیف','معنا'],[[status_fa[k],v,'شمار دسترسی به شناسه؛ جایگزین ارزیابی معنایی نیست'] for k,v in metrics['comparison_counts'].items()],[3,1,3])
para('ممیزی تازه فقط وجود شناسه‌های ارجاعی در فایل native و واژگان OWL و قرارداد ماژول‌های آزمایشی را کنترل کرد. رابطه با نام مشابه، پوشش قیود و پاسخ کامل CQ را اثبات نمی‌کند. فهرست ارجاعات حل‌نشده در comparison.json و جدول ردیابی آمده است. نیازهای غیرکارکردی با شمار کلاس سنجیده نمی‌شوند.')
para('در اجرای تازه، ۱۲ کنترل ساختاری سند و ردیابی موفق شدند و ۲۳ پرسش موجود چهار ماژول روی fixture های ثابت دوباره مطابق پاسخ ثبت شده اجرا شدند. این بازاجرا شامل SHACL یا HermiT نبود و قراردادهای جدید این سند را نیز تأیید نمی کند. خروجی و نسخه محیط در validation.json ثبت شده اند.')
para('یک اختلاف ردیابی مشخص شد: R-BA-02 به capabilityRealizedIn ارجاع می دهد، ولی این شناسه در signature مدل native یا قرارداد صادرشده BA یافت نشد. پرسش قدیمی همین نام را در FILTER NOT EXISTS مصرف می کند؛ موفقیت آن برای اثبات پوشش مسیر جدید capabilityRealizedInLogistics کافی نیست. این یافته به معنی نبود معنا در کل مخزن نیست و پیش از بستن نیاز باید نگاشت و آزمون ضد نمونه بازبینی شود.')
heading('۸ ۱ شواهد قبلی و حدود آن ها',2)
table(['بسته تاریخی','نتیجه ثبت شده','حد استناد'],[['چهار ماژول مستقل','۸۳ پذیرش داده، ۲۳ پرسش، ۱۴ ریزنر مطابق انتظار','این اجرا دوباره انجام نشد؛ پوشش محدود و پذیرش علمی باز'],['شواهد عملیاتی','۸ سند، ۴۹ استخراج، ۱۳ نگاشت پیشنهادی','نمونه هدفمند و تاریخی؛ پوشش نماینده یا تأیید متخصص نیست'],['کنترل عملیاتی','۳۱ سندی، ۸ محدوده ریسک، ۱۱ قرارداد، ۸ منطقی','معیارهای متفاوت؛ به امتیاز جامع جمع نشوند'],['آشکارسازهای ضدالگو','اجرای کامل candidate هنوز صفر از ۲۰','حساسیت روی toy با صحت مدل کامل برابر نیست'],['گیت های پژوهش','۲ از ۵ دروازه تاریخی بسته','۴۰ درصدِ تعداد گیت‌ها؛ درصد آمادگی مقاله نیست']],[2.3,2.5,2.2])
heading('۸ ۲ شکاف ها و بهبودهای اولویت دار',2)
improvements=[('P0','مرز و هم‌پوشانی نیازها','داوری FR عمومی در برابر B2 و R تخصصی؛ ثبت parent و specialization پیش از ادعای تعداد یکتا.'),('P0','معنای روابط و قیود','بستن تصمیم‌های علمی و نوع سررابطه و کاردینالیتی و subsetting؛ خودکارکردن تطبیق همه نمایش‌ها.'),('P0','هویت رکورد و محتوا و موضوع','تصمیم RG-07 و CL درباره حامل و ادعا و گزارش‌دهنده؛ آزمون مثبت و منفی مستقل.'),('P0','Event و Situation و ابزار','حفظ uncertainty و طبیعت مفاهیم؛ داوری چهار اختلاف آشکارساز پیش از تأیید کل مدل.'),('P1','شواهد چهار ماژول','داده واقعی اجرای رسیدگی و اثر آن، سفارش کار و تعهد، نسخه و اپراتور استقرار؛ شاهد مفقود نامعلوم بماند.'),('P1','قلمرو و زمان','تصمیم درباره دقت روز و ماه و سال و انواع تاریخ؛ عضویت رسمی در محدوده گروه از برچسب منبع جدا شود.'),('P1','CQ مستقل نسخه جدید','برای هر نیاز Must پذیرفته‌شده، oracle ثابت و داده مثبت و مرزی و ناقض ساخته و اجرا شود.'),('P1','تعمیم و held out','پوشش ۹۷ و ۵۱ ردیف تاریخی نسبت به نسخه جدید جدا بازبینی شود؛ استفاده از held out برای طراحی جدید افشا شود.'),('P1','مرور انسانی','نیازها و تعاریف و نمونه‌ها توسط نویسنده و متخصص دامنه بازبینی شوند؛ اختلاف نظر حفظ شود.'),('P2','مقاله و دیاگرام و انتشار','مقاله ۲ اکتبر، نمودار، Wiki و Pages پس از تثبیت همگام شوند؛ هدف BioMedInformatics و مغایرت سربرگ اصلاح شود.')]
table(['اولویت','موضوع','اقدام و خروجی'],improvements,[.6,1.8,4.6])
heading('۹ روش verification و معیار پذیرش')
para('ابتدا صورت مسئله و پاسخ موردانتظار مستقل از ساخت داده آزمون ثبت شود. سپس برای نیاز پذیرفته‌شده شاهد مثبت، ناقض، مرزی و ناتهی‌بودن یا عدم استنتاج ناخواسته تهیه شود. آزمون‌های مدل، گراف داده و پایگاه رابطه‌ای با معنای هر نمایش اجرا شوند. تغییر عمدی قید باید در آزمون مرتبط اثر قابل تشخیص داشته باشد.')
para('در OWL نبود واقعیت، نفی آن نیست. برای عدم استنتاج باید صورت ادعا و روش آزمون روشن باشد. در پروفایل داده، نبود فیلد الزامی می‌تواند نقض پذیرش باشد، بدون آنکه نقض واقعی جهان نتیجه شود. نمونه مصنوعی آزمون طراحی است و شاهد تجربی مستقل محسوب نمی‌شود.')
table(['دروازه','شرط خروج'],[['پذیرش ORSD 0.1','همه بندها منبع، نوع منشأ، معیار و وضعیت باز داشته باشند؛ شمارش و ردیابی کنترل شود'],['پذیرش نیازهای نسخه بعد','نویسنده درباره حفظ و ادغام و تعویق تصمیم دهد؛ نیاز ضروری بدون مرجع پاسخ نماند'],['پذیرش مدل','نیازهای مصوب به مفهوم و رابطه و قید مشخص و آزمون متناسب متصل شوند'],['انتشار انتالوژی','خطای مسدودکننده حل شود و مرور علمی و بازتولید و مستندات کامل باشند'],['ارسال مقاله','ادعا و عدد و نمودار با مدل پذیرفته‌شده یکسان باشد؛ ارزیابی انسانی ادعاشده واقعاً انجام شده باشد']],[2,5])
heading('۱۰ نسخه بندی و تغییرات')
para('نسخه سند از نسخه انتالوژی مستقل است. این فایل ORSD 0.1.0 برای انتالوژی هدف 2.1 است و انتشار رسمی انتالوژی ایجاد نمی‌کند. شناسه بندها پس از حذف دوباره استفاده نشوند. تغییر معنا با old و new و rationale و اثر بر CQ و مدل و تست ثبت شود. نسخه قدیمی به‌صورت پوشه تغییرناپذیر نگهداری و شاخص latest به نسخه جدید به‌روزرسانی شود.')
table(['نسخه','تغییر','وضعیت'],[['0.1.0','اولین تجمیع مستقل، ۸۳ ردیف و مقایسه ارجاعات، حفظ ورودی‌های تاریخی و ۱۳ پالایش','پیشنهادی برای مرور؛ پذیرش همه بندها باز'],['0.2.0 برنامه ریزی شده','رفع هم‌پوشانی و تصمیم نویسنده و قراردادهای CQ جدید','هنوز ایجاد نشده']],[.8,4.4,1.8])
heading('۱۱ منابع و مبنای بازتولید')
para('مرجع روش: M. C. Suarez-Figueroa, A. Gomez-Perez, B. Villazon-Terrazas. How to Write and Use the Ontology Requirements Specification Document. OTM 2009, LNCS 5871, pp. 966-982. DOI 10.1007/978-3-642-05151-7_16. https://oa.upm.es/5474/',english=True)
para('الگوی هفت‌بخشی شامل هدف، دامنه، زبان پیاده‌سازی، کاربران، کاربردها، نیازمندی‌ها و پیش‌واژه‌نامه از مرجع اقتباس ساختاری شده است؛ ردیابی، اولویت و ممیزی نسخه افزوده‌های این سند هستند. متن اصلی مرجع در این سند بازنشر نشده است.')
para('مبنای مخزن: '+BASE,english=True)
para('Repository: https://github.com/ArazSaieArasi3/CM-PharmE',english=True)
para('نشانی دقیق هر فایل و SHA256 آن در sources.json آمده است. شناسه منابع پایین در بندهای نیاز استفاده شده است. تاریخ مراجعه در این تجمیع ۲۰ اکتبر ۲۰۲۶ است؛ تاریخ اجرای شواهد آزمایشی عمدتاً ۹ اکتبر است.')
for s in sources:
 para(s['id']+'   '+s['path'],english=True)
for key,v in reconciled['sources'].items():para(key+'   '+v['title']+'   '+v['url'],english=True)
footer=sec.footer.paragraphs[0];rtl(footer);footer.add_run('CMPE 21 ORSD 0.1.0   |   ')
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');footer._p.append(fld)
name='CM_PharmE_2_1_ORSD_v0_1_0_FA'
DOC.save(OUT/(name+'.docx'))
md=['# CM PharmE 2.1 Ontology Requirements Specification Document','', 'Document version 0.1.0 | 2026-10-20 | Draft for author and domain review','',f'Baseline commit `{BASE}`. No ontology release or semantic approval is implied.','',data['counting_policy'],'','## Purpose','', 'A modular and traceable pharmaceutical ecosystem model for organizations, facilities, products, regulatory relations, supply and evidence. Retain RM, PV, BA and DS as purposeful small ontologies.','', '## Scope and representations','', 'Core plus reusable evidence, identity, geography and temporal infrastructure. Native OntoUML, OWL/RDF, SHACL/SPARQL and relational projections have distinct contracts. Clinical Care and universal legal compliance remain outside this commitment.','', '## Users and uses','', 'Regulators, pharmaceutical actors, PV/risk analysts, researchers, data stewards and developers. Principal uses: UC-01/02/03/04/05/07/09/10/15 and bounded UC-16/18.','', '## Requirements','']
for x in req:
 md += ['### '+x['id']+' '+x['domain'],'',x['statement_fa'],'',f"Origin: {x['origin']}; priority: {x['priority']}; acceptance: {x['acceptance_status']}",f"Sources: {', '.join(x['source_ids'])}; uses: {', '.join(x['use_cases'])}",f"Question: {x['cq'] or 'Quality acceptance check'}",f"Positive: {x['positive_acceptance']}",f"Negative: {x['negative_acceptance']}",f"Anchors: {', '.join(x['anchors'])}",f"Comparison: {x['comparison_status']}",f"Limit: {x['coverage_limit']}",'']
md+=['## Preglossary','']+[f'- **{a}**: {b}' for a,b in glossary]+['','## Assessment','',json.dumps(metrics,ensure_ascii=False,indent=2),'','Identifier availability is not semantic coverage. Historical tests were not rerun.','', '## Improvements','']+[f'- {p} {t}: {a}' for p,t,a in improvements]+['','## Method reference','',json.dumps(data['method_reference'],ensure_ascii=False),'','## Reproduction','', 'Run `python build.py` to regenerate canonical JSON, CSV, Markdown and DOCX. Run `python validate.py` for schema, hashes, references and historical module query replays. Render DOCX with the documents skill renderer; copy its PDF into this directory.','']
(OUT/'ORSD.md').write_text('\n'.join(md))
(OUT/'CHANGELOG.md').write_text('# Change history\n\n## 0.1.0 - 2026-10-20\n\nFirst independent CM-PharmE 2.1 ORSD. New specification of 32 core/infrastructure rows, import of 39 canonical working rows, 12 quality requirements. Retains 13 local refinements and separate 97 discovery / 51 held-out inventories. No new author approval. Identifier comparison only; historical module query replay results are recorded separately.\n')
print(json.dumps(metrics,ensure_ascii=False,indent=2))
