# Evaluation Evidence

This directory stores machine-readable and scenario-oriented evidence for CM-PharmE evaluation. It complements the human-readable method and audit documentation under `docs/evaluations/`.

## Evidence categories

- `competency-questions.yaml` — versioned competency-question registry with current B4 execution status
- `anti-patterns.yaml` — publication-derived anti-pattern baseline plus current B4 disposition
- `scenarios/` — human-readable reference scenarios and their evidential boundaries
- `samples/` — machine-readable constructed instance samples used in executable evaluation
- `evidence/` — publication provenance, structural validation, query results, anti-pattern/scenario/expert evidence, and reasoner status
- `assertions/` — reserved for additional explicit test oracles

## B4 executed evidence

B4 now includes:

- `evidence/b4-structural-validation.json` — 28/28 structural/traceability checks
- `evidence/b4-cq-results.csv` — expected and observed results for all eight executable competency queries
- `evidence/b4-scenario-validation.json` — schema compatibility of the vaccine sample
- `evidence/b4-scenario-traceability.yaml` — manuscript-to-formal scenario alignment and discrepancies
- `evidence/b4-expert-evidence.yaml` — normalized four-expert publication evidence
- `evidence/b4-reasoner-validation.md` — explicit record that OWL DL reasoner execution remains blocked / unverified in the current runtime
- `samples/vaccine-distribution.ttl` — constructed machine-readable scenario

The current anti-pattern dispositions are maintained in `anti-patterns.yaml`. The eight SPARQL queries are stored under `../ontology/queries/competency/`.

## Evidence rule

A publication-reported result, a repository-recorded provenance statement, and a repository-executed validation result are different evidence states. B4 preserves that distinction. A bounded PASS on a constructed scenario is not treated as empirical deployment evidence.

## Evaluation layers

B4 organizes evidence across E1–E9: syntax, logic, structure, ontological validation, semantic/expert validation, data/mapping validation, competency questions, application validation, and research reproducibility.

See the [evaluation method](../docs/methodology/evaluation-method.md), [B4 plan](../docs/evaluations/b4-evaluation-plan.md), [executed matrix](../docs/evaluations/b4-evaluation-matrix.md), and [B4 final evaluation](../docs/evaluations/b4-final-evaluation.md).
