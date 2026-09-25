# V2 Data and Knowledge-Graph Architecture

> **Version scope:** V2  
> **Status:** Reference implementation / Stable-to-date  
> **Updated:** 2026-09-25

This page connects the data path that is otherwise distributed across source contracts, PostgreSQL/PostGIS, ontology mappings, RDF generation, query benchmarks and the bounded API contract.

## End-to-end representation path

![DGM-ARC-004 Source transformation RDB KG pipeline](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/architecture/DGM-ARC-004--source-transformation-rdb-kg-pipeline.svg?sha=6c2ef51be63a)

**DGM-ARC-004** shows the governed path:

**Source contract / fixture → Dataset + DatasetRelease → TransformationRun → SourceRecord → normalized relational entities → ontology↔RDB mapping registry → deterministic RDF/KG → SQL/SPARQL query paths.**

The ontology remains the semantic authority. The database and KG are implementation representations of selected semantics, not competing conceptual models.

## Current reference baseline

The W6 reference realization records:
- 2 executed DOI-backed source contracts through deterministic schema-faithful fixtures;
- 7 SourceRecords;
- 7 relational aggregate observations;
- 7 Assertions and 7 EvidenceSupport records;
- 2 accepted exact cross-source presentation-match assertions;
- 398 deterministic RDF ABox triples;
- 36 registered ontology↔RDB mappings;
- 4/4 frozen SQL↔SPARQL benchmark pairs passing.

## Read the architecture by concern

- [[V2 Provenance and Evidence Flow]] — dataset/release/source/transformation, assertion support and entity-match boundaries.
- [[V2 Ontology RDB RDF Mapping]] — mapping-registry semantics and direct/non-direct realization.
- [[V2 KG Generation and Query]] — deterministic instance-graph projection.
- [[V2 SQL SPARQL Equivalence]] — bounded paired-query evidence.
- [[V2 API and Query Boundary]] — read-only OpenAPI contract.
- [[V2 End-to-End Data Trace]] — one reproducible fixture record traced through the chain.
- [[V2 Database Reference]] and [[V2 Database ERD Suite]] — physical relational reference.
- [[V2 Ontology Reference]] — semantic definitions.

## Authority boundaries

1. **OWL/SHACL** owns semantic meaning.
2. **schema.sql** owns the implemented relational structure.
3. **ontology-rdb-mapping.csv** records explicit realization mappings.
4. **export_kg.py** defines deterministic W6 instance-graph projection.
5. **sql-sparql-benchmarks.json** defines the frozen paired-query questions.
6. **openapi.yaml** defines a bounded read-only interface contract, not service availability.

## Production boundary

This architecture does not establish full external-source ingestion, production deployment, real-world entity-resolution accuracy, geocoding accuracy, arbitrary SQL↔SPARQL equivalence, or global/cross-jurisdiction completeness.

## Authoritative artifacts

- [W6 closure](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w6/W6-CLOSURE.md)
- [E10 representation consistency](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w7/e10-ontology-rdb-kg-semantic-consistency.md)
- [Data README](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/data/README.md)
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
