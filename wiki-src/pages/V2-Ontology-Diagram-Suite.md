# V2 Ontology Diagram Suite

> **Version scope:** V2  
> **Status:** Stable-to-date / Evolving; semantic review pending  
> **Updated:** 2026-09-24

This suite is the visual companion to [[V2 Ontology Reference]]. It explains the current V2 conceptual/formal baseline at several levels without requiring readers to reconstruct structure from OWL/Turtle or large reference tables.

The diagrams are governed by [[Diagram Standards and Inventory]] and were checked against `v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999`.

## How to read the suite

The hierarchy is intentional:

1. **Architecture level** — where Core, X-INFRA and Extensions sit.
2. **Core overview level** — a readable package view rather than a 32-node graph.
3. **Thematic conceptual views** — detailed concepts, stereotypes, explicit relations and protected distinctions.
4. **Extension landscape** — broad extension coverage without visually inventing cross-domain semantics.

**Authoritative projection** means that displayed nodes/edges are mechanically checked against the named conceptual/formal baseline. It does not mean that concepts or relations with pending semantic review have been human-approved.

**Illustrative** means a reader-oriented simplification whose underlying semantics remain governed by the authoritative artifacts.

## Coverage summary

- Required #235 diagram families: **10/10**
- V2 domains represented at module level: **17/17**
- Unique concept nodes represented in detailed views: **70**
- Unique object properties represented: **39**
- Semantic-validation errors: **0**
- Full concept/property lookup remains in [[V2 Ontology Reference]]; the diagram suite deliberately does not attempt to draw all 87 concepts in one graph.

## 1. V2 ontology architecture — Core, X-INFRA and Extensions — DGM-ONT-002

![DGM-ONT-002 V2 ontology architecture — Core, X-INFRA and Extensions](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/ontology/DGM-ONT-002--v2-ontology-architecture-core-x-infra-and-extensions.svg?sha=57f52a9a4974)

**Artifact status:** Authoritative projection. Top-level architecture of all 17 domains across Core, X-INFRA and Extensions. Placement is architectural grouping, not an object-property assertion.

[PlantUML source](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/source/ontology/DGM-ONT-002--v2-ontology-architecture-core-x-infra-and-extensions.puml) · [SVG](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/rendered/ontology/DGM-ONT-002--v2-ontology-architecture-core-x-infra-and-extensions.svg)

## 2. V2 Core ontology overview — DGM-ONT-003

![DGM-ONT-003 V2 Core ontology overview](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/ontology/DGM-ONT-003--v2-core-ontology-overview.svg?sha=22baaead8666)

**Artifact status:** Illustrative. Readable six-module Core overview with selected explicit relation spans stated as notes. It deliberately avoids a 32-node all-in-one graph.

[PlantUML source](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/source/ontology/DGM-ONT-003--v2-core-ontology-overview.puml) · [SVG](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/rendered/ontology/DGM-ONT-003--v2-core-ontology-overview.svg)

## 3. Ecosystem Organization and Facility Operations — DGM-ONT-004

![DGM-ONT-004 Ecosystem Organization and Facility Operations](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/ontology/DGM-ONT-004--ecosystem-organization-and-facility-operations.svg?sha=4aefd32bc2a8)

**Artifact status:** Authoritative projection. Shows organization/facility identity, contextual roles, the FacilityOperation relator, explicit generalizations, `operates`, and the protected Organization ≠ Facility distinction.

[PlantUML source](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/source/ontology/DGM-ONT-004--ecosystem-organization-and-facility-operations.puml) · [SVG](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/rendered/ontology/DGM-ONT-004--ecosystem-organization-and-facility-operations.svg)

## 4. Pharmaceutical Product and Classification — DGM-ONT-005

![DGM-ONT-005 Pharmaceutical Product and Classification](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/ontology/DGM-ONT-005--pharmaceutical-product-and-classification.svg?sha=312bbc49d459)

**Artifact status:** Authoritative projection. Shows product, presentation, substance, dosage/strength/package, classification and listing structures. Formally unspecified endpoints remain note boxes.

[PlantUML source](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/source/ontology/DGM-ONT-005--pharmaceutical-product-and-classification.puml) · [SVG](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/rendered/ontology/DGM-ONT-005--pharmaceutical-product-and-classification.svg)

## 5. Evidence and Provenance — DGM-ONT-006

![DGM-ONT-006 Evidence and Provenance](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/ontology/DGM-ONT-006--evidence-and-provenance.svg?sha=ff767d56ba68)

**Artifact status:** Authoritative projection. Shows source→dataset→release→record lineage, evidence support, assertions, observations and provenance without treating EvidenceItem as a relation that is not formally asserted.

[PlantUML source](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/source/ontology/DGM-ONT-006--evidence-and-provenance.puml) · [SVG](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/rendered/ontology/DGM-ONT-006--evidence-and-provenance.svg)

