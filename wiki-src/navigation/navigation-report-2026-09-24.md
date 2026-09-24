# Navigation QA report — reader-centered IA

**Issue:** #230  
**Date:** 2026-09-24  
**PR:** #247

## Result

**PASS — zero navigation blockers.**

Automated graph audit over the source-controlled Wiki inventory reported:

- Inventory entries: **66**
- Source-complete pages: **65**
- Planned pages: **1**
- Top-level landing pages: **9**
- Maximum depth for source-complete pages from Home: **2**
- Unreachable source-complete pages: **0**
- Source-complete pages deeper than two steps: **0**
- Orphan source-complete pages: **0**
- Missing Home landing links: **0**
- Missing Sidebar landing links: **0**
- Planned `Representative Task Evaluation`: reachable at depth **2**

## Depth distribution

| Depth from Home | Source-complete pages |
|---:|---:|
| 0 | 1 |
| 1 | 16 |
| 2 | 48 |

## Interpretation

The current information architecture satisfies the #230 navigation contract: every source-complete page is discoverable from Home within at most two meaningful Wiki links.

The graph check is implemented by `tools/wiki/check_navigation.py` and runs in Wiki Documentation CI. A failure in reachability, depth, orphan status or required landing-page presence blocks future Wiki PRs.

## Reader-journey evidence

See:
- `wiki-src/navigation/information-architecture-v2.md`
- `wiki-src/navigation/reader-journeys.md`

## Scope boundary

This report evaluates documentation navigation, not semantic completeness or research quality.
