# Medicinal Product Presentation

> **Version scope:** V2  
> **Status:** pending semantic review  
> **Updated:** 2026-09-24

> Generated concept reference from the V2 Concept Evidence Passport and formal ontology. This page does not create or approve semantics.

## Canonical definition
> Independently identifiable marketed/presented configuration of a medicinal product.

## Ontological role
| Field | Value |
|---|---|
| Concept ID | `CMPE-V2-C018` |
| Domain | [[V2 Module 04 Pharmaceutical Product|Pharmaceutical Product]] |
| Layer | Core |
| OntoUML stereotype | Kind |
| Formal entity type | OWL Class |
| Formal IRI | `cmpe:MedicinalProductPresentation` |

## Generalization
No explicit formal parent is declared in the parsed source statement.

## Principal formal relations
| Direction | Property | Other endpoint | Constraint status |
|---|---|---|---|
| Outgoing | [[V2 Object Property presentationOf|`presentationOf`]] | cmpe:MedicinalProduct | explicit domain and range |
| Outgoing | [[V2 Object Property hasDosageForm|`hasDosageForm`]] | cmpe:DosageFormSpecification | explicit domain and range |
| Outgoing | [[V2 Object Property hasStrength|`hasStrength`]] | cmpe:Strength | explicit domain and range |
| Outgoing | [[V2 Object Property hasPackageConfiguration|`hasPackageConfiguration`]] | cmpe:PackageConfiguration | explicit domain and range |
| Incoming | [[V2 Object Property listingPresentation|`listingPresentation`]] | MarketListing | explicit range and domain |
| Incoming | [[V2 Object Property shortagePresentation|`shortagePresentation`]] | MedicineShortageSituation | explicit range and domain |

Properties whose endpoint is formally unspecified are not inferred into this list.

## Constraints / SHACL relevance
- Protected conceptual distinction(s): `MedicinalProductPresentation ≠ MedicinalProduct`.
- Current SHACL source references `cmpe:MedicinalProductPresentation`. This is a syntactic reference observation, not a completeness judgment.
- See [[V2 Formal Ontology and SHACL]] for constraint semantics and validation scope.

## Evidence and provenance
- **Dataset/source evidence:** P1/P2/P4/P5
- **Held-out evidence:** H1 partial; H2 exact
- **Other support:** O1/O3/O4/M1/M2
- **Review focus:** confirm the registered definition and stereotype against admitted and held-out evidence.

## V1 lineage
- **Migration treatment:** New
- See [[V1 to V2 Concept Migration]] and [[V1 to V2 Research Evolution]] for cross-version interpretation.

## Structural example
`MedicinalProductPresentation` — `presentationOf` → `cmpe:MedicinalProduct`

This is a structural example grounded in explicit formal endpoints, not an instance-data assertion.

## Boundary / non-example
Protected conceptual distinction(s): `MedicinalProductPresentation ≠ MedicinalProduct`.

A source record, identifier or label should not be treated as this domain entity unless the governing ontology/evidence relation explicitly supports that interpretation.

## Review state
- **Passport review state:** pending
- **Evidence status:** registered_not_human_approved
- **Human/author disposition:** Pending

Pending status remains pending until the governed semantic review records a disposition.

## Authoritative sources
- Concept Evidence Passport: `v2/review/concepts/passports/018-medicinal-product-presentation.md`
- conceptual registry: `v2/ontouml/cm-pharme-v2.conceptual-model.json`
- formal source: `v2/ontology/source/modules/10-core.ttl`
- review/evolution package: `v2/review/version-evolution.md`

---

<details>
<summary>Documentation record</summary>

- **Page scope:** V2
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative source:** V2 Concept Evidence Passport, conceptual registry and formal ontology
- **Last synchronized:** 2026-09-24
- **Last synchronized ref:** v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999
- **Related issues/PRs:** #213, #234
- **Evidence status:** Generated concept reference; registered review/evidence status preserved
- **Future refresh:** #213 / #214 as applicable
- **Wiki baseline:** WB-2026.09.1

</details>
