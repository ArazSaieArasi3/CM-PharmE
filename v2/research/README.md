# CM-PharmE 2.0 Research Program

## Status
This directory contains the isolated research program for CM-PharmE 2.0. The public `main` branch remains the CM-PharmE 1.x reviewer-facing baseline. Version 2 research work is developed only on `v2/research-program` and its descendant branches until the v1 journal cycle is complete.

## Working identity
CM-PharmE 2.0 is being developed as a **data-grounded, UFO/OntoUML-based pharmaceutical ecosystem domain ontology and knowledge infrastructure**. Business Architecture is retained as an optional analytical view/mapping layer rather than as the defining identity of the ontology core.

## Core research principles
- evidence-driven concept and relation discovery;
- UFO/OntoUML as the primary conceptual modeling foundation;
- modular Core + Extension architecture;
- DOI-backed research datasets plus authoritative operational sources;
- explicit geospatial, temporal, jurisdictional, evidence, and provenance semantics;
- formal OWL/SHACL implementation with reproducible validation;
- ontology-aligned relational database and RDF knowledge graph;
- application-oriented validation through analytics, observatory, and resilience use cases;
- prospective, predeclared evaluation protocols;
- manuscript and repository co-development through an evidence ledger.

## Branch policy
- `main`: frozen CM-PharmE 1.x public/reviewer baseline.
- `v2/research-program`: integration branch for CM-PharmE 2.0 research.
- `v2/w*/*`: wave-specific implementation branches derived from `v2/research-program`.
- No v2 pull request targets `main` before the v1 publication cycle is closed and a separate migration decision is approved.

## Planned waves
1. W0 — Research Foundation
2. W1 — Needs, Uses & Opportunities
3. W2 — Data Landscape
4. W3 — Concept Discovery
5. W4 — UFO/OntoUML Conceptualization
6. W5 — Formal Ontology
7. W6 — Data Infrastructure
8. W7 — Evaluation
9. W8 — Application / Observatory
10. Paper Track — runs in parallel across all waves

## Decision gates
- Gate A — V2 identity and scope
- Gate B — primary article use cases
- Gate C — admitted primary/secondary/held-out datasets
- Gate D — conceptual model freeze
- Gate E — representation architecture
- Gate F — evidence sufficiency for manuscript
- Gate G — demonstrator scope
- Gate H — target journal and submission freeze
