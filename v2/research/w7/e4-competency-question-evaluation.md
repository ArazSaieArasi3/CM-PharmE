# W7-E4 — Positive and Negative Competency-Question Evaluation

## Status
**PASS** under the frozen W7 protocol.

## Freeze discipline
The competency-question registry was frozen before first execution at commit `b96d7317aa1203a35c1282631a1cd19147f64007`:

- registry: `v2/evaluation/protocol/e4-competency-questions.json`
- primary issue: #93
- freeze support issue: #109
- evaluation scope: Gate-E schema-faithful fixture KG plus frozen asserted W5 ontology
- held-out H1–H3 used: **false**

The expected outcomes were derived from the already frozen Gate-E fixture baseline, not adjusted after CQ execution.

## Final CI evidence
GitHub Actions run `32237841582`: **SUCCESS**.
Evidence artifact: `cm-pharme-v2-w7-e4-cq-evidence`, artifact ID `9359621534`.

## Result summary
- frozen CQs executed: **18**
- total PASS: **18/18**
- positive CQs: **8/8 PASS**
- negative CQs: **10/10 PASS**
- failures rewritten/deleted after execution: **0**
- held-out sources used: **0**

### Positive CQ results
| CQ | Research question | Expected | Actual | Status |
|---|---|---:|---:|---|
| CQ-P01 | Medicinal Product → active Pharmaceutical Substance | 2 rows | 2 | PASS |
| CQ-P02 | Product Presentation → Medicinal Product | 2 rows | 2 | PASS |
| CQ-P03 | Facility → physical Geography | 2 rows | 2 | PASS |
| CQ-P04 | Dataset → Release → Source Record provenance traversal | 7 rows | 7 | PASS |
| CQ-P05 | Entity Match Assertion + confidence + canonical presentation | 2 rows | 2 | PASS |
| CQ-P06 | Presentation resolution through Identifier Assignment | 2 rows | 2 | PASS |
| CQ-P07 | Observation subject + time + geography + source provenance | 28 rows | 28 | PASS |
| CQ-P08 | Evidence Support links Source Record and Assertion | 7 rows | 7 | PASS |

### Negative CQ results
All ten frozen negative ASK queries returned the expected `false` result:

1. Facility is not hierarchically modeled as Organization.
2. Medicinal Product is not hierarchically modeled as Pharmaceutical Substance.
3. Medicinal Product is not hierarchically modeled as Medicinal Product Presentation.
4. Geographic Feature is not hierarchically modeled as Regulatory Jurisdiction.
5. Medicine Shortage Situation is not hierarchically modeled as Source Record.
6. Observation Result is not hierarchically modeled as Observation Activity.
7. Supply Capacity Observation Result is not hierarchically modeled as Supply Capacity.
8. No fixture reimbursement/utilisation Observation Result lacks Source Record provenance.
9. No fixture Evidence Support lacks either Source Record or Assertion.
10. No fixture Identifier Assignment lacks scheme, entity, or lexical value.

## Interpretation boundary
Negative CQs are **regression/consistency checks**, not closed-world proofs. Under OWL open-world semantics, failure to find an invalid pattern does not by itself prove that the pattern is impossible in the real pharmaceutical domain. Where explicit disjointness or other axioms exist, formal logical evidence is reported separately in W7-E2.

E4 is also bounded to the frozen schema-faithful fixture KG and asserted ontology. It does **not** establish:
- global domain completeness;
- real-world dataset quality;
- held-out generalizability;
- application effectiveness;
- universal answerability of all pharmaceutical ecosystem questions.

## Manuscript-safe claim
The manuscript may report that the frozen W7-E4 suite executed 18 predefined competency questions against the Gate-E reference KG/asserted ontology and achieved **18/18 expected outcomes (8 positive, 10 negative)**. The statement must explicitly identify the fixture-bounded evaluation scope and the open-world interpretation boundary for negative queries.

## Next
W7-E5 / V2-067 / #94 — SHACL and data-conformance evaluation.
