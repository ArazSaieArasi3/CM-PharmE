# geography_alias

> **Version scope:** V2  
> **Status:** Reference implementation / Stable-to-date  
> **Updated:** 2026-09-24

> Generated physical-table reference from the authoritative PostgreSQL/PostGIS schema. It documents a research/reference realization and does **not** imply production deployment or production-scale performance.

## Purpose
Source-specific geographic names/codes and auditable normalization/resolution confidence.

## Keys and structure
- **Primary key:** `geography_alias_id`
- **Foreign keys:** 2
- **Provenance role:** normalization evidence via source_record_id

## Columns
| Column | Type | Null? | Key / constraint | Default |
|---|---|---|---|---|
| `geography_alias_id` | `BIGSERIAL` | No | PK | — |
| `geography_id` | `BIGINT` | No | FK → geography.geography_id | — |
| `source_system` | `TEXT` | No | — | — |
| `source_value` | `TEXT` | No | — | — |
| `normalized_value` | `TEXT` | No | — | — |
| `resolution_method` | `TEXT` | No | — | — |
| `confidence` | `NUMERIC(5,4)` | No | CHECK | — |
| `source_record_id` | `BIGINT` | Yes | FK → source_record.source_record_id | — |

## Table-level constraints
- `UNIQUE (source_system, source_value)`
- `CHECK confidence (confidence >= 0 AND confidence <= 1)`

## Explicit indexes
No explicit non-constraint index is declared for this table in the current schema.

## Ontology alignment
No direct row is currently registered for this table in the ontology↔RDB mapping registry. This absence must not be repaired by guessing.

See [[V2 Ontology Reference]] for semantic definitions. Mapping authority remains `v2/data/mappings/ontology-rdb-mapping.csv`.

## Common joins
- `geography_alias.geography_id` → `geography.geography_id`
- `geography_alias.source_record_id` → `source_record.source_record_id`

## Safe synthetic row fragment
`{"geography_alias_id": "1001", "geography_id": "1001", "source_system": "synthetic-source-system", "source_value": "synthetic-source-value", "normalized_value": "synthetic-normalized-value", "resolution_method": "synthetic-resolution-method", "confidence": "1.0", "source_record_id": "1001"}`

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
