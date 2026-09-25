# geography_alias

> **Version scope:** V2  
> **Status:** Reference implementation  
> **Updated:** 2026-09-25

This page documents one implemented PostgreSQL/PostGIS table. It describes a research/reference realization and does not claim production deployment.

## Purpose
Source-system geographic aliases and auditable normalization/resolution decisions.

## Provenance role
Records source alias, resolution method, confidence and optional SourceRecord.

## Physical structure
| Column | SQL type | Nullable | Key / constraint | Default |
|---|---|---|---|---|
| `geography_alias_id` | `BIGSERIAL` | NO | PK | — |
| `geography_id` | `BIGINT` | NO | FK to geography.geography_id | — |
| `source_system` | `TEXT` | NO | — | — |
| `source_value` | `TEXT` | NO | — | — |
| `normalized_value` | `TEXT` | NO | — | — |
| `resolution_method` | `TEXT` | NO | — | — |
| `confidence` | `NUMERIC(5,4)` | NO | CHECK confidence >= 0 AND confidence <= 1 | — |
| `source_record_id` | `BIGINT` | YES | FK to source_record.source_record_id | — |

## Primary key
`geography_alias_id`

## Foreign keys
| FK column | References | Nullable |
|---|---|---|
| `geography_id` | `geography.geography_id` | NO |
| `source_record_id` | `source_record.source_record_id` | YES |

## Incoming references
No implemented table references this table through a physical FK.

## UNIQUE constraints
- `source_system`, `source_value`

## CHECK constraints
- `confidence >= 0 AND confidence <= 1`

## Explicit indexes
No explicit non-constraint index is declared.

## Ontology to RDB mapping
No direct row in the current ontology-to-RDB registry targets this table. No mapping is inferred from the table name.

See [[V2 Ontology Reference]] for semantic definitions. This page does not redefine ontology meaning.

## Safe synthetic example
The following values are illustrative only and are not empirical records.

| Field | Synthetic value |
|---|---|
| `geography_alias_id` | `101` |
| `geography_id` | `<geography.geography_id>` |
| `confidence` | `0.9500` |
| `source_record_id` | `<source_record.source_record_id>` |
| `source_system` | `example` |
| `source_value` | `example` |
| `normalized_value` | `example` |

## Common join paths
- Child to parent: `geography_alias.geography_id` = `geography.geography_id`.
- Child to parent: `geography_alias.source_record_id` = `source_record.source_record_id`.

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
