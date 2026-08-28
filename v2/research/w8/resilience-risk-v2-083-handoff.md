# V2-083 handoff — T06 bounded resilience scenario

Source work item: V2-081 / #153  
Target work item: V2-083 representative-task evaluation  
Task: T06 Resilience scenario

## Candidate task contract

T06 exercises the W8 C5 bounded resilience/risk view only against the frozen W7-E12 scenario family. It does not introduce a new scenario, predictive model, risk score, causal model or intervention-effectiveness claim.

## Inputs

- frozen scenario registry: `v2/evaluation/protocol/e12-resilience-scenario-registry.json`
- frozen controlled ABox: `v2/evaluation/protocol/e12-resilience-scenarios.ttl`
- frozen evaluator: `tools/v2_evaluation/e12_resilience_scenarios.py`
- W8 renderer: `tools/v2_observatory/render_resilience_risk_view.py`
- view contract: `v2/research/w8/resilience-risk-view-contract.md`

## Expected deterministic task outcome

On the exact candidate head:

- RES-01 query expectation reproduces;
- RES-02 query expectation reproduces;
- RES-03 keeps shortage regulatory jurisdiction distinct from facility physical geography;
- RES-04 remains PARTIAL and displays all three retained extension gaps;
- RES-05 baseline exposure is supported, removal of only `dependencyProvider` makes the exposure query unsupported, and the rendered interpretation is exactly `INSUFFICIENT_EVIDENCE_NOT_RESILIENCE`;
- provenance completeness is 5/5;
- ontology goal-post changes for T06 are 0.

## V2-083 evaluation checks

V2-083 should evaluate T06 on:

1. deterministic result correctness against the frozen E12 expected outcomes;
2. provenance visibility for every displayed scenario;
3. visibility of partial/gap status rather than success-only presentation;
4. correct open-world/evidence-bounded interpretation for RES-05;
5. preservation of the jurisdiction-vs-geography distinction in RES-03;
6. absence of predictive, causal, mitigation-effectiveness, recovery-performance and validated-risk-scoring language.

## Evidence state at handoff

Implementation and deterministic gate definition are prepared by V2-081. This handoff does **not** assert that the merge-candidate hosted gate has passed. V2-083 execution must bind to the exact successful V2-081 candidate head/run before treating T06 as reproducibly available.

## Claim boundary

T06 may support scenario-level representational/application evidence only. It cannot support operational resilience, real-world risk prediction, causal effectiveness or real-world supply-chain completeness.
