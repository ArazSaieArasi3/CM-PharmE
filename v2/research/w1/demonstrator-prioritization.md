# W1 Gate B — Research Demonstrator Prioritization

## Purpose
Select a deliberately limited set of high-value demonstrators for the principal CM-PharmE 2.0 article. Other valid applications remain prototype or future-research opportunities.

## Scoring model
Each candidate is scored 1–5. Weighted criteria:
- scientific value: 20%
- ontology dependence: 20%
- novelty contribution: 15%
- data feasibility signal at W1: 15%
- objective evaluability: 15%
- cross-domain coverage: 10%
- implementation feasibility: 5%

W1 data-feasibility scores are preliminary and must be confirmed by W2 Dataset Gate.

| Candidate | Scientific | Ontology dep. | Novelty | Data signal | Evaluability | Cross-domain | Feasibility | Weighted /5 | Proposed class |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| D1 Global actor/facility geospatial integration | 5 | 5 | 4 | 5 | 5 | 5 | 4 | **4.80** | Research Demonstrator |
| D2 Critical-medicine supply vulnerability/resilience | 5 | 5 | 5 | 4 | 4 | 5 | 3 | **4.60** | Research Demonstrator |
| D3 Ontology↔RDB↔KG query consistency + provenance | 5 | 5 | 5 | 5 | 5 | 4 | 4 | **4.85** | Research Evaluation Demonstrator |
| D4 Cross-source entity resolution | 4 | 4 | 4 | 4 | 5 | 5 | 3 | **4.15** | Cross-cutting evaluation / AI candidate |
| D5 Clinical-trial sponsor/site/product network | 4 | 4 | 3 | 5 | 4 | 4 | 4 | **4.05** | Application / held-out candidate |
| D6 Pharmacovigilance evidence integration | 4 | 4 | 3 | 4 | 4 | 3 | 3 | **3.70** | Follow-on application candidate |
| D7 Market-access/reimbursement comparison | 4 | 4 | 4 | 3 | 4 | 3 | 3 | **3.70** | Follow-on application candidate |
| D8 Provenance-aware semantic QA / GraphRAG | 3 | 4 | 4 | 4 | 4 | 4 | 3 | **3.75** | Prototype candidate |
| D9 KG-assisted pharmaceutical demand forecasting | 4 | 3 | 4 | 3 | 5 | 3 | 2 | **3.55** | Future research / follow-on paper |

## Recommended Gate B portfolio

### Primary Research Demonstrator A — Global Actor/Facility Geospatial Integration
**Question:** Can heterogeneous pharmaceutical organizations, facilities/sites, roles, regulatory evidence and locations be represented and queried consistently across jurisdictions?

Why it belongs in the principal article:
- directly supports RQ1–RQ3;
- validates organization/site/role/location/jurisdiction distinctions;
- has strong official-source signals (EudraGMDP, FDA establishment data, ClinicalTrials.gov);
- provides a tangible global-ecosystem application;
- creates a natural basis for PostGIS and map visualization;
- supports held-out/cross-jurisdiction evaluation.

### Primary Research Demonstrator B — Critical Medicine Supply Vulnerability & Resilience
**Question:** Can the ontology integrate product, criticality, site/supplier/dependency, geography and alternative-supply semantics to support reproducible vulnerability/resilience queries?

Why it belongs in the principal article:
- strong ecosystem-level value and novelty;
- directly motivated by FDA/EMA/HERA shortage and preparedness needs;
- exercises relations across product, organization, site, supply, regulation and geography;
- creates a meaningful application beyond ontology syntax;
- can later support crisis/pandemic-like scenario analysis without making the Core crisis-specific.

### Mandatory Research Evaluation Demonstrator C — Ontology↔RDB↔KG Consistency & Provenance
**Question:** Do selected benchmark questions produce semantically consistent results across OntoUML/OWL-aligned PostgreSQL/PostGIS and RDF/SPARQL representations, with traceable evidence provenance?

Why it belongs in the principal article:
- operationalizes a central V2 novelty hypothesis;
- is objectively testable;
- separates CM-PharmE 2.0 from a conventional conceptual ontology paper;
- provides direct evidence for RQ2;
- supports every application without requiring the paper to become a product-development paper.

## Secondary cross-cutting evaluation candidate
**D4 Entity resolution** should be implemented if W2 data contain enough overlapping organization/site/product identifiers to build a defensible gold subset. It can become a measured AI component without making AI the identity of the V2 paper.

## Application Candidates, not principal article requirements
- Clinical-trial sponsor/site/product network.
- Provenance-aware semantic search / GraphRAG.
- Ecosystem browser/observatory shell.
- Regulatory/site evidence browser.
- Market-access/reimbursement dashboard, subject to data.

## Future Research Opportunities
- KG-assisted demand forecasting.
- Predictive shortage modeling.
- Pharmacovigilance/ADR prediction.
- Graph completion/anomaly detection.
- Dedicated Pharmaceutical Ecosystem Risk Ontology or deeper Risk & Resilience paper.
- Dynamic crisis simulation / stockpile optimization.
- Financing/counterparty exposure analytics.

## Gate B decision requested
Approve, modify, or reject the recommended principal portfolio:
1. **A — Global Actor/Facility Geospatial Integration**
2. **B — Critical Medicine Supply Vulnerability & Resilience**
3. **C — Ontology↔RDB↔KG Consistency & Provenance**

If approved, W2 dataset discovery/admission will explicitly search for datasets/source combinations capable of supporting A, B and C while retaining independent held-out evidence.
