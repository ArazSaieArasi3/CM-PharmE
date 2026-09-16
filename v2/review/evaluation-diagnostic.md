# CM-PharmE 2.0 — HORP Evaluation Diagnostic Report (E1–E13)

Status: **review projection — pending author review**  
Review candidate: `RC-V2-HORP-01`  
Source authority: W7 evaluation artifacts and `v2/evaluation/results/w7-evidence-status.csv`

This report translates the existing W7 evaluation evidence into a human-review surface. It does **not** replace the W7 evidence, upgrade warnings to passes, infer expert validation, or authorize semantic changes.

## Diagnostic matrix

| Family | Repository status | What the evidence supports | HORP warning / review focus | Human disposition |
|---|---|---|---|---|
| E1 Structural quality | PASS_WITH_WARNING | Mandatory structural checks pass; 87/87 conceptual registry; protected distinctions preserved | Annotation labels are 87/144 (60.42%); explicit domain 53/57 and range 42/57. Structural PASS is not completeness. | Pending |
| E2 Logical multi-reasoner | WARN | OWL 2 DL; HermiT/JFact exit 0; 0 unsatisfiable named classes; 91/91 named subclass pairs agree | JFact normalizes six project-native conceptual datatypes to `rdfs:Literal`; datatype compatibility claim remains bounded. | Pending |
| E3 OntoUML pattern review | PASS_WITH_WARNING | 17 executable project-native checks; stereotype/formal agreement 87/87; role grounding 10/10; protected distinctions 8/8 | Not official OntoUML-tool conformance. Mediation/dependence/bearer warnings remain for RegulatoryOversight, StrategicPartnershipAgreement, Vulnerability and EnterpriseCapability. | Pending |
| E4 Competency questions | PASS | 18/18 frozen CQ outcomes; positive 8/8; negative 10/10 | Fixture-bounded; negative ASK outcomes are regression/consistency checks under open-world semantics, not closed-world negation proof. | Pending |
| E5 SHACL data conformance | PASS_WITH_WARNING | Mandatory fixture conformance and integrity checks pass; 8/8 controlled mutations detected | Fixture-bounded; only 3/11 W5 NodeShapes had direct focus nodes. No full real/held-out data conformance claim. | Pending |
| E6 Dataset–ontology mapping | PASS_WITH_WARNING | 39/39 field decisions explicit; 36/38 direct/derived/bounded; critical fields have no ambiguous/unmapped decisions | `atc_name` remains ambiguous for substance interpretation; 16 decisions bounded; P3/P4/P5 not quantitatively field-mapped. | Pending |
| E7 Concept/relation coverage | PASS_WITH_WARNING | 97 source-semantic requirements; 88/97 represented-or-partial; 54/87 Gate-D terms evidenced | 14 partial and 9 not represented findings remain. Coverage is not global domain completeness. | Pending |
| E8 Held-out generalizability | PASS_WITH_WARNING | 51 held-out requirements; 38/51 exact-or-partial; 0 first-pass ontology changes; no Gate-D/Core identity conflict | H1 clinical-trial semantics create modular-extension pressure. Evidence supports bounded, not global, generalizability. | Pending |
| E9 Expert evaluation | LAUNCH_READY_AWAITING_COLLECTION | Prospective protocol frozen; 23-item instrument; readiness 27/27 | **Human/external evidence gate:** 0 real responses. No expert-validation/result claim is admissible until eligible responses are collected and analyzed. | Pending / gated |
| E10 Ontology–RDB–KG consistency | PASS_WITH_WARNING | 36 mappings resolve; class/relation/cardinality and identity round-trip checks pass; SQL↔SPARQL benchmarks 4/4 | Ten explicit non-direct mapping exceptions remain; evidence is bounded to registered mappings/reference fixture/frozen benchmarks. | Pending |
| E11 Analytics/AI evaluation | PASS_WITH_DEFERRED_AI | 17 candidates audited; AN-08 benchmark-supported; 4/4 SQL↔SPARQL | 16 candidates deferred; **no AI novelty/performance/application-utility claim is supported**. | Pending |
| E12 Resilience scenarios | PASS_WITH_WARNING | Five frozen scenarios; query/provenance checks complete; sensitivity mechanism demonstrated | Recovery semantics, RiskTreatmentPlan→RiskTreatmentActivity and Vulnerability bearer relation remain gaps; no predictive/causal/effectiveness claim. | Pending |
| E13 Reproducibility | PASS_WITH_WARNING | Clean CI rebuild; 54/54 audit checks; reproducible ontology/KG fingerprints; computable W7 evidence regenerated | Repository-level GitHub-hosted reproducibility is not third-party independent replication; E9 human evidence excluded. | Pending |

## Cross-family diagnostic synthesis

### Evidence strengths
1. **Structural and logical baseline is stable:** E1–E4 provide strong bounded evidence for registry integrity, OWL 2 DL reasoning, project-native OntoUML pattern checks and frozen competency questions.
2. **Data/semantic traceability is operational:** E5–E7 demonstrate executable conformance and explicit dataset/source-semantic mappings, while preserving known coverage gaps.
3. **Generalizability is tested rather than assumed:** E8 preserves first-pass held-out gaps and extension pressure without silently modifying the ontology.
4. **Cross-representation consistency is executable:** E10 provides bounded ontology↔RDB↔KG checks and frozen SQL↔SPARQL benchmarks.
5. **Claim discipline is explicit:** E11–E13 retain deferred AI claims, scenario limitations and the distinction between repository reproducibility and independent replication.

### Highest-priority human-review questions
1. **E9 gate:** when and how will real eligible expert responses be collected, analyzed and accepted? Until then, expert-validation claims remain prohibited.
2. **Formalization warnings:** should the E3 mediation, role-dependence and bearer-property warnings become semantic-change findings, documentation findings, or accepted bounded limitations?
3. **Coverage boundary:** are E7's 14 partial + 9 not-represented requirements acceptable for the intended CM-PharmE 2.0 scope?
4. **Held-out extension pressure:** should H1 clinical-trial semantics remain modular extension pressure or trigger a future scoped extension decision?
5. **Mapping ambiguity:** how should `atc_name` and the bounded/non-direct mappings be treated in the final evidence narrative?
6. **Claim boundary:** confirm that deferred AI, predictive/causal resilience, universal lossless mapping, global completeness and independent-replication claims remain out of scope unless new evidence is produced.

## HORP interpretation

- Repository statuses are evidence-family outcomes, **not semantic approval dispositions**.
- `PASS_WITH_WARNING` and `WARN` entries must retain their warning boundaries in any manuscript/release synthesis.
- E9 is an external/human-evidence dependency and cannot be autonomously promoted.
- Findings raised by the author should enter the structured HRF register before any ontology semantic change.
- All rows remain `Pending` for author HORP disposition.

## Source anchors

- `v2/evaluation/results/w7-evidence-status.csv`
- `v2/research/w7/e1-structural-quality.md` through `e13-reproducibility-independent-rebuild.md`
- `v2/research/w7/integrated-evaluation-evidence-matrix.md`
- `v2/evaluation/results/w7-claim-evidence-traceability.csv`
- `v2/manuscript/w7-integrated-evaluation-synthesis.md`
- `v2/manuscript/evidence-ledger.md`

## Next HORP step

Instantiate the structured **Human Review Finding (HRF) register and re-review workflow**. Findings should preserve source surface, evidence anchor, finding type/severity, proposed action, human disposition, implementation link, verification evidence and re-review status. No semantic finding is accepted merely because this diagnostic report identifies a review question.
