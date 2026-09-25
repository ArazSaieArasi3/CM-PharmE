# facility

> **Version scope:** V2  
> **Status:** Reference implementation  
> **Updated:** 2026-09-25

This page documents one implemented PostgreSQL/PostGIS table. It describes a research/reference realization and does not claim production deployment.

## Purpose
Canonical physical/operational facility identity with optional physical geography.

## Provenance role
Canonical entity; source provenance follows identifiers/observations/mappings where created.

## Physical structure
| Column | SQL type | Nullable | Key / constraint | Default |
|---|---|---|---|---|
| `facility_id` | `BIGSERIAL` | NO | PK | — |
| `public_id` | `TEXT` | NO | UNIQUE | — |
| `preferred_name` | `TEXT` | NO | — | — |
| `geography_id` | `BIGINT` | YES | FK to geography.geography_id | — |
| `ontology_iri` | `TEXT` | NO | — | `'https://w3id.org/cm-pharme/2.0/Facility'` |

## Primary key
`facility_id`

## Foreign keys
| FK column | References | Nullable |
|---|---|---|
| `geography_id` | `geography.geography_id` | YES |

## Incoming references
| Referencing table | FK column | Nullable |
|---|---|---|
| [[V2 Table facility_operation|facility_operation]] | `facility_id` | NO |
| [[V2 Table observation_result|observation_result]] | `facility_id` | YES |

## UNIQUE constraints
- `public_id`

## CHECK constraints
No CHECK constraint is declared.

## Explicit indexes
No explicit non-constraint index is declared.

## Ontology to RDB mapping
| Mapping | Ontology target | Kind | Status | RDB realization | Note |
|---|---|---|---|---|---|
| `M010` | `Facility` | class | direct | `facility_id/public_id` | Physical/operational facility identity |
| `M031` | `locatedIn` | object_property | direct | `geography_id` | Facility physical location; not regulatory jurisdiction |

See [[V2 Ontology Reference]] for semantic definitions. This page does not redefine ontology meaning.

## Safe synthetic example
The following values are illustrative only and are not empirical records.

| Field | Synthetic value |
|---|---|
| `facility_id` | `101` |
| `public_id` | `example:facility:001` |
| `preferred_name` | `Example Preferred Name` |
| `geography_id` | `<geography.geography_id>` |
| `ontology_iri` | `https://w3id.org/cm-pharme/2.0/Example` |

## Common join paths
- Child to parent: `facility.geography_id` = `geography.geography_id`.
- Parent from child: `facility.facility_id` = `facility_operation.facility_id`.
- Parent from child: `facility.facility_id` = `observation_result.facility_id`.

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
