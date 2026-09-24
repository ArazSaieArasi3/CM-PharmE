# product_classification_assignment

> **Version scope:** V2  
> **Status:** Reference implementation / Stable-to-date  
> **Updated:** 2026-09-24

> Generated physical-table reference from the authoritative PostgreSQL/PostGIS schema. It documents a research/reference realization and does **not** imply production deployment or production-scale performance.

## Purpose
Associative mapping between a medicinal product and a classification entry, with provenance hook.

## Keys and structure
- **Primary key:** `product_classification_assignment_id`
- **Foreign keys:** 3
- **Provenance role:** classification provenance via source_record_id

## Columns
| Column | Type | Null? | Key / constraint | Default |
|---|---|---|---|---|
| `product_classification_assignment_id` | `BIGSERIAL` | No | PK | — |
| `public_id` | `TEXT` | No | UNIQUE | — |
| `medicinal_product_id` | `BIGINT` | No | FK → medicinal_product.medicinal_product_id | — |
| `classification_entry_id` | `BIGINT` | No | FK → classification_entry.classification_entry_id | — |
| `source_record_id` | `BIGINT` | Yes | FK → source_record.source_record_id | — |
| `ontology_iri` | `TEXT` | No | — | `'https://w3id.org/cm-pharme/2.0/ProductClassificationAssignment'` |

## Table-level constraints
- `UNIQUE (medicinal_product_id, classification_entry_id)`

## Explicit indexes
No explicit non-constraint index is declared for this table in the current schema.

## Ontology alignment
| Ontology IRI | Kind | Status | RDB field/join | Representation note |
|---|---|---|---|---|
| `https://w3id.org/cm-pharme/2.0/ProductClassificationAssignment` | class | direct | `medicinal_product_id↔classification_entry_id` | Contextual assignment with provenance hook |

See [[V2 Ontology Reference]] for semantic definitions. Mapping authority remains `v2/data/mappings/ontology-rdb-mapping.csv`.

## Common joins
- `product_classification_assignment.medicinal_product_id` → `medicinal_product.medicinal_product_id`
- `product_classification_assignment.classification_entry_id` → `classification_entry.classification_entry_id`
- `product_classification_assignment.source_record_id` → `source_record.source_record_id`

## Safe synthetic row fragment
`{"product_classification_assignment_id": "1001", "public_id": "syn-product-classification-assignment-001", "medicinal_product_id": "1001", "classification_entry_id": "1001", "source_record_id": "1001", "ontology_iri": "https://w3id.org/cm-pharme/2.0/Example"}`

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
