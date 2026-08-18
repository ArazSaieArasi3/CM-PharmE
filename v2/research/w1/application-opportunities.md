# W1 Application and Observatory Opportunity Landscape

## Principle
Applications must expose or test ontology/data value. The ontology is not redesigned merely to fit a UI feature. Product scope is separated from the principal ontology paper.

## Application opportunity matrix

| ID | Application | Primary users | Ontology/data value | Research value | Build effort | W1 disposition |
|---|---|---|---|---|---|---|
| APP-01 | Global Pharmaceutical Ecosystem Observatory | Researchers, regulators, public-health analysts | Unified navigation across product, organisation, site, geography, regulation and provenance | Very high as demonstrator shell | Medium–High | **Prototype candidate** |
| APP-02 | Actor & Facility Geospatial Explorer | Regulators, supply/resilience analysts | Makes organization/site distinction and geospatial/jurisdiction semantics visible | Very high | Medium | **Primary demonstrator candidate** |
| APP-03 | Critical Medicine & Supply Vulnerability Explorer | Regulators, preparedness teams | Uses typed product/site/dependency/alternative relations | Very high | Medium–High | **Primary demonstrator candidate** |
| APP-04 | Product/Substance/Organisation Browser | Researchers/data stewards | Entity-centric access across identifiers and provenance | High | Medium | Prototype candidate |
| APP-05 | Regulatory/Site Evidence Browser | Regulators/manufacturers/researchers | Site/organization/status/evidence/time semantics | High | Medium | Prototype candidate |
| APP-06 | Clinical Trial Network Browser | Sponsors/researchers | Sponsor–collaborator–facility–intervention–country graph | Medium–High | Medium | Application/held-out candidate |
| APP-07 | Pharmacovigilance Evidence Browser | Safety analysts/researchers | Product/safety-event/source/provenance integration | High but domain-expanding | High | Follow-on application candidate |
| APP-08 | Market Access/Reimbursement Dashboard | Health-policy/payer researchers | Distinguishes access, reimbursement, availability and geography/time | Medium–High | Medium | Follow-on unless W2 data are unusually strong |
| APP-09 | Provenance Viewer | All research users | Assertion→source/dataset/record traceability | Very high enabling value | Low–Medium | **Cross-cutting mandatory feature** |
| APP-10 | Semantic Search / GraphRAG Interface | Researchers/analysts | Typed KG retrieval with evidence links | High application value | Medium | Prototype candidate; not primary novelty |
| APP-11 | SQL/SPARQL/API Query Workbench | Researchers/developers | Makes cross-representation equivalence inspectable | Very high evaluation value | Medium | **Research evaluation demonstrator** |
| APP-12 | Resilience Scenario Workbench | Preparedness/supply analysts | Disruption scenario→dependency reach→alternatives | Very high | High | Prototype candidate after data feasibility |
| APP-13 | Data Quality / Compliance Assistant | Data stewards/MAHs | Ontology + SHACL/rules identify missing/incompatible records | High | Medium | Future application candidate |
| APP-14 | Financing/Counterparty Exposure View | Financing actors/researchers | Could connect finance arrangements to ecosystem dependencies | Potentially high | High/data-constrained | Future research only pending data |

## Recommended product architecture for later W8
A single Observatory can host multiple research views rather than separate applications:

1. **Explore** — product, organization, site, study, evidence.
2. **Map** — facilities, trial sites, jurisdictions, geographic concentration.
3. **Graph** — typed relations/dependencies.
4. **Analyze** — resilience/concentration/access metrics.
5. **Ask** — provenance-aware semantic search/QA.
6. **Query** — API/SPARQL and benchmark SQL/SPARQL questions.
7. **Provenance** — source and mapping evidence for any selected assertion.

## Minimum W8 demonstrator, if Gate B selects the recommended article scope
- actor/facility geospatial browser;
- critical-medicine dependency/resilience view;
- provenance panel;
- a small set of predefined ontology-driven benchmark queries;
- optional graph view;
- no requirement for a production-scale public platform before the ontology paper is complete.

## Future exploitation opportunities
The same infrastructure could later support:
- public global pharmaceutical ecosystem observatory;
- data-quality/semantic-integration service;
- regulatory/compliance data tooling;
- resilience intelligence for health-system preparedness;
- pharmaceutical market/access research;
- provenance-aware research data services;
- domain-specific AI/GraphRAG applications.

These are opportunities, not V2 claims, until implemented and evaluated.
