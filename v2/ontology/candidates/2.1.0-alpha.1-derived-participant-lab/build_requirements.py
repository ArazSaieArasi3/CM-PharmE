"""Source-first proposal batch, explicitly separate from accepted requirements."""
import json
from pathlib import Path
H=Path(__file__).resolve().parent
S={
 'FDA-DRLS':{'url':'https://www.fda.gov/drug-registration-and-listing','title':'Drug Registration and Listing','locator':'Overview; Submitting data to FDA'},
 'FDA-NDC':{'url':'https://www.fda.gov/drugs/drug-approvals-and-databases/national-drug-code-directory','title':'National Drug Code Directory','locator':'About the NDC directory, bullets 1–6; Adding, correcting or updating'},
 'EMA-ESMP':{'url':'https://www.ema.europa.eu/en/human-regulatory-overview/post-authorisation/medicine-shortages-availability-issues/european-shortages-monitoring-platform','title':'European Shortages Monitoring Platform','locator':'Reporting via ESMP: Normal circumstances / MSSG-led preparedness / Crisis'},
 'W3C-PROV':{'url':'https://www.w3.org/TR/2013/REC-prov-o-20130430/','title':'PROV-O: The PROV Ontology','locator':'Sections 3.1, 4.1 wasGeneratedBy/wasAttributedTo/wasAssociatedWith, 4.2 wasDerivedFrom/wasRevisionOf'}
}
for s in S.values():s.update(accessed='2026-10-09',source_kind='PRIMARY',full_legal_or_standard_implementation=False)

