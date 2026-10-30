#!/usr/bin/env python3
"""Build and verify one provisional logistics/site native and formal candidate."""
import argparse
import copy
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path

import jsonschema
from owlrl import DeductiveClosure, RDFS_Semantics
from pyshacl import validate
from rdflib import Graph, Namespace, OWL, RDF, RDFS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
ASSEMBLY = ROOT / "v2/release/2.2/assembly/0.1.0"
PREP = ROOT / "v2/review/logistics-site/0.1.0"
C = Namespace("https://w3id.org/cm-pharme/2.1/")
D = Namespace("https://w3id.org/cm-pharme/experimental/coherence/")
P = Namespace("https://w3id.org/cm-pharme/experimental/logistics-site/0.1.0/")
ROLES = ("Origin", "Destination", "Storage")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text())


def require(value, message):
    if not value:
        raise ValueError(message)


def generate(base):
    model = copy.deepcopy(base)
    by = {e["id"]: e for e in model["elements"]}
    original = by["coherence-rel-logisticsFacility"]
    ends = [by[i] for i in original["properties"]]
    package = by[model["root"]]
    mapping = []
    for role in ROLES:
        term = "logistics" + role + "Facility"
        rid = "ls22-rel-" + term
        ids = [rid + "-source", rid + "-target"]
        require(all(i not in by for i in [rid] + ids), "Duplicate ID")
        relation = copy.deepcopy(original)
        relation.update(id=rid, name={"en": term}, properties=ids,
                        description={"en": "Provisional documented " + role.lower() +
                                     " physical-site participation of this event; no inferred route or occurrence."})
        for index, source in enumerate(ends):
            endpoint = copy.deepcopy(source)
            endpoint.update(id=ids[index], name={"en": term + (" source" if index == 0 else " target")},
                            subsettedProperties=[source["id"]])
            model["elements"].append(endpoint)
        model["elements"].append(relation)
        package["contents"].extend(ids + [rid])
        mapping.append(dict(native_id=rid, owl_property=str(P[term]),
                            source="DistributionLogisticsActivity", target="Facility",
                            super_relation_id=original["id"], super_property=str(D.logisticsFacility),
                            source_end_subsets=ends[0]["id"], target_end_subsets=ends[1]["id"],
                            requirement="R22-LS-02", acceptance="PROVISIONAL_NOT_AUTHOR_ACCEPTED"))
    model.update(id="cm-pharme-comprehensive-22-logistics-site-provisional",
                 name={"en": "CM-PharmE 2.2 logistics/site provisional review candidate"},
                 modified="2026-10-30")
    return model, mapping


def verify_native(base, model, mapping):
    before = {e["id"]: e for e in base["elements"]}
    after = {e["id"]: e for e in model["elements"]}
    require(len(before) == 686 and len(after) == len(model["elements"]) == 695, "Unexpected element count")
    require(set(before) <= set(after) and len(set(after) - set(before)) == 9, "Native delta")
    for i, element in before.items():
        if i != base["root"]:
            require(after[i] == element, "Base element changed: " + i)
        else:
            require({k: v for k, v in after[i].items() if k != "contents"} ==
                    {k: v for k, v in element.items() if k != "contents"}, "Root metadata changed")
            require(after[i]["contents"][:len(element["contents"])] == element["contents"], "Prior members changed")
            require(len(after[i]["contents"]) == len(set(after[i]["contents"])), "Duplicate package member")
    for row in mapping:
        e = after[row["native_id"]]
        source, target = (after[i] for i in e["properties"])
        require(e["type"] == "BinaryRelation" and e["stereotype"] is None, "Unsupported native stereotype")
        require(source["propertyType"] == row["source"] and target["propertyType"] == row["target"], "Wrong native ends")
        require(source["subsettedProperties"] == [row["source_end_subsets"]] and
                target["subsettedProperties"] == [row["target_end_subsets"]], "Missing native subsetting")
        require(source["cardinality"] == target["cardinality"] == "0..*", "Global participation strengthened")
        require(source["isReadOnly"] is False and target["isReadOnly"] is False, "Native field changed")
    schema = read(ROOT / "tools/v2_ontology/vendor/ontouml-schema.json")
    jsonschema.Draft202012Validator(schema).validate(model)


