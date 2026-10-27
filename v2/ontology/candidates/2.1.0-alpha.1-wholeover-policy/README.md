# WholeOver threshold source-policy slice

Tracking: #315 P5e-2; scientific/full-candidate gates #310/#306 remain open.
Profile: **CMPE-WholeOver-UpperSumTwo/1.0.0**.

[Decision](decision.md), [pinned sources](sources.json) and [fixed expectations](fixed-oracles.json)
were frozen at `a689d3e93bc2ab8c16a05c9f5719b8d2c12ce62a` before implementation.
The candidate explicitly gives description/formula precedence over inconsistent
illustrative diagrams; original intent and author acceptance are not established.

The independent Python frame predicate reports separately from the unchanged
archived WholeOver detector. On these restricted witnesses the raw archive uses
finite upper sum >=3; the profile uses >=2. Unlimited part ends satisfy either
threshold, while explicit disjointness removes possible overlap in both outputs.
End roles follow aggregation, including after serialized-end reordering. Whole-end
cardinalities are never summed as part cardinalities. Four sum-two witnesses stay
SOURCE_ONLY_REVIEW_REQUIRED; no engine miss or profile non-match certifies a clean
model. Thesis diagrams align with the archived finite threshold, so this package
does not assert a simple implementation defect or a proven version-history cause.

Local execution: **16/16** cases, **3/3** byte/field/count-preserving historical
replays and **10/10** malformed/unsupported refusals. Exact results and runtime
JAR hashes are in [local-results.json](local-results.json); per-case links are in
[traceability.csv](traceability.csv). Hosted evidence is recorded after execution.

```sh
python v2/ontology/candidates/2.1.0-alpha.1-wholeover-policy/run_policy.py \
  --archive /path/to/unchanged/pinned/oled \
  --ecj /path/to/ecj-3.39.0.jar
```

Input scope: two direct componentOf relations, one Kind whole, two sibling
SubKinds sharing a Kind, one explicit generalization set and explicit bounds.
This is not a complete overlap detector, modern converter, validation of archived
refactoring plans or approval of zero-upper-bound domain models. The official
parser independently verifies class/relation/end/type/bound/aggregation/ancestry/
generalization-set fields before runtime counts are accepted. No archive class,
historical fixture or historical expectation is edited.

[Applicability](applicability.json) records no full-candidate run and preserves
native unknown type/cardinality and specialized-property blockers. Source inputs
and outputs may not be narrowed silently to fit this predicate. RelRig, HomoFunc,
integration and independent author/scientific review remain pending. PR #305 stays
draft; no merge, final release, production migration or GA approval follows.
