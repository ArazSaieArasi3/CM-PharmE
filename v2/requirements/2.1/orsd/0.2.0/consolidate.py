"""Consolidate a document baseline without modifying archived ontology packages."""
import pathlib,json,csv,hashlib,collections,copy
ROOT=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'v2/ontology/candidates').exists())
OUT=pathlib.Path(__file__).resolve().parent
OLD=OUT.parent/'0.1.0'
BASE='32a964f26add298b6df25bf9896d81b69e83b9fe'
d=json.loads((OLD/'requirements.json').read_text());d=copy.deepcopy(d)
decisions=[]
def dec(i,ids,relation,reason):decisions.append(dict(id=f'OV-{i:02}',requirement_ids=ids.split(),disposition=relation,rationale_fa=reason,status='DISPOSITION_RECORDED',level='specification editorial review; not expert ontology approval'))
dec(1,'FR-02 FR-03 FR-04 FR-32','GENERAL_AND_SCOPED_REQUIREMENTS','نقش زمینه‌ای قاعده عمومی است؛ بهره‌برداری، مسئولیت تولید و نقش توزیع موضوع و معیار مستقل دارند. FR-03 و FR-04 و FR-32 تخصص‌های کاربردی FR-02 هستند.')
dec(2,'FR-05 B2-RG-01','COMPLEMENTARY','FR-05 پیوند مرجع و موضوع ثبت را می‌خواهد؛ B2-RG-01 مرز ثبت مؤسسه و فهرست محصول را کنترل می‌کند. هیچ‌یک دیگری را پوشش کامل نمی‌دهد.')
dec(3,'R-DS-06 B2-RG-02 B2-RG-03','GENERAL_AND_SCOPED_REQUIREMENTS','عدم ایجاد مجوز از رکورد دیجیتال قاعده عمومی است؛ ثبت مؤسسه و NDC دو شاهد و محرک متفاوت برای آزمون همان مرز هستند. دو بند B2 تخصص‌های R-DS-06 هستند.')
dec(4,'FR-06 B2-RG-02 B2-RG-03','COMPLEMENTARY','قلمرو اعتبار مجوز با منع نتیجه‌گیری مجوز از ثبت یا فهرست تفاوت دارد؛ حفظ هر سه بند لازم است.')
dec(5,'FR-16 B2-RP-02','GENERAL_AND_SCOPED_REQUIREMENTS','مرز کلی وضعیت و گزارش در FR-16 ثبت می‌شود؛ گزارش کمبود بالقوه یک مورد تخصصی است که نباید کمبود واقعی ایجاد کند.')
dec(6,'FR-22 B2-RG-06','COMPLEMENTARY','دقت زمانی روز و ماه و سال با نقش تاریخ بازاریابی و دریافت داده تفاوت دارد؛ این دو بعد مستقل نگه داشته می‌شوند.')
dec(7,'FR-25 R-DS-04 B2-DS-09','COMPLEMENTARY','عضویت رکورد در نسخه مجموعه داده، تولید رکورد از فعالیت دیجیتال و اشتقاق مصنوعات سه مسیر ردیابی متفاوت‌اند؛ در یک شناسه ادغام نمی‌شوند.')
dec(8,'FR-26 R-RM-03 R-PV-03','GENERAL_AND_SCOPED_REQUIREMENTS','قاعده عمومی پشتیبانی ادعا و دو کاربرد ریسک و ایمنی حفظ می‌شوند. استناد ساده به منبع، تحقق خودکار EvidenceSupport واجد شرایط نیست؛ وضعیت مدل برای هر مسیر جدا ارزیابی می‌شود.')
dec(9,'FR-30 B2-RP-01 R-PV-06','COMPLEMENTARY','تفکیک محتوا از سند، مخاطب و سناریوی اعمال، و قلمرو الزام ایمنی سه معیار متفاوت‌اند و باید جدا آزموده شوند.')
dec(10,'FR-31','ATTACHED_REFINEMENT_NOT_EXTRA_REQUIREMENT','CL-03 پالایش محلی برای تعارض ادعاهای منبع است و به FR-31 پیوند می‌خورد؛ شمار نیازها را افزایش نمی‌دهد.')
dec(11,'B2-DS-10 R-RM-06','COMPLEMENTARY','نسخه‌بندی محتوای داده به ادغام هویت منجر نمی‌شود؛ رخداد بازبینی ریسک موضوع و زمان و نتایج قبلی و جدید دارد. دو سطح با شناسه مستقل حفظ می‌شوند.')
dec(12,'B2-DS-08 R-DS-04','COMPLEMENTARY','انتساب رکورد به عامل با ارتباط فعالیت تولیدکننده تفاوت دارد؛ تولیدکننده و مسئولیت و انتساب نباید یک رابطه شوند.')
dec(13,'NFR-01 FR-28','DISTINCT_LEVELS','NFR-01 پایداری شناسه عناصر خود انتالوژی است؛ FR-28 تخصیص شناسه دامنه به موجودیت واقعی است. مشابهت واژه شناسه دلیل تکراری‌بودن نیست.')
dec(14,'NFR-03 NFR-07','COMPLEMENTARY','حفظ معنا در تبدیل نمایش‌ها شرط مدل است؛ برابری پاسخ SQL و SPARQL یک ارزیابی رفتاری مستقل دارد.')
dec(15,'FR-14 FR-15','DISTINCT_CONCEPTS','قید حامل ظرفیت با تمایز خود ظرفیت از مشاهده اندازه‌گیری آن یکسان نیست؛ یکی جایگزین دیگری نمی‌شود.')
dec(16,'FR-18 FR-19','DISTINCT_CONTEXTUAL_CLASSIFICATIONS','بحرانی بودن و ضروری بودن دو نظام و تصمیم زمینه‌ای متفاوت‌اند؛ دو بند با دو فهرست شاهد حفظ می‌شوند.')
dec(17,'FR-01 R-DS-01','DISTINCT_DOMAIN_APPLICATIONS','هر دو مرز هویت را حفظ می‌کنند ولی موضوع سازمان و محل با جزء سامانه و رکورد متفاوت است؛ شاهد و خطای ناقض متفاوت دارند.')
dec(18,'R-DS-02 R-DS-05','COMPLEMENTARY','شناسه نسخه و زمان استقرار دو فیلد با نقش مستقل‌اند. زمان وقوع از نام نسخه یا تاریخ انتشار استنتاج نمی‌شود.')
dec(19,'R-BA-01 FR-14','DISTINCT_CAPABILITY_REQUIREMENTS','قابلیت سازمانی و ظرفیت عرضه الزاماً همان مفهوم نیستند؛ قید حامل در هر پروفایل با دامنه خود نگه داشته می‌شود.')
dec(20,'FR-23 R-RM-02','GENERAL_PATTERN_DISTINCT_EVENT_FAMILY','مشاهده و ارزیابی ریسک هر دو به تمایز رخداد و نتیجه نیاز دارند؛ بدون اثبات زیرنوع‌بودن ارزیابی ریسک از مشاهده، رابطه subsumption بین این دو نیاز ادعا نمی‌شود.')
dec(21,'FR-05 B2-RG-07','COMPLEMENTARY','وجود رابطه ثبت و حل هویت موضوع ثبت در برابر گزارش‌دهنده دو معیار مستقل‌اند؛ هر دو حفظ می‌شوند.')
dec(22,'FR-21 FR-06','COMPLEMENTARY','تمایز هستی‌شناختی جغرافیا و قلمرو با قید قلمرو یک مجوز متفاوت است.')
dec(23,'R-DS-04','PRIOR_MERGE_PRESERVED','B2-DS-07 در R-DS-04 ادغام قبلی شده است؛ به عنوان alias تاریخی حفظ می‌شود و شناسه مستقل فعال ندارد.')
dec(24,'NFR-05','DISTINCT_QUALITY_LEVEL','الزام آزمون مثبت و منفی یک قاعده کیفیت برای پروتکل ارزیابی است؛ وجود معیار پذیرش در نیازهای کارکردی آن را تکراری نمی‌کند.')

