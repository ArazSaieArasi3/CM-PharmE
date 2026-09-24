# Evidence Scope and Supported Claims

> **Page scope:** V2  
> **Documentation maturity:** Stable-to-date / Evolving  
> **Authoritative source:** V2 research decision records, live issues and claim-evidence register  
> **Last synchronized:** 2026-09-23  
> **Related issues/PRs:** #24, #98, #104, #170, #171, #212, #214  
> **Evidence status:** Early/mid-program decisions are resolved; demonstrator evaluation and final research release readiness remain pending  
> **Future refresh:** #212 and #214  
> **Wiki baseline:** WB-2026.09.1

## Why research decision checkpoints exist

V2 uses explicit research decision checkpoints to prevent implementation progress from silently becoming scientific claim inflation. A checkpoint records whether the evidence is sufficient to proceed and what wording or evidential boundary remains mandatory.

Internal Gate identifiers are retained for auditability but are not required to understand the claims.

## Current decision state

| Decision | Current state | Internal reference |
|---|---|---|
| Research identity and scope | Approved | Gate A |
| Principal research use cases | Approved | Gate B |
| Evidence/data admission and held-out design | Approved | Gate C |
| Candidate concept inventory | Approved | Concept Inventory Gate |
| Conceptual baseline | Approved | Gate D |
| Formal ontology readiness | Approved | Formal Gate |
| Representation architecture | Approved | Gate E |
| Evidence sufficiency review | **Approved progression with bounded claim dispositions** | Gate F |
| Demonstrator evaluation | Pending | Gate G |
| Research release readiness | Pending | Gate H |

## Evidence sufficiency review

The evidence sufficiency review does not state that every candidate claim is fully supported. It explicitly differentiates claim dispositions.

Internal provenance: Gate F.

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

## Prospective expert-evaluation dependency

E9 remains incomplete until real eligible expert responses are collected and analyzed under the frozen protocol.

Current state:
- protocol frozen;
- 27/27 readiness checks PASS;
- 23-item instrument;
- **0 real responses**;
- **0 admissible expert-result claims**.

## Demonstrator evaluation

The final demonstrator decision must use the completed representative-task evidence from #170. Missing, partial or failed tasks must remain visible. Implementation existence is not evidence of usability or production effectiveness.

Internal provenance: Gate G.

## Research release readiness

The final research-release decision requires final traceability and a truthful disposition for remaining dependencies, including E9.

Internal provenance: Gate H.

## Authoritative evidence

- [Conceptual baseline decision — internal Gate D](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w4/gate-d-conceptual-freeze.md)
- [Evidence sufficiency decision — internal Gate F](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w7/gate-f-claim-sufficiency-decision.md)
- [Claim-evidence traceability](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/evaluation/results/w7-claim-evidence-traceability.csv)
- [Representative-task results](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/app/observatory/representative-task-results.md)

## Status-resolution rule

If a parent Epic is stale, live child issues/PRs and current decision artifacts take precedence for Wiki status.
