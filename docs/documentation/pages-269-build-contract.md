# Pages Ontology Documentation Build Contract

Issue: #269  
Parent: #267

## Rule

Generated formal documentation MUST NOT accept an arbitrary TTL/OWL file.

For each ontology family the Pages pipeline resolves:

1. exact semantic source ref from the version registry;
2. canonical module-selection rule;
3. governed build/validation tool;
4. deterministic documentation-input artifact;
5. canonical graph fingerprint;
6. version-specific validation boundary.

Only after those checks pass may WIDOCO/WebVOWL consume the resolved artifact.

## V1

- Source authority: `main@595ea30a66644c1b130b6c1a781dc7afbd7ba284`
- Canonical source: `ontology/source/modules/**/*.ttl`
- Build: `tools/ontology/build.py`
- Documentation input: generated `distributions/cm-pharme.ttl`
- Expected canonical graph fingerprint: `cc823a8aff4d7e7818f8470f2dbad6ca8045ff92e5637fbf3503bc105170a83f`
- Important boundary: the current V1 formal package MUST NOT be described as OWL 2 DL-profile conformant merely because documentation generation succeeds.

## V2

- Source authority: `v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999`
- Canonical source: six governed `v2/ontology/source/modules/*.ttl` modules
- Build: `tools/v2_ontology/build_validate.py`
- Documentation input: generated `distributions/cm-pharme-v2.ttl`
- Expected canonical graph fingerprint: `59ef47eeed732290736e60bfa1c6bf43a12d15df2f50cff931badb5938cc954a`
- Important boundary: the formal baseline can be frozen for regression while the overall CM-PharmE 2.0 research/documentation lifecycle remains **Stable-to-date / Evolving**.

## Publication failure behavior

Any of the following MUST block generated-reference publication for the affected version:

- source-ref mismatch;
- module-set/selection failure;
- semantic build failure;
- fingerprint mismatch;
- required semantic validation failure;
- missing build manifest;
- unexpected version-registry/build-contract drift.

This contract does not yet claim that fresh V1 and V2 artifacts were rebuilt in this slice. Two-run deterministic rebuild evidence and final resolved artifact hashes remain the second #269 slice.