# Statements and acceptance criteria are our modeling proposals, not quotations
# or claims that the agencies prescribe CM-PharmE's implementation.
rows=[
 ('RG-01','FDA-DRLS','Registry','Keep establishment registration separate from drug listing.',
  'Which subject is registered or listed?','Facility registration and product listing remain distinct.','Registration alone cannot create a product listing.',
  ['EstablishmentRegistration','MarketListing','rel-registrationEntity','rel-listingPresentation'],'Record-to-fact mapping unresolved.',[]),
 ('RG-02','FDA-DRLS','Registry','Registration must not imply product approval.',
  'Does registration establish approval?','Answer unknown without approval evidence.','Reject registration-to-approval inference.',
  ['EstablishmentRegistration','RegulatoryAuthorization'],'Existing authorizationParty targets organizations/facilities; product approval representation unresolved.',['R-DS-06']),
 ('RG-03','FDA-NDC','Registry','NDC listing must not imply approval.',
  'What approval evidence supports this product?','Listed product may have unknown approval.','NDC presence cannot supply approval evidence.',
  ['IdentifierAssignment','IdentifierScheme','MarketListing','EvidenceSupport'],'Approval evidence path unresolved.',['R-DS-06']),
 ('RG-04','FDA-NDC','Registry','Attribute submitted directory information to its labeler.',
  'Who supplied this entry?','Return submitting labeler.','Do not substitute FDA verification.',
  ['SourceRecord','Organization','Assertion'],'Submitter attribution differs from listing responsibility.',[]),
 ('RG-05','FDA-NDC','Registry','Directory absence must preserve uncertainty.',
  'What follows from a missing entry?','Return not-found within this source.','Do not infer unapproved or nonexistent.',
  ['SourceRecord','DatasetRelease'],'Query absence policy required.',[]),
 ('RG-06','FDA-NDC','Registry','Distinguish marketing dates from retrieval dates.',
  'Was the entry published at the queried time?','Apply declared source publication conditions.','Do not equate retrieval with marketing start.',
  ['SourceRecord','DatasetRelease','MarketListing','TimeInterval'],'Bitemporal source profile needed.',[]),
 ('RP-01','EMA-ESMP','Regulatory Policy','Qualify reporting obligations by actor role and scenario.',
  'Who reports under this scenario?','Return applicable MAH/NCA roles.','Do not generalize one scenario globally.',
  ['RegulatoryRequirement','Organization','RegulatoryJurisdiction'],'Scenario applicability path absent.',['R-PV-06']),
 ('RP-02','EMA-ESMP','Regulatory Policy','Separate potential-shortage reports from actual shortage situations.',
  'Is this a forecast or actual shortage?','Potential report remains an assertion.','Forecast alone cannot establish actual shortage.',
  ['Assertion','MedicineShortageSituation','SourceRecord'],'Potential/actual assessment policy needed.',[]),
 ('RP-03','EMA-ESMP','Regulatory Policy','Constrain reporting product scope to the selected scenario.',
  'Are CAPs, NAPs or selected medicines in scope?','Use the scenario-specific scope.','Do not apply routine CAP scope universally.',
  ['RegulatoryRequirement','MedicinalProduct','ContextualMedicineClassificationAssignment'],'Authorization route and scenario membership unresolved.',[]),
 ('RP-04','EMA-ESMP','Regulatory Policy','Bind reporting frequency to the announced action.',
  'Which frequency applies to this action?','Retrieve that action’s frequency.','Do not hard-code a universal interval.',
  ['RegulatoryRequirement','ReportingPeriod','TimeInterval'],'Trigger/version/time linkage unresolved.',[]),
 ('DS-07','W3C-PROV','Digital Systems','Distinguish a generated record from its generating activity.',
  'Which activity generated this record?','Return a linked distinct activity.','Do not identify activity with output.',
  ['SourceRecord','ProvenanceActivity'],'Generic provenance alignment pending.',['R-DS-01','R-DS-04']),
 ('DS-08','W3C-PROV','Digital Systems','Distinguish entity attribution from activity association.',
  'Is responsibility attached to artifact or activity?','Return the qualified relation.','Do not collapse both predicates.',
  ['SourceRecord','ProvenanceActivity','Organization'],'Agent typing and responsibility mapping pending.',[]),
 ('DS-09','W3C-PROV','Digital Systems','Retain derivation lineage between data artifacts.',
  'Which artifact was this derived from?','Return predecessor lineage.','Source absence cannot invent lineage.',
  ['SourceRecord','Dataset','DatasetRelease'],'Derivation relation not mapped.',['R-DS-04']),
 ('DS-10','W3C-PROV','Digital Systems','Represent revision lineage without automatic identity merging.',
  'Which prior version was revised?','Keep both versions and revision link.','Revision alone must not assert owl:sameAs.',
  ['SourceRecord','DatasetRelease'],'Revision identity policy unresolved.',['R-RM-06','R-DS-02']),
 ('RG-07','FDA-DRLS','Registry','Keep registration entity, reporting organization and source record distinct.',
  'Which organization reported on which establishment?','Return separately identified subjects and report.','Do not merge subjects through one source ID.',
  ['RegisteredFacilityRole','RegisteredOrganizationRole','SourceRecord'],'Subject resolution policy required.',['R-DS-01']),
 ('RG-08','FDA-DRLS','Registry','Treat SPL as a submission representation.',
  'Which submission represents the listed drug?','Trace submission to represented subject.','Do not identify payload with physical product.',
  ['SourceRecord','MedicinalProduct','Assertion'],'Payload/carrier/claim mapping unresolved.',['R-DS-01'])
]