specializes={'FR-03':'FR-02','FR-04':'FR-02','FR-32':'FR-02','B2-RG-02':'R-DS-06','B2-RG-03':'R-DS-06','B2-RP-02':'FR-16','R-RM-03':'FR-26','R-PV-03':'FR-26'}
req=d['requirements']
for x in req:
 x['specification_disposition']='RETAIN_SCOPED_SPECIALIZATION' if x['id'] in specializes else 'RETAIN_DISTINCT_OBLIGATION'
 x['specializes_requirement_id']=specializes.get(x['id'])
 x['overlap_decision_ids']=[z['id'] for z in decisions if x['id'] in z['requirement_ids']]
 x['specification_status']='SPECIFIED_FOR_RESEARCH_BASELINE'
 x['acceptance_status']='PENDING_SEMANTIC_REVIEW'
 x['document_version']='0.2.0'
 if x['id']=='FR-31':x['related_refinement_ids']=sorted(set(x.get('related_refinement_ids',[])+['CL-03']))
 if x['id']=='R-BA-02':
  x['prior_anchors']=x['anchors'];x['anchors']=['capabilityRealizedInLogistics']
  x['experimental_anchors_present']=['capabilityRealizedInLogistics'];x['anchors_unresolved']=[]
  x['comparison_status']='EXPERIMENTAL_ONLY'
  x['expected_answer']='در گراف داده مورد آزمون، قابلیت فاقد اجرای ثبت شده بازیابی شود؛ قابلیت دارای اجرای ثبت شده در همان رابطه بازیابی نشود. جداگانه، وجود قابلیت بدون هیچ تحقق در این رابطه با مدل OWL سازگار بماند.'
  x['coverage_limit']='Resolved for the currently exported logistics realization relation only. No equivalence, alias or generic manufacturing realization is asserted. Missing recorded execution is not real-world nonexecution.'
  x['evidence_status']='FRESH_BOUNDED_QUERY_COUNTERMODEL_AND_MUTATION'
  x['mapping_decision_id']='MAP-BA-02'
  x['prior_cq_text']=x['cq']
  x['cq']='کدام قابلیت در گراف بررسی شده فاقد اجرای لجستیک ثبت شده است؟'

