# CM-PharmE Documentation Map

This page is the human-readable map of CM-PharmE. It is intentionally lighter than a website sitemap: the goal is to help reviewers, researchers, ontology specialists, and implementers reach the relevant evidence without navigating the repository tree manually.

## Recommended paths

### Paper reviewer / research reader

1. [Why CM-PharmE Exists](research/rationale.md)
2. [Published CM-PharmE paper on IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/11301544/)
3. [Research and Model Development Method](methodology/research-and-model-development.md)
4. [Model Concepts](concepts/index.md), [Relations](relations/index.md), and [Domains](domains/index.md)
5. [Evaluation](evaluations/index.md)
6. [Repository Engineering and Reproducibility](engineering/index.md)
7. [Publications](../publications/README.md)

### Ontology / conceptual-modeling reader

1. [Formal Ontology](../ontology/README.md)
2. [Concept Registry](concepts/index.md)
3. [Relation Registry](relations/index.md)
4. [UFO/OntoUML modeling method](methodology/research-and-model-development.md#6-ufoontouml-concept-classification)
5. [Official OntoUML Ecosystem References](references/ontouml-ecosystem.md)
6. [Mappings](../mappings/README.md)
7. [Evaluation](evaluations/index.md)

### Reproducibility / engineering reader

1. [Repository Engineering](engineering/index.md)
2. [Formal Ontology](../ontology/README.md)
3. [Evaluation](evaluations/index.md)
4. [Versioning Policy](policies/versioning.md)
5. [Release Readiness](engineering/release-readiness.md)

## Documentation areas

| Area | What you will find |
|---|---|
| [Research](research/rationale.md) | Problem, research gap, artifact narrative, applications, limitations, and publication traceability |
| [Methodology](methodology/index.md) | Evidence review, thematic synthesis, Business Architecture, UFO/OntoUML modeling, and evaluation method |
| [Concepts](concepts/index.md) | 39 canonical concepts with stable IDs and concept pages |
| [Relations](relations/index.md) | 40 stable relation records and relation pages |
| [Domains](domains/index.md) | Five modeling domains and cross-domain coverage |
| [Ontology](../ontology/README.md) | Modular formal ontology, IRI policy, generated serializations, SHACL, and reasoning |
| [Mappings](../mappings/README.md) | Machine-readable traceability and future external/data mappings |
| [Evaluation](evaluations/index.md) | Nine-layer evaluation framework, executable competency questions, scenario evidence, anti-pattern review, and reasoning |
| [Engineering](engineering/index.md) | Deterministic build, CI quality gates, reproducibility, and release readiness |
| [Versions](versions/index.md) | Stable semantic baseline and integrated engineering/evaluation history |
| [Publications](../publications/README.md) | Publisher link, publication records, and publication-to-repository lineage |
| [Applications](research/applications-and-boundaries.md) | Intended uses and explicit non-claims |
| [Architecture](architecture/index.md) | Repository and research-asset architecture notes |

## Machine-readable areas

The human-readable documentation is complemented by structured sources and evidence:

- [`../catalog/`](../catalog/) — concept, relation, and domain registries
- [`../ontology/`](../ontology/) — formal ontology source and validation contracts
- [`../evaluation/`](../evaluation/) — competency questions, scenarios, and machine-readable evidence
- [`../mappings/`](../mappings/) — traceability mappings
- [`../releases/`](../releases/) — immutable historical release snapshots

## Navigation principle

Reader-facing pages use descriptive names first. Internal lifecycle identifiers such as `B3`, `B4`, `B5`, or `E1`–`E9` are retained where they improve provenance and traceability, but they should not be required knowledge for understanding CM-PharmE.