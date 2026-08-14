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
| `README.md` | Markdown | Preserve academic content, especially authors, affiliations, ORCID links, research context, publication provenance and evolving-model note | Exact original preserved at `releases/v1.0.0/README.original.md`; root README redesigned model-centrically while retaining visible academic credibility |
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

## B2 Semantic Inventory Result

- 39 canonical concepts from 40 graphical concept occurrences
- 40 canonical relations from 41 labeled semantic relation occurrences
- 5 domains
- 39 per-concept pages
- 40 per-relation pages
- 5 per-domain pages
- Concept↔Domain and Concept↔Relation traceability mappings
- Frozen v1.0 concept/relation/domain registries
- Structural extraction audit with explicit source-model review flags

## Batch Status

- [x] B0 — Baseline commit recorded
- [x] B0 — Preservation branch created
- [x] B0 — Migration branch created
- [x] B0 — Baseline artifacts inventoried
- [x] B1 — Target foundation structure created
- [x] B1 — Historical release `v1.0.0` materialized
- [x] B1 — Exact original v1.0 scholarly README preserved inside the release snapshot
- [x] B1 — Root README redesigned while retaining authors/affiliations/ORCID/publication visibility
- [x] B1 — `CHANGELOG.md` and `CITATION.cff` added
- [x] B1 — Versioning and lifecycle policies added
- [x] B1 — Publication registry and v1.0.0 publication record added
- [x] B2 — Canonical concept/relation/domain registries created
- [x] B2 — Stable IDs assigned to concepts, relations and domains
- [x] B2 — One page per canonical concept, relation and domain created
- [x] B2 — Concept↔Domain and Concept↔Relation mappings created
- [x] B2 — v1.0 release semantic inventory and frozen registries created
- [x] B2 — Current model baseline documented independently from manuscript revision numbers
- [x] B2 — Structural extraction audit and descriptive statistics recorded
- [ ] B3 — Formal ontology re-engineered
- [ ] B4 — Evaluation and methodology packages completed
- [ ] B5 — Generators, validation, final audit and release workflow completed
