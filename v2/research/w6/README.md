# W6 — Ontology-Aligned Data Infrastructure

## Status
**Implementation complete — Gate E candidate.**

W6 realizes the approved W5 formal ontology across a PostgreSQL/PostGIS reference relational model and an RDF ABox/knowledge-graph representation while keeping evidence, provenance, identifier, geography and entity-resolution semantics explicit.

## Implemented scope
- PostgreSQL/PostGIS reference schema and research views;
- machine-readable ontology↔RDB traceability registry;
- schema-faithful primary/secondary NHIF ingestion contracts and deterministic CI fixtures;
- source-record SHA-256 fingerprints and transformation-run provenance;
- geographic normalization/alias architecture with GeoNames identifier hooks;
- evidence-backed entity-match assertions with confidence/status;
- deterministic RDB→RDF ABox/KG export using W5 ontology IRIs;
- SHACL and ontology-term regression validation;
- paired SQL↔SPARQL representation-equivalence benchmark suite;
- bounded OpenAPI 3.1 read contract for future research access;
- dedicated GitHub Actions W6 representation gates.

## Representation baseline from successful CI
A successful W6 run on the implementation branch established the following schema-faithful fixture baseline:
- 7 source records;
- 7 relational aggregate observation rows;
- 2 medicinal products;
- 2 product presentations;
- 2 pharmaceutical substances;
- 2 facilities;
- 2 normalized administrative geographies;
- 2 accepted exact cross-source presentation-match assertions;
- 398 RDF ABox triples;
- canonical KG SHA-256 `6f93a00c2fa9a853e44db80b547d69f8033719948a03cf09b2b175dff5b40825`;
- SHACL conformance PASS;
- ontology-term and provenance regression PASS;
- 4/4 registered SQL↔SPARQL benchmark queries PASS.

## Critical interpretation boundary
The W6 CI corpus is **schema-faithful synthetic fixture data**, not the full external NHIF datasets. Consequently W6 PASS establishes representation mechanics, semantic traceability and reproducibility on the registered fixtures. It does not establish full-dataset completeness, source-data quality, entity-resolution accuracy on real populations, application effectiveness or external/generalizability results.

The two DOI records are used as source/schema contracts:
- outpatient: `10.5281/zenodo.19160825`;
- inpatient: `10.5281/zenodo.19160637`.

`patients_num` remains an aggregate measure. No Patient individuals are reconstructed or inferred from aggregate counts.

## Held-out protection
H1 ClinicalTrials.gov/AACT, H2 openFDA Drug Shortages and H3 the reserved national EML sample remain excluded from W6 redesign and implementation fixtures. They remain reserved for W7 evaluation.

## Gate E
Gate E evaluates the representation architecture, not empirical generalizability. Approval freezes the W6 Ontology↔RDB↔KG architecture for W7 evaluation.