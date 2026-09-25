# Knowledge Graph and Queries Guide

> **Version scope:** V2  
> **Status:** Stable-to-date / Evolving  
> **Updated:** 2026-09-25

Use this section to understand how CM-PharmE semantics are carried across **OWL/SHACL, relational storage, RDF/KG generation, SQL/SPARQL evaluation and the bounded query/API surface**.

## Semantic foundation
- [[V2 Formal Ontology and SHACL]]
- [[V2 Ontology Reference]]
- [[V2 Data Infrastructure]]
- [[V2 Ontology RDB RDF Mapping]]

## End-to-end architecture and trace
- [[V2 Data and KG Architecture]]
- [[V2 Provenance and Evidence Flow]]
- [[V2 KG Generation and Query]]
- [[V2 End-to-End Data Trace]]

## Query and access evidence
- [[V2 SQL SPARQL Equivalence]]
- [[V2 API and Query Boundary]]
- [[V2 Evaluation E1-E13|CM-PharmE 2.0 Evaluation Framework]]
- [[Reproducibility Guide]]

## Implementation artifacts
- [[Repository Artifact Index]]

## Application/query context
- [[V2 Observatory and Demonstrators]]

The current Wiki now documents the end-to-end source→RDB→KG path and a reproducible fixture trace under #237. Step-by-step task tutorials remain a separate #239 deliverable.

### Suggested path for a KG/query user
**V2 Formal Ontology and SHACL → V2 Ontology RDB RDF Mapping → V2 KG Generation and Query → V2 SQL SPARQL Equivalence → V2 End-to-End Data Trace**

---

<details>
<summary>Documentation record</summary>

- **Page scope:** V2
- **Documentation maturity:** Stable-to-date / Evolving
- **Last synchronized:** 2026-09-25
- **Related issues/PRs:** #228, #230, #237
- **Wiki baseline:** WB-2026.09.1
- **Authoritative source:** v2/research-program
- **Last synchronized ref:** `v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999`
- **Evidence status:** End-to-end architecture documented; tutorial layer remains #239
- **Future refresh:** See #211–#214 as applicable

</details>
