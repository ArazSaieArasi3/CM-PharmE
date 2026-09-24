# Relation Index

> **Version scope:** Cross-version  
> **Status:** Stable-to-date / Evolving  
> **Updated:** 2026-09-23

## V1 canonical relations

| ID | Label | Category | Source | Target |
|---|---|---|---|---|
| CMPE-R0001 | governs | material | CMPE-C0001 | CMPE-C0003 |
| CMPE-R0002 | is mediated by | mediation | CMPE-C0003 | CMPE-C0025 |
| CMPE-R0003 | is part of | componentOf | CMPE-C0002 | CMPE-C0001 |
| CMPE-R0004 | characterizes | characterization | CMPE-C0005 | CMPE-C0001 |
| CMPE-R0005 | characterizes | characterization | CMPE-C0006 | CMPE-C0002 |
| CMPE-R0006 | specializes | generalization | CMPE-C0007 | CMPE-C0003 |
| CMPE-R0007 | is mediated by | mediation | CMPE-C0008 | CMPE-C0009 |
| CMPE-R0008 | fulfills | material | CMPE-C0039 | CMPE-C0010 |
| CMPE-R0009 | characterizes | characterization | CMPE-C0008 | CMPE-C0011 |
| CMPE-R0010 | is part of | componentOf | CMPE-C0012 | CMPE-C0013 |
| CMPE-R0011 | mediates | mediation | CMPE-C0008 | CMPE-C0014 |
| CMPE-R0012 | participates in | association | CMPE-C0015 | CMPE-C0003 |
| CMPE-R0013 | is part of | componentOf | CMPE-C0016 | CMPE-C0015 |
| CMPE-R0014 | is mediated by | mediation | CMPE-C0017 | CMPE-C0018 |
| CMPE-R0015 | is mediated by | mediation | CMPE-C0019 | CMPE-C0018 |
| CMPE-R0016 | assigns | material | CMPE-C0020 | CMPE-C0021 |
| CMPE-R0017 | participates in | association | CMPE-C0022 | CMPE-C0021 |
| CMPE-R0018 | material relation | material | CMPE-C0023 | CMPE-C0024 |
| CMPE-R0019 | is mediated by | mediation | CMPE-C0024 | CMPE-C0004 |
| CMPE-R0020 | characterizes | characterization | CMPE-C0026 | CMPE-C0004 |
| CMPE-R0021 | characterizes | characterization | CMPE-C0027 | CMPE-C0026 |
| CMPE-R0022 | mitigates | material | CMPE-C0028 | CMPE-C0027 |
| CMPE-R0023 | enables | material | CMPE-C0029 | CMPE-C0015 |
| CMPE-R0024 | mediates | mediation | CMPE-C0032 | CMPE-C0031 |
| CMPE-R0025 | records | material | CMPE-C0033 | CMPE-C0034 |
| CMPE-R0026 | enables | material | CMPE-C0035 | CMPE-C0018 |
| CMPE-R0027 | is mediated by | mediation | CMPE-C0008 | CMPE-C0014 |
| CMPE-R0028 | governs | material | CMPE-C0032 | CMPE-C0001 |
| CMPE-R0029 | is part of | componentOf | CMPE-C0018 | CMPE-C0015 |
| CMPE-R0030 | characterizes | characterization | CMPE-C0034 | CMPE-C0018 |
| CMPE-R0031 | constraints | material | CMPE-C0036 | CMPE-C0037 |
| CMPE-R0032 | informs | material | CMPE-C0038 | CMPE-C0036 |
| CMPE-R0033 | informs | material | CMPE-C0038 | CMPE-C0001 |
| CMPE-R0034 | informs | material | CMPE-C0038 | CMPE-C0028 |
| CMPE-R0035 | follows | material | CMPE-C0037 | CMPE-C0022 |
| CMPE-R0036 | governs | material | CMPE-C0009 | CMPE-C0013 |
| CMPE-R0037 | records | material | CMPE-C0033 | CMPE-C0017 |
| CMPE-R0038 | assists | material | CMPE-C0030 | CMPE-C0016 |
| CMPE-R0039 | material relation | material | CMPE-C0009 | CMPE-C0039 |
| CMPE-R0040 | engages in | material | CMPE-C0001 | CMPE-C0014 |

## V2 current relation-pattern catalog

The current V2 conceptual specification uses explicit relation/truth-maker patterns rather than carrying V1 properties forward mechanically.

| Pattern | Ontological treatment | Core interpretation |
|---|---|---|
| operates | Material derived from Facility Operation | Organization ↔ Facility |
| registered with | Material derived from Establishment Registration | regulated entity ↔ authority |
| authorized for | Material derived from Regulatory Authorization | regulated party ↔ role/activity |
| authorization applies in | formal/context relation | authorization → jurisdiction |
| presentation of product | formal relation | presentation → medicinal product |
| has active substance | formal/specification relation | product/presentation → substance |
| characterized by strength | Characterization | presentation ↔ Strength |
| classified as | Material derived from Product Classification Assignment | product/substance ↔ entry |
| listed/marketed in context | Material derived from Market Listing | presentation ↔ context |
| participates in activity | participation | entity ↔ event |
| shortage involves | situation involvement | shortage ↔ product/jurisdiction |
| supply capacity characterizes | Characterization | organization/facility ↔ Supply Capacity |
| observation result about | aboutness/formal | result → domain entity/context |
| observation produces result | event→information | activity → result |
| Evidence Support | Relator | evidence item ↔ assertion/decision |
| Identifier Assignment | Relator | entity ↔ identifier value/scheme |
| Supply Dependency | Relator | dependent ↔ provider/source |
| Strategic Partnership Agreement | Relator / BA extension | organization ↔ organization |

## Current limitation

A complete human-reviewed one-row-per-V1-relation → V2-relation disposition is not yet final. The W3 relation-family policy and W4 pattern specification are authoritative for the present baseline; #173/#213 will complete/refine relation-level review.

## Evidence

- [V1 relation catalog](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/catalog/relations.yaml)
- [V2 W3 migration matrix](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w3/v1-v2-migration-matrix.md)
- [V2 relation patterns](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w4/relator-material-patterns.md)
- [V2 integrated model](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w4/integrated-ontouml-model.md)

---

<details>
<summary>Documentation record</summary>

- **Page scope:** Cross-version
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative inventories:** V1 relation catalog; V2 W4 relation-pattern specification
- **Last synchronized:** 2026-09-23
- **Related issues:** #159, #173, #208
- **Evidence status:** V1 40-relation registry complete; V2 relation-pattern baseline stable while final human-review relation catalog is pending
- **Future refresh:** #213
- **Wiki baseline:** WB-2026.09.1
- **Authoritative source:** V1: main; V2: v2/research-program
- **Last synchronized ref:** V1: main; V2: v2/research-program

</details>
