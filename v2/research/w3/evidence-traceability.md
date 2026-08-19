# W3 Evidence-to-Concept and Evidence-to-Relation Traceability

## Purpose
Provide an auditable record of why each concept/relation family appears in the W3 inventory and identify where evidence is convergent, conditional, V1-only, or deliberately excluded because it is held-out.

## 1. Source-role codes
- **V1** — frozen CM-PharmE 1.x lineage; continuity evidence, not independent empirical evidence.
- **P1/P2** — DOI-backed NHIF empirical anchors.
- **P3** — FDA DECRS + WDD/3PL.
- **P4** — openFDA NDC + FDA/openFDA SPL.
- **P5** — EMA Critical Medicines + EMA shortages/ESMP evidence.
- **P6** — WHO Model List/eEML.
- **P7** — GeoNames normalization only.
- **C1** — conditional supply-operations DOI dataset.
- **C2** — EudraGMDP public semantic evidence; ingestion conditional.
- **S1/S2/S3** — approved enrichment/extension sources.
- **H1/H2/H3** — protected held-out; **not W3 admission evidence**.

## 2. Candidate-family traceability
| Candidate family | Main candidates | Discovery support | Strength | W3 decision |
|---|---|---|---|---|
| Organization and contextual actor roles | V2C-001–009 | P3, P4, P5, C2, P2, V1 | Strong multi-source convergence | Core generic Organization/roles; payer remains extension |
| Physical site/facility | V2C-010–012 | P2, P3, C2 | Strong multi-jurisdiction/source convergence | Core; major V2 distinction |
| Registration, authorization and oversight | V2C-013–016 | P3, C2, P5, V1 | Strong regulatory evidence | Registration/authorization Core; requirements/oversight regulatory extension |
| Jurisdiction and geography | V2C-017–024 | P1, P2, P3, P5, P6; P7 normalization | Strong cross-source need | Jurisdiction Core; geography/time cross-cutting infrastructure |
| Medicinal product/substance/presentation | V2C-025–032 | P1, P2, P4, P5, P6, S1 | Very strong convergence | Core |
| Essential/critical/alternative classifications | V2C-033–035 | P5, P6 | Two authoritative international/regulatory families | Policy/resilience extension; contextual, not intrinsic kinds |
| Manufacturing/distribution activities | V2C-036–037 | P3, C2, V1 | Strong actor/site activity evidence | Core |
| Supply dependency | V2C-038 | P5 vulnerability framing + C1 operations + W1 need | Useful but relationship data incomplete | Resilience extension; bounded |
| Shortage case/status | V2C-039–040 | P5 authoritative data; H2 intentionally excluded | Strong EU discovery evidence | Core shortage semantics; later U.S. held-out test |
| Availability/demand/supply observations | V2C-041–043 | P5/ESMP, C1, P1/P2 aggregate signals | Multi-source but observation types vary | Core observation families; W4 resolves ontology pattern |
| Disruption/inventory/procurement/lead-time/stockout | V2C-044–048 | C1 + W1/P5 need framing | Mostly conditional single operational source for detailed structure | Extension; no global-completeness claim |
| Dataset/provenance/assertion infrastructure | V2C-049–059 | All sources + demonstrator C | Cross-cutting methodological necessity | X-INFRA |
| Identifier/entity-resolution infrastructure | V2C-060–064 | P1–P7/C2/S1 + W1 identity need | Strong multi-source need | X-INFRA |
| Reimbursement/utilisation/diagnosis | V2C-065–066 | P1/P2/S2 | Strong empirical but institutionally concentrated | Market Access extension |
| Risk/vulnerability/treatment | V2C-067–069 | V1 + W1 risk methodology | Methodological/reference evidence, not empirical Core data | Risk extension; align later |
| Pharmacovigilance | V2C-070–072 | V1 + optional S3 | Valid modular domain but not Gate B Core need | Safety extension |
| Business Architecture | V2C-073–075,079–080 | V1 + W1 opportunities | Prior-work continuity; weak data-driven Core need | Optional BA/partnership extension |
| Digital/application systems | V2C-076 | V1 | Technology/application layer | Extension, not Core |
| Clinical-care semantics | V2C-077–078 | V1 only in W3; H1 protected | Insufficient principal-Core evidence | Extension/defer; H1 later tests generic Core generalizability |

