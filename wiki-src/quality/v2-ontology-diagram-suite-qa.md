# V2 ontology diagram-suite QA report

**Issue:** #235  
**Date:** 2026-09-24  
**Authority ref:** `v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999`

## Result

**PASS — the 10-diagram V2 ontology suite is generated, semantically checked and integrated into the Wiki source with zero automated semantic-validation errors.**

## Required families

| # | Diagram | ID | Status |
|---:|---|---|---|
| 1 | V2 ontology architecture — Core / X-INFRA / Extensions | DGM-ONT-002 | PASS |
| 2 | V2 Core ontology overview | DGM-ONT-003 | PASS |
| 3 | Ecosystem Organization and Facility Operations | DGM-ONT-004 | PASS |
| 4 | Pharmaceutical Product and Classification | DGM-ONT-005 | PASS |
| 5 | Evidence and Provenance | DGM-ONT-006 | PASS |
| 6 | Geography, Jurisdiction and Time | DGM-ONT-007 | PASS |
| 7 | Identity and Entity Matching | DGM-ONT-008 | PASS |
| 8 | Supply Operations and Shortage | DGM-ONT-009 | PASS |
| 9 | Supply Resilience and Risk — adjacent extension views | DGM-ONT-010 | PASS |
| 10 | V2 extension landscape | DGM-ONT-011 | PASS |

## Coverage

- Required diagram families: **10/10**
- V2 domains represented at module level: **17/17**
- Unique concept nodes in detailed views: **70**
- Unique OWL object properties represented: **39**
- Automated semantic-validation errors: **0**

Entity-level coverage is intentionally selective. The exhaustive 87-concept / 57-property lookup remains in [[V2 Ontology Reference]]; the diagram suite avoids the explicitly rejected unreadable all-in-one graph.

## Semantic checks

Generation validates directly against the V2 conceptual/formal authority:
- concept nodes resolve in the 87-element conceptual registry;
- displayed UFO/OntoUML stereotypes match the registry;
- generalization edges match explicit `rdfs:subClassOf`;
- object-property arrows match explicit OWL domain/range;
- absent formal endpoints are shown as `unspecified`, not inferred;
- protected-distinction lines resolve to registered protected distinctions;
- all 17 domains resolve in the current domain-review taxonomy.

## Visual QA corrections before PR

The first generated SVG pass exposed presentation defects that mechanical semantic QA alone could not detect. Before PR:
- long node/note labels were wrapped;
- node height/row spacing was increased;
- edge endpoints were moved from box centers to box boundaries;
- parallel edges receive offsets;
- repeated `subClassOf` text was removed from the SVG while retaining the hollow-triangle notation;
- long edge labels were wrapped;
- `operates` and the Organization ≠ Facility distinction no longer render on the exact same line;
- legend text states what visual conventions do and do not imply.

## Reader-facing integration

- New page: [[V2 Ontology Diagram Suite]]
- architecture diagram embedded in [[V2 UFO and OntoUML Architecture]]
- architecture diagram embedded in [[V2 Ontology Reference]]
- suite linked from [[Ontology and Conceptual Model Guide]]
- suite linked from all **17 V2 module reference pages**
- suite registered in [[Diagram Standards and Inventory]]

## Maintainability

- generator: `tools/wiki/generate_v2_ontology_diagrams.py`
- suite checker: `tools/wiki/check_v2_ontology_diagram_suite.py`
- generic diagram checker: `tools/wiki/check_diagrams.py`
- coverage CSV/JSON and semantic-review checklist under `wiki-src/ontology-reference/`
- normal Wiki CI checks out `v2/research-program`, regenerates the suite and requires a zero diff.

Thus a later ontology change cannot silently leave the committed diagrams stale.

## Semantic-review boundary

The suite is an authoritative **projection** where stated, not a new semantic authority and not human/author approval of currently pending concepts/relations. Accepted semantic findings under #213 require regeneration and review.
