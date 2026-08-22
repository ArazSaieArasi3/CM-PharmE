# CM-PharmE 2.0 Manuscript and Evidence Ledger

## Purpose
Keep manuscript claims synchronized with repository artifacts, datasets, ontology outputs, evaluation results, limitations and application evidence. No result is treated as completed unless repository evidence exists for the applicable gate.

## Current research state
- W0–W6: complete and gate-approved on the V2 research line.
- W7 computational evaluation: complete for E1–E8 and E10–E13.
- E9 expert evaluation: **protocol/readiness complete; real recruitment and responses pending**.
- W7 task state: **13/14 complete** until real E9 evidence is collected and analyzed.
- Next decision gate: Gate F claim-evidence sufficiency.

## Authoritative W7 synthesis artifacts
- `v2/research/w7/integrated-evaluation-evidence-matrix.md` — integrated family-level evidence synthesis.
- `v2/evaluation/results/w7-claim-evidence-traceability.csv` — authoritative pre-Gate-F 32-claim matrix.
- `v2/manuscript/w7-integrated-evaluation-synthesis.md` — manuscript-safe Results/Discussion synthesis.
- `v2/research/w7/e9-readiness-synthesis.md` — expert-evaluation readiness and future handoff.
- `v2/evaluation/results/w7-evidence-status.csv` — machine-readable family status register.

## Claim disposition summary before Gate F
The 32 tracked candidate claims are not treated uniformly:
- 15 are candidates for approval with normal scope wording;
- 12 require explicit bounded/qualified wording;
- 1 is supportable only for selected evaluated tasks;
- 1 is retained as a limitation;
- C-01 must be narrowed because no like-for-like quantitative V1 coverage denominator exists;
- two downstream performance claims remain deferred: geospatial-demonstrator effectiveness (W8) and real-world entity-resolution accuracy.

The detailed wording, evidence families, manuscript location and limitation for every claim are defined in `w7-claim-evidence-traceability.csv`.

## W7 evaluation status
| Family | Status | Principal evidence | Boundary |
|---|---|---|---|
| E1 Structural | PASS WITH WARNING | 87/87 conceptual registry; 36/36 mapping IRIs; 8/8 protected distinctions | structural traceability is not completeness |
| E2 Logical | Mandatory PASS / family WARN | OWL 2 DL PASS; HermiT/JFact 0 unsatisfiable named classes; 91/91 subclass-pair agreement | six project-native datatype compatibility warnings |
| E3 UFO/OntoUML | PASS WITH WARNING | 17 checks; 87/87 stereotype agreement; 8/8 protected distinctions | project-native review, not official tool certification |
| E4 CQs | PASS | 18/18 frozen outcomes; 8 positive + 10 negative | negative ASK results are open-world-bounded checks |
| E5 SHACL/data | PASS WITH WARNING | pristine conformance; 8/8 controlled mutations detected | fixture/focus-node bounded |
| E6 Mapping | PASS WITH WARNING | 39/39 decisions explicit; 36/38 in-scope direct/derived/bounded; 0 unmapped | strongest quantitative evidence for frozen P1/P2 contracts |
| E7 Coverage | PASS WITH WARNING | 74/97 exact; 88/97 exact-or-partial; relations 33/34 bounded | not global completeness or quantitative V1 superiority |
| E8 Held-out | PASS WITH WARNING | 38/51 exact-or-partial; 0 Core identity conflicts; no first-pass ontology changes | H2/H3 stronger than H1; selected-source generalizability only |
| E9 Experts | READINESS ONLY | frozen protocol + 23-item instrument + 27/27 readiness checks | **0 real expert responses; no expert-result claim** |
| E10 RDB/KG | PASS WITH WARNING | 36 mappings; 14/14 class; 10/10 relation; 44/44 identity; 4/4 SQL↔SPARQL | registered reference representation only |
| E11 Analytics/AI | PASS WITH DEFERRED AI | 17 candidates audited; only AN-08 benchmark-supported | 0 AI novelty/performance claims |
| E12 Resilience | PASS WITH WARNING | 5/5 frozen outcomes and provenance | scenario representation only; no prediction/causality/effectiveness |
| E13 Reproducibility | PASS WITH WARNING | 54/54 clean rebuild checks; ontology/KG fingerprints reproduced byte-identically | repository-level computational reproducibility, not third-party replication |

