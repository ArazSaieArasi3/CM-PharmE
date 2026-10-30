"""Evidence-ranked RepRel questions and human-review summary for G3-3-B3."""
import json
import sys
from pathlib import Path

BASE = Path(__file__).parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else BASE / "g3-3-b3-pattern-closure"
DOCKET = Path(sys.argv[2]) if len(sys.argv) > 2 else BASE / "g3-3-b2-focused-adjudication" / "reprel-19-decision-docket.json"
CLOSURE = Path(sys.argv[3]) if len(sys.argv) > 3 else BASE / "g3-3-b2-focused-adjudication" / "g3-closure-plan.json"
structural = json.loads((OUT / "structural-results.json").read_text())
docket = json.loads(DOCKET.read_text())

explicit_context = {
    "EstablishmentRegistration": "registrationJurisdiction",
    "MarketListing": "listingJurisdiction",
    "RegulatoryAuthorization": "authorizationJurisdiction",
    "EvidenceSupport": "evidenceRecord",
}
rows = []
for d in docket["rows"]:
    name = d["relator"]
    if name in explicit_context:
        tier = "A_explicit_context_reference"
        evidence = (f"Native typed association {explicit_context[name]} exists; its cardinality is unfilled. "
                    "This is a potential discriminator, not a proven identity key.")
    elif name == "SupplyDependency":
        tier = "B_indirect_context_references"
        evidence = ("disruptionAffectsDependency and riskAssessmentConcernsDependency refer to this relator; "
                    "neither is a confirmed identity discriminator.")
    else:
        tier = "C_no_extra_typed_reference"
        evidence = "No additional typed relation or attribute proves the proposed scope/time discriminator in the native model."
    missing = []
    if name == "IdentifierAssignment":
        missing.append("lexical identifier value is not a native attribute in this overlay")
    missing.append("effective interval and uniqueness scope have not been established in the native model")
    rows.append({
        "relator": name,
        "tier": tier,
        "mediations": [m["name"] for m in d["mediations"]],
        "model_evidence": evidence,
        "untested_hypothesis": d["candidate_distinctness_basis_to_verify"],
        "known_gap": missing,
        "fixture_evidence": "Selected B2 focal SHACL accepts two same-party-tuple instances and rejects a missing end; no uniqueness constraint tested.",
        "recommended_interim_rule": "Preserve repeatability and required mediation ends; do not set blanket max 1 or add tuple uniqueness.",
        "author_question": ("Can two concurrent instances mediate exactly the same participants? If yes, which recorded key/scope/version differentiates them? "
                            "If no, which source rule and valid-time boundaries establish scoped uniqueness?"),
        "decision_options": ["allow repeats with a documented discriminator", "enforce scoped concurrent uniqueness with approved fields/interval", "defer pending source evidence"],
        "disposition": "PENDING_SCIENTIFIC_ADJUDICATION"
    })
assert len(rows) == 19
counts = {tier: sum(r["tier"] == tier for r in rows) for tier in
          ["A_explicit_context_reference", "B_indirect_context_references", "C_no_extra_typed_reference"]}
assert counts == {"A_explicit_context_reference": 4,
                  "B_indirect_context_references": 1,
                  "C_no_extra_typed_reference": 14}
packet = {"scope": "19 structural RepRel triggers, B2 selected synthetic fixtures, and native B2 review overlay",
          "evidence_ranking": counts,
          "provisional_policy": "Keep mediation cardinalities; no global tuple uniqueness; author to decide contextual and temporal identity.",
          "warning": "Typed reference existence and synthetic SHACL acceptance do not establish business-key uniqueness or validity dates.",
          "rows": rows,
          "official_detector_status": "NOT_RUN", "author_signoff": "PENDING"}
(OUT / "reprel-evidence-ranked-decisions.json").write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n")

lines = ["# G3-3-B3 — bounded pattern closure and scientific decision packet", "",
         "Input: G3-3-B2 native review overlay (523 elements), B2 synthetic fixtures and the G3-3-B catalogue inventory. This is a **review packet**, not a full anti-pattern clearance.", "",
         "## Reproduced counts", "",
         "| Check | Result | Meaning |", "| --- | ---: | --- |",
         f"| ImpAbs | {structural['ImpAbs']['trigger_end_count']} endpoints / {structural['ImpAbs']['distinct_relations']} relations | All require domain review of subtype-specific bounds; none is an automatic violation. |",
         f"| RelComp | {structural['RelComp']['known_cardinality_candidate_pairs']} known-cardinality pairs; {structural['RelComp']['unknown_A_target_cardinality_structural_pairs']} conditional pairs | The conditional A associations are `withinCountry` and `withinRegion`, whose target bounds are null; no assertion of absence follows. |",
         f"| RelOver | {structural['RelOver']['relators_with_potential_overlap']} relators with potentially overlapping mediated types; {structural['RelOver']['known_upper_sum_gt_two']} prove upper sum >2; {structural['RelOver']['unknown_upper_sum']} has an unknown bound | Four have known sum 2; `EvidenceSupport` has unknown `evidenceRecord` upper and remains conditional. |",
         f"| RepRel | {len(rows)} decision rows | 4 with typed extra context, 1 with indirect reference, 14 with no extra typed reference; none has an approved tuple/time key. |",
         "", "There are 82 native binary relations; 71 have both typed endpoints, and 33 have at least one unknown cardinality. Counts use a conservative local scanner, not the official detector. `structural-results.json` contains the exact pairs and subtype lists.", "",
         "## ImpAbs: 10 endpoint decisions", "",
         "The official criterion is an association end with upper ≥2 and a connected class with ≥2 subtypes. It asks whether subtype-specific multiplicities or meta-properties are needed. The current broad admission shapes check class membership, not subtype-specific limits. `classificationEntity` and `classificationEntry` each have a contextual specializing relation, but those native relation ends have no cardinality, so they do not close the two questions. Do not infer that every subtype requires a link or add a blanket bound.", "",
         "| Relation | Triggered ends | Current recommendation |", "| --- | --- | --- |"]
