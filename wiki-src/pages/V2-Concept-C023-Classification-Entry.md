# Classification Entry

> **Version scope:** V2  
> **Status:** pending semantic review  
> **Updated:** 2026-09-24

> Generated concept reference from the V2 Concept Evidence Passport and formal ontology. This page does not create or approve semantics.

## Canonical definition
> Identified category/entry within a classification scheme.

## Ontological role
| Field | Value |
|---|---|
| Concept ID | `CMPE-V2-C023` |
| Domain | [[V2 Module 04 Pharmaceutical Product|Pharmaceutical Product]] |
| Layer | Core |
| OntoUML stereotype | Kind |
| Formal entity type | OWL Class |
| Formal IRI | `cmpe:ClassificationEntry` |

## Generalization
No explicit formal parent is declared in the parsed source statement.

## Principal formal relations
| Direction | Property | Other endpoint | Constraint status |
|---|---|---|---|
| Incoming | [[V2 Object Property classificationEntry|`classificationEntry`]] | ProductClassificationAssignment | explicit range and domain |
| Outgoing | [[V2 Object Property entryInScheme|`entryInScheme`]] | cmpe:ProductClassificationScheme | explicit domain and range |
| Incoming | [[V2 Object Property contextClassificationEntry|`contextClassificationEntry`]] | ContextualMedicineClassificationAssignment | explicit range and domain |

Properties whose endpoint is formally unspecified are not inferred into this list.

## Constraints / SHACL relevance
- No Gate-D protected distinction is registered for this concept.
- Current SHACL source references `cmpe:ClassificationEntry`. This is a syntactic reference observation, not a completeness judgment.
- See [[V2 Formal Ontology and SHACL]] for constraint semantics and validation scope.

## Evidence and provenance
- **Dataset/source evidence:** P1/P2/P4/P5
- **Held-out evidence:** H2 exact; H3 exact
- **Other support:** O4/O5/M1/M2
- **Review focus:** confirm the registered definition and stereotype against admitted and held-out evidence.

## V1 lineage
- **Migration treatment:** New W4 split
- See [[V1 to V2 Concept Migration]] and [[V1 to V2 Research Evolution]] for cross-version interpretation.

## Structural example
`ProductClassificationAssignment` — `classificationEntry` → `ClassificationEntry`

This is a structural example grounded in explicit formal endpoints, not an instance-data assertion.

## Boundary / non-example
No Gate-D protected distinction is registered for this concept.

A source record, identifier or label should not be treated as this domain entity unless the governing ontology/evidence relation explicitly supports that interpretation.

## Review state
- **Passport review state:** pending
- **Evidence status:** registered_not_human_approved
- **Human/author disposition:** Pending

Pending status remains pending until the governed semantic review records a disposition.

## Authoritative sources
- Concept Evidence Passport: `v2/review/concepts/passports/023-classification-entry.md`
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
