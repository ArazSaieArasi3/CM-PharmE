# Diagram Standards and Inventory

> **Page scope:** Version-neutral governance  
> **Documentation maturity:** Stable diagram policy  
> **Last synchronized:** 2026-09-24  
> **Related issues:** #228, #232  
> **Wiki baseline:** WB-2026.09.1

Diagrams in CM-PharmE are documentation/semantic artifacts, not decoration. Different questions require different notations.

## Notation by problem

| Problem | Preferred notation |
|---|---|
| ontology/conceptual model | OntoUML/UFO-aware conceptual notation |
| relational database | Crow's Foot ERD |
| data/query pipeline | data-flow / architecture flow |
| software/application architecture | C4 where appropriate |
| research/evaluation process | process/activity/flow |
| cross-version evolution | lineage/evolution |

C4 must not be used as ontology notation. ERD must not substitute for the conceptual ontology.

## Artifact contract

Every governed diagram records title, purpose, version/scope, notation, source, rendered artifact, artifact status, generation method, checked ref, caption, alt text and related Wiki pages.

The machine-readable inventory is `wiki-src/diagrams/manifest.json`.

## Initial notation samples

- **DGM-ONT-001** — OntoUML-aware product/presentation/substance fragment.
- **DGM-ERD-001** — Crow's Foot evidence/source relational fragment.
- **DGM-ARC-001** — cross-representation data/query pipeline.
- **DGM-EVO-001** — V1→V2 research-evolution lineage.

These are intentionally small standard-demonstration diagrams. Complete ontology/database/KG/evaluation visuals are delivered by the later documentation issues.

## Legacy assets

The V1 model PNGs are accompanied by draw.io sources and are therefore grandfathered as editable legacy artifacts. New diagrams should prefer source-controlled SVG publication.

## QA

New/changed diagram entries are checked in CI for:
- unique IDs;
- allowed notation/status;
- source and SVG existence;
- file-name/ID alignment;
- SVG viewBox/title/description;
- caption/alt text;
- related pages;
- checked ref;
- source/rendered separation.

## Full standard

See `wiki-src/diagrams/STYLE-GUIDE.md` for the complete notation, styling, accessibility, naming, tool and staleness policy.
