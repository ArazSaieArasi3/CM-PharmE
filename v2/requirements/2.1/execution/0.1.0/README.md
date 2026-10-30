# CM-PharmE 2.1 ORSD execution ledger — 0.1.0

This review ledger is the first versioned bridge from the **CM-PharmE 2.1 ORSD document 0.2.0** to the ontology candidate, test evidence and release work. It is an execution-planning artifact, not a replacement for the ORSD and not an ontology release.

- Canonical ORSD: [0.2.0](../../orsd/0.2.0/ORSD.md), [requirements.json](../../orsd/0.2.0/requirements.json), [acceptance-contracts.json](../../orsd/0.2.0/acceptance-contracts.json), [traceability.csv](../../orsd/0.2.0/traceability.csv).
- [83-row ledger](traceability-ledger.csv). Each row preserves its stable requirement ID, candidate priority, source and CQ pointers, independent expected oracles, model anchor names, comparison and acceptance states, execution references, known issue routing and next action.
- The ORSD's comparison baseline is model commit `09d60136a990d6602438be4085a4d407c9bd5c68`. The document was consolidated at `576c4afe6a30c2a71f0c05a9677ec70320609d0f`; the later commits in PR #305 through that point changed the ORSD, not the referenced model. Recheck a changed model before treating the comparison as current.
- The candidate lives on `v2/connectivity-audit-2-1-candidate` / [draft PR #305](https://github.com/ArazSaieArasi3/CM-PharmE/pull/305). The long-lived V2 integration line is `v2/research-program`. The stable V1 `main` is outside this candidate path.

## Measured starting state

| Distinct denominator | Recorded state | Interpretation |
|---|---:|---|
| Tracked ORSD rows | 83/83 joined by unique ID | 71 functional and 12 quality; not 83 semantically independent acceptances |
| Candidate priorities | 69 Must, 14 Should | Priorities await one author content review |
| Identifier availability | 49 native, 22 experimental-only, 12 quality-review | Vocabulary presence is not semantic coverage |
| Functional contract execution | 47 specified/not executed; 23 bounded prior replays; 1 fresh scoped query plus countermodel | Replays can share one CQ; do not count rows as independent tests |
| Quality contracts | 12 protocols specified | Quality review and execution remain open |
| Direct execution-issue routing | 27 rows | FR-01–03 → #316; four six-row domain modules → #311–#314 |
| Unrouted to a direct row-level execution issue | 56 rows | This is a planning gap, not a claim that evidence is absent everywhere |

The ledger joins by the stable requirement ID and checks every ORSD source ID against the registered source list. The row-level acceptance state remains `PENDING_SEMANTIC_REVIEW`; none of the 83 rows becomes author-approved through this ledger. The `model_anchor_names` column is the recorded candidate anchor list, not a verified native/OWL/SHACL semantic crosswalk. `execution_refs` preserve the ORSD's exact identifiers; use the ORSD verification registry to resolve them before claiming an observed result.

## Version and change contract

1. **ORSD 0.2.0** is a preserved document snapshot. Its remaining document action is the author review of purpose/scope, Must/Should priorities and any essential missing requirement; corrections go into a new version, then freeze ORSD 1.0.0. A document freeze does not require all ontology tests to have passed.
2. **Ledger 0.1.0** records the current mapping and explicit gaps. New executed evidence goes in a new versioned execution directory with exact source/model commits, fixed oracles and outcome links. Preserve old rows and IDs; record merged/deferred items instead of deleting history.
3. **Ontology 2.1 candidate** stays experimental while relation identity, cardinality, stereotype, Event/Situation and four-module decisions are open. A proposed interface cannot be counted as accepted ontology behavior.
4. **W6 database baseline** is the historical 2.0 reference. #307 verifies the P1 source-contract and PostgreSQL/PostGIS integration; [#317](https://github.com/ArazSaieArasi3/CM-PharmE/issues/317) inventories the 2.0→2.1 relational delta and migration contract. A schema change follows scientific disposition and explicit SQL↔SPARQL and provenance checks.
5. **2.1 release** is a later decision backed by a pinned ontology, passed scoped validation and human review, reproducible data/database evidence, diagrams, Wiki/Pages version navigation, changelog and an actual GitHub release. The paper has its own evidence and submission gate. No release is declared by this document.

## Ordered work toward 2.1

| Order | Gate / evidence | Existing work |
|---|---|---|
| 1 | Review and freeze ORSD 1.0.0 after the finite content review; run three-row independent acceptance slice | [#316](https://github.com/ArazSaieArasi3/CM-PharmE/issues/316) |
| 2 | Resolve the four purposeful modules, remaining P3/P4 semantics and native/OWL/SHACL alignment | [#311](https://github.com/ArazSaieArasi3/CM-PharmE/issues/311)–[#314](https://github.com/ArazSaieArasi3/CM-PharmE/issues/314), [#306](https://github.com/ArazSaieArasi3/CM-PharmE/issues/306) |
| 3 | Qualify the anti-pattern input/engine, adjudicate four source-policy discrepancies and run the applicable full candidate suite | [#310](https://github.com/ArazSaieArasi3/CM-PharmE/issues/310), [#315](https://github.com/ArazSaieArasi3/CM-PharmE/issues/315) |
| 4 | Verify the P1 source and DB CI, inventory relational delta, then implement and validate accepted 2.1 mapping changes | [#307](https://github.com/ArazSaieArasi3/CM-PharmE/issues/307), [#317](https://github.com/ArazSaieArasi3/CM-PharmE/issues/317) |
| 5 | Continue author review and real expert evidence; keep expert-dependent claims bounded while responses are absent | [#159](https://github.com/ArazSaieArasi3/CM-PharmE/issues/159), [#173](https://github.com/ArazSaieArasi3/CM-PharmE/issues/173), [#98](https://github.com/ArazSaieArasi3/CM-PharmE/issues/98) |
| 6 | Align representative task results, manuscript claims, diagrams, Wiki/Pages and reproducible package; approve and publish the versioned release | [#170](https://github.com/ArazSaieArasi3/CM-PharmE/issues/170), [#171](https://github.com/ArazSaieArasi3/CM-PharmE/issues/171), [#244](https://github.com/ArazSaieArasi3/CM-PharmE/issues/244), [#24](https://github.com/ArazSaieArasi3/CM-PharmE/issues/24) |

After #316, split remaining acceptance work into 1–3 run slices using the ledger's `SPECIFIED_NOT_EXECUTED` and candidate Must priority queues. No global percentage of semantic correctness follows from the issue-closure ratio.
