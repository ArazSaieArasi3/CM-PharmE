# Formal Ontology Engineering Record (B3)

This page records the formal-ontology work originally developed during the B3 engineering stage and later integrated into `main`. It is a historical engineering record, **not** a separate CM-PharmE semantic release.

The current stable semantic baseline remains `v1.0.0`. The B3 formalization was built from that semantic inventory; later B4/B4.10 and B5 work added executable evaluation, OWL DL reasoning, reproducible builds and CI without automatically declaring a new model version.

## Formal-ontology additions established in B3

- persistent stable IRI design under `https://w3id.org/cm-pharme/`
- modular formal ontology authoring source
- formal definitions for 39 canonical concepts
- formal relation/property representation and lifecycle metadata
- complete endpoint-cardinality registry for all 40 relation IDs
- explicit generalization formalization for `CMPE-R0006`
- deprecation/supersession handling for R0011/R0027
- lexical normalization of R0031 while preserving its historical raw label
- cautious UFO/OntoUML stereotype-correspondence notes
- SHACL reference constraints and multi-serialization reference package
- structural validation report and B3 audit

## Subsequent validation and engineering

Follow-up work originally deferred from B3 has since been completed and integrated into `main`:

- B4/B4.10 added paper-grounded evaluation evidence, executable competency questions, a machine-readable evaluation scenario, semantic finding disposition and ROBOT/HermiT logical validation;
- B5 restored full annotation/provenance parity with the validated B3 reference graph and added deterministic serialization, SHACL generation, build manifests, checksums, reproducible release bundles and GitHub Actions quality gates.

The preserved `v1.0.0` artifacts remain unchanged. External `w3id.org` redirect registration, final external ontology-alignment decisions, broader independent expert/domain replication and future semantic refinements remain outside this historical engineering record.
