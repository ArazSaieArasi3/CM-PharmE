# CM-PharmE 2.0 Human Review — P1 Evidence Packets

Issue: #159  
Scope: CM-PharmE 2.0 only  
Status: author-review preparation  
Semantic effect: none  
V1/main impact: none

## Purpose

This artifact prepares bounded, repository-backed review packets for the ten P1 concepts frozen in `human-review-high-risk-queue.md`. It does not record approval, expert judgment, external ontology confirmation, empirical validation, or a semantic change.

The packets deliberately distinguish four review risks: evidence/provenance semantics (`G5`), conditional-source dependence (`G4`), foundational human judgment (`G8`), and held-out partial fit (`G7`). A packet may shorten author review without resolving its human gate.

## Source anchors

- `human-review-concept-provenance-matrix.md` — current Gate-D concept, stereotype, lineage, admitted/held-out evidence and stable IRI.
- `human-review-provenance-gap-register.md` — controlled G0–G9 gap vocabulary and claim-boundary rules.
- `human-review-high-risk-queue.md` — frozen P1 membership and review consequence.
- `../w1/evidence-sources.md` — W1 source/use-case boundaries; W1 evidence is not ontology correctness or dataset admission.
- `../../evaluation/results/e8-heldout-first-pass-mapping.csv` — held-out representational fit where recorded; partial remains partial.
- `../w3/v1-v2-migration-matrix.md` — V1→V2 lineage where applicable.

No source anchor is upgraded beyond its governed role.

---

## P1-01 — Evidence Item (`cmpe:EvidenceItem`)

**Current commitment**  
A `RoleMixin` for information objects participating as evidence in a governed research/traceability context.

**Repository-backed support**
- The provenance matrix places the concept in Evidence Traceability and records research-traceability/all-source support plus M1/M2 methodological support.
- The review queue identifies the bearer/role commitment as the material issue, not the existence of source artifacts.

**What the evidence supports now**
- Evidence participation should be contextual rather than an intrinsic identity of every information object.
- The model needs a traceable way to distinguish an information object from the role it plays in supporting a claim.

**What remains unproven / gap**
- Exact eligible bearer class and anti-rigid role conditions require review (`G5`).
- Being an Evidence Item does not imply truth, empirical validity, expert agreement, or sufficient support.

**Author review question**
Is `EvidenceItem` explicitly a contextual role borne by an information object, with role acquisition/loss independent of the bearer identity?

**Safe boundary before review**
Preserve the role semantics and prohibit any inference from evidence-role membership to truth/validation.

---

## P1-02 — Evidence Support (`cmpe:EvidenceSupport`)

**Current commitment**  
A governed support relation/relational commitment connecting evidence to a claim without equating support with truth.

**Repository-backed support**
- The provenance matrix and research-traceability layer establish the need to represent evidence→claim support.
- M1/M2 support explicit relational modeling, but do not validate the final relata/cardinality choices.

**What the evidence supports now**
- Provenance needs an explicit support link rather than relying on document proximity or labels.
- Support can be recorded while keeping the claim epistemically defeasible.

**What remains unproven / gap**
- Exact relata, multiplicities and support-strength semantics require author inspection (`G5`).
- Support must not mean causal proof, expert consensus, statistical significance, or universal truth.

**Author review question**
Do the current relata make clear what supports what, and can multiple/contradictory evidence items coexist without collapsing support into truth?

**Safe boundary before review**
Retain support as provenance/argument traceability only; stronger epistemic semantics require separate evidence and design decision.

---

## P1-03 — Match Confidence (`cmpe:MatchConfidence`)

**Current commitment**  
A `Quality` attached to a match assertion/entity-resolution result, expressing governed confidence without automatically denoting probability.

**Repository-backed support**
- The provenance matrix records entity-resolution design plus M1/M2 rather than direct domain-source validation.
- The high-risk queue marks the issue as wording-sensitive because confidence can be misread statistically.

**What the evidence supports now**
- Entity-resolution outputs need a quality/assessment dimension distinguishing stronger and weaker candidate matches.
- The quality belongs to the matching assertion/result context, not intrinsically to either matched entity.

**What remains unproven / gap**
- No calibrated probability interpretation, predictive accuracy, threshold validity, or empirical scoring performance is established (`G5`).

