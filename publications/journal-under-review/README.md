# Publication Record — Journal Manuscript Under Review

## Title

**CM-PharmE 1.0: A Business-Architecture-Informed and Ontology-Grounded Conceptual Model for Pharmaceutical Ecosystems**

## Authors

- Araz Saie Arasi — ORCID: https://orcid.org/0009-0009-6739-5717
- Hassan Haghighi — ORCID: https://orcid.org/0000-0002-6145-4095
- Hossein Azgomi — ORCID: https://orcid.org/0000-0001-7974-1845

## Status

**Journal manuscript — under review.**

The repository does not infer acceptance, publication date, DOI, volume/issue, publisher URL, or indexing metadata before those details are verified.

## Relationship to the published CM-PharmE paper

This manuscript builds on the initial CM-PharmE conceptual foundation reported in the published conference paper while preserving the core five-domain architecture. Its primary contribution relative to the earlier paper is methodological substantiation, stronger evidence-to-domain traceability, refined semantic explanation, comparative positioning, a more explicitly bounded multi-layer assessment, and clearer application and implementation boundaries.

Foundational explanatory material shared with the conference paper is treated as prior work and is condensed or cited rather than presented as a new journal contribution. The journal manuscript retains only the background needed to make the strengthened method, evaluation, and application discussion self-contained.

It should therefore be read as a strengthened research treatment of the CM-PharmE 1.0 conceptual foundation rather than as an automatic declaration of a new semantic model release.

## Research method represented in the repository

The manuscript documents:

- PRISMA-guided systematic review provenance;
- qualitative thematic synthesis;
- evidence-to-domain traceability;
- business-architecture-informed concern identification;
- UFO/OntoUML concept-classification and relation-selection procedure;
- conceptual cardinality rationale;
- DSRM-oriented research framing;
- version-controlled repository support for reproducibility.

Reusable repository documentation is maintained under [`../../docs/methodology/`](../../docs/methodology/).

## Evaluation represented in the repository and manuscript

The manuscript combines:

- a scenario-based comparative benchmark;
- qualitative review by four experts;
- focused manual inspection of eight selected OntoUML-informed anti-pattern categories;
- eight competency questions, operationalized as executable repository queries;
- an illustrative vaccine-distribution instantiation;
- repository-supported structural, mapping, logical and reproducibility checks;
- ROBOT/HermiT logical validation of the current axiom set.

For transparent synthesis, the final major-revision manuscript now explicitly reports the repository-supported evidence as a **nine-layer evaluation architecture (E1–E9)**:

| Layer | Focus | Current status |
|---|---|---|
| E1 | Syntax validation | PASS |
| E2 | Logical consistency | PASS |
| E3 | Structural integrity | PASS — 28/28 checks |
| E4 | Ontological soundness | CONDITIONAL |
| E5 | Semantic / expert evidence | PARTIAL |
| E6 | Data / mapping validation | PASS — bounded |
| E7 | Competency questions | PASS — 8/8 bounded outcomes |
| E8 | Application evidence | PARTIAL / illustrative |
| E9 | Reproducibility | PASS |

The formal/repository evidence includes the complete 1,086-triple canonical graph, deterministic generated serializations, a 574-triple SHACL graph with 76 NodeShapes and 76 PropertyShapes, 39 concept classes, 39 OWL object properties plus one generalization record, five domains, 42 qualified OWL cardinality restrictions, a machine-readable vaccine sample, executable competency-query regression checks, ROBOT/HermiT reasoning, graph fingerprints, checksums, repeated clean builds and a deterministic release bundle.

These layers are **not** treated as nine statistically independent validation studies. Several layers reuse the same formal model, scenario and repository evidence. The explicit statuses preserve the evidential boundary: formal/computational PASS results do not convert the conditional ontological findings, limited expert evidence, or illustrative application evidence into stronger claims.

The executable-query and reasoner evidence supports bounded computational traceability, reproducibility and logical consistency for the current formalized model and scenario; it does not establish empirical effectiveness, universal domain completeness, standards conformance, operational interoperability, independent external validation, or correctness of every ontological commitment. The repository integrates the evaluation procedures into versioned and executable evidence under [`../../evaluation/`](../../evaluation/) and [`../../docs/evaluations/`](../../docs/evaluations/).

## Model association

- Stable semantic baseline: `v1.0.0`
- Formal ontology engineering: B3 formalization integrated into `main`
- Evaluation evidence: B4/B4.10 paper-grounded validation and logical reasoning integrated into `main`
- Reproducible build and CI: B5 engineering integrated into `main`

A manuscript revision does not itself create a new semantic model version. Version assignment follows explicit semantic changes and repository versioning policy.

## Repository/publication boundary

The repository summarizes the problem, design rationale, method, evidence, evaluation, applications, and limitations needed to understand and reproduce the artifact. The manuscript remains the scholarly source for the complete research narrative, literature synthesis, tables, discussion, and publication-specific argument.