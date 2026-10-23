"""Create an evidence-backed checkpoint from executed G3-3-C results."""
import json
import sys
from pathlib import Path

out = Path(sys.argv[1])
prior = Path(sys.argv[2])
data = json.loads((out / "validation-results.json").read_text())
b2 = json.loads((out / "replayed-b2-shacl.json").read_text())
f = json.loads((out / "replayed-g3-2e-f-graph-checks.json").read_text())
plan = json.loads(prior.read_text())
plan["as_of"] = "2026-10-09 Asia/Tehran"
assert data["full_candidate_shacl"]["pass_count"] == 11
assert data["owl_dl_reasoner"]["pass_count"] == 8
assert data["owl_rl_subproperty_entailment"]["pass"]
assert data["full_candidate_shacl"]["new_rejections_vs_baseline_shapes"] == 8
assert b2["counts"] == {"geo_passed":6,"relators_checked":19,
                         "repeatable_tuple_allowed":19,"missing_participant_rejected":19}
assert f["all_pass"] and f["pass_count"] == f["case_count"] == 23
plan["G3_3_C_status"] = "completed bounded integrated OWL DL and full-candidate SHACL synthetic validation; human and real-data gates remain"
plan["next_exact_turn"] = "G3-3-D: select a documented versioned real-source snapshot, map source rows to approved RDF terms with provenance, run complete candidate SHACL admission and quantify accepted/rejected coverage without silently forcing pending scientific links."
plan["remaining_bounded_turns"] = ["G3-3-D real-source migration", "G3-3-E connectivity and isolate evidence", "G3-3-F traceability and human review handoff"]
plan["G3_package_status"]["P4_semantic_integration"] = "in progress; native 99 class edges and 82 relation names aligned with G3-C OWL projection, SupplyCapacity typed bearer route open"
plan["G3_package_status"]["P5_ontouml_validation"] = "in progress; B3 bounded pattern prefilters and G3-C formal fixtures pass, official 20-pattern engine not run"
plan["G3_package_status"]["P6_formal_empirical_validation"] = "in progress; HermiT 8/8 and full-candidate pySHACL 11/11 synthetic, plus selected 44 pySHACL replay; actual source data pending"
(out / "g3-closure-plan.json").write_text(json.dumps(plan,indent=2,ensure_ascii=False)+"\n")
summary = {
    "as_of":"2026-10-09 Asia/Tehran",
    "package":"G3-3-C integrated validation",
    "formal_alignment":{"native_elements":523,"native_class_generalizations":99,"owl_direct_class_edges":99,
                        "named_classes":138,"datatypes":6,"native_and_owl_binary_relations":82,
                        "owl_redundant_direct_edge_removed":1,"owl_triples":1598},
    "executed_checks":{"full_candidate_pyshacl":11,"HermiT_consistency_and_coherence":8,
                       "OWL_RL_subproperty_entailment":1,"selected_geography_pyshacl_replay":6,
                       "focal_RepRel_pyshacl_replay":38,"adapted_RDFLib_graph_and_query_on_aligned_candidate":23,
                       "total_expected_outcome_checks":87,"failures":0},
    "comparative_behavior":"8 negative cases rejected by new full candidate shapes and accepted by the older baseline shapes",
    "known_gap":"SupplyCapacity without a typed bearer conforms to candidate SHACL; a HermiT consistency pass cannot prove bearer completeness under the open-world assumption.",
    "external_gates":["Official full 20-pattern anti-pattern detector unavailable/unrun",
                      "29 relation dispositions, 14 isolate connectors, 10 ImpAbs endpoint questions and 19 RepRel uniqueness policies need scientific review",
                      "Source-data mapping and migration not executed in G3-C"],
    "progress":{"closed_major_stages":2,"total_major_stages":5,"closed_major_stage_percent":40.0,
                "closed_G3_packages":2,"total_G3_packages":7,"closed_G3_package_percent":28.6,
                "remaining_bounded_turns":["G3-3-D","G3-3-E","G3-3-F"]},
    "release_status":"REVIEW_CANDIDATE_ONLY"
}
(out / "integrated-summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n")
readme = """# G3-3-C — integrated OWL DL and SHACL validation

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
"""
(out / "README.md").write_text(readme)
print(json.dumps(summary["executed_checks"]))
