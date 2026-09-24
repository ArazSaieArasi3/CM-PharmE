# Progressive metadata and provenance contract

**Issue:** #231  
**Status:** Active for reader-facing CM-PharmE Wiki pages  
**Principle:** minimal interpretation context first; full provenance remains available through progressive disclosure.

## Reader-facing compact header

Normal explanatory, ontology/model, evaluation, evolution, reference and navigation pages use exactly three reader-facing metadata fields directly below the H1:

> **Version scope:** <V1 | V2 | Cross-version | Version-neutral>  
> **Status:** <Stable | Stable-to-date / Evolving | other truthful documentation state>  
> **Updated:** <YYYY-MM-DD>

These three fields answer the questions a reader needs immediately:
1. Which version does this page describe?
2. Is the documentation stable, evolving or pending?
3. When was it last synchronized?

## Documentation record

The complete operational/provenance metadata is preserved at the end of the page in a collapsible block:

```html
<details>
<summary>Documentation record</summary>

- **Page scope:** ...
- **Documentation maturity:** ...
- **Authoritative source:** ...
- **Last synchronized:** ...
- **Last synchronized ref:** ...
- **Related issues/PRs:** ...
- **Evidence status:** ...
- **Future refresh:** ...
- **Wiki baseline:** ...

</details>
```

The record may include additional version-specific fields such as V1 authority, V2 authority or source refs checked.

## Required provenance fields

For every migrated substantive page, the Documentation record must make these data retrievable:
- Page scope;
- Documentation maturity;
- Last synchronized;
- related issue/PR or primary documentation issue;
- authoritative source/authority;
- synchronized source ref where meaningful;
- evidence status or page-role interpretation;
- future refresh checkpoint where applicable;
- Wiki baseline.

Where an older page did not explicitly carry one of these fields, the migration may add a conservative documentation-level value derived from the page scope and inventory. It must not invent research evidence.

## Page-class policy

### Compact header + Documentation record
- Narrative / Navigation
- Narrative / Research
- Concept / Domain / Model
- Evaluation / Evidence
- Cross-Version Evolution
- Reference / Index

### Expanded governance header may remain
- Status / Governance
- Status / Changelog

Governance/status pages are operational by purpose, so dense metadata there is not reader-facing clutter.

## Source-of-truth rule

Moving metadata changes presentation, not authority. The record remains documentation metadata; ontology/model/evaluation artifacts remain authoritative for their substantive content.

## Migration safety
- Preserve every existing metadata key/value.
- Do not change evidence state, version status, counts, claims or limitations.
- Do not silently replace an exact commit/ref with a weaker source label.
- Do not duplicate a Documentation record on repeated migration.
- Keep the migration script idempotent.

## QA
The metadata checker reports:
- pages by metadata mode;
- compact-header line count;
- expanded-header line count;
- Documentation-record coverage;
- missing provenance fields;
- migrated-page count.

Final #231 acceptance requires every in-scope source-complete page to satisfy the compact contract and every governance/status page to satisfy either its existing expanded contract or a deliberate governance-specific variant.
