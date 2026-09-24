# identifier_assignment

> **Version scope:** V2  
> **Status:** Reference implementation / Stable-to-date  
> **Updated:** 2026-09-24

> Generated physical-table reference from the authoritative PostgreSQL/PostGIS schema. It documents a research/reference realization and does **not** imply production deployment or production-scale performance.

## Purpose
Auditable assignment of an identifier value/scheme to a supported entity type.

## Keys and structure
- **Primary key:** `identifier_assignment_id`
- **Foreign keys:** 2
- **Provenance role:** identifier provenance via source_record_id

## Columns
| Column | Type | Null? | Key / constraint | Default |
|---|---|---|---|---|
| `identifier_assignment_id` | `BIGSERIAL` | No | PK | — |
| `public_id` | `TEXT` | No | UNIQUE | — |
| `identifier_scheme_id` | `BIGINT` | No | FK → identifier_scheme.identifier_scheme_id | — |
| `entity_type` | `TEXT` | No | CHECK | — |
| `entity_public_id` | `TEXT` | No | — | — |
| `lexical_value` | `TEXT` | No | — | — |
| `source_record_id` | `BIGINT` | Yes | FK → source_record.source_record_id | — |
| `ontology_iri` | `TEXT` | No | — | `'https://w3id.org/cm-pharme/2.0/IdentifierAssignment'` |

## Table-level constraints
- `UNIQUE (identifier_scheme_id, lexical_value, entity_type, entity_public_id)`
- `CHECK entity_type (entity_type IN ('organization','facility','medicinal_product','product_presentation','substance','geography'))`

## Explicit indexes
No explicit non-constraint index is declared for this table in the current schema.

## Ontology alignment
| Ontology IRI | Kind | Status | RDB field/join | Representation note |
|---|---|---|---|---|
| `https://w3id.org/cm-pharme/2.0/IdentifierAssignment` | class | direct | `entity_public_id+lexical_value` | Identifier assignment does not become entity identity |
| `https://w3id.org/cm-pharme/2.0/identifierLexicalValue` | datatype_property | direct | `lexical_value` | Lexical identifier stored separately from entity key |

See [[V2 Ontology Reference]] for semantic definitions. Mapping authority remains `v2/data/mappings/ontology-rdb-mapping.csv`.

## Common joins
- `identifier_assignment.identifier_scheme_id` → `identifier_scheme.identifier_scheme_id`
- `identifier_assignment.source_record_id` → `source_record.source_record_id`

## Safe synthetic row fragment
`{"identifier_assignment_id": "1001", "public_id": "syn-identifier-assignment-001", "identifier_scheme_id": "1001", "entity_type": "organization", "entity_public_id": "synthetic-entity-public-id", "lexical_value": "synthetic-lexical-value", "source_record_id": "1001", "ontology_iri": "https://w3id.org/cm-pharme/2.0/Example"}`

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
