# Gate and Claim Dispositions

> **Page scope:** V2  
> **Documentation maturity:** Stable-to-date / Evolving  
> **Authoritative source:** V2 gate decisions, live issues and claim-evidence register  
> **Last synchronized:** 2026-09-23  
> **Related issues/PRs:** #24, #98, #104, #170, #171, #212, #214  
> **Evidence status:** Gates A–F resolved; Gate G/H pending  
> **Future refresh:** #212 and #214  
> **Wiki baseline:** WB-2026.09.1

## Why gates exist

V2 gates prevent implementation progress from silently becoming scientific claim inflation. A gate records whether the evidence is sufficient to proceed and what wording/boundaries remain mandatory.

## Current gate state

| Gate | Purpose | Current state |
|---|---|---|
| A | V2 identity and scope | Approved |
| B | primary article use cases | Approved |
| C | admitted/held-out datasets | Approved |
| Concept Inventory | discovery baseline | Approved |
| D | conceptual model freeze | Approved |
| Formal Gate | OWL/SHACL formal baseline | Approved |
| E | representation architecture | Approved |
| F | claim-evidence sufficiency | **Approved progression with bounded claim dispositions** |
| G | demonstrator/manuscript-facing application scope | Pending |
| H | target journal / manuscript / research-release freeze | Pending |

## Gate F

Gate F does not state that every candidate claim is fully supported. It explicitly differentiates claim dispositions.

### Narrowed
- C-01: V2 may describe qualitative/design expansion and source-semantic coverage, but not a like-for-like percentage improvement over V1.

### Bounded / qualified
Examples include:
- data-grounded evolution;
- UFO/OntoUML commitments without official-tool certification;
- ontology↔RDB↔KG traceability only for registered/reference mappings;
- cross-jurisdiction generalizability only for evaluated held-out families;
- resilience as scenario-level representational adequacy;
- OWL 2 DL/multi-reasoner evidence with documented warnings;
- SHACL as executable research-integrity constraints, not universal external-data conformance.

### Selected tasks only
- C-06: selected evaluated analytics/resilience tasks only; no generalized AI/application performance claim.

### Explicit limitation
- C-13: current public evidence is insufficient for complete global product→supplier→buyer→shipment reconstruction.

### Deferred
- geospatial demonstrator effectiveness;
- real-world entity-resolution performance;
- unsupported AI performance/novelty.

## E9 dependency

E9 is not “passed by readiness.” It remains incomplete until real eligible expert responses are collected and analyzed under the frozen protocol.

The current status is:
- protocol frozen;
- 27/27 readiness checks PASS;
- 23-item instrument;
- **0 real responses**;
- **0 admissible expert-result claims**.

## Gate G

Gate G must use the completed representative-task evidence from #170. Missing/partial/failed tasks must remain visible. Gate G cannot infer usability/production effectiveness merely from implementation existence.

## Gate H

Gate H is the final manuscript/research-release freeze. It requires final traceability and a truthful disposition for remaining dependencies, including E9.

## Authoritative evidence

- [Gate D decision](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w4/gate-d-conceptual-freeze.md)
- [Gate F decision](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w7/gate-f-claim-sufficiency-decision.md)
- [Claim-evidence traceability](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/evaluation/results/w7-claim-evidence-traceability.csv)
- [Representative-task results](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/app/observatory/representative-task-results.md)

## Status-resolution rule

If a parent Epic is stale, live child issues/PRs and current decision artifacts take precedence for Wiki status.
