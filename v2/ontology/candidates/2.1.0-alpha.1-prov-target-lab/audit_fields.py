"""Desk triage of all 22 previously inventoried positive-fixture profile fields.
Not a claim to have covered every field appearing in schema/negative controls.
"""
from common import *
old=json.loads((REG/'mapping-audit.json').read_text())
policies={
 'profile':('validation-control','Keep as admission metadata; no domain class.'),
 'scopeComplete':('validation-control','Local completeness assertion; never global closed-world completeness.'),
 'approvalConclusion':('query-conclusion','Separate source claim and computed answer; never derive authorization from listing.'),
 'externalKey':('source-identity-metadata','Source-scoped key; evaluate reuse of IdentifierAssignment only when scheme/authority truthmakers exist.'),
 'sourceVersion':('source-identity-metadata','Version of the cited rule/guidance snapshot, not event time.'),
 'version':('source-identity-metadata','Record version; distinctness/lineage must be explicit.'),
 'retrievedAt':('provenance-metadata','Retrieval occurrence time; not product marketing or original generation time.'),
 'payloadFormat':('source-format-metadata','Carrier syntax metadata; not a product characteristic.'),
 'recordKind':('source-format-metadata','Source-schema discriminator; do not equate to native stereotypes.'),
 'release':('existing-path-candidate','Candidate inverse path of containsSourceRecord in this ingestion contract only; no new native relation needed yet.'),
 'recordSubject':('content-aboutness-review','Keep record/content/subject distinct; existing carrierClaim + typed assertion aboutness may cover claims, not automatically every record.'),
 'representsFact':('content-aboutness-review','Source assertion about a registration/listing; requires a representation/claim bridge, not identity.'),
 'marketingStart':('source-asserted-time','Bind to product or package explicitly. Do not coalesce levels or use retrieval time.'),
 'marketingEnd':('source-asserted-time','Missing means unspecified; no infinite interval assumption in current query contract.'),
 'shortageStatus':('source-asserted-status','Potential/actual label belongs to claim; never alone instantiate a shortage situation.'),
 'actionAnnounced':('regulatory-context-review','Evidence of a specified reporting action; do not make it a timeless requirement property.'),
 'actorRole':('regulatory-context-review','Model applicability of a role in context; string values are current interface vocabulary.'),
 'authorizationRoute':('regulatory-context-review','Context selector CAP/NAP; not proof of current product approval.'),
 'frequency':('regulatory-context-review','Versioned action-specific obligation; no universal cadence.'),
 'jurisdiction':('regulatory-context-review','Context of applicability; distinguish listingJurisdiction from reporting applicability.'),
 'scenario':('regulatory-context-review','Routine/preparedness/crisis selector; not an actual disruption event.'),
 'scopedProduct':('regulatory-context-review','Declared product scope of one action; absence is not global exclusion.')}
rows=[]
for item in old['predicate_inventory']:
 if item['iri'].startswith(str(P)):
  name=item['iri'][len(str(P)):];category,note=policies[name]
  rows.append({'field':name,'category':category,'design_note':note,'native_change':False,'author_accepted':False})
assert len(rows)==22 and set(policies)=={x['field'] for x in rows}
predicates=set()
for f in [H/'ndc-abox.ttl']+list((H/'target-fixtures').glob('*-positive.ttl')):
 for _,p,_ in Graph().parse(f):
  if str(p).startswith(str(Q)):predicates.add(str(p))
out={'previous_positive_fixture_fields':rows,'reviewed':len(rows),'new_positive_fixture_Q_predicates':sorted(predicates),
 'no_native_addition_from_these_fields':True,
 'next_design':'Develop the minimum contextual reporting-applicability model and record/claim/fact bridge from source witnesses; reuse provenance/source metadata instead of adding a native class per field.',
 'limit':'Desk triage only, not complete implementation or scientific acceptance. Other fields in SHACL/negative controls, e.g. approvalEvidence, are outside the historical 22-field inventory.'}
write('field-audit.json',out)
lines=['# بررسی ۲۲ فیلد پروفایل پیشین','', 'این طبقه‌بندی پیشنهاد طراحی است؛ تمام فیلدهای schema یا کل انتالوژی را پوشش نمی‌دهد. تبدیل به مفهوم native در این اجرا انجام نشد.','', '| فیلد | دسته | سیاست پیشنهادی |','|---|---|---|']
lines += ['| '+x['field']+' | '+x['category']+' | '+x['design_note']+' |' for x in rows]
lines+=['','فیلدهای جدید Q در شاهدهای مثبت: '+str(len(predicates))+'. این‌ها متادیتای منبع یا کنترل سناریو هستند؛ فهرست دقیق در field-audit.json ثبت شده است.']
(H/'field-audit-fa.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'reviewed':len(rows),'new_Q_predicates':len(predicates)}))
