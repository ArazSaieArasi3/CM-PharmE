# CM-PharmE 2.0 Human Review — Risk-First Queue

Issue: #159  
Scope: CM-PharmE 2.0 only  
Status: active review-support artifact  
V1/main impact: none

## Purpose

This queue narrows the 87-concept human-review matrix to concepts whose current semantics, migration treatment, held-out behavior, or publication claims deserve earlier inspection. It does **not** change Gate-D semantics, add external evidence, or record author/expert approval.

The queue is derived only from the current repository-backed provenance matrix and the governed `G0–G9` gap taxonomy. A row appears here because review consequence is comparatively high, not because the concept is presumed wrong.

## Prioritization contract

Order rows by the first material risk encountered:

1. foundational category/stereotype commitment that cannot be justified by source presence alone;
2. V1→V2 transformation where semantic continuity could be mistaken for label continuity;
3. risk/resilience semantics where scenario evidence must not be upgraded into predictive/operational validation;
4. held-out partial fit that must remain partial;
5. legacy/extension concepts whose V2 admission is mostly lineage-driven.

`claim_impact` uses the controlled values from the provenance gap register: `none`, `wording-only`, `local-semantic`, `cross-domain`, `publication-blocking`.

## Review queue

| Priority | Domain | Concept / IRI | Why early review is justified | Current support | Primary gap | Claim impact | Next evidence/review action | Automatic ontology change? |
|---|---|---|---|---|---|---|---|---|
| P0 | Risk Management | Asset at Risk / `cmpe:AssetAtRisk` | `RoleMixin` adapter imports a generic risk-role commitment into the pharmaceutical model; source presence alone cannot validate the bearer/role semantics. | V1/W1 + R1/M1/M2 | `G8` | cross-domain | Author checks intended bearer range and COVER/ROSE/UFO-grounded role commitment against the current W4 model. | No |
| P0 | Risk Management | Vulnerability / `cmpe:Vulnerability` | `Mode` commitment is foundational and materially affects how risk-bearing entities are modeled. | W1 risk alignment + R1/M1/M2 | `G8` | cross-domain | Author verifies that susceptibility/disposition is the intended commitment and that the bearer relation is explicit enough for publication wording. | No |
| P0 | Risk Management | Risk Treatment Plan / `cmpe:RiskTreatmentPlan` | Separates normative treatment specification from treatment execution; conflation would alter downstream semantics. | W1/V1 + R1/M1/M2 | `G8` | local-semantic | Review Plan-as-information-object versus Activity execution distinction; retain only bounded claims supported by current sources. | No |
| P0 | Risk Management | Risk Treatment Activity / `cmpe:RiskTreatmentActivity` | Event counterpart to Risk Treatment Plan; requires explicit separation of prescribed action and performed occurrence. | W1/V1 + R1/M1/M2 | `G8` | local-semantic | Review event identity and plan↔execution relation; route any semantic change to a design-decision issue. | No |
| P0 | Supply Resilience | Supply Dependency / `cmpe:SupplyDependency` | Refines a broad V1 predecessor and bridges supply semantics with the risk/resilience view. | P5/C1/W1 + O4/R1/M1/M2 | `G8` | cross-domain | Check dependency relata, direction/context, and whether current wording overreaches beyond source-bounded supply dependency. | No |
| P0 | Supply Resilience | Disruption Event / `cmpe:DisruptionEvent` | Event semantics are central to resilience scenarios, but scenario success must not imply predictive/operational resilience validation. | W1/P5/C1 + O1/O4/R1/M1/M2 | `G9` | publication-blocking | Preserve event concept while explicitly bounding manuscript/product claims to representational/scenario use. | No |
| P1 | Evidence Traceability | Evidence Item / `cmpe:EvidenceItem` | `RoleMixin` commitment controls how evidence-bearing information objects participate in research traceability. | research traceability/all sources + M1/M2 | `G5` | cross-domain | Verify role-bearing semantics and bearer class; do not infer empirical validity from the evidence role itself. | No |
| P1 | Evidence Traceability | Evidence Support / `cmpe:EvidenceSupport` | W4 truth-maker for evidence→claim support; weak semantics here can blur provenance with validation. | research traceability/all sources + M1/M2 | `G5` | cross-domain | Review relata/cardinality intent and ensure support never means truth, expert agreement, or causal proof. | No |
| P1 | Entity Identity | Match Confidence / `cmpe:MatchConfidence` | `Quality` commitment is method-driven while domain evidence is indirect; confidence semantics can be mistaken for probability/validation. | entity-resolution design + M1/M2 | `G5` | wording-only | Bound the definition to a quality attached to match assertion; avoid statistical interpretation unless separately evidenced. | No |
| P1 | Supply Resilience | Inventory Observation Result / `cmpe:InventoryObservationResult` | Conditional C1 support only; admission is operationally plausible but narrow. | C1 + M2 | `G4` | local-semantic | Keep observational claim source-bounded; verify C1 admissibility/provenance before stronger domain-necessity wording. | No |
| P1 | Supply Resilience | Procurement Activity / `cmpe:ProcurementActivity` | Split from broad V1 activity and currently grounded primarily in conditional C1 evidence. | C1 + M1/M2 | `G4` | local-semantic | Check whether current scope is justified beyond C1; otherwise retain as bounded extension semantics. | No |
| P1 | Supply Resilience | Lead Time Observation Result / `cmpe:LeadTimeObservationResult` | Conditional C1 support and observation-result modeling are both material. | C1 + M2 | `G4` | local-semantic | Verify source provenance and observation-result treatment; avoid implying generic pharmaceutical universality. | No |
| P1 | Supply Resilience | Stockout Situation / `cmpe:StockoutSituation` | Situation semantics are grounded by conditional C1 plus regulatory shortage framing, but stockout and shortage must not be collapsed. | C1 + P5 framing + O3/O4/M1/M2 | `G8` | local-semantic | Author reviews stockout-versus-shortage boundary and temporal/context conditions. | No |
| P1 | Pharmaceutical Product | Medicinal Product / `cmpe:MedicinalProduct` | Held-out mapping is partial in H1/H3 while H2 is exact; partial fit must remain visible. | P1/P2/P4/P5/P6; H1 partial, H2 exact, H3 partial | `G7` | wording-only | Inspect the exact source-specific mismatch before any coverage/completeness claim; no automatic concept change. | No |
| P1 | Pharmaceutical Product | Pharmaceutical Substance / `cmpe:PharmaceuticalSubstance` | Multiple held-out sources map only partially; product/substance identity boundary is publication-relevant. | P1/P2/P4/P5/P6/S1; H1 partial, H2 exact, H3 partial | `G7` | local-semantic | Review whether partial fit reflects source granularity versus a genuine model gap; preserve mismatch evidence. | No |
| P1 | Pharmaceutical Product | Product Classification Assignment / `cmpe:ProductClassificationAssignment` | H3 is partial; classification assignment contextuality could be lost in simplified claims. | P1/P2/P4/P5; H2 exact, H3 partial + O4/O5/M1/M2 | `G7` | wording-only | Inspect H3 mismatch and retain source/list/version context in claims. | No |
| P2 | Business Architecture | Enterprise Capability / `cmpe:EnterpriseCapability` | Retained in an optional extension largely from V1 lineage; domain necessity is not independently strong in the current matrix. | V1 + PR1/M1/M2 | `G6` | local-semantic | Treat as legacy/optional extension unless independent V2 use/evidence is established; no Core claim. | No |
| P2 | Digital Systems | Digital System Component / `cmpe:DigitalInformationSystemComponent` | Generalizes/deprecates several technology-specific V1 forms; migration traceability matters more than label similarity. | V1 lineage + PR1/M2 | `G6` | local-semantic | Review predecessor coverage and confirm generic extension role; do not imply that all deprecated V1 technologies are semantically equivalent. | No |
| P2 | Clinical Care | Clinical Care Participant / `cmpe:ClinicalCareParticipant` | Consolidates four V1 concepts; admission is V1-driven and held-out H1 shows extension pressure rather than exact validation. | V1 only at admission; H1 extension pressure + PR1/M1/M2 | `G6` | local-semantic | Author reviews whether consolidation preserves required role distinctions; treat H1 as pressure/evidence lead, not approval. | No |

