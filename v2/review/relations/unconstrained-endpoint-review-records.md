---
artifact_type: horp_relation_review_records
ontology_id: CM-PharmE
ontology_version: 2.0.0-alpha.1
review_candidate: RC-V2-HORP-01
record_count: 17
review_status: pending_author_review
---

# HORP Relation Review Records — Formally Unconstrained Endpoints

These 17 records instantiate the first bounded relation-review batch from the Relation Catalog risk queue. They are review projections only: an OWL endpoint shown as `unspecified` is **not** treated as a defect and no missing semantic constraint is inferred. Human disposition remains `Pending`.

Each record follows the HORP relation-review sequence: inspect source/domain → relation → target/range, direction, current formalization, evidence anchor, review question, and human disposition.

## RR-001 — `registrationEntity`
- Module: Core
- Current OWL: `Establishment Registration → registrationEntity → unspecified`
- Current treatment: registered-entity participant of the Establishment Registration relator.
- Evidence anchor: `v2/research/w4/integrated-ontouml-model.md`; `v2/ontology/source/modules/10-core.ttl`.
- Review question: Should the participant range remain intentionally open, or should V2 constrain the class of registrable entities?
- Formalization flag: range unspecified.
- Human disposition: **Pending**.

## RR-002 — `authorizationParty`
- Module: Core
- Current OWL: `Regulatory Authorization → authorizationParty → unspecified`
- Current treatment: authorized-party participant.
- Evidence anchor: W4 integrated OntoUML model; `10-core.ttl`.
- Review question: Is the authorized-party role intentionally polymorphic, or is an explicit range justified by the conceptual model/evidence?
- Formalization flag: range unspecified.
- Human disposition: **Pending**.

## RR-003 — `hasActiveSubstance`
- Module: Core
- Current OWL: `unspecified → hasActiveSubstance → Pharmaceutical Substance`
- Current treatment: formal/compositional specification.
- Evidence anchor: W4 integrated OntoUML model; `10-core.ttl`.
- Review question: Which V2 bearer(s), if any, should formally own the active-substance relation?
- Formalization flag: domain unspecified.
- Human disposition: **Pending**.

## RR-004 — `classificationEntity`
- Module: Core
- Current OWL: `Product Classification Assignment → classificationEntity → unspecified`
- Current treatment: classified-entity participant of the assignment relator.
- Evidence anchor: W4 integrated OntoUML model; `10-core.ttl`.
- Review question: Should the classified endpoint remain generic or be constrained to a governed product/entity superclass?
- Formalization flag: range unspecified.
- Human disposition: **Pending**.

## RR-005 — `capacityBearer`
- Module: Core
- Current OWL: `Supply Capacity → capacityBearer → unspecified`
- Current treatment: characterization bearer.
- Evidence anchor: W4 integrated OntoUML model; `10-core.ttl`.
- Review question: What kinds of entities can bear Supply Capacity, and is that set stable enough for an OWL range constraint?
- Formalization flag: range unspecified.
- Human disposition: **Pending**.

## RR-006 — `observationResultAbout`
- Module: Core
- Current OWL: `Observation Result → observationResultAbout → unspecified`
- Current treatment: aboutness relation.
- Evidence anchor: W4 integrated OntoUML model; `10-core.ttl`.
- Review question: Is open-ended aboutness intentional across observation types, or should the target be constrained?
- Formalization flag: range unspecified.
- Human disposition: **Pending**.

## RR-007 — `usedSourceArtifact`
- Module: Cross-cutting infrastructure
- Current OWL: `Provenance Activity → usedSourceArtifact → unspecified`
- Current treatment: provenance input.
- Evidence anchor: `v2/ontology/source/modules/20-xinfra.ttl`.
- Review question: Which source-artifact abstraction should govern provenance inputs without excluding legitimate evidence forms?
- Formalization flag: range unspecified.
- Human disposition: **Pending**.

## RR-008 — `identifierEntity`
- Module: Cross-cutting infrastructure
- Current OWL: `Identifier Assignment → identifierEntity → unspecified`
- Current treatment: identified-entity participant.
- Evidence anchor: `20-xinfra.ttl`.
- Review question: Is intentionally generic entity identification required, or can a stable V2 range be stated?
- Formalization flag: range unspecified.
- Human disposition: **Pending**.

