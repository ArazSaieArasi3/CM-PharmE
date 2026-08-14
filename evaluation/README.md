# Evaluation Evidence

This directory stores machine-readable and scenario-oriented evidence for CM-PharmE evaluation. It complements the human-readable method and audit documentation under `docs/evaluations/`.

## Evidence categories

- `competency-questions.yaml` — versioned competency-question registry
- `anti-patterns.yaml` — historical and current OntoUML-informed inspection records
- `scenarios/` — reference scenarios used for representational and application checks
- `evidence/` — publication-to-evidence traceability and evidence-status policy
- `assertions/` — future machine-readable expected assertions and test oracles
- `samples/` — future representative instance/data samples used in executable evaluation

## Evidence rule

A publication-reported result, a repository-recorded provenance statement, and a repository-executed validation result are different evidence states. Every B4 result should preserve that distinction.

## Evaluation layers

B4 organizes evidence across E1–E9:

1. syntax validation
2. logical validation
3. structural validation
4. ontological validation
5. semantic/expert validation
6. data and mapping validation
7. competency questions
8. application validation
9. research reproducibility

See [`../docs/methodology/evaluation-method.md`](../docs/methodology/evaluation-method.md) and [`../docs/evaluations/b4-evaluation-plan.md`](../docs/evaluations/b4-evaluation-plan.md).