# CM-PharmE Semantic Engineering Completion

## Scope

This document records the completed post-paper repository-engineering wave for the current CM-PharmE 1.0 semantic baseline. It strengthens formats, validation, regression testing, reproducibility, and documentation without declaring a new semantic model version.

The authoritative ontology source remains the modular Turtle under `ontology/source/modules/`. Generated files are reproducible views and must not be edited independently.

## Closure status

B6 is **integrated into `main`**. The final B6 pull-request CI completed successfully before merge and exercised the complete semantic-engineering workflow: deterministic dual builds, extended-format generation, structural validation, executable SHACL, positive and negative CQs, ROBOT format generation, formal-view axiom comparison, ontology metrics/profile assessment, HermiT reasoning, deterministic release packaging, and reasoner enforcement.

Integration evidence:

- B6 merge commit on `main`: `935a56e788930d449d998464ae2caf8824eba38c`
- final full B6 pull-request CI run: `32161058369`
- workflow conclusion: **success**
- stable semantic baseline after integration: **unchanged — `v1.0.0`**

The public homepage and engineering documentation were subsequently refreshed and merged through PR #7 so that the repository entry point reflects the integrated B6 state. This documentation-only follow-up introduced no semantic ontology change.

## Completion dashboard

| Gate | Evidence | Current result |
|---|---|---|
| Canonical source integrity | 1,086-triple canonical graph and pinned fingerprint | **PASS** |
| Core RDF/OWL distributions | TTL, OWL/RDF-XML, RDF/XML, expanded JSON-LD, N-Triples | **PASS** |
| Extended data formats | compact JSON-LD + context, TriG, N-Quads | **PASS**; graph-equivalent to canonical source |
| Human/formal OWL views | Manchester and OWL Functional Syntax via ROBOT | **PASS**; deterministic generation and axiom-level comparison |
| Formal-view normalization | ROBOT/OWLAPI diff | **PASS with explicit declaration-only normalization**; no removed axioms or added non-Declaration axioms |
| SHACL generation | 574 triples, 76 NodeShapes, 76 PropertyShapes | **PASS** |
| SHACL execution | pySHACL over the vaccine sample | **PASS for registered finding profile**; sample itself does not fully conform |
| SHACL findings | two Violations + one Warning | **REPRODUCED** and intentionally retained |
| Positive competency regression | 8 executable SPARQL CQs | **8/8 PASS** |
| Negative competency regression | 4 explicit absence queries | **4/4 PASS** with zero rows |
| Structural regression | graph fingerprint, counts, lifecycle and cleanup checks | **PASS** |
| OWL profile assessment | ROBOT `validate-profile --profile DL` + metrics | **MEASURED**; canonical v1 source is not claimed OWL 2 DL-profile conformant |
| Logical reasoning | ROBOT + HermiT | **PASS**; exit code 0 |
| Deterministic builds | two clean RDF builds + formal-syntax output comparison | **PASS** |
| Deterministic package | fixed-order/fixed-time release ZIP + SHA-256 | **PASS** |
| Semantic engineering B6 | merged to `main` | **INTEGRATED / CLOSED** |
| Repository boundary | no semantic-release/tag change in this wave | **PRESERVED** |

## Important formal findings preserved for future model evolution

### SHACL sample findings

The full generated shape set identifies three findings in the constructed vaccine scenario:

1. `ecosystemRelationship` has more than one inverse value for `CMPE-R0007` — Violation.
2. `ecosystemRelationship` has fewer than one value for `CMPE-R0036` — Violation.
3. `supplyChainRelationship` has fewer than two values for `CMPE-R0024` — Warning.

These are not hidden or cosmetically repaired. They are retained as bounded evidence and as inputs for later semantic/data refinement.

### OWL 2 DL profile assessment

ROBOT/OWLAPI reports that the canonical CM-PharmE 1.0 RDF source is not fully within the OWL 2 DL profile as currently serialized. The profile report identifies formalization-hygiene issues involving declaration expectations for annotation/external vocabulary resources and related OWLAPI signature treatment. This is distinct from logical inconsistency: HermiT still completes successfully with exit code 0 for the current axiom set.

The B6 wave deliberately does not mutate the validated v1 canonical graph only to make the profile report green. A DL-normalized formal view or explicit declaration strategy belongs to a governed future formalization/evolution decision rather than this closed v1 engineering wave.

## Important evidence boundary

The repository distinguishes engineering validity from semantic and empirical validity. Syntax, graph equivalence, deterministic builds, SHACL execution, query regression, and logical reasoning strengthen reproducibility and formal traceability. They do not establish domain completeness, standards conformance, implementation effectiveness, or independent empirical validity. Open ontological findings remain visible and belong to later semantic evolution rather than being edited away to make automated checks pass.

## Main implemented code

- `tools/ontology/build.py` — deterministic canonical ontology build and core distributions.
- `tools/ontology/extend_formats.py` — compact JSON-LD/context, TriG, and N-Quads generation plus equivalence checks.
- `tools/ontology/validate.py` — canonical structural/fingerprint quality gates.
- `tools/ontology/validate_shacl.py` — executed SHACL validation with registered expected findings.
- `tools/ontology/run_cqs.py` — positive and negative competency-query regression runner.
- `tools/ontology/semantic_diff.py` — canonical RDF graph comparison utility.
- `tools/ontology/check_robot_diff.py` — guarded OWL axiom-level comparison allowing only declaration-only OWLAPI normalization.
- `tools/ontology/package_release.py` — deterministic expanded semantic release bundle.
- `.github/workflows/ontology-reasoner.yml` — CI orchestration, ROBOT conversions/profile/metrics, HermiT reasoning, regression checks, and artifact publication.

## Closure outcome

The intended CM-PharmE 1.0 repository-engineering scope is complete: the stable semantic source can be reconstructed, serialized into multiple consumer formats, assessed through complementary automated gates, and packaged reproducibly. The stable semantic baseline remains `v1.0.0`.

Persistent IRI deployment, licensing, new datasets, new semantic concepts/relations, relational/KG application layers, and any future semantic release remain separate governance or research cycles and do not reopen this completed v1 engineering closure.