## Queue metrics

- Frozen risk-first queue size: **19 concepts**.
- P0: **6** concepts — highest semantic/claim consequence.
- P1: **10** concepts — material evidence/foundational/held-out review.
- P2: **3** concepts — legacy/extension migration review.
- Queue completion means **human disposition recorded for all 19 rows**, not that #159 or CM-PharmE V2 is scientifically validated.

## Reviewer recording template

For each reviewed queue row, append a review record in the #159 review log or a dedicated companion artifact:

```text
concept:
reviewer_or_author:
date:
primary_gap:
disposition: APPROVE | APPROVE WITH WORDING CHANGE | REVISE SEMANTICS | SPLIT/MERGE | MOVE DOMAIN/MODULE | DEFER
claim_boundary:
resolution_evidence:
follow_up_issue:
```

Do not populate `reviewer_or_author`, disposition, or resolution evidence until an actual review occurs.

## Exit from the risk-first queue

A row leaves this queue only when one of the following is traceably recorded:

1. author/reviewer disposition with no semantic change required;
2. wording/claim boundary is explicitly bounded and linked to evidence;
3. a semantic change is routed to a separate design-decision issue;
4. the row is explicitly deferred with rationale.

The remaining 68 matrix concepts still require domain-by-domain author review. Absence from this queue means lower first-pass risk, not automatic approval.
