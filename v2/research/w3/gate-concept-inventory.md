# W3 Concept Inventory Gate — Proposed Pre-UFO Scope

## Status
**W3 discovery complete — awaiting Concept Inventory Gate approval.**

This gate approves the **evidence-backed conceptual scope** that W4 will analyze using UFO/OntoUML. It does not approve final stereotypes, cardinalities, OWL axioms or module imports.

## 1. Inventory summary
| Disposition | Count | Meaning |
|---|---:|---|
| CORE candidates | **29** | Stable pharmaceutical-ecosystem distinctions to be subjected to W4 foundational analysis. |
| Cross-cutting infrastructure | **23** | Geography/time, provenance/evidence, identifier/entity-resolution semantics used across modules. |
| Extension candidates | **26** | Market access, detailed supply/resilience, risk, safety, BA, digital/application and clinical semantics. |
| Deferred | **2** | Useful but outside principal V2 ontology/article commitment. |
| **Total normalized concept candidates** | **80** | Pre-UFO inventory; W4 may split/merge/reclassify. |
| Candidate relationship semantics | **80** | Pre-UFO relation/event/participation inventory. |

## 2. Proposed Core semantic backbone
### Actors and regulation
- Organization.
- Ecosystem Participant Role.
- Regulatory Authority Role.
- Manufacturer, Importer, Product-Responsible/Labeler, Wholesale Distributor and 3PL roles.
- Site / Facility with Manufacturing/Distribution Site roles.
- Establishment Registration.
- Regulatory Authorization / License.
- Regulatory Jurisdiction.

### Product/material structure
- Medicinal Product.
- Pharmaceutical Substance / Active Ingredient.
- Medicinal Product Presentation.
- Dosage Form.
- Strength / Concentration Specification.
- Package Configuration.
- Product Classification.
- Product Listing / Marketing Status.

### Activities and ecosystem states
- Manufacturing Activity.
- Distribution / Logistics Activity.
- Medicine Shortage Case and Shortage Status.
- Availability Observation.
- Demand Observation.
- Supply Capacity Observation.

## 3. Cross-cutting infrastructure proposed for explicit modeling
### Geography/time
- Geographic Feature, Administrative Region, Country, Geospatial Position, Address, Time Interval and Reporting Period.

### Evidence/provenance
- Data Source, Dataset, Dataset Release, Source Record, Assertion, Observation, Measure/Quantity Value, Evidence Item, Mapping Assertion, Provenance Activity and Data Quality Finding.

### Identity
- Identifier, Identifier Scheme, Identifier Assignment, Entity Match Assertion and Match Evidence/Confidence.

## 4. Extension architecture proposed
### Resilience / supply
Critical Medicine Classification, Alternative Product Role, Supply Dependency, Disruption Event, Inventory Observation, Procurement Activity, Lead-Time Observation and Stockout Event.

### Policy / market access
Essential Medicine Classification, Payer/Funding Role, Reimbursement/Utilisation Observation and Diagnosis Classification Reference.

### Risk
Risk Assessment, Vulnerability and Risk Treatment/Mitigation; align with UFO-grounded risk reference work rather than redefining generic risk semantics in Core.

### Regulatory / safety
Regulatory Requirement, Regulatory Oversight Relationship, Pharmacovigilance Requirement, Adverse Event Reporting Activity and Post-Market Surveillance Activity.

### Business architecture / partnerships
Business Architecture View, Enterprise Capability, Strategic Partnership Agreement and Service Offering Specification. Public–Private Partnership Arrangement is deferred from principal scope.

### Digital / clinical
Digital/Information System Component and generic Clinical Care Participant Role remain extensions. Detailed Clinical Care Pathway/Activity Pattern is deferred.

## 5. Key V1→V2 design decisions requiring Gate acceptance
1. **Business Architecture is no longer the Core decomposition principle.** It remains an optional analytical view.
2. **Pharmaceutical Enterprise is generalized to Organization + contextual roles.**
3. **Organization and physical Site/Facility are distinct.**
4. **Ecosystem Actor becomes a contextual participant role rather than a universal actor kind.**
5. Generic `Ecosystem Relationship` and `Supply Chain Relationship` are split into typed relations rather than retained as catch-all semantics.
6. Demand and supply-capacity “signals/modes” are reframed as source/time/context-bounded observations where the evidence is observational.
7. **Medicinal Product–Substance–Presentation–Form–Strength–Package** becomes an explicit domain layer absent from the original V1 Core.
8. Critical/Essential medicine semantics are modeled as contextual classification/status relations tied to list/jurisdiction/version, not permanent intrinsic drug kinds.
9. Shortage is time/source/jurisdiction bounded; W4 will decide Event vs Situation vs case/record distinctions.
10. Provenance, identifiers and mapping assertions are first-class infrastructure to support ontology↔RDB↔KG evaluation.
11. Generic risk remains a modular extension/alignment problem rather than Core pharmaceutical semantics.
12. Technology-specific V1 items such as a Blockchain Supply Chain Ledger or AI-CDSS are not Core ontology classes.

## 6. Protected held-out boundary carried into the gate
- H1 ClinicalTrials.gov/AACT was not mined to admit Core concepts/relations.
- H2 openFDA Drug Shortages was not used to design the W3 shortage Core.
- H3 selected national EML schemas were not used to expand essential/critical semantics.

W7 can therefore evaluate whether the independently derived Core covers those source families without circular concept discovery.

## 7. Explicit non-claims / exclusions
- No complete global product-level supplier→buyer→shipment graph is claimed.
- Financing/counterparty semantics are not promoted to Core.
- C1 detailed supply operations remain conditional and non-redistributable unless terms are clarified.
- EudraGMDP automated ingestion remains conditional on compliant access.
- AI performance is not a W3 result.
- The 80 candidates are not final ontology classes; W4 foundational analysis may reduce or restructure them.

## 8. W4 questions already identified
W4 must explicitly resolve:
- Organization Kind/Category architecture and role bearers.
- Site/Facility identity, ownership/operation and site roles.
- Product vs presentation/specification/artifact distinctions.
- Dosage form/package/strength ontological status.
- Authorization/registration/license as relator vs normative/social object vs information record.
- Critical/Essential classification assignment pattern.
- Shortage Event vs Situation vs socially recognized case/record.
- Observation act vs observation result/information record.
- Supply Capacity as disposition/quality vs observed capacity value.
- Supply Dependency as relator/material/dependency relation.
- Jurisdiction as social/legal object distinct from geographic region.
- Provenance/identifier patterns and alignment to PROV-O/SOSA/DCAT where useful.
- Risk extension alignment to COVER/ROSE patterns.

## 9. Gate recommendation
**Approve the W3 pre-UFO inventory and proceed to W4 UFO/OntoUML Conceptualization.**

Reason: the inventory is broad enough to support the approved demonstrators, materially improves the V1 domain semantics, preserves data/held-out traceability, and avoids prematurely expanding the Core into finance, clinical trials, pharmacovigilance, business architecture or technology-specific applications.
