# Ontology Validation and Build Evidence

CM-PharmE separates logical, structural, semantic and application evidence. B5 turns structural/logical/build checks into reproducible CI quality gates while preserving the B4 evidential boundaries.

## Repository-pinned validation inputs

- [`b3-reference-fingerprints.json`](b3-reference-fingerprints.json) — pinned B3 ontology and SHACL graph fingerprints used to enforce full source parity
- [`../../evaluation/evidence/b4-reasoner-validation.md`](../../evaluation/evidence/b4-reasoner-validation.md) — B4.10 ROBOT/HermiT evidence
- [`../../evaluation/assertions/cq-expectations.json`](../../evaluation/assertions/cq-expectations.json) — executable competency-question regression assertions

Historical B3/B4 validation records remain preserved for provenance.

## CI-generated evidence

Each B5 CI run generates and uploads, rather than hand-maintains in Git:

- `build-manifest.json`;
- `SHA256SUMS.txt`;
- `quality-report.json`;
- `cq-report.json`;
- generated ontology distributions and SHACL;
- HermiT log, summary and reasoned OWL;
- deterministic release bundle and its SHA-256.

## Automated quality gates

The CI pipeline validates:

- exact 1,086-triple B3 ontology graph fingerprint;
- exact 574-triple B3 SHACL graph fingerprint;
- 39 concept classes, 39 object properties, one generalization record and five domains;
- 42 OWL qualified restrictions;
- 76 SHACL NodeShapes and 76 PropertyShapes;
- serialization graph equivalence;
- byte-identical output from two independent clean builds;
- lifecycle and curation repairs;
- eight competency-query assertions;
- ROBOT/HermiT logical consistency.

A PASS in these gates does not imply pharmaceutical-domain completeness, deployed effectiveness, or resolution of B4.10 semantic refinement candidates.
