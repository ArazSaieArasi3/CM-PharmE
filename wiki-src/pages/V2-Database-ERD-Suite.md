# V2 Database ERD Suite

> **Version scope:** V2  
> **Status:** Reference implementation  
> **Updated:** 2026-09-25

This suite documents the implemented V2 PostgreSQL/PostGIS reference schema at logical, full-physical and subject-area levels. The SQL DDL remains authoritative.

## Reading conventions
- Logical ERD: orientation-level simplification.
- Full physical ERD: all 24 base tables and every physical foreign key.
- Subject-area ERDs: readable local views of the same physical schema.
- Arrow direction: foreign-key table to referenced table.
- PK/FK/UK labels are physical-schema markers.
- No ERD layout creates ontology semantics.

## 1. V2 logical relational model — DGM-ERD-002

![DGM-ERD-002 V2 logical relational model](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/erd/DGM-ERD-002--v2-logical-relational-model.svg?sha=d5ae71259bf5)

Logical reader view of the principal V2 relational entities and implemented foreign-key structure.

Source: `wiki-src/diagrams/source/erd/DGM-ERD-002--v2-logical-relational-model.mmd`  
Rendered SVG: `wiki-src/diagrams/rendered/erd/DGM-ERD-002--v2-logical-relational-model.svg`

## 2. V2 full physical ERD — 24 tables — DGM-ERD-003

![DGM-ERD-003 V2 full physical ERD — 24 tables](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/erd/DGM-ERD-003--v2-full-physical-erd-24-tables.svg?sha=3249c374ff65)

Full physical ERD covering all 24 implemented base tables and every declared foreign key.

Source: `wiki-src/diagrams/source/erd/DGM-ERD-003--v2-full-physical-erd-24-tables.mmd`  
Rendered SVG: `wiki-src/diagrams/rendered/erd/DGM-ERD-003--v2-full-physical-erd-24-tables.svg`

## 3. Dataset / Release / Source / Transformation — DGM-ERD-004

![DGM-ERD-004 Dataset / Release / Source / Transformation](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/erd/DGM-ERD-004--dataset-release-source-transformation.svg?sha=0caa8269c9f0)

Readable subject-area ERD generated from the implemented V2 reference schema.

Source: `wiki-src/diagrams/source/erd/DGM-ERD-004--dataset-release-source-transformation.mmd`  
Rendered SVG: `wiki-src/diagrams/rendered/erd/DGM-ERD-004--dataset-release-source-transformation.svg`

## 4. Organization / Facility / Geography / Jurisdiction — DGM-ERD-005

![DGM-ERD-005 Organization / Facility / Geography / Jurisdiction](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/erd/DGM-ERD-005--organization-facility-geography-jurisdiction.svg?sha=92279fae275c)

Readable subject-area ERD generated from the implemented V2 reference schema.

Source: `wiki-src/diagrams/source/erd/DGM-ERD-005--organization-facility-geography-jurisdiction.mmd`  
Rendered SVG: `wiki-src/diagrams/rendered/erd/DGM-ERD-005--organization-facility-geography-jurisdiction.svg`

## 5. Product / Substance / Presentation / Classification — DGM-ERD-006

![DGM-ERD-006 Product / Substance / Presentation / Classification](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/erd/DGM-ERD-006--product-substance-presentation-classification.svg?sha=b2ccab78b7d4)

Readable subject-area ERD generated from the implemented V2 reference schema.

Source: `wiki-src/diagrams/source/erd/DGM-ERD-006--product-substance-presentation-classification.mmd`  
Rendered SVG: `wiki-src/diagrams/rendered/erd/DGM-ERD-006--product-substance-presentation-classification.svg`

## 6. Identifier / Identity / Entity Match — DGM-ERD-007

![DGM-ERD-007 Identifier / Identity / Entity Match](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/erd/DGM-ERD-007--identifier-identity-entity-match.svg?sha=ee7cf463182a)

Readable subject-area ERD generated from the implemented V2 reference schema.

Source: `wiki-src/diagrams/source/erd/DGM-ERD-007--identifier-identity-entity-match.mmd`  
Rendered SVG: `wiki-src/diagrams/rendered/erd/DGM-ERD-007--identifier-identity-entity-match.svg`

## 7. Assertion / Evidence / Provenance — DGM-ERD-008

![DGM-ERD-008 Assertion / Evidence / Provenance](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/erd/DGM-ERD-008--assertion-evidence-provenance.svg?sha=55dc2d6657ec)

Readable subject-area ERD generated from the implemented V2 reference schema.

Source: `wiki-src/diagrams/source/erd/DGM-ERD-008--assertion-evidence-provenance.mmd`  
Rendered SVG: `wiki-src/diagrams/rendered/erd/DGM-ERD-008--assertion-evidence-provenance.svg`

## 8. Observation — DGM-ERD-009

![DGM-ERD-009 Observation](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/erd/DGM-ERD-009--observation.svg?sha=d3bc1b57c35c)

Readable subject-area ERD generated from the implemented V2 reference schema.

Source: `wiki-src/diagrams/source/erd/DGM-ERD-009--observation.mmd`  
Rendered SVG: `wiki-src/diagrams/rendered/erd/DGM-ERD-009--observation.svg`

## 9. Shortage / Resilience-related implemented representation — DGM-ERD-010

![DGM-ERD-010 Shortage / Resilience-related implemented representation](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/erd/DGM-ERD-010--shortage-resilience-related-implemented-representation.svg?sha=4bd288cbcc20)

Readable subject-area ERD generated from the implemented V2 reference schema.

Source: `wiki-src/diagrams/source/erd/DGM-ERD-010--shortage-resilience-related-implemented-representation.mmd`  
Rendered SVG: `wiki-src/diagrams/rendered/erd/DGM-ERD-010--shortage-resilience-related-implemented-representation.svg`

## Coverage

- ERDs: **9/9**
- full physical tables: **24/24**
- full physical FK edges: **31/31**
- subject-area ERDs: **7/7**

## Boundary
These diagrams document a reference/research implementation. They do not demonstrate production scalability, availability, full-source ingestion or semantic superiority of the relational representation.

---

<details>
<summary>Documentation record</summary>

- **Page scope:** V2
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative source:** V2 PostgreSQL/PostGIS DDL
- **Last synchronized:** 2026-09-25
- **Last synchronized ref:** v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999
- **Related issues/PRs:** #232, #236, #237
- **Evidence status:** 9 governed ERDs generated from schema.sql
- **Future refresh:** #212 / #213 / #214 as applicable
- **Wiki baseline:** WB-2026.09.1

</details>
