# CM-PharmE 2.0 Human Review — Provenance Gap Register

Issue: #159  
Scope: CM-PharmE 2.0 only  
Status: active review-support artifact  
V1/main impact: none

## Purpose

This register complements `human-review-concept-provenance-matrix.md`. It does **not** add evidence by assumption. It makes missing or weak concept-level support visible so the author/reviewer can distinguish:

1. evidence already admitted by the V2 research program;
2. methodological support for the modeling treatment;
3. held-out/generalizability evidence;
4. external ontology/literature support that is still unmapped or absent;
5. claims that must therefore remain bounded.

A blank or weak literature/ontology cell is a traceability gap, not proof that a concept is invalid. Conversely, presence in a dataset or official system is not proof that the current ontological interpretation is correct.

## Governed evidence sources already available

| Evidence family | Canonical repository source | What it can support | What it cannot support by itself |
|---|---|---|---|
| V1 lineage | `catalog/concepts.yaml`, `docs/concepts/`, `v2/research/w3/v1-v2-migration-matrix.md` | predecessor identity and migration history | correctness of the V2 ontological treatment |
| Admitted dataset/official evidence | `v2/research/w2/gate-c-dataset-portfolio.md`, `v2/research/w3/evidence-traceability.md` | observed need for a distinction; source-level provenance | foundational category or stereotype correctness |
| W1 literature/official sources | `v2/research/w1/evidence-sources.md` | problem/use-case plausibility and selected methodological support | admission of a dataset or universal concept validity |
| UFO/OntoUML method | W4 conceptualization artifacts and cited methodology | stereotype/category rationale | pharmaceutical-domain factual truth |
| Formal V2 implementation | `v2/ontology/source/modules/*.ttl` | stable formal identity and implemented axioms | empirical validity or expert agreement |
| Held-out evidence | `v2/evaluation/results/e8-heldout-first-pass-mapping.csv` | later representational fit/generalizability signals | full external validity or completeness |
| W7 computational evaluation | W7 evidence register and family reports | bounded structural/formal/data/application findings | real expert agreement; E9 remains separate |

## Gap classes

Use exactly one primary gap class per review concern and add secondary notes when needed.

| Code | Gap class | Meaning | Required treatment |
|---|---|---|---|
| `G0` | No material gap | Current repository evidence is adequate for the bounded claim being reviewed. | Preserve current provenance; no enrichment required. |
| `G1` | Literature support unmapped | Relevant literature may exist, but no row-level citation is currently registered for this semantic distinction. | Search/verify before making literature-backed claims; otherwise keep the claim source-bounded. |
| `G2` | External ontology alignment unmapped | No verified row-level mapping to an external ontology/reference model is registered. | Record as no external-alignment claim; add mapping only after identity and semantic compatibility checks. |
| `G3` | Source identity/version incomplete | A supporting official/ontology source is named but exact version/distribution/date is not fixed. | Resolve authoritative identity before version-specific or reproducibility claims. |
| `G4` | Dataset-only support | The distinction is grounded in admitted data/official schemas but lacks independent conceptual/methodological corroboration. | Keep the claim observational/operational; prioritize conceptual review. |
| `G5` | Method-only support | The modeling pattern is methodologically defensible but domain evidence is weak or absent. | Keep the claim methodological; seek domain evidence before pharmaceutical-necessity claims. |
| `G6` | V1-lineage-only support | The concept is retained/refined mainly because it existed in CM-PharmE 1.x. | Require independent V2 evidence or mark as legacy-driven. |
| `G7` | Held-out mismatch/partial fit | Held-out evidence is partial, indirect, or exposes a representational gap. | Preserve the mismatch and evaluate whether revision, extension, or explicit limitation is needed. |
| `G8` | Human semantic decision needed | Evidence exists, but the semantic commitment itself requires author/expert judgment. | Do not auto-change ontology; route through review/design decision. |
| `G9` | Claim-boundary gap | The concept may be acceptable, but a proposed manuscript/product claim is stronger than the evidence. | Narrow wording or obtain the missing evidence before publication. |

## Current cross-cutting review priorities

The following priorities are derived from the existing V2 evidence package and #159; they are not new ontology decisions.

### P1 — Foundational category / stereotype commitments
Prioritize concepts whose acceptance depends more on ontological commitment than on source presence: Roles/RoleMixins, Relators, Modes/Qualities, Events/Situations, observation/result distinctions, risk/value/vulnerability patterns, and provenance entities.

Review question: **Does the evidence support the existence of the distinction, and does UFO/OntoUML support the chosen category?** These are separate questions.

Likely gap classes: `G4`, `G5`, `G8`.

