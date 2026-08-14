# CM-PharmE

**CM-PharmE** is an evolving, versioned, ontology-grounded conceptual model and research knowledge base for the pharmaceutical ecosystem. The repository is organized as a long-lived research asset supporting conceptual modeling, ontology engineering, evaluation, data mapping, publication traceability, and future applications.

> **Current stable semantic baseline:** `v1.0.0`  
> Ongoing development is managed through versioned branches and pull requests.  
> A manuscript revision does **not** automatically create a new CM-PharmE model version. A new model release is declared only when semantic changes to concepts, relations, domains, mappings, or ontology commitments are explicitly identified and versioned.

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

Pharmaceutical ecosystems combine enterprises, regulators, healthcare actors, collaborative arrangements, operational and clinical processes, governance constraints, and digital infrastructures. Existing ontology, architecture, process, supply-chain, and digital-health contributions provide valuable but often separated views of these concerns. CM-PharmE addresses the resulting ecosystem-level semantic fragmentation by providing a shared conceptual structure with explicit ontological commitments and cross-domain dependencies.

The repository follows a compact artifact narrative rather than reproducing manuscript sections:

**Problem → Research gap → CM-PharmE response → Design method → Evidence → Evaluation → Applications → Limitations → Evolution**

[Read the repository research rationale](docs/research/rationale.md).

## Design Logic

CM-PharmE uses a two-stage modeling logic derived from the associated research:

1. **Business-architecture concerns identify what requires representation** — organization design, capabilities, stakeholder participation, value delivery, strategy, process, governance, and digital enablement.
2. **UFO/OntoUML clarifies the ontological meaning of the selected constructs** — identity, dependence, roles, relators, modes, temporally unfolding activities, relation semantics, and participation constraints.

The model-development lineage combines a PRISMA-guided evidence review, thematic synthesis, evidence-to-domain decomposition, business-architecture-informed conceptualization, and UFO/OntoUML classification and relation-selection procedures. The repository documents this as a reusable method rather than as a second copy of the papers.

[Research and model-development method](docs/methodology/research-and-model-development.md)

## Model at a Glance — v1.0.0

| Item | Count |
|---|---:|
| Canonical concepts | **39** |
| Canonical semantic relations | **40** |
| Architectural domains | **5** |
| Concept stereotype families | **5** |
| Relation categories | **6** |

Concept stereotypes: 13 `kind`, 8 `mode`, 7 `role`, 6 `relator`, and 5 `perdurant`. The normalized documentation is derived primarily from the original Draw.io/XML source while preserving the historical OWL export for reproducibility and cross-checking.

[Full v1.0.0 statistics and structural audit](docs/evaluations/v1.0.0-structural-audit.md)

## Model Snapshot — v1.0.0

![CM-PharmE v1.0.0 conceptual model](releases/v1.0.0/model/CM-PharmE-1.0.png)

A domain-oriented view is also preserved in the historical release: [Domains of CM-PharmE v1.0.0](releases/v1.0.0/model/Domains-of-CM-PharmE-1.0.png).

## Five Modeling Domains

CM-PharmE separates modeling responsibilities into five interrelated domains while preserving explicit cross-domain relations:

1. Organizational / Structural
2. Ecosystem / Collaborative
3. Operational / Process
4. Governance / Regulatory
5. Digital Transformation

These domains are conceptual modeling domains, not predefined DDD bounded contexts, services, or microservices.

## Explore CM-PharmE

| Area | Purpose |
|---|---|
| [Concepts](docs/concepts/index.md) | Canonical registry and one page per concept, with stable IDs, stereotypes, domains, relation traceability, and historical OWL snippets |
| [Relations](docs/relations/index.md) | Canonical relation registry and one page per relation, including source/target and semantic relation category |
| [Domains](docs/domains/index.md) | Five-domain architecture, domain scope, membership, and cross-domain mapping |
| [Versions](docs/versions/index.md) | Stable releases, semantic inventories, and unreleased engineering work |
| [Ontology](ontology/README.md) | Historical ontology provenance plus the modular formal-ontology source, IRI policy, mappings, and validation boundary |
| [Mappings](mappings/README.md) | Concept↔Domain, Concept↔Relation, ontology/data/publication mappings and traceability |
| [Evaluation](docs/evaluations/index.md) | Layered evaluation framework and version-/batch-specific evidence |
| [Methodology](docs/methodology/index.md) | Evidence synthesis, model development, ontology engineering, and evaluation methods |
| [Research Rationale](docs/research/rationale.md) | Problem, gap, response, significance, evidence, and limitations in repository form |
| [Applications & Boundaries](docs/research/applications-and-boundaries.md) | Governance, requirements, interoperability, architecture, DDD, and computational use boundaries |
| [References](docs/references/research-method-and-evaluation.md) | Curated method/evaluation references used by repository documentation |
| [Architecture](docs/architecture/index.md) | Layered architecture and traceability model |
| [Publications](publications/README.md) | Scholarly publications linked to model states and research evidence |
| [Applications](applications/README.md) | Applications and tools built on CM-PharmE |

## Evidence and Evaluation

The associated research evaluates CM-PharmE through complementary procedures rather than a single aggregate score. The later journal manuscript under review strengthens the earlier evaluation by explicitly documenting a scenario-based comparative benchmark, qualitative review by four experts, focused manual inspection of eight OntoUML-informed anti-pattern categories, eight competency questions, and an illustrative vaccine-distribution instantiation.

