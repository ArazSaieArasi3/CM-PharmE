#!/usr/bin/env python3
"""Static release-plan inventory/preservation audit; not an ontology GA gate."""
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def read_json(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def read_csv(name):
    with (HERE / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def main():
    plan = read_json("release-plan.json")
    sources = read_json("sources.json")
    backlog = read_csv("backlog.csv")
    packets = read_csv("packets.csv")
    allocation = read_csv("requirements-allocation.csv")
    prs = read_csv("pull-requests.csv")
    decisions = read_json("decision-proposals.json")
    checks = []

    def require(condition, label):
        if not condition:
            raise ValueError(label)
        checks.append(label)

    issues = {int(x["issue"]) for x in backlog}
    require(len(backlog) == len(issues) == 29, "exactly 29 unique original open issue rows")
    require(issues == set(plan["inventory"]["original_open_issue_numbers"]), "issue allocation equals source inventory")
    require(issues == {x["number"] for x in sources["original_issues"]}, "all original issue body hashes retained")
    require(all(x["original_state"] == "open" and x["original_milestone"] == "none" for x in backlog), "no invented source issue closure or milestone")
    require(all(x["allocation_status"] == "PROPOSED_NOT_APPROVED" for x in backlog + allocation), "release allocations explicitly proposed")
    require({int(x["issue"]) for x in backlog if x["role"] == "EXPLICIT_EPIC"} == {21,22,23,202,228}, "five actual explicit epics retained")
    require(Counter(x["workstream"] for x in backlog) == Counter({g:len(ns) for g,ns in plan["workstreams"].items()}), "six workstreams reconcile to 29 issues")

    packet_ids = {x["packet_id"] for x in packets}
    decision_ids = {x["id"] for x in decisions}
    require(len(packet_ids) == len(packets) == 60, "60 unique bounded packet templates")
    require(all(x["effort"] in {"S", "M-"} and x["exit"] for x in packets), "all packets have bounded size and observable exit")
    require(all(int(x["issue"]) in issues | {328,329,330} for x in packets), "all packet issue links resolve to retained or actual new issues")
    for x in backlog:
        require(bool(x["packets"]) and set(x["packets"].split(";")) <= packet_ids, "issue %s has bounded packet links" % x["issue"])
    edges = {}
    for p in packets:
        deps = set(p["depends_on"].split(";")) - {"none"}
        require(deps <= packet_ids | decision_ids, "%s dependencies resolve" % p["packet_id"])
        edges[p["packet_id"]] = deps & packet_ids
    pending = dict(edges)
    while pending:
        leaves = {n for n,d in pending.items() if not (d & pending.keys())}
        require(bool(leaves), "packet dependency graph is acyclic at %s remaining nodes" % len(pending))
        pending = {n:d for n,d in pending.items() if n not in leaves}
    require({x["packet_id"] for x in packets if x["state"] == "READY_AUDIT"} == {"CORE-001"}, "only bounded independent core audit is currently ready")
    require(next(x for x in packets if x["packet_id"] == "RC-001")["state"] == "WAITING_ARAZ", "first follow-up remains actual RelComp scientific decision")
    require(plan["adopted_operating_direction"]["first_followup_issue"] == 329, "RelComp remains first substantive follow-up")

    req_path = ROOT / "v2/requirements/2.1/orsd/0.2.0/requirements.json"
    requirements = json.loads(req_path.read_text())["requirements"]
    historical = {x["id"]: x for x in requirements}
    require(len(allocation) == len({x["requirement_id"] for x in allocation}) == 83, "exactly 83 unique requirement allocations")
    require({x["requirement_id"] for x in allocation} == historical.keys(), "all ORSD stable IDs preserved")
    require(all(x["semantic_acceptance"] == historical[x["requirement_id"]]["acceptance_status"] == "PENDING_SEMANTIC_REVIEW" for x in allocation), "no new scientific requirement approval")
    require(Counter(x["proposed_release"] for x in allocation) == {"2.1.0":16, "2.2.0":61, "2.3.0":6}, "initial requirement buckets reconcile 16+61+6=83")
    require({x["requirement_id"] for x in allocation if x["selection_role"] == "FUNCTIONAL_SEED_PENDING_DEPENDENCY_AUDIT"} == {"FR-01","FR-02","FR-25","FR-28"}, "four seed anchors are not silently expanded or declared complete")
    require(len(prs) == 4 and {int(x["pr"]) for x in prs} == {172,201,305,308}, "four actual open PRs inventoried")
    require(next(x for x in prs if x["pr"] == "308")["track"] == "PRODUCTIUM_CASE_SEPARATE_PRODUCT", "Productium case explorer remains distinct from Observatory")

    for pin in sources["source_pins"]:
        p = ROOT / pin["path"]
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        require(actual == pin["sha256"], "preserved source bytes: " + pin["path"])
        frozen = subprocess.check_output(["git", "show", pin["commit"] + ":" + pin["path"]], cwd=ROOT)
        require(hashlib.sha256(frozen).hexdigest() == pin["sha256"], "source hash exists at declared checkpoint: " + pin["path"])
    tag = subprocess.check_output(["git", "rev-parse", "refs/tags/2.1.0-rc.1"], cwd=ROOT, text=True).strip()
    require(tag == plan["published_tag_commit"], "published RC tag remains unchanged")
    require(not any(plan[k] for k in ["ga_ready", "scope_amendment_approved", "scientific_acceptance_created", "license_adopted"]), "proposal creates no GA readiness scope approval scientific acceptance or license grant")
    require(plan["original_ga_gates_unchanged"] and plan["original_ga_gate_groups"] == 7, "original seven GA groups remain in force pending actual amendment")
    require(plan["inventory"]["expected_open_after_completion"] == 29+2 == 31, "open-count arithmetic accounts for new children without scientific closure")
    require(not plan["cadence"]["stable_publication_automatic"] and not plan["cadence"]["fixed_frequency_or_date_promised"], "release-cut rule does not promise or automate publication")

    broken = []
    for p in HERE.glob("*.md"):
        for link in re.findall(r"\]\(([^)]+)\)", p.read_text()):
            if link.startswith(("https://", "http://", "#")):
                continue
            target = link.split("#")[0]
            if target == "validation.json":
                continue
            if not (p.parent / target).exists():
                broken.append((p.name, link))
    require(not broken, "local documentation links resolve")
    result = {
        "status": "PASS_PLANNING_INVENTORY_AND_PRESERVATION_ONLY",
        "source_commit": plan["source_commit"],
        "original_open_issues": 29,
        "open_prs": 4,
        "packet_templates": 60,
        "requirements_allocated": 83,
        "source_file_pins_verified": len(sources["source_pins"]),
        "static_checks_passed": len(checks),
        "checks": checks,
        "scientific_acceptance_created": False,
        "original_ga_gates_changed": False,
        "new_ontology_runtime_or_ci_executed": False,
        "new_model_or_db_delta": False,
        "ga_ready": False,
    }
    (HERE / "validation.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k:v for k,v in result.items() if k != "checks"}, indent=2))


if __name__ == "__main__":
    main()
