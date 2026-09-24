# CM-PharmE 2.0 Research Method and Development

> **Version scope:** V2  
> **Status:** Stable-to-date / Evolving  
> **Updated:** 2026-09-23

## Development stages

The V2 research program progresses from research framing through formalization, implementation, evaluation and application evidence.

| Stage | Purpose | Current state |
|---|---|---|
| Research foundation | identity, scope, research framing | Complete |
| Needs, uses and opportunities | requirements and use-case framing | Complete |
| Data landscape | source portfolio and admission rules | Complete |
| Concept discovery | evidence-driven candidate concepts/relations | Complete |
| UFO/OntoUML conceptualization | foundational analysis and conceptual baseline | Complete |
| Formal ontology development | OWL/SHACL realization | Complete |
| Data and knowledge infrastructure | PostgreSQL/PostGIS, KG and mappings | Complete |
| Evaluation | multi-family ontology/data/evidence assessment | 13/14; prospective expert evidence pending |
| Observatory and demonstrators | research application surfaces and representative tasks | 7/8 by live child-issue state |
| Manuscript and research release | integrated paper/release package | Active |

## Research decision checkpoints

Decision checkpoints prevent implementation progress from being mistaken for scientific evidence.

| Decision | Current state |
|---|---|
| Research identity and scope | Approved |
| Principal research use cases | Approved |
| Evidence/data admission and held-out design | Approved |
| Candidate concept inventory | Approved |
| Conceptual baseline | Approved |
| Formal ontology readiness | Approved |
| Representation architecture | Approved |
| Evidence sufficiency review | **Approved progression with bounded claim dispositions** |
| Demonstrator evaluation | Pending |
| Research release readiness | Pending |

## Conceptual baseline

The current conceptual baseline establishes the identity and dependence commitments used for formalization and contains 87 modeled elements across Core, X-INFRA and Extensions.

This baseline remains subject to explicit semantic review where a material revision is proposed; documentation does not itself authorize such a change.

## Evidence sufficiency review

The evidence sufficiency review allows the research to progress while preserving explicit claim boundaries:
- no quantitative V1→V2 coverage-superiority claim without a common denominator;
- selected claims require bounded wording;
- selected analytics/resilience tasks are supportable only within the evaluated scope;
- geospatial demonstrator effectiveness and real-world entity-resolution performance remain deferred;
- prospective expert evidence (E9) cannot be treated as complete.

## Current demonstrator status

The application/demonstrator program has seven of eight current work items complete by live child-issue state: #169 is closed and #170 remains open.

Older parent-Epic prose that reports six of eight is stale and should not be used as the current Wiki status.

## Current research sequence

1. Continue semantic review of the ontology.
2. Continue integrated manuscript Draft 0.
3. Complete #170 representative-task evaluation.
4. Complete the demonstrator-evaluation decision for the manuscript-facing application scope.
5. Complete E9 when real eligible participants are available.
6. Build the reproducible research package/DOI if approved.
7. Complete the final manuscript↔repository↔data traceability audit.
8. Complete research release readiness before any final V2 freeze.

## Branch boundary

V2 research integrates on `v2/research-program`. The stable V1 `main` line remains semantically isolated from V2 changes pending an explicit migration decision.

## Evidence

- [V2 research program](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/README.md)
- [Conceptual baseline decision record](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w4/gate-d-conceptual-freeze.md)
- [Evidence sufficiency decision record](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w7/gate-f-claim-sufficiency-decision.md)

<details>
<summary>Internal research-control references</summary>

These identifiers are retained for repository traceability and historical audit.

### Stage identifiers

| Reader-facing stage | Internal reference |
|---|---|
| Research foundation | W0 |
| Needs, uses and opportunities | W1 |
| Data landscape | W2 |
| Concept discovery | W3 |
| UFO/OntoUML conceptualization | W4 |
| Formal ontology development | W5 |
| Data and knowledge infrastructure | W6 |
| Evaluation | W7 |
| Observatory and demonstrators | W8 |

### Decision identifiers

| Reader-facing decision | Internal reference |
|---|---|
| Research identity and scope | Gate A |
| Principal research use cases | Gate B |
| Evidence/data admission and held-out design | Gate C |
| Candidate concept inventory | Concept Inventory Gate |
| Conceptual baseline | Gate D |
| Formal ontology readiness | Formal Gate |
| Representation architecture | Gate E |
| Evidence sufficiency review | Gate F |
| Demonstrator evaluation | Gate G |
| Research release readiness | Gate H |

</details>

---

<details>
<summary>Documentation record</summary>

- **Page scope:** V2
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative source:** V2 research program and live issue/PR state
- **Last synchronized:** 2026-09-23
- **Last synchronized ref:** `1226b0a5484f8f5d3a8d214e0d0f52f066b88999`
- **Related issues/PRs:** #21–#24, #98, #104, #159, #169, #170, #171, #173
- **Evidence status:** Research stages through evidence sufficiency review are stable-to-date; demonstrator evaluation and research release readiness remain pending
- **Future refresh:** #212 and #214
- **Wiki baseline:** WB-2026.09.1

</details>
