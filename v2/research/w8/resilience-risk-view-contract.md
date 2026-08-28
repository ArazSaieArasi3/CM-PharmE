# V2-081 — W8 C5 bounded resilience/risk view contract

Issue: #153  
Representative task: T06  
Source evidence family: W7-E12  
Ontology mutation for demonstrator convenience: **prohibited**

## Frozen evidence contract

The W8 C5 view consumes only the five already-frozen E12 controlled scenarios:

1. RES-01 — Critical medicine single-provider disruption — EXACT
2. RES-02 — Alternative medicine under provider disruption — EXACT
3. RES-03 — Jurisdictional shortage versus physical geography — EXACT
4. RES-04 — Risk treatment and recovery boundary — PARTIAL
5. RES-05 — Sensitivity to missing supply evidence — EXACT_TEST_MECHANISM

The executable source remains:
- `v2/evaluation/protocol/e12-resilience-scenario-registry.json`
- `v2/evaluation/protocol/e12-resilience-scenarios.ttl`
- `tools/v2_evaluation/e12_resilience_scenarios.py`

W8 must re-run that evaluator rather than copying the historical PASS into a new claim.

## Required reproduction invariants

A W8 C5 candidate is acceptable only when all of the following are reproduced from the current candidate state:

- five and only five frozen scenarios are present, in the frozen IDs RES-01..RES-05;
- 5/5 executable scenario queries match their frozen expected outcomes;
- 5/5 controlled provenance checks pass;
- RES-05 changes from supported exposure to unsupported after removal of only the provider edge;
- RES-05 remains interpreted as `INSUFFICIENT_EVIDENCE_NOT_RESILIENCE`;
- RES-03 keeps `RegulatoryJurisdiction` distinct from facility physical `GeographicFeature` location;
- RES-04 remains partial and the three extension gaps remain visible;
- ontology goal-post changes made to improve the demonstrator result remain exactly zero.

## Retained extension gaps

The view must display rather than repair:

1. no explicit RecoveryEvent / RecoveredState semantic element;
2. no explicit RiskTreatmentPlan→RiskTreatmentActivity object property;
3. no explicit Vulnerability bearer/domain object property.

These are extension/refinement inputs, not W8 demonstrator patch requirements.

## Deterministic outputs

`tools/v2_observatory/render_resilience_risk_view.py` re-runs E12 and produces:

- `v2/application/observatory/generated/resilience-risk-view.json`
- `v2/application/observatory/generated/resilience-risk-view.html`

The JSON is the machine-readable article-scope evidence view. The HTML is a deterministic human-readable rendering of the same bounded state.

Every scenario row exposes:
- scenario identity;
- frozen representability category;
- observed query result;
- whether the frozen expectation reproduced;
- provenance completeness;
- limitation flags;
- retained gap text where applicable.

## Claim boundary

A successful exact-head hosted gate may support only this claim:

> CM-PharmE 2.0 reproducibly represents and queries the five frozen controlled W7-E12 resilience scenarios through an inspectable W8 view that preserves provenance, evidence sensitivity and known extension gaps.

It does **not** support prediction accuracy, causal validity, intervention effectiveness, stockout prevention, recovery performance, operational resilience, real-world supply-chain completeness, or validated risk scoring.

## V2-083 handoff condition

T06 is ready for representative-task evaluation only after the exact merge-candidate head successfully executes the dedicated V2-081 hosted gate and the generated JSON/HTML artifacts are retained from that head.
