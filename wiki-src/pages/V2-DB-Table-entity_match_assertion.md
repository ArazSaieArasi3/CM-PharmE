# entity_match_assertion

> **Version scope:** V2  
> **Status:** Reference implementation / Stable-to-date  
> **Updated:** 2026-09-24

> Generated physical-table reference from the authoritative PostgreSQL/PostGIS schema. It documents a research/reference realization and does **not** imply production deployment or production-scale performance.

## Purpose
Auditable entity-matching decision between two source records, including method, confidence and status.

## Keys and structure
- **Primary key:** `entity_match_assertion_id`
- **Foreign keys:** 2
- **Provenance role:** matching provenance across two source records

## Columns
| Column | Type | Null? | Key / constraint | Default |
|---|---|---|---|---|
| `entity_match_assertion_id` | `BIGSERIAL` | No | PK | — |
| `public_id` | `TEXT` | No | UNIQUE | — |
| `source_record_a_id` | `BIGINT` | No | FK → source_record.source_record_id | — |
| `source_record_b_id` | `BIGINT` | No | FK → source_record.source_record_id | — |
| `matched_entity_type` | `TEXT` | No | — | — |
| `matched_public_id` | `TEXT` | No | — | — |
| `method` | `TEXT` | No | — | — |
| `confidence` | `NUMERIC(5,4)` | No | CHECK | — |
| `status` | `TEXT` | No | CHECK | — |
| `ontology_iri` | `TEXT` | No | — | `'https://w3id.org/cm-pharme/2.0/EntityMatchAssertion'` |

## Table-level constraints
- `CHECK (source_record_a_id <> source_record_b_id)`
- `CHECK confidence (confidence >= 0 AND confidence <= 1)`
- `CHECK status (status IN ('accepted','ambiguous','rejected'))`

## Explicit indexes
No explicit non-constraint index is declared for this table in the current schema.

## Ontology alignment
| Ontology IRI | Kind | Status | RDB field/join | Representation note |
|---|---|---|---|---|
| `https://w3id.org/cm-pharme/2.0/EntityMatchAssertion` | class | direct | `entity_match_assertion_id` | Auditable match assertion with method/confidence/status |
| `https://w3id.org/cm-pharme/2.0/MatchConfidence` | quality | relational_projection | `confidence` | Quality projected to bounded numeric field |

See [[V2 Ontology Reference]] for semantic definitions. Mapping authority remains `v2/data/mappings/ontology-rdb-mapping.csv`.

## Common joins
- `entity_match_assertion.source_record_a_id` → `source_record.source_record_id`
- `entity_match_assertion.source_record_b_id` → `source_record.source_record_id`

## Safe synthetic row fragment
`{"entity_match_assertion_id": "1001", "public_id": "syn-entity-match-assertion-001", "source_record_a_id": "1001", "source_record_b_id": "1001", "matched_entity_type": "synthetic-matched-entity-type", "matched_public_id": "synthetic-matched-public-id", "method": "synthetic-method", "confidence": "1.0"}`

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
