# V2 Database Reference

> **Version scope:** V2  
> **Status:** Reference implementation / Stable-to-date  
> **Updated:** 2026-09-24

This is the complete reader-facing reference for the current CM-PharmE PostgreSQL/PostGIS **research/reference realization**. It documents the implemented schema; it does not present the database as a deployed production system.

## Recomputed authoritative baseline
- **Tables:** 24
- **Columns:** 168
- **Foreign keys:** 31
- **CHECK constraints:** 11
- **UNIQUE constraints:** 29
- **Explicit indexes:** 5
- **SQL views:** 4 (not included in the 24-table count)
- **PostGIS:** enabled
- **Geometry columns:** 1
- **Authority:** `v2/data/db/schema.sql` at `v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999`

## Purpose and scope
The schema provides an executable relational twin of selected V2 semantic commitments: source/provenance lineage, geography, organizations/facilities, medicinal-product identity, identifiers/entity matching, classification, assertions/evidence, observations and shortage situations.

It is designed for research reproducibility, mapping/evaluation and demonstration. It is not evidence of production deployment, operational scale, clinical use or complete realization of all 87 conceptual elements.

## PostgreSQL/PostGIS role
PostgreSQL provides relational integrity, auditable keys/constraints and queryable reference data. PostGIS is enabled for the canonical geography table. The current spatial realization uses `geometry(Geometry,4326)` plus a GiST index and remains bounded to the implemented reference use cases.

## Ontology-alignment principles
- table names/foreign keys implement selected semantic elements but do not replace ontology definitions;
- mapping status is explicit in `v2/data/mappings/ontology-rdb-mapping.csv`;
- direct vs bounded/polymorphic/projection/deferred mappings remain distinguishable;
- Organization, Facility, Geography and RegulatoryJurisdiction remain separate;
- product/substance/presentation remain separate;
- identifiers are assignments, not identities;
- observations are aggregates and do not fabricate patient individuals.

## Provenance model
The principal lineage is:

Dataset → DatasetRelease → SourceRecord → TransformationRun / Assertion / EvidenceSupport → canonical/reference entities and observations.

See [[V2 Database ERD Suite]] and `v_provenance_lineage`.

## Identity and entity-match model
IdentifierAssignment separates scheme/value assignment from real-world entity identity. EntityMatchAssertion records source-record pairs, method, confidence and status; it does not silently merge source rows.

## Implementation boundaries
The schema does **not** instantiate every V2 concept. Current Resilience/Risk implementation is especially bounded: `medicine_shortage_situation` exists, while dedicated relational tables for SupplyDependency, Vulnerability, RiskAssessmentActivity or RiskTreatmentPlan/Activity are not present in this baseline.

