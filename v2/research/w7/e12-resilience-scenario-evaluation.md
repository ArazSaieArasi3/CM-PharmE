# W7-E12 — Pharmaceutical Resilience Scenario Evaluation

## Status
**Mandatory gate: PASS**  
**Family interpretation: PASS WITH WARNING**

Freeze anchor: `04baf01415f3d1d51724b59032ac0c761c48a738`  
Final GitHub Actions run: `32544985010` — **SUCCESS**  
Evidence artifact: `9468209198`  
Artifact digest: `sha256:266738bad7626dcd97d0b7e3ab514016e46f2791f80c3357ea524b59aa839185`

## Evaluation design
E12 is a controlled scenario-level evaluation of whether the frozen CM-PharmE 2.0 ontology can represent and query selected pharmaceutical resilience and critical-medicine vulnerability situations. The scenario registry, assumptions, expected query outcomes, representability categories, provenance expectations and missing-evidence sensitivity rule were frozen before evaluator execution.

The five frozen cases trace to the W1 resilience catalog and the later frozen ontology:
1. **RES-01 — Critical medicine single-provider disruption**
2. **RES-02 — Alternative medicine under provider disruption**
3. **RES-03 — Jurisdictional shortage versus physical geography**
4. **RES-04 — Risk treatment and recovery boundary**
5. **RES-05 — Sensitivity to missing supply evidence**

The ABox is intentionally synthetic and controlled. It does not describe real products, organizations, shortages, interventions or outcomes.

## Results
- frozen scenarios: **5**
- expected representability: **3 exact + 1 partial + 1 sensitivity mechanism**
- scenario queries matching frozen expectations: **5/5**
- scenario provenance complete: **5/5**
- missing-evidence sensitivity: **PASS**
- first-pass ontology changes made to improve results: **0**

### RES-01 — critical medicine / provider disruption
The ontology represented a medicinal product with contextual critical-medicine classification, an explicit supply dependency on a provider, a disruption affecting that provider, and a shortage situated in a regulatory jurisdiction. The frozen executable query returned the expected result.

### RES-02 — alternative-supply semantics
The disrupted dependency and an explicit `AlternativeMedicineAssignment` were represented simultaneously. The frozen query recovered both the disrupted supply path and the alternative medicinal product as expected.

### RES-03 — jurisdiction versus physical geography
A shortage was related to a `RegulatoryJurisdiction`, while a facility was separately related to a physical `GeographicFeature` through `locatedIn`. The query confirmed that the two contextual dimensions remained distinct in the controlled case, consistent with Gate-D semantics.

### RES-04 — risk treatment and recovery boundary
`Vulnerability`, `RiskTreatmentPlan` and `RiskTreatmentActivity` are available, and a treatment activity can explicitly address a vulnerability. However, the frozen ontology does **not** yet provide:
- an explicit RecoveryEvent / RecoveredState semantic element;
- an explicit relation linking `RiskTreatmentPlan` to `RiskTreatmentActivity`;
- an explicit bearer/domain property grounding `Vulnerability` in the OWL extension.

This scenario therefore remains **PARTIAL**, and the gaps are retained rather than patched after first-pass execution.

### RES-05 — missing-evidence sensitivity
The baseline exposure query was `true`. After the evaluator removed only the `dependencyProvider` edge, the same query became `false`, exactly as frozen. The result is interpreted as **INSUFFICIENT_EVIDENCE_NOT_RESILIENCE**. Under open-world and evidence-bounded semantics, absence of a provider edge is not evidence that the product is resilient or independent.

## Gap taxonomy
The following extension gaps were detected and retained:
1. **Recovery-semantics gap** — no explicit recovery event/state representation.
2. **Risk-treatment linkage gap** — no explicit RiskTreatmentPlan→RiskTreatmentActivity property.
3. **Vulnerability grounding gap** — no explicit object property with `Vulnerability` as domain/bearer relation.

These findings are refinement inputs for a later Risk & Resilience Extension and should not be silently promoted into the frozen Core during W7.

## Interpretation boundary
E12 supports a bounded claim that CM-PharmE 2.0 can represent and query selected critical-medicine, dependency, disruption, shortage, alternative-supply and treatment-oriented scenarios while exposing specific extension gaps and evidence sensitivity.

E12 does **not** establish:
- shortage or disruption prediction accuracy;
- causal validity of the scenarios;
- intervention or mitigation effectiveness;
- stockout prevention;
- recovery performance;
- operational resilience;
- complete real-world supply-chain reconstruction;
- validated risk scoring.

## Reproducibility assets
- `v2/evaluation/protocol/e12-resilience-scenario-registry.json`
- `v2/evaluation/protocol/e12-resilience-scenarios.ttl`
- `tools/v2_evaluation/e12_resilience_scenarios.py`
- `.github/workflows/v2-w7-e12-resilience.yml`
- Actions run `32544985010`
- artifact `9468209198`

## W7 hand-off
E12 is complete. E13 should now perform the independent reproducibility/rebuild audit while E9 remains open for real expert collection. Gate F must continue to treat E9 as unresolved until real eligible expert responses are analyzed.
