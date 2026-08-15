# CM-PharmE

**CM-PharmE** is an evolving, versioned, ontology-grounded conceptual model and research knowledge base for the pharmaceutical ecosystem. The repository is designed as a long-lived research asset supporting conceptual modeling, formal ontology engineering, evaluation, data mapping, publication traceability, reproducible builds and future applications.

> **Current stable semantic baseline:** `v1.0.0`  
> Engineering, evaluation or manuscript revisions do **not** automatically create a new semantic model version. A new CM-PharmE release is declared only when semantic changes are explicitly identified, evaluated and versioned.

## Start Here

If you are reviewing CM-PharmE, the shortest path is:

**[Published paper](https://ieeexplore.ieee.org/abstract/document/11301544/) → [Model](#model-at-a-glance--v100) → [Research method](docs/methodology/research-and-model-development.md) → [Evaluation](docs/evaluations/index.md) → [Reproducibility](docs/engineering/index.md)**

If you are primarily interested in ontology engineering, start with:

**[Ontology](ontology/README.md) → [Concepts](docs/concepts/index.md) → [Relations](docs/relations/index.md) → [Official OntoUML references](docs/references/ontouml-ecosystem.md) → [Executable evaluation](docs/evaluations/index.md)**

For a broader map of the repository, see the [Documentation Map](docs/index.md).

## Authors and Affiliations

1. **Araz Saie Arasi**  
   Department of Computer Engineering, Ra.C., Islamic Azad University, Rasht, Iran  
   [ORCID: 0009-0009-6739-5717](https://orcid.org/0009-0009-6739-5717)

2. **Hassan Haghighi**  
   Department of Software and Information Systems, Faculty of Computer Science and Engineering, Shahid Beheshti University, Tehran, Iran  
   [ORCID: 0000-0002-6145-4095](https://orcid.org/0000-0002-6145-4095)

3. **Hossein Azgomi**  
   Department of Computer Engineering, Ra.C., Islamic Azad University, Rasht, Iran  
   [ORCID: 0000-0001-7974-1845](https://orcid.org/0000-0001-7974-1845)

## Why CM-PharmE?

Pharmaceutical ecosystems combine enterprises, regulators, healthcare actors, collaborative arrangements, operational and clinical processes, governance constraints and digital infrastructures. Existing ontology, architecture, process, supply-chain and digital-health contributions provide valuable but often separated views of these concerns. CM-PharmE addresses this ecosystem-level semantic fragmentation through a shared conceptual structure with explicit ontological commitments and cross-domain dependencies.

The repository follows an artifact-oriented narrative rather than reproducing manuscript sections:

**Problem → Research gap → CM-PharmE response → Design method → Evidence → Evaluation → Applications → Limitations → Evolution**

[Research rationale](docs/research/rationale.md)

## Design Logic

CM-PharmE uses a two-stage modeling logic derived from the associated research:

1. **Business-architecture concerns identify what requires representation** — organization design, capabilities, stakeholder participation, value delivery, strategy, processes, governance and digital enablement.
2. **UFO/OntoUML clarifies the ontological meaning of the selected constructs** — identity, dependence, roles, relators, modes, temporally unfolding activities, relation semantics and participation constraints.

The model-development lineage combines PRISMA-guided evidence review, thematic synthesis, evidence-to-domain decomposition, business-architecture-informed conceptualization and UFO/OntoUML classification/relation-selection procedures.

[Research and model-development method](docs/methodology/research-and-model-development.md) · [Official OntoUML ecosystem references](docs/references/ontouml-ecosystem.md)

## Model at a Glance — v1.0.0

| Item | Count |
|---|---:|
| Canonical concepts | **39** |
| Canonical semantic relations | **40** |
| Architectural domains | **5** |
| Concept stereotype families | **5** |
| Relation categories | **6** |

Concept stereotypes: 13 `kind`, 8 `mode`, 7 `role`, 6 `relator`, and 5 `perdurant`.

## Model Snapshot — v1.0.0

![CM-PharmE v1.0.0 conceptual model](releases/v1.0.0/model/CM-PharmE-1.0.png)

[Domains of CM-PharmE v1.0.0](releases/v1.0.0/model/Domains-of-CM-PharmE-1.0.png)

## Five Modeling Domains

1. Organizational / Structural
2. Ecosystem / Collaborative
3. Operational / Process
4. Governance / Regulatory
5. Digital Transformation

These are conceptual modeling domains, not predefined DDD bounded contexts, services or microservices.

## Explore CM-PharmE

| Area | Purpose |
|---|---|
| [Documentation Map](docs/index.md) | Reader-oriented map of the repository and recommended paths |
| [Concepts](docs/concepts/index.md) | Stable concepts, stereotypes, domains and relation traceability |
| [Relations](docs/relations/index.md) | Stable relation registry and semantic endpoints |
| [Domains](docs/domains/index.md) | Five-domain architecture and mappings |
| [Ontology](ontology/README.md) | Formal ontology source, distributions, IRI policy and validation |
| [Mappings](mappings/README.md) | Concept/domain/relation/data/publication traceability |
| [Evaluation](docs/evaluations/index.md) | Nine-layer evaluation evidence and executable validation |
| [Methodology](docs/methodology/index.md) | Evidence synthesis, modeling and evaluation methods |
| [Engineering](docs/engineering/index.md) | Reproducible build, CI and release-readiness architecture |
| [Research Rationale](docs/research/rationale.md) | Problem, gap, significance and boundaries |
| [Applications & Boundaries](docs/research/applications-and-boundaries.md) | Intended application pathways and non-claims |
| [Publications](publications/README.md) | Publication lineage, publisher links and model/evidence association |
| [Versions](docs/versions/index.md) | Stable semantic baseline and integrated engineering/evaluation history |

## Formal Ontology and Reproducible Build

The historical OWL export bundled with `v1.0.0` is preserved unchanged for provenance but is not the cleaned canonical ontology source.

The repository modernization progressed through named engineering stages: **Formal Ontology Engineering (B3)** established the modular ontology; **Evaluation and Evidence (B4/B4.10)** added executable evaluation and ROBOT/HermiT reasoning; and **Reproducible Build and CI (B5)** completed the repository-engineering loop. The B-codes are retained as historical/provenance identifiers, while the natural-language names are preferred for reader-facing documentation.

- the authoritative modular source reconstructs the **complete 1,086-triple reference graph**;
- the SHACL reference is reproduced at **574 triples / 76 NodeShapes / 76 PropertyShapes**;
- consolidated Turtle, RDF/XML/OWL, RDF/XML, expanded JSON-LD and canonical N-Triples are generated deterministically;
- two independent clean builds must be byte-identical in CI, and generated distributions are uploaded as CI/release artifacts;
- build manifests and SHA-256 checksums are generated for each build;
- eight competency queries run as regression gates;
- ROBOT/HermiT remains a required logical-validation gate;
- CI produces a deterministic release bundle without automatically declaring a semantic release.

Canonical graph fingerprint:

`cc823a8aff4d7e7818f8470f2dbad6ca8045ff92e5637fbf3503bc105170a83f`

[Reproducible-build architecture](docs/engineering/b5-reproducible-build.md)

## Evidence and Evaluation

The associated research evaluates CM-PharmE through complementary procedures rather than a single aggregate score. The repository organizes this as a **nine-layer evaluation framework**: Syntax Validation (E1), Logical Consistency (E2), Structural Integrity (E3), Ontological Soundness (E4), Semantic & Expert Validation (E5), Data & Mapping Validation (E6), Competency Questions (E7), Application Validation (E8), and Reproducibility (E9).

Current repository evidence includes:

- **28/28** structural and traceability checks;
- **8/8** executable competency queries meeting their bounded expectations;
- a machine-readable vaccine scenario spanning all five domains;
- anti-pattern re-evaluation and explicit semantic finding disposition;
- ROBOT/HermiT logical validation for the current logical axiom set;
- graph-fingerprint, SHACL, serialization and build-reproducibility gates.

Open semantic findings remain explicit: three model-refinement candidates and one item deferred pending domain evidence. The engineering pipeline does not silently change the ontology to eliminate those findings.

[Final evaluation report](docs/evaluations/b4-final-evaluation.md) · [Release readiness](docs/engineering/release-readiness.md)

## Applications and Boundaries

CM-PharmE may support ecosystem/governance reasoning, requirements engineering, interoperability-oriented analysis, reference-architecture interpretation, standards-specific semantic mapping, knowledge-graph development, DDD/software-architecture analysis, dataset mapping and future database/application implementations.

These are application pathways rather than claims of deployed effectiveness. CM-PharmE does not by itself establish legal compliance, FHIR/IDMP/BACM conformance, implementation feasibility, migration cost or organizational adoption.

## Featured Publications

- **CM-PharmE ver.1: Towards a Conceptual Model for Pharmaceutical Ecosystem with a Business-Architecture Perspective** — published conference paper associated with the historical `v1.0.0` conceptual foundation. [IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/11301544/) · [Repository record](publications/ieee-2025/README.md)
- **CM-PharmE 1.0: A Business-Architecture-Informed and Ontology-Grounded Conceptual Model for Pharmaceutical Ecosystems** — journal manuscript **under review**, strengthening methodology, traceability and bounded multi-layer evaluation while retaining the five-domain architecture. [Repository record](publications/journal-under-review/README.md)

Publication status, DOI, publisher links and bibliographic identifiers are recorded only when supported or verified.

## Release and Traceability Model

Released semantic entities are not hard-deleted from history. Concepts, relations and domains use stable identifiers and explicit lifecycle states. Frozen release snapshots preserve semantic inventories and source artifacts.

- [v1.0.0](docs/versions/v1.0.0.md)
- [Versioning policy](docs/policies/versioning.md)
- [Lifecycle policy](docs/policies/lifecycle.md)
- [Semantic changelog](CHANGELOG.md)
- [Migration inventory](MIGRATION_INVENTORY.md)

## Validation Boundary

Current evidence supports structural traceability, formal-source coverage, executable CQs, bounded scenario instantiation, reproducible serializations and OWL logical consistency for the validated axiom set. It does **not** establish universal domain completeness, empirical effectiveness, standards conformance or correctness of every open ontological modeling decision.

The planned namespace is `https://w3id.org/cm-pharme/`, but the external `w3id.org` redirect is not yet registered. License selection is also intentionally left for an explicit repository-owner decision.

## Citation

A machine-readable citation record is provided in [`CITATION.cff`](CITATION.cff). Publications should cite the specific CM-PharmE semantic release used in the research whenever possible.

## Repository Status

The completed repository-modernization cycle covers historical preservation, repository foundation, knowledge-model normalization, formal ontology engineering, paper-grounded evaluation, executable logical validation and reproducible build/CI engineering. The stable semantic baseline remains `v1.0.0` until an intentional next-generation semantic cycle is evaluated and released.
