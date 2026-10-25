# RDB-M1: versioned 2.1 provenance projection

This is the executable, read-only follow-on to [the #317 inventory](../0.1.0/README.md) and [issue #318](https://github.com/ArazSaieArasi3/CM-PharmE/issues/318). It projects only M001–M004 (`Dataset`, `DatasetRelease`, `SourceRecord`, `ProvenanceActivity`) into the separately named 2.1 graph. Its explicit [36-row disposition table](mapping-dispositions.csv) marks every other W6 registry row unimplemented for 2.1, including M023's still-reviewed quality projection and M035/M036's zero-change/no-table status. [Pinned inputs](scope.json) identify the W6 and model commits and verify source file digests at execution.

The 2.1 instance IRIs are separate from 2.0. Dataset and release use the unchanged W6 public IDs; a source record without a public ID gets a collision-resistant composite of `(release public ID, row number, source hash)` encoded as its IRI and `dct:identifier`. `prov:value` carries the original hash and `prov:wasGeneratedBy` links the original transformation-run public ID when present. A DOI is associated with its dataset; the release and record links use the corresponding declared 2.1 object properties. This is a bounded mapping decision for the candidate, not an assertion that every same-named term across versions has approved semantics.

Run on a **copied, isolated** W6 PostgreSQL 16/PostGIS 3.4 fixture database (the [dedicated CI workflow](../../../../../.github/workflows/v2-21-rdb-m1.yml) provisions one):

```bash
python tools/v2_data/bootstrap_ingest.py --reset --report build/v2-21-rdb-m1/ingest.json
python v2/data/migrations/2.1/0.2.0/verify_m1.py
```

The verifier hashes every W6 base table's rows and the column/constraint catalog before and after, then runs the four historical W6 SQL/SPARQL pairs twice and checks that both 2.0 graphs have the same canonical hash. For Q21-01 it compares normalized `(DOI, release public ID, row number, source hash, run public ID)` answers across SQL and 2.1 SPARQL, checks the encoded source identity after RDF serialization round trip, and validates the bounded 2.1 graph against candidate SHACL. The [CI report artifact](https://github.com/ArazSaieArasi3/CM-PharmE/actions/workflows/v2-21-rdb-m1.yml) includes exact PostgreSQL/PostGIS and Python dependency versions, before/after data and schema hashes, normalized answer hashes and the graph fingerprint.

**Rollback:** this path issues no DDL or DML, does not edit 2.0 `ontology_iri` defaults, hashes, DOI, release/run identifiers, assertions or evidence links. Delete the separate 2.1 export files to roll back. The legacy W6 graph remains the only exported assertion/evidence representation in this slice; candidate M025 `EvidenceSupport` has changed role semantics and is deferred. The fixture demonstrates representation mechanics, not source completeness or release 2.1 GA readiness. #319 is the next relational slice.
