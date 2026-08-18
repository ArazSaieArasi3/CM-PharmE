# Repository Engineering

CM-PharmE treats repository engineering as part of research reproducibility. The conceptual model and ontology remain research artifacts; build, validation and release automation exist to ensure that derived files can be reconstructed from the authoritative source without manual drift.

## Current engineering documents

- [Semantic Engineering Completion](SEMANTIC_ENGINEERING_COMPLETION.md) — current integrated state of formats, validation, regression testing, formal findings and closure boundaries.
- [Ontology Formats](FORMATS.md) — Turtle, RDF/XML/OWL, RDF/XML, expanded/compacted JSON-LD, JSON-LD context, N-Triples, TriG, N-Quads, Manchester Syntax, OWL Functional Syntax and SHACL usage/equivalence rules.
- [Validation Architecture](VALIDATION.md) — layered structural, SHACL, positive/negative competency-query, OWL profile and HermiT reasoning gates.
- [Reproducible Build](BUILD.md) — source-of-truth rule, local build sequence, dual-build reproducibility contract and generated-artifact policy.
- [Reproducible Ontology Build and CI](b5-reproducible-build.md) — historical B5 deterministic source assembly, checksums, query regression and reasoner architecture.
- [Final CI Audit](b5-ci-audit.md) — evidence from the earlier repository-engineering closure.
- [Release Readiness](release-readiness.md) — current closure state plus remaining semantic-release and administrative decisions.

## Current engineering state

The latest semantic-engineering completion wave has been merged into `main` while preserving the stable semantic baseline `v1.0.0`.

The current pipeline provides:

- deterministic reconstruction of the 1,086-triple canonical ontology graph;
- deterministic core and extended RDF/OWL distribution generation;
- compact JSON-LD/context, TriG and N-Quads application/data views;
- Manchester and OWL Functional Syntax generation through ROBOT/OWLAPI;
- graph-equivalence and formal-view axiom-diff checks;
- generated SHACL plus executed SHACL validation against registered bounded findings;
- eight positive and four negative executable competency-query regressions;
- ROBOT ontology metrics and explicit OWL 2 DL profile assessment;
- ROBOT/HermiT logical reasoning;
- independent-build byte-reproducibility and deterministic semantic package generation;
- CI artifact publication and SHA-256 integrity evidence.

## Evidence boundary

Engineering PASS results are intentionally separated from semantic and empirical validity. The current vaccine scenario reproduces three registered SHACL findings, and the current v1 canonical serialization is not overclaimed as fully OWL 2 DL-profile conformant. HermiT logical reasoning succeeds for the current axiom set, but this does not establish universal domain completeness, external standards conformance, deployed effectiveness or correctness of every modeling decision.

The stable semantic baseline remains `v1.0.0`; repository engineering alone does not create a new semantic version.