def main():
 model=json.loads((H.parent/'2.1.0-alpha.1-four-domain-refinement/ontouml-experimental.json').read_text())
 ids={x['id'] for x in model['elements']}
 old={x['id'] for x in json.loads((H.parent/'2.1.0-alpha.1-four-domain-lab/requirement-traceability.json').read_text())['requirements']}
 requirements=[]
 for rid,sid,domain,statement,cq,pos,neg,mapping,gap,overlap in rows:
  assert all(x in ids for x in mapping),rid
  assert all(x in old for x in overlap),rid
  requirements.append({'id':'B2-'+rid,'source_id':sid,'domain':domain,'statement':statement,
   'competency_question':cq,'positive_acceptance':pos,'negative_acceptance':neg,
   'candidate_existing_ids':mapping,'mapping_gap':gap,'related_prior_requirement_ids':overlap,
   'overlap_status':'PARTIAL_OVERLAP_REQUIRES_DEDUPLICATION' if overlap else 'NO_DIRECT_MATCH_IN_PRIOR_24_BY_DESK_REVIEW',
   'origin':'SOURCE_DERIVED_MODELING_PROPOSAL','author_accepted':False,
   'baseline_implementation_verified':False,'dedicated_executable_acceptance_tests':0})
 out={'status':'SOURCE_FIRST_PROPOSALS_NOT_ACCEPTED','sources':S,'requirements':requirements,
  'batch_rows':len(requirements),'prior_requirement_rows':24,'accepted_new_requirements':0,
  'total_unique_project_requirements':None,'reason_no_combined_total':'Partial overlaps and all-domain extraction remain unresolved.'}
 (H/'source-requirements.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 lines=['# بستهٔ نیازمندی‌های مستقل رجیستری، سیاست مقرراتی و منشأ داده',
 '۱۶ پیشنهاد از چهار منبع اصلی؛ هر بند پرسش شایستگی، معیار مثبت/منفی و نگاشت اولیه دارد. این‌ها طراحی پیشنهادی‌اند؛ اجرای حقوقی یا انطباق با استاندارد ادعا نمی‌شود.',
 '۲۴ نیازمندی قبلی حفظ شده است. به دلیل هم‌پوشانی، جمع ۴۰ نیازمندی یکتا گزارش نمی‌شود. آزمون اجرایی اختصاصی این ۱۶ بند و پذیرش آن‌ها هنوز صفر است.',
 '| شناسه | دامنه | نیاز پیشنهادی | شکاف | هم‌پوشانی قبلی |','|---|---|---|---|---|']
 for r in requirements:lines.append('| '+' | '.join([r['id'],r['domain'],r['statement'],r['mapping_gap'],', '.join(r['related_prior_requirement_ids']) or 'تطابق مستقیم یافت نشد'])+' |')
 lines+=['','مشخصات کامل، پرسش‌ها، معیارها و نشانی دقیق منابع در `source-requirements.json` است.',
  'پیشنهاد مرز N06: رجیستری، هویت منبع/شناسه/رکورد و وضعیت ثبت داده را مدیریت کند؛ ادعای مجوز، تعهد یا وضعیت واقعی از مسیر شواهد و مفاهیم تخصصی آن دامنه بیان شود. نبود داده «نامعلوم» بماند.',
  'پیشنهاد N07: RegulatoryRequirement با زمینهٔ اعمال شامل قلمرو، نقش مخاطب، سناریو، موضوع، زمان و نسخهٔ منبع پیوند بخورد. فعلاً ایجاد کلاس تازه، قانون انطباق عمومی یا پیوند اجباری به تمام محصولات تصویب نشده است.',
  'شکاف تازه: RegulatoryAuthorization موجود به AuthorizedParty سازمان/تأسیسات وصل می‌شود؛ این مسیر به‌تنهایی مدل مجوز محصول نیست. افزودن معنای product approval به آن بدون تصمیم علمی مجاز شمرده نشده است.',
  'گام بعد: رفع هم‌پوشانی، انتخاب نیازهای ضروری نسخه، سپس ساخت شاهد مستقل و آزمون عدم‌استنتاج برای ۱۶ بند. چهار دامنهٔ محل بحث حفظ می‌شوند؛ جایگاه نهایی هنوز باز است.']
 (H/'source-requirements-fa.md').write_text('\n\n'.join(lines[:3])+'\n\n'+'\n'.join(lines[3:])+'\n')
 print(json.dumps({'rows':len(requirements),'sources':len(S),'existing_mapping_ids_checked':True,'overlapping_rows':sum(bool(r['related_prior_requirement_ids']) for r in requirements),'accepted':0}))

if __name__=='__main__':main()
