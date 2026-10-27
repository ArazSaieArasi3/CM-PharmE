# P5e-2 WholeOver threshold decision

Profile: **CMPE-WholeOver-UpperSumTwo/1.0.0**. Issue #315; wider gates #310/#306.
This is a scoped candidate interpretation pending author/scientific review.

Sales 2014 Table 51 spans printed pages 196–197 (PDF 197–198). Fresh text and
rendered-page inspection confirms an internal inconsistency: description and
formal constraint specify >=2, but both illustrative diagrams label b+d>2.
The pinned archived occurrence constructor uses >=3. The current catalogue
corroborates >=2, although its formula mistakenly says mediatedEnd where its
surrounding definition and the thesis say partEnd. Exact retrieved bytes are
pinned in sources.json; the latest web page is not an immutable version claim.

| ID | Candidate decision | Reason and boundary |
|---|---|---|
| WO-D01 | Give the thesis explicit description/formal constraint precedence over its illustrative diagrams for this named profile. | This is a documented precedence choice, not resolution of the author's historical intent. |
| WO-D02 | Require potentially overlapping sibling parts and finite part-upper sum >=2, or an unlimited part upper. | Whole ends are identified by aggregation; their bounds do not enter the sum. Missing/ambiguous roles or bounds are refused. |
| WO-D03 | Classify this as a source-internal threshold conflict plus archive divergence from the selected prose/formula. | The diagrams align with >=3 for integer finite sums. A simple implementation-defect or version-drift conclusion is not established. |
| WO-D04 | Keep unchanged archived counts and independent profile-frame matches separate. | Source-only sum-two cases remain review items; an engine miss or profile non-match is never a clean-model certificate. |
| WO-D05 | Preserve historical fixtures/results byte-for-byte; freeze new expected values before implementation. | New witnesses cover below/equal/above threshold, unlimited, disjointness, end-role bounds and reordering. |
| WO-D06 | Limit execution to two direct componentOf relations and sibling SubKinds with one explicit generalization set. | No full overlap algorithm, inherited meronymics, modern adapter, refactoring correctness or whole-candidate claim. |

Completion contract: 16 synthetic witnesses, official-parser field fidelity,
three unchanged historical replays, ten malformed/unsupported-input refusals,
independent hosted execution, and explicit applicability limits. The profile is
an independent frame predicate, not a modified official engine. Negative/zero
upper-bound witnesses test the signature only; they are not domain model approvals.

RelComp retains its completed bounded result. RelRig, HomoFunc, integration,
full-model adapter fidelity and author/scientific acceptance remain open.
Keep #315/#310/#306 open and PR #305 draft.
