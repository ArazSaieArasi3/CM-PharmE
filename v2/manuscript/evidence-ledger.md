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
| Claim ID | Candidate claim | Evidence required | Initial status |
|---|---|---|---|
| C-01 | V2 provides broader pharmaceutical-ecosystem concept coverage than V1. | V1→V2 migration matrix + dataset/literature coverage evidence. | Evidence pending |
| C-02 | V2 is data-grounded rather than scenario-grounded. | Admitted DOI-backed/authoritative datasets + concept provenance. | Evidence pending |
| C-03 | UFO/OntoUML commitments are more explicit and systematically justified. | Decision records + OntoUML evaluation. | Evidence pending |
| C-04 | Ontology, relational database, and knowledge graph preserve traceable semantics. | Mapping rules + cross-representation tests. | Evidence pending |
| C-05 | V2 supports cross-jurisdiction/generalizable representation. | Held-out/cross-jurisdiction evaluation. | Evidence pending |
| C-06 | Selected analytics/resilience use cases can be reproducibly executed. | Demonstrator + metrics + reproducible datasets/code. | Evidence pending |

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

## Writing rule
The manuscript is updated after each wave, but no result is written as completed until its corresponding repository/data evidence exists and passes the applicable gate.
