# RelRig explicit-endpoint review slice

Tracking #315 P5e-3; #310/#306 remain open. Profile:
**CMPE-RelRig-ExplicitEndpointReview/1.0.0**.

[Decision](decision.md), [primary/source digests](sources.json) and
[independent oracles](fixed-oracles.json) were frozen at
`a7c48d75d76972190c9c76d2ba61dcbe64710aaf` before implementation.
The governing candidate interpretation is the source's semantic review procedure:
rigidity, optionality and actual dependency direction require domain investigation.
It does not treat the table condition or archive predicate as a domain-error oracle.

For a rigid mediated type the independently preserved Boolean channels are:

| Relator-end readOnly | Mediated-end readOnly | Raw archive | Literal published frame | Candidate disposition |
|---|---|---|---|---|
| false | false | 1 | 0 | Rigid dependency review; mediation baseline review |
| false | true | 1 | 1 | Rigid dependency review |
| true | false | 0 | 0 | Rigid dependency review; mediation baseline review |
| true | true | 0 | 1 | Rigid dependency review |

The literal published condition is retained as a signature, not promoted to a
complete error detector. Explicit false is distinct from unknown/missing. Both
flags must be explicit; endpoint roles follow the unique Relator type, including
when serialized ends are reordered. No flag combination proves that a rigid
mediation is correct or incorrect. Role controls preserve the separate baseline
review when the mediated flag is false. A Role signature non-match is not a full
model approval. Optional/unlimited bounds are inspected without introducing a
new lower-bound gate not present in these two compared predicates.

The historical archive and adapters are unchanged. In the two old basic fixtures,
absent readOnly attributes still parse as legacy false defaults: those original
runtime observations are replayed, but those fixtures are refused by this profile's
explicit-input contract. The four historical Boolean fixtures are replayed with
explicit-field preservation and original raw/published outputs.

The [native admission wrapper](native_admission.py) requires exact native bool
values before invoking the historical structural adapter. Synthetic known true
and false controls are checked with the official parser. Null, missing, string
and integer alternatives are refused. Full-candidate admission must stop before
conversion; original source bytes and uncertainty are preserved. Passing this
extra guard does not resolve the old adapter's full-fidelity limits.

```sh
python v2/ontology/candidates/2.1.0-alpha.1-relrig-policy/run_policy.py \
  --archive /path/to/unchanged/pinned/oled \
  --ecj /path/to/ecj-3.39.0.jar
```

Local evidence: **16/16** explicit witnesses, **6/6** unchanged historical replays, **12/12** malformed/out-of-scope legacy refusals and **7/7** native admission cases pass. [local-results.json](local-results.json) records structural/readOnly/role parser evidence and exact runtime hashes; [traceability.csv](traceability.csv) preserves the per-case channels. Hosted evidence is recorded after execution. [Applicability](applicability.json) explicitly
records no full-candidate run or modern adapter/scientific acceptance. This is
review routing for one restricted frame; inherited relators, other rigid/mixin
stereotypes, arbitrary topology, refactoring correctness and actual temporal
facts are outside scope. Do not close #315/#310/#306 or promote draft PR #305.

The unchanged native snapshot has **172 Properties, 82 unknown readOnly values and three mediations with six unknown ends**. These are input inventories, not RelRig detections; original IDs are retained in the report. No values were filled and no full-candidate conversion/detector run occurred.
