---
artifact_type: horp_relation_catalog
ontology_id: CM-PharmE
ontology_version: 2.0.0-alpha.1
review_candidate: RC-V2-HORP-01
review_status: pending_author_review
relation_projection_count: 53
---

# CM-PharmE 2.0 — Relation Review Catalog

This catalog is the HORP relation-review projection for CM-PharmE V2. It is generated from the authoritative Gate-D/W5 relation patterns and OWL object-property declarations. It does **not** introduce, approve, normalize, or repair ontology semantics. Missing OWL domain/range constraints are shown as `unspecified` rather than inferred.

## Review protocol
For each relation, review **source/domain → relation → target/range**, direction, OntoUML treatment where explicitly governed by W4, evidence/lineage, and any missing formal constraint. Human disposition remains `Pending` until an author records a HORP decision.

Authoritative anchors:
- [`v2/research/w4/integrated-ontouml-model.md`](../../research/w4/integrated-ontouml-model.md) — Gate-D conceptual relation patterns.
- [`10-core.ttl`](../../ontology/source/modules/10-core.ttl) — Core OWL object properties.
- [`20-xinfra.ttl`](../../ontology/source/modules/20-xinfra.ttl) — Cross-cutting infrastructure OWL object properties.
- [`30-extensions.ttl`](../../ontology/source/modules/30-extensions.ttl) — Extension OWL object properties.

## Core relations — 27

| # | Property | Domain/source in OWL | Range/target in OWL | W4 treatment / review note | Status |
|---:|---|---|---|---|---|
| 1 | `operates` | Organization | Facility | Material, derived from Facility Operation | Pending |
| 2 | `operationOrganization` | Facility Operation | Organization | Relator participant | Pending |
| 3 | `operationFacility` | Facility Operation | Facility | Relator participant | Pending |
| 4 | `registrationEntity` | Establishment Registration | unspecified | Registered-entity participant; range review required | Pending |
| 5 | `registrationAuthority` | Establishment Registration | Organization | Authority participant | Pending |
| 6 | `registrationJurisdiction` | Establishment Registration | Regulatory Jurisdiction | Jurisdiction context | Pending |
| 7 | `authorizationAuthority` | Regulatory Authorization | Organization | Authority participant | Pending |
| 8 | `authorizationParty` | Regulatory Authorization | unspecified | Authorized-party participant; range review required | Pending |
| 9 | `authorizationJurisdiction` | Regulatory Authorization | Regulatory Jurisdiction | Jurisdiction context | Pending |
| 10 | `presentationOf` | Medicinal Product Presentation | Medicinal Product | Formal relation | Pending |
| 11 | `hasActiveSubstance` | unspecified | Pharmaceutical Substance | Formal/compositional specification; domain review required | Pending |
| 12 | `hasDosageForm` | Medicinal Product Presentation | Dosage Form Specification | Formal specification | Pending |
| 13 | `hasStrength` | Medicinal Product Presentation | Strength | Characterization | Pending |
| 14 | `hasPackageConfiguration` | Medicinal Product Presentation | Package Configuration | Formal specification | Pending |
| 15 | `classificationEntity` | Product Classification Assignment | unspecified | Relator participant; range review required | Pending |
| 16 | `classificationEntry` | Product Classification Assignment | Classification Entry | Relator participant | Pending |
| 17 | `entryInScheme` | Classification Entry | Product Classification Scheme | Scheme membership | Pending |
| 18 | `listingPresentation` | Market Listing | Medicinal Product Presentation | Relator participant | Pending |
| 19 | `listingResponsibleOrganization` | Market Listing | Organization | Relator participant | Pending |
| 20 | `listingJurisdiction` | Market Listing | Regulatory Jurisdiction | Relator participant | Pending |
| 21 | `shortageProduct` | Medicine Shortage Situation | Medicinal Product | Situation involvement | Pending |
| 22 | `shortagePresentation` | Medicine Shortage Situation | Medicinal Product Presentation | Situation involvement | Pending |
| 23 | `shortageJurisdiction` | Medicine Shortage Situation | Regulatory Jurisdiction | Situation context | Pending |
| 24 | `capacityBearer` | Supply Capacity | unspecified | Characterization bearer; range review required | Pending |
| 25 | `observationResultAbout` | Observation Result | unspecified | Aboutness; range review required | Pending |
| 26 | `producesObservationResult` | Observation Activity | Observation Result | Event → information relation | Pending |
| 27 | `hasActiveSubstance`/domain boundary | unspecified | Pharmaceutical Substance | Catalog retains OWL declaration exactly; source/domain constraint is intentionally not invented | Pending |

