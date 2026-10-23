# P1 source contract repair — issue #307

The published asset pinned to Zenodo record **19160825** is `pharmacy_data_20260322_131416.csv`, size **1,704,038,344 bytes**, publisher checksum **md5:b43fb62d3d44525de74f930f472d2f03**. The prose description retains a different filename; it is not an accepted discovery alias. The record is pinned even though Zenodo links a newer version.

Source: https://zenodo.org/records/19160825. Attribution and CC BY 4.0 metadata are retained in the manifest and metadata excerpt. `metadata-provenance.json` distinguishes the archived official API response from the independently reopened HTML file list. Refreshing the API timed out during this run; no fresh API response is claimed.

Changes:

- W6 manifest now pins record, actual filename, checksum metadata, size, license, ordered 19-column header, and a separate hashed synthetic fixture alias.
- `source_contract.py` rejects lookalike/stale names, record/DOI/license/size/checksum discrepancies, altered slices, changed fixtures and header mismatches.
- `bootstrap_ingest.py` validates input before connecting to PostgreSQL. Synthetic fixture release identity and filename are explicit. Published-file validation requires a complete local size/MD5 match and is available through `--contract-only`; this fixture loader does not silently become a real-data ingestion pipeline.
- `check_p1_contract.py` replays all five archived real slices before invoking the original G3-D projection; it does not redownload the full source.
- W6 CI now runs source-contract checks before database/KG integration and retains their evidence artifact.

Local results: **12/12 negative contract tests**; W6 fixture preflight passes; **768 real sampled rows → 39,272 RDF triples**, **5/5 migration sensitivity tests**, full shape conformance and exactly the prior canonical ABox hash. Full W6 PostgreSQL/PostGIS execution is tracked separately in `ci-evidence.json` when available; preflight alone does not close #307.

The full 1.704 GB file has **not** been downloaded or locally checksummed. Metadata agreement is not content-integrity verification. The five deterministic slice prefixes are not a representative sample or empirical validation of the four new domains.

Reproduce from repository root with the ontology test Python dependencies:

```bash
python tools/v2_data/check_p1_contract.py --output build/w6/source-contract
python tools/v2_data/bootstrap_ingest.py --contract-only --report build/w6/fixture-preflight.json
```

The PostgreSQL/PostGIS fixture, KG export, SHACL and SQL/SPARQL gates execute in `.github/workflows/v2-data-ci.yml`.
