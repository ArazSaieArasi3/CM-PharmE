# P5e-1 RelComp lower-bound decision

Profile: **CMPE-RelComp-PositiveLowerBound/1.0.0**. Issue #315; wider gates
#310/#306. This is a delegated, scoped candidate decision for later author review.

## Source interpretation

Sales (2014), Table 44, printed page 166 (PDF page 167), is the governing source
for the positive-lower-bound requirement. The current official catalogue agrees
on this condition. The pinned archived implementation omits this check from its
selection code. The original PDF and rendered table were reviewed in this slice;
retrieval locations and exact digests are in sources.json.

For an explicitly declared composition frame, the selected outer end must have
a positive lower bound and either a plural finite upper bound or an unlimited
upper bound. The inner association differs from the outer one, and both its end
types must equal or specialize the selected shared outer-end type.

The selected shared end is assigned the pattern role ATarget explicitly. End-list
reordering must preserve that role binding and its cardinality. This normalization
is our documented modeling interpretation of the source's two endpoint variants,
not a claim that its original orientation wording is unambiguous. The adapter must
preserve which end was selected. An unbound or uncertain frame is refused rather
than normalized by guesswork.

## Recorded decisions

| ID | Scoped decision | Reason and boundary |
|---|---|---|
| RC-D01 | Use the published positive-lower-bound rule for this named candidate profile. | Thesis and catalogue agree; their provenance is pinned. The archive is not the governing specification by virtue of being executable. |
| RC-D02 | Keep raw archived-engine occurrences and source-profile frame matches as separate outputs. | Optional plural ends remain visible as engine-only review items. A failed source signature does not prove absence of a modeling problem. |
| RC-D03 | Classify the missing lower-bound test as a pinned implementation conformance gap relative to the selected published condition. | No claim is made about the developers' intent or the historical cause; a deliberate semantic version change is not established. |
| RC-D04 | Preserve all historical fixtures, expectations and results byte-for-byte; create new independent oracles before implementation. | Never adjust archived expectations to hide the discrepancy. |
| RC-D05 | Evaluate only declared, fully typed association frames with explicit bounds and acyclic ancestry. | Unknown bounds/types, duplicate IDs and unsupported subsetting are refused. This is not a modern-to-legacy adapter or a full model search. |
| RC-D06 | Adopt the implementation choice for this candidate slice; keep scientific/author and full-candidate acceptance open. | No silent engine patch, automatic ontology refactoring, clean-model certificate or release promotion follows. |

No archived Java class is changed. This profile is a separately named frame
predicate plus a comparison report, not an official detector or a fork claiming
official behavior. Runtime count agreement alone does not validate archived
occurrence orientation or its refactoring plans.

## Completion contract

Freeze 14 independent paired/boundary expectations, then check their serialized
fields with the official parser, execute the unchanged pinned RelComp detector,
and compare the independent profile predicate. Replay the three historical
RelComp witnesses and require identical fields, hashes and engine counts.
Exercise eight fail-closed malformed/unsupported-input cases. Publish both output
channels and their discrepancies without counting a profile non-match as clean.

This completes only the lower-bound discrepancy slice when the evidence passes.
WholeOver, RelRig, HomoFunc, integration/applicability, author review and all modern
adapter fidelity blockers remain tracked. Do not close #315/#310/#306 from this
slice alone.
