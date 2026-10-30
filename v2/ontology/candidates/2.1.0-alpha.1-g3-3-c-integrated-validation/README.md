# G3-3-C — integrated OWL DL and SHACL validation

This review candidate aligns the B2 native OntoUML overlay and the G3-2e-F formal candidate. One **previously approved redundant** direct `ListingResponsibleOrganizationRole → Organization` OWL superclass assertion was removed; the path via `ProductResponsibleLabelerRole → Organization` remains. No domain-only cardinality, identity key or bearer axiom was invented. The native direct hierarchy (99 edges), 138 OWL classes plus six native datatypes, and 82 relation/object-property names now match exactly.

| Executed check | Observed result | Scope |
| --- | ---: | --- |
| Full candidate SHACL graph, pySHACL 0.30.1 | 11/11 expected outcomes | Synthetic positive and negative ABox cases; eight new rejections relative to older baseline shapes. |
| HermiT via Owlready2 0.49 | 8/8 expected outcomes | Baseline and candidate TBox coherent with no unsatisfiable named classes; selected ABox consistency and explicit `owl:differentFrom` counterexamples. |
| OWL RL subproperty entailment | 1/1 | Product-specific active-substance property entails broad `hasActiveSubstance` on a named example. |
| Selected B2 geography rules (pySHACL) | 6/6 | Includes self-loop and two-step-cycle rejection. |
| Selected B2 focal RepRel shapes (pySHACL) | 38/38 | For 19 relators, repeat participant tuples conform and a missing mediated end fails; no scientific uniqueness rule follows. |
| Adapted G3-2e-F RDFLib graph/query regression | 23/23 | Executed on aligned G3-C files: graph checks, manually evaluated admission conditions and snapshot query; distinct from the actual pySHACL and HermiT checks above. |

Total **87/87 expected outcomes** across these bounded groups, with the exact cases, checksums, tool versions and baseline comparisons in [validation-results.json](validation-results.json), [selected B2 replay](replayed-b2-shacl.json) and [prior graph-check replay](replayed-g3-2e-f-graph-checks.json). The count is a suite result, not a 100% ontology-quality score or a substitute for empirical validation.

OWL and SHACL differ deliberately: OWL DL uses an open-world assumption and makes no unique-name assumption. Two IRIs for bearer individuals violate an exact-one restriction only when they are asserted distinct; SHACL rejects two explicit values in the graph. A missing active substance remains allowed. The `SupplyCapacity` object without a typed Organization/Facility bearer **passes** the current SHACL shapes, so the approved exactly-one-of-two bearer route remains an implementation blocker. The model's 10 ImpAbs questions, 19 RepRel tuple policies, 29 remaining relation dispositions and 14 isolate proposals still need scientific adjudication. The official complete 20-pattern anti-pattern detector has not run.

## Reproduce

From this directory, use Python 3.12 with `rdflib==7.6.0`, `pyshacl==0.30.1`, `owlready2==0.49`, `owlrl==7.6.2`, Java 17 and the adjacent prior packages:

```bash
python prepare_g3c.py ../2.1.0-alpha.1-g3-3-b2-focused-adjudication/ontouml-b2-review-overlay.json ../2.1.0-alpha.1-g3-2e-f-formal-alignment/active.ttl ../2.1.0-alpha.1-g3-2e-f-formal-alignment/constraints.ttl .
python run_g3c_validation.py active.ttl constraints.ttl ../2.1.0-alpha.1-g3d-candidate/active.ttl ../2.1.0-alpha.1-g3d-candidate/constraints.ttl ../2.1.0-alpha.1-g3-3-b2-focused-adjudication/ontouml-b2-review-overlay.json validation-results.json
python ../2.1.0-alpha.1-g3-3-b2-focused-adjudication/run_b2_shacl_fixtures.py constraints.ttl ../2.1.0-alpha.1-g3-3-b2-focused-adjudication/ontouml-b2-review-overlay.json ../2.1.0-alpha.1-g3-3-b-pattern-adjudication/pattern-prefilter.json replayed-b2-shacl.json
```

Run `python run_graph_regression.py ../2.1.0-alpha.1-g3d-candidate/active.ttl ../2.1.0-alpha.1-g3d-candidate/constraints.ttl active.ttl constraints.ttl ../2.1.0-alpha.1-g3-2e-f-formal-alignment/operates-snapshot.rq replayed-g3-2e-f-graph-checks.json` for the adapted 23 graph/query cases on this aligned candidate. Each test family records its own epistemic scope. HermiT receives a temporary RDF/XML serialization of the Turtle graph; this does not alter the committed OWL source.

## Gate and next step

G3-P4, P5 and P6 remain in progress: the bearer design, full anti-pattern run and real-source evidence are open. PR #305 stays draft and issue #306 open. G1/G2 are **2/5 major stages closed (40%)**; G3 is **2/7 named packages closed (28.6%)**. Three bounded turns remain: **G3-3-D real-source migration**, then E connectivity/isolate evidence, then F traceability and human-review handoff. Human scientific and detector gates may add work.

The exact next turn, **G3-3-D**, selects a documented, versioned source snapshot, maps actual records to approved RDF classes and relations with provenance, executes full candidate SHACL admission on the mapped data, and reports accepted, rejected and missing-value counts. It must keep unsupported relation proposals out of the released ontology.
