#!/usr/bin/env python3
"""Build the bounded product-type integration from pinned 695-element candidate."""
import argparse
import copy
import gzip
import hashlib
import importlib.util
import io
import json
from pathlib import Path

import jsonschema
from owlrl import DeductiveClosure, RDFS_Semantics
from pyshacl import validate
from rdflib import Dataset, Graph, Namespace, RDF, RDFS, OWL

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
REVIEW = ROOT / "v2/review/logistics-product/0.1.0"
C = Namespace("https://w3id.org/cm-pharme/2.1/")
D = Namespace("https://w3id.org/cm-pharme/experimental/coherence/")
W = Namespace("urn:cmpe:logistics-product-integration:")
REL = "coherence-rel-logisticsProduct"
MEANING = ("Provisional source-documented MedicinalProduct type associated with a particular "
           "occurred DistributionLogisticsActivity. Source claims are candidates in named "
           "record graphs; this association does not identify batch, item, consignment, "
           "route or completed delivery. Null stereotype awaits scientific Event review.")


def check(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def candidate(base):
    model = copy.deepcopy(base)
    by = {e["id"]: e for e in model["elements"]}
    check(len(by) == len(model["elements"]) == 695, "Baseline native inventory")
    by[REL]["description"] = {"en": MEANING}
    model["id"] = "cm-pharme-comprehensive-22-logistics-product-provisional"
    model["name"] = {"en": "CM-PharmE 2.2 logistics/product provisional review candidate"}
    before = {e["id"]: e for e in base["elements"]}
    check(set(before) == set(by), "Native element inventory changed")
    for key, original in before.items():
        if key == REL:
            original = {k: v for k, v in original.items() if k != "description"}
            observed = {k: v for k, v in by[key].items() if k != "description"}
            check(observed == original, "Unexpected relation delta")
        else:
            check(by[key] == original, "Prior element changed: " + key)
    relation = by[REL]
    source, target = (by[x] for x in relation["properties"])
    check(relation["type"] == "BinaryRelation" and relation["stereotype"] is None,
          "Unsupported native relation")
    check(source["propertyType"] == "DistributionLogisticsActivity" and
          target["propertyType"] == "MedicinalProduct", "Wrong native end")
    check(source["cardinality"] == target["cardinality"] == "0..*", "Global bound changed")
    schema = read(ROOT / "tools/v2_ontology/vendor/ontouml-schema.json")
    jsonschema.Draft202012Validator(schema).validate(model)
    return model


def formal():
    graph = Graph().parse(HERE / "model.ttl", format="turtle")
    check((D.logisticsProduct, RDF.type, OWL.ObjectProperty) in graph and
          (D.logisticsProduct, RDFS.domain, C.DistributionLogisticsActivity) in graph and
          (D.logisticsProduct, RDFS.range, C.MedicinalProduct) in graph, "Formal mapping mismatch")
    check(len(list(graph.subjects(RDF.type, OWL.ObjectProperty))) == 1, "Extra property")
    check(not list(graph.triples((None, OWL.someValuesFrom, None))) and
          not list(graph.triples((None, OWL.cardinality, None))) and
          not list(graph.triples((None, OWL.sameAs, None))) and
          not list(graph.triples((None, OWL.equivalentClass, None))), "Unsupported global axiom")
    probes = []
    for label, triples, expected in (
        ("explicit-type-link", [(W.event, D.logisticsProduct, W.typeA)], True),
        ("registration-only", [(W.typeA, RDF.type, C.MedicinalProduct)], False),
        ("listing-only", [(W.typeA, RDF.type, C.MedicinalProduct)], False),
        ("bare-event", [(W.event, RDF.type, C.DistributionLogisticsActivity)], False),
    ):
        g = graph + Graph()
        for triple in triples:
            g.add(triple)
        DeductiveClosure(RDFS_Semantics).expand(g)
        check(((W.event, D.logisticsProduct, W.typeA) in g) == expected,
              "Unexpected link entailment: " + label)
        if expected:
            check((W.event, RDF.type, C.DistributionLogisticsActivity) in g and
                  (W.typeA, RDF.type, C.MedicinalProduct) in g, "Domain/range inference")
        check(not any("Batch" in str(s) or "Consignment" in str(s) or
                      "Batch" in str(p) or "Consignment" in str(p)
                      for s, p, _ in g), "Identity invented")
        probes.append({"id": label, "product_link_entails": expected,
                       "batch_or_consignment_entails": False})
    return probes


def claims():
    spec = importlib.util.spec_from_file_location("frozen_product_probe", REVIEW / "verify.py")
    frozen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(frozen)
    shape = Graph().parse(REVIEW / "admission.ttl", format="turtle")
    oracle = read(REVIEW / "fixed-oracles.json")
    outcomes = []
    for case in oracle["cases"]:
        data, event, product, record = frozen.fixture(case)
        admitted = bool(validate(data, shacl_graph=shape, inference="none", advanced=True)[0])
        check(admitted == case["admit"], "Frozen case: " + case["id"])
        dataset = frozen.project(data, shape, event, product, record)
        links = list(dataset.quads((None, D.logisticsProduct, None, None)))
        check(len(links) == int(admitted) and len(dataset.default_graph) == 0,
              "Source projection: " + case["id"])
        if admitted:
            check(links[0][3] == record, "Wrong source-qualified graph")
        outcomes.append({"id": case["id"], "admitted": admitted, "named_links": len(links)})
    check(len(outcomes) == 12 and len(oracle["combined"]) == 3, "Frozen inventory drift")
    check(read(REVIEW / "report.json")["passed_combinations"] == 3,
          "Prior combined result changed")
    return outcomes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--check-committed", action="store_true")
    args = parser.parse_args()
    pins = read(HERE / "inputs.json")
    for rel, expected in pins["sha256"].items():
        check(sha(ROOT / rel) == expected, "Pinned input changed: " + rel)
    base = json.loads(gzip.decompress((ROOT / pins["candidate_base"]).read_bytes()))
    native = candidate(base)
    probes = formal()
    cases = claims()
    mapping = {
        "native_relation": REL, "native_source": "DistributionLogisticsActivity",
        "native_target": "MedicinalProduct", "owl_property": str(D.logisticsProduct),
        "local_shape": "v2/review/logistics-product/0.1.0/admission.ttl",
        "source_graph": "sourceRecord IRI (named graph only)",
        "projection": "Only a performed, valid, opted-in source claim maps event to product type",
        "global_cardinality": "0..* at both ends", "asserted_identity": "event and product type only",
        "excluded_identity": ["batch", "item", "package", "consignment", "source record"],
        "scientific_status": "PROVISIONAL_NOT_AUTHOR_ACCEPTED"
    }
    report = {
        "schema_version": "CMPE22LogisticsProductIntegration/0.1.0", "issue": 349,
        "passed": True, "candidate_elements": 695, "added_or_deleted_elements": 0,
        "exact_previous_element_preservation_except_relation_description": True,
        "changed_native_fields": [REL + ".description.en"],
        "later_22_shared_fields_preserved": True,
        "other_47_relation_proposals_unchanged": True,
        "native_schema_valid": True, "owl_domain_range_match_native": True,
        "owl_rdfs_entailment_probes": probes, "frozen_single_cases": len(cases),
        "frozen_combined_cases_replayed_by_prior_probe": 3,
        "source_qualified_named_graph_only": True, "default_world_assertions": 0,
        "global_occurrence_inferred": False, "batch_identity_inferred": False,
        "full_native_event_semantics_pending": True, "hermit_status": "HOSTED_PENDING",
        "scientific_acceptance": False, "full_model_reasoned": False,
        "source_policy_acceptance": "1/4", "historical_orsd_author_acceptance": "0/83",
        "pages_cutover_executed": False, "release_ready": False
    }
    artifacts = {
        "candidate-ontouml.json.gz": gzip.compress(
            (json.dumps(native, ensure_ascii=False, indent=2) + "\n").encode(), mtime=0),
        "mapping.json": (json.dumps(mapping, indent=2) + "\n").encode(),
        "report.json": (json.dumps(report, indent=2) + "\n").encode(),
        "case-results.json": (json.dumps(cases, indent=2) + "\n").encode()
    }
    args.output.mkdir(parents=True, exist_ok=True)
    for name, raw in artifacts.items():
        (args.output / name).write_bytes(raw)
        if args.check_committed:
            check((HERE / name).read_bytes() == raw, "Committed output differs: " + name)
    print(json.dumps({"passed": True, "elements": 695, "frozen_single_cases": 12,
                      "frozen_combined_cases": 3, "release_ready": False}))


if __name__ == "__main__":
    main()
