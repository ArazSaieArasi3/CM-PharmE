# W5 — Formal Ontology, SHACL, Mappings and Semantic CI

## Objective
Translate the Gate-D-approved conceptual baseline into a reproducible formal ontology while preserving foundational commitments and keeping `main` untouched.

## Work items
- V2-045 formal OWL implementation.
- V2-046 machine-readable conceptual registry.
- V2-047 SHACL constraints and validation profiles.
- V2-048 stable IRI/version/provenance policy.
- V2-049 conservative external mapping modules.
- V2-050 deterministic build, OWL-profile, reasoning and semantic-regression CI.

## Formal Gate rule
W5 is complete only when the exact GitHub branch passes mandatory source parsing, conceptual-registry coverage, RDF serialization equivalence, deterministic canonical build, SHACL smoke validation, OWL 2 DL profile validation and ROBOT/HermiT logical validation. The canonical graph fingerprint must be frozen after the bootstrap run and the gate rerun against that frozen baseline.

## Methodological boundaries
- W5 formalizes W4; it does not reopen evidence-driven concept discovery.
- A formal PASS does not prove domain completeness or empirical correctness.
- Mapping hints do not imply full standards conformance.
- H1–H3 remain held out.
- `https://w3id.org/cm-pharme/2.0/` is the selected target namespace; redirect registration remains pending until separately completed.
