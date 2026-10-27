# P5e-4 HomoFunc part-minimum decision

Profile: **CMPE-HomoFunc-MinimumTwo/1.0.0**. Issue #315; wider gates #310/#306.
This is a delegated scoped candidate interpretation pending author/scientific review.

Sales 2014 section 5.8 opens with a broad single-component description, then
Table 38 explicitly requires a part-end lower bound >=2. The current catalogue
repeats that condition. Fresh text and rendered-table review is pinned in
sources.json. The archived selection and occurrence constructor omit this lower-
bound check. Source-code behavior remains unchanged as a reproducibility channel.

| ID | Candidate decision | Reason and boundary |
|---|---|---|
| HF-D01 | Use Table 38's explicit part-minimum >=2 constraint for this named profile. | The introductory prose omits the threshold; explicit constraint plus catalogue corroboration governs this scoped interpretation. |
| HF-D02 | Resolve whole/part by aggregation and apply the lower bound to the part end only. | Reordering and changing the whole-end lower must not shift the source requirement. |
| HF-D03 | Compare the independent profile and unchanged raw archive separately. | Zero/one-minimum raw detections remain engine-only review items; profile non-match never establishes a clean model. |
| HF-D04 | Record a missing-threshold implementation conformance gap relative to the selected explicit condition. | The archive aligns with the broader description; developer intent, chronology and a deliberate semantic version change are not established. |
| HF-D05 | Restrict this executable slice to one direct componentOf, plus a two-distinct-part negative control, on nonabstract legacy Kinds without ancestry. | Whole and part are functional-complex witness types. This is not evidence for modern nature conversion, inherited part counting or the complete HomoFunc algorithm. |
| HF-D06 | Freeze independent expectations before implementation and preserve all four historical fixtures/results. | Cover below/at/above threshold, finite/unlimited uppers, role-bound reversal, whole-end controls and non-single-part structure. |
| HF-D07 | Keep full-candidate/scientific/author and integration acceptance separate. | No automatic conversion to Collective/memberOf, new part invention, ontology edit, full model run, official-engine patch or release promotion. |

Completion contract: 16 synthetic witnesses; official parser structural and
whole/part role checks; four historical byte/field/count-preserving replays; ten
missing/invalid/out-of-scope refusals; independent hosted results and applicability.
All declared intervals are preserved, including zero-upper signature controls;
those witnesses are not approvals of their domain semantics. Other part-whole
modeling constraints are outside this threshold slice.

This completes only the fourth scoped implementation when the evidence passes.
P5e-5 cross-rule integration, author/scientific source adjudication and the full
native adapter/detector gates remain open. Keep #315/#310/#306 and draft PR #305.
