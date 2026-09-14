---
artifact_type: concept_evidence_passport_registry
ontology_id: CM-PharmE
ontology_version: 2.0.0-alpha.1
review_status: active
passport_count: 8
planned_passport_count: 87
---

# CM-PharmE 2.0 — Concept Evidence Passport Registry

This registry instantiates Phase 2 of #173 using the canonical OGCM-RF Concept Evidence Passport pattern. Passports are review projections over governed V2 evidence; they do not create new semantic authority or imply human approval.

## Current instantiated batch — Ecosystem Organization

| # | Concept | Stereotype | Review status | Passport |
|---:|---|---|---|---|
| 1 | Organization | Kind | Pending | [Open](001-organization.md) |
| 2 | Ecosystem Participant | RoleMixin | Pending | [Open](002-ecosystem-participant.md) |
| 3 | Regulatory Authority | Role | Pending | [Open](003-regulatory-authority.md) |
| 4 | Manufacturer | Role | Pending | [Open](004-manufacturer.md) |
| 5 | Importer | Role | Pending | [Open](005-importer.md) |
| 6 | Product Responsible Organization | Role | Pending | [Open](006-product-responsible-organization.md) |
| 7 | Wholesale Distributor | Role | Pending | [Open](007-wholesale-distributor.md) |
| 8 | Third-Party Logistics Provider | Role | Pending | [Open](008-third-party-logistics-provider.md) |

## Coverage
- Instantiated: **8/87** concepts.
- Domain coverage in this batch: **Ecosystem Organization 8/8**.
- Remaining: **79** passports across the other 16 domains.

## Evidence discipline
Each passport inherits its registered definition, stereotype, V1 lineage, dataset evidence, held-out evidence, support codes and IRI from the governed V2 provenance matrix. Missing concept-level external definitions are left as evidence gaps rather than inferred.

## Governed anchors
- [87-concept catalog](../index.md)
- [Concept provenance matrix](../../../research/w4/human-review-concept-provenance-matrix.md)
- [Integrated OntoUML model](../../../research/w4/integrated-ontouml-model.md)
- [HORP pilot control center](../../README.md)
