# CM-PharmE Release Readiness

## Post-closure engineering status

The repository modernization and semantic-engineering cycle through **B6** is integrated into `main` while preserving the stable semantic baseline `v1.0.0`.

The earlier B0–B5 closure established historical preservation, normalized knowledge-model artifacts, formal ontology source, evaluation evidence and deterministic build/CI. The subsequent B6 completion wave extended that engineering baseline with additional semantic formats, executable SHACL, negative competency regressions, formal-view checks, explicit OWL profile assessment, expanded deterministic packaging and consolidated engineering documentation.

B6 integration evidence:

- merge commit on `main`: `935a56e788930d449d998464ae2caf8824eba38c`
- final pull-request CI run before merge: `32161058369`
- pull-request workflow conclusion: **success**
- stable semantic version after merge: **unchanged — `v1.0.0`**

The ontology workflow is configured to execute on relevant pushes to `main`; engineering integration is therefore kept under the same automated validation contract after merge.

## Current release-decision gates

| Gate | Current status | Interpretation |
|---|---|---|
| Historical v1.0.0 preservation | PASS | Immutable historical release artifacts retained |
| Stable IDs / lifecycle / traceability | PASS | 39 concepts, 40 relation records, 5 domains |
| Formal ontology source | PASS | Modular Turtle authoring source established |
| Canonical graph parity | PASS | 1,086-triple reference graph reconstructable |
| OWL qualified restrictions | PASS | 42 qualified cardinality restrictions represented |
| SHACL generation | PASS | 574 triples; 76 NodeShapes + 76 PropertyShapes |
| Executed SHACL validation | PASS — bounded finding profile | Two Violations + one Warning reproduced intentionally on the vaccine sample |
| Structural validation | PASS | 28/28 structural and traceability checks |
| Positive competency-query regression | PASS — bounded | Eight executable queries meet registered expectations |
| Negative competency-query regression | PASS — bounded | Four absence queries return the expected zero rows |
| RDF-compatible distributions | PASS | Canonical graph preserved across generated RDF views |
| Extended formats | PASS | Compacted JSON-LD/context, TriG and N-Quads generated deterministically |
| Manchester / OWL Functional views | PASS with documented normalization boundary | Generated deterministically and compared at OWL axiom level |
| OWL profile assessment | MEASURED | Current v1 canonical serialization is not claimed fully OWL 2 DL-profile conformant |
| Logical reasoning | PASS | ROBOT/HermiT completes successfully for the current axiom set |
| Deterministic dual build | PASS | Independent generated builds must be byte-identical |
| Deterministic release bundle | PASS | Fixed-order/fixed-time package with SHA-256 evidence |
| Semantic engineering B6 | INTEGRATED | Merged to `main` after successful full PR CI |
| Open semantic findings | OPEN | Three refinement candidates + one domain-evidence deferral |
| Independent expert/domain replication | PARTIAL | Publication evidence exists; broader replication remains future research |
| License policy | OPEN — owner decision required | Must be selected explicitly before a formal public release policy is finalized |
| `w3id.org` redirect deployment | OPEN | IRI policy exists; redirect registration is external administrative work |
| New semantic version/tag | NOT YET | Must follow intentional semantic evolution, not engineering automation |

## Formal findings deliberately preserved

### SHACL

The constructed vaccine scenario does not fully conform to the complete generated SHACL constraint set. The validator reproducibly identifies three registered findings: two Violations and one Warning. These are preserved as evidence and future refinement inputs rather than removed solely to obtain a cosmetically green conformance result.

### OWL 2 DL profile

ROBOT/OWLAPI profile assessment is executed explicitly. The current v1 canonical RDF serialization is not described as fully OWL 2 DL-profile conformant; formalization-hygiene findings around declaration/signature treatment are recorded separately from logical consistency. HermiT reasoning nevertheless succeeds for the current axiom set.

These two results illustrate the repository's evidence policy: validation outcomes are reported according to what each technique actually establishes.

## Closure definition and outcome

The repository has now completed the intended v1 engineering modernization scope: the stable semantic model can be reconstructed, validated through multiple complementary gates, serialized into multiple consumer formats and packaged reproducibly from authoritative source.

The following work is deliberately outside this completed v1 engineering cycle and belongs to subsequent governance or research cycles:

- semantic refinement and CM-PharmE v2 design;
- new concept discovery and domain-extension decisions;
- independent DOI-backed datasets and empirical evaluation;
- ontology-to-relational mapping and relational database implementation;
- knowledge graph and application/observatory layers;
- additional cross-dataset or cross-jurisdiction validation;
- persistent IRI deployment;
- licensing and publication-administration decisions;
- any intentional new semantic version or tag.

License selection and `w3id.org` registration are governance follow-ups and do not reopen the completed v1 engineering/modeling cycle.
