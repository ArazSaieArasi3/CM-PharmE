# V1 Relations

> **Version scope:** V1  
> **Status:** Stable  
> **Updated:** 2026-09-23

## Inventory

V1 has **40 canonical semantic relations**.

| Relation category | Count |
|---|---:|
| material | 19 |
| mediation | 8 |
| characterization | 6 |
| componentOf | 4 |
| association | 2 |
| generalization | 1 |

## Relation-design discipline

Relation semantics follow the ontological status of connected concepts:
- Mediation links a Relator to participating roles/entity types.
- Characterization links a Mode to its bearer.
- Part-whole semantics are used only where composition/membership is intended.
- Domain-specific associations are retained when evidence supports a dependency but not a stronger foundational commitment.

Cardinalities are conceptual participation constraints, not empirical frequency estimates.

## Authoritative navigation

- [Relation documentation index](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/relations/index.md)
- [Canonical relation catalog](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/catalog/relations.yaml)
- [Concept-relation mapping](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/mappings/concept-relation.csv)

## Known V1 relation issues

The V1 record intentionally retains provenance for duplicated/ambiguous source occurrences and wording rather than silently normalizing away uncertainty.

Examples include mediation-direction ambiguity around Strategic Partnership Agreement and duplicated governance-relator mediation.

## Cross-version note

V2 may refine directionality, mediation patterns, modular placement or relation semantics. Those changes belong in [[V1 to V2 Relation Migration]] rather than being retroactively applied to V1.

---

<details>
<summary>Documentation record</summary>

- **Page scope:** V1
- **Documentation maturity:** Stable
- **Authoritative source:** `main/catalog/relations.yaml`, relation docs and mappings
- **Last synchronized:** 2026-09-23
- **Last synchronized ref:** `5099888668d35f798e4759e3534e707ed906db24`
- **Related issues/PRs:** V1 model normalization/formalization
- **Evidence status:** 40 canonical semantic relations
- **Future refresh:** Frozen V1; V2 changes documented separately
- **Wiki baseline:** WB-2026.09.1

</details>
