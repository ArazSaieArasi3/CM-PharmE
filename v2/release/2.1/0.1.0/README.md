# CM-PharmE 2.1 release decision and gate register — 0.1.0

The [six-row decision register](decision-register.csv) records delegated bounded choices, their evidence, negative conditions, current status and explicit later-review questions. It does not turn research observations into an author's or external expert's review. The target is ontology **2.1**; this directory is release-planning record **0.1.0**, not an ontology version.

| Gate | Current evidence | Status for GA 2.1.0 |
|---|---|---|
| ORSD | Document 0.2.0, 83 stable IDs; execution ledger 0.2.0 with three fresh bounded contracts | OPEN: author content freeze and remaining contract slices |
| Facility operation decision | [Native/OWL/SHACL overlay](../../../ontology/candidates/2.1.0-alpha.1-p3-facility-operation/README.md), 10/10 scoped fixtures, native parser, OWL RL/HermiT, zero-violation real ABox nonregression | SCOPED PASS; real operation/source evidence and broader P3 review open |
| Four purposeful modules | RM/PV/BA/DS preserved as experimental independent packages | OPEN: detailed contracts and author semantic review #311–#314 |
| Official full anti-patterns | Detector source-policy discrepancies documented; bounded tests exist | OPEN: #310/#315 full-candidate adjudication |
| Database/source | W6 2.0 historical; [2.1 delta inventory](../../../data/migrations/2.1/0.1.0/README.md) and conditional tests; P1 contract repaired | OPEN: #307 hosted PostgreSQL CI and #318–#321 executed 2.1 mapping |
| Human/expert and paper | Provenance and manuscript tasks tracked | OPEN: #159/#173/#98/#171 and claim review |
| Publication | PR #305 draft on V2 integration branch; no completed GA release evidence | OPEN: versioned diagrams, docs/Wiki, changelog, validation bundle, reviewed release/tag |

An optional `2.1.0-rc.1` **prerelease** can publish a research checkpoint only with an explicit experimental scope and these open gates. It is not a substitute for GA `2.1.0`. A final tag and release must be anchored to a pinned tested commit; no issue-closure ratio is a semantic quality measure. Do not merge #305 into the integration line or stable `main` while the listed blockers are open.
