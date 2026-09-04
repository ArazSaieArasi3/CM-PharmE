# CM-PharmE 2.0 Human Review — P0 Evidence Packets

Issue: #159  
Scope: CM-PharmE 2.0 only  
Status: author-review preparation  
Semantic effect: none  
V1/main impact: none

## Purpose

This artifact prepares bounded, repository-backed evidence packets for the six P0 concepts in `human-review-high-risk-queue.md`. It is a review aid, not an approval record and not a substitute for real author/expert judgment.

No packet below establishes expert consensus, empirical validation, predictive performance, operational resilience, or publication readiness. Any semantic change remains a separate design decision.

## Source anchors used in this packet set

- W1 evidence register: `../w1/evidence-sources.md`
  - `W1-S04` — EMA Union List of Critical Medicines and supply-chain vulnerability methodology: need/use-case support for critical-medicine prioritization, vulnerability assessment, alternative-supply reasoning and resilience scenarios.
  - `W1-S13` — COVER/ROSE UFO-grounded risk literature: methodological support for reusing/alignment of generic risk, vulnerability, event, value, consequence and treatment semantics rather than duplicating them in the pharmaceutical Core.
- V1→V2 migration: `../w3/v1-v2-migration-matrix.md`
  - `C0028 Risk Management Activity` → move/refine into Risk & Resilience extension.
  - `C0032 Supply Chain Relationship` → split/deprecate generic form into typed `Supply Dependency` and related evidence-backed relations.
- Human-review matrix: `human-review-concept-provenance-matrix.md`
  - freezes the six concepts' current working definitions, stereotypes, evidence codes and stable IRIs.
- Risk-first queue: `human-review-high-risk-queue.md`
  - freezes the P0 set and review consequence.

These anchors establish provenance for review. They do not by themselves prove the foundational stereotype or all relation constraints.

---

## P0-01 — Asset at Risk (`cmpe:AssetAtRisk`)

**Current commitment**  
A `RoleMixin` adapter representing entities that participate as assets in a risk situation/context.

**Repository-backed support**
- V1/W1 continuity establishes risk management as an existing concern, but not the final V2 role-bearing semantics.
- `W1-S13` supports UFO-grounded risk semantics and reuse/alignment with COVER/ROSE rather than a pharmaceutical-specific reinvention.
- The current provenance matrix records support as `V1/W1 + R1/M1/M2`.

**What the evidence supports now**
- It is defensible to review `Asset at Risk` as a contextual risk role rather than an intrinsic pharmaceutical kind.
- Reuse/alignment with a generic risk pattern is methodologically motivated.

**What remains unproven / gap**
- Exact eligible bearer range is not established by source presence alone.
- The final `RoleMixin` commitment still requires author-level foundational judgment (`G8`).
- No claim should imply that every pharmaceutical entity is an asset, or that risk/value has been empirically assessed.

**Author review question**
Does the intended bearer range justify a `RoleMixin` adapter, and is the role explicitly dependent on a risk/value context rather than asserted intrinsically?

**Safe disposition boundary before review**
Keep current semantics unchanged; record only a wording boundary if needed. Any bearer/stereotype change must go to a design-decision issue.

---

## P0-02 — Vulnerability (`cmpe:Vulnerability`)

**Current commitment**  
A `Mode` representing susceptibility/disposition of a bearer to adverse effects under relevant threat/risk conditions.

**Repository-backed support**
- `W1-S04` provides pharmaceutical resilience/vulnerability use-case relevance.
- `W1-S13` provides methodological risk-ontology support for vulnerability as part of a generic UFO-grounded risk pattern.
- The current provenance matrix records `W1 risk alignment + R1/M1/M2`.

**What the evidence supports now**
- Vulnerability is relevant to resilience reasoning and should remain separated from an observed disruption event or shortage situation.
- Treating vulnerability as bearer-dependent is consistent with the intended risk pattern.

**What remains unproven / gap**
- Source evidence does not independently validate the exact `Mode` stereotype.
- Bearer relation, trigger/context and distinction from measured risk score/observation require author confirmation (`G8`).
- No empirical vulnerability score or predictive interpretation is evidenced here.

**Author review question**
Is `Vulnerability` intended as an intrinsic-but-contextually-relevant disposition of a bearer, and are bearer and triggering/risk-context relations explicit enough to prevent interpretation as a mere metric or observed state?

**Safe disposition boundary before review**
Preserve `Mode` and current definition as a candidate commitment; do not strengthen claims beyond susceptibility/disposition semantics.

---

## P0-03 — Risk Treatment Plan (`cmpe:RiskTreatmentPlan`)

**Current commitment**  
An information object/specification prescribing intended risk-treatment actions, separate from any performed occurrence.

**Repository-backed support**
- `C0028 Risk Management Activity` is explicitly moved/refined in the V1→V2 migration rather than copied generically.
- `W1-S13` supports treatment semantics as part of a reusable generic risk pattern.
- The current provenance matrix records `W1/V1 + R1/M1/M2`.

**What the evidence supports now**
- Separating normative/planned treatment from actual treatment execution is a legitimate modeling concern.
- The V2 migration explicitly avoids retaining one undifferentiated generic risk-management activity.

**What remains unproven / gap**
- The exact information-object stereotype and its commitment/plan relations require author inspection (`G8`).
- Existing evidence does not establish completeness of treatment-plan content or effectiveness.

