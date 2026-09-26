# Pages Ontology Documentation Build Contract

Issue: #269  
Parent: #267

## Rule

Generated formal documentation MUST NOT accept an arbitrary TTL/OWL file. The Pages pipeline resolves exact source ref, module-selection rule, governed build, deterministic artifact, fingerprint and validation boundary before WIDOCO/WebVOWL may consume anything.

## V1

- Source authority: `main@595ea30a66644c1b130b6c1a781dc7afbd7ba284`
- Canonical source: `ontology/source/modules/**/*.ttl`
- Build: `tools/ontology/build.py`
- Documentation input: generated `distributions/cm-pharme.ttl`
- Canonical graph SHA-256: `cc823a8aff4d7e7818f8470f2dbad6ca8045ff92e5637fbf3503bc105170a83f`
- Boundary: documentation generation MUST NOT be converted into a claim of OWL 2 DL-profile conformance for V1.

## V2 — frozen formal baseline vs current documentation snapshot

Two identities are intentionally preserved.

### Historical W5 formal/reproducibility baseline
- Reproduced in E13 run `32566080703`
- Source snapshot: `952d6a42f8c1d92d6f2d3d2e78e76847dc9ed8b4`
- Canonical graph SHA-256: `59ef47eeed732290736e60bfa1c6bf43a12d15df2f50cff931badb5938cc954a`
- Status: immutable historical formal/reproducibility anchor.

### Current V2 Pages snapshot
- Source authority: `v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999`
- Current canonical graph SHA-256: `302a5f70db30701608712a2c346f6a5b4bbc72b4cb9c7a921ed6e38bbebd341f`
- Baseline file: `docs/documentation/v2-current-pages-baseline.json`
- Documentation input: generated `distributions/cm-pharme-v2.ttl`
- Lifecycle: **Stable-to-date / Evolving**, not frozen/final.

The fingerprint changed after the governed 2026-09-04 naming consolidation commit `4bebc04...`. That change normalized human-facing `rdfs:label` values and added `skos:altLabel` values while explicitly preserving IRIs, stereotypes, class hierarchies, formal axioms, SHACL constraints and mappings.

Pages may use the current snapshot only if executable graph comparison confirms that, relative to the frozen W5 snapshot, all graph differences are limited to `rdfs:label` and `skos:altLabel`.

## Publication failure behavior

Publication MUST fail on source-ref mismatch, unexpected module set, build failure, fingerprint mismatch, missing manifest, non-annotation V2 drift relative to W5, or registry/contract drift.

The W5 fingerprint is never rewritten merely to make current Pages generation pass.
