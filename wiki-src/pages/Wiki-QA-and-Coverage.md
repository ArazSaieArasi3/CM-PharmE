# Wiki QA and Coverage

> **Page scope:** Version-neutral documentation governance  
> **Documentation maturity:** Candidate / pre-publication QA  
> **Authoritative source:** `wiki-src/`, Wiki issues and CI evidence  
> **Last synchronized:** 2026-09-23  
> **Related issues:** #202, #203, #209, #216, #217, #218  
> **Evidence status:** Source QA operational; actual GitHub Wiki rendered QA pending #218  
> **Future refresh:** #218 → #209 → #217  
> **Wiki baseline:** WB-2026.09.1 Candidate

## Current source coverage

At the pre-publication audit point, the Wiki inventory contains **57 planned/current page entries**.

Before this page is marked complete:
- 55 entries were source-complete;
- 2 were planned.

This page itself completes one of those planned entries. The remaining planned page is **Representative Task Evaluation**, intentionally deferred to #212 because the corresponding W8/Gate G work is not yet final.

## Completed documentation workstreams

- #210 — Versioning / Changelog / Lifecycle: complete.
- #215 — Authoring Standard / Templates / Metadata Contract: complete.
- #204 — V1 documentation package: complete.
- #205 — current stable-to-date V2 documentation package: complete.
- #206 — V1→V2 evolution/provenance/traceability: complete.
- #207 — evaluation/assurance/reproducibility navigation: complete.
- #208 — reference/index layer: complete.
- #216 — automated source QA: complete.

## Source CI

Automated source validation checks:
- duplicate names/slugs;
- missing source-complete pages;
- mandatory metadata;
- internal Wiki links against inventory;
- orphan-page detection;
- Home/Sidebar presence;
- required Home sections;
- premature V2 Final/Frozen status;
- baseline manifest/inventory presence.

The workflow also executes an intentional invalid-fixture self-test to prove failure detection.

## Current QA boundary

This page does **not** declare WB-2026.09.1 a final/QA-clean published Wiki baseline.

Still required:
1. #218 — publish/synchronize accepted source to the actual GitHub Wiki repository and verify rendering.
2. #209 — combined final source + published-surface + status/claim audit.
3. #217 — archive the QA-approved published baseline with exact Wiki commit/ref.

## Known deliberate non-blockers

- V2 remains evolving.
- E9 has 0 real expert responses.
- #170 / Gate G remains open.
- #159/#173 human semantic review remains active.
- #171 manuscript integration remains active.
- future refreshes #212/#213/#214 remain intentionally open/blocked.

These are research-program states, not current Wiki-source defects, provided they remain truthfully documented.

## Publication blocker

The currently connected GitHub API surface has no direct Wiki write operation. Therefore source completion must not be represented as actual Wiki publication. #218 remains the explicit publication/render-verification gate.

## Related pages

[[Wiki Versioning and Lifecycle]] · [[Wiki Authoring Standard]] · [[Wiki Update Register]] · [[Current Status and Limitations]]
