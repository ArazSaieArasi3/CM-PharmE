# Use and reproduce the selected core

Use Python 3.12; formal checks also need Java 17. Commands below start at the
repository or curated source-package root and retain the original directory
layout. No Git metadata is needed by the declared computational entrypoints.
External Python packages, Java libraries and PostGIS retain upstream terms and
are not vendored. Direct versions are pinned; this is not a transitive lock or
an immutable container image digest. Record actual runtime in replay evidence.

```bash
python -m pip install -r v2/ontology/profiles/2.1/m1-provenance/0.1.0/requirements-runtime.txt
python v2/ontology/profiles/2.1/m1-provenance/0.1.0/profile.py admit v2/ontology/profiles/2.1/m1-provenance/0.1.0/fixtures/with-run.ttl
python v2/release/2.1/support/0.1.0/verify_contract.py
python -m pip install -r v2/ontology/profiles/2.1/m1-provenance/0.1.0/requirements-verify.txt
python v2/ontology/profiles/2.1/m1-provenance/0.1.0/verify_profile.py
```

To reproduce Q21-01, parse the unchanged query.rq and the raw TTL with RDFLib;
`verify_profile.py` checks all accepted fixtures against frozen expected tuples.
An admission exit of 0 means ADMITTED, and 1 reports the rejected stage. See
the profile README for the allowed local export contract. A malformed file may
raise a parser exception; the CLI is not a general input-format repair service.

## Isolated copied-fixture replay

Provision a new disposable local PostgreSQL 16/PostGIS 3.4 database named exactly
`cmpe_m1_core_332`. The existing integration workflow specifies
`postgis/postgis:16-3.4`; it records actual versions rather than claiming an
immutable image digest. Install the integration requirements and set an explicit
local fixture URL. The following reset destroys only that disposable fixture.
Never substitute a production/default database. Run the preflight before reset.

```bash
python -m pip install -r v2/data/integrations/2.1/m1-core/0.1.0/requirements.txt
export CMPE_FIXTURE_URL='postgresql://postgres:postgres@localhost:5432/cmpe_m1_core_332'
python v2/data/integrations/2.1/m1-core/0.1.0/verify_integration.py --preflight-only --database-url "$CMPE_FIXTURE_URL"
python tools/v2_data/bootstrap_ingest.py --database-url "$CMPE_FIXTURE_URL" --reset --report build/m1-copied-integration/ingest.json
python v2/data/integrations/2.1/m1-core/0.1.0/verify_integration.py --database-url "$CMPE_FIXTURE_URL" --ingest-report build/m1-copied-integration/ingest.json
```

The supported procedure is this preflight/bootstrap/integration sequence. The
old bootstrap's default URL and old verify_m1.py main are not supported standalone
production tools. Export is read-only; a separate one-row nullable-FK test makes
an explicit transaction change and rolls it back. Reports are written under build/.
No local PostgreSQL execution is claimed merely by a successful preflight.

## Verify the proposed release contract

`verify_contract.py --cold-profile` copies only the declared files into a fresh
temporary tree and runs the unmodified profile verifier and integration preflight.
It does not construct a deterministic archive or execute a database. Those are
separate release-package checks. Existing hosted receipts are historical exact
evidence, not a substitute for replaying the eventual final archive.