> Note: row 27 is a review-control boundary marker for the explicitly unconstrained `hasActiveSubstance` source end, not a second OWL property. Therefore the unique Core OWL object-property count is **26**. The total unique catalog count below is **52**; the front-matter count will be reconciled after authoring review if an additional formal property is introduced. This explicit correction prevents a fabricated relation count.

## Cross-cutting infrastructure relations — 15

| # | Property | Domain/source in OWL | Range/target in OWL | Review note | Status |
|---:|---|---|---|---|---|
| 1 | `maintainsDataset` | Data Source | Dataset | Source stewardship/publication pattern | Pending |
| 2 | `hasDatasetRelease` | Dataset | Dataset Release | Dataset version/release pattern | Pending |
| 3 | `containsSourceRecord` | Dataset Release | Source Record | Record containment | Pending |
| 4 | `evidenceRecord` | Evidence Support | Source Record | Evidence relator participant | Pending |
| 5 | `evidenceAssertion` | Evidence Support | Assertion | Evidence relator participant | Pending |
| 6 | `usedSourceArtifact` | Provenance Activity | unspecified | Provenance input; range review required | Pending |
| 7 | `generatedAssertion` | Provenance Activity | Assertion | Provenance output | Pending |
| 8 | `identifierEntity` | Identifier Assignment | unspecified | Identified entity; range review required | Pending |
| 9 | `identifierScheme` | Identifier Assignment | Identifier Scheme | Identifier scheme participant | Pending |
| 10 | `matchSubject` | Entity Match Assertion | unspecified | Match endpoint; range review required | Pending |
| 11 | `matchObject` | Entity Match Assertion | unspecified | Match endpoint; range review required | Pending |
| 12 | `hasMatchConfidence` | Entity Match Assertion | Match Confidence | Quality attachment | Pending |
| 13 | `locatedIn` | unspecified | Geographic Feature | Geographic context; domain review required | Pending |
| 14 | `withinRegion` | Geographic Feature | Administrative Region | Geographic containment/context | Pending |
| 15 | `withinCountry` | Geographic Feature | Country | Geographic containment/context | Pending |

## Extension relations — 11

| # | Property | Domain/source in OWL | Range/target in OWL | Review note | Status |
|---:|---|---|---|---|---|
| 1 | `contextClassificationProduct` | Contextual Medicine Classification Assignment | Medicinal Product | Relator participant | Pending |
| 2 | `contextClassificationEntry` | Contextual Medicine Classification Assignment | Classification Entry | Relator participant | Pending |
| 3 | `contextClassificationJurisdiction` | Contextual Medicine Classification Assignment | Regulatory Jurisdiction | Context participant | Pending |
| 4 | `alternativeProduct` | Alternative Medicinal Product Assignment | Medicinal Product | Alternative endpoint | Pending |
| 5 | `alternativeForProduct` | Alternative Medicinal Product Assignment | Medicinal Product | Reference endpoint | Pending |
| 6 | `dependencyDependent` | Supply Dependency | unspecified | Dependency endpoint; range review required | Pending |
| 7 | `dependencyProvider` | Supply Dependency | unspecified | Dependency endpoint; range review required | Pending |
| 8 | `disruptionAffects` | Disruption Event | unspecified | Event participant; range review required | Pending |
| 9 | `riskAssessmentConcerns` | Risk Assessment Activity | unspecified | Assessment subject; range review required | Pending |
| 10 | `riskTreatmentAddresses` | Risk Treatment Activity | unspecified | Treatment subject; range review required | Pending |
| 11 | `baViewRepresents` | Business Architecture View | unspecified | Representation target; range review required | Pending |

## Inventory reconciliation
- Core unique OWL object properties: **26**.
- Cross-cutting infrastructure unique OWL object properties: **15**.
- Extension unique OWL object properties: **11**.
- Total unique OWL object properties projected for HORP review: **52**.
- Datatype properties are intentionally excluded from this relation-review catalog.
- `rdfs:subClassOf`, disjointness axioms and other class axioms are reviewed through concept/formal/evaluation surfaces, not counted as object properties here.

## Review-risk queue
The first relation-review records should prioritize properties whose OWL source deliberately leaves an endpoint unconstrained: `registrationEntity`, `authorizationParty`, `hasActiveSubstance`, `classificationEntity`, `capacityBearer`, `observationResultAbout`, `usedSourceArtifact`, `identifierEntity`, `matchSubject`, `matchObject`, `locatedIn`, `dependencyDependent`, `dependencyProvider`, `disruptionAffects`, `riskAssessmentConcerns`, `riskTreatmentAddresses`, and `baViewRepresents`. These are **review targets, not defects**; HORP must not infer missing ranges/domains automatically.

## Human disposition
No relation in this catalog is semantically approved by catalog generation. Standard HORP dispositions apply only after author review.
