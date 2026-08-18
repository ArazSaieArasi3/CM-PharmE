# W1 — Needs, Uses & Opportunities Closure Report

## Status
**W1 implementation: COMPLETE**

**Gate B: APPROVED on 2026-08-18**

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

## Approved principal portfolio
1. **Global Actor/Facility Geospatial Integration**
2. **Critical Medicine Supply Vulnerability & Resilience**
3. **Ontology↔RDB↔KG Consistency & Provenance**

Secondary candidate: measured cross-source entity resolution if W2 exposes sufficient overlapping identifiers/records to construct a defensible gold subset.

## Principal findings
- The highest-value ecosystem needs are cross-source identity, organization/site separation, geography/jurisdiction, temporal status, cross-domain dependency and provenance.
- Geospatial semantics are a cross-cutting Core concern rather than a standalone domain.
- Resilience/shortage analysis is strongly motivated by regulatory and preparedness practice, but quantitative claims require W2 data admission.
- Generic risk semantics remain modular and aligned/reused rather than duplicated in the pharmaceutical Core.
- AI is a supporting/evaluable capability. Entity resolution is the strongest cross-cutting candidate; GraphRAG/semantic QA is an application candidate; forecasting and predictive models remain follow-on work unless datasets justify promotion.
- Funding/translation opportunities are tracked independently from scientific scope decisions.

## Next wave
**W2 — Dataset Landscape, Admission and Held-out Evaluation Design**

W2 searches broadly across product/substance, organization/site, manufacturing/supply/logistics, shortage/criticality, clinical trial, safety/pharmacovigilance, reimbursement/access and geospatial sources; verifies DOI/stable identifiers, access, license/reuse, schema, provenance and research fit; and reserves independent held-out evidence before W3 concept discovery.

## Main-branch safety
W1 was merged only into `v2/research-program`. No V2 model, dataset, manuscript or application change targeted `main`.
