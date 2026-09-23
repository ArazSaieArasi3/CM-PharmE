# Evaluation Artifact Index

> **Page scope:** Cross-version  
> **Documentation maturity:** Stable-to-date / Evolving  
> **Authoritative sources:** V1 evaluation tree and V2 E1–E13 evaluation tree  
> **Last synchronized:** 2026-09-23  
> **Related issues:** #98, #103, #104, #208  
> **Evidence status:** Major evaluation artifacts indexed; live E9/Gate G dependencies remain visible  
> **Future refresh:** #212/#214  
> **Wiki baseline:** WB-2026.09.1 Candidate

## V1 evaluation artifacts

| Artifact family | Repository location |
|---|---|
| Evaluation overview | `docs/evaluations/index.md` |
| Structural audit | `docs/evaluations/v1.0.0-structural-audit.md` |
| Formal ontology audit | `docs/evaluations/b3-formal-ontology-audit.md` |
| Evaluation plan | `docs/evaluations/b4-evaluation-plan.md` |
| Executed evaluation matrix | `docs/evaluations/b4-evaluation-matrix.md` |
| Final evaluation report | `docs/evaluations/b4-final-evaluation.md` |
| Semantic finding disposition | `docs/evaluations/b4-10-semantic-finding-disposition.md` |
| Machine-readable CQ/anti-pattern/scenario evidence | `evaluation/` |
| Build/validation/release readiness | `docs/engineering/` |

See [[V1 Evaluation Index]].

## V2 evaluation artifacts

| Family | Primary protocol/evidence area | Current state |
|---|---|---|
| E1 Structural | `v2/research/w7/e1-structural-quality.md` + executable tooling | PASS WITH WARNING |
| E2 Logical | `v2/research/w7/e2-logical-multireasoner.md` | mandatory PASS / family warning |
| E3 UFO/OntoUML | `v2/research/w7/e3-ontouml-pattern-review.md` | PASS WITH WARNING |
| E4 CQs | `v2/evaluation/protocol/e4-competency-questions.json` + results/tooling | PASS |
| E5 SHACL | `v2/evaluation/protocol/e5-*` + tooling | PASS WITH WARNING |
| E6 Mapping | `v2/evaluation/protocol/e6-mapping-quality-rules.json` + results | PASS WITH WARNING |
| E7 Coverage | `v2/evaluation/protocol/e7-*` | PASS WITH WARNING |
| E8 Held-out | `v2/evaluation/heldout/`, `v2/evaluation/results/e8-*` | PASS WITH WARNING |
| E9 Expert | `v2/evaluation/protocol/e9-*`, participant package | READINESS ONLY; 0 real responses |
| E10 Representation | `v2/research/w7/e10-ontology-rdb-kg-semantic-consistency.md` | PASS WITH WARNING |
| E11 Analytics/AI | `v2/research/w7/e11-analytics-ai-evaluation.md` | PASS WITH DEFERRED AI |
| E12 Resilience | `v2/research/w7/e12-resilience-scenario-evaluation.md` | PASS WITH WARNING |
| E13 Reproducibility | `v2/research/w7/e13-reproducibility-independent-rebuild.md` | PASS WITH WARNING |

## Cross-family synthesis

- `v2/research/w7/integrated-evaluation-evidence-matrix.md`
- `v2/evaluation/results/w7-evidence-status.csv`
- `v2/evaluation/results/w7-claim-evidence-traceability.csv`
- `v2/research/w7/gate-f-claim-sufficiency-decision.md`

## Application/task evaluation

- `v2/app/observatory/representative-task-suite.md`
- `v2/app/observatory/representative-task-results.md`
- #170 remains open for completion and Gate G mapping.

## Reading rule

A protocol is not a result; a result is not a universal claim; a PASS label must always be interpreted with its evidence boundary.

## Related pages

[[Evaluation and Assurance]] · [[V2 Evaluation E1-E13]] · [[Gate and Claim Dispositions]] · [[Reproducibility Guide]]
