# V2-079 → V2-083 Evaluation Handoff

Issue: #149 / V2-079
Target evaluation workstream: V2-083

## Frozen representative task
T03 — relation traversal over a bounded graph slice using stable semantic identifiers and registered edge types only.

## Deterministic evidence contract
- Mapping freeze: `v2/research/w8/kg-explorer-mapping-freeze.csv`
- Fixture: `v2/app/observatory/fixtures/kg-explorer-fixture.csv`
- Explorer: `v2/app/observatory/kg_explorer.py`
- Validator: `v2/app/observatory/validate_kg_explorer.py`
- Hosted gate: `.github/workflows/v2-w8-kg-explorer.yml`

## Expected results for V2-083
1. `N-PROD-001` exposes exactly two admitted fixture edges: `presentationOf` and bounded `hasActiveSubstance`.
2. `N-ORG-001` exposes no traversable edge from the helper-only unregistered fixture adjacency; adjacency must not be promoted to ontology relation.
3. MedicinalProduct and MedicinalProductPresentation identities remain distinct.
4. Organization and Facility identities remain distinct.
5. Every displayed node/edge has either `source-backed` or explicit `provenance-unavailable` status.
6. Layout, lexical similarity, source co-occurrence, and helper adjacency remain non-semantic presentation/fixture mechanics.

## Evaluation boundary
This handoff supports deterministic correctness, semantic-boundary, and provenance-visibility checks for T03. It does not establish usability/effectiveness, global ecosystem completeness, graph coverage, AI performance, expert validation, or Gate-G PASS. Any representative-task effectiveness claim remains deferred to V2-083.
