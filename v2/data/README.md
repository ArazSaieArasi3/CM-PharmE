# CM-PharmE 2.0 — Ontology-Aligned Data Infrastructure

Status: **W6 implementation branch; Gate E candidate architecture.**

## Purpose
W6 realizes the Gate-D/W5 semantics across a PostgreSQL/PostGIS reference database and an RDF instance graph while preserving explicit provenance and source boundaries.

## Representation contract
The W5 ontology remains the semantic authority. The relational database is an implementation representation, not a replacement conceptual model. Material table/column mappings are registered in `mappings/ontology-rdb-mapping.csv`.

Protected distinctions preserved in the relational design include:
- Organization ≠ Facility;
- Geography ≠ Regulatory Jurisdiction;
- Medicinal Product ≠ Pharmaceutical Substance ≠ Product Presentation;
- Observation Result ≠ Source Record;
- identifier value/assignment ≠ entity identity;
- provenance/evidence records remain first-class.

## Directory
- `db/schema.sql` — PostgreSQL/PostGIS DDL.
- `db/views.sql` — stable research/query views.
- `mappings/ontology-rdb-mapping.csv` — ontology↔RDB traceability.
- `sources/source-manifest.json` — admitted W6 source contracts and execution status.
- `fixtures/` — deterministic schema-faithful CI fixtures; not empirical study results.
- `queries/` — paired SQL/SPARQL benchmark registry.
- `api/openapi.yaml` — bounded read-only access contract; not a production deployment.
- `tools/v2_data/` — bootstrap, ingestion, validation, KG export and equivalence tooling.

## Empirical boundary
CI uses small deterministic fixtures matching published source schemas. This verifies mapping/representation mechanics but **does not mean the full external datasets have been downloaded or empirically evaluated in W6 CI**. Full-scale data-quality, coverage and held-out generalizability belong to W7.

The primary NHIF outpatient source contract is based on DOI `10.5281/zenodo.19160825`; the NHIF inpatient secondary contract uses DOI `10.5281/zenodo.19160637`. Aggregate `patients_num` values are represented as aggregate observation measures and are never reinterpreted as unique patient identities.

## Held-out protection
H1 ClinicalTrials.gov/AACT, H2 openFDA Drug Shortages and H3 the reserved national EML sample are not used to redesign the W6 Core/RDB/KG mapping architecture.