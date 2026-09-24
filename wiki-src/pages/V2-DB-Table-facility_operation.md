# facility_operation

> **Version scope:** V2  
> **Status:** Reference implementation / Stable-to-date  
> **Updated:** 2026-09-24

> Generated physical-table reference from the authoritative PostgreSQL/PostGIS schema. It documents a research/reference realization and does **not** imply production deployment or production-scale performance.

## Purpose
Associative/relator realization connecting Organization and Facility with validity dates.

## Keys and structure
- **Primary key:** `facility_operation_id`
- **Foreign keys:** 2
- **Provenance role:** No dedicated provenance role; provenance is reached through documented foreign-key paths where applicable.

## Columns
| Column | Type | Null? | Key / constraint | Default |
|---|---|---|---|---|
| `facility_operation_id` | `BIGSERIAL` | No | PK | — |
| `public_id` | `TEXT` | No | UNIQUE | — |
| `organization_id` | `BIGINT` | No | FK → organization.organization_id | — |
| `facility_id` | `BIGINT` | No | FK → facility.facility_id | — |
| `valid_from` | `DATE` | Yes | — | — |
| `valid_to` | `DATE` | Yes | — | — |
| `ontology_iri` | `TEXT` | No | — | `'https://w3id.org/cm-pharme/2.0/FacilityOperation'` |

## Table-level constraints
- `CHECK (valid_to IS NULL OR valid_from IS NULL OR valid_to >= valid_from)`

## Explicit indexes
No explicit non-constraint index is declared for this table in the current schema.

## Ontology alignment
| Ontology IRI | Kind | Status | RDB field/join | Representation note |
|---|---|---|---|---|
| `https://w3id.org/cm-pharme/2.0/FacilityOperation` | class | direct | `organization_id↔facility_id` | Relator represented as associative table with its own identity |
| `https://w3id.org/cm-pharme/2.0/validFrom` | datatype_property | bounded | `valid_from` | Temporal projection for relator validity |
| `https://w3id.org/cm-pharme/2.0/validTo` | datatype_property | bounded | `valid_to` | Temporal projection for relator validity |

See [[V2 Ontology Reference]] for semantic definitions. Mapping authority remains `v2/data/mappings/ontology-rdb-mapping.csv`.

## Common joins
- `facility_operation.organization_id` → `organization.organization_id`
- `facility_operation.facility_id` → `facility.facility_id`

## Safe synthetic row fragment
`{"facility_operation_id": "1001", "public_id": "syn-facility-operation-001", "organization_id": "1001", "facility_id": "1001", "valid_from": "2026-01-15", "valid_to": "2026-01-15", "ontology_iri": "https://w3id.org/cm-pharme/2.0/Example"}`

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
