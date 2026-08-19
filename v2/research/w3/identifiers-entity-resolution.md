# W3 Identifier and Entity-Resolution Requirements

## Objective
Define identity-reconciliation requirements before implementation so heterogeneous source identifiers are not mistaken for universal real-world identity.

## 1. Identifier pattern
W3 admits three infrastructure candidates:
- **Identifier** — a symbolic value used to identify a source/domain entity under a defined scheme.
- **Identifier Scheme** — defines the scope/issuer/syntax of identifiers.
- **Identifier Assignment** — context connecting identifier, identified entity, scheme/source and validity.

This allows the same real-world entity to carry several source-scoped identifiers without asserting that any one identifier is globally authoritative.

## 2. Identifier families already present in discovery sources
| Family | Source | Intended semantic use | Important boundary |
|---|---|---|---|
| NHIF medicine code | P1/P2 | Source-scoped reimbursable medicinal item/product identity | Not a universal medicinal-product identifier. |
| ATC code | P1/P2/P6 | Product/substance therapeutic classification | Classification, not entity identity. |
| INN/common name | P1/P2/P5/P6 | Substance naming/cross-reference | Name alone does not guarantee exact entity match. |
| Hospital/facility code | P2 | Source-scoped facility identity | May represent operational facility rather than legal organization. |
| Regional code | P1/P2 | Administrative reporting region | Normalize separately to geography. |
| Product NDC / Package NDC | P4 | U.S. product/package identifier | Source/jurisdiction specific; package/product granularity differs. |
| SPL ID / SPL Set ID | P4 | Structured Product Label/submission identity/version family | Information artifact identity, not medicinal product itself. |
| Application Number | P4 | Regulatory application reference | Regulatory record reference, not product identity alone. |
| UNII | P4/S1 | Substance identifier | Substance-level, not product-level. |
| RxCUI | P4 | Harmonized clinical-drug concept identifier where available | External terminology concept, scope-specific. |
| Establishment/registration IDs | P3 | Registered site/establishment record identity | Registration record/site/organization must be distinguished. |
| License/reporting identifiers | P3 | Facility/license reporting identity | One facility can have multiple licenses. |
| EMA/OMS identifiers | C2 where available | Organization/location identity in EMA ecosystem | Automated ingestion remains conditional. |
| GeoNames ID | P7 | Geographic feature identity | Geographic normalization only. |
| Dataset DOI/version | P1/P2/C1/S2 | Research dataset/release identity | Identifies dataset artifact, not domain entity. |

## 3. Entity-resolution target types
Priority target types for W6/W7:
1. **Organization** — names/addresses/roles may vary by source.
2. **Site/Facility** — physical location matching must remain separate from legal organization matching.
3. **Medicinal Product / Presentation** — product name, form, strength, package and source identifiers must be considered jointly.
4. **Pharmaceutical Substance** — INN/UNII/other controlled identifiers can support stronger exact/crosswalk matching.
5. **Geographic Feature / Region** — normalize through GeoNames/native region codes while preserving source labels.

## 4. Match-state model
Entity resolution should not use a binary “same/different” field only. W3 requires at least:
- **Exact identifier match** — same valid identifier in the same scheme.
- **Authoritative crosswalk match** — different identifiers linked by an authoritative mapping.
- **Deterministic composite match** — stable combination such as normalized name + address + jurisdiction, subject to validation.
- **Probable match** — algorithmic/fuzzy/embedding evidence above a threshold.
- **Ambiguous** — evidence insufficient to select one entity.
- **No match** — evidence supports distinct entities.
- **Rejected match** — previously proposed mapping invalidated by evidence.

Final representation (phase/quality/enumeration/information object) is deferred to W4/W5.

## 5. Match evidence requirements
Every non-trivial match should retain:
- source record A and B;
- identifiers compared;
- normalized names/addresses where used;
- method/algorithm/version;
- rule/threshold;
- confidence score where applicable;
- reviewer/gold judgment where applicable;
- date/version of decision;
- status and reason for ambiguity/rejection.

## 6. Candidate entity-resolution benchmark design
The W1 AI candidate is promoted only if W6 can curate a defensible overlapping sample.

### Possible benchmark sources
- P3 FDA DECRS ↔ FDA WDD/3PL for organization/site overlap.
- P3/P4 FDA establishment/product-label records where explicit linkage exists.
- P4 openFDA harmonized identifiers across NDC/SPL.
- P1/P2 NHIF product identity overlap through `nhif_code`, ATC/INN and product presentation fields.
- P7 GeoNames for location normalization.
- H1 ClinicalTrials.gov/AACT may be used **only during held-out evaluation**, not to tune W3 identity requirements.

### Required evaluation if activated
- curated gold subset with explicit same/different/ambiguous judgments;
- precision;
- recall;
- F1;
- ambiguity/unresolved rate;
- type-specific performance (Organization vs Site vs Product);
- error analysis by identifier/source/jurisdiction;
- comparison against deterministic baseline before any ML/embedding model.

## 7. Identity anti-patterns to prevent
1. Same string name ⇒ same entity.
2. Same address ⇒ same organization.
3. Facility ⇒ organization.
4. NDC ⇒ abstract medicinal product universally.
5. ATC ⇒ product identity.
6. INN text ⇒ exact substance identity without normalization.
7. License number ⇒ facility identity.
8. Dataset row identifier ⇒ real-world entity identifier.
9. Probabilistic match ⇒ asserted `owl:sameAs` without evidence/boundary.

## 8. Later semantic-web mapping rule
Avoid uncontrolled use of `owl:sameAs`. W5 should define graded/exact mapping relations or SKOS/PROV-compatible patterns appropriate to the evidence. `owl:sameAs` is reserved only for identity claims that truly satisfy indiscernibility expectations at the modeled level.

## Conclusion
Identity reconciliation is not merely ETL plumbing in V2; it is part of the semantic research problem. Explicit identifier schemes, assignments, match assertions and evidence are necessary to support geospatial integration, cross-source provenance, RDB/KG consistency and any later measured entity-resolution AI component.
