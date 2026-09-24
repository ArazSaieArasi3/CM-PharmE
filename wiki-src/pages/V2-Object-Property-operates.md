# operates

> **Version scope:** V2  
> **Status:** Pending relation review  
> **Updated:** 2026-09-24

> Generated object-property reference. Missing domain/range values remain **unspecified** and are never inferred by this page.

## Formal definition
| Field | Value |
|---|---|
| IRI | `cmpe:operates` |
| Property type | OWL ObjectProperty |
| Domain | [[V2 Concept C001 Organization|Organization]] |
| Range | [[V2 Concept C009 Facility|Facility]] |
| Formal layer | Core |

## Semantic / review note
Material, derived from Facility Operation

## Related concepts
- **Domain/source:** [[V2 Concept C001 Organization|Organization]]
- **Range/target:** [[V2 Concept C009 Facility|Facility]]

## Formal characteristics
- Explicitly marked as material relation.
- Derived from relator `FacilityOperation`.

## Structural example
[[V2 Concept C001 Organization|Organization]] — `operates` → [[V2 Concept C009 Facility|Facility]]

## Related implementation, mappings and evaluation context
- [[V2 Data Infrastructure]]
- [[V2 Evaluation E1-E13|CM-PharmE 2.0 Evaluation Framework]]
- Mapping authority: `v2/data/mappings/ontology-rdb-mapping.csv`
- Relation/data realization remains bounded to registered mappings.

## Review boundary
- **Review state:** Pending
- Unspecified endpoints are review targets, not automatically defects.
- Catalog generation does not approve relation semantics.

## Authoritative sources
- formal source: `v2/ontology/source/modules/10-core.ttl`
- relation review catalog: `v2/review/relations/index.md`
- integrated conceptual model: `v2/research/w4/integrated-ontouml-model.md`

---

<details>
<summary>Documentation record</summary>

- **Page scope:** V2
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative source:** V2 formal ontology and relation-review catalog
- **Last synchronized:** 2026-09-24
- **Last synchronized ref:** v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999
- **Related issues/PRs:** #213, #234
- **Evidence status:** Generated object-property reference; missing constraints not inferred
- **Future refresh:** #213 / #214 as applicable
- **Wiki baseline:** WB-2026.09.1

</details>
