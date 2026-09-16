---
artifact_type: horp_relation_review_records
ontology_id: CM-PharmE
ontology_version: 2.0.0-alpha.1
review_candidate: RC-V2-HORP-01
record_count: 35
review_status: pending_author_review
---

# CM-PharmE 2.0 — Formally Constrained Relation Review Records

These 35 records complement `unconstrained-endpoint-review-records.md` and cover every V2 object property whose OWL source currently declares both domain and range. They are review projections only: no relation is approved, repaired, normalized, or semantically changed here. Each record preserves the currently declared direction and asks the author to confirm that the formalized source → relation → target semantics match the intended conceptualization.

Authoritative anchors: `../../research/w4/integrated-ontouml-model.md`, `../../ontology/source/modules/10-core.ttl`, `../../ontology/source/modules/20-xinfra.ttl`, and `../../ontology/source/modules/30-extensions.ttl`.

## Core — 20 records

| ID | Property | Current formalization | Evidence / treatment | HORP review question | Disposition |
|---|---|---|---|---|---|
| CR-01 | `operates` | Organization → Facility | W4: material, derived from Facility Operation | Does the derived material relation preserve the intended operational meaning and direction? | Pending |
| CR-02 | `operationOrganization` | Facility Operation → Organization | W4 relator participant | Is Organization the correct mandatory participant type for this relator projection? | Pending |
| CR-03 | `operationFacility` | Facility Operation → Facility | W4 relator participant | Is Facility the correct participant target and direction? | Pending |
| CR-04 | `registrationAuthority` | Establishment Registration → Organization | W4 authority participant | Does Organization adequately represent the registering authority role? | Pending |
| CR-05 | `registrationJurisdiction` | Establishment Registration → Regulatory Jurisdiction | W4 jurisdiction context | Is jurisdiction contextualization represented at the correct semantic level? | Pending |
| CR-06 | `authorizationAuthority` | Regulatory Authorization → Organization | W4 authority participant | Does Organization adequately represent the authorization authority role? | Pending |
| CR-07 | `authorizationJurisdiction` | Regulatory Authorization → Regulatory Jurisdiction | W4 jurisdiction context | Is the authorization-to-jurisdiction direction and target correct? | Pending |
| CR-08 | `presentationOf` | Medicinal Product Presentation → Medicinal Product | W4 formal relation | Does this distinguish product identity from presentation identity correctly? | Pending |
| CR-09 | `hasDosageForm` | Medicinal Product Presentation → Dosage Form Specification | W4 formal specification | Is dosage form correctly attached at presentation level? | Pending |
| CR-10 | `hasStrength` | Medicinal Product Presentation → Strength | W4 characterization | Is Strength correctly modeled as the presentation characterization target? | Pending |
| CR-11 | `hasPackageConfiguration` | Medicinal Product Presentation → Package Configuration | W4 formal specification | Is package configuration correctly scoped to presentation? | Pending |
| CR-12 | `classificationEntry` | Product Classification Assignment → Classification Entry | W4 relator participant | Is the classification-entry participant direction correct? | Pending |
| CR-13 | `entryInScheme` | Classification Entry → Product Classification Scheme | W4 scheme membership | Does this relation capture scheme membership without conflating assignment? | Pending |
| CR-14 | `listingPresentation` | Market Listing → Medicinal Product Presentation | W4 relator participant | Is presentation the correct listed product granularity? | Pending |
| CR-15 | `listingResponsibleOrganization` | Market Listing → Organization | W4 relator participant | Does Organization adequately capture the responsible-party role? | Pending |
| CR-16 | `listingJurisdiction` | Market Listing → Regulatory Jurisdiction | W4 relator participant/context | Is jurisdiction participation/context modeled correctly? | Pending |
| CR-17 | `shortageProduct` | Medicine Shortage Situation → Medicinal Product | W4 situation involvement | Is product-level shortage involvement intentionally distinct from presentation-level involvement? | Pending |
| CR-18 | `shortagePresentation` | Medicine Shortage Situation → Medicinal Product Presentation | W4 situation involvement | Is presentation-level shortage involvement correctly distinguished from product-level involvement? | Pending |
| CR-19 | `shortageJurisdiction` | Medicine Shortage Situation → Regulatory Jurisdiction | W4 situation context | Is jurisdiction the correct contextual target for shortage situations? | Pending |
| CR-20 | `producesObservationResult` | Observation Activity → Observation Result | W4 event → information | Does the activity-to-result direction capture provenance/production semantics correctly? | Pending |

