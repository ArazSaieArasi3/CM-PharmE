# HomoFunc minimum-two source-policy slice

Tracking #315 P5e-4; broader gates #310/#306 remain open. Profile:
**CMPE-HomoFunc-MinimumTwo/1.0.0**.

[Decision](decision.md), [pinned primary sources](sources.json) and
[fixed expectations](fixed-oracles.json) were frozen at
`9dd92b243391a0ac5d45ad51925b9ea170eeac3c` before implementation.
Sales 2014 Table 38 and current catalogue explicitly require part lower>=2.
Section 5.8's broad introduction omits the threshold; the named candidate policy
uses the explicit constraint. Archive selection/constructor omit that check,
which is recorded as a conformance gap relative to this selected interpretation,
not a proven historical-intent or version-drift finding.

The independent source predicate reports separately from unchanged archived
HomoFunc counts. Below-threshold raw detections remain ENGINE_ONLY_REVIEW_REQUIRED.
A profile non-match is never a clean-model certificate. Aggregation binds whole
and part roles independently of serialized order. Whole-end lower bounds and
unlimited uppers do not substitute for the part-end minimum. Two distinct direct
part types fail the single-part signature in both channels.

```sh
python v2/ontology/candidates/2.1.0-alpha.1-homofunc-policy/run_policy.py \
  --archive /path/to/unchanged/pinned/oled \
  --ecj /path/to/ecj-3.39.0.jar
```

Local evidence: **16/16** witness rows, **4/4** historical byte/field/count-preserving replays and **10/10** malformed/unsupported refusals pass. [local-results.json](local-results.json) retains exact fields, roles, raw/profile outputs and runtime hashes; [traceability.csv](traceability.csv) records the per-case expectations. Nine below-minimum states remain engine-only review items. [Hosted run 40472176042](https://github.com/ArazSaieArasi3/CM-PharmE/actions/runs/40472176042) passes at implementation `5493bc041291e3cd1459bc148106c5c7ee998aaf`, with **21/21 distinct workflows successful**. [hosted-results.json](hosted-results.json) and [ci-evidence.json](ci-evidence.json) preserve exact results and original implementation/job/artifact provenance. Local and hosted cases, parsed structural/role fields, refusals and runtime JAR hashes agree exactly. Artifact ID `12719615888`, digest `sha256:d41191b96ca9a511658e05441c8712360269da28f74096017338f9ae6b27621d`. Historical source, fixtures,
expectations and results remain unchanged. The official parser independently
checks class/relation/end/type/bound/aggregation fields and resolves whole/part
roles. Zero-upper witnesses test the signature, not model validity.

[Applicability](applicability.json) records no full-candidate run. This restricted
legacy Kind witness scope is not a converter of modern nature, a proof for all
inheritance/part-count variations, a validation of refactoring plans or author/
scientific acceptance. No automatic Collective/memberOf change or new part
invention follows. Keep #315/#310/#306 open and PR #305 draft. Cross-rule
integration and full-candidate acceptance remain separate work.

The four scoped implementations are **4/4 verified**. The [technical integration/review bundle](../2.1.0-alpha.1-source-policy-integration/README.md) consolidates their evidence without granting scientific/author acceptance or full-model validation.
