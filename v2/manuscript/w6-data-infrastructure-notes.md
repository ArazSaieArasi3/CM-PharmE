# W6 Manuscript Notes — Ontology-Aligned Data Infrastructure

## Method text now supportable
The CM-PharmE 2.0 formal ontology is realized through an ontology-aligned PostgreSQL/PostGIS reference schema and a deterministic RDF ABox projection. A machine-readable traceability registry links material relational structures to W5 ontology IRIs. Dataset, release, source-record, assertion, evidence-support and transformation-run entities preserve provenance across representations.

The source adapter design distinguishes source contracts from ontology semantics. The primary/outpatient and secondary/inpatient NHIF DOI schemas are exercised in CI using deterministic schema-faithful synthetic fixtures. Aggregate `patients_num` fields are represented as aggregate measures and are not reconstructed as patient individuals.

## Representation result now supportable
For the registered W6 fixture baseline, the reference implementation creates 7 source records, 7 relational aggregate observations and a deterministic 398-triple RDF ABox. The canonical ABox fingerprint is `6f93a00c2fa9a853e44db80b547d69f8033719948a03cf09b2b175dff5b40825`.

The generated KG passes applicable SHACL validation, uses no unknown CM-PharmE terms, and preserves the registered provenance/representation invariants. Four registered paired SQL↔SPARQL benchmark queries return equivalent normalized result sets on the fixture baseline.

## Entity-resolution wording
W6 demonstrates an auditable entity-match representation and executes two exact deterministic cross-source presentation matches in the synthetic fixture. Do **not** report these as entity-resolution precision/recall or real-world matching accuracy. Any such metric requires a W7 evaluated real/gold subset.

## Geospatial wording
W6 implements PostGIS-ready geography storage, spatial indexing, source alias normalization and GeoNames identifier hooks. The current fixture does not establish production geocoding or GeoNames resolution accuracy.

## API wording
The OpenAPI artifact is a documented bounded read-access contract for research/future application implementation. It is not evidence of a deployed public API.

## Interpretation boundary
W6 establishes reproducible representation mechanics, ontology↔RDB traceability, provenance continuity, deterministic KG generation and bounded SQL↔SPARQL equivalence on schema-faithful fixtures. It does not establish full-dataset empirical validity, domain completeness, cross-jurisdiction generalizability, demonstrator effectiveness or held-out results.

Those claims remain W7/W8 responsibilities.