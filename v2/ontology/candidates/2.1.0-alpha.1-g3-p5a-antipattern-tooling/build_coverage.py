#!/usr/bin/env python3
"""Compare bounded structural triggers and qualify archived detector compatibility."""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
OLED = Path(sys.argv[1])
HEAD = "42b926f6c2859dc87e49a96b8482eae28d02e7d5"
names = [x["name"] for x in json.loads((BASE / "g3-3-a-official-checks/anti-pattern-coverage.json").read_text())["entries"]]
assert len(names) == len(set(names)) == 20
native_path = BASE / "g3-p4a-supply-capacity/ontouml.json"
native = json.loads(native_path.read_text())
elements = {x["id"]: x for x in native["elements"]}
domains = {c["id"]: d["domain"] for d in json.loads(
    (BASE / "g3-3-f-review-handoff/domain-inventory.json").read_text())["domains"]
    for c in d["concepts"]}
assert set(domains) == {x["id"] for x in native["elements"] if x["type"] == "Class"}
prefix = OLED / "br.ufes.inf.nemo.antipattern/src/br/ufes/inf/nemo/antipattern"
processor = prefix / "MultipleModelProcesser.java"
source = processor.read_text()
registered = re.findall(r"apList\.add\(new (\w+Antipattern)\(parser\)\)", source)
assert len(registered) == 21 and len(set(registered)) == 21
assert "AssCycAntipattern" in registered
implementations = {p.name.removesuffix("Antipattern.java"): str(p.relative_to(OLED))
                   for p in prefix.rglob("*Antipattern.java")}
assert all(x.removesuffix("Antipattern") in implementations for x in registered)
current = json.loads((HERE / "current-prefilter.json").read_text())
prior = json.loads((HERE / "b2-prefilter-comparison.json").read_text())
structural = json.loads((HERE / "structural-results.json").read_text())
assert current["native_elements"] == 536 and prior["native_elements"] == 523
assert current["counts"] == prior["counts"]

key = {"BinOver": "BinOver_definite", "DecInt": "DecInt_multiple_concrete_parents",
       "DepPhase": "DepPhase", "FreeRole": "FreeRole_direct_path", "GSRig": "GSRig",
       "MixIden": "MixIden_precondition", "MixRig": "MixRig",
       "MultDep": "MultDep_direct", "RelRig": "RelRig_rigid_endpoint",
       "RelSpec": "RelSpec_simple", "RepRel": "RepRel_direct", "ImpAbs": "ImpAbs",
       "UndefFormal": "UndefFormal", "UndefPhase": "UndefPhase"}
meronymic = {"HetColl", "HomoFunc", "PartOver", "WholeOver"}
assert set(names) == set(key) | meronymic | {"RelComp", "RelOver"}


def relation_classes(ref):
    relation = elements.get(ref)
    if relation is None or relation["type"] != "BinaryRelation":
        return []
    return [elements[e].get("propertyType") for e in relation["properties"]]


def affected_domains(name, rows):
    ids = set()
    for row in rows:
        if isinstance(row, str):
            ids.add(row)
        elif isinstance(row, list):
            for relation_name in row:
                ids.update(relation_classes("rel-" + relation_name))
        elif isinstance(row, dict):
            ids.update(row.get(k) for k in ("class", "relator", "non_sortal", "type", "source", "target"))
            if row.get("id", "").startswith("rel-"):
                ids.update(relation_classes(row["id"]))
            if "relation" in row:
                ids.update(relation_classes("rel-" + row["relation"]))
            if "A" in row:
                ids.update(relation_classes("rel-" + row["A"]))
            if "B" in row:
                ids.update(relation_classes("rel-" + row["B"]))
    return sorted({domains[i] for i in ids if i in domains})


