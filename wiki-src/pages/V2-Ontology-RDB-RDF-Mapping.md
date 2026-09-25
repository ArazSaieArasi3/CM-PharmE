# V2 Ontology RDB RDF Mapping

> **Version scope:** V2  
> **Status:** Reference implementation / Stable-to-date  
> **Updated:** 2026-09-25

The mapping registry is the explicit contract between selected ontology semantics and their relational realization. It prevents table/column structure from silently redefining ontology meaning.

![DGM-ARC-006 Ontology RDB RDF semantic mapping](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/architecture/DGM-ARC-006--ontology-rdb-rdf-semantic-mapping.svg?sha=c6f2a63ee67d)

## Mapping registry purpose

`v2/data/mappings/ontology-rdb-mapping.csv` contains **36 registered mappings**. Each row records:
- ontology IRI;
- entity kind;
- relational table;
- field or join;
- mapping status;
- representation note.

E10 verified that all 36 registered IRIs resolve and that all registered relational tables exist.

## Direct and non-direct realization

The registry deliberately does not claim every mapping is lossless or direct. E10 reports:
- direct: **26**;
- bounded: **4**;
- polymorphic: **2**;
- relational projection: **1**;
- one-to-many RDF projection: **1**;
- deferred: **2**.

The ten non-direct mappings are explicit boundaries, not hidden failures.

A central example is `M027`: one relational reimbursement-utilisation aggregate row may project to multiple metric-level RDF ObservationResult nodes. Therefore relational row count and RDF node count are not expected to be equal.

## Protected distinctions

The realization preserves distinctions including:
- Organization ≠ Facility;
- Geography ≠ Regulatory Jurisdiction;
- Medicinal Product ≠ Pharmaceutical Substance ≠ Product Presentation;
- Observation Result ≠ Source Record;
- identifier assignment/value ≠ entity identity;
- evidence/provenance records remain first-class.

## Semantic authority

The ontology/SHACL artifacts own the meaning of classes and properties. Mapping rows and database pages explain implementation realization only.

See [[V2 Ontology Reference]], [[V2 Database Reference]] and [[V2 KG Generation and Query]].
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
