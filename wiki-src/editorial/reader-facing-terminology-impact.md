# Reader-facing terminology migration — implementation record

**Issue:** #229  
**Policy:** `wiki-src/editorial/reader-facing-terminology.md`  
**Baseline:** WB-2026.09.1 evidence preserved

## Scope

This migration reduces reader-facing exposure to internal research-management terminology without deleting the internal identifiers needed for provenance and audit.

## Canonical visible-title changes

| Compatibility slug | Previous visible title | New canonical visible title |
|---|---|---|
| V2-Research-Program-and-Gates | V2 Research Program and Gates | CM-PharmE 2.0 Research Method and Development |
| V2-Evaluation-E1-E13 | V2 Evaluation E1-E13 | CM-PharmE 2.0 Evaluation Framework |
| V2-Human-Ontology-Review | V2 Human Ontology Review | CM-PharmE 2.0 Semantic Review |
| Gate-and-Claim-Dispositions | Gate and Claim Dispositions | Evidence Scope and Supported Claims |

Compatibility slugs are intentionally retained during #229. Any coordinated slug migration belongs to #230 so navigation and redirects can be handled as one information-architecture change.

## Navigation changes

Home and Sidebar display descriptive labels while targeting the existing compatibility slugs.

Internal workstream/checkpoint terminology is no longer required to understand:
- the V2 research sequence;
- the evaluation framework;
- semantic review;
- supported/deferred claims.

## Narrative changes

Primary prose now leads with:
- research stages rather than Waves;
- research decision checkpoints rather than Gates;
- conceptual baseline rather than Gate D;
- evidence sufficiency review rather than Gate F;
- demonstrator evaluation rather than Gate G;
- research release readiness rather than Gate H;
- semantic review rather than Human Ontology Review.

Exact internal identifiers remain in:
- provenance columns;
- evidence-link labels;
- repository artifact paths;
- internal status notes where useful.

## Scientific-equivalence statement

This migration does **not** change:
- V1/V2 semantic authority;
- concept/property/table counts;
- evaluation results;
- supported/deferred claim dispositions;
- current issue/PR status;
- limitations/non-claims;
- research readiness status.

## Regression control

`tools/wiki/check_reader_vocabulary.py` verifies:
- canonical H1 titles;
- approved Home/Sidebar aliases;
- absence of internal-process branding in canonical H1s;
- authoring-standard linkage to the terminology policy.

Body-level internal identifiers are measured but deliberately not forbidden because provenance must remain recoverable.
