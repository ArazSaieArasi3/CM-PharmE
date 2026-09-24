# V2 Data Infrastructure

> **Version scope:** V2  
> **Status:** Stable-to-date / Evolving  
> **Updated:** 2026-09-23

## Representation architecture

V2 realizes selected ontology semantics across:
- PostgreSQL/PostGIS;
- ontology↔RDB mapping registry;
- evidence/provenance tables;
- auditable entity-match structures;
- deterministic RDF ABox/KG generation;
- paired SQL↔SPARQL benchmarks;
- bounded OpenAPI/query layer.

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
- 4/4 SQL↔SPARQL equivalence.

## Semantic-source boundary

The relational schema and application layer must preserve ontology identity rather than becoming a competing semantic model.

Source schemas are mapped into the research representation; they do not define ontology classes merely because fields/tables exist.

## Provenance and entity resolution

The data layer records source/evidence lineage and entity-match assertions explicitly. Ambiguity should remain visible.

No real-world precision/recall/F1 claim is supported by the reference fixtures.

## Production boundary

W6 does **not** establish:
- full external-source ingestion;
- production API deployment;
- real-world entity-resolution accuracy;
- geocoding accuracy;
- global completeness;
- cross-jurisdiction generalizability.

## Evidence

- [Data README](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/data/README.md)
- [W6 closure](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w6/W6-CLOSURE.md)
- [Relational schema](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/data/db/schema.sql)
- [Ontology-RDB mappings](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/data/mappings/ontology-rdb-mapping.csv)
- [OpenAPI contract](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/data/api/openapi.yaml)

---

<details>
<summary>Documentation record</summary>

- **Page scope:** V2
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative source:** V2 W6 data/representation artifacts
- **Last synchronized:** 2026-09-23
- **Last synchronized ref:** `1226b0a5484f8f5d3a8d214e0d0f52f066b88999`
- **Related issues/PRs:** W6, E10, E13
- **Evidence status:** Reference realization complete; production/full-ingestion claims explicitly excluded
- **Future refresh:** #214 if final release architecture changes
- **Wiki baseline:** WB-2026.09.1

</details>
