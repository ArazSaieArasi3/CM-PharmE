---
artifact_type: concept_evidence_passport_registry
ontology_id: CM-PharmE
ontology_version: 2.0.0-alpha.1
review_status: active
passport_count: 87
planned_passport_count: 87
---
# CM-PharmE 2.0 — Concept Evidence Passport Registry

This registry instantiates Phase 2 of #173 using the canonical OGCM-RF Concept Evidence Passport pattern. Passports are review projections over governed V2 evidence; they do not create new semantic authority or imply human approval.

## Instantiated coverage

| # | Concept | Domain | Stereotype | Review status | Passport |
|---:|---|---|---|---|---|
| 1 | Organization | Ecosystem Organization | Kind | Pending | [Open](001-organization.md) |
| 2 | Ecosystem Participant | Ecosystem Organization | RoleMixin | Pending | [Open](002-ecosystem-participant.md) |
| 3 | Regulatory Authority | Ecosystem Organization | Role | Pending | [Open](003-regulatory-authority.md) |
| 4 | Manufacturer | Ecosystem Organization | Role | Pending | [Open](004-manufacturer.md) |
| 5 | Importer | Ecosystem Organization | Role | Pending | [Open](005-importer.md) |
| 6 | Product Responsible Organization | Ecosystem Organization | Role | Pending | [Open](006-product-responsible-organization.md) |
| 7 | Wholesale Distributor | Ecosystem Organization | Role | Pending | [Open](007-wholesale-distributor.md) |
| 8 | Third-Party Logistics Provider | Ecosystem Organization | Role | Pending | [Open](008-third-party-logistics-provider.md) |
| 9 | Facility | Facility Operations | Kind | Pending | [Open](009-facility.md) |
| 10 | Manufacturing Site | Facility Operations | Role | Pending | [Open](010-manufacturing-site.md) |
| 11 | Distribution Site | Facility Operations | Role | Pending | [Open](011-distribution-site.md) |
| 12 | Facility Operation | Facility Operations | Relator | Pending | [Open](012-facility-operation.md) |
| 13 | Establishment Registration | Regulatory Governance | Relator | Pending | [Open](013-establishment-registration.md) |
| 14 | Regulatory Authorization | Regulatory Governance | Relator | Pending | [Open](014-regulatory-authorization.md) |
| 15 | Regulatory Jurisdiction | Regulatory Governance | Kind | Pending | [Open](015-regulatory-jurisdiction.md) |
| 16 | Medicinal Product | Pharmaceutical Product | Kind | Pending | [Open](016-medicinal-product.md) |
| 17 | Pharmaceutical Substance | Pharmaceutical Product | Kind | Pending | [Open](017-pharmaceutical-substance.md) |
| 18 | Medicinal Product Presentation | Pharmaceutical Product | Kind | Pending | [Open](018-medicinal-product-presentation.md) |
| 19 | Dosage Form Specification | Pharmaceutical Product | Kind | Pending | [Open](019-dosage-form-specification.md) |
| 20 | Strength | Pharmaceutical Product | Quality | Pending | [Open](020-strength.md) |
| 21 | Package Configuration | Pharmaceutical Product | Kind | Pending | [Open](021-package-configuration.md) |
| 22 | Product Classification Scheme | Pharmaceutical Product | Kind | Pending | [Open](022-product-classification-scheme.md) |
| 23 | Classification Entry | Pharmaceutical Product | Kind | Pending | [Open](023-classification-entry.md) |
| 24 | Product Classification Assignment | Pharmaceutical Product | Relator | Pending | [Open](024-product-classification-assignment.md) |
| 25 | Market Listing | Pharmaceutical Product | Relator | Pending | [Open](025-market-listing.md) |
| 26 | Manufacturing Activity | Supply Operations | Event | Pending | [Open](026-manufacturing-activity.md) |
| 27 | Pharmaceutical Logistics Activity | Supply Operations | Event | Pending | [Open](027-pharmaceutical-logistics-activity.md) |
| 28 | Medicine Shortage Situation | Supply Operations | Situation | Pending | [Open](028-medicine-shortage-situation.md) |
| 29 | Supply Capacity | Supply Operations | Mode | Pending | [Open](029-supply-capacity.md) |
| 30 | Availability Observation Result | Ecosystem Observation | Subkind | Pending | [Open](030-availability-observation-result.md) |
| 31 | Demand Observation Result | Ecosystem Observation | Subkind | Pending | [Open](031-demand-observation-result.md) |
| 32 | Supply Capacity Observation Result | Ecosystem Observation | Subkind | Pending | [Open](032-supply-capacity-observation-result.md) |
| 33 | Geographic Feature | Spatiotemporal Context | Kind | Pending | [Open](033-geographic-feature.md) |
| 34 | Administrative Region | Spatiotemporal Context | Subkind | Pending | [Open](034-administrative-region.md) |
| 35 | Country | Spatiotemporal Context | Subkind | Pending | [Open](035-country.md) |
| 36 | Geospatial Position | Spatiotemporal Context | Datatype | Pending | [Open](036-geospatial-position.md) |
| 37 | Address | Spatiotemporal Context | Datatype | Pending | [Open](037-address.md) |
| 38 | Time Interval | Spatiotemporal Context | Datatype | Pending | [Open](038-time-interval.md) |
| 39 | Reporting Period | Spatiotemporal Context | Datatype | Pending | [Open](039-reporting-period.md) |
| 40 | Data Source | Evidence Traceability | Kind | Pending | [Open](040-data-source.md) |
| 41 | Dataset | Evidence Traceability | Kind | Pending | [Open](041-dataset.md) |
| 42 | Dataset Release | Evidence Traceability | Kind | Pending | [Open](042-dataset-release.md) |
| 43 | Source Record | Evidence Traceability | Kind | Pending | [Open](043-source-record.md) |
| 44 | Assertion | Evidence Traceability | Kind | Pending | [Open](044-assertion.md) |
| 45 | Observation Activity | Evidence Traceability | Event | Pending | [Open](045-observation-activity.md) |
| 46 | Observation Result | Evidence Traceability | Kind | Pending | [Open](046-observation-result.md) |
| 47 | Measure Value | Evidence Traceability | Datatype | Pending | [Open](047-measure-value.md) |
| 48 | Evidence Item | Evidence Traceability | RoleMixin | Pending | [Open](048-evidence-item.md) |
| 49 | Evidence Support | Evidence Traceability | Relator | Pending | [Open](049-evidence-support.md) |
| 50 | Mapping Assertion | Evidence Traceability | Subkind | Pending | [Open](050-mapping-assertion.md) |
| 51 | Provenance Activity | Evidence Traceability | Event | Pending | [Open](051-provenance-activity.md) |
| 52 | Data Quality Finding | Evidence Traceability | Subkind | Pending | [Open](052-data-quality-finding.md) |
| 53 | Identifier Value | Entity Identity | Datatype | Pending | [Open](053-identifier-value.md) |
| 54 | Identifier Scheme | Entity Identity | Kind | Pending | [Open](054-identifier-scheme.md) |
| 55 | Identifier Assignment | Entity Identity | Relator | Pending | [Open](055-identifier-assignment.md) |
| 56 | Entity Match Assertion | Entity Identity | Subkind | Pending | [Open](056-entity-match-assertion.md) |
| 57 | Match Confidence | Entity Identity | Quality | Pending | [Open](057-match-confidence.md) |
| 58 | Regulatory Requirement | Regulatory Policy | Kind | Pending | [Open](058-regulatory-requirement.md) |
| 59 | Regulatory Oversight | Regulatory Policy | Relator | Pending | [Open](059-regulatory-oversight.md) |
| 60 | Contextual Medicine Classification Assignment | Supply Resilience | Relator | Pending | [Open](060-contextual-medicine-classification-assignment.md) |
| 61 | Essential Medicine Classification Assignment | Supply Resilience | Subkind | Pending | [Open](061-essential-medicine-classification-assignment.md) |
| 62 | Critical Medicine Classification Assignment | Supply Resilience | Subkind | Pending | [Open](062-critical-medicine-classification-assignment.md) |
| 63 | Alternative Medicinal Product | Supply Resilience | Role | Pending | [Open](063-alternative-medicinal-product.md) |
| 64 | Alternative Medicinal Product Assignment | Supply Resilience | Relator | Pending | [Open](064-alternative-medicinal-product-assignment.md) |
| 65 | Supply Dependency | Supply Resilience | Relator | Pending | [Open](065-supply-dependency.md) |
| 66 | Disruption Event | Supply Resilience | Event | Pending | [Open](066-disruption-event.md) |
| 67 | Inventory Observation Result | Supply Resilience | Subkind | Pending | [Open](067-inventory-observation-result.md) |
| 68 | Procurement Activity | Supply Resilience | Event | Pending | [Open](068-procurement-activity.md) |
| 69 | Lead Time Observation Result | Supply Resilience | Subkind | Pending | [Open](069-lead-time-observation-result.md) |
| 70 | Stockout Situation | Supply Resilience | Situation | Pending | [Open](070-stockout-situation.md) |
| 71 | Healthcare Financing Organization | Market Access | Role | Pending | [Open](071-healthcare-financing-organization.md) |
| 72 | Reimbursement and Utilization Observation Result | Market Access | Subkind | Pending | [Open](072-reimbursement-and-utilization-observation-result.md) |
| 73 | Diagnosis Classification Reference | Market Access | Kind | Pending | [Open](073-diagnosis-classification-reference.md) |
| 74 | Asset at Risk | Risk Management | RoleMixin | Pending | [Open](074-asset-at-risk.md) |
| 75 | Risk Assessment Activity | Risk Management | Event | Pending | [Open](075-risk-assessment-activity.md) |
| 76 | Vulnerability | Risk Management | Mode | Pending | [Open](076-vulnerability.md) |
| 77 | Risk Treatment Plan | Risk Management | Kind | Pending | [Open](077-risk-treatment-plan.md) |
| 78 | Risk Treatment Activity | Risk Management | Event | Pending | [Open](078-risk-treatment-activity.md) |
| 79 | Pharmacovigilance Requirement | Pharmacovigilance | Kind | Pending | [Open](079-pharmacovigilance-requirement.md) |
| 80 | Adverse Event Reporting Activity | Pharmacovigilance | Event | Pending | [Open](080-adverse-event-reporting-activity.md) |
| 81 | Post-Market Surveillance Activity | Pharmacovigilance | Event | Pending | [Open](081-post-market-surveillance-activity.md) |
| 82 | Business Architecture View | Business Architecture | Kind | Pending | [Open](082-business-architecture-view.md) |
| 83 | Enterprise Capability | Business Architecture | Mode | Pending | [Open](083-enterprise-capability.md) |
| 84 | Strategic Partnership Agreement | Business Architecture | Relator | Pending | [Open](084-strategic-partnership-agreement.md) |
| 85 | Service Offering Specification | Business Architecture | Kind | Pending | [Open](085-service-offering-specification.md) |
| 86 | Digital System Component | Digital Systems | Kind | Pending | [Open](086-digital-system-component.md) |
| 87 | Clinical Care Participant | Clinical Care | RoleMixin | Pending | [Open](087-clinical-care-participant.md) |

## Coverage
- Instantiated: **87/87** concepts.
- Complete domains: **Ecosystem Organization 8/8; Facility Operations 4/4; Regulatory Governance 3/3; Pharmaceutical Product 10/10; Supply Operations 4/4; Ecosystem Observation 3/3; Spatiotemporal Context 7/7; Evidence Traceability 13/13; Entity Identity 5/5; Regulatory Policy 2/2; Supply Resilience 11/11; Market Access 3/3; Risk Management 5/5; Pharmacovigilance 3/3; Business Architecture 4/4; Digital Systems 1/1; Clinical Care 1/1**.
- Remaining: **0** concept passports. Relation review and the remaining Phase 2 HORP artifacts are tracked separately under #173.

## Evidence discipline
Each passport inherits its registered definition, stereotype, V1 lineage, dataset evidence, held-out evidence, support codes and IRI from the governed V2 provenance matrix. Missing concept-level external definitions are left as evidence gaps rather than inferred.

## Governed anchors
- [87-concept catalog](../index.md)
- [Concept provenance matrix](../../../research/w4/human-review-concept-provenance-matrix.md)
- [Integrated OntoUML model](../../../research/w4/integrated-ontouml-model.md)
- [HORP pilot control center](../../README.md)
