# V2 Concept and Relation Discovery

> **Page scope:** V2  
> **Documentation maturity:** Stable-to-date / Evolving  
> **Authoritative source:** W2/W3 evidence, concept discovery and W4 conceptualization artifacts  
> **Last synchronized:** 2026-09-23  
> **Last synchronized ref:** `1226b0a5484f8f5d3a8d214e0d0f52f066b88999`  
> **Related issues/PRs:** W3/W4 program, #159, #173  
> **Evidence status:** Gate-D baseline stable; concept-level human provenance review still active  
> **Future refresh:** #213  
> **Wiki baseline:** WB-2026.09.1

## Discovery principle

V2 does not inherit the complete V1 concept set by default. Candidate concepts and relations are admitted through an evidence-driven process using literature, datasets, schemas, authoritative sources and explicit use cases, followed by UFO/OntoUML analysis.

## Admission discipline

A candidate should have a clear reason to exist:
- independent identity/rigidity/dependence semantics;
- a necessary relation/relator pattern;
- repeated evidence from admitted sources;
- a requirement needed to answer frozen competency questions/use cases;
- a justified extension role.

Source labels or database fields do not automatically become ontology classes.

## Conceptual baseline

Gate D freezes 87 named conceptual types/pattern elements:
- 32 Core;
- 25 X-INFRA;
- 30 Extensions.

Two W3 deferred candidates remain outside that freeze.

## Core versus infrastructure versus extensions

- **Core** carries stable domain semantics.
- **X-INFRA** carries cross-cutting evidence, provenance, identifier, geography/time/data infrastructure semantics.
- **Extensions** isolate specialized concerns such as risk/resilience or business-architecture views so they do not distort Core identity commitments.

## Relation discovery

Relations are evaluated together with the ontological status of their endpoints. Mediation, bearer/dependence, participation and context are treated explicitly rather than inferred from source-schema foreign keys alone.

## Human review still matters

The formal Gate-D freeze is not a substitute for human evidence review. #159 and #173 continue to inspect provenance, definitions, V1 predecessors, migration treatment and relation semantics.

No Wiki page should promote a human-review proposal to canonical status before explicit author disposition.

## Evidence

- [Gate D conceptual freeze](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w4/gate-d-conceptual-freeze.md)
- [V1→V2 novelty/migration matrix](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/v1-v2-novelty-migration-matrix.md)
- [Human review control center](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/review/README.md)
- [Concept review index](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/review/concepts/index.md)
