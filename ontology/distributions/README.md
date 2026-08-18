# Generated Ontology Distributions

CM-PharmE ontology distributions are **generated artifacts**, not independent authoring sources. The authoritative source is the modular Turtle under [`../source/modules/`](../source/modules/).

## Generated formats

The reproducible semantic pipeline produces:

- `cm-pharme.ttl` — consolidated Turtle
- `cm-pharme.owl` — deterministic RDF/XML / OWL
- `cm-pharme.rdf` — deterministic RDF/XML
- `cm-pharme.jsonld` — deterministic expanded JSON-LD
- `cm-pharme.compact.jsonld` — deterministic compacted JSON-LD
- `cm-pharme.context.json` — application-facing JSON-LD context
- `cm-pharme.nt` — canonical sorted N-Triples
- `cm-pharme.trig` — dataset-capable TriG view using the default graph
- `cm-pharme.nq` — dataset-capable N-Quads view using the default graph
- `cm-pharme.omn` — Manchester Syntax generated through ROBOT/OWLAPI
- `cm-pharme.ofn` — OWL Functional Syntax generated through ROBOT/OWLAPI
- SHACL at `shapes/cm-pharme.shacl.ttl`

RDF-compatible generated views are checked for graph equivalence with the canonical 1,086-triple graph. Manchester and Functional Syntax are generated twice for byte reproducibility and compared against the source at the OWL axiom level. OWLAPI may materialize explicit Declaration axioms in those human/formal views; CI permits declaration-only normalization but fails on removed axioms or added non-Declaration axioms.

## Publication model

Generated files are **not hand-maintained in Git**. GitHub Actions performs clean builds, validates graph equivalence and reference fingerprints, executes SHACL/CQ/logical checks, requires independent builds to be byte-identical, and uploads the generated distributions plus validation evidence as a CI artifact. The deterministic bundle is suitable for a future governed GitHub Release after release governance is approved.

This keeps one source of truth while making every consumer format reproducible and traceable.
