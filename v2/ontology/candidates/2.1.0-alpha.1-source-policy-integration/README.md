# Four-rule source-policy review bundle

Bundle **CMPE-SourcePolicyReview/0.1.0**; #315 P5e-5 technical integration.
The [contract](contract.json) and [integration decisions](decision.md) were frozen
at `a87639243f8924a447ebfc7fd062bc1654169309` before verifier implementation.

Four separately named profiles retain unchanged archived detector outputs and
independent candidate interpretation/review channels. [review-questions.csv](review-questions.csv)
lists the unresolved author/scientific questions. [review-state.json](review-state.json)
explicitly leaves all four scientific acceptances pending and every release/full-
candidate approval flag false. The bundle supplies review evidence, not acceptance.

| Rule | Candidate disposition | Critical limit |
|---|---|---|
| RelComp | Positive lower at explicitly bound shared end | Orientation normalization is candidate interpretation; engine-only states need review |
| WholeOver | Prose/formula >=2 precedence | Source diagrams say >2; original intent remains unresolved |
| RelRig | Review every admitted rigid frame's actual dependency direction | Archive and literal formula differ; Boolean declarations do not establish dependency facts |
| HomoFunc | Explicit part lower>=2 | Broader introduction omits the threshold; modern nature and inherited-part scope remain open |

The verifier pins source/decision/oracle/local/hosted/CI/applicability files, checks
original implementation/run/artifact provenance, compares every new case with its
own pre-implementation oracle, requires identical local/hosted evidence and shared
archive/compiler/JAR fingerprints, and recomputes authoritative input inventories.
It never invokes a converter or detector. Tampered results, a defaulted source
unknown, fabricated scientific acceptance and missing-rule coverage must be refused.

```sh
python v2/ontology/candidates/2.1.0-alpha.1-source-policy-integration/verify_integration.py
```

Expected bookkeeping: **62 synthetic case rows, 16 historical replay rows,
40 legacy refusal rows and 7 native admission rows**. Replays and graph variants
are not independent scientific samples or exhaustive detector-correctness evidence.
Native inventories are overlapping sets, not anti-pattern detections. Original IDs
are retained in the verification output so counts can be inspected.

Technical integration passed locally and in [hosted run 40472813955](https://github.com/ArazSaieArasi3/CM-PharmE/actions/runs/40472813955) at implementation `524c270d6eef737cf094ff97d9426b30ec8e0740`; **21/21 distinct workflows succeeded**. [local-results.json](local-results.json) and [hosted-results.json](hosted-results.json) agree exactly. [ci-evidence.json](ci-evidence.json) pins the implementation, job and artifact. The shared HomoFunc evidence artifact includes `integration-report.json` and a fresh `report.json` runtime replay; [hosted-homofunc-rerun.json](hosted-homofunc-rerun.json) retains that rerun, whose case/field/role/refusal/JAR evidence matches the original verified HomoFunc package. Artifact ID `12718727953`, digest `sha256:7c0a3aa7e17af0fcc572d0968e9b0707517600991e0f8e457675d88a82eb29c1`. The technical integration can
be completed with #315 still open for scientific/author acceptance. #310 full-
candidate adapter/execution and #306 scientific release review remain open.
PR #305 stays draft; no merge, automatic refactoring, final tag or release follows.

[Central four-rule disposition](adjudication-register.csv): **4/4 scoped implementations and technical integration verified; 0/4 author/scientific acceptances recorded**. The next work is scientific/source review and bounded native-fidelity resolution for #310/#306. These pending states are explicit, not inferred from passing CI.
