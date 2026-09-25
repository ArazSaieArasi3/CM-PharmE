# V2 End-to-End Data Trace

> **Version scope:** V2  
> **Status:** Reproducible reference trace  
> **Updated:** 2026-09-25

This page traces one actual deterministic W6 fixture row from source data through relational provenance, assertion/evidence representation and RDF/KG projection. The example is intentionally fixture-based and is not presented as an empirical clinical or market observation.

## 1. Admitted source row

Source contract: **P1-NHIF-OUTPATIENT**  
DOI: **10.5281/zenodo.19160825**  
Fixture: `v2/data/fixtures/nhif_outpatient_fixture.csv`  
Fixture row: **1**

Selected values:
- region: `22 / sofia city`;
- NHIF code: `NHIF-TEST-001`;
- product: `TEST PRODUCT ALPHA`;
- package: `tablet blister`;
- concentration: `10 mg`;
- patient count: `12`;
- package count: `16`;
- BGN cost: `320.00`;
- EUR cost: `163.6130`;
- period: `2025-01-01`;
- part: `01`.

## 2. Deterministic SourceRecord fingerprint

`bootstrap_ingest.py` canonicalizes the CSV row with sorted JSON keys and compact separators, then computes SHA-256.

For this fixture row:

`source_hash = fc4f28d217129c90048aa48ae817d46ec9700198bd225de85897488d523817f4`

The row is stored in `cmpe.source_record` with its DatasetRelease, row number, transformation-run reference and `raw_key`.

## 3. Transformation provenance

The W6 loader records adapter:
- `w6-nhif-fixture-loader`;
- version `1.0.0`.

For the checked fixture pair, the deterministic run public ID is:

`run:w6-fixture:3cef83edd2c025392ef3`

This run is represented semantically as `cmpe:ProvenanceActivity`.

## 4. Normalized domain representation

For this row the deterministic public identifiers include:

- substance: `substance:source-label:5b7c9e04321068d35ae0`;
- product: `product:source-normalized:c8a9859abe6ffd900982`;
- presentation: `presentation:nhif:b1730e50e764943e8891`.

The `NHIF-TEST-001` lexical code is represented through IdentifierAssignment rather than being promoted to universal entity identity.

## 5. Assertion and evidence

The ingest creates:

`assertion:observation:fc4f28d217129c90048aa48ae817d46ec9700198bd225de85897488d523817f4`

and

`evidence-support:fc4f28d217129c90048aa48ae817d46ec9700198bd225de85897488d523817f4`

EvidenceSupport links this SourceRecord to the Assertion. The same row creates the relational aggregate ObservationResult:

`observation:fc4f28d217129c90048aa48ae817d46ec9700198bd225de85897488d523817f4`

## 6. Ontology↔RDB mapping

Relevant registered mappings include:
- M003 SourceRecord → `source_record`;
- M014 MedicinalProductPresentation → `product_presentation`;
- M021 IdentifierAssignment → `identifier_assignment`;
- M024 Assertion → `assertion`;
- M025 EvidenceSupport → `evidence_support`;
- M027 ReimbursementUtilisationObservationResult → one-to-many RDF projection.

## 7. RDF/KG projection

The SourceRecord instance IRI is deterministically generated as:

`https://w3id.org/cm-pharme/2.0/instance/source-record/fc4f28d217129c90048aa48ae817d46ec9700198bd225de85897488d523817f4`

The aggregate observation is projected into four metric-level RDF ObservationResult nodes because all four reference measures are non-null: patients, packages, cost-BGN and cost-EUR.

Each metric node is linked back to this SourceRecord through `prov:wasDerivedFrom`. The SourceRecord is linked to the DatasetRelease and, where present, its ProvenanceActivity.

## 8. Query paths

This trace participates in the same representation used by:
- QREP-01 presentation identity/code mapping;
- QREP-02 aggregate patient-count query;
- QREP-03 DOI → SourceRecord provenance traversal.

The API contract can address the lineage by:

`GET /v1/provenance/records/fc4f28d217129c90048aa48ae817d46ec9700198bd225de85897488d523817f4`

## Reproduction basis

The values above are derived from the committed fixture plus the deterministic algorithms in:
- [bootstrap_ingest.py](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/tools/v2_data/bootstrap_ingest.py)
- [export_kg.py](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/tools/v2_data/export_kg.py)
- [mapping registry](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/data/mappings/ontology-rdb-mapping.csv)
- [benchmark registry](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/data/queries/sql-sparql-benchmarks.json)

See also [[V2 Provenance and Evidence Flow]], [[V2 KG Generation and Query]] and [[V2 SQL SPARQL Equivalence]].
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
