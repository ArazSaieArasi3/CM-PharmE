# CM-PharmE

**CM-PharmE** is an evolving, versioned, ontology-grounded conceptual model and research knowledge base for the pharmaceutical ecosystem. The repository is being restructured from a single-publication snapshot into a long-lived research asset that supports conceptual modeling, ontology engineering, evaluation, data mapping, publication traceability, and future applications.

> **Current stable historical release:** `v1.0.0`  
> **Current development line:** `vNext` on `refactor/research-repository-v1`  
> CM-PharmE is expected to evolve over time. Released artifacts remain preserved and traceable even when concepts, relations, domains, mappings, or ontology alignments are refined in later versions.

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

## Overview

Pharmaceutical ecosystems involve multi-layered interactions across organizational, regulatory, clinical, technological, and inter-organizational domains. CM-PharmE provides a coherent conceptual foundation for representing those elements and their relationships with explicit ontological grounding. The initial model was developed with a business-architecture perspective and grounded in the Unified Foundational Ontology (UFO). The repository now separates the evolving conceptual model, formal ontology, release history, evaluation evidence, mappings, publications, and future applications so that each research release can be reproduced and compared over time.

## Model Snapshot — v1.0.0

![CM-PharmE v1.0.0 conceptual model](releases/v1.0.0/model/CM-PharmE-1.0.png)

A domain-oriented view is also preserved in the historical release: [Domains of CM-PharmE v1.0.0](releases/v1.0.0/model/Domains-of-CM-PharmE-1.0.png).

## Explore CM-PharmE

| Area | Purpose |
|---|---|
| [Concepts](docs/concepts/index.md) | Concept registry and future one-page-per-concept documentation |
| [Relations](docs/relations/index.md) | Relation registry, semantics, source/target, lifecycle and version history |
| [Domains](docs/domains/index.md) | Domain definitions, membership and cross-domain relationships |
| [Versions](docs/versions/index.md) | Stable releases, development line and reproducible snapshots |
| [Ontology](ontology/README.md) | Formal ontology source, distributions, upper-ontology grounding and validation |
| [Mappings](mappings/README.md) | Concept/domain/ontology/data/publication mappings and traceability |
| [Evaluation](docs/evaluations/index.md) | Layered evaluation framework and per-release evidence |
| [Methodology](docs/methodology/index.md) | Model-design, ontology-engineering, mapping and evaluation methods |
| [Architecture](docs/architecture/index.md) | Layered architecture and traceability model |
| [Publications](publications/README.md) | Scholarly publications linked to specific model releases |
| [Applications](applications/README.md) | Applications and tools built on CM-PharmE |

## Featured Publications

CM-PharmE has been developed in connection with peer-reviewed academic research. The repository keeps publication records explicitly linked to the model release used by each study.

- **Towards a Conceptual Model for Pharmaceutical Ecosystem with a Business-Architecture Perspective** — associated with the historical `v1.0.0` model. [Publication record](publications/ieee-2025/README.md)
- Additional journal publications and their exact model-version mappings will be added as their repository metadata is finalized.

> Publication status, DOI, publisher links, and other bibliographic identifiers are recorded only when verified; the repository does not infer missing bibliographic metadata.

## Release and Traceability Model

Released semantic entities are not hard-deleted from history. Concepts, relations, and domains receive stable identifiers and lifecycle states such as `Proposed`, `Active`, `Deprecated`, `Retired`, or `Superseded`. Each stable release is intended to have a manifest recording the exact model, ontology, concepts, relations, domains, mappings, evaluation evidence, and linked publications for that release.

- [v1.0.0 release documentation](docs/versions/v1.0.0.md)
- [Semantic changelog](CHANGELOG.md)
- [Migration inventory and provenance](MIGRATION_INVENTORY.md)

## Ontology

The OWL file distributed with the original v1.0 model is preserved as a historical artifact. It was generated from the conceptual diagram and is **not** treated as the future canonical ontology source. The formal ontology will be re-engineered in subsequent repository cycles with a canonical source, generated serializations, validation, stable IRIs, and explicit foundational-ontology mappings.

## Evaluation

CM-PharmE uses a layered evaluation architecture covering syntax, logical consistency, structure, ontological grounding, expert/semantic validation, data and mapping validation, competency questions, application usability, and research reproducibility. Results are version-specific and are separated from the reusable evaluation methodology.

## Citation

A machine-readable citation record is provided in [`CITATION.cff`](CITATION.cff). Publications should cite the specific CM-PharmE release used in the research whenever possible.

## Repository Status

This branch represents the first research-repository restructuring cycle. Historical artifacts remain preserved byte-for-byte through Git object identity and are materialized under `releases/v1.0.0/`. The original paths are retained during migration for traceability and will not be removed without explicit review.
