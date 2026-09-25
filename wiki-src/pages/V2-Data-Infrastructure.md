# V2 Data Infrastructure

> **Version scope:** V2  
> **Status:** Stable-to-date / Evolving  
> **Updated:** 2026-09-25

CM-PharmE 2.0 includes a bounded ontology-aligned reference data realization. The ontology remains the semantic authority; the database, mappings, RDF/KG and query surfaces are implementation representations.

## Start here

- [[V2 Data and KG Architecture]] — end-to-end source→RDB→KG architecture.
- [[V2 End-to-End Data Trace]] — one reproducible fixture record traced through provenance, mappings and RDF.
- [[V2 Provenance and Evidence Flow]] — Dataset/Release/SourceRecord, Assertion/EvidenceSupport and entity-match boundaries.
- [[V2 Ontology RDB RDF Mapping]] — the 36-entry mapping registry and direct/non-direct realization.
- [[V2 KG Generation and Query]] — deterministic RDF ABox/KG projection.
- [[V2 SQL SPARQL Equivalence]] — the bounded 4/4 paired-query benchmark.
- [[V2 API and Query Boundary]] — read-only OpenAPI research contract.

## Database documentation

- [[V2 Database Reference]] — complete 24-table reference.
- [[V2 Database ERD Suite]] — logical, physical and subject-area ERDs.
- [[V2 Database Data Dictionary]] — field-level physical dictionary.
- [[V2 Database Views]] — research/query views.

## Representation architecture

V2 realizes selected ontology semantics across:
- PostgreSQL/PostGIS;
- ontology↔RDB mapping registry;
- evidence/provenance tables;
- auditable entity-match assertions;
- deterministic RDF ABox/KG generation;
- paired SQL↔SPARQL benchmarks;
- bounded OpenAPI/query contract.

## Fixture baseline

The W6 closure records:
- 2 DOI dataset contracts/releases executed through fixture adapters;
- 7 source records;
- 7 aggregate relational observations;
- 2 medicinal products and 2 presentations;
- 2 pharmaceutical substances;
- 2 facilities and 2 normalized geographic entities;
- 7 assertions + 7 evidence-support records;
- 2 accepted exact cross-source presentation-match assertions;
- 398 deterministic RDF ABox triples;
- SHACL conformance PASS;
- 36 ontology↔RDB mapping IRIs resolve;
- 4/4 SQL↔SPARQL equivalence for the frozen benchmark suite.

## Semantic-source boundary

Source schemas do not define ontology classes merely because their fields/tables exist. IdentifierAssignment does not become entity identity, and EntityMatchAssertion is an auditable matching claim rather than proof of identity.

The relational schema and application/query layers must preserve ontology distinctions rather than becoming competing semantic models.

## Production boundary

W6 does **not** establish:
- full external-source ingestion;
- production API/KG deployment;
- real-world entity-resolution accuracy;
- geocoding accuracy;
- arbitrary SQL↔SPARQL equivalence;
- global completeness;
- cross-jurisdiction generalizability.

## Evidence

- [Data README](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/data/README.md)
- [W6 closure](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w6/W6-CLOSURE.md)
- [E10 representation consistency](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w7/e10-ontology-rdb-kg-semantic-consistency.md)
- [Relational schema](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/data/db/schema.sql)
- [Ontology-RDB mappings](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/data/mappings/ontology-rdb-mapping.csv)
- [SQL-SPARQL benchmark registry](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/data/queries/sql-sparql-benchmarks.json)
- [OpenAPI contract](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/data/api/openapi.yaml)

---

<details>
<summary>Documentation record</summary>

- **Page scope:** V2
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative source:** V2 W6 data/representation artifacts and W7 E10 evidence
- **Last synchronized:** 2026-09-25
- **Last synchronized ref:** `v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999`
- **Related issues/PRs:** #236, #237
- **Evidence status:** End-to-end reference realization documented; production/full-ingestion claims explicitly excluded
- **Future refresh:** #212 / #213 / #214 as applicable
- **Wiki baseline:** WB-2026.09.1

</details>
