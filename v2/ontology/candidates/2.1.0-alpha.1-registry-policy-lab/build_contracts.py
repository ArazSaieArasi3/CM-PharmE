"""Desk reconciliation of a bounded source batch; no scientific acceptance."""
import copy,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent
OLD=H.parent/'2.1.0-alpha.1-four-domain-lab'
B2=H.parent/'2.1.0-alpha.1-derived-participant-lab'
def write(name,d):(H/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

DECISIONS={
 'RG-01':('RETAIN','Registration and listing have different subjects and facts; no matching prior requirement.'),
 'RG-02':('RETAIN_SCOPED_EXTENSION','R-DS-06 addresses digital records, not establishment-registration facts.'),
 'RG-03':('RETAIN_SCOPED_EXTENSION','NDC identification/listing is a distinct insufficient premise from registration and mere record existence.'),
 'RG-04':('RETAIN','Submitting labeler attribution is not regulatory verification or listing responsibility.'),
 'RG-05':('RETAIN','Source-scoped absence and global negative conclusions were not addressed by the prior 24.'),
 'RG-06':('RETAIN','Marketing validity and retrieval time differ from deployment time and result timestamps.'),
 'RP-01':('RETAIN_SCOPED_EXTENSION','R-PV-06 constrains jurisdiction; actor-role and scenario selectors add independent criteria.'),
 'RP-02':('RETAIN','Potential-shortage content is distinct from an actual situation; PV signal criteria do not establish this.'),
 'RP-03':('RETAIN','Product authorization route and action-specific scope are independent selectors.'),
 'RP-04':('RETAIN','Action-scoped frequency and version selection are distinct from the existence of a timestamp.'),
 'DS-07':('REFINE_EXISTING','Fold generation traversal and record/activity separation into R-DS-04; retain B2 alias and source provenance.'),
 'DS-08':('RETAIN','Artifact attribution and activity association are different responsibilities; neither implies the other.'),
 'DS-09':('RETAIN_SCOPED_EXTENSION','Artifact-to-artifact derivation is not the same relation as record-to-generating-activity.'),
 'DS-10':('RETAIN_SCOPED_EXTENSION','R-RM-06 is review ordering and R-DS-02 is component version tracing; artifact revision adds a lineage contract.'),
 'RG-07':('REFINE_AND_RETAIN','Separate record from subject; reporter may equal organizational subject. Do not impose pairwise distinctness universally.'),
 'RG-08':('RETAIN_SCOPED_EXTENSION','SPL payload-to-subject representation differs from component-record identity and subject/reporter resolution.')}

def main():
 old=json.loads((OLD/'requirement-traceability.json').read_text())['requirements']
 source=json.loads((B2/'source-requirements.json').read_text())
 out=[]
 for r in source['requirements']:
  row=copy.deepcopy(r);short=r['id'][3:];decision,reason=DECISIONS[short]
  row.update(desk_decision=decision,decision_reason=reason,canonical_requirement_id='R-DS-04' if short=='DS-07' else r['id'],
   desk_review_scope='All prior 24 headings and acceptance criteria plus the other 15 B2 rows; human expert acceptance pending.',
   original_statement=r['statement'],mapping_state='EXPERIMENTAL_PROFILE_WITH_NATIVE_GAPS',scientific_acceptance=False)
  if short=='RG-07':
   row.update(statement='Keep a source record distinct from its represented subject; resolve reporter identity without requiring reporter and organizational subject to differ.',
    positive_acceptance='An organizational subject may report on itself; record identity remains separate.',
    negative_acceptance='Reject record-subject identity collision, including known owl:sameAs aliases.')
  if short=='RG-06':
   row['clarification']='Date fields support a declared publication-window check, not a promise that the actual directory contains the entry; retrieval time can equal marketing time by coincidence.'
  if short=='RP-01':row['clarification']='Synthetic applicability profiles are bounded encodings of cited guidance, not a complete legal compliance engine.'
  out.append(row)
 catalogue=[{'id':r['id'],'source_row_ids':[r['id']],'original_statement_fa':r['statement_fa'],'accepted':False} for r in old]
 for row in out:
  if row['desk_decision']=='REFINE_EXISTING':
   entry=next(r for r in catalogue if r['id']==row['canonical_requirement_id']);entry['source_row_ids'].append(row['id']);entry['proposed_refinement']=row['statement']
  else:catalogue.append({'id':row['id'],'source_row_ids':[row['id']],'statement':row['statement'],'accepted':False})
 assert len(catalogue)==39 and sum(len(r['source_row_ids']) for r in catalogue)==40
 source['sources']['FDA-DRLS'].update(resolved_url='https://www.fda.gov/drugs/guidance-compliance-regulatory-information/electronic-drug-registration-and-listing-system-edrls',resolved_title='Electronic Drug Registration and Listing System (eDRLS)')
 data={'status':'DESK_RECONCILED_PROPOSAL_CATALOGUE','sources':source['sources'],'requirements':out,'canonical_proposal_headings':catalogue,
  'input_rows':40,'prior_rows':24,'new_batch_rows':16,'desk_decisions':16,'merged_into_existing_headings':1,'retained_batch_headings':15,
  'working_heading_count':39,'accepted_requirements':0,'all_project_requirements_exhaustive':False,
  'count_limit':'39 is a reconciled working heading count for these two inputs only, not a claim of global completeness or independent expert validation.',
  'changes_to_prior_contracts':['B2-DS-07 proposed as refinement of R-DS-04, without rewriting original files.','B2-RG-07 universal reporter/subject separation withdrawn in favor of record/subject separation.'],
  'input_sha256':{str(p.relative_to(H.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [OLD/'requirement-traceability.json',B2/'source-requirements.json']}}
 write('reconciled-requirements.json',data)
 lines=['# تطبیق نیازمندی‌ها — پیشنهاد برای پذیرش',
 '۱۶/۱۶ بند جدید با ۲۴ بند قبلی و بندهای هم‌دسته مقایسه شد. یک بند (DS-07) در R-DS-04 به‌عنوان اصلاح پیشنهادی ادغام می‌شود؛ ۱۵ عنوان حفظ می‌شود. ۴۰ ردیف ورودی به ۳۹ عنوان کاری ردیابی شده‌اند. این عدد، پوشش کامل پروژه یا پذیرش علمی نیست.',
 'اصلاح معنایی RG-07: رکورد از موضوعش جداست؛ ثبت‌کننده می‌تواند همان سازمانِ موضوع ثبت باشد. قید تمایز عمومیِ همهٔ طرف‌ها کنار گذاشته شد. RG-06 نیز فقط پنجرهٔ زمانی انتشار را می‌سنجد؛ وجود واقعی رکورد یا تفاوت اجباری تاریخ‌ها را نتیجه نمی‌دهد.',
 '| بند | تصمیم پیشنهادی | دلیل |','|---|---|---|']
 for r in out:lines.append('| '+r['id']+' | '+r['desk_decision']+' → '+r['canonical_requirement_id']+' | '+r['decision_reason']+' |')
 (H/'reconciliation-fa.md').write_text('\n\n'.join(lines[:3])+'\n\n'+'\n'.join(lines[3:])+'\n')
 print(json.dumps({'reviewed':16,'working_headings':39,'source_rows_preserved':40,'accepted':0}))

if __name__=='__main__':main()
