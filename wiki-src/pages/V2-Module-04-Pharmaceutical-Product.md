# Pharmaceutical Product

> **Version scope:** V2  
> **Status:** Pending semantic review  
> **Updated:** 2026-09-24

> Generated module reference projection. Semantic authority remains in the linked V2 conceptual, formal and review artifacts.

## Purpose and scope
Medicinal products, substances, presentations, dosage/strength/package specifications and product classification/listing semantics.

## Layer and architecture
- **Layer:** Core
- **Concept count:** 10
- **Ontology version:** 2.0.0-alpha.1
- **Authority ref:** `v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999`

## Principal concepts
| Concept | Stereotype | Formal entity | Review |
|---|---|---|---|
| [[V2 Concept C016 Medicinal Product|Medicinal Product]] | Kind | OWL Class | pending |
| [[V2 Concept C017 Pharmaceutical Substance|Pharmaceutical Substance]] | Kind | OWL Class | pending |
| [[V2 Concept C018 Medicinal Product Presentation|Medicinal Product Presentation]] | Kind | OWL Class | pending |
| [[V2 Concept C019 Dosage Form Specification|Dosage Form Specification]] | Kind | OWL Class | pending |
| [[V2 Concept C020 Strength|Strength]] | Quality | OWL Class | pending |
| [[V2 Concept C021 Package Configuration|Package Configuration]] | Kind | OWL Class | pending |
| [[V2 Concept C022 Product Classification Scheme|Product Classification Scheme]] | Kind | OWL Class | pending |
| [[V2 Concept C023 Classification Entry|Classification Entry]] | Kind | OWL Class | pending |
| [[V2 Concept C024 Product Classification Assignment|Product Classification Assignment]] | Relator | OWL Class | pending |
| [[V2 Concept C025 Market Listing|Market Listing]] | Relator | OWL Class | pending |

## Relation patterns
| Property | Domain | Range | Review note |
|---|---|---|---|
| [[V2 Object Property presentationOf|`presentationOf`]] | MedicinalProductPresentation | cmpe:MedicinalProduct | Formal relation |
| [[V2 Object Property hasActiveSubstance|`hasActiveSubstance`]] | unspecified | cmpe:PharmaceuticalSubstance | Formal/compositional specification; domain review required |
| [[V2 Object Property hasDosageForm|`hasDosageForm`]] | MedicinalProductPresentation | cmpe:DosageFormSpecification | Formal specification |
| [[V2 Object Property hasStrength|`hasStrength`]] | MedicinalProductPresentation | cmpe:Strength | Characterization |
| [[V2 Object Property hasPackageConfiguration|`hasPackageConfiguration`]] | MedicinalProductPresentation | cmpe:PackageConfiguration | Formal specification |
| [[V2 Object Property classificationEntity|`classificationEntity`]] | ProductClassificationAssignment | unspecified | Relator participant; range review required |
| [[V2 Object Property classificationEntry|`classificationEntry`]] | ProductClassificationAssignment | cmpe:ClassificationEntry | Relator participant |
| [[V2 Object Property entryInScheme|`entryInScheme`]] | ClassificationEntry | cmpe:ProductClassificationScheme | Scheme membership |
| [[V2 Object Property listingPresentation|`listingPresentation`]] | MarketListing | cmpe:MedicinalProductPresentation | Relator participant |
| [[V2 Object Property listingResponsibleOrganization|`listingResponsibleOrganization`]] | MarketListing | cmpe:Organization | Relator participant |
| [[V2 Object Property listingJurisdiction|`listingJurisdiction`]] | MarketListing | cmpe:RegulatoryJurisdiction | Relator participant |
| [[V2 Object Property shortageProduct|`shortageProduct`]] | MedicineShortageSituation | cmpe:MedicinalProduct | Situation involvement |
| [[V2 Object Property shortagePresentation|`shortagePresentation`]] | MedicineShortageSituation | cmpe:MedicinalProductPresentation | Situation involvement |
| [[V2 Object Property contextClassificationProduct|`contextClassificationProduct`]] | ContextualMedicineClassificationAssignment | cmpe:MedicinalProduct | Relator participant |
| [[V2 Object Property contextClassificationEntry|`contextClassificationEntry`]] | ContextualMedicineClassificationAssignment | cmpe:ClassificationEntry | Relator participant |
| [[V2 Object Property alternativeProduct|`alternativeProduct`]] | AlternativeMedicineAssignment | cmpe:MedicinalProduct | Alternative endpoint |
| [[V2 Object Property alternativeForProduct|`alternativeForProduct`]] | AlternativeMedicineAssignment | cmpe:MedicinalProduct | Reference endpoint |

Properties with an unspecified OWL endpoint remain unspecified; this page does not infer the missing endpoint.

## Constraints and protected distinctions
`MedicinalProduct` ≠ `PharmaceuticalSubstance`; `MedicinalProduct` ≠ `MedicinalProductPresentation`

For executable constraints and validation evidence, see [[V2 Formal Ontology and SHACL]] and [[V2 Evaluation E1-E13|CM-PharmE 2.0 Evaluation Framework]].

## Modeling decisions
This module belongs to the **Core** layer in the approved 17-domain V2 review taxonomy. Its definition and concept ownership come from the V2 domain review catalog and integrated conceptual model. The generated page does not move, split, merge or approve concepts.

## Structural example
`MedicinalProductPresentation` — `presentationOf` → `MedicinalProduct`

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
