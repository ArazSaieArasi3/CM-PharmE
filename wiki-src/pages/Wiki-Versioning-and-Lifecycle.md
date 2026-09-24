# Wiki Versioning and Lifecycle

> **Page scope:** Version-neutral governance  
> **Documentation maturity:** Stable governance policy  
> **Authoritative documentation source:** `wiki-src/`  
> **Last synchronized:** 2026-09-23  
> **V1 source:** `main@5099888668d35f798e4759e3534e707ed906db24`  
> **V2 source:** `v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999`  
> **Related issues:** #202, #210, #211, #212, #213, #214, #217  
> **Evidence status:** Governance rule; no scientific claim is created by this page

## Purpose

CM-PharmE documentation is maintained as a versioned research artifact. Documentation versioning is intentionally distinct from ontology versions, manuscript revisions, repository tags, GitHub Releases and DOI-backed research releases.

## Documentation baseline identifiers

Declared Wiki baselines use:

`WB-YYYY.MM.N`

where:
- `WB` means Wiki Baseline;
- `YYYY.MM` is the synchronization month;
- `N` is the sequence of declared baselines in that month.

The first declared current documentation baseline is **WB-2026.09.1**. It passed the required source, publication and rendered-surface QA gates. This declaration freezes the documentation snapshot only; it does **not** declare CM-PharmE 2.0 final or frozen.

## Documentation maturity states

| State | Meaning |
|---|---|
| Stable | Documentation corresponds to a selected stable/frozen underlying baseline. |
| Stable-to-date / Evolving | Documentation accurately reflects all stable evidence available at the synchronization point while the underlying version remains active. |
| Candidate | Documentation is being prepared for a declared baseline and still awaits required QA/publication steps. |
| Frozen | Documentation has been synchronized to an explicit final declared research/repository baseline and passed the final documentation gate. |

### Current interpretation

- **CM-PharmE 1.x:** Stable.
- **CM-PharmE 2.0:** Stable-to-date / Evolving.
- V2 must not be labeled Final/Frozen before the final V2 documentation gate.

## Authority and synchronization

A Wiki page may summarize authoritative artifacts but may not silently supersede them.

- V1 statements must resolve to `main` unless explicitly historical/external.
- V2 statements must resolve to `v2/research-program` unless explicitly historical/external.
- Cross-version statements must identify which assertion belongs to which version.
- Open issues, unmerged proposals, protocols and incomplete evaluations remain pending.

## What triggers a Wiki update

A documentation impact review is mandatory after any of the following:
1. semantic concept/relation decision;
2. ontology/model release or baseline change;
3. evaluation result or gate decision;
4. demonstrator stabilization;
5. manuscript claim-disposition change;
6. release/tag/DOI event;
7. major repository consolidation;
8. closure/reopening of a Wiki-relevant dependency;
9. correction of a material documentation error.

## Change classes

| Class | Description | Baseline impact |
|---|---|---|
| Editorial | Grammar, wording, formatting; no meaning/status change | Changelog entry optional unless widespread |
| Documentation-only | Navigation or explanatory restructuring; no research semantics change | Changelog required |
| Evidence/status | New evaluation result, issue/gate status, evidence link | Changelog + impacted-page audit |
| Semantic reflection | Wiki updated to reflect an approved semantic/model change | Changelog + traceability + semantic-impact audit |
| Release/freeze | Documentation synchronized to a declared project baseline | New declared Wiki baseline + QA + archive |

## GitHub Wiki history versus Release

GitHub Wiki has Git history, but the Wiki itself does not have an independent GitHub Releases surface. A Wiki edit is therefore **not** a GitHub Release.

At the 2026-09-23 foundation check, the CM-PharmE repository had **no formal GitHub Release published**. Future release documentation must verify this state again rather than relying on this historical statement.

## Declaring a baseline

A candidate may become a declared baseline only when:
- required pages for that stage exist;
- version scope is explicit;
- authoritative refs are recorded;
- current status has been checked against live issues/PRs;
- required automated/manual QA is complete;
- blocking documentation findings are zero;
- the update register is current.

## Correction and rollback policy

If a declared Wiki baseline contains a material error:
1. record the error in the update register;
2. identify whether the error is editorial, evidential, status-related or semantic;
3. correct the page from authoritative evidence;
4. rerun affected QA;
5. declare a corrective baseline if the error could materially affect interpretation;
6. never rewrite the historical changelog to hide the correction.

## Future checkpoints

- #212 — post-W8 / Gate G synchronization.
- #213 — post-human-review / semantic-stabilization synchronization.
- #214 — final V2 documentation freeze.

These checkpoints exist so that the evolving V2 Wiki cannot silently become stale.
