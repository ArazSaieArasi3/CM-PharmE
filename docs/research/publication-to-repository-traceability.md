# Publication-to-Repository Traceability

CM-PharmE has evolved through a published conference paper and a later journal manuscript under review. The repository preserves that lineage while keeping the artifact narrative separate from manuscript narrative.

## Publication lineage

### Published conference paper
**CM-PharmE ver.1: Towards a Conceptual Model for Pharmaceutical Ecosystem with a Business-Architecture Perspective**

This paper introduced the five-domain conceptual model and reported an initial qualitative evaluation across structural correctness, semantic accuracy, conceptual clarity, adaptability, and pragmatic value.

### Journal manuscript under review
**CM-PharmE 1.0: A Business-Architecture-Informed and Ontology-Grounded Conceptual Model for Pharmaceutical Ecosystems**

This manuscript preserves the five-domain architecture while strengthening methodological traceability, comparative positioning, concept/relation-selection rationale, expert review, focused anti-pattern inspection, competency questions, and illustrative scenario assessment.

## Evidence rule

Publications report research at a point in time; the repository records the evolving artifact and the current evidence state. Historical publication claims are not silently converted into current repository verification results.

| Topic | Earlier publication | Later manuscript | Repository treatment |
|---|---|---|---|
| Structural validation | Stronger validation wording | Focused manual inspection with explicit limits | Historical claim preserved; reproducible checks remain a B4/B5 target |
| Conceptual clarity | Reports an 8/10 user result | Qualitative interpretability; no standardized usability scale | Mark the earlier result as publication-reported and not yet repository-reproduced |
| Adaptability | Reports easy customization | One illustrative vaccine-distribution instantiation | Treat as illustrative evidence, not an experimental extension result |
| Pragmatic value | Reports participant actionability | Describes plausible application pathways without adoption evidence | Current repository wording follows the bounded interpretation |
| Competency questions | Limited formal role | Eight traceability-based CQs, not executable | B4 records them and targets executable queries |

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