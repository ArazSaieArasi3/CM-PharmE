# medicine_shortage_situation

> **Version scope:** V2  
> **Status:** Reference implementation / Stable-to-date  
> **Updated:** 2026-09-24

> Generated physical-table reference from the authoritative PostgreSQL/PostGIS schema. It documents a research/reference realization and does **not** imply production deployment or production-scale performance.

## Purpose
Contextual medicine-shortage situation with optional product/presentation/jurisdiction/source evidence links.

## Keys and structure
- **Primary key:** `shortage_id`
- **Foreign keys:** 4
- **Provenance role:** shortage evidence via source_record_id

## Columns
| Column | Type | Null? | Key / constraint | Default |
|---|---|---|---|---|
| `shortage_id` | `BIGSERIAL` | No | PK | — |
| `public_id` | `TEXT` | No | UNIQUE | — |
| `medicinal_product_id` | `BIGINT` | Yes | FK → medicinal_product.medicinal_product_id | — |
| `product_presentation_id` | `BIGINT` | Yes | FK → product_presentation.product_presentation_id | — |
| `regulatory_jurisdiction_id` | `BIGINT` | Yes | FK → regulatory_jurisdiction.regulatory_jurisdiction_id | — |
| `starts_on` | `DATE` | Yes | — | — |
| `ends_on` | `DATE` | Yes | — | — |
| `source_record_id` | `BIGINT` | Yes | FK → source_record.source_record_id | — |
| `ontology_iri` | `TEXT` | No | — | `'https://w3id.org/cm-pharme/2.0/MedicineShortageSituation'` |

## Table-level constraints
- `CHECK (ends_on IS NULL OR starts_on IS NULL OR ends_on >= starts_on)`

## Explicit indexes
No explicit non-constraint index is declared for this table in the current schema.

## Ontology alignment
| Ontology IRI | Kind | Status | RDB field/join | Representation note |
|---|---|---|---|---|
| `https://w3id.org/cm-pharme/2.0/MedicineShortageSituation` | class | direct | `shortage_id/public_id` | Contextual shortage situation table |

See [[V2 Ontology Reference]] for semantic definitions. Mapping authority remains `v2/data/mappings/ontology-rdb-mapping.csv`.

## Common joins
- `medicine_shortage_situation.medicinal_product_id` → `medicinal_product.medicinal_product_id`
- `medicine_shortage_situation.product_presentation_id` → `product_presentation.product_presentation_id`
- `medicine_shortage_situation.regulatory_jurisdiction_id` → `regulatory_jurisdiction.regulatory_jurisdiction_id`
- `medicine_shortage_situation.source_record_id` → `source_record.source_record_id`

## Safe synthetic row fragment
`{"shortage_id": "1001", "public_id": "syn-medicine-shortage-situation-001", "medicinal_product_id": "1001", "product_presentation_id": "1001", "regulatory_jurisdiction_id": "1001", "starts_on": "2026-01-15", "ends_on": "2026-01-15", "source_record_id": "1001"}`

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
