# V2-078 → V2-083 evaluation handoff

## Scope
This handoff supplies bounded, reproducible evidence for later T01 entity lookup and T03 registered-relation traversal evaluation. It does **not** constitute Gate-G PASS, global ecosystem coverage, production deployment, comparator superiority, or user-effectiveness evidence.

## Governed implementation
- Mapping freeze: `v2/research/w8/entity-relationship-browser-mapping-freeze.csv`
- Read-only SQL contract: `v2/app/observatory/sql/entity-relationship-browser.sql`
- Deterministic fixture: `v2/app/observatory/fixtures/entity-relationship-browser-fixture.csv`
- Semantic/source-leakage validator: `v2/app/observatory/validate_entity_relationship_browser.py`
- Hosted gate: `.github/workflows/v2-w8-entity-relationship-browser.yml`

## Observed hosted evidence before this handoff commit
- Tested commit: `661e82da38e4b1d32e1b3b6bb7feaf7fab7cdd19`
- Run: `32801718526`
- Conclusion: `success`
- Evidence artifact: `9546709185` (`v2-w8-entity-relationship-browser-evidence`)
- Artifact digest: `sha256:be0a89589ba4aece19f38a546e7113c5b71e7d366dfbb5bd18dc535969a448fd`

Because this handoff file itself changes the PR head, final closure requires a fresh successful hosted browser gate on the new exact head. V2-083 must use the latest successful run/artifact, not this predecessor run, as exact-head evidence.

## Preserved boundaries
- Organization ≠ Facility.
- MedicinalProduct ≠ Presentation.
- Source label/code ≠ semantic identity.
- `presentationOf` traversal is restricted to registered M015 realization.
- `hasActiveSubstance` is bounded to the W6 primary-substance hook and is not a complete composition model.
- Missing lineage is rendered as `provenance-unavailable`; it is not silently inferred.

## V2-083 evaluation use
Use the deterministic cases as representative task fixtures for T01/T03 reproducibility and trace them to the exact successful head/run. Treat task success as evidence about implemented structures only; do not promote it into global completeness, usability, or real-world effectiveness claims.
