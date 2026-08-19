# W3 — Evidence-Driven Concept & Relation Discovery Closure Report

## Status
**W3 implementation: COMPLETE**

**Concept Inventory Gate: READY FOR USER DECISION**

## Issues covered
- V2-028 / #47 — source schema profiling and candidate concepts
- V2-029 / #48 — candidate relations, roles, relators and events
- V2-030 / #49 — geospatial, temporal and jurisdiction concepts
- V2-031 / #50 — provenance, evidence and observation concepts
- V2-032 / #51 — identifiers and entity-resolution requirements
- V2-033 / #52 — V1→V2 reconciliation
- V2-034 / #53 — evidence-to-concept/relation traceability
- V2-035 / #54 — admission protocol and Concept Inventory Gate

## Main outputs
1. `README.md`
2. `source-schema-concept-extraction.md`
3. `candidate-concept-inventory.md`
4. `candidate-relations-events.md`
5. `geospatial-temporal-jurisdiction.md`
6. `provenance-evidence-observation.md`
7. `identifiers-entity-resolution.md`
8. `v1-v2-migration-matrix.md`
9. `evidence-traceability.md`
10. `concept-admission-protocol.md`
11. `gate-concept-inventory.md`
12. `../../manuscript/w3-concept-discovery-notes.md`
13. updated `../evidence-registry.md`
14. updated `../../manuscript/evidence-ledger.md`

## Quantitative discovery result
- **80** normalized pre-UFO concept candidates.
- **80** candidate relationship/event semantics.
- Concept dispositions:
  - **29 CORE**
  - **23 X-INFRA**
  - **26 EXT**
  - **2 DEFER**

These are discovery counts, not final ontology class/property counts. W4 may merge/split/reclassify/reject candidates after UFO/OntoUML analysis.

## Principal semantic backbone discovered
**Organization / Contextual Role → Site / Facility → Regulatory Authorization & Jurisdiction → Medicinal Product / Substance / Presentation → Geography & Time → Shortage / Availability / Demand / Supply Observations → Evidence / Provenance / Identifier Infrastructure**

This backbone is materially more domain-centered and data-grounded than the V1 Business-Architecture-centered organization.

## Major V2 evolution decisions supported by W3
1. Business Architecture retained as optional extension/view, not Core decomposition.
2. Pharmaceutical Enterprise generalized to Organization + contextual pharmaceutical roles.
3. Organization, physical Site/Facility, License/Registration and Role explicitly separated.
4. Product semantics expanded to Medicinal Product, Substance, Presentation, Dosage Form, Strength and Package.
5. Essential/Critical medicine modeled as contextual classifications tied to list/jurisdiction/version.
6. Shortage/status/availability/demand/supply represented with temporal/source/context semantics.
7. Generic V1 ecosystem/supply relationships replaced by typed candidate relations.
8. Provenance, identifiers, mappings and entity-match evidence become first-class infrastructure.
9. Risk/resilience, market access, safety, BA, digital/application and clinical semantics remain modular extensions.
10. Technology-specific V1 classes do not determine Core ontology structure.

## Held-out integrity audit
**PASS**

Protected H1/H2/H3 source families were not used to admit W3 Core concepts/relations:
- ClinicalTrials.gov/AACT
- openFDA Drug Shortages
- selected national EML schemas

Their high-level existence/feasibility from W2 remains documented, but detailed schema mining is reserved for W7.

## Important limitations retained
- No claim of complete global product-level supplier→buyer→shipment reconstruction.
- Detailed procurement/inventory/lead-time/stockout semantics rely substantially on conditional C1 and remain extension-level.
- EudraGMDP automated ingestion remains conditional.
- Finance/counterparty remains outside Core.
- AI/entity-resolution performance has not yet been evaluated.
- W3 candidate UFO interpretations are provisional hypotheses only.

## Gate recommendation
Approve the pre-UFO inventory and authorize **W4 — UFO/OntoUML Conceptualization**.

W4 should not simply assign stereotypes to the 80 candidates. It must perform identity, rigidity, dependence, unity, role/relator, event/situation, observation/result, part-whole and normative/social-object analysis, with explicit modeling decision records and Core/Extension refinement.

## Main-branch safety
All W3 work is isolated on `v2/w3-concept-discovery` and will target `v2/research-program`. No V2 content targets `main`.
