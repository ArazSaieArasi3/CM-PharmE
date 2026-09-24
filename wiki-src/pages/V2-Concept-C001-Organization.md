# Organization

> **Version scope:** V2  
> **Status:** pending semantic review  
> **Updated:** 2026-09-24

> Generated concept reference from the V2 Concept Evidence Passport and formal ontology. This page does not create or approve semantics.

## Canonical definition
> Institutional, legal, or social entity that can bear contextual pharmaceutical roles.

## Ontological role
| Field | Value |
|---|---|
| Concept ID | `CMPE-V2-C001` |
| Domain | [[V2 Module 01 Ecosystem Organization|Ecosystem Organization]] |
| Layer | Core |
| OntoUML stereotype | Kind |
| Formal entity type | OWL Class |
| Formal IRI | `cmpe:Organization` |

## Generalization
No explicit formal parent is declared in the parsed source statement.

## Principal formal relations
| Direction | Property | Other endpoint | Constraint status |
|---|---|---|---|
| Outgoing | [[V2 Object Property operates|`operates`]] | cmpe:Facility | explicit domain and range |
| Incoming | [[V2 Object Property operationOrganization|`operationOrganization`]] | FacilityOperation | explicit range and domain |
| Incoming | [[V2 Object Property registrationAuthority|`registrationAuthority`]] | EstablishmentRegistration | explicit range and domain |
| Incoming | [[V2 Object Property authorizationAuthority|`authorizationAuthority`]] | RegulatoryAuthorization | explicit range and domain |
| Incoming | [[V2 Object Property listingResponsibleOrganization|`listingResponsibleOrganization`]] | MarketListing | explicit range and domain |

Properties whose endpoint is formally unspecified are not inferred into this list.

## Constraints / SHACL relevance
- Protected conceptual distinction(s): `Organization ≠ Facility`.
- Current SHACL source references `cmpe:Organization`. This is a syntactic reference observation, not a completeness judgment.
- See [[V2 Formal Ontology and SHACL]] for constraint semantics and validation scope.

## Evidence and provenance
- **Dataset/source evidence:** —
- **Held-out evidence:** —
- **Other support:** —
- **Review focus:** —

## V1 lineage
- **Migration treatment:** Refined / generalized
- See [[V1 to V2 Concept Migration]] and [[V1 to V2 Research Evolution]] for cross-version interpretation.

## Structural example
`Organization` — `operates` → `cmpe:Facility`

This is a structural example grounded in explicit formal endpoints, not an instance-data assertion.

## Boundary / non-example
Protected conceptual distinction(s): `Organization ≠ Facility`.

A source record, identifier or label should not be treated as this domain entity unless the governing ontology/evidence relation explicitly supports that interpretation.

## Related implementation, mappings and visual/evaluation context
- [[V2 Data Infrastructure]]
- [[V2 Evaluation E1-E13|CM-PharmE 2.0 Evaluation Framework]]
- [[Diagram Standards and Inventory]]
- Mapping authority: `v2/data/mappings/ontology-rdb-mapping.csv`
- Concept/data mapping evidence remains governed by the mapping registry and E6/E10 artifacts; this generated page does not infer a direct table mapping.

## Review state
- **Passport review state:** pending
- **Evidence status:** registered_not_human_approved
- **Human/author disposition:** Pending

Pending status remains pending until the governed semantic review records a disposition.

## Authoritative sources
- Concept Evidence Passport: `v2/review/concepts/passports/001-organization.md`
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
