# V1 Concepts

> **Page scope:** V1  
> **Documentation maturity:** Stable  
> **Authoritative source:** `main/catalog/concepts.yaml` and `main/docs/concepts/`  
> **Last synchronized:** 2026-09-23  
> **Last synchronized ref:** `5099888668d35f798e4759e3534e707ed906db24`  
> **Related issues/PRs:** V1 model normalization  
> **Evidence status:** 39 canonical concepts  
> **Future refresh:** V1 remains frozen; migration is documented separately  
> **Wiki baseline:** WB-2026.09.1 Candidate

## Inventory

V1 has **39 canonical concepts** across five stereotype families:

| Stereotype | Count |
|---|---:|
| kind | 13 |
| mode | 8 |
| role | 7 |
| relator | 6 |
| perdurant | 5 |

The canonical concept registry is the semantic reference. Wiki descriptions should not create alternate definitions.

## How to use this page

For each concept, inspect:
1. canonical ID/name;
2. OntoUML stereotype;
3. primary/cross-domain membership;
4. linked relations;
5. provenance and semantic review flags;
6. later V1→V2 migration status where available.

## Authoritative indexes

- [Concept documentation index](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/concepts/index.md)
- [Canonical concept catalog](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/catalog/concepts.yaml)
- [Concept-domain mapping](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/mappings/concept-domain.csv)
- [Concept-relation mapping](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/mappings/concept-relation.csv)

## Version discipline

A concept appearing in V2 does not mean its V1 semantics were identical. Cross-version interpretation belongs in [[V1 to V2 Concept Migration]].

## Known review context

V1 preserves model-extraction and semantic-review flags explicitly rather than modifying the frozen source to make every construct appear cleaner.

See [[V1 Conceptual Model]] and [[V1 Limitations and Boundaries]].