## RR-009 — `matchSubject`
- Module: Cross-cutting infrastructure
- Current OWL: `Entity Match Assertion → matchSubject → unspecified`
- Current treatment: match endpoint.
- Evidence anchor: `20-xinfra.ttl`.
- Review question: Should matching remain entity-agnostic, and if not, what common endpoint type is evidence-supported?
- Formalization flag: range unspecified.
- Human disposition: **Pending**.

## RR-010 — `matchObject`
- Module: Cross-cutting infrastructure
- Current OWL: `Entity Match Assertion → matchObject → unspecified`
- Current treatment: match endpoint.
- Evidence anchor: `20-xinfra.ttl`.
- Review question: Should this endpoint share exactly the same admissible type policy as `matchSubject`?
- Formalization flag: range unspecified.
- Human disposition: **Pending**.

## RR-011 — `locatedIn`
- Module: Cross-cutting infrastructure
- Current OWL: `unspecified → locatedIn → Geographic Feature`
- Current treatment: geographic context.
- Evidence anchor: `20-xinfra.ttl`.
- Review question: Which V2 entities are legitimately locatable, and would a domain constraint improve precision without overcommitment?
- Formalization flag: domain unspecified.
- Human disposition: **Pending**.

## RR-012 — `dependencyDependent`
- Module: Extensions
- Current OWL: `Supply Dependency → dependencyDependent → unspecified`
- Current treatment: dependency endpoint.
- Evidence anchor: `v2/ontology/source/modules/30-extensions.ttl`.
- Review question: What entity types can occupy the dependent endpoint of Supply Dependency?
- Formalization flag: range unspecified.
- Human disposition: **Pending**.

## RR-013 — `dependencyProvider`
- Module: Extensions
- Current OWL: `Supply Dependency → dependencyProvider → unspecified`
- Current treatment: dependency endpoint.
- Evidence anchor: `30-extensions.ttl`.
- Review question: What entity types can occupy the provider endpoint, and should provider/dependent use a shared abstraction?
- Formalization flag: range unspecified.
- Human disposition: **Pending**.

## RR-014 — `disruptionAffects`
- Module: Extensions
- Current OWL: `Disruption Event → disruptionAffects → unspecified`
- Current treatment: event participant/affected endpoint.
- Evidence anchor: `30-extensions.ttl`.
- Review question: Which supply-system entities may be affected by a Disruption Event, and is a common range justified?
- Formalization flag: range unspecified.
- Human disposition: **Pending**.

## RR-015 — `riskAssessmentConcerns`
- Module: Extensions
- Current OWL: `Risk Assessment Activity → riskAssessmentConcerns → unspecified`
- Current treatment: assessment subject.
- Evidence anchor: `30-extensions.ttl`.
- Review question: Should the assessment subject be constrained to Asset at Risk or remain broader?
- Formalization flag: range unspecified.
- Human disposition: **Pending**.

## RR-016 — `riskTreatmentAddresses`
- Module: Extensions
- Current OWL: `Risk Treatment Activity → riskTreatmentAddresses → unspecified`
- Current treatment: treatment subject.
- Evidence anchor: `30-extensions.ttl`.
- Review question: Does treatment address an assessed risk, vulnerability, asset, plan target, or a deliberately broader subject?
- Formalization flag: range unspecified.
- Human disposition: **Pending**.

## RR-017 — `baViewRepresents`
- Module: Extensions
- Current OWL: `Business Architecture View → baViewRepresents → unspecified`
- Current treatment: representation target.
- Evidence anchor: `30-extensions.ttl`.
- Review question: Which business-architecture elements may be represented, and is an explicit common target abstraction warranted?
- Formalization flag: range unspecified.
- Human disposition: **Pending**.

## Batch reconciliation
- Records instantiated: **17/17** catalog risk-queue properties.
- Semantic changes introduced: **0**.
- Formal constraints added/removed: **0**.
- Human dispositions inferred: **0**.
- Next step: author/HORP inspection may disposition individual records; any semantic revision must follow finding → issue → impact analysis → implementation → retest → re-review.
