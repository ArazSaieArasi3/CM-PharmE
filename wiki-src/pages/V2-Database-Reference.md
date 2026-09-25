# V2 Database Reference

> **Version scope:** V2  
> **Status:** Stable-to-date / Reference implementation  
> **Updated:** 2026-09-25

This is the master reference for the implemented CM-PharmE V2 PostgreSQL/PostGIS research database.

## Scope and authority
- authoritative DDL: `v2/data/db/schema.sql`
- authoritative query views: `v2/data/db/views.sql`
- ontology-to-RDB registry: `v2/data/mappings/ontology-rdb-mapping.csv`
- source-field registry: `v2/data/mappings/source-field-ontology-mapping.csv`
- checked ref: `v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999`

The ontology remains semantic authority. The database is an implementation representation, not a replacement conceptual model.

## Current physical baseline
- base tables: **24**
- query views: **4**
- primary keys: **24**
- foreign keys: **31**
- UNIQUE constraints: **29**
- CHECK constraints: **11**
- explicit indexes: **5**
- PostGIS extension: enabled in DDL
- spatial column: `geography.geom geometry(Geometry,4326)`

## Navigation
- [[V2 Database ERD Suite]]
- [[V2 Database Data Dictionary]]
- [[V2 Database Views]]
- [[V2 Data Infrastructure]]
- [[V2 Ontology Reference]]

## Table catalog
| Table | Purpose | PK | FKs | UNIQUE | CHECK | Indexes | Mapping rows |
|---|---|---|---:|---:|---:|---:|---:|
| [[V2 Table dataset|dataset]] | Dataset/source identity and source-role metadata. | `dataset_id` | 0 | 1 | 1 | 0 | 1 |
| [[V2 Table dataset_release|dataset_release]] | A versioned/retrieved release of a Dataset. | `dataset_release_id` | 1 | 1 | 0 | 0 | 1 |
| [[V2 Table transformation_run|transformation_run]] | Auditable ingestion/transformation execution represented as provenance activity. | `transformation_run_id` | 0 | 1 | 1 | 0 | 1 |
| [[V2 Table source_record|source_record]] | Row-level admitted source record with deterministic content fingerprint and optional transformation provenance. | `source_record_id` | 2 | 1 | 0 | 0 | 1 |
| [[V2 Table geography|geography]] | Canonical geographic feature store, including supported country/administrative-region types and PostGIS geometry. | `geography_id` | 0 | 1 | 1 | 2 | 3 |
| [[V2 Table geography_alias|geography_alias]] | Source-system geographic aliases and auditable normalization/resolution decisions. | `geography_alias_id` | 2 | 1 | 1 | 0 | 0 |
| [[V2 Table regulatory_jurisdiction|regulatory_jurisdiction]] | Regulatory jurisdiction kept semantically distinct from physical geography. | `regulatory_jurisdiction_id` | 1 | 1 | 0 | 0 | 1 |
| [[V2 Table organization|organization]] | Canonical organization identity. | `organization_id` | 0 | 1 | 0 | 0 | 1 |
| [[V2 Table facility|facility]] | Canonical physical/operational facility identity with optional physical geography. | `facility_id` | 1 | 1 | 0 | 0 | 2 |
| [[V2 Table facility_operation|facility_operation]] | Associative/relator table linking an Organization and Facility with optional validity interval. | `facility_operation_id` | 2 | 1 | 1 | 0 | 3 |
| [[V2 Table pharmaceutical_substance|pharmaceutical_substance]] | Canonical pharmaceutical-substance identity layer. | `substance_id` | 0 | 1 | 0 | 0 | 1 |
| [[V2 Table medicinal_product|medicinal_product]] | Canonical medicinal-product identity with a bounded primary-substance implementation hook. | `medicinal_product_id` | 1 | 1 | 0 | 0 | 2 |
| [[V2 Table product_presentation|product_presentation]] | Presentation/package-level medicinal-product identity and retained source presentation attributes. | `product_presentation_id` | 1 | 1 | 0 | 0 | 2 |
| [[V2 Table identifier_scheme|identifier_scheme]] | Identifier namespace/scheme definition. | `identifier_scheme_id` | 0 | 1 | 0 | 0 | 1 |
| [[V2 Table identifier_assignment|identifier_assignment]] | Scheme-scoped identifier assignment to a supported canonical entity; identifier value is not entity identity. | `identifier_assignment_id` | 2 | 2 | 1 | 0 | 2 |
| [[V2 Table product_classification_scheme|product_classification_scheme]] | Classification scheme such as ATC. | `classification_scheme_id` | 0 | 1 | 0 | 0 | 1 |
| [[V2 Table classification_entry|classification_entry]] | Code/label entry within a product-classification scheme. | `classification_entry_id` | 1 | 2 | 0 | 0 | 1 |
| [[V2 Table product_classification_assignment|product_classification_assignment]] | Provenance-aware assignment of a medicinal product to a classification entry. | `product_classification_assignment_id` | 3 | 2 | 0 | 0 | 1 |
| [[V2 Table diagnosis_reference|diagnosis_reference]] | Diagnosis-classification reference retained for market-access/reimbursement observations. | `diagnosis_reference_id` | 0 | 2 | 0 | 0 | 1 |
| [[V2 Table assertion|assertion]] | Canonical auditable assertion/evidence target. | `assertion_id` | 0 | 1 | 0 | 0 | 1 |
| [[V2 Table evidence_support|evidence_support]] | Relator linking a SourceRecord to an Assertion. | `evidence_support_id` | 2 | 2 | 0 | 0 | 1 |
| [[V2 Table observation_result|observation_result]] | Aggregate observation/result representation used by implemented source adapters; includes provenance and contextual hooks. | `observation_result_id` | 6 | 1 | 1 | 3 | 3 |
| [[V2 Table entity_match_assertion|entity_match_assertion]] | Auditable cross-source match assertion with method, confidence and disposition. | `entity_match_assertion_id` | 2 | 1 | 3 | 0 | 2 |
| [[V2 Table medicine_shortage_situation|medicine_shortage_situation]] | Contextual medicine-shortage situation linked to product/presentation/jurisdiction and optional source provenance. | `shortage_id` | 4 | 1 | 1 | 0 | 1 |

