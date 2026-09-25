# geography

> **Version scope:** V2  
> **Status:** Reference implementation  
> **Updated:** 2026-09-25

This page documents one implemented PostgreSQL/PostGIS table. It describes a research/reference realization and does not claim production deployment.

## Purpose
Canonical geographic feature store, including supported country/administrative-region types and PostGIS geometry.

## Provenance role
Canonical geography used by provenance-linked observations and facilities.

## Physical structure
| Column | SQL type | Nullable | Key / constraint | Default |
|---|---|---|---|---|
| `geography_id` | `BIGSERIAL` | NO | PK | — |
| `public_id` | `TEXT` | NO | UNIQUE | — |
| `geography_type` | `TEXT` | NO | CHECK geography_type IN ('country','administrative_region','other') | — |
| `canonical_name` | `TEXT` | NO | — | — |
| `country_code` | `CHAR(2)` | YES | — | — |
| `source_region_code` | `TEXT` | YES | — | — |
| `geonames_id` | `BIGINT` | YES | — | — |
| `geom` | `geometry(Geometry,4326)` | YES | — | — |
| `ontology_iri` | `TEXT` | NO | — | — |

## Primary key
`geography_id`

## Foreign keys
No outgoing foreign key is declared.

## Incoming references
| Referencing table | FK column | Nullable |
|---|---|---|
| [[V2 Table geography_alias|geography_alias]] | `geography_id` | NO |
| [[V2 Table regulatory_jurisdiction|regulatory_jurisdiction]] | `geography_id` | YES |
| [[V2 Table facility|facility]] | `geography_id` | YES |
| [[V2 Table observation_result|observation_result]] | `geography_id` | YES |

## UNIQUE constraints
- `public_id`

## CHECK constraints
- `geography_type IN ('country','administrative_region','other')`

## Explicit indexes
- **geography_geom_gix** — GIST on `geom`
- **geography_geonames_idx** — BTREE on `geonames_id` WHERE `geonames_id IS NOT NULL`
## PostGIS representation
The geom column uses geometry(Geometry,4326), with WGS 84 / EPSG:4326 as the declared spatial reference. The geography_geom_gix GiST index supports spatial access. Geometry presence does not establish geocoding accuracy or geographic completeness.


## Ontology to RDB mapping
| Mapping | Ontology target | Kind | Status | RDB realization | Note |
|---|---|---|---|---|---|
| `M005` | `GeographicFeature` | class | polymorphic | `geography_id/public_id` | geography_type distinguishes supported subtypes |
| `M006` | `AdministrativeRegion` | class | direct | `geography_type='administrative_region'` | Administrative region row |
| `M007` | `Country` | class | direct | `geography_type='country'` | Country row |

See [[V2 Ontology Reference]] for semantic definitions. This page does not redefine ontology meaning.

## Safe synthetic example
The following values are illustrative only and are not empirical records.

| Field | Synthetic value |
|---|---|
| `geography_id` | `101` |
| `public_id` | `example:geography:001` |
| `geography_type` | `administrative_region` |
| `canonical_name` | `Example Canonical Name` |
| `ontology_iri` | `https://w3id.org/cm-pharme/2.0/Example` |
| `country_code` | `EX` |
| `source_region_code` | `example` |

## Common join paths
- Parent from child: `geography.geography_id` = `geography_alias.geography_id`.
- Parent from child: `geography.geography_id` = `regulatory_jurisdiction.geography_id`.
- Parent from child: `geography.geography_id` = `facility.geography_id`.
- Parent from child: `geography.geography_id` = `observation_result.geography_id`.

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
