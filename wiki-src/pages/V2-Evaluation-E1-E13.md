# V2 Evaluation E1-E13

> **Page scope:** V2  
> **Documentation maturity:** Stable-to-date / Evolving  
> **Authoritative source:** V2 W7 evaluation artifacts and live E9 status  
> **Last synchronized:** 2026-09-23  
> **Last synchronized ref:** `1226b0a5484f8f5d3a8d214e0d0f52f066b88999`  
> **Related issues/PRs:** #21, #98, #103, #104  
> **Evidence status:** E1–E8 and E10–E13 complete; E9 readiness only  
> **Future refresh:** #214 when E9/final release is dispositioned  
> **Wiki baseline:** WB-2026.09.1

## Evaluation matrix

| Family | Focus | Current supported state |
|---|---|---|
| E1 | Structural/ontology quality | PASS WITH WARNING |
| E2 | OWL 2 DL / multi-reasoner | Mandatory PASS; family warning retained |
| E3 | UFO/OntoUML commitments | PASS WITH WARNING |
| E4 | Competency questions | PASS — 18/18 |
| E5 | SHACL/data conformance | PASS WITH WARNING; 8/8 mutations detected |
| E6 | Dataset→ontology mapping | PASS WITH WARNING; 39/39 decisions explicit |
| E7 | Source semantic coverage | PASS WITH WARNING |
| E8 | Held-out generalizability | PASS WITH WARNING |
| E9 | Prospective expert review | **READINESS ONLY — 0 real responses** |
| E10 | Ontology↔RDB↔KG consistency | PASS WITH WARNING |
| E11 | Analytics/AI eligibility | PASS WITH DEFERRED AI |
| E12 | Resilience scenarios | PASS WITH WARNING |
| E13 | Reproducibility | PASS WITH WARNING |

## Important quantitative evidence

- E2: HermiT/JFact 91/91 named subclass-pair agreement; 0 unsatisfiable named classes.
- E4: 18/18 frozen CQ outcomes.
- E5: pristine profiles 0 findings; 8/8 controlled mutations detected.
- E6: 39/39 mapping decisions explicit; 36/38 in-scope direct/derived/bounded; 2 ambiguous.
- E7: 74/97 exact; 88/97 exact-or-partial.
- E8: 23/51 exact; 38/51 exact-or-partial; 0 first-pass Core identity conflicts.
- E10: 36 mappings; 14/14 class, 10/10 relation, 44/44 identity checks; 4/4 SQL↔SPARQL.
- E11: 17 candidates audited; only AN-08 benchmark-supported; no AI performance/novelty claims.
- E12: 5/5 frozen scenario outcomes/provenance.
- E13: 54/54 clean rebuild checks and reproduced ontology/KG fingerprints.

## E9 boundary

The protocol/instrument is frozen and readiness automation passes 27/27 checks. The instrument has 23 items.

There are **0 real expert responses**. No text may say experts validated, confirmed, approved or rated V2 until real eligible responses are collected/analyzed under the frozen plan.

## Gate F

Gate F approves progression with bounded claim dispositions. It does not convert E9 readiness into human-result evidence.

## Evidence

- [Integrated evaluation matrix](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w7/integrated-evaluation-evidence-matrix.md)
- [Gate F decision](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w7/gate-f-claim-sufficiency-decision.md)
- [Evidence status register](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/evaluation/results/w7-evidence-status.csv)
- [E9 protocol](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w7/e9-expert-evaluation-protocol.md)
