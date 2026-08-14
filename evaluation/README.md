# Evaluation Evidence

This directory stores machine-readable and scenario-oriented evidence for CM-PharmE evaluation. It complements the human-readable method and audit documentation under `docs/evaluations/`.

## Evidence categories

- `competency-questions.yaml` — versioned competency-question registry with B4 execution status
- `anti-patterns.yaml` — publication-derived anti-pattern baseline plus current B4 re-evaluation
- `scenarios/` — human-readable reference scenarios and their evidential boundaries
- `samples/` — machine-readable constructed instance samples used in executable evaluation
- `evidence/` — publication provenance, structural validation, query results, scenario/expert evidence, reasoner evidence, semantic-finding disposition, and source-parity evidence
- `assertions/` — reserved for additional explicit test oracles

## Executed evidence

B4/B4.10 includes:

- `evidence/b4-structural-validation.json` — 28/28 structural/traceability checks
- `evidence/b4-cq-results.csv` — expected and observed results for all eight executable competency queries
- `evidence/b4-scenario-validation.json` — schema compatibility of the vaccine sample
- `evidence/b4-scenario-traceability.yaml` — manuscript-to-formal scenario alignment and discrepancies
- `evidence/b4-expert-evidence.yaml` — normalized four-expert publication evidence
- `evidence/b4-reasoner-validation.md` — successful repository-executed ROBOT/HermiT logical validation
- `evidence/b4-10-source-parity.json` — graph-difference evidence between the B3 packaged canonical source and GitHub modular-source assembly
- `evidence/b4-10-semantic-findings.yaml` — machine-readable disposition of the five targeted semantic findings
- `samples/vaccine-distribution.ttl` — constructed machine-readable scenario

The eight SPARQL queries are stored under `../ontology/queries/competency/`. The reproducible reasoner workflow is `.github/workflows/ontology-reasoner.yml`, with assembly performed by `../tools/ontology/assemble_modules.py`.

## B4.10 reasoner result

GitHub Actions run `31796520297` executed ROBOT `v1.9.10` with HermiT against the assembled logical ontology. The ROBOT JAR was verified by SHA-256 before execution and the workflow enforced a zero reasoner exit code. The run concluded **success** and uploaded a reasoner evidence artifact.

The GitHub modular source and B3 packaged canonical source differ in annotation/provenance coverage, but B4.10 found zero logical-predicate differences between them. Annotation parity remains an engineering follow-up rather than a logical-validation failure.

## Evidence rule

A publication-reported result, a repository-recorded provenance statement, and a repository-executed validation result are different evidence states. B4 preserves that distinction. A bounded PASS on a constructed scenario is not treated as empirical deployment evidence, and a HermiT logical PASS is not treated as proof of ontological or domain completeness.

## Evaluation layers

B4 organizes evidence across E1–E9: syntax, logic, structure, ontological validation, semantic/expert validation, data/mapping validation, competency questions, application validation, and research reproducibility.

See the [evaluation method](../docs/methodology/evaluation-method.md), [B4 plan](../docs/evaluations/b4-evaluation-plan.md), [executed matrix](../docs/evaluations/b4-evaluation-matrix.md), [B4/B4.10 final evaluation](../docs/evaluations/b4-final-evaluation.md), and [B4.10 semantic finding disposition](../docs/evaluations/b4-10-semantic-finding-disposition.md).
