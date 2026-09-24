# observation_result

> **Version scope:** V2  
> **Status:** Reference implementation / Stable-to-date  
> **Updated:** 2026-09-24

> Generated physical-table reference from the authoritative PostgreSQL/PostGIS schema. It documents a research/reference realization and does **not** imply production deployment or production-scale performance.

## Purpose
Polymorphic aggregate observation-result realization covering selected implemented observation kinds and measures.

## Keys and structure
- **Primary key:** `observation_result_id`
- **Foreign keys:** 6
- **Provenance role:** observation provenance via source_record_id + assertion_id

## Columns
| Column | Type | Null? | Key / constraint | Default |
|---|---|---|---|---|
| `observation_result_id` | `BIGSERIAL` | No | PK | — |
| `public_id` | `TEXT` | No | UNIQUE | — |
| `observation_kind` | `TEXT` | No | CHECK | — |
| `product_presentation_id` | `BIGINT` | Yes | FK → product_presentation.product_presentation_id | — |
| `facility_id` | `BIGINT` | Yes | FK → facility.facility_id | — |
| `geography_id` | `BIGINT` | Yes | FK → geography.geography_id | — |
| `diagnosis_reference_id` | `BIGINT` | Yes | FK → diagnosis_reference.diagnosis_reference_id | — |
| `reporting_period` | `DATE` | No | — | — |
| `reporting_part` | `TEXT` | Yes | — | — |
| `patient_count` | `NUMERIC` | Yes | — | — |
| `package_count` | `NUMERIC` | Yes | — | — |
| `cost_original` | `NUMERIC` | Yes | — | — |
| `currency` | `CHAR(3)` | Yes | — | — |
| `cost_bgn` | `NUMERIC` | Yes | — | — |
| `cost_eur` | `NUMERIC` | Yes | — | — |
| `source_record_id` | `BIGINT` | No | FK → source_record.source_record_id | — |
| `assertion_id` | `BIGINT` | No | FK → assertion.assertion_id | — |
| `ontology_iri` | `TEXT` | No | — | `'https://w3id.org/cm-pharme/2.0/ReimbursementUtilisationObservationResult'` |

## Table-level constraints
- `CHECK observation_kind (observation_kind IN ('availability','demand','supply_capacity','inventory','lead_time','reimbursement_utilisation'))`

## Explicit indexes
| Index | Method | Columns | Predicate |
|---|---|---|---|
| `observation_period_idx` | btree(default) | `reporting_period` | — |
| `observation_geo_idx` | btree(default) | `geography_id` | — |
| `observation_presentation_idx` | btree(default) | `product_presentation_id` | — |

## Ontology alignment
| Ontology IRI | Kind | Status | RDB field/join | Representation note |
|---|---|---|---|---|
| `https://w3id.org/cm-pharme/2.0/ObservationResult` | class | polymorphic | `observation_result_id/public_id` | Relational source-level aggregate holds multiple measures and retains subtype through observation_kind/ontology_iri |
| `https://w3id.org/cm-pharme/2.0/ReimbursementUtilisationObservationResult` | class | one_to_many_rdf_projection | `observation_kind='reimbursement_utilisation'` | One source-level relational aggregate row is deterministically projected to separate RDF observation-result nodes per reported metric; no patient identity is created |
| `https://w3id.org/cm-pharme/2.0/observationResultAbout` | object_property | bounded | `product_presentation_id` | Reference implementation uses presentation as principal aboutness target |

See [[V2 Ontology Reference]] for semantic definitions. Mapping authority remains `v2/data/mappings/ontology-rdb-mapping.csv`.

## Common joins
- `observation_result.product_presentation_id` → `product_presentation.product_presentation_id`
- `observation_result.facility_id` → `facility.facility_id`
- `observation_result.geography_id` → `geography.geography_id`
- `observation_result.diagnosis_reference_id` → `diagnosis_reference.diagnosis_reference_id`
- `observation_result.source_record_id` → `source_record.source_record_id`
- `observation_result.assertion_id` → `assertion.assertion_id`

## Safe synthetic row fragment
`{"observation_result_id": "1001", "public_id": "syn-observation-result-001", "observation_kind": "availability", "product_presentation_id": "1001", "facility_id": "1001", "geography_id": "1001", "diagnosis_reference_id": "1001", "reporting_period": "2026-01-15"}`

This example is synthetic and exists only to clarify field shape.

## Boundaries
- This table belongs to a reproducible **reference implementation**, not a production claim.
- Relational representation may be direct, bounded, polymorphic, relational-projection or deferred as stated in the mapping registry.
- The table definition does not redefine ontology semantics.

---

<details>
<summary>Documentation record</summary>

- **Page scope:** V2
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative source:** v2/data/db/schema.sql + ontology↔RDB mapping registry
- **Last synchronized:** 2026-09-24
- **Last synchronized ref:** v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999
- **Related issues/PRs:** #205, #236
- **Evidence status:** Generated table reference; reference-implementation boundary preserved
- **Future refresh:** Re-run after authoritative schema changes
- **Wiki baseline:** WB-2026.09.1

</details>
