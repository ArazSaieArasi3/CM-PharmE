# observation_result

> **Version scope:** V2  
> **Status:** Reference implementation  
> **Updated:** 2026-09-25

This page documents one implemented PostgreSQL/PostGIS table. It describes a research/reference realization and does not claim production deployment.

## Purpose
Aggregate observation/result representation used by implemented source adapters; includes provenance and contextual hooks.

## Provenance role
Required SourceRecord + Assertion provenance.

## Physical structure
| Column | SQL type | Nullable | Key / constraint | Default |
|---|---|---|---|---|
| `observation_result_id` | `BIGSERIAL` | NO | PK | — |
| `public_id` | `TEXT` | NO | UNIQUE | — |
| `observation_kind` | `TEXT` | NO | CHECK observation_kind IN ('availability','demand','supply_capacity','inventory','lead_time','reimbursement_utilisation') | — |
| `product_presentation_id` | `BIGINT` | YES | FK to product_presentation.product_presentation_id | — |
| `facility_id` | `BIGINT` | YES | FK to facility.facility_id | — |
| `geography_id` | `BIGINT` | YES | FK to geography.geography_id | — |
| `diagnosis_reference_id` | `BIGINT` | YES | FK to diagnosis_reference.diagnosis_reference_id | — |
| `reporting_period` | `DATE` | NO | — | — |
| `reporting_part` | `TEXT` | YES | — | — |
| `patient_count` | `NUMERIC` | YES | — | — |
| `package_count` | `NUMERIC` | YES | — | — |
| `cost_original` | `NUMERIC` | YES | — | — |
| `currency` | `CHAR(3)` | YES | — | — |
| `cost_bgn` | `NUMERIC` | YES | — | — |
| `cost_eur` | `NUMERIC` | YES | — | — |
| `source_record_id` | `BIGINT` | NO | FK to source_record.source_record_id | — |
| `assertion_id` | `BIGINT` | NO | FK to assertion.assertion_id | — |
| `ontology_iri` | `TEXT` | NO | — | `'https://w3id.org/cm-pharme/2.0/ReimbursementUtilisationObservationResult'` |

## Primary key
`observation_result_id`

## Foreign keys
| FK column | References | Nullable |
|---|---|---|
| `product_presentation_id` | `product_presentation.product_presentation_id` | YES |
| `facility_id` | `facility.facility_id` | YES |
| `geography_id` | `geography.geography_id` | YES |
| `diagnosis_reference_id` | `diagnosis_reference.diagnosis_reference_id` | YES |
| `source_record_id` | `source_record.source_record_id` | NO |
| `assertion_id` | `assertion.assertion_id` | NO |

## Incoming references
No implemented table references this table through a physical FK.

## UNIQUE constraints
- `public_id`

## CHECK constraints
- `observation_kind IN ('availability','demand','supply_capacity','inventory','lead_time','reimbursement_utilisation')`

## Explicit indexes
- **observation_period_idx** — BTREE on `reporting_period`
- **observation_geo_idx** — BTREE on `geography_id`
- **observation_presentation_idx** — BTREE on `product_presentation_id`

## Ontology to RDB mapping
| Mapping | Ontology target | Kind | Status | RDB realization | Note |
|---|---|---|---|---|---|
| `M026` | `ObservationResult` | class | polymorphic | `observation_result_id/public_id` | Relational source-level aggregate holds multiple measures and retains subtype through observation_kind/ontology_iri |
| `M027` | `ReimbursementUtilisationObservationResult` | class | one_to_many_rdf_projection | `observation_kind='reimbursement_utilisation'` | One source-level relational aggregate row is deterministically projected to separate RDF observation-result nodes per reported metric; no patient identity is created |
| `M028` | `observationResultAbout` | object_property | bounded | `product_presentation_id` | Reference implementation uses presentation as principal aboutness target |

See [[V2 Ontology Reference]] for semantic definitions. This page does not redefine ontology meaning.

## Safe synthetic example
The following values are illustrative only and are not empirical records.

| Field | Synthetic value |
|---|---|
| `observation_result_id` | `101` |
| `public_id` | `example:observation_result:001` |
| `observation_kind` | `availability` |
| `product_presentation_id` | `<product_presentation.product_presentation_id>` |
| `facility_id` | `<facility.facility_id>` |
| `geography_id` | `<geography.geography_id>` |
| `diagnosis_reference_id` | `<diagnosis_reference.diagnosis_reference_id>` |
| `reporting_period` | `2026-01-01` |
| `source_record_id` | `<source_record.source_record_id>` |
| `assertion_id` | `<assertion.assertion_id>` |

## Common join paths
- Child to parent: `observation_result.product_presentation_id` = `product_presentation.product_presentation_id`.
- Child to parent: `observation_result.facility_id` = `facility.facility_id`.
- Child to parent: `observation_result.geography_id` = `geography.geography_id`.
- Child to parent: `observation_result.diagnosis_reference_id` = `diagnosis_reference.diagnosis_reference_id`.
- Child to parent: `observation_result.source_record_id` = `source_record.source_record_id`.
- Child to parent: `observation_result.assertion_id` = `assertion.assertion_id`.

## Boundaries
- Reference/research realization only.
- Fixture rows are deterministic test data, not population evidence.
- Relational convenience must not collapse protected ontology distinctions.
- Missing mappings remain explicit rather than inferred.

## Authoritative sources
- v2/data/db/schema.sql
- v2/data/mappings/ontology-rdb-mapping.csv
- v2/data/mappings/source-field-ontology-mapping.csv


---

<details>
<summary>Documentation record</summary>

- **Page scope:** V2
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative source:** V2 PostgreSQL/PostGIS DDL and mapping registry
- **Last synchronized:** 2026-09-25
- **Last synchronized ref:** v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999
- **Related issues/PRs:** #236, #237
- **Evidence status:** Generated physical reference with curated purpose/provenance note
- **Future refresh:** #212 / #213 / #214 as applicable
- **Wiki baseline:** WB-2026.09.1

</details>
