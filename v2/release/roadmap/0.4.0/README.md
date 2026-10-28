# Scoped 2.1 progress — planning record 0.4.0

**Target 2.1.0; stable release not yet published.** Approved D-01 / SC-REL / D-03
continue from [record 0.2.0](../0.2.0/README.md). **#332 is verified; #333 is next.**

The [isolated copied-W6 integration](../../../data/integrations/2.1/m1-core/0.1.0/README.md)
at implementation `51185d591c9d681d943388d32e86f6d60b77042f` passed
[direct push run 40746588214](https://github.com/ArazSaieArasi3/CM-PharmE/actions/runs/40746588214)
and an independent PR run. Actual PR execution used merge commit
`376612671f3c4b710e75875810a710a8f485beea` with the same Git tree. Each run used a
separately bootstrapped PostgreSQL/PostGIS fixture. Both downloaded artifact ZIP
sizes/digests match the GitHub metadata; all 24 declared normalized fields agree.
Fresh bootstrap timestamps differ across runs and are explicitly excluded from
cross-run equality. Full before/after preservation is verified within each run.
All 27 head-referenced workflow families passed within their own pinned scopes.

Both baseline and optional-run boundary cases preserve the seven golden Q21-01
SQL/SPARQL tuples and pass actual targeted admission. The 54/53-triple raw graphs
remain distinct from the explicitly scoped strict OWL view, which excludes seven
rdf:value triples. Four legacy query pairs, 24 tables, their row/schema/catalog
state, 22 default 2.0 IRIs, indexes/views and legacy KG/query hashes survive the
execution. Export connections are enforced read-only; the separate one-row
nullable-FK boundary test is explicitly rolled back. No local DB execution is
claimed. See [exact CI receipts](../../../data/integrations/2.1/m1-core/0.1.0/ci-evidence.json).

| Next bounded work | Issue | Release point |
|---|---|---|
| Minimum supported file/claim/rights manifest and use/reproduce docs | [#333](https://github.com/ArazSaieArasi3/CM-PharmE/issues/333), ready | Supported 2.1 contract frozen |
| New deterministic curated archive and cold replay | Separate child of #306, after #333 | Exact GA package verified |
| Reviewed publication and downloaded-byte verification | #306, after exact package checks | Stable 2.1.0 |
| Next completed compatible capability | Retained source/native/domain/data work | Incremental 2.2.0 |

The [four-packet release-cut review](release-cut-review.json) is HOLD for concrete
minimum-release-contract and new-package checks. These are bounded work groups,
not a promise of a fixed number of executions. Whole-model, other module/source,
ORSD, human/expert and research obligations remain tracked for their own scope;
they do not all need to land in this limited core release. A critical defect in
the retained supported cut still blocks it. Keep WIP one and at most three ready
children; create the next archive child only when its contract is ready.

Source-policy acceptance remains **1/4**, historical ORSD semantic acceptance
**0/83**, and no external expert responses were created. PR #305 remains draft;
full modern-native validation and all 36 mappings are not accepted by this fixture
check. Frozen W5/W6, the old M1 verifier/profile/oracles and published
[2.1.0-rc.1](https://github.com/ArazSaieArasi3/CM-PharmE/releases/tag/2.1.0-rc.1)
remain unchanged. [release-plan.json](release-plan.json) and
[next-steps.csv](next-steps.csv) record this checkpoint. Release targets after
2.2.0 retain semantic MAJOR.MINOR.PATCH compatibility rules, not a waterfall scope
commitment or a deadline.
