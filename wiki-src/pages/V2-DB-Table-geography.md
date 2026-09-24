# geography

> **Version scope:** V2  
> **Status:** Reference implementation / Stable-to-date  
> **Updated:** 2026-09-24

> Generated physical-table reference from the authoritative PostgreSQL/PostGIS schema. It documents a research/reference realization and does **not** imply production deployment or production-scale performance.

## Purpose
Canonical geographic entity table with optional PostGIS geometry and supported geography subtype.

## Keys and structure
- **Primary key:** `geography_id`
- **Foreign keys:** 0
- **Provenance role:** No dedicated provenance role; provenance is reached through documented foreign-key paths where applicable.

## Columns
| Column | Type | Null? | Key / constraint | Default |
|---|---|---|---|---|
| `geography_id` | `BIGSERIAL` | No | PK | — |
| `public_id` | `TEXT` | No | UNIQUE | — |
| `geography_type` | `TEXT` | No | CHECK | — |
| `canonical_name` | `TEXT` | No | — | — |
| `country_code` | `CHAR(2)` | Yes | — | — |
| `source_region_code` | `TEXT` | Yes | — | — |
| `geonames_id` | `BIGINT` | Yes | — | — |
| `geom` | `geometry(Geometry,4326)` | Yes | — | — |
| `ontology_iri` | `TEXT` | No | — | — |

## Table-level constraints
- `CHECK geography_type (geography_type IN ('country','administrative_region','other'))`

## Explicit indexes
| Index | Method | Columns | Predicate |
|---|---|---|---|
| `geography_geom_gix` | GIST | `geom` | — |
| `geography_geonames_idx` | btree(default) | `geonames_id` | `geonames_id IS NOT NULL` |

## Ontology alignment
| Ontology IRI | Kind | Status | RDB field/join | Representation note |
|---|---|---|---|---|
| `https://w3id.org/cm-pharme/2.0/GeographicFeature` | class | polymorphic | `geography_id/public_id` | geography_type distinguishes supported subtypes |
| `https://w3id.org/cm-pharme/2.0/AdministrativeRegion` | class | direct | `geography_type='administrative_region'` | Administrative region row |
| `https://w3id.org/cm-pharme/2.0/Country` | class | direct | `geography_type='country'` | Country row |

See [[V2 Ontology Reference]] for semantic definitions. Mapping authority remains `v2/data/mappings/ontology-rdb-mapping.csv`.

## Common joins
No outgoing foreign-key join is declared from this table.

## Safe synthetic row fragment
`{"geography_id": "1001", "public_id": "syn-geography-001", "geography_type": "other", "canonical_name": "synthetic-canonical-name", "country_code": "ZZ", "source_region_code": "synthetic-source-region-code", "geonames_id": "1001", "geom": "POINT(8.68 50.11) [synthetic]"}`

This example is synthetic and exists only to clarify field shape.

## Boundaries
- This table belongs to a reproducible **reference implementation**, not a production claim.
- Relational representation may be direct, bounded, polymorphic, relational-projection or deferred as stated in the mapping registry.
- The table definition does not redefine ontology semantics.

## PostGIS note
`geom` is declared as `geometry(Geometry,4326)`. SRID 4326 identifies the coordinate reference system. A GiST index `geography_geom_gix` supports spatial access. The generic Geometry type does not imply that every row contains the same geometry subtype or that geospatial completeness is established.

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
