# facility_operation

> **Version scope:** V2  
> **Status:** Reference implementation  
> **Updated:** 2026-09-25

This page documents one implemented PostgreSQL/PostGIS table. It describes a research/reference realization and does not claim production deployment.

## Purpose
Associative/relator table linking an Organization and Facility with optional validity interval.

## Provenance role
Temporal relational implementation; no direct source-record FK.

## Physical structure
| Column | SQL type | Nullable | Key / constraint | Default |
|---|---|---|---|---|
| `facility_operation_id` | `BIGSERIAL` | NO | PK | — |
| `public_id` | `TEXT` | NO | UNIQUE | — |
| `organization_id` | `BIGINT` | NO | FK to organization.organization_id | — |
| `facility_id` | `BIGINT` | NO | FK to facility.facility_id | — |
| `valid_from` | `DATE` | YES | — | — |
| `valid_to` | `DATE` | YES | — | — |
| `ontology_iri` | `TEXT` | NO | — | `'https://w3id.org/cm-pharme/2.0/FacilityOperation'` |

## Primary key
`facility_operation_id`

## Foreign keys
| FK column | References | Nullable |
|---|---|---|
| `organization_id` | `organization.organization_id` | NO |
| `facility_id` | `facility.facility_id` | NO |

## Incoming references
No implemented table references this table through a physical FK.

## UNIQUE constraints
- `public_id`

## CHECK constraints
- `valid_to IS NULL OR valid_from IS NULL OR valid_to >= valid_from`

## Explicit indexes
No explicit non-constraint index is declared.

## Ontology to RDB mapping
| Mapping | Ontology target | Kind | Status | RDB realization | Note |
|---|---|---|---|---|---|
| `M011` | `FacilityOperation` | class | direct | `organization_id↔facility_id` | Relator represented as associative table with its own identity |
| `M033` | `validFrom` | datatype_property | bounded | `valid_from` | Temporal projection for relator validity |
| `M034` | `validTo` | datatype_property | bounded | `valid_to` | Temporal projection for relator validity |

See [[V2 Ontology Reference]] for semantic definitions. This page does not redefine ontology meaning.

## Safe synthetic example
The following values are illustrative only and are not empirical records.

| Field | Synthetic value |
|---|---|
| `facility_operation_id` | `101` |
| `public_id` | `example:facility_operation:001` |
| `organization_id` | `<organization.organization_id>` |
| `facility_id` | `<facility.facility_id>` |
| `ontology_iri` | `https://w3id.org/cm-pharme/2.0/Example` |
| `valid_from` | `2026-01-01` |
| `valid_to` | `2026-01-01` |

## Common join paths
- Child to parent: `facility_operation.organization_id` = `organization.organization_id`.
- Child to parent: `facility_operation.facility_id` = `facility.facility_id`.

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