def verify_formal(path, mapping):
    graph = Graph().parse(path, format="turtle")
    require(len(list(graph.subjects(RDF.type, OWL.ObjectProperty))) == 4, "Object property declarations")
    for row in mapping:
        iri = P[row["owl_property"].rsplit("/", 1)[-1]]
        require((iri, RDF.type, OWL.ObjectProperty) in graph and
                (iri, RDFS.subPropertyOf, D.logisticsFacility) in graph and
                (iri, RDFS.domain, C.DistributionLogisticsActivity) in graph and
                (iri, RDFS.range, C.Facility) in graph, "OWL declaration mismatch")
    require(not list(graph.triples((None, OWL.someValuesFrom, None))) and
            not list(graph.triples((None, OWL.cardinality, None))) and
            not list(graph.triples((None, OWL.disjointWith, None))), "Unsupported global axiom")
    t = Namespace("urn:cmpe:logistics-integration:")
    probes = []
    for role in ROLES:
        pred = P["logistics" + role + "Facility"]
        case = graph + Graph().parse(data=f"<{t.event}> <{pred}> <{t.site}> .", format="turtle")
        DeductiveClosure(RDFS_Semantics).expand(case)
        require((t.event, D.logisticsFacility, t.site) in case, "Specific failed to imply generic")
        require(all((t.event, P["logistics" + other + "Facility"], t.site) not in case
                    for other in ROLES if other != role), "Invented another function")
        probes.append(role.lower() + "_implies_generic_only")
    generic = graph + Graph().parse(data=f"<{t.event}> <{D.logisticsFacility}> <{t.site}> .", format="turtle")
    DeductiveClosure(RDFS_Semantics).expand(generic)
    require(all((t.event, P["logistics" + role + "Facility"], t.site) not in generic for role in ROLES),
            "Generic invents a role")
    probes.append("generic_invents_no_function")
    return probes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--check-committed", action="store_true")
    a = parser.parse_args()
    pinned = read(HERE / "inputs.json")
    for rel, digest in pinned["sha256"].items():
        require(sha((ROOT / rel).read_bytes()) == digest, "Pinned source changed: " + rel)
    base = read(ASSEMBLY / "ontouml-experimental.json")
    model, mapping = generate(base)
    verify_native(base, model, mapping)
    formal = verify_formal(HERE / "model.ttl", mapping)
    source_shape = Graph().parse(PREP / "admission.ttl", format="turtle")
    probe = Graph().parse(data="""
        @prefix l: <urn:cmpe:logistics-site-lab:> .
        @prefix c: <https://w3id.org/cm-pharme/2.1/> .
        l:claim a l:SiteClaim; l:activity l:event; l:site l:site;
          l:function "origin"; l:occurrenceStatus "performed"; l:sourceRecord l:record .
        l:event a c:DistributionLogisticsActivity . l:site a c:Facility .
        l:record a c:SourceRecord .
    """, format="turtle")
    admitted, _, _ = validate(probe, shacl_graph=source_shape, inference="none", advanced=True)
    require(admitted, "Opted-in source claim should be admitted")
    require(len(read(PREP / "report.json")["cases"]) == 19, "Previous oracle count")
    require(read(PREP / "report.json")["passed"], "Frozen oracle report failed")
    trace = io.StringIO(newline="")
    writer = csv.writer(trace, lineterminator="\n")
    writer.writerow(["requirement_id", "candidate_artifact", "verification", "scientific_acceptance"])
    for n in range(1, 7):
        writer.writerow([f"R22-LS-{n:02d}", "native candidate;model.ttl;prior opted-in claim profile",
                         "native-preservation;OWL-RDFS;SHACL;frozen-19", "PENDING"])
    report = dict(schema_version="CMPE22LogisticsParticipation/0.1.0", issue=347, passed=True,
                  base_elements=686, candidate_elements=695, added_relations=3, added_native_ends=6,
                  base_elements_preserved=True, later_22_fields_preserved_by_exact_base_equality=True,
                  source_49_proposals_unchanged=True, rdf_subproperties_match_native_end_subsettings=True,
                  source_qualified_shacl_profile_reused=True, prior_19_frozen_oracles_retained=True,
                  rdfs_probes=formal, full_native_event_situation_semantic_validation=False,
                  hermit_status="HOSTED_PENDING", scientific_acceptance=False,
                  target_release_ready=False, pages_cutover_executed=False)
    artifacts = {"candidate-ontouml.json": (json.dumps(model, ensure_ascii=False, indent=2) + "\n").encode(),
                 "mapping.json": (json.dumps(mapping, indent=2) + "\n").encode(),
                 "requirements-trace.csv": trace.getvalue().encode(),
                 "report.json": (json.dumps(report, indent=2) + "\n").encode()}
    a.output.mkdir(parents=True, exist_ok=True)
    for name, raw in artifacts.items():
        (a.output / name).write_bytes(raw)
        if a.check_committed:
            recorded = gzip.decompress((HERE / (name + ".gz")).read_bytes()) if name == "candidate-ontouml.json" else (HERE / name).read_bytes()
            require(recorded == raw, "Committed output differs: " + name)
    print(json.dumps({k: report[k] for k in ["passed", "base_elements", "candidate_elements",
                                          "added_relations", "hermit_status", "target_release_ready"]}))


if __name__ == "__main__":
    main()
