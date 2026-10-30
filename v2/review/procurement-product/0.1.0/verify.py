#!/usr/bin/env python3
"""Replay independently frozen procurement/product boundaries on source claims."""
import argparse
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path

from pyshacl import validate
from rdflib import Dataset, Graph, Literal, Namespace, RDF, RDFS, OWL, XSD

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
FREEZE = "5c956a67b7df929e2d0ecfa5613a52fab49fd3cc"
P = Namespace("urn:cmpe:procurement-product-lab:")
C = Namespace("https://w3id.org/cm-pharme/2.1/")
D = Namespace("https://w3id.org/cm-pharme/experimental/coherence/")
N = Namespace("urn:cmpe:procurement-product-witness:")


def check(condition, message):
    if not condition:
        raise ValueError(message)


def fixture(case, suffix="", shared_event=None, shared_type=None):
    graph = Graph()
    claim = N[case["id"] + suffix + "-claim"]
    event = shared_event or N[case["id"] + suffix + "-event"]
    product = shared_type or N[case["id"] + suffix + "-product"]
    record = N[case["id"] + suffix + "-record"]
    graph.add((claim, RDF.type, P.ProcurementProductClaim))
    if case["status"] != "none":
        graph.add((claim, P.activity, event))
        graph.add((event, RDF.type, C.ProcurementActivity))
        graph.add((claim, P.status, Literal(case["status"])))
    if case["product_class"] != "none":
        graph.add((claim, P.productType, product))
        graph.add((product, RDF.type, C[case["product_class"]]))
    if case["record_kind"] != "none":
        graph.add((claim, P.sourceRecord, record))
        graph.add((record, RDF.type, C.SourceRecord))
        graph.add((claim, P.recordKind, Literal(case["record_kind"])))
    if case["date"] != "none":
        graph.add((claim, P.transactionDate, Literal(case["date"], datatype=XSD.date)))
    return graph, event, product, record


def project(graph, shape, event, product, record):
    dataset = Dataset()
    if validate(graph, shacl_graph=shape, inference="none", advanced=True)[0]:
        dataset.graph(record).add((event, D.procurementProduct, product))
    check(len(dataset.default_graph) == 0, "Candidate promoted into default world graph")
    return dataset


def baseline_alignment():
    candidate = json.loads(gzip.decompress((ROOT / "v2/release/2.2/logistics-product/0.1.0/candidate-ontouml.json.gz").read_bytes()))
    by = {e["id"]: e for e in candidate["elements"]}
    check(len(by) == len(candidate["elements"]) == 695, "Native baseline changed")
    relation = by["coherence-rel-procurementProduct"]
    source, target = (by[e] for e in relation["properties"])
    check(relation["type"] == "BinaryRelation" and relation["stereotype"] is None and
          source["propertyType"] == "ProcurementActivity" and
          target["propertyType"] == "MedicinalProduct" and
          source["cardinality"] == target["cardinality"] == "0..*", "Native mapping drift")
    formal = Graph().parse(ROOT / "v2/ontology/candidates/2.1.0-alpha.1-domain-coherence-lab/proposed-delta.ttl", format="turtle")
    check((D.procurementProduct, RDF.type, OWL.ObjectProperty) in formal and
          (D.procurementProduct, RDFS.domain, C.ProcurementActivity) in formal and
          (D.procurementProduct, RDFS.range, C.MedicinalProduct) in formal,
          "Existing experimental OWL proposal drift")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--check-committed", action="store_true")
    args = parser.parse_args()
    pins = json.loads((HERE / "freeze.json").read_text())
    check(pins["oracle_commit"] == FREEZE, "Wrong freeze commit")
    for rel, expected in pins["sha256"].items():
        check(hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() == expected,
              "Frozen input drift: " + rel)
    baseline_alignment()
    shape = Graph().parse(HERE / "admission.ttl", format="turtle")
    oracles = json.loads((HERE / "fixed-oracles.json").read_text())
    cases = {case["id"]: case for case in oracles["cases"]}
    single = []
    for case in oracles["cases"]:
        graph, event, product, record = fixture(case)
        actual = bool(validate(graph, shacl_graph=shape, inference="none", advanced=True)[0])
        check(actual == case["admit"], "Frozen case mismatch: " + case["id"])
        data = project(graph, shape, event, product, record)
        links = list(data.quads((None, D.procurementProduct, None, None)))
        check(len(links) == int(actual), "Unexpected projection: " + case["id"])
        if actual:
            check(links[0][3] == record, "Wrong provenance graph")
        single.append(dict(id=case["id"], expected=case["admit"], observed=actual,
                           projected_links=len(links), passed=True))
    combined = []
    for group in oracles["combined"]:
        dataset = Dataset()
        actual_admitted = 0
        for index, name in enumerate(group["member_cases"]):
            case = cases[name]
            shared_event = N.sharedPurchase if group["id"] == "two_types_same_purchase" else None
            shared_type = N.sharedProductType if group["id"] in (
                "same_type_two_purchases", "executed_and_planned_same_type") else None
            graph, event, product, record = fixture(case, "-" + str(index),
                                                     shared_event, shared_type)
            admitted = bool(validate(graph, shacl_graph=shape, inference="none", advanced=True)[0])
            check(admitted == case["admit"], "Combined member mismatch: " + name)
            if admitted:
                actual_admitted += 1
                dataset.graph(record).add((event, D.procurementProduct, product))
        links = list(dataset.quads((None, D.procurementProduct, None, None)))
        expected = group["expected_candidate_links"]
        check(len(links) == expected == actual_admitted, "Combined identity error: " + group["id"])
        check(len(dataset.default_graph) == 0, "Combined promoted to world truth")
        check(not any(any(word in str(term) for word in ("Batch", "Consignment", "Receipt", "Delivery"))
                      for s, p, o, g in dataset.quads() for term in (s, p, o)),
              "Purchase invented batch or receipt")
        combined.append(dict(id=group["id"], expected=expected, projected_links=len(links),
                             batch_links=0, receipt_links=0, passed=True))
    check(len(single) == 14 and len(combined) == 4 and len(oracles["negative_inferences"]) == 5,
          "Frozen inventory changed")
    report = dict(schema_version="CMPE-ProcurementProductProbe/0.1.0", issue=350,
                  freeze_commit=FREEZE, passed=True, cases=single, combined=combined,
                  passed_cases=len(single), passed_combinations=len(combined),
                  native_candidate_695_untouched=True, candidate_statements_only=True,
                  native_and_existing_experimental_owl_typed_ends_aligned=True,
                  default_world_assertions=0, source_policy_acceptance_unchanged="1/4",
                  historical_orsd_author_acceptance_unchanged="0/83",
                  full_model_accepted=False, pages_cutover_executed=False)
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=["id", "expected", "observed", "projected_links", "passed"],
                            lineterminator="\n")
    writer.writeheader(); writer.writerows(single)
    outputs = {"report.json": (json.dumps(report, indent=2) + "\n").encode(),
               "results.csv": stream.getvalue().encode()}
    args.output.mkdir(parents=True, exist_ok=True)
    for name, raw in outputs.items():
        (args.output / name).write_bytes(raw)
        if args.check_committed:
            check((HERE / name).read_bytes() == raw, "Committed output differs: " + name)
    print(json.dumps({"passed": True, "cases": len(single), "combined": len(combined)}))


if __name__ == "__main__":
    main()
