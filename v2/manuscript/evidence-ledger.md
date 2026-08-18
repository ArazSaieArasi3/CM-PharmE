# CM-PharmE 2.0 Manuscript and Evidence Ledger

## Purpose
Keep the manuscript, repository, datasets, ontology artifacts, evaluation results, and application evidence synchronized throughout development.

## Claim lifecycle
Each manuscript claim should be tracked as:
- Proposed
- Evidence pending
- Supported
- Bounded / qualified
- Rejected
- Deferred to future work

## Ledger schema
| Claim ID | Manuscript section | Claim | Required evidence | Repository artifact / source | Status | Boundary / limitation |
|---|---|---|---|---|---|---|

## Initial claims to test, not assume
| Claim ID | Candidate claim | Evidence required | Current status |
|---|---|---|---|
| C-01 | V2 provides broader pharmaceutical-ecosystem concept coverage than V1. | V1→V2 migration matrix + dataset/literature coverage evidence. | Evidence pending |
| C-02 | V2 is data-grounded rather than scenario-grounded. | Admitted DOI-backed/authoritative datasets + concept provenance. | Evidence pending |
| C-03 | UFO/OntoUML commitments are more explicit and systematically justified. | Decision records + OntoUML evaluation. | Evidence pending |
| C-04 | Ontology, relational database, and knowledge graph preserve traceable semantics. | Mapping rules + cross-representation tests. | Evidence pending |
| C-05 | V2 supports cross-jurisdiction/generalizable representation. | Held-out/cross-jurisdiction evaluation. | Evidence pending |
| C-06 | Selected analytics/resilience use cases can be reproducibly executed. | Demonstrator + metrics + reproducible datasets/code. | Evidence pending |
| C-07 | Cross-source organization/site identity, geography/jurisdiction, temporal status and provenance are material pharmaceutical-ecosystem integration needs. | Official regulatory/trial/safety/access sources + W1 stakeholder/use-case synthesis. | **Bounded support at W1** |
| C-08 | Geospatial actor/facility integration is a defensible research demonstrator for V2. | W1 need/use-case evidence + W2 admitted data + W6 implementation + W7 metrics. | W1 rationale supported; implementation evidence pending |
| C-09 | Critical-medicine supply vulnerability/resilience is a defensible ecosystem-level research demonstrator. | FDA/EMA/HERA need evidence + admitted dependency/criticality data + reproducible analysis. | W1 rationale supported; data/evaluation pending |
| C-10 | AI opportunities such as entity resolution, semantic QA, forecasting and shortage prediction are plausible but should not be claimed as V2 contributions before benchmark evaluation. | W1 primary-research examples + later task-specific data/baselines/metrics. | **Bounded / future-dependent** |

## W1 evidence artifacts
- `v2/research/w1/evidence-sources.md`
- `v2/research/w1/stakeholder-needs.md`
- `v2/research/w1/use-case-catalog.md`
- `v2/research/w1/analytics-ai-opportunities.md`
- `v2/research/w1/geospatial-resilience-risk.md`
- `v2/research/w1/application-opportunities.md`
- `v2/research/w1/research-funding-opportunities.md`
- `v2/research/w1/demonstrator-prioritization.md`

## Manuscript skeleton
1. Introduction
2. Background and prior CM-PharmE lineage
3. Research design and dataset admission protocol
4. Concept discovery and evidence traceability
5. UFO/OntoUML conceptualization
6. Formal ontology and constraints
7. Relational/KG realization and data integration
8. Evaluation
9. Application demonstrator(s)
10. Discussion
11. Limitations
12. Conclusion

## W1 manuscript guidance
The Introduction may now state, with appropriate citations, that pharmaceutical ecosystem information needs span shortage/supply monitoring, manufacturing/site evidence, clinical-research networks, pharmacovigilance, access and crisis preparedness, and that cross-source identity/geography/provenance integration is a central problem. It must **not** state that V2 already solves these needs.

The application section should remain provisional until Gate B and W2. The preferred working demonstrators are recorded in W1 but become manuscript commitments only after Gate B approval and Dataset Gate confirmation.

## Writing rule
The manuscript is updated after each wave, but no result is written as completed until its corresponding repository/data evidence exists and passes the applicable gate.
