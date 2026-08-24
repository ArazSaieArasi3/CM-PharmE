# W7-E12 Manuscript Evidence Note — Resilience Scenarios

## Evidence-qualified result
CM-PharmE 2.0 was evaluated on five frozen, controlled resilience-oriented scenarios. Three scenarios were expected to be exactly representable, one was prospectively marked partial, and one was a missing-evidence sensitivity mechanism. All **5/5** frozen executable queries matched their expected outcomes, provenance was complete for **5/5** controlled scenarios, and the missing-supply-evidence mutation behaved as frozen: the exposure query changed from `true` to `false` after removal of the provider edge.

The family result is **PASS WITH WARNING**. The warning is substantive: the current Risk & Resilience Extension lacks explicit recovery-event/state semantics, an explicit RiskTreatmentPlan→RiskTreatmentActivity relation, and an explicit bearer relation for `Vulnerability`. These gaps were retained after first-pass evaluation and were not corrected to improve the score.

## Suitable manuscript wording
A defensible result statement is:

> In a prospectively frozen controlled scenario evaluation, CM-PharmE 2.0 supported all five predefined resilience-oriented query outcomes, including critical-medicine dependency/disruption, alternative-supply, jurisdiction-versus-geography and evidence-sensitivity cases. The evaluation also identified bounded extension gaps in recovery semantics and vulnerability/treatment grounding. These results demonstrate scenario-level representational adequacy only and are not evidence of predictive or operational resilience effectiveness.

## Claim restrictions
Do not state or imply that E12 establishes shortage prediction, causal disruption propagation, intervention effectiveness, stockout prevention, recovery performance, validated risk scoring, operational resilience, or complete real-world pharmaceutical supply-chain coverage.

Freeze anchor: `04baf01415f3d1d51724b59032ac0c761c48a738`  
Actions run: `32544985010` — SUCCESS  
Artifact: `9468209198`  
Digest: `sha256:266738bad7626dcd97d0b7e3ab514016e46f2791f80c3357ea524b59aa839185`
