# بررسی ۲۲ فیلد پروفایل پیشین

این طبقه‌بندی پیشنهاد طراحی است؛ تمام فیلدهای schema یا کل انتالوژی را پوشش نمی‌دهد. تبدیل به مفهوم native در این اجرا انجام نشد.

| فیلد | دسته | سیاست پیشنهادی |
|---|---|---|
| actionAnnounced | regulatory-context-review | Evidence of a specified reporting action; do not make it a timeless requirement property. |
| actorRole | regulatory-context-review | Model applicability of a role in context; string values are current interface vocabulary. |
| approvalConclusion | query-conclusion | Separate source claim and computed answer; never derive authorization from listing. |
| authorizationRoute | regulatory-context-review | Context selector CAP/NAP; not proof of current product approval. |
| externalKey | source-identity-metadata | Source-scoped key; evaluate reuse of IdentifierAssignment only when scheme/authority truthmakers exist. |
| frequency | regulatory-context-review | Versioned action-specific obligation; no universal cadence. |
| jurisdiction | regulatory-context-review | Context of applicability; distinguish listingJurisdiction from reporting applicability. |
| marketingEnd | source-asserted-time | Missing means unspecified; no infinite interval assumption in current query contract. |
| marketingStart | source-asserted-time | Bind to product or package explicitly. Do not coalesce levels or use retrieval time. |
| payloadFormat | source-format-metadata | Carrier syntax metadata; not a product characteristic. |
| profile | validation-control | Keep as admission metadata; no domain class. |
| recordKind | source-format-metadata | Source-schema discriminator; do not equate to native stereotypes. |
| recordSubject | content-aboutness-review | Keep record/content/subject distinct; existing carrierClaim + typed assertion aboutness may cover claims, not automatically every record. |
| release | existing-path-candidate | Candidate inverse path of containsSourceRecord in this ingestion contract only; no new native relation needed yet. |
| representsFact | content-aboutness-review | Source assertion about a registration/listing; requires a representation/claim bridge, not identity. |
| retrievedAt | provenance-metadata | Retrieval occurrence time; not product marketing or original generation time. |
| scenario | regulatory-context-review | Routine/preparedness/crisis selector; not an actual disruption event. |
| scopeComplete | validation-control | Local completeness assertion; never global closed-world completeness. |
| scopedProduct | regulatory-context-review | Declared product scope of one action; absence is not global exclusion. |
| shortageStatus | source-asserted-status | Potential/actual label belongs to claim; never alone instantiate a shortage situation. |
| sourceVersion | source-identity-metadata | Version of the cited rule/guidance snapshot, not event time. |
| version | source-identity-metadata | Record version; distinctness/lineage must be explicit. |

فیلدهای جدید Q در شاهدهای مثبت: 18. این‌ها متادیتای منبع یا کنترل سناریو هستند؛ فهرست دقیق در field-audit.json ثبت شده است.
