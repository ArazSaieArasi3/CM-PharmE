# Facility Operations

> **Version scope:** V2  
> **Status:** Pending semantic review  
> **Updated:** 2026-09-24

> Generated module reference projection. Semantic authority remains in the linked V2 conceptual, formal and review artifacts.

## Purpose and scope
Physical or organizational facilities and the operational roles/relators through which sites participate in pharmaceutical activities.

## Layer and architecture
- **Layer:** Core
- **Concept count:** 4
- **Ontology version:** 2.0.0-alpha.1
- **Authority ref:** `v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999`

## Principal concepts
| Concept | Stereotype | Formal entity | Review |
|---|---|---|---|
| [[V2 Concept C009 Facility|Facility]] | Kind | OWL Class | pending |
| [[V2 Concept C010 Manufacturing Site|Manufacturing Site]] | Role | OWL Class | pending |
| [[V2 Concept C011 Distribution Site|Distribution Site]] | Role | OWL Class | pending |
| [[V2 Concept C012 Facility Operation|Facility Operation]] | Relator | OWL Class | pending |

## Relation patterns
| Property | Domain | Range | Review note |
|---|---|---|---|
| [[V2 Object Property operates|`operates`]] | Organization | cmpe:Facility | Material, derived from Facility Operation |
| [[V2 Object Property operationOrganization|`operationOrganization`]] | FacilityOperation | cmpe:Organization | Relator participant |
| [[V2 Object Property operationFacility|`operationFacility`]] | FacilityOperation | cmpe:Facility | Relator participant |

Properties with an unspecified OWL endpoint remain unspecified; this page does not infer the missing endpoint.

## Constraints and protected distinctions
`Organization` ≠ `Facility`; `Facility` ≠ `GeographicFeature`

For executable constraints and validation evidence, see [[V2 Formal Ontology and SHACL]] and [[V2 Evaluation E1-E13|CM-PharmE 2.0 Evaluation Framework]].

## Modeling decisions
This module belongs to the **Core** layer in the approved 17-domain V2 review taxonomy. Its definition and concept ownership come from the V2 domain review catalog and integrated conceptual model. The generated page does not move, split, merge or approve concepts.

## Structural example
`Organization` — `operates` → `Facility`

This is a structural relation example, not an instance-data claim.

## Evaluation and competency-question context
- [[V2 Evaluation E1-E13|CM-PharmE 2.0 Evaluation Framework]]
- [[V2 Formal Ontology and SHACL]]
- [[V2 Human Ontology Review|CM-PharmE 2.0 Semantic Review]]

## Related implementation, mappings and visual/evaluation context
- [[V2 Data Infrastructure]]
- [[V2 Evaluation E1-E13|CM-PharmE 2.0 Evaluation Framework]]
- [[Diagram Standards and Inventory]]
- Mapping authority: `v2/data/mappings/ontology-rdb-mapping.csv`
- Dataset→ontology evaluation: `v2/research/w7/e6-dataset-ontology-mapping-quality.md`
- Ontology↔RDB↔KG evaluation: `v2/research/w7/e10-ontology-rdb-kg-semantic-consistency.md`
- Ontology-specific diagram suite is governed separately by #235.

## Known boundaries
- Current domain review state: **Pending**.
- Generated reference does not constitute human/author semantic approval.
- Coverage does not imply pharmaceutical-domain completeness.
- Future accepted findings are synchronized through #213.

## Authoritative sources
- V2 domain review catalog: `v2/review/domains/index.md`
- conceptual registry: `v2/ontouml/cm-pharme-v2.conceptual-model.json`
- formal ontology modules: `v2/ontology/source/modules/*.ttl`

---

<details>
<summary>Documentation record</summary>

- **Page scope:** V2
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative source:** V2 domain review catalog, conceptual registry and formal ontology
- **Last synchronized:** 2026-09-24
- **Last synchronized ref:** v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999
- **Related issues/PRs:** #213, #234
- **Evidence status:** Generated reference projection; semantic approval not implied
- **Future refresh:** #213 / #214 as applicable
- **Wiki baseline:** WB-2026.09.1

</details>
