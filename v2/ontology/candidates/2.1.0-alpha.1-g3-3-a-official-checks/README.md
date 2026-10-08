# G3-3-A — native OntoUML tooling checkpoint

Source candidate: [G3-2e-E native model](../2.1.0-alpha.1-g3-2e-e-native-integration/ontouml.json), 524 flat elements. No model change in this checkpoint.

## Executed checks

| Check | Version and input | Observed result | Boundary |
| --- | --- | --- | --- |
| OntoUML JSON Schema | `ontouml-schema` 1.0.2, Ajv 8.20.0, direct candidate | Valid; 0 schema errors | Exchange shape only, not semantic correctness |
| Current OntoUML JS parser | `ontouml-js` 1.0.0, direct candidate | Parsed `Project16`; 144 classes | Parser acceptance only |
| Legacy syntax verifier | `ontouml-js` 0.4.1, compatibility projection | 244 diagnostics: 144 missing nature restrictions, 100 incompatible generalization natures | Version/projection sensitive; not 244 independently confirmed anti-patterns |
| JSON2Graph | `ontouml-json2graph` 2.0.2, compatibility projection | Strict invalid-cardinality, invalid-stereotype and unresolved-element policies accepted; 3761 RDF triples | Decoder, not semantic or anti-pattern engine |
| Full 20-item anti-pattern catalogue | No compatible detector successfully run on native candidate | **Not evaluated** | No zero-anti-pattern or global conformance claim |

The compatibility projection nests the flat model, renames `BinaryRelation` to `Relation`, and omits 24 Notes. It does **not** alter the authoring candidate. The legacy verifier yields `restrictedTo: null` for each projected class; all 144 source classes have an empty `restrictedTo` array. The 100 generalization messages cascade from the nature data. The earlier G3-2d source contains the same 144 class JSON records and 100 generalization JSON records (0 differences), so this checkpoint did not introduce those source records or their empty nature restrictions. This comparison does not substitute for a legacy verifier rerun on the baseline.

The [normalized verifier findings](legacy-verifier-findings.json) retain every diagnostic's code, severity, source ID and description. [Tool results and baseline comparison](tool-and-baseline-inventory.json) and the [20-entry coverage ledger](anti-pattern-coverage.json) distinguish completed checks from open ones. The complete raw verifier output and intermediate compatibility projection were retained during execution, but the normalized report avoids duplicating embedded model objects in the repository.

Reproduce parser, schema and legacy diagnostics with [run_checks.cjs](run_checks.cjs) under Node 24.19.0. Install `ontouml-js@1.0.0 ontouml-schema@1.0.2 ajv@8.20.0 ajv-formats` in one temporary prefix and `ontouml-js@0.4.1` in another. Run `node run_checks.cjs ../2.1.0-alpha.1-g3-2e-e-native-integration/ontouml.json /path/to/current/node_modules /path/to/legacy/node_modules /path/to/output`. A fresh rerun matched the committed schema and normalized issue JSON exactly.

Official source references: [OntoUML schema](https://github.com/OntoUML/ontouml-schema), [OntoUML JS](https://github.com/OntoUML/ontouml-js), [OntoUML Server verification scope](https://github.com/OntoUML/ontouml-server#available-services), [anti-pattern catalogue](https://ontouml.readthedocs.io/en/latest/anti-patterns/index.html). The server's `/v1/verify` is syntactic verification; it does not promise all 20 catalogue detectors. The archived Python validator and OLED/Menthor tooling do not supply an established direct run on this flat JSON in this checkpoint.

## Decision gate

G3-P5 has started and remains open. In G3-3-B, adjudicate the legacy nature findings and generalizations against current OntoUML semantics, then get reproducible full-catalogue detection where feasible and record each occurrence's scope, truthmaker, counterexample, and disposition. If a compatible engine remains unavailable, explicitly maintain the coverage gap and use bounded manual checks without converting an absence of findings into a clean certificate. Keep PR #305 draft and issue #306 open.

Progress: G1/G2 closed, G3 active, G4/G5 pending = **2/5 major stages (40% closed)**. G3 has **2/7 named packages closed (28.6%)**; P3/P4/P5 in progress. Five bounded G3 turns remain (B–F) plus scientific human gates. Percentages count closures, not elapsed effort or ontology quality.