by_rel = {}
for r in structural["ImpAbs"]["rows"]:
    by_rel.setdefault(r["relation"], []).append(r["end"])
for name, ends in by_rel.items():
    note = "Review contextual subset and fill only source-supported bounds." if name.startswith("classification") else "Retain broad typing; collect subtype-specific positive and negative instances before adding bounds."
    lines.append(f"| `{name}` | {', '.join(ends)} | {note} |")
lines += ["", "## RepRel: ranked questions", "",
          "The typed context in rank A is evidence of a possible discriminator, not a unique key. Rank B contains reverse references that do not establish identity. Rank C requires source data or author input. For all 19, ask whether the same participant tuple can recur concurrently, under different jurisdiction/scope, or in a later interval. The prior selected SHACL fixture accepted duplicates and rejected missing mediation ends; it did not test time. Preserve repeatability until the rule is approved.", "",
          "| Rank | Relators | Evidence and action |", "| --- | --- | --- |",
          "| A (4) | EstablishmentRegistration, MarketListing, RegulatoryAuthorization, EvidenceSupport | Inspect typed jurisdiction or evidence-record reference; establish cardinality, scope and temporal identity. |",
          "| B (1) | SupplyDependency | Check whether disruption and risk-assessment references are merely downstream context. |",
          "| C (14) | All remaining rows in `reprel-evidence-ranked-decisions.json` | Find a source-backed discriminator; a proposed lexical value or period does not yet exist in the native model. |", "",
          "## Semantic disposition and gate", "",
          "1. Request concrete positive/rejecting source examples for each ImpAbs subtype family, then constrain only the approved cases in OntoUML and SHACL/OCL.",
          "2. Fill the geography relation bounds from domain evidence; re-run RelComp. Resolve the `EvidenceSupport/evidenceRecord` mediated-end bound and potential dual role; re-run RelOver.",
          "3. Author-adjudicate the 19 RepRel policies; encode any accepted current uniqueness rule with explicit scope and temporal fields and both acceptance/rejection fixtures.",
          "4. Run a compatible official full 20-pattern detector with reproducible model import and inspect every finding. The archived 13 class rules, schema/parser, and these structural scans cannot certify catalogue-wide absence of anti-patterns.", "",
          "No new ontology axiom was committed in B3: the necessary cardinalities and domain keys are scientifically unconfirmed. G3-P5 remains in progress. The 29 relation dispositions, 14 isolate proposals and the `SupplyCapacity` typed bearer route also remain open.", "",
          "## Reproduction and next turn", "",
          "From this directory using Python 3, run `python scan_b3.py ../2.1.0-alpha.1-g3-3-b2-focused-adjudication/ontouml-b2-review-overlay.json .` and `python build_b3_decisions.py . ../2.1.0-alpha.1-g3-3-b2-focused-adjudication/reprel-19-decision-docket.json ../2.1.0-alpha.1-g3-3-b2-focused-adjudication/g3-closure-plan.json`; compare the produced JSON and assertions. The next bounded turn is **G3-3-C: integrated OWL DL and pySHACL validation** of the currently approved candidate, with positive/negative fixtures and reasoner limits explicit. Keep B3's scientific and full-detector gates in the G3 closure list.", "",
          "G1/G2 are closed (2/5 = 40% by closed-stage count). G3 has P1/P2 closed (2/7 = 28.6% by package count); P3/P4/P5 are in progress, P6/P7 pending. After B3, bounded turns C, D, E, F remain, plus human decisions and conditional detector work.", "",
          "Definitions: [ImpAbs](https://ontouml.readthedocs.io/en/latest/anti-patterns/ImpAbs/index.html), [RelComp](https://ontouml.readthedocs.io/en/latest/anti-patterns/RelComp/index.html), [RelOver](https://ontouml.readthedocs.io/en/latest/anti-patterns/RelOver/index.html), [RepRel](https://ontouml.readthedocs.io/en/latest/anti-patterns/RepRel/index.html).", ""]
(OUT / "README.md").write_text("\n".join(lines))
closure = json.loads(CLOSURE.read_text())
closure["G3_3_B2_status"] = "completed"
closure["G3_3_B3_status"] = "completed bounded structural and evidence-ranking packet; author and official detector gates remain"
closure["next_exact_turn"] = "G3-3-C integrated OWL DL and pySHACL validation of approved candidate, positive/negative regressions and explicit reasoner limits"
closure["remaining_bounded_turns"] = ["G3-3-C integrated OWL DL and SHACL validation", "G3-3-D real-source migration", "G3-3-E connectivity and isolate evidence", "G3-3-F traceability and human review handoff"]
closure["G3_package_status"]["P3_scientific_adjudication"] = "in progress; 29 relation rows, 14 isolate proposals, 10 ImpAbs endpoint questions, 19 RepRel tuple policies pending"
closure["G3_package_status"]["P5_ontouml_validation"] = "in progress; B3 bounded RelComp/RelOver/ImpAbs prefilters done; official full 20-pattern engine not run"
(OUT / "g3-closure-plan.json").write_text(json.dumps(closure, indent=2, ensure_ascii=False) + "\n")
print(counts)
