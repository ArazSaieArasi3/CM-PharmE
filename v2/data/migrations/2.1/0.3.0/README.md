# RDB-M2: FacilityOperation copied-database projection

This is the executable bounded follow-on to [M1](../0.2.0/README.md) and [issue #319](https://github.com/ArazSaieArasi3/CM-PharmE/issues/319). [The P3 decision overlay](../../../../ontology/candidates/2.1.0-alpha.1-p3-facility-operation/README.md) chooses one operating organization and one facility **per** FacilityOperation. Joint and successive operator assignments have separate operation IDs. The 2.1 `operates` relationship is derived through the relator property chain; it is not asserted from names or shared location.

The [verifier](verify_m2.py) runs against a fresh, isolated PostgreSQL/PostGIS **copy** of W6 through the [M2 CI workflow](https://github.com/ArazSaieArasi3/CM-PharmE/actions/workflows/v2-21-rdb-m2.yml):

```bash
python tools/v2_data/bootstrap_ingest.py --reset --report build/v2-21-rdb-m2/ingest.json
python v2/data/migrations/2.1/0.3.0/verify_m2.py
```

It adds a reversible, copy-only `facility_operation_21_evidence` side table. The original W6 `facility_operation.organization_id` and `facility_id`, 2.0 ontology IRIs, source hashes, public IDs and views remain. Four distinct operation IDs exercise one organization at two sites, two organizations at one site via different relators during an overlapping interval, and a successive assignment. A same-name organization/facility without a relator creates no operation. SQL rejects null endpoints, a bad FK, duplicate operation public ID and an inverted date interval. Candidate SHACL rejects a removed endpoint, two operators/sites on one relator and an unbacked direct `operates`. OWL RL checks the derived organization/facility pairs; HermiT checks a valid relator, an open-world incomplete relator and explicitly distinct dual operators on one relator.

One operation is linked through the side table to a **synthetic fixture** EvidenceSupport, Assertion and SourceRecord with a fixture DatasetRelease/TransformationRun; the others have unknown operation provenance and receive no invented source triple. The 2.1 projection carries that existing fixture link through PROV/Dublin Core IDs without promoting the still-unreviewed M025 EvidenceSupport role semantics. SQL↔SPARQL compares normalized operation ID, endpoint IDs, dates and source/evidence chain; RDF serialization round trip is checked. The old four W6 pairs run before, during and after. The side table and all namespaced synthetic rows are removed, then complete table/schema and 2.0 KG fingerprints must match their original values. [scope.json](scope.json) pins source/model commits and input file hashes; the CI report stores versions, expected SQLSTATEs, normalized tuples and checksums.

This is representation and logic evidence on synthetic data. There is no actual external FacilityOperation witness in the P1 mapped ABox; author semantic review and empirical validation remain release gates under #306. No stable 2.0 schema or `main` change is implied.
