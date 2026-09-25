# V2 API and Query Boundary

> **Version scope:** V2  
> **Status:** Interface contract / Stable-to-date  
> **Updated:** 2026-09-25

The V2 OpenAPI artifact is a **bounded read-only research contract** over the reference database/KG. It documents an intended interface; it is not proof that a production service is deployed or available.

![DGM-ARC-008 API query boundary](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/architecture/DGM-ARC-008--api-query-boundary.svg?sha=6cb63d393069)

## Contracted endpoints

The OpenAPI 3.1 contract currently defines:
- `GET /v1/meta` — ontology/data-wave metadata;
- `GET /v1/presentations` — normalized product-presentation query;
- `GET /v1/observations` — aggregate observation query;
- `GET /v1/geographies` — normalized geography query;
- `GET /v1/provenance/records/{source_hash}` — source-record lineage.

The server entry is explicitly a localhost reference target.

## Provenance endpoint

The provenance response can expose:
- source hash;
- dataset ID;
- dataset-release ID;
- DOI;
- transformation-run ID;
- linked assertions.

This makes the primary source-to-assertion trace available at the contract boundary without conflating the API with semantic authority.

## Query boundary

SQL views, SPARQL benchmarks and the OpenAPI contract are consumer/query surfaces over the reference realization. Semantic definitions remain in the ontology; relational structure remains in schema.sql.

## Non-claims

The contract does not establish:
- hosted endpoint availability;
- authentication/authorization completeness;
- production SLA/scalability;
- full-source ingestion;
- operational privacy/security certification;
- arbitrary semantic-query completeness.

Authoritative artifact: [openapi.yaml](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/data/api/openapi.yaml).
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