## PostgreSQL and PostGIS notes
The reference implementation uses PostgreSQL-specific BIGSERIAL, TIMESTAMPTZ, JSONB, partial indexes and PostGIS geometry. The GiST spatial index on geography supports spatial access. These choices do not establish production scalability, geocoding accuracy or operational service levels.

## Provenance model
Dataset to DatasetRelease to SourceRecord is the primary lineage chain, with optional TransformationRun provenance. EvidenceSupport connects SourceRecord to Assertion. ObservationResult requires SourceRecord and Assertion references. EntityMatchAssertion retains both source-record endpoints.

## Identity model
IdentifierScheme and IdentifierAssignment keep lexical identifiers separate from entity identity. EntityMatchAssertion stores method, confidence and disposition rather than silently merging source records.

## Protected distinctions preserved
- Organization is not Facility.
- Geography is not Regulatory Jurisdiction.
- Medicinal Product, Pharmaceutical Substance and Product Presentation remain distinct.
- Observation Result is not Source Record.
- Identifier assignment/value is not entity identity.

## Production boundary
The database is a reference/research realization. Deterministic fixtures do not demonstrate full-source ingestion, production deployment, real-world entity-resolution accuracy, global coverage or operational scalability.


---

<details>
<summary>Documentation record</summary>

- **Page scope:** V2
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative source:** V2 data infrastructure and PostgreSQL/PostGIS DDL
- **Last synchronized:** 2026-09-25
- **Last synchronized ref:** v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999
- **Related issues/PRs:** #236, #237
- **Evidence status:** Complete 24-table reference; ERD suite generated separately
- **Future refresh:** #212 / #213 / #214 as applicable
- **Wiki baseline:** WB-2026.09.1

</details>
