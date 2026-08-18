# CM-PharmE Semantic Engineering Completion

## Scope

This document closes the post-paper repository-engineering wave for the current CM-PharmE 1.0 semantic baseline. It strengthens formats, validation, regression testing, reproducibility, and documentation without declaring a new semantic model version.

The authoritative ontology source remains the modular Turtle under `ontology/source/modules/`. Generated files are reproducible views and must not be edited independently.

## Completion dashboard

| Gate | Evidence | Status / interpretation |
|---|---|---|
| Canonical source integrity | 1,086-triple canonical graph and pinned fingerprint | PASS |
| RDF/OWL distributions | TTL, OWL/RDF-XML, RDF/XML, JSON-LD, N-Triples | PASS |
| Extended data formats | compact JSON-LD + context, TriG, N-Quads | PASS when graph-equivalence checks succeed |
| Human/formal OWL views | Manchester and OWL Functional Syntax via ROBOT | Generated and round-trip checked in CI |
| SHACL generation | 574 triples, 76 NodeShapes, 76 PropertyShapes | PASS |
| SHACL execution | pySHACL over the vaccine sample | Executed against a registered bounded finding profile; conformance itself is not forced |
| Positive competency regression | 8 executable SPARQL CQs | PASS when all predefined outcomes are met |
| Negative competency regression | 4 explicit absence queries | PASS when all remain empty |
| Structural regression | graph fingerprint, counts, lifecycle and cleanup checks | PASS |
| OWL profile assessment | ROBOT `validate-profile --profile DL` + metrics | Measured and reported; profile result is not silently upgraded |
| Logical reasoning | ROBOT + HermiT | PASS when reasoner exit code is 0 |
| Deterministic builds | two clean RDF builds + formal-syntax output comparison | Required by CI |
| Deterministic package | fixed-order/fixed-time release ZIP + SHA-256 | Required by CI |
| Repository boundary | no semantic-release/tag change in this wave | Preserved |

## Important evidence boundary

The repository distinguishes engineering validity from semantic and empirical validity. Syntax, graph equivalence, deterministic builds, SHACL execution, query regression, and logical reasoning strengthen reproducibility and formal traceability. They do not establish domain completeness, standards conformance, implementation effectiveness, or independent empirical validity. Open ontological findings remain visible and belong to later semantic evolution rather than being edited away to make automated checks pass.

## Main implemented code

- `tools/ontology/build.py` — deterministic canonical ontology build and core distributions.
- `tools/ontology/extend_formats.py` — compact JSON-LD/context, TriG, and N-Quads generation plus equivalence checks.
- `tools/ontology/validate.py` — canonical structural/fingerprint quality gates.
- `tools/ontology/validate_shacl.py` — executed SHACL validation with registered expected findings.
- `tools/ontology/run_cqs.py` — positive and negative competency-query regression runner.
- `tools/ontology/semantic_diff.py` — canonical RDF graph comparison utility.
- `tools/ontology/package_release.py` — deterministic release bundle.
- `.github/workflows/ontology-reasoner.yml` — CI orchestration, ROBOT conversions/profile/metrics, HermiT reasoning, regression checks, and artifact publication.

## Closure rule

This engineering wave is complete when the pull-request CI passes, the branch is merged into `main`, and the post-merge CI run also succeeds. Semantic changes, persistent IRI deployment, licensing, new datasets, and a new model version remain separate decision cycles.
