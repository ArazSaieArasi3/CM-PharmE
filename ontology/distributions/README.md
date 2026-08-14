# Generated Ontology Distributions

CM-PharmE ontology distributions are **generated artifacts**, not independent authoring sources. The authoritative source is the modular Turtle under [`../source/modules/`](../source/modules/).

## Generated formats

The B5 pipeline deterministically produces:

- `cm-pharme.ttl` — consolidated Turtle
- `cm-pharme.owl` — deterministic RDF/XML / OWL
- `cm-pharme.rdf` — deterministic RDF/XML
- `cm-pharme.jsonld` — deterministic expanded JSON-LD
- `cm-pharme.nt` — canonical sorted N-Triples
- SHACL at `shapes/cm-pharme.shacl.ttl`

## Publication model

Generated files are **not hand-maintained in Git**. GitHub Actions performs clean builds, validates graph equivalence and reference fingerprints, requires two independent builds to be byte-identical, and uploads the generated distributions plus validation evidence as a CI artifact. The same deterministic bundle is the input for a future GitHub Release after release governance is approved.

This keeps one source of truth while making every consumer format reproducible.
