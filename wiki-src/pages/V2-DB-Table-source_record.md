# source_record

> **Version scope:** V2  
> **Status:** Reference implementation / Stable-to-date  
> **Updated:** 2026-09-24

> Generated physical-table reference from the authoritative PostgreSQL/PostGIS schema. It documents a research/reference realization and does **not** imply production deployment or production-scale performance.

## Purpose
Row-level source evidence with deterministic hash and transformation lineage.

## Keys and structure
- **Primary key:** `source_record_id`
- **Foreign keys:** 2
- **Provenance role:** row-level provenance anchor

## Columns
| Column | Type | Null? | Key / constraint | Default |
|---|---|---|---|---|
| `source_record_id` | `BIGSERIAL` | No | PK | — |
| `dataset_release_id` | `BIGINT` | No | FK → dataset_release.dataset_release_id | — |
| `transformation_run_id` | `BIGINT` | Yes | FK → transformation_run.transformation_run_id | — |
| `row_number` | `BIGINT` | No | — | — |
| `source_hash` | `CHAR(64)` | No | — | — |
| `raw_key` | `JSONB` | No | — | `'{}'::jsonb` |
| `ontology_iri` | `TEXT` | No | — | `'https://w3id.org/cm-pharme/2.0/SourceRecord'` |

## Table-level constraints
- `UNIQUE (dataset_release_id, row_number, source_hash)`

## Explicit indexes
No explicit non-constraint index is declared for this table in the current schema.

## Ontology alignment
| Ontology IRI | Kind | Status | RDB field/join | Representation note |
|---|---|---|---|---|
| `https://w3id.org/cm-pharme/2.0/SourceRecord` | class | direct | `source_record_id/source_hash` | Source record has deterministic content fingerprint |

See [[V2 Ontology Reference]] for semantic definitions. Mapping authority remains `v2/data/mappings/ontology-rdb-mapping.csv`.

## Common joins
- `source_record.dataset_release_id` → `dataset_release.dataset_release_id`
- `source_record.transformation_run_id` → `transformation_run.transformation_run_id`

## Safe synthetic row fragment
`{"source_record_id": "1001", "dataset_release_id": "1001", "transformation_run_id": "1001", "row_number": "1001", "source_hash": "0000000000000000000000000000000000000000000000000000000000000000", "raw_key": "{\"synthetic\": true}", "ontology_iri": "https://w3id.org/cm-pharme/2.0/Example"}`

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