## Cross-cutting infrastructure — 10 records

| ID | Property | Current formalization | Evidence / treatment | HORP review question | Disposition |
|---|---|---|---|---|---|
| CR-21 | `maintainsDataset` | Data Source → Dataset | X-INFRA stewardship/publication | Does Data Source → Dataset correctly express maintenance/stewardship? | Pending |
| CR-22 | `hasDatasetRelease` | Dataset → Dataset Release | X-INFRA version/release | Is Dataset Release the correct versioned manifestation target? | Pending |
| CR-23 | `containsSourceRecord` | Dataset Release → Source Record | X-INFRA containment | Is record containment correctly scoped to a release rather than the abstract dataset? | Pending |
| CR-24 | `evidenceRecord` | Evidence Support → Source Record | X-INFRA evidence relator participant | Does this participant relation preserve evidence provenance correctly? | Pending |
| CR-25 | `evidenceAssertion` | Evidence Support → Assertion | X-INFRA evidence relator participant | Is Assertion the correct supported-claim target? | Pending |
| CR-26 | `generatedAssertion` | Provenance Activity → Assertion | X-INFRA provenance output | Does this direction correctly represent generated semantic output? | Pending |
| CR-27 | `identifierScheme` | Identifier Assignment → Identifier Scheme | X-INFRA identifier participant | Is scheme participation attached at assignment level correctly? | Pending |
| CR-28 | `hasMatchConfidence` | Entity Match Assertion → Match Confidence | X-INFRA quality attachment | Is confidence modeled at the match-assertion level with the right target? | Pending |
| CR-29 | `withinRegion` | Geographic Feature → Administrative Region | X-INFRA geographic context | Does this relation preserve intended containment/context semantics? | Pending |
| CR-30 | `withinCountry` | Geographic Feature → Country | X-INFRA geographic context | Is country contextualization correctly modeled independently of region? | Pending |

## Extensions — 5 records

| ID | Property | Current formalization | Evidence / treatment | HORP review question | Disposition |
|---|---|---|---|---|---|
| CR-31 | `contextClassificationProduct` | Contextual Medicine Classification Assignment → Medicinal Product | Extension relator participant | Is Medicinal Product the correct classified entity and granularity? | Pending |
| CR-32 | `contextClassificationEntry` | Contextual Medicine Classification Assignment → Classification Entry | Extension relator participant | Is Classification Entry the correct classification target? | Pending |
| CR-33 | `contextClassificationJurisdiction` | Contextual Medicine Classification Assignment → Regulatory Jurisdiction | Extension context participant | Is jurisdiction contextualization explicit at the correct level? | Pending |
| CR-34 | `alternativeProduct` | Alternative Medicinal Product Assignment → Medicinal Product | Extension alternative endpoint | Does the direction identify the proposed alternative unambiguously? | Pending |
| CR-35 | `alternativeForProduct` | Alternative Medicinal Product Assignment → Medicinal Product | Extension reference endpoint | Does the direction identify the reference/original product unambiguously and complement `alternativeProduct`? | Pending |

## Reconciliation

- Formally constrained relation records in this artifact: **35/35**.
- Previously instantiated unconstrained-endpoint records: **17/17**.
- Total V2 object-property relation-review records after this artifact: **52/52**.
- Human semantic dispositions recorded by automation: **0**.
- Every disposition remains **Pending** until author review.

## Next HORP step

With relation-review records instantiated for all 52 object properties, the next autonomous evidence artifact under #173 is the V1→V2 Version Evolution Review Package. Semantic acceptance, endpoint repair, relation renaming, cardinality changes, or release/freeze decisions remain Human Gates.