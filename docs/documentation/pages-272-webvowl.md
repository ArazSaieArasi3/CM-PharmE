# PAGES-05 Static WebVOWL Integration Contract

Issue: #272  
Parent: #267

## Toolchain

- WebVOWL: **1.1.7**, exact source commit `28e7dd9540622e8cb723dc000824b5eef5ae775f`.
- OWL2VOWL: **0.3.7**, exact source commit `2833ead00122ca252a0fd0e18c5e5b696d711d2c`.
- WebVOWL build runtime: Node 12.22.12, matching the release's documented Node 12 build family.
- OWL2VOWL build/runtime: Java 8.

The official GHCR frontend image was evaluated first but anonymous retrieval returned `unauthorized`; the integration therefore builds from exact official release source commits rather than relying on an inaccessible package.

## Static Pages model

No OWL2VOWL server is deployed. Each governed ontology input is converted during CI into VOWL JSON and packaged with a static WebVOWL frontend.

Routes:
- V1: `/ontology/v1.0.0/explore/`
- V2: `/ontology/v2/current/explore/`

Each route contains its own `webvowl/data/cmpe.json`.

## Version isolation

The embedded WebVOWL ontology selector/converter UI is disabled for the governed Pages explorer, and all bundled sample datasets are removed. Search, navigation and zoom capabilities remain part of WebVOWL.

This means the route cannot silently switch from its governed ontology dataset through the normal UI. Cross-version navigation occurs at the outer CM-PharmE Pages level where version/lifecycle context is visible.

## Authority and accessibility boundary

The outer explorer page always shows:
- version/lifecycle status;
- exact semantic source ref;
- an explicit **Interactive exploration** label;
- statement that WebVOWL is not the complete formal/logical specification;
- link back to generated formal reference;
- link to Research Wiki;
- link to exact semantic source.

The formal-reference link is also the non-interactive accessibility fallback.

## Slice 1 acceptance

This slice proves:
- exact-source conversion for both V1/V2;
- separate explorer routes and datasets;
- static local asset integrity;
- no bundled sample ontology leakage;
- visible source/lifecycle/fallback context;
- deployable static explorer candidate.

Public browser rendering, console/CORS checks, and search/zoom interaction evidence remain for the deployment-stage #275 integration before #272 can close.
