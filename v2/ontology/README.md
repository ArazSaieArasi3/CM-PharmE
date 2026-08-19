# CM-PharmE 2.0 Formal Ontology

Status: **W5 formalization candidate; Formal Gate not yet approved.**

## Authoritative source
`source/modules/*.ttl` is the controlled semantic source. Generated OWL/RDF distributions are build artifacts and must not be edited independently.

## Conceptual baseline
The formal ontology implements the Gate-D-approved UFO/OntoUML baseline recorded in `v2/research/w4/`. The companion machine-readable registry is `v2/ontouml/cm-pharme-v2.conceptual-model.json`. That JSON is a project-native deterministic representation, **not** an official OntoUML JSON export or an automated-tool validation result.

## Current formal inventory target
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

## Validation
`tools/v2_ontology/build_validate.py` builds deterministic canonical N-Triples, creates Turtle/RDF/XML/OWL/JSON-LD distributions, verifies graph equivalence, checks the Gate-D registry, checks protected disjointness and executes the SHACL smoke profile. GitHub Actions adds OWL 2 DL profile validation and ROBOT/HermiT reasoning.

## Important boundaries
Formal validation does not establish domain completeness, empirical correctness, organizational adoption, external-standard conformance or the quality of future instance data. H1–H3 remain protected for W7 external/generalizability evaluation.
