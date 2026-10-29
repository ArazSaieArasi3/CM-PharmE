# Verify, use and rebuild this distribution

Use Python 3.12. Java 17 is additionally needed for formal checks. External
Python libraries and PostgreSQL/PostGIS are not bundled. Their upstream terms
apply. Keep the complete source directory layout and run commands from it.

Before extracting, verify the archive SHA-256 against the independently trusted
release checksum/receipt. The trusted verifier also rejects unexpected files,
missing dependencies, changed bytes, traversal and all symlinks/nonregular members.

```bash
cd source
python -m pip install -r v2/ontology/profiles/2.1/m1-provenance/0.1.0/requirements-verify.txt
python -m pip install -r v2/data/integrations/2.1/m1-core/0.1.0/requirements.txt
python v2/ontology/profiles/2.1/m1-provenance/0.1.0/profile.py admit v2/ontology/profiles/2.1/m1-provenance/0.1.0/fixtures/with-run.ttl
python v2/ontology/profiles/2.1/m1-provenance/0.1.0/verify_profile.py
cd ..
python release-tools/build_archive.py --root source --output-dir rebuilt
```

Two builds must yield the same archive bytes. Verify the original archive using
trusted release-tools/verify_archive.py with --archive, --expected-sha256 and
--output-dir. It validates/extracts the archive and runs the support, profile and
integration preflight checks. Add --self-test to exercise malformed-archive controls.

Full copied-database replay additionally requires a fresh disposable loopback
PostgreSQL 16/PostGIS 3.4 database named cmpe_m1_core_332 and explicit
--database-url. The verifier runs the target guard before fixture bootstrap --reset
and executes only extracted source. Reset destroys that isolated synthetic fixture.
Never supply production/default database credentials. Existing export connections
are read-only; one separate nullable-FK test explicitly changes and rolls back a row.
No database execution is inferred from preflight-only success.

The archive is deterministic, but external transitive package versions and the
postgis/postgis:16-3.4 image tag are not an immutable environment lock. Actual
runtime and exact archive digest belong in the replay receipt. Published RC bytes
are outside this archive and stay unchanged.