### P2 — External-regulatory identity and provenance
For FDA, EMA, WHO, EudraGMDP, EudraVigilance and related official sources, verify that concept-level support does not silently become an ontology-equivalence claim.

Review question: **Is this source being used as factual/schema evidence, or is an external semantic identity actually asserted?**

Likely gap classes: `G2`, `G3`, `G9`.

### P3 — V1 → V2 transformations
Focus on retained/refined/split/moved concepts where the V2 meaning is materially different from CM-PharmE 1.x.

Review question: **Is the migration treatment traceable to both predecessor semantics and new V2 evidence, rather than label continuity?**

Likely gap classes: `G1`, `G6`, `G8`.

### P4 — Resilience/risk concepts
Keep resilience, risk, vulnerability, consequence, treatment and asset/value semantics aligned with the bounded UFO-grounded COVER/ROSE lineage already registered in W1, without claiming that the CM-PharmE scenario evidence proves predictive or operational resilience.

Review question: **Is the ontology reusing a generic risk pattern while keeping pharmaceutical scenario evidence at scenario level?**

Likely gap classes: `G1`, `G2`, `G9`.

### P5 — Held-out partial mappings
Where E8 records only partial representational fit, retain that fact in review rather than upgrading it to exact coverage.

Review question: **Does the partial mapping reveal a genuine semantic gap, or only a source-specific representation difference?**

Likely gap classes: `G7`, `G8`.

## Row-level review record

For each concept that is not immediately `G0`, record the following in review notes or a future machine-readable companion:

| Field | Required content |
|---|---|
| `concept` | Exact V2 canonical label and stable IRI |
| `domain` | One of the 17 canonical V2 domains |
| `current_support` | Existing matrix evidence codes and repository anchors |
| `primary_gap` | One of `G1`–`G9` |
| `gap_statement` | Precise missing/weak evidence or decision boundary |
| `claim_impact` | none / wording-only / local-semantic / cross-domain / publication-blocking |
| `next_evidence_action` | verify source / literature search / ontology alignment check / author decision / expert review / no action |
| `resolution_evidence` | DOI/URL/repository path/issue/decision record when actually resolved |
| `state` | open / bounded-deferred / resolved |

## Decision rule for concept acceptance

A reviewer should not collapse all evidence into one binary decision. Use this sequence:

1. **Identity:** Is the concept and IRI the intended V2 element?
2. **Lineage:** Is V1→V2 migration traceable where a predecessor exists?
3. **Domain evidence:** Is the distinction observed or required in admitted/official evidence?
4. **Foundational treatment:** Is the OntoUML stereotype/category defensible for the intended meaning?
5. **External alignment:** Is any claimed external ontology identity actually verified?
6. **Held-out behavior:** Does E8 support exact/partial/no fit, and is that represented accurately?
7. **Claim boundary:** What is the strongest claim the combined evidence justifies?
8. **Disposition:** APPROVE / APPROVE WITH WORDING CHANGE / REVISE SEMANTICS / SPLIT-MERGE / MOVE DOMAIN-MODULE / DEFER.

A semantic disposition that changes the frozen Gate-D baseline must be routed through a separate V2 design decision before OWL/SHACL modification.

## Literature / ontology enrichment rule

External enrichment is **delta-first**:

- do not search merely to fill every row with citations;
- prioritize `G1/G2/G3/G4/G6/G7/G8/G9` rows that affect a material semantic or publication claim;
- record exact source identity, persistent locator/DOI when available, source type, and what semantic proposition it supports;
- distinguish external ontology reuse/alignment from ordinary literature support;
- do not use a source title/keyword match as equivalence evidence;
- do not upgrade a discovery lead into admitted evidence without the appropriate V2 governance step.

## Claim-boundary invariants

- Dataset/source presence ≠ ontological correctness.
- OWL/HermiT/SHACL/CQ evidence ≠ expert agreement.
- Held-out partial mapping ≠ exact coverage.
- Official regulatory vocabulary ≠ automatic ontology equivalence.
- UFO/OntoUML pattern fit ≠ pharmaceutical empirical validation.
- W7 resilience scenario success ≠ predictive, causal, or operational resilience validation.
- E9 expert evidence remains absent until real eligible participants complete the frozen protocol.
- CM-PharmE 1.x provenance ≠ independent V2 evidence.

## Completion criterion for this gap register

This artifact is complete as a **review control surface** when it is linked from the human-review entry point and used to record material gaps during author review. It does not mean #159 itself is complete. #159 can close only when the 87-concept matrix has been author-reviewed and material evidence gaps are either resolved or explicitly bounded with claim impact.