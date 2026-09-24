# Supply Resilience

> **Version scope:** V2  
> **Status:** Pending semantic review  
> **Updated:** 2026-09-24

> Generated module reference projection. Semantic authority remains in the linked V2 conceptual, formal and review artifacts.

## Purpose and scope
Contextual criticality, alternatives, dependencies, disruption, procurement, inventory, lead-time and stockout semantics for resilience analysis.

## Layer and architecture
- **Layer:** Extension
- **Concept count:** 11
- **Ontology version:** 2.0.0-alpha.1
- **Authority ref:** `v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999`

## Principal concepts
| Concept | Stereotype | Formal entity | Review |
|---|---|---|---|
| [[V2 Concept C060 Contextual Medicine Classification Assignment|Contextual Medicine Classification Assignment]] | Relator | OWL Class | pending |
| [[V2 Concept C061 Essential Medicine Classification Assignment|Essential Medicine Classification Assignment]] | Subkind | OWL Class | pending |
| [[V2 Concept C062 Critical Medicine Classification Assignment|Critical Medicine Classification Assignment]] | Subkind | OWL Class | pending |
| [[V2 Concept C063 Alternative Medicinal Product|Alternative Medicinal Product]] | Role | OWL Class | pending |
| [[V2 Concept C064 Alternative Medicinal Product Assignment|Alternative Medicinal Product Assignment]] | Relator | OWL Class | pending |
| [[V2 Concept C065 Supply Dependency|Supply Dependency]] | Relator | OWL Class | pending |
| [[V2 Concept C066 Disruption Event|Disruption Event]] | Event | OWL Class | pending |
| [[V2 Concept C067 Inventory Observation Result|Inventory Observation Result]] | Subkind | OWL Class | pending |
| [[V2 Concept C068 Procurement Activity|Procurement Activity]] | Event | OWL Class | pending |
| [[V2 Concept C069 Lead Time Observation Result|Lead Time Observation Result]] | Subkind | OWL Class | pending |
| [[V2 Concept C070 Stockout Situation|Stockout Situation]] | Situation | OWL Class | pending |

## Relation patterns
| Property | Domain | Range | Review note |
|---|---|---|---|
| [[V2 Object Property contextClassificationProduct|`contextClassificationProduct`]] | ContextualMedicineClassificationAssignment | cmpe:MedicinalProduct | Relator participant |
| [[V2 Object Property contextClassificationEntry|`contextClassificationEntry`]] | ContextualMedicineClassificationAssignment | cmpe:ClassificationEntry | Relator participant |
| [[V2 Object Property contextClassificationJurisdiction|`contextClassificationJurisdiction`]] | ContextualMedicineClassificationAssignment | cmpe:RegulatoryJurisdiction | Context participant |
| [[V2 Object Property alternativeProduct|`alternativeProduct`]] | AlternativeMedicineAssignment | cmpe:MedicinalProduct | Alternative endpoint |
| [[V2 Object Property alternativeForProduct|`alternativeForProduct`]] | AlternativeMedicineAssignment | cmpe:MedicinalProduct | Reference endpoint |
| [[V2 Object Property dependencyDependent|`dependencyDependent`]] | SupplyDependency | unspecified | Dependency endpoint; range review required |
| [[V2 Object Property dependencyProvider|`dependencyProvider`]] | SupplyDependency | unspecified | Dependency endpoint; range review required |
| [[V2 Object Property disruptionAffects|`disruptionAffects`]] | DisruptionEvent | unspecified | Event participant; range review required |

Properties with an unspecified OWL endpoint remain unspecified; this page does not infer the missing endpoint.

## Constraints and protected distinctions
No Gate-D protected distinction is registered specifically for this module.

For executable constraints and validation evidence, see [[V2 Formal Ontology and SHACL]] and [[V2 Evaluation E1-E13|CM-PharmE 2.0 Evaluation Framework]].

## Modeling decisions
This module belongs to the **Extension** layer in the approved 17-domain V2 review taxonomy. Its definition and concept ownership come from the V2 domain review catalog and integrated conceptual model. The generated page does not move, split, merge or approve concepts.

## Structural example
`ContextualMedicineClassificationAssignment` — `contextClassificationProduct` → `MedicinalProduct`

This is a structural relation example, not an instance-data claim.

## Evaluation and competency-question context
- [[V2 Evaluation E1-E13|CM-PharmE 2.0 Evaluation Framework]]
- [[V2 Formal Ontology and SHACL]]
- [[V2 Human Ontology Review|CM-PharmE 2.0 Semantic Review]]

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
