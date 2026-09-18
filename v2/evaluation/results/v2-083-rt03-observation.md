# V2-083 RT-03 observed result

Issue: #170
Task: RT-03 — KG exploration
Frozen integration baseline: `1226b0a5484f8f5d3a8d214e0d0f52f066b88999`
Observed result: **PASS**

## Execution evidence

The deterministic KG-explorer contract was executed from the exact baseline source/fixture semantics used by the integrated W8 implementation. The execution asserted:

- all six frozen representative nodes are admitted;
- every node/edge provenance state is one of `source-backed` or `provenance-unavailable`;
- the `N-PROD-001` neighborhood exposes exactly `E-PRES-PROD` and `E-PROD-SUB`;
- `N-ORG-001` exposes no traversable edge because unregistered helper adjacency must not become an ontology relation.

Observed terminal result: `PASS: RT-03 deterministic KG explorer contract`.

## Provenance

Repository sources reconciled before execution:
- `v2/app/observatory/kg_explorer.py`
- `v2/app/observatory/validate_kg_explorer.py`
- `v2/app/observatory/fixtures/kg-explorer-fixture.csv`
- `v2/research/w8/kg-explorer-mapping-freeze.csv`

The workflow contract in `.github/workflows/v2-w8-kg-explorer.yml` independently defines the same deterministic validator and representative product/organization neighborhood renderings.

## Claim boundary

This PASS establishes only the frozen representative KG-exploration behavior over registered fixture edges. It does **not** establish global KG completeness, arbitrary traversal correctness, ecosystem completeness, production readiness, or clinical/regulatory validity.

RT-04 and RT-05 remain unexecuted by this observation and must not be promoted from implementation existence or historical CI alone.
