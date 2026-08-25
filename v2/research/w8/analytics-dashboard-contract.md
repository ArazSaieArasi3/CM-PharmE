# V2-080 — Bounded Ecosystem Analytics Contract

Issue: #151
Parent: #22
Capability: C4 Ecosystem analytics
Representative tasks: T04, T05

## Frozen evidence basis
V2-080 is restricted to the W7-E11 admitted analytics candidate `AN-08 — Cross-representation benchmark analytics` and the four registered benchmark pairs in `v2/data/queries/sql-sparql-benchmarks.json` (`QREP-01` through `QREP-04`).

The implementation must rebuild the existing W6 PostgreSQL/PostGIS fixture and deterministic RDF/KG, run the existing `tools/v2_data/compare_sql_sparql.py`, and generate dashboard outputs only from a fully passing four-pair comparison report.

## Provenance and semantic invariants
- ontology/RDB/KG mappings remain the semantic source of truth;
- dashboard labels, layout, counts and presentation metadata do not create ontology identity;
- each displayed benchmark is traceable to the frozen benchmark registry and comparison tool;
- absence of broader analytics evidence is not converted into evidence of absence;
- deferred W7-E11 analytics/AI candidates remain deferred.

## Admissible claim
For the registered W6 fixture benchmark questions only, canonicalized answers are preserved across the reference relational and RDF representations when the dedicated V2-080 gate observes all four pairs passing.

## Explicit non-claims
This work does not establish arbitrary SQL↔SPARQL equivalence, pharmaceutical-market completeness, real-world coverage, production deployment, usability/effectiveness, forecasting, causal inference, or AI novelty/performance.

## Closure rule
V2-080 may close only after a dedicated hosted gate succeeds on the exact merge-candidate head and the generated JSON/HTML evidence plus V2-083 handoff are persisted.