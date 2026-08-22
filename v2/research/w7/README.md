# CM-PharmE 2.0 — W7 Prospective Multi-Family Evaluation

## Status
W7 starts from Gate-E-approved W6 baseline `59417e352c68585effc3056440fd1a815f6b92bc`. The protocol was frozen before result interpretation and evidence families remain analytically distinct; no composite quality score is used.

## Work register
- V2-062 / #89 — prospective protocol and metric registry — COMPLETE
- V2-063 / #90 — syntactic, structural and ontology quality — COMPLETE
- V2-064 / #91 — OWL profile and multi-reasoner logic — COMPLETE
- V2-065 / #92 — OntoUML pattern/anti-pattern review — COMPLETE
- V2-066 / #93 — positive and negative competency questions — COMPLETE
- V2-067 / #94 — SHACL/data conformance — COMPLETE
- V2-068 / #95 — dataset-to-ontology mapping quality — COMPLETE
- V2-069 / #96 — concept/relation coverage — COMPLETE
- V2-070 / #97 — held-out and cross-jurisdiction evaluation — COMPLETE
- V2-071 / #98 — prospective structured expert evaluation — **PROTOCOL/READINESS COMPLETE; REAL RESPONSES PENDING**
- V2-072 / #99 — ontology↔RDB↔KG semantic consistency — COMPLETE
- V2-073 / #100 — selected analytics/AI demonstrators — COMPLETE
- V2-074 / #101 — pharmaceutical resilience scenarios — COMPLETE
- V2-075 / #102 — independent rebuild/reproducibility audit — COMPLETE
- W7 evidence register / #103
- Gate F / #104 — evidence sufficiency for principal manuscript claims

## Integrated synthesis
Current authoritative synthesis artifacts:
- `integrated-evaluation-evidence-matrix.md`
- `e9-readiness-synthesis.md`
- `../../evaluation/results/w7-claim-evidence-traceability.csv`
- `../../manuscript/w7-integrated-evaluation-synthesis.md`
- `../../manuscript/evidence-ledger.md`

The computational/documentary evidence is consolidated and ready for Gate-F claim-by-claim adjudication. E9 remains open as a real-human-evidence dependency and must not be counted as completed expert validation.

## W7 family state
E1–E8 and E10–E13 are complete with their documented PASS/WARN/deferred boundaries. E9 has a frozen 23-item prospective instrument and operational participant package; final readiness CI run `32573278794` passed 27/27 checks, but no real expert response exists yet.

## Claim synthesis before Gate F
Across 32 candidate manuscript claims:
- 15 are candidates for normal scoped approval;
- 12 require explicit bounded wording;
- 1 is supportable only for selected evaluated tasks;
- 1 is an explicit limitation;
- C-01 must be narrowed because no comparable V1 quantitative coverage denominator exists;
- W8 demonstrator effectiveness and real-world entity-resolution accuracy remain deferred.

These are pre-Gate recommendations, not the Gate-F decision.

## Main evidence boundaries
- multi-source/data-grounded does not imply complete full-source ingestion;
- held-out evidence supports bounded transfer, not global completeness;
- project-native OntoUML checks are not official OntoUML-tool certification;
- SQL↔SPARQL equivalence is limited to frozen registered benchmarks;
- resilience evidence is scenario-level, not predictive/causal/operational validation;
- no AI performance/novelty claim is supported;
- clean CI rebuild is repository-level computational reproducibility, not third-party replication;
- E9 empirical human evidence remains pending.

## Main-branch boundary
All W7/V2 work remains on the V2 research line. `main` is not a W7 target.

## Next
Proceed to **Gate F / #104** for claim-evidence sufficiency adjudication while keeping E9/#98 open as a future human-evidence insertion point. After Gate F, continue to W8 application/observatory work and the Paper Track according to approved claim boundaries.