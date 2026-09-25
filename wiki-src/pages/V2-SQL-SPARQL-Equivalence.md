# V2 SQL SPARQL Equivalence

> **Version scope:** V2  
> **Status:** Frozen benchmark evidence / Stable-to-date  
> **Updated:** 2026-09-25

CM-PharmE uses a frozen set of paired SQL and SPARQL questions to test whether selected answers are preserved across the relational and RDF representations.

![DGM-ARC-007 SQL SPARQL benchmark path](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/architecture/DGM-ARC-007--sql-sparql-benchmark-path.svg?sha=b6e63e7c645e)

## Benchmark registry

`v2/data/queries/sql-sparql-benchmarks.json` defines four pairs:

| ID | Question |
|---|---|
| QREP-01 | Product-presentation identity/code mapping |
| QREP-02 | Regional/time/product aggregate patient-count observation |
| QREP-03 | Dataset DOI → SourceRecord provenance traversal |
| QREP-04 | Facility → physical geography traversal |

The comparison runner executes both representations, canonicalizes the returned rows and compares the result sets.

## Current evidence

W6 and E10 report **4/4 PASS**.

This establishes answer agreement only for the four registered questions against the same deterministic reference realization and generated KG.

## What 4/4 does not mean

It does **not** establish:
- equivalence for arbitrary SQL and SPARQL queries;
- universal lossless bidirectional mapping;
- identical relational row counts and RDF node counts;
- complete realization of every ontology term;
- production query performance equivalence.

The one-to-many observation projection is an intentional example where semantic agreement is governed by the documented rule rather than raw count equality.

## Reproduction

Authoritative artifacts:
- [benchmark registry](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/data/queries/sql-sparql-benchmarks.json)
- [comparison tool](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/tools/v2_data/compare_sql_sparql.py)
- [E10 evidence](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w7/e10-ontology-rdb-kg-semantic-consistency.md)
---
<details>
<summary>Documentation record</summary>

- **Page scope:** V2
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative source:** V2 W6 data/representation artifacts and W7 E10 evidence
- **Last synchronized:** 2026-09-25
- **Last synchronized ref:** `v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999`
- **Related issues/PRs:** #228, #236, #237
- **Evidence status:** Reference implementation evidence; production/full-ingestion claims excluded
- **Future refresh:** #212 / #213 / #214 as applicable
- **Wiki baseline:** WB-2026.09.1

</details>
