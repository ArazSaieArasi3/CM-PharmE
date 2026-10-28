# Next-publication route — planning record 0.2.0

Next publication target: **2.1.0-rc.1, an explicitly experimental research
checkpoint**. Final target **2.1.0 GA** is unchanged. This is a preparation plan,
not an existing release, tag, completed approval or promise of a fixed number of
runs. The earlier six rows were workstreams, several containing multiple bounded
executions. Completing six labels is not a release acceptance criterion.

## Cut line for the next publication

After the bounded #323 EvidenceRecord implementation, stop adding features and
stop making exhaustive unknown-field cleanup a prerequisite for this experimental
checkpoint. Prepare the existing, tested evidence as an inspectable versioned
bundle with explicit limits. Correct a defect before RC only if it breaks its
stated contract, reproducibility or truthful claim envelope.

Include the separate native review candidate and its exact delta; independently
scoped ContextClass/EvidenceRecord, source-policy and copied-W6 evidence; ORSD
0.2.0 with its current pending content status; original version/provenance links;
and a clear known-limits/claim matrix. Do not assert that old frozen CI baselines,
experimental OWL modules or toy detector calibration prove a complete translation
or full scientific validation of the newest native model.

Do not delay RC for expanded features in the four domain modules, a finished
manuscript, a complete Wiki portal redesign or exhaustive native unknown cleanup.
Retain those tasks and their existing issues. Minimum release documentation,
artifact identity, scope/claims, known-limit disclosure and replay evidence remain
mandatory. Do not merge draft PR #305 into stable main to manufacture readiness.

| Order | One bounded package | Acceptance before moving on |
|---|---|---|
| RC-01 | Freeze experimental RC contents and claims | Exact source/artifact list, version boundaries, supported versus pending claims, exclusions and known limits; no scientific/GA approval invented |
| RC-02 | Build and replay the release bundle | Versioned archive, checksums, provenance, minimal changelog/README, reproducible commands and a clean-checkout bounded replay tied to the exact source |
| RC-03 | Prepare tag/release payload and publish prerelease | Tag/asset/source agreement, experimental prerelease flag, explicit pending gates and verified publication URL/status; never claim success from a prepared payload alone |

Each row is intended as one manageable execution, with an explicit end criterion;
new failures or missing external access may require a separately recorded fix.
There is no calendar or automatic three-run guarantee. The current connector
supports repository/issue/PR writes but exposes no release-publication write tool.
RC-03 therefore needs a supported release-write route or a maintainer publication
action after the concrete payload/assets are ready. Do not treat this as grounds
to pause the already executable preparation work or request speculative approval.

## GA remains a separate gate

The original [GA gate register](../0.1.0/README.md) still governs 2.1.0. It includes
native input fidelity and full-candidate validation, explicit source/author
adjudication, ORSD/domain scientific commitments, source/empirical and human/expert
claims, and reviewed publication assets. In particular, full 20-family execution
has not happened and the four source-policy scientific acceptances remain pending.
RC does not close #306/#310/#315 or stand in for expert evidence. Publication of
this research checkpoint must label every such open gate.

The planned three packages reach an experimental prerelease only when their
actual criteria pass and publication is confirmed. They do not by themselves make
GA ready. A final GA release follows verified closure of its own scientific and
artifact gates, not a preselected issue-count or task-count threshold.
