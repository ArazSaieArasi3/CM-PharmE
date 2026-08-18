# CM-PharmE Reproducible Build

## Source-of-truth rule

Author ontology semantics only under `ontology/source/modules/`. Generated distributions, SHACL, validation reports, reasoned ontologies, and release bundles are build products.

## Local build sequence

```bash
python -m pip install 'rdflib==7.5.0' 'pyshacl==0.31.0'
python tools/ontology/build.py --output-root build/ontology-artifacts
python tools/ontology/extend_formats.py --artifact-root build/ontology-artifacts
python tools/ontology/validate.py \
  --artifact-root build/ontology-artifacts \
  --report build/ontology-artifacts/validation/quality-report.json
python tools/ontology/validate_shacl.py \
  --ontology build/ontology-artifacts/source/cm-pharme.ttl \
  --data evaluation/samples/vaccine-distribution.ttl \
  --shapes build/ontology-artifacts/shapes/cm-pharme.shacl.ttl \
  --summary build/ontology-artifacts/validation/shacl-summary.json \
  --report-ttl build/ontology-artifacts/validation/shacl-report.ttl \
  --report-text build/ontology-artifacts/validation/shacl-report.txt
```

ROBOT-dependent Manchester/Functional conversion, profile assessment, ontology metrics, HermiT reasoning, and final packaging are executed by GitHub Actions using the pinned ROBOT release.

## Reproducibility contract

- Two independent clean RDF builds must be byte-identical.
- The canonical graph fingerprint must match the pinned reference.
- RDF-compatible distributions must parse and represent the same graph.
- Manchester and Functional Syntax are generated twice and compared byte-for-byte.
- Their round-trip RDF/OWL conversions must match the canonical RDF graph.
- The final ZIP bundle is built twice with fixed ordering and timestamps and must be byte-identical.
- SHA-256 digests are published for integrity checking.

## Generated-artifact policy

Generated files are published in GitHub Actions artifacts and future governed releases rather than maintained by hand on `main`. This prevents semantic drift while preserving reproducible access to all consumer formats.
