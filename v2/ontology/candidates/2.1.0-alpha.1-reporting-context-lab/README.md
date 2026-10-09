# Reporting-context and claim-bridge proposal laboratory

Isolated successor to `2.1.0-alpha.1-prov-target-lab`; no native or baseline mutation.

Run with Python 3 and Java 17, using versions in `runtime.json`, from this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python run_tests.py
PYTHONDONTWRITEBYTECODE=1 python run_esmp.py
PYTHONDONTWRITEBYTECODE=1 python run_real_data.py
PYTHONDONTWRITEBYTECODE=1 python run_regression.py
PYTHONDONTWRITEBYTECODE=1 python finalize.py
```

The previous labs are runtime dependencies. Replays use pinned source JSON, not new API results. Reruns regenerate graphs with non-stable blank-node labels and timestamps, so byte identity is not expected for generated artifacts; semantic results should match. Source snapshot hashes must match. HermiT receives RDF/XML verified graph-isomorphic to input, with the earlier explicitly documented PROV projection.

The five EMA profiles are manual design interpretations of official guidance. Contexts are synthetic. No real action announcement or operational submission is present. The PDF is URL/hash pinned but not archived here. NDC sampling is purposive, 15 source products with 5 overlapping the prior sample, 19 package projections. 74 direct field claims and 76 mapping interpretations are kept distinct; no described listing/authorization fact is materialized. Native identity, full OWL2-DL/UFO validity, legal compliance and release readiness are not established.

See `decision-report-fa.md`, `work-status-fa.md`, `requirements-traceability.json`, `continuation-checkpoint.json` and machine-readable results. Historical C 88/89 and scientific acceptance remain open. PR305 stays draft; the four domain disposition decisions stay on hold.
