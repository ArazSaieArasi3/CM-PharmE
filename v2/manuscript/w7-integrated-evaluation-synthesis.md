# CM-PharmE 2.0 — W7 Integrated Evaluation Synthesis for Manuscript Drafting

## Intended use
This note converts the repository evidence into manuscript-safe Results/Discussion wording. It is not a replacement for the final manuscript section and does not promote pending evidence to completed results.

## Evaluation architecture
CM-PharmE 2.0 was evaluated prospectively across separate evidence families covering structural quality, logical consistency, UFO/OntoUML commitments, competency questions, SHACL/data conformance, dataset mapping, semantic coverage, held-out generalizability, expert-review readiness, cross-representation consistency, analytics/AI eligibility, resilience scenarios and computational reproducibility. No composite ontology-quality score is used because the families answer different validity questions.

## Manuscript-ready results synthesis

### Structural, logical and conceptual evidence
The frozen ontology baseline passed the mandatory structural checks, preserved all eight protected Gate-D distinctions, and maintained complete registry traceability for the 87 conceptual elements and registered mappings. OWL 2 DL profile validation passed; HermiT and JFact both completed with zero unsatisfiable named CM-PharmE classes and exact agreement on 91 evaluated named-class subclass pairs. A separate project-native UFO/OntoUML pattern review executed 17 checks with zero blocking failures and preserved all protected distinctions. The latter is not presented as official OntoUML-tool certification, and documented extension-level formalization warnings are retained.

### Competency-question and constraint evidence
Eighteen competency questions were frozen before execution and produced all expected outcomes (8/8 positive and 10/10 negative). The negative queries are interpreted as regression/consistency checks under OWL open-world semantics rather than closed-world proof of absence. SHACL validation produced zero findings on the pristine reference fixture, and eight predefined controlled mutations were all detected. Because not every W5 NodeShape had populated focus nodes in the reference fixture, the result supports shape executability and selected defect sensitivity rather than universal data conformance.

### Mapping and coverage evidence
For the frozen P1/P2 source contracts, all 39 source-field decisions were explicitly classified; 36 of 38 in-scope fields were direct, derived or bounded mappings, two remained explicitly ambiguous, and no in-scope field was silently unmapped. The normalized source-semantic evaluation contained 97 requirements, of which 74 were exactly represented and 88 were exact-or-partial. Relation semantics showed 33/34 bounded representation. These results support data-grounded ontology evolution with explicit semantic-loss accounting, but they are not interpreted as global pharmaceutical-domain completeness.

### Held-out generalizability
Held-out evaluation used 51 requirements frozen before first-pass mapping and introduced no first-pass ontology changes. Overall, 38/51 requirements were exact-or-partial, with no conflict against the frozen Core identity distinctions. Coverage varied by source family: openFDA Drug Shortages and the selected national essential-medicine list transferred comparatively well, whereas ClinicalTrials.gov/AACT exposed substantial semantics better treated as pressure for a modular Clinical Trials Extension. The result therefore supports bounded cross-source/cross-jurisdiction reuse rather than unrestricted generalizability.

### Ontology–RDB–KG consistency
The reference ontology↔RDB↔KG realization passed the registered consistency checks: 36 mappings resolved, 14/14 class/cardinality checks and 10/10 relation/cardinality checks passed, 44/44 identity round-trip checks passed, the seven relational aggregate observations produced the expected 28 RDF metric nodes, and four frozen SQL↔SPARQL benchmark pairs returned equivalent results. These findings are bounded to the registered reference representation and do not establish universal lossless bidirectional equivalence between arbitrary relational and RDF representations.

### Analytics, AI and resilience
Seventeen analytics/AI candidates were audited against the predefined requirement that a defensible performance claim must have a task, data, baseline and metric. Only the cross-representation benchmark analytics task met the current evidence threshold, and no AI candidate was promoted to a novelty or performance claim. Separately, five frozen resilience scenarios produced all expected query outcomes with complete scenario provenance. The resilience evidence supports scenario-level representational adequacy only; predictive, causal, intervention-effectiveness and operational-resilience claims remain unsupported.

### Reproducibility
A clean GitHub-hosted rebuild executed 54/54 audit checks successfully. Two independent formal builds reproduced the frozen ontology fingerprint and byte-identical canonical artifacts, while two data/KG rebuilds reproduced the frozen KG fingerprint and byte-identical canonical artifacts after fresh PostgreSQL/PostGIS bootstrap. The executable W7 evidence families were regenerated under the captured environment. This establishes repository-level computational reproducibility, not third-party independent replication.

### Expert evaluation boundary
The prospective expert-review protocol, eligibility rules, two-stratum recruitment design, 23-item instrument, confidence ratings, red-flag rules, anonymization, analysis plan and participant-facing package are frozen and operationally ready. Readiness CI passed 27/27 checks. Real expert recruitment and empirical response analysis have not yet occurred, so no expert-validation result is reported in the current Results synthesis.

## Suggested evaluation table structure for the article
| Layer | Method | Key result | Claim boundary |
|---|---|---|---|
| Conceptual/structural | E1 + E3 | protected distinctions preserved; 0 blocking conceptual findings | project-native OntoUML review, not official certification |
| Logical | E2 | OWL 2 DL PASS; HermiT/JFact consistent on evaluated named-class hierarchy | datatype compatibility warning retained |
| Requirements | E4 | 18/18 frozen CQ outcomes | negative ASK is open-world bounded |
| Constraints | E5 | pristine conformance; 8/8 mutation detection | fixture/focus-node bounded |
| Data grounding | E6 + E7 | explicit mappings; 88/97 exact-or-partial semantic requirements | not global completeness |
| Generalizability | E8 | 38/51 held-out exact-or-partial; 0 Core identity conflicts | selected held-out sources only |
| Human evaluation | E9 | protocol/readiness complete | empirical expert results pending |
| Representation | E10 | registered mapping/invariant and 4/4 SQL↔SPARQL checks | not universal equivalence |
| Analytics/AI | E11 | one eligible benchmark task; 0 AI performance claims | unsupported candidates deferred |
| Resilience | E12 | 5/5 controlled scenario outcomes | representation, not prediction/causality |
| Reproducibility | E13 | 54/54 clean-rebuild checks; fingerprints reproduced | repository-level, not third-party replication |

## Discussion points that should remain explicit
1. V2 is empirically grounded in multiple source schemas and held-out evidence, but the current reference execution is not a full global ingestion pipeline.
2. The ontology is deliberately modular: new Clinical Trials semantics and selected Risk/Resilience refinements should be extensions rather than reasons to destabilize the Core.
3. The strongest current contribution is semantic traceability across conceptualization, formalization, source mappings, relational realization, KG projection and executable evaluation—not AI performance.
4. Negative findings are retained: source gaps, ambiguous ATC-name interpretation, incomplete extension formalization, limited shape activation, held-out clinical-trial gaps, and deferred application/AI performance.
5. Expert evidence should be inserted later as an additional independent family without rewriting the already frozen computational results.

## Gate-F readiness
The computational evidence is ready for claim-by-claim Gate-F adjudication. Use `v2/evaluation/results/w7-claim-evidence-traceability.csv` as the authoritative pre-gate claim matrix. The E9 dependency remains open and must not be counted as completed human validation.