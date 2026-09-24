# CM-PharmE 2.0

> **Page scope:** V2  
> **Documentation maturity:** Stable-to-date / Evolving  
> **Authoritative source:** `v2/research-program`  
> **Last synchronized:** 2026-09-23  
> **Last synchronized ref:** `1226b0a5484f8f5d3a8d214e0d0f52f066b88999`  
> **Related issues/PRs:** #21–#24, #98, #159, #170, #171, #173  
> **Evidence status:** Substantial stable baseline with explicit pending human/application/manuscript work  
> **Future refresh:** #212, #213, #214  
> **Wiki baseline:** WB-2026.09.1

## Research identity

CM-PharmE 2.0 is being developed as a **data-grounded, UFO/OntoUML-based pharmaceutical ecosystem domain ontology and knowledge infrastructure**.

Business Architecture remains useful as an analytical view/mapping layer, but V2 does not make it the defining identity of the ontology Core.

## Research objective

V2 aims to:
1. ground concepts and relations in traceable evidence/data;
2. conceptualize them explicitly through UFO/OntoUML;
3. implement a modular OWL/SHACL ontology;
4. preserve semantics across ontology, relational database and RDF/KG representations;
5. support reproducible cross-domain, geospatial and resilience-oriented analyses;
6. evaluate the resulting infrastructure through prospectively defined evidence families.

## Current program state

At this synchronization point:
- W0–W6 are complete.
- W7 computational/documentary evaluation is complete for E1–E8 and E10–E13.
- E9 expert evaluation is protocol-frozen and operationally ready, but **0 real responses** exist.
- Gate F is approved with bounded claim dispositions.
- W8 is **7/8 complete** by live child-issue state; #169 is closed and #170 remains open.
- Human ontology review remains active (#159, #173).
- Integrated manuscript Draft 0 remains active (#171).
- Gate G and Gate H are not final.

## Approved conceptual/formal baseline

Gate D froze:
- 32 Core conceptual types/pattern elements;
- 25 X-INFRA;
- 30 Extensions;
- **87 total**.

Formal version `2.0.0-alpha.1` records:
- 642 asserted triples;
- 81 OWL classes + 6 declared datatypes;
- 52 object properties;
- 5 datatype properties;
- OWL 2 DL profile PASS;
- ROBOT/HermiT validation PASS for the evaluated axiom set.

## Representation baseline

W6 establishes a reference realization using:
- PostgreSQL/PostGIS;
- ontology↔RDB mappings;
- provenance and entity-match structures;
- deterministic RDF ABox/KG generation;
- SQL↔SPARQL benchmark pairs;
- bounded OpenAPI/query contract.

This is a research/reference realization, not a production-scale deployment claim.

## Evaluation position

V2 uses a multi-family evaluation program E1–E13. Most computational/documentary families are complete; E9 human evidence remains genuinely pending.

See [[V2 Evaluation E1-E13]].

## Relationship to V1

V2 is a controlled evolution of V1, not a retroactive rewrite. It retains important foundations such as UFO/OntoUML grounding and ecosystem-level integration while changing evidence strategy, modular architecture, formalization depth, data realization and evaluation rigor.

See [[V1 to V2 Research Evolution]] and [[Continuity Refinement and Novelty]].

## Authoritative navigation

- [V2 research program](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/README.md)
- [Research canvas](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/research-canvas.md)
- [Evidence registry](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/evidence-registry.md)
- [Formal ontology](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/ontology/README.md)
- [Data layer](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/data/README.md)
- [Human review control center](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/review/README.md)
