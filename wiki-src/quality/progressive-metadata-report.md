# Progressive metadata migration report

**Issue:** #231  
**Date:** 2026-09-24  
**Contract:** `wiki-src/editorial/progressive-metadata-contract.md`

## Result

**PASS — reader-facing metadata was compacted without losing provenance.**

## Coverage

Current source-complete inventory: **65 pages**

- Reader-facing pages migrated to compact header + Documentation record: **58**
- Reader-facing pages with complete Documentation record: **58/58**
- Governance/status pages intentionally retaining expanded metadata: **6**
- Home: **1** (navigation surface; no page metadata block required)
- Metadata-contract errors: **0**

## Header-density change

Frozen pre-improvement baseline:
- top metadata lines: **470**
- average recorded at Stage A: **8.25 lines/page**

After #231 migration:
- top metadata lines: **213**
- reader-facing compact header: exactly **3 lines/page**
- reduction in top-level metadata lines: **257**
- reduction relative to baseline: **54.7%**

The reduction is a presentation change, not a provenance deletion.

## Compact reader header

Reader-facing pages expose only:
- Version scope
- Status
- Updated

## Documentation record

The complete provenance is retained in a collapsible `Documentation record` at the end of each migrated page.

Required data remain retrievable:
- page scope;
- documentation maturity;
- authoritative source/authority;
- last synchronized date;
- synchronized ref;
- related issues/PRs;
- evidence status;
- future refresh;
- Wiki baseline.

Where a newly created navigation page lacked an explicit operational field, only conservative documentation-level defaults were added from page scope/inventory. No scientific evidence was inferred.

## Page-class disposition

Compact:
- Narrative / Navigation
- Narrative / Research
- Concept / Domain / Model
- Evaluation / Evidence
- Cross-Version Evolution
- Reference / Index

Expanded by design:
- Status / Governance
- Status / Changelog

The V2 Research Method and Development page was reclassified from the historical `Status / Changelog` class to `Narrative / Research`, because it is now a reader-facing research-method page rather than an internal status log.

## Automation

- Migration: `tools/wiki/migrate_progressive_metadata.py`
- Contract validator: `tools/wiki/check_metadata_contract.py`
- Permanent CI enforcement: Wiki Documentation CI
- Templates updated for future authoring.
- Wiki Authoring Standard updated.

## Scientific/evidential equivalence

The migration changes metadata placement only. It does not change:
- research results;
- ontology semantics;
- version authority;
- evaluation outcomes;
- claim dispositions;
- limitations/non-claims;
- pending/completed status.

## Follow-up

#240 will later perform the full page-by-page prose/editorial review. #231 is limited to metadata/provenance presentation.
