# Diagram Standards and Inventory

> **Page scope:** Version-neutral governance  
> **Documentation maturity:** Stable diagram policy  
> **Last synchronized:** 2026-09-24  
> **Related issues:** #228, #232, #235  
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

These are intentionally small standard-demonstration diagrams. Complete ontology/database/KG/evaluation visuals are delivered by the later documentation issues.

### DGM-ONT-001 — OntoUML-aware conceptual notation

![DGM-ONT-001 illustrative ontology fragment](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/ontology/DGM-ONT-001--product-presentation-substance.svg)

[Source](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/source/ontology/DGM-ONT-001--product-presentation-substance.puml) · [SVG](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/rendered/ontology/DGM-ONT-001--product-presentation-substance.svg)

### DGM-ERD-001 — Crow's Foot relational notation

![DGM-ERD-001 illustrative evidence ERD](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/erd/DGM-ERD-001--evidence-source-records.svg)

[Source](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/source/erd/DGM-ERD-001--evidence-source-records.mmd) · [SVG](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/rendered/erd/DGM-ERD-001--evidence-source-records.svg)

### DGM-ARC-001 — data/query architecture flow

![DGM-ARC-001 illustrative cross-representation pipeline](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/architecture/DGM-ARC-001--cross-representation-pipeline.svg)

[Source](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/source/architecture/DGM-ARC-001--cross-representation-pipeline.mmd) · [SVG](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/rendered/architecture/DGM-ARC-001--cross-representation-pipeline.svg)

### DGM-EVO-001 — cross-version lineage

![DGM-EVO-001 illustrative V1 to V2 research lineage](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/evolution/DGM-EVO-001--v1-v2-research-lineage.svg)

[Source](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/source/evolution/DGM-EVO-001--v1-v2-research-lineage.dot) · [SVG](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/rendered/evolution/DGM-EVO-001--v1-v2-research-lineage.svg)

## Governed ontology suite

- [[V2 Ontology Diagram Suite]] — 10 semantic-validated V2 ontology diagrams covering all 17 domains at module level and selected thematic concept/relation views.
- Coverage and semantic-review evidence: `wiki-src/ontology-reference/ontology-diagram-coverage.*` and `ontology-diagram-semantic-review.md`.

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
