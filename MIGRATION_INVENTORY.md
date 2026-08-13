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

| Original Path | Artifact Type | Current Role | Preservation Decision | Planned Target Role |
|---|---|---|---|---|
| `README.md` | Markdown | Academic landing page for CM-PharmE v1.0 | Preserve content; do not lose authors, affiliations, ORCID links, abstract/history, publication context, or evolving-model note | Reorganize into a model-centric root README while preserving academic credibility; archive scholarly/version-specific content under publication/history documentation |
| `models/CM-PharmE-1.0/CM-PharmE-1.0.drawio` | Draw.io source | Editable conceptual-model source for v1.0 | Preserve byte-for-byte as historical artifact | Historical model source for release `v1.0.0`; future current model maintained separately |
| `models/CM-PharmE-1.0/CM-PharmE-1.0.owl` | OWL/RDF/XML | Auto-converted ontology artifact for v1.0 | Preserve byte-for-byte; do not treat as cleaned canonical ontology | Historical ontology artifact for `v1.0.0`; future formal ontology maintained separately |
| `models/CM-PharmE-1.0/CM-PharmE-1.0.png` | PNG | Full conceptual-model visualization for v1.0 | Preserve byte-for-byte | Historical full-model image for `v1.0.0`; also usable as publication evidence/reference |
| `models/CM-PharmE-1.0/CM-PharmE-1.0.xml` | XML | Draw.io/XML representation for v1.0 | Preserve byte-for-byte | Historical editable/source representation for `v1.0.0` |
| `models/CM-PharmE-1.0/Domains of CM-PharmE-1.0.png` | PNG | Domain-view visualization for v1.0 | Preserve byte-for-byte | Historical domain-view image for `v1.0.0`; future domain documentation maintained separately |

## Migration Principles

1. **Historical preservation:** baseline scholarly/model artifacts remain reproducible.
2. **No hard delete of released semantic entities:** concepts, relations, and domains that have appeared in a released version are retired/deprecated rather than erased from history.
3. **Current vs. release separation:** current development artifacts are separated from immutable release snapshots.
4. **Model-centric home page:** the future root README presents CM-PharmE as an evolving research model rather than as a single-paper repository.
5. **Academic credibility on the home page:** authors, affiliations, ORCID links, and featured publications remain visible in the root README because journal reviewers and academic readers may use the repository as evidence of scholarly provenance and credibility.
6. **Traceability:** every migrated or reclassified baseline artifact must remain traceable from its original path and baseline commit to its new role.
7. **Single-source preference:** generated ontology/documentation distributions should not become independent manual sources of truth.

## Status

- [x] Baseline commit recorded
- [x] Preservation branch created
- [x] Migration branch created
- [x] Baseline artifacts inventoried
- [ ] Target repository structure created
- [ ] Historical release `v1.0.0` materialized
- [ ] Root README redesigned
- [ ] Concept/relation/domain registries created
- [ ] Formal ontology re-engineered
- [ ] Evaluation and publication traceability added

