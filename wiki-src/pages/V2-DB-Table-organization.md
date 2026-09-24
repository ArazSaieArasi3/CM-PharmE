# organization

> **Version scope:** V2  
> **Status:** Reference implementation / Stable-to-date  
> **Updated:** 2026-09-24

> Generated physical-table reference from the authoritative PostgreSQL/PostGIS schema. It documents a research/reference realization and does **not** imply production deployment or production-scale performance.

## Purpose
Canonical organization identity used by ecosystem and facility-operation relations.

## Keys and structure
- **Primary key:** `organization_id`
- **Foreign keys:** 0
- **Provenance role:** No dedicated provenance role; provenance is reached through documented foreign-key paths where applicable.

## Columns
| Column | Type | Null? | Key / constraint | Default |
|---|---|---|---|---|
| `organization_id` | `BIGSERIAL` | No | PK | — |
| `public_id` | `TEXT` | No | UNIQUE | — |
| `preferred_name` | `TEXT` | No | — | — |
| `ontology_iri` | `TEXT` | No | — | `'https://w3id.org/cm-pharme/2.0/Organization'` |

## Table-level constraints
No table-level UNIQUE/CHECK constraint beyond column-level key/nullability declarations.

## Explicit indexes
No explicit non-constraint index is declared for this table in the current schema.

## Ontology alignment
| Ontology IRI | Kind | Status | RDB field/join | Representation note |
|---|---|---|---|---|
| `https://w3id.org/cm-pharme/2.0/Organization` | class | direct | `organization_id/public_id` | Organization identity not collapsed into Facility |

See [[V2 Ontology Reference]] for semantic definitions. Mapping authority remains `v2/data/mappings/ontology-rdb-mapping.csv`.

## Common joins
No outgoing foreign-key join is declared from this table.

## Safe synthetic row fragment
`{"organization_id": "1001", "public_id": "syn-organization-001", "preferred_name": "synthetic-preferred-name", "ontology_iri": "https://w3id.org/cm-pharme/2.0/Example"}`

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
