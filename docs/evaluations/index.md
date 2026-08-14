# Evaluation

CM-PharmE evaluation is organized as a layered evidence architecture. Reusable evaluation methodology is separated from version- or batch-specific evidence and results.

## Evaluation layers

The repository uses nine complementary layers:

1. syntax validation;
2. logical consistency;
3. structural validation;
4. ontological validation;
5. semantic/expert validation;
6. data and mapping validation;
7. competency questions;
8. application validation;
9. research reproducibility.

These layers extend the five qualitative evaluation dimensions reported in the associated research: Syntactic and Structural Correctness, Semantic and Conceptual Accuracy, Conceptual Clarity, Adaptability and Modifiability, and Pragmatic Value.

## Available evaluations

- [CM-PharmE v1.0.0 — Structural Extraction Audit](v1.0.0-structural-audit.md): descriptive statistics, source-model anomalies, extraction quality, and B2 documentation assessment.
- [B3 — Formal Ontology Audit](b3-formal-ontology-audit.md): formal source coverage, relation/cardinality traceability, IRI design, lifecycle/provenance decisions, validation evidence, and remaining release-readiness gaps.
- [B4 — Paper-Grounded Evaluation Plan](b4-evaluation-plan.md): translates the evaluation procedures and evidential boundaries reported in the published conference paper and journal manuscript under review into a repository-native validation program.

## B4 evidence package

Machine-readable and scenario evidence is maintained under [`../../evaluation/`](../../evaluation/), including:

- eight competency questions;
- eight OntoUML-informed anti-pattern categories and historical observations;
- the vaccine-distribution reference scenario;
- publication-derived evidence status and traceability.

## Validation boundary

B3 records successful structural/reference-package validation but does not claim full OWL DL reasoner consistency. B4 preserves the qualitative research evidence while targeting stronger repository-reproducible checks, including reasoner evidence, executable competency questions, scenario/data tests, and explicit publication-to-result traceability.

No evaluation result should be generalized beyond the procedure and evidence that produced it.