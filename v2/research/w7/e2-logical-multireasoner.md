# W7-E2 — Logical and Multi-Reasoner Evaluation

## Status
**Mandatory logical gate: PASS**  
**Family interpretation: WARN (non-blocking reasoner compatibility warning)**

## Frozen protocol basis
W7-E2 was executed under the prospective protocol frozen before W7 result interpretation. Mandatory conditions were: OWL 2 DL profile PASS, no inconsistency, no unintended unsatisfiable named class, and agreement between HermiT and a second applicable reasoner where technically feasible.

## Execution evidence
Final successful workflow run: `32234016236`  
Artifact: `cm-pharme-v2-w7-e2-logical-evidence`  
Artifact ID: `9358275161`

The workflow rebuilt the frozen W5 ontology, verified ROBOT checksum/version, enforced OWL 2 DL, executed HermiT and JFact independently, captured runtimes/logs, and compared named CM-PharmE class hierarchy results.

## Results
| Check | HermiT | JFact | Result |
|---|---:|---:|---|
| Process exit | 0 | 0 | PASS |
| Unsatisfiable named CM-PharmE classes | 0 | 0 | PASS |
| Named internal classes evaluated | 81 | 81 | PASS |
| Named subclass pairs materialized | 91 | 91 | PASS |
| Named subclass hierarchy agreement | — | — | **91/91 agreement** |
| OWL 2 DL profile | PASS | same asserted input | PASS |

Runtime evidence from the recorded CI run:
- HermiT elapsed time: **1.97 s**, max RSS **157,776 KB**.
- JFact elapsed time: **1.20 s**, max RSS **143,672 KB**.

The asserted ontology remained in OWL 2 DL: `Ontology and imports closure in profile`.

## JFact compatibility warning
JFact emitted six datatype-factory ERROR log messages for the six project-native conceptual datatypes:
- `MeasureValue`
- `IdentifierValue`
- `ReportingPeriod`
- `GeospatialPosition`
- `Address`
- `TimeInterval`

JFact reported that these unknown datatypes were replaced internally with `rdfs:Literal`.

The W7-E2 evaluator inspected the frozen asserted graph and found **no semantic use of these project-native datatypes in datatype ranges/restrictions or other reasoning-bearing positions**; they are currently declared conceptual datatype placeholders. Therefore the warning does not invalidate the named-class hierarchy/unsatisfiability comparison performed in W7-E2. It is nevertheless retained as a real tool-compatibility finding and should be addressed before any future datatype-dependent reasoning claim.

## Harness correction log
The first E2 workflow attempt successfully executed both reasoners but the comparison harness expected ROBOT to create an unsatisfiable-class dump file even when the unsatisfiable set was empty. ROBOT omitted the empty dump, so the comparison step failed before producing its report. The harness was corrected to interpret an absent/empty unsatisfiable dump as an empty set while retaining the same frozen evaluation criteria. No protocol threshold or scientific criterion was changed after observing the reasoner outputs.

## Interpretation
The current ontology is logically processable under the selected OWL 2 DL profile. HermiT and JFact both completed successfully, reported no unsatisfiable named CM-PharmE classes, and materialized the same 91 named-class subclass pairs. This supports bounded logical-consistency/processability claims for the current axiom set.

This result does **not** establish semantic truth, domain completeness, correctness of every anonymous expression, standards conformance beyond the tested profile, or empirical validity. JFact's custom-datatype warning prevents an unqualified statement of complete cross-reasoner datatype compatibility.

## Next evidence family
**W7-E3 / V2-065 / issue #92 — UFO/OntoUML pattern and anti-pattern evaluation.**
