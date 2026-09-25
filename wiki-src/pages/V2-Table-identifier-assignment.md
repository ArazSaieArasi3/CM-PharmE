# identifier_assignment

> **Version scope:** V2  
> **Status:** Reference implementation  
> **Updated:** 2026-09-25

This page documents one implemented PostgreSQL/PostGIS table. It describes a research/reference realization and does not claim production deployment.

## Purpose
Scheme-scoped identifier assignment to a supported canonical entity; identifier value is not entity identity.

## Provenance role
Optional SourceRecord provenance for identifier assignment.

## Physical structure
| Column | SQL type | Nullable | Key / constraint | Default |
|---|---|---|---|---|
| `identifier_assignment_id` | `BIGSERIAL` | NO | PK | — |
| `public_id` | `TEXT` | NO | UNIQUE | — |
| `identifier_scheme_id` | `BIGINT` | NO | FK to identifier_scheme.identifier_scheme_id | — |
| `entity_type` | `TEXT` | NO | CHECK entity_type IN ('organization','facility','medicinal_product','product_presentation','substance','geography') | — |
| `entity_public_id` | `TEXT` | NO | — | — |
| `lexical_value` | `TEXT` | NO | — | — |
| `source_record_id` | `BIGINT` | YES | FK to source_record.source_record_id | — |
| `ontology_iri` | `TEXT` | NO | — | `'https://w3id.org/cm-pharme/2.0/IdentifierAssignment'` |

## Primary key
`identifier_assignment_id`

## Foreign keys
| FK column | References | Nullable |
|---|---|---|
| `identifier_scheme_id` | `identifier_scheme.identifier_scheme_id` | NO |
| `source_record_id` | `source_record.source_record_id` | YES |

## Incoming references
No implemented table references this table through a physical FK.

## UNIQUE constraints
- `public_id`
- `identifier_scheme_id`, `lexical_value`, `entity_type`, `entity_public_id`

## CHECK constraints
- `entity_type IN ('organization','facility','medicinal_product','product_presentation','substance','geography')`

## Explicit indexes
No explicit non-constraint index is declared.

## Ontology to RDB mapping
| Mapping | Ontology target | Kind | Status | RDB realization | Note |
|---|---|---|---|---|---|
| `M021` | `IdentifierAssignment` | class | direct | `entity_public_id+lexical_value` | Identifier assignment does not become entity identity |
| `M032` | `identifierLexicalValue` | datatype_property | direct | `lexical_value` | Lexical identifier stored separately from entity key |

See [[V2 Ontology Reference]] for semantic definitions. This page does not redefine ontology meaning.

## Safe synthetic example
The following values are illustrative only and are not empirical records.

| Field | Synthetic value |
|---|---|
| `identifier_assignment_id` | `101` |
| `public_id` | `example:identifier_assignment:001` |
| `identifier_scheme_id` | `<identifier_scheme.identifier_scheme_id>` |
| `entity_type` | `facility` |
| `source_record_id` | `<source_record.source_record_id>` |
| `ontology_iri` | `https://w3id.org/cm-pharme/2.0/Example` |
| `entity_public_id` | `example` |

## Common join paths
- Child to parent: `identifier_assignment.identifier_scheme_id` = `identifier_scheme.identifier_scheme_id`.
- Child to parent: `identifier_assignment.source_record_id` = `source_record.source_record_id`.

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
