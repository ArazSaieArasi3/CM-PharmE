# regulatory_jurisdiction

> **Version scope:** V2  
> **Status:** Reference implementation  
> **Updated:** 2026-09-25

This page documents one implemented PostgreSQL/PostGIS table. It describes a research/reference realization and does not claim production deployment.

## Purpose
Regulatory jurisdiction kept semantically distinct from physical geography.

## Provenance role
No dedicated source-record FK; provenance follows linked ingestion/mapping context.

## Physical structure
| Column | SQL type | Nullable | Key / constraint | Default |
|---|---|---|---|---|
| `regulatory_jurisdiction_id` | `BIGSERIAL` | NO | PK | — |
| `public_id` | `TEXT` | NO | UNIQUE | — |
| `name` | `TEXT` | NO | — | — |
| `geography_id` | `BIGINT` | YES | FK to geography.geography_id | — |
| `ontology_iri` | `TEXT` | NO | — | `'https://w3id.org/cm-pharme/2.0/RegulatoryJurisdiction'` |

## Primary key
`regulatory_jurisdiction_id`

## Foreign keys
| FK column | References | Nullable |
|---|---|---|
| `geography_id` | `geography.geography_id` | YES |

## Incoming references
| Referencing table | FK column | Nullable |
|---|---|---|
| [[V2 Table medicine_shortage_situation|medicine_shortage_situation]] | `regulatory_jurisdiction_id` | YES |

## UNIQUE constraints
- `public_id`

## CHECK constraints
No CHECK constraint is declared.

## Explicit indexes
No explicit non-constraint index is declared.

## Ontology to RDB mapping
| Mapping | Ontology target | Kind | Status | RDB realization | Note |
|---|---|---|---|---|---|
| `M008` | `RegulatoryJurisdiction` | class | direct | `regulatory_jurisdiction_id` | Kept separate from physical geography |

See [[V2 Ontology Reference]] for semantic definitions. This page does not redefine ontology meaning.

## Safe synthetic example
The following values are illustrative only and are not empirical records.

| Field | Synthetic value |
|---|---|
| `regulatory_jurisdiction_id` | `101` |
| `public_id` | `example:regulatory_jurisdiction:001` |
| `geography_id` | `<geography.geography_id>` |
| `ontology_iri` | `https://w3id.org/cm-pharme/2.0/Example` |
| `name` | `Example Name` |

## Common join paths
- Child to parent: `regulatory_jurisdiction.geography_id` = `geography.geography_id`.
- Parent from child: `regulatory_jurisdiction.regulatory_jurisdiction_id` = `medicine_shortage_situation.regulatory_jurisdiction_id`.

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
