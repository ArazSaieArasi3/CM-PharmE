# source_record

> **Version scope:** V2  
> **Status:** Reference implementation  
> **Updated:** 2026-09-25

This page documents one implemented PostgreSQL/PostGIS table. It describes a research/reference realization and does not claim production deployment.

## Purpose
Row-level admitted source record with deterministic content fingerprint and optional transformation provenance.

## Provenance role
Row-level evidence/provenance anchor.

## Physical structure
| Column | SQL type | Nullable | Key / constraint | Default |
|---|---|---|---|---|
| `source_record_id` | `BIGSERIAL` | NO | PK | — |
| `dataset_release_id` | `BIGINT` | NO | FK to dataset_release.dataset_release_id | — |
| `transformation_run_id` | `BIGINT` | YES | FK to transformation_run.transformation_run_id | — |
| `row_number` | `BIGINT` | NO | — | — |
| `source_hash` | `CHAR(64)` | NO | — | — |
| `raw_key` | `JSONB` | NO | — | `'{}'::jsonb` |
| `ontology_iri` | `TEXT` | NO | — | `'https://w3id.org/cm-pharme/2.0/SourceRecord'` |

## Primary key
`source_record_id`

## Foreign keys
| FK column | References | Nullable |
|---|---|---|
| `dataset_release_id` | `dataset_release.dataset_release_id` | NO |
| `transformation_run_id` | `transformation_run.transformation_run_id` | YES |

## Incoming references
| Referencing table | FK column | Nullable |
|---|---|---|
| [[V2 Table geography_alias|geography_alias]] | `source_record_id` | YES |
| [[V2 Table identifier_assignment|identifier_assignment]] | `source_record_id` | YES |
| [[V2 Table product_classification_assignment|product_classification_assignment]] | `source_record_id` | YES |
| [[V2 Table evidence_support|evidence_support]] | `source_record_id` | NO |
| [[V2 Table observation_result|observation_result]] | `source_record_id` | NO |
| [[V2 Table entity_match_assertion|entity_match_assertion]] | `source_record_a_id` | NO |
| [[V2 Table entity_match_assertion|entity_match_assertion]] | `source_record_b_id` | NO |
| [[V2 Table medicine_shortage_situation|medicine_shortage_situation]] | `source_record_id` | YES |

## UNIQUE constraints
- `dataset_release_id`, `row_number`, `source_hash`

## CHECK constraints
No CHECK constraint is declared.

## Explicit indexes
No explicit non-constraint index is declared.

## Ontology to RDB mapping
| Mapping | Ontology target | Kind | Status | RDB realization | Note |
|---|---|---|---|---|---|
| `M003` | `SourceRecord` | class | direct | `source_record_id/source_hash` | Source record has deterministic content fingerprint |

See [[V2 Ontology Reference]] for semantic definitions. This page does not redefine ontology meaning.

## Safe synthetic example
The following values are illustrative only and are not empirical records.

| Field | Synthetic value |
|---|---|
| `source_record_id` | `101` |
| `dataset_release_id` | `<dataset_release.dataset_release_id>` |
| `transformation_run_id` | `<transformation_run.transformation_run_id>` |
| `source_hash` | `0000000000000000000000000000000000000000000000000000000000000000` |
| `ontology_iri` | `https://w3id.org/cm-pharme/2.0/Example` |
| `row_number` | `101` |
| `raw_key` | `{"example": true}` |

## Common join paths
- Child to parent: `source_record.dataset_release_id` = `dataset_release.dataset_release_id`.
- Child to parent: `source_record.transformation_run_id` = `transformation_run.transformation_run_id`.
- Parent from child: `source_record.source_record_id` = `geography_alias.source_record_id`.
- Parent from child: `source_record.source_record_id` = `identifier_assignment.source_record_id`.
- Parent from child: `source_record.source_record_id` = `product_classification_assignment.source_record_id`.
- Parent from child: `source_record.source_record_id` = `evidence_support.source_record_id`.
- Parent from child: `source_record.source_record_id` = `observation_result.source_record_id`.

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
