# CM-PharmE V2 Branch Retirement Inventory

Status date: 2026-09-04

## Purpose
Reduce branch sprawl while preserving the reviewer-facing CM-PharmE 1.x line and the audit trail of CM-PharmE 2.0 research work.

## Long-lived branches

| Branch | Disposition | Rationale |
|---|---|---|
| `main` | KEEP | Stable CM-PharmE 1.x public/reviewer-facing baseline while the journal manuscript remains under review. No V2 model, manuscript, dataset, or application work is merged here. |
| `v2/research-program` | KEEP | Single long-lived CM-PharmE 2.0 integration branch. Human-review/naming/provenance work was consolidated here through PR #168. |

## Active short-lived branch

| Branch | Disposition | Rationale |
|---|---|---|
| `v2/paper-draft0` | KEEP TEMPORARILY | Active manuscript Draft 0 branch, tracked by #171 / PR #172. Retire after its accepted manuscript integration is merged. |

## V2 branches that are retirement candidates

These branches represent already integrated waves, intermediate human-review preparation, or completed demonstrator slices. They should not remain long-lived once their content is verified on `v2/research-program` and no open PR depends on them.

- `v2/concept-label-normalization`
- `v2/domain-architecture-normalization`
- `v2/human-review-disposition-log`
- `v2/human-review-provenance-gap-audit`
- `v2/human-review-risk-queue`
- `v2/p0-evidence-packets`
- `v2/p1-evidence-packets`
- `v2/p2-evidence-packets`
- `v2/w1-needs-usecases-opportunities`
- `v2/w2-data-landscape`
- `v2/w3-concept-discovery`
- `v2/w4-ufo-ontouml`
- `v2/w5-formal-ontology`
- `v2/w6-data-infrastructure`
- `v2/w7-evaluation`
- `v2/w8-observatory`
- `v2/w8-actor-facility-map`
- `v2/w8-entity-relationship-browser`
- `v2/w8-kg-explorer`
- `v2/w8-analytics-dashboard`
- `v2/w8-resilience-risk-view`

Deletion is a repository-hygiene action only; research provenance is retained through commits, merged PRs, issues, release artifacts, and the integration branch.

## V1 branches to retain during the current journal-review cycle

Do not clean these aggressively while CM-PharmE 1.x remains externally reviewable. Reassess only after the journal cycle is complete and the V1 release/tag/archive policy is confirmed.

- `archive/pre-refactor-2026-08-13`
- `automation/b5-reproducible-build-v1`
- `automation/g6-semantic-engineering-completion-v1`
- `docs/main-homepage-refresh-v1`
- `docs/post-closure-cleanup-v1`
- `evaluation/b4-paper-grounded-validation-v1`
- `ontology/b3-formal-ontology-v1`
- `refactor/research-repository-v1`

## Branch lifecycle policy going forward

For V2 and later ontology work, use:

`Issue -> short-lived branch -> PR -> CI/review -> merge to integration branch -> delete branch`

Long-lived branches should be exceptional. For the current project the intended long-lived pair is only:

1. `main` — CM-PharmE 1.x stable/public evidence surface.
2. `v2/research-program` — CM-PharmE 2.0 integration line.

## Current consolidation outcome

PR #168 merged the active human-review, naming, provenance and visual-ontology work into `v2/research-program` without modifying `main`. The next active work should branch from the V2 integration line, not from historical wave branches.
