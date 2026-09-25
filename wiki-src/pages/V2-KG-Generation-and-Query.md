# V2 KG Generation and Query

> **Version scope:** V2  
> **Status:** Reference implementation / Stable-to-date  
> **Updated:** 2026-09-25

The W6 knowledge graph is a deterministic RDF ABox generated from the reference PostgreSQL/PostGIS realization. It is not a second semantic authority.

## Deterministic generation

`tools/v2_data/export_kg.py` reads the reference database and creates instance IRIs under:

`https://w3id.org/cm-pharme/2.0/instance/`

Examples include deterministic nodes for Dataset, DatasetRelease, SourceRecord, ProvenanceActivity, Facility, Product, Presentation, IdentifierAssignment, ObservationResult, Assertion, EvidenceSupport and EntityMatchAssertion.

The frozen W6 baseline contains:
- **398 RDF triples**;
- canonical N-Triples SHA-256 `6f93a00c2fa9a853e44db80b547d69f8033719948a03cf09b2b175dff5b40825`;
- SHACL conformance PASS;
- zero unknown CM-PharmE terms in the KG.

## Source lineage in RDF

A SourceRecord instance:
- is typed `cmpe:SourceRecord`;
- is linked from its DatasetRelease through `cmpe:containsSourceRecord`;
- carries the source hash through `dct:identifier`;
- links to the generating ProvenanceActivity through `prov:wasGeneratedBy` when applicable.

Generated ObservationResult metric nodes use `prov:wasDerivedFrom` to point back to the SourceRecord.

## Aggregate-to-metric projection

Each reimbursement-utilisation aggregate row can contain up to four measures:
- patient count;
- package count;
- BGN cost;
- EUR cost.

The RDF export creates a separate metric-level ObservationResult node for each non-null measure. In E10, 7 aggregate relational rows produced 28 expected and 28 observed metric nodes; all 7/7 per-row projection checks passed.

## Query layer

SPARQL benchmarks query the generated KG and are paired with SQL queries over the reference RDB. See [[V2 SQL SPARQL Equivalence]].

For a concrete source-to-KG walkthrough see [[V2 End-to-End Data Trace]].

## Boundary

The deterministic KG verifies the registered reference projection. It is not evidence of full external-source ingestion, universal ontology population, arbitrary bidirectional RDB↔RDF reconstruction or production KG operation.
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
