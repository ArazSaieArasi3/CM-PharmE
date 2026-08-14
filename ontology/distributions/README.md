# Generated Ontology Distributions

This directory is reserved for generated full-ontology serializations derived from the authoritative modular B3 source under `ontology/source/modules/` plus the relation-cardinality registry under `mappings/cardinality/`.

The B3 local reference build successfully produced and structurally validated:

- `cm-pharme.owl` — OWL/RDF/XML
- `cm-pharme.rdf` — RDF/XML
- `cm-pharme.jsonld` — JSON-LD
- `cm-pharme.nt` — N-Triples
- canonical consolidated Turtle
- SHACL shapes

The locally validated artifact hashes are recorded in [`../validation/B3_ARTIFACT_SHA256SUMS.txt`](../validation/B3_ARTIFACT_SHA256SUMS.txt).

## Source-of-truth rule

These distribution files are **generated artifacts**, not independent manual sources of truth. B3 establishes the modular authoring source and validated reference package; automated GitHub rebuild/materialization of the complete distributions is deferred to the B5 build/CI workflow so that serializations cannot drift from the canonical source.

Until that automated pipeline is installed, consumers should treat `ontology/source/modules/`, `mappings/cardinality/`, the IRI policy, and the B3 validation/audit records as the GitHub-authoritative B3 engineering source.
