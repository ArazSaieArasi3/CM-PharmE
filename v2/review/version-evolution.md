---
artifact_type: version_evolution_review_package
ontology_id: CM-PharmE
from_version: 1.x
review_candidate: RC-V2-HORP-01
review_status: pending_human_review
issue: 173
---

# CM-PharmE 1.x → 2.0 — Version Evolution Review Package

## Purpose
This HORP review projection makes continuity, refinement, modularization, deprecation and novelty between the reviewer-facing CM-PharmE 1.x baseline and the V2 review candidate explicit. It does **not** change either ontology and does not convert migration evidence into semantic approval.

## Authoritative evidence anchors
- V1 concept registry: [`../../catalog/concepts.yaml`](../../catalog/concepts.yaml)
- V1 concept documentation: [`../../docs/concepts/`](../../docs/concepts/)
- W0 novelty/migration policy: [`../research/v1-v2-novelty-migration-matrix.md`](../research/v1-v2-novelty-migration-matrix.md)
- W3 concept-by-concept migration matrix: [`../research/w3/v1-v2-migration-matrix.md`](../research/w3/v1-v2-migration-matrix.md)
- W4 concept provenance/V1-lineage matrix: [`../research/w4/human-review-concept-provenance-matrix.md`](../research/w4/human-review-concept-provenance-matrix.md)
- W3→W4 transformation ledger: [`../research/w4/w3-w4-transformation-ledger.md`](../research/w4/w3-w4-transformation-ledger.md)
- Final conceptual specification: [`../research/w4/integrated-ontouml-model.md`](../research/w4/integrated-ontouml-model.md)
- Concept Evidence Passports: [`concepts/passports/index.md`](concepts/passports/index.md)
- V2 Relation Catalog: [`relations/index.md`](relations/index.md)
- HORP relation-review records: [`relations/review-records.md`](relations/review-records.md)

## Evolution status vocabulary
The review uses the governed migration meanings already established in the V2 research stream: **Retain/Refine, Split, Move to Extension, Defer, Deprecate Generic/Technology-specific Form**, plus explicit V2-new normalized distinctions where no V1 concept should be claimed as the source of novelty.

## Concept evolution summary
The W3 migration matrix accounts for all **39 V1 concepts**. Its summary records:

| Evolution outcome | W3 evidence summary | HORP interpretation |
|---|---:|---|
| Retain/refine into Core or cross-cutting V2 semantics | 15 V1 concepts materially contribute | Continuity exists, but the V2 definition/stereotype/structure must still be reviewed on its own evidence. |
| Move to modular extensions | 18 V1 concepts | Useful predecessor semantics are preserved outside the principal Core where evidence/scope warrants. |
| Defer/deprecate generic or technology-specific form | 6 V1 concepts | V1 identity is not automatically carried into V2; rationale must remain visible. |
| New normalized V2 candidates | substantial | Novelty is concentrated especially in product, site, geography/jurisdiction, shortage/observation, evidence/provenance and identifier layers. |

These W3 counts are migration-decision counts, **not** final W4 class counts. The final V2 review surface contains 87 concepts and must be reviewed through the provenance matrix/passports rather than by treating the W3 candidate inventory as the final ontology.

## Material architectural evolution requiring author attention

| V1 concern | V2 treatment | Review question | Human disposition |
|---|---|---|---|
| Five-domain architecture | Refined; not inherited as fixed V2 Core decomposition | Is the evidence-emergent 17-domain V2 review structure preferable to preserving the five-domain decomposition? | Pending |
| Business-architecture-informed identity | Moved to optional extension/view | Is BA correctly retained as an analytical view rather than ontology Core identity? | Pending |
| UFO grounding | Retained and strengthened | Are the V2 foundational commitments and stereotypes justified concept-by-concept? | Pending |
| OntoUML model | Retained and strengthened | Does the integrated OntoUML model preserve justified continuity while correcting V1 modeling weaknesses? | Pending |
| OWL implementation | Retained and strengthened | Does the V2 OWL formalization correctly realize the reviewed conceptual commitments? | Pending |
| Scenario-only data evidence | Replaced by data-grounded evidence | Is the stronger prospective dataset/evidence strategy sufficient for the distinctions introduced? | Pending |
| Repository-supported evaluation | Retained and expanded | Do E1–E13 adequately cover the claims and new V2 representations? | Pending |
| Risk Management Activity | Moved/refined into Risk & Resilience extension | Is generic risk semantics correctly modularized/aligned rather than duplicated in Core? | Pending |
| Reference-architecture applications | Retained as optional application view | Is application value sufficiently separated from Core ontological commitments? | Pending |

