# Evaluation Method

## Evaluation philosophy

CM-PharmE evaluation is evidence-layered rather than score-driven. Different procedures test different claims and have different evidential strength. Results are therefore reported criterion by criterion, with explicit boundaries, instead of being collapsed into a single composite validation score.

The later journal manuscript operationalizes five qualitative evaluation criteria:

1. Syntactic and Structural Correctness
2. Semantic and Conceptual Accuracy
3. Conceptual Clarity
4. Adaptability and Modifiability
5. Pragmatic Value

The repository extends those criteria into a broader E1–E9 evidence architecture so that future computational and empirical evidence can be added without rewriting the research history.

## Mapping from publication criteria to repository evaluation layers

| Publication criterion | Main repository layers | Repository interpretation |
|---|---|---|
| Syntactic and Structural Correctness | E1 Syntax, E2 Logic, E3 Structure, E4 Ontology | Parsing, referential integrity, logical consistency, stereotypes, relations, cardinalities, anti-patterns |
| Semantic and Conceptual Accuracy | E4 Ontology, E5 Semantic, E7 Competency Questions | Domain meaning, expert evidence, explicit answerability and traceability |
| Conceptual Clarity | E3 Structure, E5 Semantic, E8 Application | Terminology, definitions, interpretability, stakeholder-facing use |
| Adaptability and Modifiability | E6 Data/Mapping, E7 CQ, E8 Application | Scenario instantiation, extensions, mappings, controlled context changes |
| Pragmatic Value | E6 Data/Mapping, E8 Application, E9 Reproducibility | Governance, requirements, architecture, downstream use and repeatability |

## E1 — Syntax validation

Checks whether formal ontology and supporting machine-readable artifacts parse correctly and use valid syntax. Evidence should record the exact tool, version, command, input artifact, and result.

## E2 — Logical validation

Checks logical consistency, unsatisfiable classes, and reasoner-relevant consequences using explicit OWL reasoning tooling. B3 does not claim completion of this layer. B4/B5 must record exact HermiT/ELK/ROBOT or equivalent evidence before a full consistency claim is made.

## E3 — Structural validation

Checks entity counts, stable identifiers, source/target integrity, cardinality coverage, domain assignments, lifecycle fields, duplicate or dangling records, and consistency across registries, mappings, documentation, and formal source.

## E4 — Ontological validation

Examines whether constructs and relations follow the intended UFO/OntoUML commitments. The historical research used a focused manual inspection of eight categories:

- Type–Role Confusion
- Role without Relator
- Relator without Mediation
- Event as Object
- Mode vs. Attribute Confusion
- Part–Whole Misuse
- Relation as Class
- Overloaded Association

The later manuscript reports no critical issue in the inspected scope, two minor issues, and one low-risk observation. These results are historical manual evidence, not exhaustive computational clearance.

## E5 — Semantic / expert validation

The later manuscript reports a qualitative review by four purposively selected experts covering enterprise/business architecture, health information systems, pharmaceutical operations, and regulatory/governance concerns. The panel was used to identify ambiguity and refinement needs rather than to provide statistical validation.

Repository evidence should preserve:

- expert profile rationale without unnecessary personal identification;
- assessment dimension;
- documented observation;
- author decision;
- revision/response;
- effect on the core model;
- evidence status and version.

## E6 — Data and mapping validation

Representative instances and external mappings are used to test whether the ontology can be instantiated and connected to real or realistic ecosystem data without semantic contradiction. This layer should distinguish conceptual mapping from standards conformance.

## E7 — Competency questions

The journal manuscript defines eight competency questions. CQ1–CQ5 address domain-specific coverage, CQ6 cross-domain business-architecture/UFO alignment, and CQ7–CQ8 prospective reference-architecture use and contextual extension.

The manuscript assessment is traceability-based rather than executable. B4 records the questions as versioned requirements and targets SPARQL-based execution against representative data where feasible.

Results use bounded categories such as:

- `addressed`
- `addressed-conceptually`
- `partially-addressed`
- `not-addressed`
- `executable-pass`
- `executable-fail`

## E8 — Application validation

Scenarios and downstream analytical tasks test whether the model can support intended use. The vaccine-distribution instantiation is retained as the first reference scenario. It demonstrates representational plausibility but is not operational deployment evidence.

Future application evidence may cover governance analysis, requirements derivation, architecture interpretation, standards mapping, knowledge-graph use, or controlled context extensions.

## E9 — Research reproducibility

Checks whether another researcher or maintainer can reconstruct the relevant model state, evaluation inputs, commands, evidence, outputs, and publication association from the repository.

Reproducibility evidence includes:

- stable release/commit references;
- frozen registries and mappings;
- evaluation-plan version;
- tool and dependency versions;
- machine-readable result files;
- scenario and CQ identifiers;
- publication-to-evidence traceability.

## Publication-derived evaluation procedures

The two publications provide five complementary assessment procedures that are preserved as provenance:

1. scenario-based comparative benchmark;
2. qualitative expert review;
3. focused manual OntoUML-informed anti-pattern inspection;
4. competency-question assessment;
5. illustrative vaccine-distribution instantiation.

The published conference paper also contains stronger early claims concerning clarity, customization, and pragmatic actionability. Those claims remain recorded as publication evidence but are not silently treated as current repository-verified results.

## Evidence-strength rule

Every evaluation result should state:

- claim being tested;
- indicator;
- evidence source;
- procedure;
- result;
- limitation/evidential boundary;
- model version or commit;
- reproducibility status.

A result must not be generalized beyond the procedure that produced it. In particular, manual anti-pattern review is not equivalent to reasoner validation, a constructed scenario is not empirical deployment, and conceptual standards mapping is not implementation conformance.