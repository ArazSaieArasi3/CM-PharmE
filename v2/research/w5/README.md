# W5 — Formal Ontology, SHACL, Mappings and Semantic CI

Status: **IMPLEMENTATION COMPLETE — Formal Gate READY FOR USER DECISION.**

## Objective
Translate the Gate-D-approved conceptual baseline into a reproducible formal ontology while preserving foundational commitments and keeping `main` untouched.

## Completed work items
- V2-045 formal OWL implementation — complete.
- V2-046 machine-readable conceptual registry — complete.
- V2-047 SHACL constraints and validation profiles — complete.
- V2-048 stable IRI/version/provenance policy — complete.
- V2-049 conservative external mapping modules — complete.
- V2-050 deterministic build, OWL-profile, reasoning and semantic-regression CI — implementation complete; gate decision open.

## Formal Gate evidence
Latest mandatory source/workflow run `32215753957`: **SUCCESS**.

Frozen baseline: 642 triples; SHA-256 `59ef47eeed732290736e60bfa1c6bf43a12d15df2f50cff931badb5938cc954a`; 87 conceptual elements represented by 81 OWL classes + 6 datatypes; 52 object properties; 5 datatype properties.

PASS: source parse, conceptual-registry coverage, protected Gate-D distinctions, graph-equivalent RDF serializations, deterministic two-pass build, Meta-SHACL, SHACL smoke (11 NodeShapes), OWL 2 DL profile, ROBOT/HermiT, Manchester/Functional review views and frozen fingerprint regression.

## Methodological boundaries
- W5 formalizes W4; it does not reopen evidence-driven concept discovery.
- A formal PASS does not prove domain completeness, empirical correctness or future data quality.
- Mapping hints do not imply full standards conformance.
- H1–H3 remain held out.
- `https://w3id.org/cm-pharme/2.0/` is the selected target namespace; redirect registration remains pending until separately completed.
- Domain competency-query execution is deferred to W6/W7 where instance/RDB/KG representations exist.
