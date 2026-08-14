# Publication-to-Repository Traceability

CM-PharmE has evolved through a published conference paper and a later journal manuscript under review. The repository preserves that lineage while keeping the artifact narrative separate from manuscript narrative.

## Publication lineage

### Published conference paper
**CM-PharmE ver.1: Towards a Conceptual Model for Pharmaceutical Ecosystem with a Business-Architecture Perspective**

[IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/11301544/)

This paper introduced the five-domain conceptual model and reported an initial qualitative evaluation across structural correctness, semantic accuracy, conceptual clarity, adaptability, and pragmatic value.

### Journal manuscript under review
**CM-PharmE 1.0: A Business-Architecture-Informed and Ontology-Grounded Conceptual Model for Pharmaceutical Ecosystems**

This manuscript preserves the five-domain architecture while strengthening methodological traceability, comparative positioning, concept/relation-selection rationale, expert review, focused anti-pattern inspection, competency questions, and illustrative scenario assessment.

## Evidence rule

Publications report research at a point in time; the repository records the evolving artifact and the current evidence state. Historical publication claims are not silently converted into current repository verification results.

| Topic | Earlier publication | Later manuscript | Current repository treatment |
|---|---|---|---|
| Structural validation | Stronger validation wording | Focused manual inspection with explicit limits | Historical claim preserved; **28/28** repository structural/traceability checks are now executable and recorded |
| Conceptual clarity | Reports an 8/10 user result | Qualitative interpretability; no standardized usability scale | Earlier result remains publication-reported; no new standardized usability study is claimed |
| Adaptability | Reports easy customization | One illustrative vaccine-distribution instantiation | Machine-readable vaccine scenario is executable evidence, but remains illustrative rather than an experimental multi-context extension study |
| Pragmatic value | Reports participant actionability | Describes plausible application pathways without adoption evidence | Repository documents application pathways while retaining the no-adoption/no-effectiveness boundary |
| Competency questions | Limited formal role | Eight traceability-based CQs | All eight CQs are now implemented as executable SPARQL regression checks with bounded expectations |
| Logical consistency | Not established computationally | Explicitly identified as future computational work | ROBOT/HermiT now executes in CI and passes for the current logical axiom set |
| Reproducibility | Publication-level artifact support | Version-controlled repository emphasis | Deterministic ontology builds, serialization equivalence, SHACL generation, checksums and CI evidence are now repository-executed |

## Evidence statuses

Publication-derived evidence may be marked as:

- `reported-in-published-paper`
- `reported-in-journal-manuscript`
- `repository-provenance-recorded`
- `repository-structurally-verified`
- `repository-computationally-verified`
- `repository-externally-validated`
- `not-yet-reproduced`
- `superseded-or-narrowed`

## Translation rule

Publication content is transferred into the repository only when it supports the problem statement, design method, model rationale, evaluation method/evidence, applications, limitations, evolution, or citation provenance. Long literature-review prose and manuscript-specific rhetoric are not duplicated.

Neither publication automatically creates a new semantic model version. Version assignment follows the repository semantic-diff and lifecycle policies.

See the [Evaluation overview](../evaluations/index.md), [Publication registry](../../publications/README.md), and [Release Readiness](../engineering/release-readiness.md).