**Author review question**
Is the definition sufficiently explicit that Match Confidence is a quality of a match assertion/result and not a probability unless a separately validated scoring method supplies that interpretation?

**Safe boundary before review**
Use non-statistical confidence wording; do not publish calibration/performance claims.

---

## P1-04 — Inventory Observation Result (`cmpe:InventoryObservationResult`)

**Current commitment**  
An observation-result information object recording inventory-related evidence in a bounded source/context.

**Repository-backed support**
- The matrix records conditional `C1` plus M2.
- The queue explicitly treats C1 as conditional evidence whose admissibility/provenance must remain visible.

**What the evidence supports now**
- Inventory observations are a plausible supply-resilience extension requirement.
- Observation result should remain distinct from the inventory-bearing entity and from a shortage situation.

**What remains unproven / gap**
- `C1` cannot establish generic pharmaceutical universality or completeness (`G4`).
- Broader domain necessity beyond the admitted conditional source remains unestablished.

**Author review question**
Is the concept needed as a bounded extension under current C1 provenance, and does its definition avoid universal claims about all pharmaceutical inventory systems?

**Safe boundary before review**
Keep C1 conditional and preserve extension-level, source-bounded wording.

---

## P1-05 — Procurement Activity (`cmpe:ProcurementActivity`)

**Current commitment**  
An `Event` representing a procurement occurrence in the supply-resilience extension.

**Repository-backed support**
- The queue records C1 plus M1/M2 and notes the V1 broad-activity split.
- V2 migration uses refinement rather than treating broad V1 activity labels as equivalent.

**What the evidence supports now**
- Procurement can be represented as a temporally situated occurrence distinct from generic supply activity.
- V1 lineage motivates traceability but does not independently validate final V2 scope.

**What remains unproven / gap**
- Current domain grounding is primarily conditional C1 (`G4`).
- No claim of exhaustive procurement workflow, transaction semantics, or cross-jurisdiction universality is supported.

**Author review question**
Does current evidence justify retaining Procurement Activity as a bounded extension event, and are its participants/context narrow enough to avoid implying a complete procurement model?

**Safe boundary before review**
Retain event semantics as an extension candidate; do not generalize beyond conditional evidence.

---

## P1-06 — Lead Time Observation Result (`cmpe:LeadTimeObservationResult`)

**Current commitment**  
An observation-result information object recording source/context-bounded lead-time evidence.

**Repository-backed support**
- The provenance matrix records conditional C1 plus M2.
- The queue marks both source provenance and observation-result treatment as material.

**What the evidence supports now**
- Lead-time observations can be represented without turning a measured/reported result into an intrinsic supply-chain property.

**What remains unproven / gap**
- C1 remains conditional (`G4`).
- No universal lead-time definition, distribution, causal interpretation, or predictive validity is established.

**Author review question**
Is the result explicitly tied to its source, period/context and observed subject so that it cannot be read as a timeless universal lead-time property?

**Safe boundary before review**
Preserve observation-result and provenance semantics; avoid generic-universality and prediction claims.

---

## P1-07 — Stockout Situation (`cmpe:StockoutSituation`)

**Current commitment**  
A bounded `Situation` representing a stockout state, kept distinct from the broader/regulatory `Medicine Shortage Situation`.

**Repository-backed support**
- The queue records conditional C1 plus P5 framing and O3/O4/M1/M2.
- W1 official shortage/resilience sources establish the relevance of shortage states but do not make stockout and regulatory shortage synonymous.

**What the evidence supports now**
- A local/source-bounded stockout state can be semantically distinct from a jurisdictional/regulatory medicine-shortage situation.
- Situation modeling is appropriate for a state that can hold over an interval rather than an instantaneous disruptive occurrence.

**What remains unproven / gap**
- The precise stockout-versus-shortage boundary and temporal/context conditions require author judgment (`G8`).
- C1 cannot be upgraded into a universal regulatory definition.

**Author review question**
Are stockout and medicine shortage distinguished by scope, reporting authority, product/location context and time conditions strongly enough to prevent synonymy in manuscript claims?

**Safe boundary before review**
Preserve the distinction; never map stockout automatically to regulatory shortage without contextual evidence.

---