## 6. Geography, Jurisdiction and Time — DGM-ONT-007

![DGM-ONT-007 Geography, Jurisdiction and Time](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/ontology/DGM-ONT-007--geography-jurisdiction-and-time.svg?sha=15d06eac9c43)

**Artifact status:** Authoritative projection. Separates geographic identity from regulatory jurisdiction and preserves the Facility ≠ GeographicFeature and GeographicFeature ≠ RegulatoryJurisdiction distinctions.

[PlantUML source](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/source/ontology/DGM-ONT-007--geography-jurisdiction-and-time.puml) · [SVG](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/rendered/ontology/DGM-ONT-007--geography-jurisdiction-and-time.svg)

## 7. Identity and Entity Matching — DGM-ONT-008

![DGM-ONT-008 Identity and Entity Matching](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/ontology/DGM-ONT-008--identity-and-entity-matching.svg?sha=3344cb365666)

**Artifact status:** Authoritative projection. Shows identifier assignment and entity-match assertions while preserving the unspecified identifier/match endpoints.

[PlantUML source](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/source/ontology/DGM-ONT-008--identity-and-entity-matching.puml) · [SVG](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/rendered/ontology/DGM-ONT-008--identity-and-entity-matching.svg)

## 8. Supply Operations and Shortage — DGM-ONT-009

![DGM-ONT-009 Supply Operations and Shortage](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/ontology/DGM-ONT-009--supply-operations-and-shortage.svg?sha=969480137e94)

**Artifact status:** Authoritative projection. Shows shortage-product/presentation/jurisdiction relations, supply capacity and observation-result hierarchy with unspecified bearer/aboutness endpoints retained.

[PlantUML source](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/source/ontology/DGM-ONT-009--supply-operations-and-shortage.puml) · [SVG](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/rendered/ontology/DGM-ONT-009--supply-operations-and-shortage.svg)

## 9. Supply Resilience and Risk — adjacent extension views — DGM-ONT-010

![DGM-ONT-010 Supply Resilience and Risk — adjacent extension views](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/ontology/DGM-ONT-010--supply-resilience-and-risk-adjacent-extension-views.svg?sha=252fad41328b)

**Artifact status:** Authoritative projection. Places Supply Resilience and Risk Management side by side but explicitly states that the current formal baseline asserts no cross-domain object property between them.

[PlantUML source](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/source/ontology/DGM-ONT-010--supply-resilience-and-risk-adjacent-extension-views.puml) · [SVG](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/rendered/ontology/DGM-ONT-010--supply-resilience-and-risk-adjacent-extension-views.svg)

## 10. V2 extension landscape — DGM-ONT-011

![DGM-ONT-011 V2 extension landscape](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/ontology/DGM-ONT-011--v2-extension-landscape.svg?sha=b3f7e648569c)

**Artifact status:** Authoritative projection. Summarizes all eight extension domains and counts without creating an unreadable entity-level extension graph.

[PlantUML source](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/source/ontology/DGM-ONT-011--v2-extension-landscape.puml) · [SVG](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/rendered/ontology/DGM-ONT-011--v2-extension-landscape.svg)

## Semantic safeguards

The suite follows these rules:
- stereotypes are shown as text, not inferred from shape/color alone;
- subclass edges are drawn only when an explicit formal `rdfs:subClassOf` exists;
- object-property arrows are drawn only when formal endpoints match;
- absent OWL domain/range endpoints are rendered as **unspecified** notes rather than guessed classes;
- protected-distinction lines correspond only to registered conceptual distinctions;
- no cardinality, equivalence or additional disjointness is introduced by layout;
- module placement is architectural grouping, not a semantic edge;
- accepted future semantic findings under #213 require regeneration/review of this suite.

## Coverage and QA evidence

Repository evidence:
- `wiki-src/ontology-reference/ontology-diagram-coverage.csv`
- `wiki-src/ontology-reference/ontology-diagram-coverage.json`
- `wiki-src/ontology-reference/ontology-diagram-semantic-review.md`
- `tools/wiki/generate_v2_ontology_diagrams.py`
- `wiki-src/diagrams/manifest.json`

## Relationship to the exhaustive reference

Use the diagrams to build a mental model; use [[V2 Ontology Reference]] for exhaustive lookup of all 17 modules, 87 conceptual elements, 52 object properties and 5 datatype properties. The diagrams do not replace the reference pages or the V2 semantic authority.

---

<details>
<summary>Documentation record</summary>

- **Page scope:** V2
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative source:** V2 conceptual registry, domain review catalog and formal ontology
- **Last synchronized:** 2026-09-24
- **Last synchronized ref:** v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999
- **Related issues/PRs:** #213, #232, #234, #235
- **Evidence status:** 10-diagram visual projection; semantic review status preserved
- **Future refresh:** #213 / #214 as applicable
- **Wiki baseline:** WB-2026.09.1

</details>
