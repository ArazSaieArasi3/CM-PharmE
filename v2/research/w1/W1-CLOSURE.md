# W1 — Needs, Uses & Opportunities Closure Report

## Status
**W1 implementation: COMPLETE**

**Gate B: READY FOR USER DECISION**

## Issues covered
- V2-008 Stakeholders and unmet information needs
- V2-009 Pharmaceutical ecosystem use-case catalog
- V2-010 High-value data-analytics use cases
- V2-011 Ontology-enabled AI use cases
- V2-012 Geospatial intelligence use cases
- V2-013 Pharmaceutical resilience/disruption use cases
- V2-014 Relationship with reusable Risk Ontology research
- V2-015 Application/observatory opportunities
- V2-016 Translation, partnership, research and funding opportunities
- V2-017 Demonstrator prioritization

## Main outputs
1. `evidence-sources.md`
2. `stakeholder-needs.md`
3. `use-case-catalog.md`
4. `analytics-ai-opportunities.md`
5. `geospatial-resilience-risk.md`
6. `application-opportunities.md`
7. `research-funding-opportunities.md`
8. `demonstrator-prioritization.md`
9. `../../manuscript/w1-problem-usecase-notes.md`
10. Updated `../evidence-registry.md`
11. Updated `../../manuscript/evidence-ledger.md`

## Principal findings
- The highest-value ecosystem needs are cross-source identity, organization/site separation, geography/jurisdiction, temporal status, cross-domain dependency and provenance.
- Geospatial semantics should be a cross-cutting Core concern rather than a standalone domain.
- Resilience/shortage analysis is strongly motivated by current regulatory and preparedness practice, but quantitative claims require W2 data admission.
- Generic risk semantics should remain modular and aligned/reused rather than duplicated in the pharmaceutical Core.
- AI is a supporting/evaluable capability. Entity resolution is the best current cross-cutting AI candidate for the principal research; GraphRAG/semantic QA is a strong application candidate; forecasting and predictive models are better treated as follow-on work unless datasets justify promotion.
- Funding/translation opportunities exist around research infrastructure, regulatory-data compliance, health innovation and preparedness, but scientific scope remains independent of funding calls.

## Gate B recommendation
Approve the following principal V2 demonstrator portfolio:

### A. Global Actor/Facility Geospatial Integration
Cross-source/cross-jurisdiction representation and analysis of organizations, sites/facilities, roles, locations and regulatory evidence.

### B. Critical Medicine Supply Vulnerability & Resilience
Ontology-driven dependency/concentration/alternative-supply analysis across medicines, organizations, sites, geography and shortage/preparedness evidence.

### C. Ontology↔RDB↔KG Consistency & Provenance
A mandatory research-evaluation demonstrator testing equivalent semantic questions across relational and RDF representations with source-level traceability.

### Secondary candidate
Cross-source entity resolution becomes a measured AI component if W2 exposes sufficient overlapping identifiers/records to build a defensible gold subset.

## Deferred from the principal article unless later evidence is exceptional
- demand forecasting;
- predictive shortage modeling;
- pharmacovigilance prediction;
- general GraphRAG as a novelty claim;
- full market-access product;
- financing/counterparty analytics;
- full crisis simulation/optimization;
- standalone Pharmaceutical Risk Ontology.

## Next wave after Gate B
**W2 — Dataset Landscape, Admission and Held-out Evaluation Design**

W2 will search broadly across product/substance, organization/site, manufacturing/supply/logistics, shortage/criticality, clinical trial, safety/pharmacovigilance, reimbursement/access and geospatial sources. It will score DOI-backed and authoritative sources, verify access/license/schema/provenance, and reserve independent held-out evidence before W3 concept discovery.

## Main-branch safety
All W1 work is isolated on `v2/w1-needs-usecases-opportunities`. No V2 model, data, manuscript or application change has been targeted to `main`.