## Table catalog — 24/24
| Table | Purpose | Columns | FKs | Ontology mapping |
|---|---|---:|---:|---|
| [[V2 DB Table dataset|dataset]] | Registered dataset identity and source-level metadata used by the reproducible ingestion/provenance layer. | 7 | 0 | direct |
| [[V2 DB Table dataset_release|dataset_release]] | Version/release identity for a dataset, including source filename and retrieval time. | 7 | 1 | direct |
| [[V2 DB Table transformation_run|transformation_run]] | Auditable transformation/provenance activity for an adapter execution. | 8 | 0 | direct |
| [[V2 DB Table source_record|source_record]] | Row-level source evidence with deterministic hash and transformation lineage. | 7 | 2 | direct |
| [[V2 DB Table geography|geography]] | Canonical geographic entity table with optional PostGIS geometry and supported geography subtype. | 9 | 0 | direct, polymorphic |
| [[V2 DB Table geography_alias|geography_alias]] | Source-specific geographic names/codes and auditable normalization/resolution confidence. | 8 | 2 | no direct registry row |
| [[V2 DB Table regulatory_jurisdiction|regulatory_jurisdiction]] | Regulatory jurisdiction identity kept explicitly separate from physical geography. | 5 | 1 | direct |
| [[V2 DB Table organization|organization]] | Canonical organization identity used by ecosystem and facility-operation relations. | 4 | 0 | direct |
| [[V2 DB Table facility|facility]] | Canonical physical/operational facility identity with optional geographic location. | 5 | 1 | direct |
| [[V2 DB Table facility_operation|facility_operation]] | Associative/relator realization connecting Organization and Facility with validity dates. | 7 | 2 | bounded, direct |
| [[V2 DB Table pharmaceutical_substance|pharmaceutical_substance]] | Canonical pharmaceutical substance identity. | 5 | 0 | direct |
| [[V2 DB Table medicinal_product|medicinal_product]] | Canonical medicinal-product identity with a bounded primary-substance hook. | 5 | 1 | bounded, direct |
| [[V2 DB Table product_presentation|product_presentation]] | Presentation/package-level medicinal-product identity and packaging/concentration fields. | 7 | 1 | direct |
| [[V2 DB Table identifier_scheme|identifier_scheme]] | Identifier-scheme identity kept separate from identifier lexical values. | 4 | 0 | direct |
| [[V2 DB Table identifier_assignment|identifier_assignment]] | Auditable assignment of an identifier value/scheme to a supported entity type. | 8 | 2 | direct |
| [[V2 DB Table product_classification_scheme|product_classification_scheme]] | Classification-scheme identity such as ATC or another product classification system. | 4 | 0 | direct |
| [[V2 DB Table classification_entry|classification_entry]] | Code/label entry within a product classification scheme. | 6 | 1 | direct |
| [[V2 DB Table product_classification_assignment|product_classification_assignment]] | Associative mapping between a medicinal product and a classification entry, with provenance hook. | 6 | 3 | direct |
| [[V2 DB Table diagnosis_reference|diagnosis_reference]] | Diagnosis-classification reference used by market-access/observation data. | 6 | 0 | direct |
| [[V2 DB Table assertion|assertion]] | Canonical assertion target for evidence/provenance linkage. | 8 | 0 | direct |
| [[V2 DB Table evidence_support|evidence_support]] | Relator/associative evidence link from SourceRecord to Assertion. | 5 | 2 | direct |
| [[V2 DB Table observation_result|observation_result]] | Polymorphic aggregate observation-result realization covering selected implemented observation kinds and measures. | 18 | 6 | bounded, one_to_many_rdf_projection, polymorphic |
| [[V2 DB Table entity_match_assertion|entity_match_assertion]] | Auditable entity-matching decision between two source records, including method, confidence and status. | 10 | 2 | direct, relational_projection |
| [[V2 DB Table medicine_shortage_situation|medicine_shortage_situation]] | Contextual medicine-shortage situation with optional product/presentation/jurisdiction/source evidence links. | 9 | 4 | direct |

## Derived SQL views — 4
| View | Source tables | Role |
|---|---|---|
| `v_product_presentations` | `identifier_assignment`, `identifier_scheme`, `medicinal_product`, `pharmaceutical_substance`, `product_presentation` | Product/presentation/substance + identifier read model. |
| `v_observations` | `dataset`, `dataset_release`, `diagnosis_reference`, `facility`, `geography`, `medicinal_product`, `observation_result`, `product_presentation`, `source_record` | Observation read model with product/facility/geography/diagnosis and source lineage. |
| `v_provenance_lineage` | `assertion`, `dataset`, `dataset_release`, `evidence_support`, `source_record`, `transformation_run` | Assertion→EvidenceSupport→SourceRecord→Release→Dataset→Transformation lineage. |
| `v_entity_matches` | `entity_match_assertion`, `source_record` | Entity-match review surface joining both source-record endpoints. |

Views are read/query surfaces and are not counted as physical tables.

## Data dictionary and mechanical evidence
- `wiki-src/database-reference/field-dictionary.csv`
- `wiki-src/database-reference/fk-coverage.csv`
- `wiki-src/database-reference/constraint-coverage.csv`
- `wiki-src/database-reference/schema-catalog.json`
- [[V2 Database ERD Suite]]

## Related semantic and query documentation
- [[V2 Ontology Reference]]
- [[V2 Data Infrastructure]]
- [[Knowledge Graph and Queries Guide]]
- [[V2 Evaluation E1-E13|CM-PharmE 2.0 Evaluation Framework]]

---

<details>
<summary>Documentation record</summary>

- **Page scope:** V2
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative source:** v2/data/db/schema.sql, views.sql and ontology↔RDB mapping registry
- **Last synchronized:** 2026-09-24
- **Last synchronized ref:** v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999
- **Related issues/PRs:** #205, #236
- **Evidence status:** Complete 24-table reference projection
- **Future refresh:** Re-run after authoritative schema changes
- **Wiki baseline:** WB-2026.09.1

</details>
