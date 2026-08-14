# Repository Engineering

CM-PharmE treats repository engineering as part of research reproducibility. The conceptual model and ontology remain research artifacts; build, validation and release automation exist to ensure that derived files can be reconstructed from the authoritative source without manual drift.

## Current engineering documents

- [Reproducible Ontology Build and CI](b5-reproducible-build.md) — deterministic source assembly, serializations, SHACL, checksums, regression queries and HermiT reasoning. This work was historically tracked as phase `B5`.
- [Final CI Audit](b5-ci-audit.md) — evidence from the completed repository-engineering cycle.
- [Release Readiness](release-readiness.md) — completed closure status plus the remaining semantic-release and administrative decisions.

## Current engineering state

The repository-modernization cycle is complete on `main`: formal ontology source, executable evaluation, deterministic build, SHACL generation, competency-query regression, ROBOT/HermiT logical validation, and post-merge CI evidence are integrated.

The stable semantic baseline remains `v1.0.0`. Engineering automation does not create a semantic version by itself.

The historical `B5` identifier is retained in filenames and audit provenance, but descriptive names are preferred in reader-facing documentation.