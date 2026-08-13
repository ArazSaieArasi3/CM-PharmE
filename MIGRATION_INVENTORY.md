# CM-PharmE Migration Inventory

## Purpose

This file records the pre-refactor repository baseline and the preservation/migration plan for all artifacts that existed before the research-repository restructuring began.

## Baseline

- Repository: `ArazSaieArasi3/CM-PharmE`
- Baseline branch: `main`
- Baseline commit: `9efd0e3ac909e4065012fae7aeb6b0a94029c440`
- Preservation branch: `archive/pre-refactor-2026-08-13`
- Migration branch: `refactor/research-repository-v1`
- Preservation rule: no released semantic or scholarly artifact from the baseline is to be hard-deleted during migration; historical artifacts must remain reproducible and traceable.

## Baseline Artifact Inventory

| Original Path | Artifact Type | Preservation Decision | Materialized Historical Target |
|---|---|---|---|
| `README.md` | Markdown | Preserve academic content, especially authors, affiliations, ORCID links, research context, publication provenance and evolving-model note | Root README redesigned model-centrically; publication/history content preserved in dedicated records |
| `models/CM-PharmE-1.0/CM-PharmE-1.0.drawio` | Draw.io source | Preserve byte-for-byte | `releases/v1.0.0/model/CM-PharmE-1.0.drawio` |
| `models/CM-PharmE-1.0/CM-PharmE-1.0.owl` | OWL/RDF/XML | Preserve byte-for-byte; do not treat as cleaned canonical ontology | `releases/v1.0.0/ontology/CM-PharmE-1.0.owl` |
| `models/CM-PharmE-1.0/CM-PharmE-1.0.png` | PNG | Preserve byte-for-byte | `releases/v1.0.0/model/CM-PharmE-1.0.png` |
| `models/CM-PharmE-1.0/CM-PharmE-1.0.xml` | XML | Preserve byte-for-byte | `releases/v1.0.0/model/CM-PharmE-1.0.xml` |
| `models/CM-PharmE-1.0/Domains of CM-PharmE-1.0.png` | PNG | Preserve byte-for-byte | `releases/v1.0.0/model/Domains-of-CM-PharmE-1.0.png` |

## Migration Principles

1. Historical scholarly/model artifacts remain reproducible.
2. No hard delete of released semantic entities.
3. Current-development artifacts are separated from immutable release snapshots.
4. The root README is model-centric while preserving visible academic credibility.
5. Authors, affiliations, ORCID links, and featured publications remain visible on the root README.
6. Every migrated/reclassified artifact remains traceable to its original path and baseline commit.
7. Generated ontology/documentation distributions should not become independent manual sources of truth.

## Batch Status

- [x] B0 — Baseline commit recorded
- [x] B0 — Preservation branch created
- [x] B0 — Migration branch created
- [x] B0 — Baseline artifacts inventoried
- [x] B1 — Target foundation structure created
- [x] B1 — Historical release `v1.0.0` materialized
- [x] B1 — Root README redesigned while retaining authors/affiliations/ORCID/publication visibility
- [x] B1 — `CHANGELOG.md` and `CITATION.cff` added
- [x] B1 — Versioning and lifecycle policies added
- [x] B1 — Publication registry and v1.0.0 publication record added
- [ ] B2 — Concept/relation/domain registries created
- [ ] B2 — Current/vNext conceptual model documented
- [ ] B3 — Formal ontology re-engineered
- [ ] B4 — Evaluation and methodology packages completed
- [ ] B5 — Generators, validation, final audit and release workflow completed
