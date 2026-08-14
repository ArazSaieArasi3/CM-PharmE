# B5 — Reproducible Ontology Build and CI

## Objective

B5 converts the B3/B4 ontology engineering and evaluation work into a reproducible repository pipeline. The authoritative authoring source remains the modular Turtle under `ontology/source/modules/`; consolidated ontology files, serializations, SHACL and release bundles are generated artifacts.

## Source-of-truth rule

**Author manually:** `ontology/source/modules/**/*.ttl`

**Generate, do not independently edit:**

- consolidated `cm-pharme.ttl`
- `cm-pharme.owl`
- `cm-pharme.rdf`
- `cm-pharme.jsonld`
- `cm-pharme.nt`
- `cm-pharme.shacl.ttl`
- build/checksum manifests

The cardinality registry and research/evaluation registries remain authoritative inputs/evidence; B5 does not reinterpret the open semantic findings from B4.10.

## Full B3 parity closure

B4.10 established that the 888-triple GitHub modular source and the 1,086-triple B3 reference package had identical logical axioms but incomplete annotation/provenance parity. B5 closes that engineering gap.

The modular source now reconstructs the full B3 reference graph:

- ontology triples: **1,086**
- canonical graph SHA-256: `cc823a8aff4d7e7818f8470f2dbad6ca8045ff92e5637fbf3503bc105170a83f`
- SHACL triples: **574**
- SHACL node shapes: **76**
- SHACL property shapes: **76**
- SHACL canonical graph SHA-256: `2a79cc94a2118a0f6f6edb6eb3b72ed9ad20f278ebda60e9e258b0e3d0a9e893`

The parity restoration adds missing B3 annotation/provenance statements and restores nine annotation values to the validated reference wording. It does **not** change the logical axiom set or resolve the three model-refinement candidates identified in B4.10.

## Deterministic build

`tools/ontology/build.py`:

1. recursively reads all Turtle authoring modules;
2. unions and canonicalizes the RDF graph;
3. generates consolidated Turtle;
4. generates deterministic RDF/XML, JSON-LD and N-Triples distributions;
5. derives SHACL cardinality shapes from active relation metadata;
6. writes a build manifest and SHA-256 file.

The build is pinned to Python 3.12 and RDFLib 7.5.0 in CI. RDF/XML and expanded JSON-LD are serialized through deterministic repository code rather than relying on nondeterministic iteration order from generic serializers.

## Quality gates

The B5 validation pipeline checks:

- exact B3 graph fingerprint and triple count;
- exact B3 SHACL graph fingerprint;
- 39 concept classes;
- 39 OWL object properties plus one generalization record;
- five domains;
- 42 OWL qualified restrictions;
- 76 SHACL node shapes and 76 property shapes;
- distribution graph equivalence;
- artifact checksums;
- byte-for-byte agreement between two independent clean builds;
- preservation of the R0011→R0027 lifecycle repair;
- R0031 label normalization;
- C0025 canonical Relator treatment;
- absence of historical `example.org` / converter cardinality artifacts;
- eight executable competency-question regression assertions;
- ROBOT/HermiT logical validation.

## CI behavior

`.github/workflows/ontology-reasoner.yml` runs for relevant Pull Requests, pushes to `main`, the B5 branch, and manual dispatch. It creates an evidence artifact containing the fresh build, quality reports, reasoner output and deterministic release bundle.

CI is a reproducibility and regression gate. It does not establish domain completeness, empirical usefulness, standards conformance, or resolve open ontological-semantic findings.

## Release bundle

`tools/ontology/package_release.py` creates a byte-deterministic ZIP with fixed file timestamps and ordering. CI builds it twice and requires the two bundles to be byte-identical before publishing the workflow artifact.

A GitHub Release or new semantic tag is intentionally **not** created by B5. Semantic version assignment remains a separate research/model-evolution decision.