## 3. Relation-family traceability
| Relation family | Candidate relation IDs | Main support | W3 confidence |
|---|---|---|---|
| Role bearing / actor roles | R001–R006 | P3/P4/P5/C2/V1 | High |
| Authorization / registration / oversight | R007–R012 | P3/C2/P5/V1 | High; exact relator splits W4 |
| Product composition/presentation/classification | R013–R023 | P1/P2/P4/P5/P6 | Very high |
| Activity participation | R024–R027 | P3/C2; C1 conditional for product logistics detail | High for generic participation; bounded for product-level network claims |
| Supply/dependency/resilience | R028–R036 | P5/C1/W1 | Medium; extension and conditional boundaries required |
| Shortage/observation | R037–R048 | P5/C1/P1/P2 | High for shortage/product/time; medium for supply-capacity detail |
| Geospatial/jurisdiction | R049–R055 | P1/P2/P3/P5/P6/P7 | High |
| Provenance/mapping/identifier | R056–R070 | all source families + demonstrator C | High methodological necessity |
| Market access | R071–R072 | P1/P2/S2 | High within extension |
| Risk/safety/BA/application | R073–R080 | V1/W1/S3 conditional | Extension-only |

## 4. Single-source / conditional dependencies requiring caution
The following candidates must not be presented as globally validated Core semantics solely from W3:
- Procurement Activity — detailed evidence mainly C1.
- Lead-Time Observation — C1.
- Inventory Observation — C1.
- Stockout Event — C1 plus general shortage framing.
- Detailed supplier/product procurement relations — C1 and limited regulatory semantics; no complete global public graph.
- Financing/Counterparty concepts — insufficient evidence; not admitted to Core.
- Detailed clinical-trial roles — H1 is protected and therefore not W3 admission evidence.
- U.S.-specific shortage fields — H2 protected.
- National-list-specific essentiality structures — H3 protected.

## 5. Held-out contamination audit
| Held-out family | W3 allowed knowledge | W3 prohibited use | Audit status |
|---|---|---|---|
| H1 ClinicalTrials.gov/AACT | Existence, access feasibility, high-level purpose documented in W2 | Mining tables/fields to admit Core sponsor/trial/facility/intervention concepts | **Protected** |
| H2 openFDA Drug Shortages | Existence/access feasibility documented in W2 | Mining U.S. shortage fields to design W3 shortage Core | **Protected** |
| H3 selected WHO national EMLs | Repository existence and future selection plan | Mining selected list structure to expand W3 Core | **Protected** |

## 6. Core admission evidence rule applied
A candidate is eligible for Core when at least one of the following holds:
1. convergent evidence across multiple admitted primary/authoritative sources plus demonstrator/RQ relevance; or
2. one authoritative source provides a fundamental domain distinction and V1/use-case evidence independently supports the need; or
3. it is necessary cross-domain ontology infrastructure (e.g., Jurisdiction) whose absence would force repeated source-specific constructs.

Candidates based mainly on one conditional dataset, V1-only technology/application content, or generic future opportunities are routed to extensions/deferred status.

## 7. Traceability result
All **80** normalized W3 concept candidates and all **80** candidate relationship semantics are covered by an identified evidence family, V1 lineage or an explicit extension rationale. Protected held-out sources are not used as concept/relation admission evidence.

This traceability is sufficient for the Concept Inventory Gate, but it is **not** equivalent to empirical ontology validation. W4–W7 must still establish foundational semantics, formalization quality, mapping performance, held-out coverage and application results.