contracts=[]
for x in req:
 c=dict(id='AC-'+x['id'],requirement_id=x['id'],kind=x['kind'],priority=x['priority'],purpose=x['statement_fa'],question=x.get('cq'),input=dict(graph='A versioned declared-scope dataset or a pinned model snapshot',subject='A named instance or model element appropriate to '+x['domain'],source_requirement='Record the exact input source and sampling boundary'),expected_answer=x['expected_answer'],positive_oracle=x['positive_acceptance'],negative_oracle=x['negative_acceptance'],boundary_oracle='Missing information must stay unknown unless the declared admission profile explicitly requires it; no inferred global negation.',model_anchors=x['anchors'],source_ids=x['source_ids'],independence_rule='Fix the requirement and oracle before fixture construction; do not copy current implementation output into expected values.',acceptance_status='PENDING_SEMANTIC_REVIEW',execution_status='SPECIFIED_NOT_EXECUTED',execution_refs=[])
 if x['id'].startswith('R-'):
  c['execution_status']='BOUNDED_PRIOR_CONTRACT_REPLAY'
  c['execution_refs']=x.get('original_cq_ids',[])
 if x['id']=='R-BA-02':c['execution_status']='FRESH_QUERY_AND_COUNTERMODEL';c['execution_refs']=['BA02-zero-recorded','BA02-executed','BA02-mixed','BA02-countermodel','BA02-mutant-countermodel','BA02-positive-world']
 if x['id']=='R-BA-02':
  c['input']['realization_relations']=['https://w3id.org/cm-pharme/experimental/coherence/capabilityRealizedInLogistics']
  c['expected_bindings']=['cap','org']
  c['absence_policy']='No matching realization recorded in this graph under the selected relation. Not real-world nonexecution.'
 if x['kind']=='nonfunctional':
  c['checking_mode']='REPRODUCTION_OR_REVIEW_PROTOCOL'
  c['execution_status']='REVIEW_PROTOCOL_SPECIFIED'
 else:c['checking_mode']='QUERY_AND_ADMISSION_OR_REASONER_AS_REQUIRED'
 contracts.append(c)

