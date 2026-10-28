# Isolated M1 copied-W6 integration — 0.1.0

This is #332's bounded integration for the approved small **2.1.0** support cut.
It binds the pinned standalone M1 profile to one fresh PostgreSQL/PostGIS copy of
the existing W6 synthetic fixture. It does not migrate a default/production DB,
change the historical M1 verifier or add any mapping outside M001–M004.

## Frozen reference and executed cases

The contract, source pins and golden tuples were frozen at
`44803b489a44b484fa603e6fb4e4c92d50d82641` before the integration verifier.
The seven expected source rows come from the pinned four outpatient and three
inpatient synthetic CSV rows. Their release/public IDs and hashes follow the
existing pinned loader rules. Golden tuples are not copied from this verifier's
output. The secondary loader's historical release naming is retained; all rows
remain explicitly synthetic regardless of source DOI/filename metadata.

| Case | Expected output and boundary |
|---|---|
| Baseline copied fixture | Seven Q21-01 tuples; 54 raw RDF triples; direct profile focuses 2 Dataset / 2 DatasetRelease / 7 SourceRecord / 1 ProvenanceActivity |
| Optional run, rolled back | One selected row's nullable run FK is temporarily NULL; seven expected tuples, one missing run and 53 triples; transaction always rolls back |
| Export-data countercontrols | Missing record type/key and a changed hash/key component are refused by the actual profile |
| Enforced read-only connection | A harmless UPDATE WHERE FALSE command is refused with SQLSTATE 25006 |

The original four W6 SQL/SPARQL pairs are executed before and after. The unchanged
Q21-01 query is checked against SQL and the frozen seven-tuples in both cases.
Four RDF serialization roundtrips preserve graph and query answers. The strict
OWL view explicitly excludes only the seven rdf:value serialization triples;
the complete raw graph remains intact for query/identity/admission.

## Preservation and runtime

Before/after evidence compares all 24 cmpe base tables' row hashes, the existing
column/constraint catalog, all 22 declared 2.0 ontology_iri defaults, indexes,
views and the legacy KG/query hashes. The only fixture variation is one temporary
nullable-FK update, explicitly reported and rolled back. Thus the exporter uses
enforced read-only connections while the separate boundary test exercises an
actual rollback; do not describe the entire test as containing no DML.

The old M1 source is imported only for its pinned pure SQL/export/hash/legacy-query
helpers. Its main/full-P3 validation is never called. Admission loads only the
50-triple isolated profile and 143-triple shape graph; no experimental P3 ontology
or shapes are parsed. New source/profile/oracle pins are rechecked after execution.

The dedicated workflow provisions `postgis/postgis:16-3.4` with a private job-local
database named `cmpe_m1_core_332`. The verifier refuses other names/remote hosts,
has no implicit database URL and checks the target before fixture bootstrap.
Actual PostgreSQL/PostGIS, Python, driver and libpq versions are recorded. The
requested image tag is not represented as an immutable image digest.

```bash
python -m pip install -r v2/data/integrations/2.1/m1-core/0.1.0/requirements.txt
python v2/data/integrations/2.1/m1-core/0.1.0/verify_integration.py --preflight-only
```

The full run requires the named isolated service and a bootstrap receipt from
tools/v2_data/bootstrap_ingest.py. The workflow supplies its explicit URL and
writes results under build/m1-copied-integration. There is no claim of a local
PostgreSQL execution where no such server is available; hosted execution receipts
identify their actual commit/event and independent database instance.

The next release packet freezes the final supported file/claim/rights manifest
and minimum use/reproduction docs, then constructs and cold-replays a new exact
GA bundle. Published RC, W5/W6, old M1, full modern native and scientific/ORSD/
expert records remain unchanged. Fixture integration is not broad scientific,
full-source, full 36-mapping, full OntoUML or GA acceptance.

## Rights

Original verification code and workflow are MIT under approved D-03; original
contracts, evidence arrangement and documentation are CC BY 4.0. See
v2/release/roadmap/0.2.0/licenses/MIT.txt and license-scope.json. The underlying
source/fixture notices, external dependencies and historical payloads retain
their own terms; no blanket data/runtime relicense is applied.
