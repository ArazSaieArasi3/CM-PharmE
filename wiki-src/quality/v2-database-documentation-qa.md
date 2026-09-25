# V2 database documentation QA report

**Issue:** #236  
**Date:** 2026-09-25  
**Authority ref:** `v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999`

## Result

**PASS — the implemented V2 PostgreSQL/PostGIS reference schema is documented exhaustively at table, field, constraint and ERD levels with zero unexplained structural gaps.**

## Structural baseline

| Metric | Verified |
|---|---:|
| Base tables | 24 |
| Primary keys | 24 |
| Foreign keys | 31 |
| UNIQUE constraints | 29 |
| CHECK constraints | 11 |
| Explicit indexes | 5 |
| Query views | 4 |
| PostGIS extension | 1 |
| Tables with ontology↔RDB registry rows | 23 |
| Tables without direct registry row | 1 — `geography_alias` |

`geography_alias` is explicitly documented as having no direct mapping row; no ontology mapping is inferred from its name.

## Page coverage

- 24 table-reference pages
- 1 master [[V2 Database Reference]]
- 1 [[V2 Database Data Dictionary]]
- 1 [[V2 Database Views]]
- 1 [[V2 Database ERD Suite]]

**Total #236 Wiki pages: 28**

Each table page documents:
- purpose and provenance role;
- every column/type/nullability;
- PK/FKs;
- UNIQUE/CHECK constraints;
- explicit indexes;
- ontology↔RDB registry rows and mapping status where present;
- safe synthetic example;
- common join paths;
- implementation/production boundary.

## ERD coverage

- DGM-ERD-002 — logical relational model
- DGM-ERD-003 — full physical ERD, **24/24 tables**
- DGM-ERD-004 — Dataset / Release / Source / Transformation
- DGM-ERD-005 — Organization / Facility / Geography / Jurisdiction
- DGM-ERD-006 — Product / Substance / Presentation / Classification
- DGM-ERD-007 — Identifier / Identity / Entity Match
- DGM-ERD-008 — Assertion / Evidence / Provenance
- DGM-ERD-009 — Observation
- DGM-ERD-010 — Shortage / Resilience-related implementation

Physical FK coverage: **31/31**.

All generated SVGs use the governed theme-safe rendering contract and cache-busted Wiki URLs.

## PostGIS coverage

The geography reference documents:
- `geom geometry(Geometry,4326)`;
- WGS 84 / EPSG:4326 interpretation;
- `geography_geom_gix`;
- GiST spatial indexing;
- explicit boundary that geometry presence does not establish geocoding accuracy or geographic completeness.

## Query-view distinction

The 4 query/research views are documented separately from the 24-table count:
- `v_product_presentations`
- `v_observations`
- `v_provenance_lineage`
- `v_entity_matches`

This prevents views from being misreported as base tables.

## Human-oriented sample review

Manual sample review covered:
- `observation_result` — all 6 FKs documented; synthetic example now includes required provenance FKs `source_record_id` and `assertion_id`;
- `geography` — PostGIS geometry, GiST and partial GeoNames index documented;
- DGM-ERD-003 — all 24 tables and 31 FKs present;
- parallel `entity_match_assertion → source_record` FK edges are visually separated rather than overprinted.

## Boundaries

The documentation deliberately does not claim:
- production deployment;
- production-scale performance or availability;
- full external-source ingestion;
- real-world entity-resolution accuracy;
- geocoding accuracy;
- global coverage;
- semantic authority of the relational schema.

Ontology semantics remain authoritative in the ontology/review artifacts.

## Machine controls

- parser: `tools/wiki/db_schema_model.py`
- page/reference generator: `tools/wiki/generate_v2_database_pages.py`
- ERD generator: `tools/wiki/generate_v2_database_erds.py`
- exhaustive checker: `tools/wiki/check_v2_database_docs.py`
- FK coverage: `wiki-src/database-reference/fk-coverage.csv`
- constraint/index coverage: `wiki-src/database-reference/constraint-coverage.csv`
- structural coverage: `wiki-src/database-reference/coverage.json`
- ERD coverage: `wiki-src/database-reference/erd-coverage.json`

Latest controlled generation passed database coverage, diagram QA, cache-safe URLs, Wiki source validation, navigation and metadata validation.
