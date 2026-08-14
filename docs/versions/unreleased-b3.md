# Unreleased — B3 Formal Ontology Development

This page records the formal-ontology work performed on `ontology/b3-formal-ontology-v1`. It is **not** a new CM-PharmE semantic release by itself.

The current stable semantic baseline remains `v1.0.0`. B3 is an unreleased formalization and engineering cycle based on that semantic inventory. A new model version is assigned only when an explicit semantic diff justifies it.

## B3 additions

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

## Not yet a release claim

B3 does not yet constitute a new immutable release and does not alter the preserved `v1.0.0` artifacts. Full OWL DL reasoner evidence, CI/rebuild automation, final external ontology alignment, w3id registration, and broader evaluation remain follow-up work.
