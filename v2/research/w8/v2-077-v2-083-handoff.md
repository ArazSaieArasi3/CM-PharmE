# V2-077 → V2-083 Evaluation Handoff

Issue: #145
W8 task scope: T01 ecosystem entity lookup; T02 bounded facility geospatial query.

## Implemented evidence surface

- Exact admitted W6 mapping freeze: `actor-facility-mapping-freeze.csv`.
- Read-only SQL contract: `v2/app/observatory/sql/actor-facility-map.sql`.
- Read-only executable CLI/query layer: `tools/v2_w8/actor_facility_map.py`.
- Controlled/non-empirical spatial fixture: `v2/app/observatory/fixtures/actor-facility-spatial-fixture.csv`.
- Deterministic validator: `tools/v2_w8/validate_actor_facility_map.py`.
- Hosted reproducibility gate: `.github/workflows/v2-w8-actor-facility-map.yml`.
- Article-facing bounded HTML render is produced during the hosted gate as `build/w8/actor-facility-map.html`.

## Observed hosted evidence

Exact validated implementation head before this documentation-only handoff commit:
`c2c513745bdd555a15b543b37baa6e6a8eeea72e`

GitHub Actions:
- workflow: `CM-PharmE 2.0 W8 Actor Facility Map`
- run: `32790987670`
- job: `97632341420`
- conclusion: `SUCCESS`
- artifact: `9543114034` (`cm-pharme-v2-v2-077-evidence`)
- artifact digest: `sha256:c438c9f91f0acfc3ce867c36b8ad6ab279e90d61950d4f2a69ce680f7f9474f7`

Observed successful stages include W6 PostgreSQL/PostGIS bootstrap, mapping/fixture validation, T01 lookup, T02 spatial query, bounded HTML rendering, render-boundary assertions, summary generation and evidence upload.

## Deterministic task evidence for V2-083

### T01 — ecosystem entity lookup
Use the controlled seeded facility `facility:w8-controlled:alpha`.
Expected properties:
- semantic type resolves to the admitted W6 `Facility` IRI;
- mapping identity is M010;
- provenance is visible and source-backed through the controlled fixture source record;
- an entity with missing location remains retrievable and reports `unknown/not-supplied` rather than negative facility evidence.

Organization lookup remains intentionally conservative: W6 does not guarantee direct source-record lineage for Organization, so the application returns `provenance-unavailable` where no governed lineage exists rather than fabricating provenance.

### T02 — bounded facility geospatial query
Controlled bounding box `[5,5,15,15]` returns only `facility:w8-controlled:alpha` from the controlled fixture.
The wider controlled box `[0,0,30,30]` returns alpha and beta but excludes the no-location facility from geometric computation.
Every spatial result carries M010/M031 mapping identities and the explicit boundary `regulatory-jurisdiction-not-inferred`.

## Claim boundary for evaluation

V2-077 demonstrates reproducible representation/query/provenance mechanics over the admitted W6 architecture plus controlled W8 fixtures. It does **not** establish:
- global actor/facility coverage;
- geospatial completeness or geocoding accuracy;
- real-world entity-resolution accuracy;
- usability or task effectiveness;
- operational monitoring;
- production API/UI deployment;
- regulatory jurisdiction from physical geometry.

C-08 therefore remains deferred to V2-083 representative-task evaluation. The controlled fixture must not be reported as empirical pharmaceutical ecosystem evidence.

## V2-083 evaluation inputs

V2-083 should evaluate the frozen T01/T02 task procedures against the exact implementation and evidence above, preserving the distinction between deterministic correctness/reproducibility and user/task effectiveness. Any later real-world data demonstration requires separately admitted, licensed, provenance-traceable sources and must not silently replace the controlled fixture evidence.