queries={
'corrected':'''PREFIX c: <https://w3id.org/cm-pharme/2.1/> PREFIX d: <https://w3id.org/cm-pharme/experimental/coherence/>
SELECT DISTINCT ?cap ?org WHERE { ?cap a c:EnterpriseCapability ; c:capabilityBearer ?org . FILTER NOT EXISTS { ?cap d:capabilityRealizedInLogistics ?activity } } ORDER BY ?cap ?org''',
'recorded_execution':'''PREFIX c: <https://w3id.org/cm-pharme/2.1/> PREFIX d: <https://w3id.org/cm-pharme/experimental/coherence/>
SELECT DISTINCT ?cap ?activity WHERE { ?cap a c:EnterpriseCapability ; d:capabilityRealizedInLogistics ?activity } ORDER BY ?cap ?activity'''}
for name,q in queries.items():(OUT/'verification'/f'ba02-{name}.rq').write_text(q+'\n')
ba_map=dict(id='MAP-BA-02',prior_reference='https://w3id.org/cm-pharme/experimental/four-domain/capabilityRealizedIn',selected_reference='https://w3id.org/cm-pharme/experimental/coherence/capabilityRealizedInLogistics',decision='Bind the current scoped CQ to the exported logistics relation. Retire the old generic query as evidence for this ORSD row; preserve historical files. Do not assert owl:equivalentProperty or rename the ontology silently.',status='SCOPED_MAPPING_RESOLVED',generic_requirement_status='Still requires future per-domain realization paths if scope expands',queries=queries)
d.update(document_version='0.2.0',date='2026-10-21',status='CONSOLIDATED_RESEARCH_SPECIFICATION_BASELINE',previous_document_version='0.1.0',previous_document_commit=BASE,model_baseline_commit=d['baseline_commit'],document_closure=dict(editorial_and_traceability='COMPLETE_FOR_DECLARED_SCOPE',independent_expert_approval='NOT_PERFORMED',ontology_release='NOT_DECLARED',next_document_action='One author content review, then freeze 1.0.0; broader model verification is tracked separately.'),overlap_decisions=decisions,acceptance_contracts=contracts,mapping_decisions=[ba_map])
d['metrics']['comparison_counts']=dict(collections.Counter(x['comparison_status'] for x in req))
d['metrics'].update(overlap_decisions=len(decisions),unresolved_document_mapping_rows=0,specified_acceptance_contracts=len(contracts),functional_contracts=sum(x['kind']=='functional' for x in contracts),quality_protocols=sum(x['kind']=='nonfunctional' for x in contracts),scoped_specializations=len(specializes))
d['counting_policy']='83 retained tracked rows: 71 functional and 12 quality. Eight functional rows are explicit scoped specializations. Counts are neither independent domain needs nor expert-approved requirements. Thirteen refinements remain attached; B2-DS-07 remains merged into R-DS-04.'
for rel in ['v2/requirements/2.1/orsd/0.1.0/requirements.json','v2/ontology/candidates/2.1.0-alpha.1-module-contract-lab/modules/BA/ontology.ttl','v2/ontology/candidates/2.1.0-alpha.1-module-contract-lab/modules/BA/shapes.ttl','v2/ontology/candidates/2.1.0-alpha.1-module-contract-lab/modules/BA/hierarchy.ttl']:
 if not any(x['path']==rel for x in d['sources']):
  d['sources'].append(dict(id=f'S{len(d["sources"])+1:02}',path=rel,sha256=hashlib.sha256((ROOT/rel).read_bytes()).hexdigest(),url=f'https://github.com/ArazSaieArasi3/CM-PharmE/blob/{BASE}/{rel}',fresh_execution=False))
(OUT/'sources.json').write_text(json.dumps(d['sources'],ensure_ascii=False,indent=2)+'\n')
for name,obj in [('requirements.json',d),('overlap-decisions.json',decisions),('acceptance-contracts.json',contracts),('mapping-decisions.json',[ba_map]),('comparison.json',dict(model_baseline_commit=d['baseline_commit'],counts=d['metrics']['comparison_counts'],scope='Identifier availability only; not semantic coverage',requirements=[{k:x[k] for k in ['id','comparison_status','anchors','specification_disposition','specializes_requirement_id','acceptance_status']} for x in req]))]:
 (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
with (OUT/'traceability.csv').open('w',encoding='utf-8-sig',newline='') as f:
 fields=['id','kind','priority','domain','statement_fa','specification_disposition','specializes_requirement_id','overlap_decision_ids','anchors','comparison_status','acceptance_status']
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for x in req:w.writerow({k:';'.join(x[k]) if isinstance(x[k],list) else x[k] for k in fields})
print(json.dumps(d['metrics'],ensure_ascii=False))