The repository converts that methodology into evaluation layers E1–E9: syntax, logic, structure, ontological validation, semantic/expert validation, data/mapping validation, competency questions, application validation, and reproducibility.

B4 explicitly distinguishes **publication-reported evidence** from **repository-reproduced or computationally verified evidence**. This is important because the published conference paper contains some stronger early evaluation statements that the later manuscript subsequently bounds more conservatively.

B4/B4.10 now includes 28/28 structural checks, eight executable competency queries, a machine-readable five-domain vaccine scenario, anti-pattern re-evaluation, publication/expert traceability, and a reproducible GitHub Actions ROBOT/HermiT logical-validation workflow.

- [Evaluation method](docs/methodology/evaluation-method.md)
- [B4 paper-grounded evaluation plan](docs/evaluations/b4-evaluation-plan.md)
- [B4/B4.10 executed evaluation matrix](docs/evaluations/b4-evaluation-matrix.md)
- [B4.10 reasoner and semantic finding disposition](docs/evaluations/b4-10-semantic-finding-disposition.md)
- [Machine-readable evaluation evidence](evaluation/README.md)
- [Publication-to-repository traceability](docs/research/publication-to-repository-traceability.md)

## Applications and Boundaries

CM-PharmE may support ecosystem/governance reasoning, requirements engineering, interoperability-oriented analysis, reference-architecture interpretation, standards-specific semantic mapping, knowledge-graph development, and later DDD/software-architecture analysis.

These are application pathways rather than claims of deployed effectiveness. CM-PharmE does not by itself establish legal compliance, FHIR/IDMP conformance, implementation feasibility, migration cost, organizational adoption, or a final service architecture.

[Applications and evidential boundaries](docs/research/applications-and-boundaries.md)

## Featured Publications

CM-PharmE has been developed through a traceable publication lineage:

- **CM-PharmE ver.1: Towards a Conceptual Model for Pharmaceutical Ecosystem with a Business-Architecture Perspective** — published conference paper associated with the historical `v1.0.0` conceptual foundation. [Publication record](publications/ieee-2025/README.md)
- **CM-PharmE 1.0: A Business-Architecture-Informed and Ontology-Grounded Conceptual Model for Pharmaceutical Ecosystems** — journal manuscript **under review**, preserving the five-domain architecture while strengthening methodology, traceability, and bounded multi-layer evaluation. [Publication record](publications/journal-under-review/README.md)

> Publication status, DOI, publisher links, and other bibliographic identifiers are recorded only when supported or verified; missing metadata is not inferred.

## Release and Traceability Model

Released semantic entities are not hard-deleted from history. Concepts, relations, and domains receive stable identifiers and lifecycle states such as `Proposed`, `Active`, `Deprecated`, `Retired`, or `Superseded`. Each stable release maintains a manifest and frozen registries so that the exact semantic inventory remains reconstructable.

- [v1.0.0 release documentation](docs/versions/v1.0.0.md)
- [Unreleased B3 formal-ontology work](docs/versions/unreleased-b3.md)
- [Semantic changelog](CHANGELOG.md)
- [Migration inventory and provenance](MIGRATION_INVENTORY.md)
- [Current-model baseline](model/current/README.md)

## Ontology

The OWL file distributed with the original v1.0 model is preserved unchanged as a historical artifact. It was automatically generated from the conceptual diagram and contains converter artifacts, so it is **not** treated as the canonical cleaned ontology source.

B3 introduced a modular formal-ontology authoring source with stable identifier-based IRIs, formal concept definitions, relation/property semantics, endpoint cardinality traceability, lifecycle/provenance metadata, and cautious UFO/OntoUML correspondence notes. B3 is integrated into `main` while the stable semantic baseline remains `v1.0.0`; the formalization cycle did not itself declare a new semantic release.

See [Ontology](ontology/README.md) and the [B3 Formal Ontology Audit](docs/evaluations/b3-formal-ontology-audit.md).

## Validation Boundary

Current repository evidence supports structural traceability, formal-source coverage, bounded executable competency questions, a machine-readable cross-domain scenario, and **repository-executed ROBOT/HermiT logical validation for the current logical axiom set**. GitHub Actions run `31796520297` completed successfully with HermiT exit code `0` after ROBOT `v1.9.10` was verified by SHA-256.

The logical PASS does **not** establish universal ontology completeness, empirical effectiveness, technical interoperability, standards conformance, or correctness of every ontological modeling choice. B4.10 retains targeted role/mediation and part-whole findings as explicit semantic review items rather than silently changing the model.

The GitHub modular source also differs from the B3 packaged canonical source in annotation/provenance coverage, while B4.10 records zero logical-predicate differences. Annotation parity remains a repository-engineering follow-up.

The journal manuscript itself similarly treats expert review, anti-pattern inspection, competency questions, benchmarking, and scenario instantiation as complementary but preliminary evidence rather than definitive empirical validation.

## Citation

A machine-readable citation record is provided in [`CITATION.cff`](CITATION.cff). Publications should cite the specific CM-PharmE release used in the research whenever possible.

## Repository Status

B0–B3 are integrated into `main`: historical preservation, repository foundation, knowledge-model normalization, and formal-ontology engineering are established. On the B4 evaluation branch, the two-paper research/evaluation lineage has been transferred into a repository-native evidence architecture; structural checks, competency queries, scenario validation, and ROBOT/HermiT logical validation have been executed. Open work is now concentrated on targeted semantic refinement decisions, annotation/provenance normalization, stronger independent expert/domain evidence where needed, deterministic generated-distribution/release automation, persistent-IRI deployment, and public documentation tooling.
