# V2 Database ERD Suite

> **Version scope:** V2  
> **Status:** Reference implementation / Stable-to-date  
> **Updated:** 2026-09-24

This suite visualizes the current PostgreSQL/PostGIS reference schema. Logical and physical views are intentionally separate. The diagrams document an executable research/reference realization, not a production deployment.

## 1. Logical model — DGM-ERD-002

![Logical V2 relational model](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/erd/DGM-ERD-002--v2-logical-relational-model.svg)

A reader-oriented view of major implemented identities and lineage. It omits many physical columns/tables by design.

## 2. Full physical ERD — DGM-ERD-003

![Full physical V2 ERD](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/erd/DGM-ERD-003--v2-full-physical-erd-24-tables.svg)

All **24 physical tables** are represented. Every declared FK is represented in the source-derived physical model.

## Subject-area ERDs

### Dataset, Release, Source and Transformation — DGM-ERD-004

![Dataset, Release, Source and Transformation](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/erd/DGM-ERD-004--dataset-release-source-and-transformation.svg)

Show the source-ingestion and execution-provenance backbone.

[Source](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/source/erd/DGM-ERD-004--dataset-release-source-and-transformation.mmd) · [SVG](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/rendered/erd/DGM-ERD-004--dataset-release-source-and-transformation.svg)

### Organization, Facility, Geography and Jurisdiction — DGM-ERD-005

![Organization, Facility, Geography and Jurisdiction](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/erd/DGM-ERD-005--organization-facility-geography-and-jurisdiction.svg)

Show organization/facility identities, geographic normalization and regulatory-jurisdiction separation.

[Source](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/source/erd/DGM-ERD-005--organization-facility-geography-and-jurisdiction.mmd) · [SVG](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/rendered/erd/DGM-ERD-005--organization-facility-geography-and-jurisdiction.svg)

### Product, Substance, Presentation and Classification — DGM-ERD-006

![Product, Substance, Presentation and Classification](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/erd/DGM-ERD-006--product-substance-presentation-and-classification.svg)

Show product/substance/presentation identity and product-classification realization.

[Source](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/source/erd/DGM-ERD-006--product-substance-presentation-and-classification.mmd) · [SVG](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/rendered/erd/DGM-ERD-006--product-substance-presentation-and-classification.svg)

### Identifier, Identity and Entity Match — DGM-ERD-007

![Identifier, Identity and Entity Match](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/erd/DGM-ERD-007--identifier-identity-and-entity-match.svg)

Show identifier assignment and auditable entity matching without collapsing identifier values into entity identity.

[Source](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/source/erd/DGM-ERD-007--identifier-identity-and-entity-match.mmd) · [SVG](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/rendered/erd/DGM-ERD-007--identifier-identity-and-entity-match.svg)

### Assertion, Evidence and Provenance — DGM-ERD-008

![Assertion, Evidence and Provenance](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/erd/DGM-ERD-008--assertion-evidence-and-provenance.svg)

Show traceability from dataset/release/source row and transformation activity to assertions/evidence support.

[Source](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/source/erd/DGM-ERD-008--assertion-evidence-and-provenance.mmd) · [SVG](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/rendered/erd/DGM-ERD-008--assertion-evidence-and-provenance.svg)

### Observation — DGM-ERD-009

![Observation](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/erd/DGM-ERD-009--observation.svg)

Show the implemented observation aggregate and its contextual/provenance foreign keys.

[Source](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/source/erd/DGM-ERD-009--observation.mmd) · [SVG](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/rendered/erd/DGM-ERD-009--observation.svg)

### Shortage and Implemented Resilience-Related Data — DGM-ERD-010

![Shortage and Implemented Resilience-Related Data](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/erd/DGM-ERD-010--shortage-and-implemented-resilience-related-data.svg)

Show the implemented shortage realization. Dedicated SupplyDependency, Vulnerability and risk-treatment tables are not present in the current schema.

[Source](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/source/erd/DGM-ERD-010--shortage-and-implemented-resilience-related-data.mmd) · [SVG](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/rendered/erd/DGM-ERD-010--shortage-and-implemented-resilience-related-data.svg)

## Cardinality convention
The source is generated from physical FK nullability:
- a NOT NULL FK means each child row requires exactly one referenced parent;
- a nullable FK allows zero-or-one referenced parent;
- the parent side is zero-to-many child rows unless another constraint says otherwise.

No cardinality is invented beyond schema constraints.

## Resilience boundary
The shortage subject-area diagram shows only implemented relational structures. The current schema has `medicine_shortage_situation` but no dedicated tables for SupplyDependency, Vulnerability, RiskAssessmentActivity or RiskTreatmentPlan/Activity.

## Mechanical coverage
- physical tables: **24/24**
- foreign keys: **31**
- subject-area diagrams: **7**
- logical + physical + subject diagrams: **9**
- PostGIS geometry: `geography.geom geometry(Geometry,4326)`
- explicit indexes: **5**

See [[V2 Database Reference]] for the field/table catalog and mapping links.

---

<details>
<summary>Documentation record</summary>

- **Page scope:** V2
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative source:** v2/data/db/schema.sql
- **Last synchronized:** 2026-09-24
- **Last synchronized ref:** v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999
- **Related issues/PRs:** #205, #236
- **Evidence status:** Nine schema-derived ERDs; logical/physical distinction preserved
- **Future refresh:** Re-run after authoritative schema changes
- **Wiki baseline:** WB-2026.09.1

</details>