## P1-08 — Medicinal Product (`cmpe:MedicinalProduct`)

**Current commitment**  
A `Kind` for pharmaceutical product identity across regulatory, access, shortage and reference contexts.

**Repository-backed support**
- Admission evidence: P1/P2/P4/P5/P6; other support O3/O4/O5/M1/M2.
- Held-out evidence is explicitly mixed: H1 partial, H2 exact, H3 partial.

**What the evidence supports now**
- The concept has broad multi-source support and exact representational fit in H2.
- Held-out evidence demonstrates useful coverage while preserving source-specific mismatches.

**What remains unproven / gap**
- H1/H3 partial mappings must not be reported as exact coverage (`G7`).
- The current evidence does not establish universal product identity harmonization across all regulatory/clinical vocabularies.

**Author review question**
Do H1/H3 mismatches arise from source granularity/context rather than a missing identity distinction, and is manuscript wording explicit about partial fit?

**Safe boundary before review**
Keep the concept unchanged pending mismatch inspection; report held-out fit source-by-source, never as universal completeness.

---

## P1-09 — Pharmaceutical Substance (`cmpe:PharmaceuticalSubstance`)

**Current commitment**  
A `Kind` for medicinal/active substance identity distinct from product identity and presentation.

**Repository-backed support**
- Admission evidence spans P1/P2/P4/P5/P6/S1 with O4/O5/M1/M2 support.
- Held-out status is H1 partial, H2 exact, H3 partial.

**What the evidence supports now**
- Substance/product separation is repeatedly needed across admitted sources.
- H2 provides exact held-out fit while H1/H3 retain mismatch evidence.

**What remains unproven / gap**
- Partial mappings do not prove a model defect or universal substance normalization (`G7`).
- Source-specific ingredient/substance granularity may differ and requires inspection before semantic revision.

**Author review question**
Are H1/H3 partial mappings caused by source granularity/terminology, or do they reveal a missing distinction between substance, ingredient and product identity?

**Safe boundary before review**
Preserve product/substance separation and mismatch evidence; no automatic split/merge.

---

## P1-10 — Product Classification Assignment (`cmpe:ProductClassificationAssignment`)

**Current commitment**  
A `Relator` representing a contextual assignment of a product/substance to a classification entry, rather than intrinsic membership without source/version context.

**Repository-backed support**
- Admission evidence P1/P2/P4/P5 with O4/O5/M1/M2.
- H2 is exact; H3 is partial.
- W4 explicitly split scheme, entry and assignment to preserve classification context.

**What the evidence supports now**
- Classification should retain scheme/entry/source context rather than become an intrinsic product property.
- Exact H2 and partial H3 fit show that representational behavior varies by held-out source.

**What remains unproven / gap**
- H3 partial fit must remain visible (`G7`).
- No universal equivalence among classification schemes/entries is established.

**Author review question**
Does the H3 mismatch reflect list/version/context granularity, and do current relations preserve scheme and assignment context sufficiently for bounded coverage claims?

**Safe boundary before review**
Retain contextual assignment semantics; no cross-scheme equivalence or completeness claim without separate evidence.

---

## Cross-packet review checklist

Before recording any P1 disposition, verify:

1. `G5`: provenance/evidence relations never imply truth, empirical validity, expert agreement, causal proof or calibrated probability.
2. `G4`: C1 remains conditional; its presence never becomes generic pharmaceutical universality.
3. `G8`: foundational distinctions such as stockout-versus-shortage remain human semantic judgments.
4. `G7`: held-out `partial` remains partial and is reported source-by-source rather than averaged into a completeness claim.
5. V1 lineage is traceability, not automatic semantic continuity.
6. Any post-Gate-D semantic change is routed to a separate design-decision issue before OWL/SHACL modification.
7. E9 expert evidence is not inferred from author preparation or repository documentation.

## Packet completion state

- P1 packet inventory: **10/10 prepared**.
- Human/author dispositions: **0/10 recorded**.
- Semantic changes caused by this artifact: **0**.
- External expert evidence added: **0**.
- Hosted CI/Actions required: **no**.

Packet preparation means only that P1 rows have bounded evidence, non-claims and review questions. It does not mean P1 passed review, #159 is complete, or CM-PharmE V2 is publication-ready.
