# CM-PharmE 2.0 Research Method and Development

> **Page scope:** V2  
> **Documentation maturity:** Stable-to-date / Evolving  
> **Authoritative source:** V2 research program and live issue/PR state  
> **Last synchronized:** 2026-09-23  
> **Last synchronized ref:** `1226b0a5484f8f5d3a8d214e0d0f52f066b88999`  
> **Related issues/PRs:** #21–#24, #98, #104, #159, #169, #170, #171, #173  
> **Evidence status:** Research stages through evidence sufficiency review are stable-to-date; demonstrator evaluation and research release readiness remain pending  
> **Future refresh:** #212 and #214  
> **Wiki baseline:** WB-2026.09.1

## Development stages

The V2 research program is organized as a staged progression from research framing through formalization, implementation, evaluation and application evidence. Internal workstream identifiers are retained only as secondary provenance.

| Stage | Purpose | Current state | Internal reference |
|---|---|---|---|
| Research foundation | identity, scope, research framing | Complete | W0 |
| Needs, uses and opportunities | requirements and use-case framing | Complete | W1 |
| Data landscape | source portfolio and admission rules | Complete | W2 |
| Concept discovery | evidence-driven candidate concepts/relations | Complete | W3 |
| UFO/OntoUML conceptualization | foundational analysis and conceptual baseline | Complete | W4 |
| Formal ontology development | OWL/SHACL realization | Complete | W5 |
| Data and knowledge infrastructure | PostgreSQL/PostGIS, KG and mappings | Complete | W6 |
| Evaluation | multi-family ontology/data/evidence assessment | 13/14; prospective expert evidence pending | W7 |
| Observatory and demonstrators | research application surfaces and representative tasks | 7/8 by live child-issue state | W8 |
| Manuscript and research release | integrated paper/release package | Active | Paper Track |

## Research decision checkpoints

Decision checkpoints are used to prevent implementation progress from being mistaken for scientific evidence. The descriptive decision name is primary; the internal identifier is retained for auditability.

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

## Conceptual baseline

The current conceptual baseline establishes the identity and dependence commitments used for formalization and contains 87 modeled elements across Core, X-INFRA and Extensions.

The corresponding internal decision record is Gate D. That record does not make later semantic review unnecessary; material reversals still require an explicit reviewed disposition.

## Evidence sufficiency review

The evidence sufficiency review allows the research to progress while preserving explicit claim boundaries:
- no quantitative V1→V2 coverage-superiority claim without a common denominator;
- selected claims require bounded wording;
- selected analytics/resilience tasks are supportable only within the evaluated scope;
- geospatial demonstrator effectiveness and real-world entity-resolution performance remain deferred;
- prospective expert evidence (E9) cannot be treated as complete.

Internal provenance: this decision corresponds to Gate F.

## Current demonstrator status

The application/demonstrator program has seven of eight current work items complete by live child-issue state: #169 is closed and #170 remains open.

In the internal work plan this corresponds to W8 = **7/8**. Older parent-Epic prose that still reports 6/8 is stale and should not be used as the current Wiki status.

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
- [Conceptual baseline decision — internal Gate D](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w4/gate-d-conceptual-freeze.md)
- [Evidence sufficiency decision — internal Gate F](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w7/gate-f-claim-sufficiency-decision.md)
