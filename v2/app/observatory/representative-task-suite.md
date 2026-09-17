# V2-083 Representative Task Suite — Frozen Evaluation Protocol

Status: **FROZEN BEFORE FINAL RESULT INTERPRETATION**
Work item: #170
Baseline: `v2/research-program` at `08927baf1c45149d9473395b7a01a2728b48f889`

## Evaluation boundary
This suite evaluates only the admitted CM-PharmE 2.0 W8 demonstrator/reference-fixture surfaces. PASS on these tasks does not establish universal usability, production readiness, predictive or causal validity, global pharmaceutical-market completeness, clinical effectiveness, or regulatory effectiveness. Failures and partial outcomes must be retained.

## Frozen task matrix

| ID | Surface | Task statement | Expected outcome | Required elements | Execution path | Success criterion | Provenance expectation |
|---|---|---|---|---|---|---|---|
| RT-01 | Actor/facility exploration | Retrieve the admitted actor/facility map representation and preserve its declared evidence boundary. | The reference actor/facility view is reproducible from admitted fixture data. | actor/facility fixture; map validator | existing actor/facility map validation path | validator passes and no completeness claim is introduced | source/provenance state remains visible or explicitly unavailable |
| RT-02 | Entity/relationship browser | Traverse a registered entity and at least one admitted visible relation. | Entity and relation are exposed only when registered/admitted. | browser fixture; allowed relation set | existing entity/relationship browser validation path | registered relationship is visible and unsupported relation is not manufactured | relation evidence retains source/target identifiers and provenance state |
| RT-03 | KG exploration | Explore a registered KG node and its visible admitted edges. | Node/edge exploration is deterministic over the fixture. | KG explorer fixture; allowed edges | existing KG explorer validation path | expected node and visible edge behavior reproduces | node/edge provenance is retained; unavailable provenance remains explicit |
| RT-04 | Analytics/query representation | Reproduce a frozen analytics/query-representation consistency case. | Paired representation remains consistent within the previously admitted reference case. | W8 analytics/query fixtures and validators | existing analytics/query validation path | declared frozen expectation passes; no arbitrary-query equivalence claim | result remains traceable to the frozen fixture/query evidence |
| RT-05 | Resilience/risk | Reproduce the bounded resilience/risk reference scenario without converting insufficient evidence into resilience. | Frozen scenario reproduces and insufficient evidence remains explicit. | resilience/risk fixture; W7-E12-derived evidence | existing resilience/risk validation path | scenario expectations pass and `INSUFFICIENT_EVIDENCE_NOT_RESILIENCE` boundary is preserved | scenario outputs retain their evidence/provenance references |
| RT-06 | Semantic/search assistance | Search for `product`. | `supported` with at least one result and evidence boundary. | `semantic_search.py`; KG explorer fixture | `search('product')` | status is `supported`; result exists; provenance state is admitted | every result exposes provenance state; registered visible-edge evidence carries provenance state |
| RT-07 | Semantic/search assistance | Search for `substance`. | `supported` with at least one result and evidence boundary. | same as RT-06 | `search('substance')` | same supported-result invariants as RT-06 | same provenance invariants as RT-06 |
| RT-08 | Semantic/search failure | Search for `definitely-not-in-fixture`. | `insufficient-evidence`; no result; absence is not ecosystem absence. | `semantic_search.py` | unmatched lexical lookup | explicit insufficient-evidence status and bounded absence statement | no provenance is fabricated for a nonexistent result |
| RT-09 | Semantic/search failure | Submit an empty search term. | `insufficient-evidence` with non-empty-query boundary. | `semantic_search.py` | empty lookup | explicit insufficient-evidence status | no evidence/provenance is fabricated |

## Interpretation protocol
For every task, the evaluation record must capture: observed result, PASS/PARTIAL/FAIL, exact evidence or validator reference, provenance behavior, and error/failure analysis. A task may not be silently removed after execution. Changes to task wording, expected outcomes, or success criteria after results are observed require a new version and an explicit rationale rather than rewriting this frozen protocol.

## Gate-G/manuscript mapping
RT-01..RT-05 test continuity of the existing W8 demonstrator surfaces. RT-06..RT-09 explicitly carry V2-082 into V2-083. Only results actually observed under this frozen suite may support manuscript-facing demonstrator claims; all claims remain bounded to these representative tasks and admitted data.
