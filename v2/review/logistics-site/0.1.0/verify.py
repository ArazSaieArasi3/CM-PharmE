#!/usr/bin/env python3
"""Bounded claim-admission/projection probes for the frozen logistics/site card."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path

from owlrl import DeductiveClosure, RDFS_Semantics
from pyshacl import validate
from rdflib import Dataset, Graph, Literal, Namespace, OWL, RDF, RDFS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
FREEZE_COMMIT = "653534b5c431ca19b53333ff40a0258bcddbd99e"
FREEZE_SHA = "3dff1a2f3104a38194044fb9139f7c103d40482a0e5ce57744192583b371f272"
C = Namespace("https://w3id.org/cm-pharme/2.1/")
D = Namespace("https://w3id.org/cm-pharme/experimental/coherence/")
P = Namespace("https://w3id.org/cm-pharme/experimental/logistics-site/0.1.0/")
L = Namespace("urn:cmpe:logistics-site-lab:")
SH = Namespace("http://www.w3.org/ns/shacl#")
SPECIFIC = {"origin": P.logisticsOriginFacility, "destination": P.logisticsDestinationFacility, "storage": P.logisticsStorageFacility}


def world_graph(dataset):
    return dataset.default_graph if hasattr(dataset, "default_graph") else dataset.default_context


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frozen():
    require(sha(HERE / "freeze.json") == FREEZE_SHA, "Frozen manifest changed")
    manifest = json.loads((HERE / "freeze.json").read_text())
    for section in ["oracle_files_sha256", "protected_inputs_sha256"]:
        for path, digest in manifest[section].items():
            require(sha(ROOT / path) == digest, "Frozen input drift: " + path)
    return manifest


def fixture(data, claim_id, ns):
    g, claim = Graph(), ns[claim_id]
    g.add((claim, RDF.type, L.SiteClaim))
    for field, pred in [("activity", L.activity), ("site", L.site), ("record", L.sourceRecord)]:
        value = data.get(field)
        if value is None:
            continue
        node = ns[value]
        g.add((claim, pred, node))
        kind = data.get(field + "_type")
        if kind == "FacilityAndOrganization":
            g.add((node, RDF.type, C.Facility))
            g.add((node, RDF.type, C.Organization))
        elif kind:
            g.add((node, RDF.type, C[kind]))
    for field, pred in [("function", L.function), ("status", L.occurrenceStatus)]:
        if data.get(field) is not None:
            g.add((claim, pred, Literal(data[field])))
    if data.get("same_as_activity_site"):
        g.add((ns[data["activity"]], OWL.sameAs, ns[data["site"]]))
    return g


def projection(g, query):
    candidates = Dataset()
    pairs = set()
    generic = set()
    for row in g.query(query):
        claim, activity, site, function, record = row
        named = candidates.graph(record)
        named.add((activity, D.logisticsFacility, site))
        generic.add((str(activity), str(site)))
        if str(function) in SPECIFIC:
            named.add((activity, SPECIFIC[str(function)], site))
            pairs.add((str(function), str(site).rsplit(":", 1)[-1]))
    # Quads remain source-qualified candidates, with no default-world assertion.
    require(len(world_graph(candidates)) == 0, "Source claim promoted into default world graph")
    return sorted(pairs), sorted(generic), candidates


def entails(g):
    out = Graph()
    for triple in g:
        out.add(triple)
    DeductiveClosure(RDFS_Semantics).expand(out)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--check-committed", action="store_true")
    args = parser.parse_args()
    manifest = frozen()
    cases = json.loads((HERE / "fixed-oracles.json").read_text())
    shapes = Graph().parse(HERE / "admission.ttl", format="turtle")
    schema = Graph().parse(HERE / "proposed-properties.ttl", format="turtle")
    query = (HERE / "project-claims.rq").read_text()
    by = {c["id"]: c for c in cases["cases"]}
    require(len(by) == len(cases["cases"]), "Duplicate case IDs")
    results = []
    for case in cases["cases"] + cases["combined_cases"]:
        ns = Namespace("urn:cmpe:site-witness:" + case["id"] + ":")
        data_graph = Graph()
        if "data" in case:
            data_graph += fixture(case["data"], "claim", ns)
            expected_pairs = sorted((f, case["data"]["site"]) for f in case["expected_functions"])
            expected_generic = [(str(ns[case["data"]["activity"]]), str(ns[case["data"]["site"]]))] if case["expected_admission"] else []
        else:
            expected_pairs = sorted(tuple(p) for p in case["expected_specific_pairs"])
            expected_generic = set()
            for i, member in enumerate(case["members"]):
                data = dict(by[member["case"]]["data"], site=member["site"])
                data_graph += fixture(data, "claim-" + str(i), ns)
                expected_generic.add((str(ns[data["activity"]]), str(ns[data["site"]])))
                if case.get("same_label_for_sites"):
                    data_graph.add((ns[data["site"]], RDFS.label, Literal("Same recorded label")))
            expected_generic = sorted(expected_generic)
        admitted, violations, _ = validate(data_graph, shacl_graph=shapes, inference="none", advanced=True)
        admitted = bool(admitted)
        require(admitted == case["expected_admission"], "Admission oracle mismatch: " + case["id"])
        pairs, generic, candidate_graph = projection(data_graph, query) if admitted else ([], [], Dataset())
        require(pairs == expected_pairs, "Specific projection oracle mismatch: " + case["id"])
        require(generic == expected_generic, "Generic projection mismatch: " + case["id"])
        require(not any(p == OWL.sameAs for _, p, _, _ in candidate_graph.quads()), "Projection invented identity")
        results.append(dict(id=case["id"], expected_admission=case["expected_admission"], observed_admission=admitted,
                            specific_pairs=[list(p) for p in pairs], generic_pairs=len(generic),
                            default_world_graph_empty=len(world_graph(candidate_graph)) == 0,
                            violation_components=sorted({str(violations.value(n, SH.sourceConstraintComponent)) for n in violations.subjects(RDF.type, SH.ValidationResult)}),
                            source_classification="SYNTHETIC_BOUNDARY_WITNESS", passed=True))

    t = Namespace("urn:cmpe:site-entailment:")
    probes = []
    for role, prop in SPECIFIC.items():
        entailed = entails(schema + Graph().parse(data=f"<{t.event}> <{prop}> <{t.site}> .", format="turtle"))
        require((t.event, D.logisticsFacility, t.site) in entailed, "Specific does not imply generic")
        require(all((t.event, other, t.site) not in entailed for other in SPECIFIC.values() if other != prop), "A site function implies another function")
        probes.append({"case": role + "_implies_generic_only", "passed": True})
    generic = schema + Graph().parse(data=f"<{t.event}> <{D.logisticsFacility}> <{t.site}> .", format="turtle")
    require(all((t.event, prop, t.site) not in entails(generic) for prop in SPECIFIC.values()), "Broad relation guesses a function")
    probes.append({"case": "generic_does_not_guess_function", "passed": True})
    registration = schema + Graph().parse(data=f"<{t.registration}> a <{C.EstablishmentRegistration}> . <{t.site}> a <{C.DistributionSiteRole}> .", format="turtle")
    reg = entails(registration)
    require(not list(reg.subjects(RDF.type, C.DistributionLogisticsActivity)), "Registration invents an event")
    require(not list(reg.triples((None, D.logisticsFacility, None))), "Registration invents site participation")
    probes.append({"case": "registration_alone_invents_no_event_or_participation", "passed": True})
    # These are RDFS probes of the proposal; no OWL2DL/HermiT/native claim follows.
    frozen()
    report = dict(schema_version="CMPE-LogisticsSiteDecisionProbe/0.1.0", issue=345, profile="CMPE-QualifiedLogisticsSiteClaim/0.1.0",
                  oracle_freeze_commit=FREEZE_COMMIT, freeze_sha256=FREEZE_SHA, passed=True,
                  cases=results, rdfs_probes=probes, oracle_cases_passed=len(results), rdfs_probes_passed=len(probes),
                  protected_native_assembly_and_crosswalk_unchanged=True, source_qualified_candidates_only=True,
                  default_world_truth_assertions_created=0, model_promoted=False, independent_scientific_acceptance=False,
                  whole_model_native_or_hermit_validation=False, source_policy_acceptances="1/4",
                  historical_orsd_author_acceptance="0/83", new_expert_results=0,
                  pages_cutover_executed=False,
                  scope="Source-qualified synthetic claim admission and proposed relation RDFS entailment only. Fixed oracles predate implementation. Broad links do not invent site function,actual event,legal role,identity merge or world truth.")
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=["id", "expected_admission", "observed_admission", "generic_pairs", "specific_pair_count", "passed"], lineterminator="\n")
    writer.writeheader()
    for row in results:
        writer.writerow({k: row[k] for k in ["id", "expected_admission", "observed_admission", "generic_pairs", "passed"]} | {"specific_pair_count": len(row["specific_pairs"])})
    outputs = {"report.json": (json.dumps(report, indent=2) + "\n").encode(), "boundary-results.csv": stream.getvalue().encode()}
    args.output.mkdir(parents=True, exist_ok=True)
    for name, content in outputs.items():
        (args.output / name).write_bytes(content)
        if args.check_committed:
            require((HERE / name).read_bytes() == content, "Committed probe output differs: " + name)
    print(json.dumps({k: report[k] for k in ["passed", "oracle_cases_passed", "rdfs_probes_passed", "model_promoted", "pages_cutover_executed"]}, indent=2))


if __name__ == "__main__":
    main()
