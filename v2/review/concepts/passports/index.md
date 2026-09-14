---
artifact_type: concept_evidence_passport_registry
ontology_id: CM-PharmE
ontology_version: 2.0.0-alpha.1
review_status: active
passport_count: 25
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

## Coverage
- Instantiated: **25/87** concepts.
- Complete domains: **Ecosystem Organization 8/8; Facility Operations 4/4; Regulatory Governance 3/3; Pharmaceutical Product 10/10**.
- Remaining: **62** passports across the other 13 domains.

## Evidence discipline
Each passport inherits its registered definition, stereotype, V1 lineage, dataset evidence, held-out evidence, support codes and IRI from the governed V2 provenance matrix. Missing concept-level external definitions are left as evidence gaps rather than inferred.

## Governed anchors
- [87-concept catalog](../index.md)
- [Concept provenance matrix](../../../research/w4/human-review-concept-provenance-matrix.md)
- [Integrated OntoUML model](../../../research/w4/integrated-ontouml-model.md)
- [HORP pilot control center](../../README.md)
