# CM-PharmE 2.0 Formal Ontology

Status: **W5 implementation complete; Formal Gate ready for approval.**

## Authoritative source
`source/modules/*.ttl` is the controlled semantic source. Generated OWL/RDF distributions are build artifacts and must not be edited independently.

## Conceptual baseline
The formal ontology implements the Gate-D-approved UFO/OntoUML baseline recorded in `v2/research/w4/`. The companion machine-readable registry is `v2/ontouml/cm-pharme-v2.conceptual-model.json`. That JSON is a project-native deterministic representation, **not** an official OntoUML JSON export or an automated-tool validation result.

## Frozen formal baseline
- formal development version: `2.0.0-alpha.1`;
- canonical graph: **642 triples**;
- SHA-256: `59ef47eeed732290736e60bfa1c6bf43a12d15df2f50cff931badb5938cc954a`;
- 87 Gate-D conceptual types/pattern elements;
- 81 OWL classes;
- 6 declared RDF/OWL datatypes;
- 52 object properties;
- 5 datatype properties.

Raw OWL entity counts are implementation counts and should not be confused with the conceptual-model count.

## Modules
- `00-metadata.ttl` — ontology/version/provenance metadata and foundational annotations.
- `10-core.ttl` — pharmaceutical ecosystem Core.
- `20-xinfra.ttl` — geography/time, evidence/provenance and identifier infrastructure.
- `25-gate-d-disjointness.ttl` — explicit protected conceptual distinctions.
- `30-extensions.ttl` — regulatory, resilience, market-access, risk, safety, BA and application extensions.
- `40-mappings.ttl` — conservative external alignment hints.

## Formal validation result
GitHub Actions run `32215753957` and follow-up workflow-only run `32215753957`/success evidence establish the frozen ontology baseline. The latest workflow implementation also completed successfully after the evidence artifact was reduced to a lean package.

Mandatory checks:
- Turtle parsing — PASS;
- conceptual-registry coverage — PASS;
- eight Gate-D protected distinctions — PASS;
- TTL/RDF/XML/OWL/JSON-LD/N-Triples graph equivalence — PASS;
- deterministic two-pass canonical build — PASS;
- SHACL Meta-SHACL and smoke validation — PASS (11 NodeShapes);
- OWL 2 DL profile via ROBOT/OWLAPI — PASS;
- HermiT logical validation — PASS;
- Manchester and Functional Syntax generation — PASS;
- frozen fingerprint regression — PASS.

`tools/v2_ontology/build_validate.py` performs the repository-native build/regression checks; `.github/workflows/v2-ontology-ci.yml` adds the reasoner/profile gates.

## Namespace status
`https://w3id.org/cm-pharme/2.0/` is the selected target namespace. External w3id redirect registration remains pending and is not represented as deployed infrastructure.

## Important boundaries
Formal validation does not establish domain completeness, empirical correctness, organizational adoption, external-standard conformance or the quality of future instance data. H1–H3 remain protected for W7 external/generalizability evaluation.