## Formal W5 baseline
- version `2.0.0-alpha.1`;
- 642 asserted triples;
- canonical SHA-256 `59ef47eeed732290736e60bfa1c6bf43a12d15df2f50cff931badb5938cc954a`;
- 87 Gate-D conceptual elements represented by 81 OWL classes + 6 declared datatypes;
- 52 object properties and 5 datatype properties;
- eight protected Gate-D distinctions;
- 11 SHACL NodeShapes.

E13 reproduced the frozen formal fingerprint in two clean rebuilds and regenerated the applicable logical/structural evidence.

## W6 representation baseline
- PostgreSQL/PostGIS reference realization;
- 36 registered ontology↔RDB mappings;
- 398-triple reference RDF ABox;
- canonical KG SHA-256 `6f93a00c2fa9a853e44db80b547d69f8033719948a03cf09b2b175dff5b40825`;
- 4/4 frozen SQL↔SPARQL benchmark pairs;
- provenance, identifier and auditable entity-match mechanics.

E10 and E13 support consistency/reproducibility for the registered reference realization. This does not imply universal lossless RDB↔RDF equivalence, production-scale ingestion or real-world entity-resolution accuracy.

## E9 expert-evaluation boundary
The prospective E9 design is frozen at commit `7eb6be02b0acbf77f391813f616ab483d0018b86`. A derivative participant package and readiness validator are operational. Final readiness CI run `32573278794` passed 27/27 checks; artifact `9475882128`, digest `sha256:87f05b69aa7bf43bb429d4e49af6239abffcae70f8c48f1447520a639edc3daf`.

Until real eligible participants are recruited and analyzed under the frozen plan, the manuscript may describe only the prospective method/readiness. It must not say that experts validated, confirmed, approved or rated CM-PharmE 2.0.

## Persistent limitations
1. No complete global Product→Supplier→Buyer→Shipment reconstruction claim.
2. The W6 reference execution uses deterministic schema-faithful fixtures; full-source ingestion is not implied.
3. Held-out generalizability is bounded to H1–H3 and reveals substantial Clinical Trials extension pressure.
4. No AI novelty/performance, GraphRAG utility, forecasting, shortage prediction or production application-effectiveness claim is supported.
5. Controlled resilience scenarios do not establish predictive or causal validity.
6. Project-native OntoUML checks are not official OntoUML-tool conformance.
7. Six project-native datatype compatibility warnings bound datatype-level multi-reasoner claims.
8. Selected extension formalization gaps remain for mediation, Mode bearers, recovery semantics and risk-treatment linkage.
9. E13 is clean computational reproducibility, not independent third-party replication.
10. Expert-result evidence remains pending.
11. Exact external-standard/risk-ontology conformance remains unclaimed without dedicated evaluation.
12. C-01 must not be expressed as a quantitative V1→V2 coverage improvement without a comparable V1 denominator.

## Manuscript integration map
1. Introduction — bounded novelty and V1→V2 qualitative delta.
2. Background/lineage — V1 and related prior work.
3. Research design/data protocol — multi-source evidence, admission and held-out discipline.
4. Concept discovery/traceability — E6/E7 data-grounded mapping and coverage.
5. UFO/OntoUML conceptualization — E3 and protected distinctions.
6. Formal ontology/constraints — E1/E2/E5 and W5 baseline.
7. Relational/KG realization — E10 and W6 reference architecture.
8. Evaluation — E1–E13 with E9 explicitly pending empirical human evidence.
9. Application demonstrators — only bounded W7 mechanics/scenarios until W8 evidence exists.
10. Discussion — generalizability, modular extension pressure, negative findings and claim boundaries.
11. Limitations — persistent limitations above.
12. Conclusion — contributions bounded to actual evidence.

## Next gate
Gate F must adjudicate each candidate claim as approved, bounded/narrowed, deferred or rejected. The current integrated matrix is ready for that decision. E9 remains a separate human-evidence dependency and must not be silently counted as complete.