**Author review question**
Is the plan intended to be a persistent normative/specification information object that can exist without execution, and is its relation to the later activity explicit and non-conflating?

**Safe disposition boundary before review**
Retain plan/execution separation; do not claim that a plan was executed or effective unless separate evidence exists.

---

## P0-04 — Risk Treatment Activity (`cmpe:RiskTreatmentActivity`)

**Current commitment**  
An `Event` representing an actually performed risk-treatment occurrence, distinct from the plan/specification that may prescribe it.

**Repository-backed support**
- `C0028 Risk Management Activity` supplies historical lineage but V2 deliberately refines/splits it.
- `W1-S13` supports treatment/event semantics in the generic risk-alignment layer.
- The current provenance matrix records `W1/V1 + R1/M1/M2`.

**What the evidence supports now**
- A performed occurrence should remain ontologically distinct from the information object that specifies or recommends it.
- Event semantics are appropriate for review because execution is temporally situated and participant-bearing.

**What remains unproven / gap**
- Event identity criteria and exact plan↔execution relation are not established by source presence alone (`G8`).
- No implementation or effectiveness evidence is implied.

**Author review question**
Does the activity represent a concrete occurrence with participants/time, and can it occur with zero, one or multiple associated treatment plans without collapsing prescription and execution?

**Safe disposition boundary before review**
Keep event identity and plan separation; route any cardinality, participation or identity change through a design-decision issue.

---

## P0-05 — Supply Dependency (`cmpe:SupplyDependency`)

**Current commitment**  
A typed dependency relation/relational commitment connecting supply-relevant relata in a bounded context, replacing the generic V1 `Supply Chain Relationship` form.

**Repository-backed support**
- `C0032 Supply Chain Relationship` is explicitly split/deprecated in W3 in favor of typed `Supply Dependency` and other relations.
- `W1-S04` motivates supply-chain vulnerability and alternative-supply reasoning.
- The provenance matrix records `P5/C1/W1 + O4/R1/M1/M2`; `C1` remains conditional evidence and must not be upgraded.

**What the evidence supports now**
- The generic V1 supply-chain relation is too broad for V2.
- A typed dependency concept is relevant for resilience analysis and can bridge supply and risk views.

**What remains unproven / gap**
- Exact relata, directionality, dependency object and contextual qualifiers require author judgment (`G8`).
- Conditional `C1` evidence cannot establish universal pharmaceutical-supply semantics.
- No complete transaction network or causal dependency graph is established.

**Author review question**
What exactly depends on what, under which supply context, and is the dependency directional/contextual rather than a generic symmetric association?

**Safe disposition boundary before review**
Preserve typed dependency and the explicit non-claim of a complete transaction network; do not generalize beyond admitted/conditional evidence.

---

## P0-06 — Disruption Event (`cmpe:DisruptionEvent`)

**Current commitment**  
An `Event` representing a bounded disruptive occurrence relevant to supply/resilience scenarios.

**Repository-backed support**
- `W1-S04` supports vulnerability/resilience and crisis-oriented pharmaceutical supply reasoning.
- `W1-S01` documents shortage causes such as manufacturing/quality problems, delays, raw-material/component problems, demand increases and discontinuations, which supports the need to distinguish disruptive occurrences from shortage states.
- `W1-S13` supports generic risk/event alignment.
- The provenance matrix records `W1/P5/C1 + O1/O4/R1/M1/M2`; `C1` remains conditional.

**What the evidence supports now**
- A disruptive occurrence can be modeled separately from a resulting `Medicine Shortage Situation`, vulnerability, or observation result.
- The concept is suitable for representational/scenario reasoning.

**What remains unproven / gap**
- Scenario success is not predictive validation, operational resilience evidence, or causal proof (`G9`).
- Source evidence does not establish exhaustive disruption taxonomy or probability/impact values.
- No claim should state that CM-PharmE predicts disruptions or verifies real-world resilience effectiveness.

**Author review question**
Is the event boundary sufficiently clear relative to shortage situations, vulnerabilities and observations, and are manuscript/product claims limited to representation/scenario reasoning?

**Safe disposition boundary before review**
Preserve the event concept and explicitly retain the publication non-claim: representational/scenario support only unless separate empirical evidence is later produced.

---

## Cross-packet review checklist

For each P0 concept, the author/reviewer should answer all applicable questions before any disposition is recorded:

1. Is the concept's current stereotype consistent with the intended foundational commitment?
2. Is the bearer/relata/event identity explicit enough to avoid category conflation?
3. Does V1→V2 continuity reflect semantic continuity rather than label continuity?
4. Is every use of `C1` kept conditional?
5. Are `W1-S04`/official resilience sources used only for need/domain relevance, not as proof of ontology correctness?
6. Is `W1-S13` used as methodological/risk-pattern support rather than expert validation of this implementation?
7. Are scenario/held-out results prevented from becoming predictive, causal or operational-effectiveness claims?
8. If semantics need change, is the change routed to a separate design-decision issue rather than silently edited during review?

## Packet completion state

- P0 packet inventory: **6/6 prepared**.
- Human/author dispositions: **0/6 recorded**.
- Semantic changes caused by this artifact: **0**.
- External expert evidence added: **0**.
- Hosted CI/Actions required: **no**.

Packet preparation complete means only that the six P0 rows now have bounded evidence and review questions. It does **not** mean the rows have passed human review or that #159 is ready to close.
