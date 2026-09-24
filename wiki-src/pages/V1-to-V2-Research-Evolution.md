# V1 to V2 Research Evolution

> **Page scope:** Cross-version  
> **Documentation maturity:** Stable-to-date / Evolving  
> **V1 authority:** `main`  
> **V2 authority:** `v2/research-program`  
> **Last synchronized:** 2026-09-23  
> **V1 ref:** current stable V1 documentation baseline on `main`  
> **V2 ref:** `1226b0a5484f8f5d3a8d214e0d0f52f066b88999`  
> **Related issues/PRs:** #159, #173, #206  
> **Evidence status:** Stable cross-version narrative; semantic-review-dependent details remain refreshable  
> **Future refresh:** #213 and #214  
> **Wiki baseline:** WB-2026.09.1

## Purpose

CM-PharmE 2.0 is best understood as a controlled research evolution from CM-PharmE 1.x rather than as an unrelated replacement or a claim that V1 was “wrong.” V1 established the initial ecosystem-level conceptual foundation. V2 changes the research design where new evidence, modeling requirements and evaluation goals justify doing so.

## What V1 established

V1 contributed:
- an ecosystem-level conceptual scope;
- a five-domain architecture;
- business-architecture-informed concern identification;
- UFO/OntoUML-grounded conceptual commitments;
- 39 canonical concepts and 40 canonical semantic relations;
- formal ontology/repository engineering;
- competency questions, structural/logical checks and bounded application/evaluation evidence;
- a publication/repository traceability model.

These are predecessor contributions, not V2 novelty.

## Why V2 was initiated

V2 responds to research opportunities that are materially different from simply revising prose:
- stronger grounding in heterogeneous real datasets and authoritative sources;
- explicit held-out evaluation;
- finer identity distinctions for organizations, facilities, products, substances, presentations, geography and jurisdiction;
- first-class evidence, provenance, mapping and entity-resolution semantics;
- explicit ontology↔RDB↔KG realization;
- more prospective, multi-family evaluation;
- dedicated semantic review of concepts, relations and evidence;
- bounded research demonstrators.

## Research progression

### 1. From evidence review to multi-source data grounding

V1 uses a PRISMA-guided evidence-review lineage and thematic synthesis to establish ecosystem concerns.

V2 retains literature/methodological evidence but adds a governed portfolio of DOI-backed datasets, authoritative sources, held-out sources and source-field mappings. Dataset presence is not treated as ontological truth; it is one form of evidence used in concept/relation admission and evaluation.

### 2. From five-domain conceptual architecture to modular ontology architecture

V1 organizes the ecosystem into five modeling domains.

V2 does not automatically preserve those five domains as its Core decomposition. It derives a new modular architecture through evidence discovery and UFO/OntoUML analysis:
- Core;
- X-INFRA;
- modular Extensions.

The current V2 taxonomy contains 17 domains/modules.

### 3. From broad ecosystem concepts to explicit identity/context distinctions

V2 introduces or sharpens distinctions such as:
- Organization versus Facility;
- Facility versus Geographic Feature;
- Country/Region versus Regulatory Jurisdiction;
- Medicinal Product versus Substance versus Product Presentation;
- identifier value versus entity identity;
- observation activity versus observation result;
- shortage situation versus records/assertions about shortage;
- supply capacity versus evidence about capacity.

These are conceptual changes justified through the V2 research/evidence process, not merely new names.

### 4. From repository formalization to cross-representation realization

V1 develops a cleaned formal ontology and reproducible semantic-engineering pipeline.

V2 retains formal OWL/SHACL work and additionally realizes selected semantics through PostgreSQL/PostGIS and a deterministic RDF KG, with registered ontology↔RDB mappings and SQL↔SPARQL benchmark checks.

### 5. From layered evaluation to prospective multi-family evaluation

V1 evaluation provides valuable structural, logical, semantic, competency-question, data/application and reproducibility evidence.

V2 prospectively defines E1–E13 evaluation families, includes held-out evidence, cross-representation checks, resilience scenarios and an explicit expert-evaluation protocol. E9 real expert results remain pending and must not be inferred.

### 6. From application pathways to bounded demonstrators

V1 discusses application pathways and illustrative use.

V2 implements specific research demonstrators while separating representability/task correctness from production effectiveness or AI novelty claims.

## Research continuity

V2 retains important V1 foundations:
- ecosystem-level research scope;
- UFO/OntoUML lineage;
- conceptual-model discipline;
- explicit relation semantics;
- competency-question practice;
- version/repository traceability;
- interest in governance, supply, process, risk, digital and ecosystem concerns.

## Research redirection

V2 deliberately changes several design assumptions:
- Business Architecture moves from a defining concern-identification identity toward an optional analytical extension/view.
- Generic actor/relationship/process constructs are replaced or refined through typed roles, relators, events and evidence-grounded distinctions.
- technology-specific classes are moved out of Core or deprecated in generic form.
- evidence/provenance and identity-resolution semantics become first-class infrastructure.

## What this evolution does not prove

Chronological evolution is not evidence that V2 is universally “better” than V1. In particular:
- V1 and V2 do not share a like-for-like quantitative coverage denominator;
- their evaluation programs differ;
- their concept counts measure different model granularities;
- V2 is not yet final;
- E9 expert evidence and final demonstrator-evaluation evidence remain incomplete.

Internal provenance for the application checkpoint is retained under the W8/Gate G controls.

## Evidence

- [V1 research method](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/methodology/research-and-model-development.md)
- [V1 version record](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/versions/v1.0.0.md)
- [V2 research canvas](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/research-canvas.md)
- [V1→V2 migration matrix](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w3/v1-v2-migration-matrix.md)
- [Conceptual baseline decision — internal Gate D](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w4/gate-d-conceptual-freeze.md)
- [V2 concept provenance matrix](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w4/human-review-concept-provenance-matrix.md)

## Related pages

[[V1 to V2 Concept Migration]] · [[V1 to V2 Relation Migration]] · [[V1 to V2 Domain Evolution]] · [[V1 to V2 Evidence and Provenance]] · [[Continuity Refinement and Novelty]] · [[Cross-Version Comparison Limits]]
