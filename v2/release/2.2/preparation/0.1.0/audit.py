#!/usr/bin/env python3
"""Read-only, pinned reconciliation audit; a passing audit is not a model release."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from collections import Counter
from pathlib import Path

from rdflib import Graph, OWL, RDF, URIRef

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
CANDIDATES = "v2/ontology/candidates/"
LATEST = CANDIDATES + "2.1.0-alpha.1-evidencerecord-projection/ontouml.json"
EXPERIMENT = CANDIDATES + "2.1.0-alpha.1-domain-coherence-lab/ontouml-experimental.json"
FORMAL_BASE = CANDIDATES + "2.1.0-alpha.1-p3-facility-operation/active.ttl"
GATE_D = "v2/ontouml/cm-pharme-v2.conceptual-model.json"
DOMAIN = CANDIDATES + "2.1.0-alpha.1-g3-3-f-review-handoff/domain-inventory.json"
LEDGER = "v2/requirements/2.1/execution/0.2.0/traceability-ledger.csv"


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def rows(path):
    with (ROOT / path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def local_name(value):
    return str(value).rsplit("/", 1)[-1].rsplit("#", 1)[-1]


def topology(model):
    elements = {e["id"]: e for e in model["elements"]}
    require(len(elements) == len(model["elements"]), "Duplicate native element IDs")
    classes = {i for i, e in elements.items() if e["type"] == "Class" and e["stereotype"] != "datatype"}
    adjacency = {i: set() for i in classes}
    edges = []
    for e in elements.values():
        if e["type"] == "Generalization":
            ends = [e["general"], e["specific"]]
            require(all(i in elements for i in ends), "Unknown generalization endpoint")
        elif e["type"] == "BinaryRelation":
            require(len(e["properties"]) == 2, "Nonbinary relation in binary audit")
            ends = []
            for p in e["properties"]:
                require(p in elements and elements[p]["type"] == "Property", "Missing relation-end record")
                end = elements[p]["propertyType"]
                require(end is None or end in elements, "Unknown native endpoint: " + str(end))
                ends.append(end)
        else:
            continue
        if all(i in classes for i in ends):
            a, b = ends
            adjacency[a].add(b)
            adjacency[b].add(a)
            edges.append((e["id"], a, b))
    unseen, components = set(classes), []
    while unseen:
        todo, seen = [min(unseen)], set()
        while todo:
            node = todo.pop()
            if node not in seen:
                seen.add(node)
                todo.extend(adjacency[node] - seen)
        unseen -= seen
        components.append(sorted(seen))
    props = [e for e in elements.values() if e["type"] == "Property"]
    relations = [e for e in elements.values() if e["type"] == "BinaryRelation"]
    return {
        "elements": len(elements), "classes_including_datatypes": sum(e["type"] == "Class" for e in elements.values()),
        "named_nondatatype_classes": len(classes), "binary_relations": len(relations),
        "components": len(components), "component_sizes": sorted(map(len, components), reverse=True),
        "isolates": sorted(i for i in classes if not adjacency[i]), "edge_records": len(edges),
        "unknown_endpoint_types": sum(p["propertyType"] is None for p in props),
        "unknown_cardinality_ends": sum(p["cardinality"] is None for p in props),
        "unknown_readonly_ends": sum(p["isReadOnly"] is None for p in props),
        "unclassified_relations": sum(e["stereotype"] is None for e in relations),
    }


def csv_bytes(records, fields):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(records)
    return stream.getvalue().encode("utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--check-committed", action="store_true")
    args = parser.parse_args()
    pins = json.loads((HERE / "input-pins.json").read_text())
    for path, pin in pins["files"].items():
        data = (ROOT / path).read_bytes()
        require(hashlib.sha256(data).hexdigest() == pin["sha256"], "Input drift: " + path)
        require(hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() == pin["git_blob_sha"], "Git byte identity mismatch: " + path)
    facts = json.loads((HERE / "source-snapshot.json").read_text())
    contract_data = (HERE / "release-contract.json").read_bytes()
    contract = json.loads(contract_data)
    require(contract["target_distribution"] == "2.2.0" and contract["release_kind"] == "COMPREHENSIVE_FULL_V2_CONTINUATION", "Comprehensive release target was reduced")
    require(not contract["comprehensive_release_ready"], "Prerequisite audit cannot claim full release readiness")
    objective_ids = {o["id"] for o in contract["objectives"]}
    require(objective_ids == {"O22-01", "O22-02", "O22-03", "O22-04"}, "Authorized objective lost")
    require(set().union(*(set(g["objectives"]) for g in contract["release_gates"])) == objective_ids, "Release gates omit an objective")
    current = read_json("v2/release/current.json")
    require(current["current_planning_record"] == "roadmap/0.13.0/release-plan.json", "Current plan does not select the comprehensive route")
    plan = read_json("v2/release/" + current["current_planning_record"])
    require(plan["target_distribution"] == "2.2.0" and not plan["ga_ready"], "Planning readiness exceeds preparation evidence")
    latest, experiment = read_json(LATEST), read_json(EXPERIMENT)
    latest_by = {e["id"]: e for e in latest["elements"]}
    exp_by = {e["id"]: e for e in experiment["elements"]}
    top = {"latest_native_candidate": topology(latest), "prior_coherence_experiment": topology(experiment)}
    # Recompute rather than copying the stored zero-isolate result.
    historical = read_json(CANDIDATES + "2.1.0-alpha.1-domain-coherence-lab/topology.json")["new_experiment"]
    require(top["prior_coherence_experiment"]["isolates"] == historical["isolates"], "Historical isolate result is not reproduced")
    require(top["prior_coherence_experiment"]["components"] == historical["components"], "Historical component result is not reproduced")

    gate_d = read_json(GATE_D)
    domain = read_json(DOMAIN)
    ownership = {}
    for d in domain["domains"]:
        for c in d["concepts"]:
            require(c["id"] not in ownership, "Duplicate primary domain")
            ownership[c["id"]] = (d["domain"], c["domain_assignment"])
    deferred = domain["deferred_not_in_active_candidate"]
    preservation = []
    for module, concepts in gate_d["modules"].items():
        for name, stereotype in concepts:
            present = name in latest_by and latest_by[name]["type"] == "Class"
            require(present or name in deferred, "Unaccounted Gate-D concept: " + name)
            preservation.append({"concept_id": name, "baseline_module": module, "baseline_stereotype": stereotype,
                                 "latest_native_present": present, "experimental_present": name in exp_by,
                                 "prior_disposition": "ACTIVE_ID_RETAINED" if present else deferred[name],
                                 "2_2_obligation": "VERIFY_SEMANTIC_PRESERVATION" if present else "REVIEW_PRIOR_DEFERRAL_AGAINST_COMPREHENSIVE_SCOPE"})
    require(len(preservation) == gate_d["counts"]["total"], "Gate-D denominator mismatch")
    require(set(ownership) == {i for i, e in latest_by.items() if e["type"] == "Class"}, "Domain inventory does not cover latest native IDs")

    differences = []
    for identifier in sorted(set(latest_by) & set(exp_by)):
        if latest_by[identifier]["type"] == "Package":
            continue  # Package membership differs; element sets are accounted below.
        for field in sorted(set(latest_by[identifier]) | set(exp_by[identifier])):
            a, b = latest_by[identifier].get(field), exp_by[identifier].get(field)
            if a != b:
                differences.append({"element_id": identifier, "field": field, "latest_candidate": a, "older_experiment": b,
                                    "integration_rule": "PRESERVE_LATER_DECISION_OR_RECORD_EXPLICIT_VERSIONED_REPLACEMENT"})
    additions = [{"element_id": i, "element_type": exp_by[i]["type"], "acceptance": "EXPERIMENTAL_NOT_PROMOTED"}
                 for i in sorted(set(exp_by) - set(latest_by))]
    latest_only = sorted(set(latest_by) - set(exp_by))

    baseline_graph = Graph()
    for path in sorted(p for p in pins["files"] if p.startswith("v2/ontology/source/modules/") and p.endswith(".ttl")):
        baseline_graph.parse(ROOT / path, format="turtle")
    base = Graph().parse(ROOT / FORMAL_BASE, format="turtle")
    native_names = {i for i, e in latest_by.items() if e["type"] == "Class"}
    relation_names = {e["name"]["en"] for e in latest_by.values() if e["type"] == "BinaryRelation"}
    terms = []
    for kind, rdf_type in [("class", OWL.Class), ("object_property", OWL.ObjectProperty), ("datatype_property", OWL.DatatypeProperty)]:
        base_names = {local_name(x) for x in base.subjects(RDF.type, rdf_type) if isinstance(x, URIRef)}
        for iri in sorted(set(baseline_graph.subjects(RDF.type, rdf_type)), key=str):
            if not isinstance(iri, URIRef):
                continue
            name = local_name(iri)
            terms.append({"baseline_iri": str(iri), "term_kind": kind, "local_name": name,
                          "formal_base_declaration_present_by_local_name": name in base_names,
                          "native_class_or_relation_name_present": name in (native_names if kind == "class" else relation_names) if kind != "datatype_property" else "NOT_A_NATIVE_CLASS_EDGE",
                          "meaning_preserved": "NOT_ESTABLISHED_BY_NAME_PRESENCE"})

    ledger = rows(LEDGER)
    require(len({r["requirement_id"] for r in ledger}) == len(ledger), "Duplicate ORSD requirement")
    allocation = rows("v2/release/roadmap/0.1.0/requirements-allocation.csv")
    require({r["requirement_id"] for r in ledger} == {r["requirement_id"] for r in allocation}, "Original ORSD IDs lost in routing")
    new_allocation = rows("v2/release/roadmap/0.13.0/requirements-allocation.csv")
    require({r["requirement_id"] for r in new_allocation} == {r["requirement_id"] for r in ledger}, "Comprehensive route loses ORSD IDs")
    acceptance_by_id = {r["requirement_id"]: r["acceptance_status"] for r in ledger}
    require(all(r["semantic_acceptance"] == acceptance_by_id[r["requirement_id"]] and r["target_distribution"] == "2.2.0" for r in new_allocation), "Routing changes scientific acceptance or target")
    requirement_rows = []
    exp_names = set(exp_by) | {e.get("name", {}).get("en", "") for e in exp_by.values()}
    names = set(latest_by) | relation_names
    for r in ledger:
        anchors = [a.strip() for a in r["model_anchor_names"].split(";") if a.strip()]
        requirement_rows.append({"requirement_id": r["requirement_id"], "domain": r["domain"],
                                 "recorded_execution_status": r["contract_execution_status"], "recorded_acceptance": r["acceptance_status"],
                                 "latest_native_missing_anchor_names": ";".join(a for a in anchors if a not in names),
                                 "experimental_missing_anchor_names": ";".join(a for a in anchors if a not in exp_names),
                                 "interpretation": "LEXICAL_ANCHOR_CHECK_ONLY; CURRENT_TARGET_EXECUTION_AND_DISPOSITION_REQUIRED"})

    domain_rows = []
    for d in domain["domains"]:
        ids = [c["id"] for c in d["concepts"]]
        domain_rows.append({"domain": d["domain"], "current_elements_including_datatypes": len(ids),
                            "current_named_class_isolates": sum(i in top["latest_native_candidate"]["isolates"] for i in ids),
                            "provisional_ownership_count": sum(ownership[i][1] != "GATE_D_APPROVED" for i in ids),
                            "status": "NO_ACTIVE_CONCEPTS_REVIEW_REQUIRED" if not ids else "PRESENCE_IS_NOT_DOMAIN_COMPLETENESS"})
    datasets = {}
    for path in ["v2/data/mappings/ontology-rdb-mapping.csv", "v2/data/mappings/source-field-ontology-mapping.csv", "v2/data/mappings/source-mapping-coverage.csv", "v2/evaluation/protocol/e7-source-semantic-coverage.csv", "v2/evaluation/results/w7-claim-evidence-traceability.csv"]:
        rr = rows(path)
        status = next((k for k in ["mapping_status", "coverage_status", "current_status", "execution_status"] if rr and k in rr[0]), None)
        datasets[path] = {"rows": len(rr), "recorded_status_counts": dict(sorted(Counter(r[status] for r in rr).items())) if status else {},
                          "scope": "HISTORICAL_INVENTORY_NOT_REEXECUTED_ON_COMPREHENSIVE_2_2"}
    profile = Graph().parse(ROOT / "v2/ontology/profiles/2.1/m1-provenance/0.1.0/profile.ttl", format="turtle")
    m1_pin = pins["files"]["v2/ontology/profiles/2.1/m1-provenance/0.1.0/profile.ttl"]["sha256"]
    require(m1_pin == facts["stable_m1"]["ttl_sha256"], "Released M1 byte identity changed")

    report = {
        "schema_version": "CMPE-Comprehensive22Prerequisites/0.1.0", "date": "2026-10-30", "timezone": "Asia/Tehran",
        "packet_issue": 343, "audit_passed": True, "comprehensive_2_2_ready": False, "model_semantics_changed": False,
        "source_commit": pins["candidate_source_commit"], "verified_input_files": len(pins["files"]),
        "release_contract_sha256": hashlib.sha256(contract_data).hexdigest(),
        "metric": "Undirected explicit named nondatatype native classes; generalization and binary relation edges only when both ends name such a class. Unknown/anonymous ends and datatypes excluded. No semantic closure or coherence certification.",
        "topology": top,
        "gate_d": {"total": len(preservation), "active_ids_retained": sum(r["latest_native_present"] for r in preservation),
                   "prior_deferred_ids": sorted(r["concept_id"] for r in preservation if not r["latest_native_present"]),
                   "all_ids_accounted": True, "full_semantic_preservation_proved": False},
        "domains": {"baseline_domains": len(domain_rows), "with_active_elements": sum(r["current_elements_including_datatypes"] > 0 for r in domain_rows),
                    "provisional_ownerships": sum(r["provisional_ownership_count"] for r in domain_rows)},
        "branch_divergence": {"shared_nonpackage_field_differences": len(differences), "experiment_additions_by_type": dict(sorted(Counter(r["element_type"] for r in additions).items())),
                              "latest_only_ids": latest_only, "copy_older_experiment_over_latest_allowed": False},
        "formal_baseline": {"triples": len(baseline_graph), "declarations_by_type": dict(sorted(Counter(r["term_kind"] for r in terms).items())),
                            "term_presence_is_not_semantic_equivalence": True},
        "orsd": {"total": len(ledger), "original_ids_retained": True,
                 "recorded_acceptance_counts": dict(sorted(Counter(r["acceptance_status"] for r in ledger).items())),
                 "recorded_execution_status_counts": dict(sorted(Counter(r["contract_execution_status"] for r in ledger).items())),
                 "accepted_by_this_audit": 0},
        "mapping_and_evaluation_inventories": datasets,
        "released_m1": {"tbox_triples": len(profile), "released_ttl_bytes_match": True, "scope": "M1 profile only"},
        "public_source_snapshot": "source-snapshot.json; captured GitHub registry/issue metadata, not a new public-browser QA",
        "scientific_status": facts["scientific_status"],
        "next_ready_issue": 344,
        "conclusion": "Earlier zero-isolate evidence is real but experimental. Later native decisions and additional domain experiments are separate lineages. Comprehensive integration, prior-deferral review, semantic decisions, current-target evaluation and same-model public documentation remain release gates."
    }
    artifacts = {
        "report.json": (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode(),
        "branch-divergence.json": (json.dumps({"shared_nonpackage_field_differences": differences, "experimental_additions": additions, "latest_only_ids": latest_only}, indent=2) + "\n").encode(),
        "gate-d-preservation.csv": csv_bytes(preservation, list(preservation[0])),
        "baseline-formal-terms.csv": csv_bytes(terms, list(terms[0])),
        "domain-inventory.csv": csv_bytes(domain_rows, list(domain_rows[0])),
        "requirement-inventory.csv": csv_bytes(requirement_rows, list(requirement_rows[0])),
    }
    args.output.mkdir(parents=True, exist_ok=True)
    for name, data in artifacts.items():
        (args.output / name).write_bytes(data)
        if args.check_committed:
            require((HERE / name).read_bytes() == data, "Committed audit result drift: " + name)
    print(json.dumps({k: report[k] for k in ["audit_passed", "comprehensive_2_2_ready", "verified_input_files", "branch_divergence", "next_ready_issue"]}, indent=2))


if __name__ == "__main__":
    main()