entries = []
for name in names:
    code = "MultiDep" if name == "MultDep" else name
    impl = implementations[code]
    if name in key:
        rows = current["triggers"][key[name]]
        bounded = {"probe": key[name], "candidate_count": len(rows),
                   "sample_witnesses": rows[:5], "domains_touched_by_probe": affected_domains(name, rows)}
    elif name in meronymic:
        rows = current["triggers"]["meronymic_relations"]
        bounded = {"probe": "meronymic association inventory (necessary condition only)",
                   "candidate_count": None, "underlying_meronymic_relations": len(rows),
                   "sample_witnesses": rows[:5], "domains_touched_by_probe": affected_domains(name, rows)}
    elif name == "RelComp":
        rows = structural[name]["unknown_cardinality_pairs"]
        bounded = {"probe": "bounded A/B association-composition precondition",
                   "candidate_count": structural[name]["known_cardinality_candidate_pairs"],
                   "unknown_cardinality_structural_pairs": len(rows),
                   "sample_witnesses": rows[:5], "domains_touched_by_probe": affected_domains(name, rows)}
    else:
        rows = structural[name]["rows"]
        bounded = {"probe": "potentially overlapping relator mediation pairs",
                   "candidate_count": len(rows),
                   "unknown_upper_sum_relators": structural[name]["unknown_upper_sum"],
                   "sample_witnesses": rows[:5], "domains_touched_by_probe": affected_domains(name, rows)}
    entries.append({"pattern": name,
                    "catalogue_url": f"https://ontouml.readthedocs.io/en/latest/anti-patterns/{name}/index.html",
                    "archived_OLED_implementation": impl,
                    "automated_20_pattern_engine": "NOT_EXECUTED_ON_THIS_JSON",
                    "semantic_disposition": "PENDING_HUMAN_REVIEW",
                    "bounded_prefilter": bounded})

report = {
    "scope": "G3-P5a official engine compatibility audit plus current-candidate bounded triggers; no complete 20-antipattern run and no zero-finding certificate",
    "model": {"sha256": hashlib.sha256(native_path.read_bytes()).hexdigest(),
              "elements": len(native["elements"]), "classes_including_datatypes": len(domains),
              "binary_relations": sum(x["type"] == "BinaryRelation" for x in native["elements"])},
    "source_audit": {
        "repository": "https://github.com/nemo-ufes/ontouml-lightweight-editor",
        "checkout_commit": HEAD,
        "processor": str(processor.relative_to(OLED)),
        "registered_detector_classes": registered,
        "catalogue_code_alias": "MultDep is named MultiDep in archived Java",
        "extra_registered_detector": "AssCyc (not one of the 20 catalogue items)",
        "input_contract": ".refontouml XMI read via RefOntoUML.parser.OntoUMLParser(fileName)",
        "candidate_contract": "flat ontouml-schema 1.0.2 JSON, 536 elements",
        "conversion_verified": False,
        "execution_result": "BLOCKED_FORMAT_AND_RUNTIME_COMPATIBILITY",
        "reason": "Archived batch processor accepts legacy RefOntoUML EMF/XMI files, not ontouml-schema JSON; no semantics-preserving conversion and roundtrip have been validated. Counts from direct execution on the candidate therefore do not exist."
    },
    "official_modern_api_probe": json.loads((HERE / "tool-probe.json").read_text()),
    "bounded_comparison": {
        "baseline_elements": prior["native_elements"],
        "current_elements": current["native_elements"],
        "baseline_and_current_prefilter_counts_equal": current["counts"] == prior["counts"],
        "changed_count_keys": sorted(k for k in current["counts"]
                                     if current["counts"][k] != prior["counts"][k]),
        "structural_current": {"ImpAbs_end_count": structural["ImpAbs"]["trigger_end_count"],
                               "RelComp_known_pairs": structural["RelComp"]["known_cardinality_candidate_pairs"],
                               "RelComp_unknown_cardinality_pairs": structural["RelComp"]["unknown_A_target_cardinality_structural_pairs"],
                               "RelOver_potential_relators": structural["RelOver"]["relators_with_potential_overlap"]}
    },
    "entries": entries,
    "full_20_engine_executed": False,
    "all_patterns_cleared": False,
    "limitations": ["A zero bounded trigger count only means this specific necessary-condition probe found no witness, not that the anti-pattern is absent.",
                    "The editorial domain allocations for 60 candidate roles and relators remain pending author review.",
                    "Findings across pattern families overlap; counts are not summed into an ontology quality score."]
}
assert len(entries) == 20
(HERE / "coverage-ledger.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({"catalogue_items":len(entries),
                  "archived_registered_detectors":len(registered),
                  "full_run":report["full_20_engine_executed"],
                  "bounded_unchanged_vs_B2":report["bounded_comparison"]["baseline_and_current_prefilter_counts_equal"],
                  "notable_bounded_counts":{x:report["bounded_comparison"]["structural_current"][x]
                                            for x in report["bounded_comparison"]["structural_current"]}}))
