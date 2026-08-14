# Versions

CM-PharmE separates the living/current model from immutable historical release snapshots and from engineering work that does not itself declare a new semantic version.

| Version / record | Status | Description |
|---|---|---|
| [`v1.0.0`](v1.0.0.md) | Current stable semantic baseline | Original conceptual-model and ontology artifacts preserved from the pre-refactor repository, with normalized traceability documentation |
| [Formal ontology engineering record](unreleased-b3.md) | Integrated into `main`; not a semantic release | B3–B5 formalization, evaluation, logical validation, reproducible build and CI engineering performed against the `v1.0.0` semantic inventory |

A semantic version is assigned only after authoritative model changes are compared against the current stable baseline and an explicit semantic delta justifies a new release. Engineering improvements, evaluation work, or manuscript revisions alone do not create a new CM-PharmE semantic version.
