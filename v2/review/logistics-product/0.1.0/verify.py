#!/usr/bin/env python3
"""Replay precommitted independent product/event identity boundaries."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path

from pyshacl import validate
from rdflib import Dataset, Graph, Literal, Namespace, RDF

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
FREEZE = "34a1553f341f20f046482a51d811df6eadc98c74"
L = Namespace("urn:cmpe:logistics-product-lab:")
C = Namespace("https://w3id.org/cm-pharme/2.1/")
D = Namespace("https://w3id.org/cm-pharme/experimental/coherence/")
N = Namespace("urn:cmpe:logistics-product-witness:")


def check(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixture(case, suffix=""):
    graph = Graph()
    claim = N[case["id"] + suffix + "-claim"]
    event = N[case["id"] + suffix + "-event"]
    product = N[case["id"] + suffix + "-product"]
    record = N[case["id"] + suffix + "-record"]
    graph.add((claim, RDF.type, L.ProductActivityClaim))
    if case["status"] != "none":
        graph.add((claim, L.activity, event))
        graph.add((event, RDF.type, C.DistributionLogisticsActivity))
        graph.add((claim, L.status, Literal(case["status"])))
    if case["product_class"] != "none":
        graph.add((claim, L.productType, product))
        graph.add((product, RDF.type, C[case["product_class"]]))
    if case["record_class"] != "none":
        graph.add((claim, L.sourceRecord, record))
        graph.add((record, RDF.type, C[case["record_class"]]))
    return graph, event, product, record


def project(graph, source, event, product, record):
    dataset = Dataset()
    if validate(graph, shacl_graph=source, inference="none", advanced=True)[0]:
        dataset.graph(record).add((event, D.logisticsProduct, product))
    check(len(dataset.default_graph) == 0, "Claim promoted to default-world truth")
    return dataset


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--check-committed", action="store_true")
    a = parser.parse_args()
    pins = json.loads((HERE / "freeze.json").read_text())
    check(pins["oracle_commit"] == FREEZE, "Wrong freeze commit")
    for path, expected in pins["sha256"].items():
        check(digest(ROOT / path) == expected, "Frozen input drift: " + path)
    shape = Graph().parse(HERE / "admission.ttl", format="turtle")
    oracle = json.loads((HERE / "fixed-oracles.json").read_text())
    cases = {}
    results = []
    for case in oracle["cases"]:
        graph, event, product, record = fixture(case)
        actual = bool(validate(graph, shacl_graph=shape, inference="none", advanced=True)[0])
        check(actual == case["admit"], "Case mismatch: " + case["id"])
        candidate = project(graph, shape, event, product, record)
        count = sum(1 for _ in candidate.quads((None, D.logisticsProduct, None, None)))
        check(count == int(actual), "Projection mismatch: " + case["id"])
        cases[case["id"]] = case
        results.append(dict(id=case["id"],expected=case["admit"],observed=actual,
                            projected_links=count,passed=True))
    combined = []
    for group in oracle["combined"]:
        graph = Graph()
        members = []
        for index, name in enumerate(group["member_cases"]):
            case = cases[name]
            member, event, product, record = fixture(case, "-" + str(index))
            if group["id"] == "two_product_types_same_event":
                # The two explicit claims concern one event, distinct product IDs.
                for s, p, o in list(member.triples((event, None, None))):
                    member.remove((s, p, o))
                    member.add((N.sharedEvent, p, o))
                member.remove((N[name + "-" + str(index) + "-claim"], L.activity, event))
                member.add((N[name + "-" + str(index) + "-claim"], L.activity, N.sharedEvent))
                event = N.sharedEvent
            if group["id"] == "same_type_different_events":
                claim = N[name + "-" + str(index) + "-claim"]
                member.remove((claim, L.productType, product))
                member.add((claim, L.productType, N.sharedType))
                member.add((N.sharedType, RDF.type, C.MedicinalProduct))
                product = N.sharedType
            graph += member
            members.append((event, product, record))
        check(bool(validate(graph, shacl_graph=shape, inference="none", advanced=True)[0]),
              "Combined admission failed: " + group["id"])
        dataset = Dataset()
        for event, product, record in members:
            dataset.graph(record).add((event, D.logisticsProduct, product))
        n = sum(1 for _ in dataset.quads((None, D.logisticsProduct, None, None)))
        expected = group.get("expected_candidate_links", 1)
        check(n == expected, "Combined identity error: " + group["id"])
        check(len(dataset.default_graph) == 0, "Combined claims promoted")
        if group["id"] == "type_does_not_identify_batch":
            check(not any("Batch" in str(pred) or "Consignment" in str(pred)
                          for _, pred, _, _ in dataset.quads()), "Type invented batch/consignment")
        combined.append(dict(id=group["id"],candidate_links=n,expected=expected,passed=True))
    check(len(oracle["negative_inferences"]) == 5, "Frozen negative oracle inventory changed")
    report=dict(schema_version="CMPE-LogisticsProductProbe/0.1.0",issue=348,
                freeze_commit=FREEZE,passed=True,cases=results,combined=combined,
                passed_cases=len(results),passed_combinations=len(combined),
                candidate_statements_only=True,default_world_assertions=0,
                model_promoted=False,source_policy_acceptance_unchanged="1/4",
                historical_orsd_acceptance_unchanged="0/83",
                full_model_accepted=False,pages_cutover_executed=False)
    stream=io.StringIO(newline="")
    writer=csv.DictWriter(stream,fieldnames=["id","expected","observed","projected_links","passed"],lineterminator="\n")
    writer.writeheader();writer.writerows(results)
    outputs={"report.json":(json.dumps(report,indent=2)+"\n").encode(),"results.csv":stream.getvalue().encode()}
    a.output.mkdir(parents=True,exist_ok=True)
    for name,raw in outputs.items():
        (a.output/name).write_bytes(raw)
        if a.check_committed:check((HERE/name).read_bytes()==raw,"Committed output changed")
    print(json.dumps({"passed":True,"cases":len(results),"combined":len(combined)}))


if __name__=="__main__":
    main()