## High-value concept migration decisions
The complete 39-row source is the W3 matrix; the following cases are the most consequential semantic transformations for review.

| V1 concept/family | V2 evolution | Why it matters |
|---|---|---|
| Pharmaceutical Enterprise | Refine → `Organization` + contextual pharmaceutical roles | Removes enterprise/BA identity from Core while retaining ecosystem organizations. |
| Organizational Stakeholder / Ecosystem Actor | Refine/Split → contextual participant roles | Replaces actor-as-universal-kind assumptions with role-bearing semantics. |
| Regulatory Oversight | Refine → authority role, jurisdiction, authorization/license and typed oversight | Makes regulatory semantics explicit rather than one broad relator. |
| Ecosystem Relationship | Split/deprecate generic form → typed relations | Eliminates a catch-all relationship in favor of evidence-backed semantics. |
| Ecosystem Demand Signal / Supply Capacity | Refine → time/context-bounded observations | Separates observed evidence from intrinsic/dispositional claims. |
| Medicinal-product layer | New normalized distinctions | Introduces Product–Substance–Presentation–Form–Strength–Package structure absent from V1's coarse model. |
| Supply Chain Relationship | Split/deprecate generic form | Replaces generic supply relation with typed participation/dependency/availability/shortage semantics. |
| Patient Record Quality | Generalize → `Data Quality Finding` | Moves quality semantics to reusable cross-cutting infrastructure. |
| Real-World Evidence Platform | Generalize/move → data/evidence/provenance layer | Replaces platform-specific ontology identity with durable evidence semantics. |
| Digital/AI/blockchain-specific constructs | Move/defer/deprecate technology-specific Core forms | Prevents implementation technology from becoming durable Core ontology semantics without evidence. |

## Relation evolution
V1 contains **39 object properties plus one explicit generalization record**. V2 does not preserve relation identity merely because a V1 property exists. The W3 policy migrates relations by semantic family: enterprise/BA relations move to the BA extension; generic actor/relationship relations become role-bearing or typed relations; clinical relations move to the Clinical extension; governance relations are refined; business-process and supply-chain relations are split into typed activity/participation/dependency patterns; digital relations move to application extensions; safety/PV and risk relations move to their extensions.

The current V2 formal review surface contains **52 OWL object properties**, each now represented in the Relation Catalog and HORP relation-review records. Relation continuity therefore requires semantic review, not numeric one-to-one mapping. Where a direct V1 predecessor exists, `replaces/refines` lineage should be verified against the W3/W4 evidence; absence of a predecessor must not be treated as an error when the V2 distinction is evidence-driven.

## V2 novelty that must not be misreported as retained V1 content
The W3 migration analysis identifies these material V2 advances:
1. Organization vs contextual role vs physical Site/Facility.
2. Medicinal Product–Substance–Presentation–Form–Strength–Package structure.
3. Jurisdiction–Geography–Time semantics.
4. Contextual Critical/Essential Medicine classification.
5. Time/source-bounded Shortage, Availability, Demand and Supply observations.
6. Dataset–Record–Assertion–Mapping–Provenance infrastructure.
7. Identifier Scheme/Assignment/Entity Match semantics.
8. Business Architecture demoted from Core identity to optional view.
9. Typed supply/resilience relations replacing generic Supply Chain Relationship.
10. Prospective held-out evaluation design preceding W3 concept discovery.

## Human review checklist
For each material evolution decision, the author should determine whether:
- the V1 semantic intent has been represented accurately;
- retained semantics are not falsely presented as V2 novelty;
- refinement/split/generalization has adequate evidence and UFO/OntoUML justification;
- moved/deferred/deprecated constructs have an explicit scope rationale;
- new V2 distinctions have independent evidence rather than merely new names;
- concept and relation lineage is consistent across the migration matrix, provenance matrix, passports and formal model;
- no semantic approval is inferred from repository presence alone.

## Disposition
**Overall Version Evolution Review: Pending author review.**

This package is complete as a review surface when all evidence anchors remain resolvable and the 39 V1 concepts plus V1 relation families are accounted for. Any accepted semantic finding must enter the structured HRF/re-review workflow before changing the V2 semantic baseline.
