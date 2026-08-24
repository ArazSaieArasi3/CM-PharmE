# V2-077 Actor/Facility Map — Implementation Contract

Issue: #145
Depends on: V2-076 / #143 complete
Status: preimplementation freeze

## Canonical inputs

- W8 design: `v2/research/w8/observatory-design.md`
- W8 task traceability: `v2/research/w8/observatory-task-traceability.csv`
- W6 PostgreSQL/PostGIS implementation: `v2/data/db/`
- W6 read-only interface contract: `v2/data/api/openapi.yaml`
- W6 baseline: ontology-aligned RDB, deterministic RDF KG, registered ontology↔RDB mappings, provenance/entity-match structures, paired SQL↔SPARQL benchmarks.

## Scope frozen for this work item

Implement only the article-scope capabilities required by:
- T01 — Ecosystem entity lookup
- T02 — Facility geospatial query

No general dashboard suite, production API, live global feed, predictive map, alerting, commercial workflow or ontology redesign belongs to V2-077.

## Semantic-source rule

The map is a read-only consumer. It may display canonical semantic identifiers/types already admitted by the ontology and W6 mappings, but must not create or reinterpret ontology classes/relations from UI categories, database convenience fields or map-layer labels.

Before implementation, the exact actor/facility mappings consumed by T01/T02 must be enumerated from the W6 mapping registry. Any source field lacking an admitted mapping remains source metadata and is not promoted into ontology identity.

## Query contract

### T01 — entity lookup
Minimum response fields:
- canonical semantic identifier;
- preferred display label;
- admitted semantic type;
- source/artifact identity;
- mapping/derivation identity;
- provenance/limitation status;
- optional location only when source-backed.

### T02 — facility spatial filter
Minimum request semantics:
- explicit spatial predicate;
- bounded geometry/coordinate input;
- optional admitted semantic-type filter.

Minimum response semantics:
- facility semantic identifier/type;
- source-backed geometry/coordinates;
- spatial predicate result;
- source and mapping lineage;
- evidence/limitation status.

Spatial storage/query mechanics use the existing EPSG:4326-ready PostGIS baseline. Physical geography must remain distinct from regulatory jurisdiction.

## Provenance invariants

1. Every displayed entity has an inspectable source/evidence path or an explicit `provenance-unavailable` status.
2. Missing coordinates are `unknown/not supplied`, never interpreted as absence of a facility.
3. Derived or normalized geography is identified as derived, not represented as raw source truth.
4. Entity-match evidence/confidence, if displayed, remains separate from canonical identity claims.
5. The application never hides source-specific limitations behind a generic global-view label.

## Deterministic fixtures to add

### F-T01-01
Given a seeded admitted entity with registered semantic type and provenance, entity lookup returns the expected canonical identifier/type and provenance record.

### F-T01-02
Given a source record without an admitted semantic mapping, the application must not manufacture a canonical semantic type.

### F-T02-01
Given seeded facilities with source-backed EPSG:4326 locations, a bounded spatial predicate returns exactly the expected facility set.

### F-T02-02
A facility lacking source-backed coordinates is excluded from geometric result computation but remains retrievable as an entity with an explicit missing-location status.

### F-T02-03
Regulatory jurisdiction is not inferred solely from physical point geometry.

## Implementation acceptance criteria

- consumes W6 governed structures rather than duplicating semantic truth;
- read-only query path implemented for T01/T02;
- provenance fields visible in machine-readable responses and UI presentation;
- deterministic fixtures pass;
- no ontology source files modified by the demonstrator implementation;
- no claim of geospatial completeness, global coverage or effectiveness;
- V2-083 handoff records exact fixtures, tested commit and observed results.

## Action dependency

A0 for implementation and deterministic local/tool-assisted validation. A1 only for a later hosted reproducibility/application gate. No hosted PASS is required to begin coding.