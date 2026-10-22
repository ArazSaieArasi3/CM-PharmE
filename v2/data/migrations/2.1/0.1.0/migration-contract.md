# Conditional migration and representation contract for CM-PharmE 2.1

This is a **read-only design contract**, not executable DDL or permission to promote the research candidate. The source of record remains W6's 2.0 schema and fixtures. Implement one accepted semantic slice at a time after the corresponding ontology disposition in #306 and #311–#314; verify #307 source/hosted integration separately.

## Invariants and decision order

1. Preserve all W6 primary keys, public IDs, immutable source hashes, release/DOI links, transformation-run IDs, assertion/evidence links and the 2.0 ontology IRIs. Version the 2.1 RDF projection explicitly; never update all `ontology_iri` defaults or reinterpret old rows by string replacement alone.
2. For a candidate addition, record a truthmaker and a named source witness before any non-null backfill. A role, relational commitment or `SupplyCapacity` Mode cannot be inferred from an organization name or a measurement row. Missing information remains unknown in OWL; only a declared admission profile may reject a row.
3. Review the `FacilityOperation` operator cardinality first: W6 has one non-null `organization_id`; candidate SHACL has `operationOrganization` **min 1 without max**, `operationFacility` exactly one, and role-typed endpoints. If the author accepts multiple operators per relator, propose an additive participant table and keep the W6 column/view through migration. If the author instead accepts max 1, record that ontology decision and validate the existing column as the bounded representation. Do not silently insert the missing max into the ontology or silently limit the database's new 2.1 contract.
4. P4a `SupplyCapacity` is a Mode with one eligible Organization **or** Facility bearer, not an `observation_result` row. A proposed additive capacity table needs a distinct public ID, exactly-one typed bearer, a source/evidence route when asserted, and an optional result link only if scientifically supported. Preserve the old aggregate observations.
5. The 36 W6 registry entries are declarations, not proof that all tables reach RDF. In particular, `tools/v2_data/export_kg.py` has no `facility_operation` SELECT/export branch. A facility operation SQL↔SPARQL test must first implement or select an explicit exporter route; a SQL-only positive is insufficient.

## Acceptance protocol for each approved slice

| Gate | Positive witness | Rejected / boundary witness | Evidence |
|---|---|---|---|
| DDL and integrity | Stable IDs, valid foreign keys, allowed temporal window; if multi-operator approved, two distinct operator rows for one operation | Orphan FKs, duplicate public ID, `valid_to < valid_from`, zero operator or two facilities under the candidate admission profile; no false global negation for missing OWL assertions | Migration SQL, PostgreSQL version, transaction and constraint results; positive and failed inserts |
| Identity and provenance | One Organization, two distinct Facilities, two operation IDs, source record→release→dataset and assertion→evidence chain | Same name or place must not merge Organization with Facility or imply operation; an unsupported operation assertion must not acquire fabricated source provenance | Preserved public IDs/source hashes and row-level lineage before/after |
| SQL↔SPARQL | Normalized `(operation_public_id, organization_public_id, facility_public_id)` multisets equal across the relational query and the **2.1** RDF graph | Co-location only yields zero operation tuples; incomplete operation is rejected by declared admission or omitted from a query, not called false in OWL | Exact SQL and SPARQL texts, row counts, sorted normalized answers and graph checksum |
| RDF round trip | RDB→RDF→RDB preserves each operation ID, parties, valid interval and declared evidence link; typed role assertions correspond to mediation | Reusing the same IRI as Organization and Facility or casting an observation as `SupplyCapacity` Mode fails the scoped validation | Diff of normalized rows, SHACL report, reasoner result if applicable |
| Version/rollback | Old 2.0 queries and data still work during side-by-side projection; new 2.1 terms resolve to pinned candidate snapshot | No destructive rewrite/drop, no reinterpretation of source records | Dry-run migration and rollback on copied fixture database; old/new query checks |

Example *conditional* comparison for an accepted single-operator semantics (the SQL is valid against existing W6 schema; the 2.1 RDF side first needs an exporter):

```sql
SELECT fo.public_id AS operation_id, o.public_id AS organization_id,
       f.public_id AS facility_id
FROM cmpe.facility_operation fo
JOIN cmpe.organization o ON o.organization_id = fo.organization_id
JOIN cmpe.facility f ON f.facility_id = fo.facility_id
ORDER BY operation_id, organization_id, facility_id;
```

```sparql
PREFIX cmpe: <https://w3id.org/cm-pharme/2.1/>
SELECT ?operation_id ?organization_id ?facility_id WHERE {
  ?op a cmpe:FacilityOperation ; cmpe:operationOrganization ?org ; cmpe:operationFacility ?site .
  ?org a cmpe:OperatingOrganizationRole .
  ?site a cmpe:OperatedFacilityRole .
  ?op <http://purl.org/dc/terms/identifier> ?operation_id .
  ?org <http://purl.org/dc/terms/identifier> ?organization_id .
  ?site <http://purl.org/dc/terms/identifier> ?facility_id .
} ORDER BY ?operation_id ?organization_id ?facility_id
```

The `dcterms:identifier` projection above is a **proposed 2.1 export contract**, not an assertion that W6 exports those triples. Pin the source of every ID and the exact RDF serialization before running equivalence. If multi-operator semantics is accepted, adapt SQL to the new participant table and keep this same tuple key for comparison. Compare multisets, not only row counts. Extend with the four established W6 benchmark pairs as regressions; a 4/4 historical fixture pass does not establish the new pair.

## Rollback and release boundary

First apply new structures and views to a copied database in a transaction; preserve the 2.0 view and exporter behavior. For a dry-run rollback, verify all pre-migration rows and source hashes match the saved snapshot. A populated multi-operator relationship cannot be squeezed back into one W6 `organization_id` without loss: rollback must preserve such rows in an exported, versioned side table or explicitly block downgrade. New `SupplyCapacity` Modes similarly require exported IDs, bearers and evidence before dropping anything. Publish only after approved ontology semantics, source-backed examples, database execution, OWL/SHACL checks, SQL↔SPARQL parity and author review.
