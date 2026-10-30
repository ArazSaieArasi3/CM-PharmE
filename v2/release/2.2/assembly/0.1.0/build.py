#!/usr/bin/env python3
"""Assemble an explicitly unaccepted native review copy without reverting later fields."""
import argparse
import copy
import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path

import jsonschema
from rdflib import Graph, OWL, RDF, RDFS, URIRef

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PREP = ROOT / "v2/release/2.2/preparation/0.1.0"
spec = importlib.util.spec_from_file_location("prerequisite", PREP / "audit.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def load(path):
    return json.loads((ROOT / path).read_text())


def require(ok, message):
    if not ok:
        raise ValueError(message)


def build(base, experiment):
    result = copy.deepcopy(base)
    ids = {e["id"] for e in result["elements"]}
    result["elements"].extend(copy.deepcopy(e) for e in experiment["elements"] if e["id"] not in ids)
    package = next(e for e in result["elements"] if e["id"] == result["root"])
    prior_package = next(e for e in experiment["elements"] if e["id"] == experiment["root"])
    package["contents"] += sorted(set(prior_package["contents"]) - set(package["contents"]))
    result.update(id="cm-pharme-comprehensive-22-reconciliation-experiment",
                  name={"en": "CM-PharmE comprehensive 2.2 reconciliation EXPERIMENT - not accepted"}, modified="2026-10-30")
    return result


def check(base, experiment, result, schema):
    by = {e["id"]: e for e in result["elements"]}
    baseline = {e["id"]: e for e in base["elements"]}
    old = {e["id"]: e for e in experiment["elements"]}
    require(len(by) == len(result["elements"]), "Duplicate assembled IDs")
    require(set(by) == set(baseline) | set(old), "Assembled element set changed")
    for identifier, element in baseline.items():
        if element["type"] != "Package":
            require(by[identifier] == element, "Later native decision reverted: " + identifier)
        else:
            require({k: v for k, v in by[identifier].items() if k != "contents"} == {k: v for k, v in element.items() if k != "contents"}, "Package metadata changed")
            contents = by[identifier]["contents"]
            require(len(contents) == len(set(contents)), "Duplicate package member")
            require(set(contents) == set(element["contents"]) | set(old[identifier]["contents"]), "Package membership changed")
            require(all(i in by for i in contents), "Unknown package member")
    for identifier in set(old) - set(baseline):
        require(by[identifier] == old[identifier], "Experimental addition altered: " + identifier)
    require({k: v for k, v in base.items() if k not in {"elements", "id", "name", "modified"}} == {k: v for k, v in result.items() if k not in {"elements", "id", "name", "modified"}}, "Unauthorized project metadata delta")
    jsonschema.Draft202012Validator(schema).validate(result)
    return audit.topology(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--check-committed", action="store_true")
    args = parser.parse_args()
    manifest = json.loads((HERE / "inputs.json").read_text())
    for path, pin in manifest["files"].items():
        raw = (ROOT / path).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == pin["sha256"], "Input drift: " + path)
        require(hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == pin["git_blob_sha"], "Git blob differs: " + path)
    base, experiment = load(manifest["native_base"]), load(manifest["native_experiment"])
    schema = load(manifest["serialization_schema"])
    result = build(base, experiment)
    topology = check(base, experiment, result, schema)
    differences = json.loads((PREP / "branch-divergence.json").read_text())
    by = {e["id"]: e for e in result["elements"]}
    for d in differences["shared_nonpackage_field_differences"]:
        require(by[d["element_id"]][d["field"]] == d["latest_candidate"], "Later field decision lost")

    formal = Graph()
    for path in manifest["experimental_declaration_sources"]:
        formal.parse(ROOT / path, format="turtle")
    properties = {}
    for iri in formal.subjects(RDF.type, OWL.ObjectProperty):
        name = audit.local_name(iri)
        require(name not in properties or properties[name] == iri, "Ambiguous property local name")
        properties[name] = iri
    c = "v2/ontology/candidates/"
    lab = load(c + "2.1.0-alpha.1-four-domain-lab/relation-review-queue.json")
    refinement = load(c + "2.1.0-alpha.1-four-domain-refinement/model-manifest.json")
    coherence = load(c + "2.1.0-alpha.1-domain-coherence-lab/relation-decision-cards.json")
    evidence = {}
    for row in lab["relations"]:
        evidence[row["name"]] = (";".join(row["requirement_ids"]), "four-domain-lab/relation-review-queue.json", "TRUTHMAKER_STEREOTYPE_AND_GLOBAL_BOUNDS_PENDING")
    for row in refinement["relations"]:
        evidence[row["name"]] = (row["requirement"], "four-domain-refinement/model-manifest.json", "PROFILE_VS_GLOBAL_IDENTITY_AND_BOUNDS_PENDING")
    for row in coherence["cards"]:
        evidence[row["property"]] = (row["source_id"] + ":" + row["locator"], "domain-coherence-lab/relation-decision-cards.json", row["important_limit"])
    baseline_ids = {e["id"] for e in base["elements"]}
    additions = [e for e in result["elements"] if e["id"] not in baseline_ids]
    relations = []
    for e in additions:
        if e["type"] != "BinaryRelation":
            continue
        name = e["name"]["en"]
        require(name in evidence and name in properties, "Unaccounted experimental relation")
        iri = properties[name]
        source, target = [by[p]["propertyType"] for p in e["properties"]]
        domains, ranges = list(formal.objects(iri, RDFS.domain)), list(formal.objects(iri, RDFS.range))
        require(len(domains) == len(ranges) == 1 and all(isinstance(i, URIRef) for i in domains + ranges), "Non-named experimental endpoints")
        require(audit.local_name(domains[0]) == source and audit.local_name(ranges[0]) == target, "Native/formal proposed endpoints differ")
        requirement, reference, unresolved = evidence[name]
        relations.append(dict(native_id=e["id"], property_iri=str(iri), source=source, target=target,
                              identity="SOURCE_PROPOSAL_ID_RETAINED;NO_NEW_EQUIVALENCE_OR_KEY", direction="SOURCE_TO_TARGET_AS_RECORDED",
                              requirement_or_source=requirement, evidence_path=c + "2.1.0-alpha.1-" + reference,
                              acceptance="PENDING;NOT_PROMOTED", unresolved=unresolved,
                              bounds="PROVISIONAL_NATIVE_VALUES;LOCAL_ADMISSION_IS_SEPARATE"))
    relations.sort(key=lambda x: x["native_id"])

    refusals = []
    first = differences["shared_nonpackage_field_differences"][0]
    mutations = []
    altered = copy.deepcopy(result)
    next(e for e in altered["elements"] if e["id"] == first["element_id"])[first["field"]] = first["older_experiment"]
    mutations.append(("rollback_later_shared_field", altered))
    altered = copy.deepcopy(result)
    added_end = next(e for e in additions if e["type"] == "Property")
    altered["elements"] = [e for e in altered["elements"] if e["id"] != added_end["id"]]
    mutations.append(("drop_added_relation_end", altered))
    altered = copy.deepcopy(result)
    next(e for e in altered["elements"] if e["id"] == added_end["id"])["cardinality"] = "1"
    mutations.append(("silently_strengthen_proposed_bounds", altered))
    for name, altered in mutations:
        try:
            check(base, experiment, altered, schema)
        except (ValueError, jsonschema.ValidationError):
            refusals.append({"case": name, "refused": True})
        else:
            raise ValueError("Unsafe assembled mutation admitted: " + name)
    native_bytes = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    report = dict(schema_version="CMPE22ReconciliationAssembly/0.1.0", issue=344, passed=True,
                  scope="PROVISIONAL_NATIVE_REVIEW_ASSEMBLY;NOT_ACCEPTED_COMPLETE_MODEL", source_commit=manifest["source_commit"],
                  verified_inputs=len(manifest["files"]), native_sha256=hashlib.sha256(native_bytes).hexdigest(),
                  topology=topology, baseline_nonpackage_elements_preserved=True,
                  later_field_differences_preserved=len(differences["shared_nonpackage_field_differences"]),
                  added_relation_rows=len(relations), proposed_native_formal_endpoint_names_match=True,
                  official_vendored_schema_serialization_pass=True, semantic_ontouml_validation=False,
                  full_owl_shacl_alignment=False, full_owl_shacl_blocker="Only proposed endpoint declarations are crosswalked; full constraint semantics and profile layering require individual decisions. No obsolete formal ontology is unioned over newer decisions.",
                  prior_deferred_gate_d_ids=["AssetAtRisk", "ClinicalCareParticipant", "Vulnerability"],
                  refusal_controls=refusals, new_semantic_acceptances=0, comprehensive_2_2_ready=False,
                  next_packet="One logisticsFacility decision: Facility currently fails to distinguish origin, destination and storage participation; preserve event/site/organization distinctions.")
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(relations[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(relations)
    outputs = {"ontouml-experimental.json": native_bytes, "relation-crosswalk.csv": stream.getvalue().encode(),
               "report.json": (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode()}
    args.output.mkdir(parents=True, exist_ok=True)
    for name, raw in outputs.items():
        (args.output / name).write_bytes(raw)
        if args.check_committed:
            require((HERE / name).read_bytes() == raw, "Committed assembly differs: " + name)
    print(json.dumps({k: report[k] for k in ["passed", "native_sha256", "later_field_differences_preserved", "added_relation_rows", "comprehensive_2_2_ready"]}, indent=2))


if __name__ == "__main__":
    main()
