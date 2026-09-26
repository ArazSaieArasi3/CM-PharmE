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

## Slice 1 reproducibility pins

The first successful governed candidate run established and this contract now enforces:

- OWL2VOWL 0.3.7 is rebuilt from exact source. Its raw shaded-JAR SHA is **not** a reproducibility identity because ZIP entry timestamps vary between builds. The governed converter digest therefore hashes sorted ZIP entry names plus uncompressed entry bytes, excluding ZIP metadata; this content digest is pinned after discovery.
- WebVOWL 1.1.7 built frontend tree SHA-256: `94a74bead0c5b4ab1be4d069dea48837016eee2bee88ecdec1c9396610e2705c`;
- V1 VOWL JSON SHA-256: `c45fa53aab846a1bf4a2c73d1cb4d21f3b0011810c124ad4b952a36ae33c5b2f`, projection counts 44 classes / 42 properties;
- V2 VOWL JSON SHA-256: `70f7cd6e6853bb98d85afce2a5a22aca14987b18e71356355257a7c9ff5f6de4`, projection counts 102 classes / 110 properties.

The VOWL counts are **converter projection counts**, not replacements for the governed ontology inventory counts.

WebVOWL 1.1.7 is a legacy frontend with semver-ranged npm dependencies and no lockfile in the upstream release. Therefore the exact source commit alone is not treated as sufficient reproducibility evidence: the expected built frontend-tree digest is also enforced. Any future dependency-resolution drift fails the build instead of silently changing published explorer assets.

## Converter content identity

A second exact-source rebuild established the metadata-independent OWL2VOWL 0.3.7 shaded-JAR **content digest**:

`f500951cdd4a0963fb80a96b974f463e8cfc84660f3b46ce802b14296e5e9aee`

This digest is computed from sorted ZIP entry names plus uncompressed entry bytes. It is now enforced in CI. Raw JAR bytes are intentionally not used as the identity because archive timestamps vary without changing executable content.

## Hypothetical V3 onboarding guard

`tools/pages/test_webvowl_v3_contract.py` creates a disposable V3 registry entry and adapter configuration. It proves that the shared packager can create an isolated V3 route, binds the manifest to its source and data checksum, rejects an overwrite or source-ref mismatch, and rejects a route collision. The synthetic input is confined to a temporary directory and is never added to the published registry or artifact. This test does not claim a scientific V3 ontology exists.
