#!/usr/bin/env python3
"""Build an auditable G3-3-F traceability and review handoff packet."""
import base64
import gzip
import hashlib
import io
import json
from collections import Counter, defaultdict
from pathlib import Path

from rdflib import Graph, OWL, RDF, SH, URIRef

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
NS = "https://w3id.org/cm-pharme/2.1/"
NATIVE = BASE / "g3-3-b2-focused-adjudication/ontouml-b2-review-overlay.json"
OWL_FILE = BASE / "g3-3-c-integrated-validation/active.ttl"
SHAPES = BASE / "g3-3-c-integrated-validation/constraints.ttl"
ABOX = BASE / "g3-3-d-real-source-migration/real-source-abox.nt.gz.b64"
ISOLATE = BASE / "g3-3-e-connectivity-evidence/connectivity-evidence.json"
IMPABS = BASE / "g3-3-b3-pattern-closure/structural-results.json"
REPREL = BASE / "g3-3-b3-pattern-closure/reprel-evidence-ranked-decisions.json"
FOCAL = BASE / "g3-3-b2-focused-adjudication/reprel-19-decision-docket.json"
G3C = BASE / "g3-3-c-integrated-validation/validation-results.json"
G3D = BASE / "g3-3-d-real-source-migration/migration-results.json"
CATALOGUE = BASE / "g3-3-b-pattern-adjudication/catalogue-triage.json"


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    native_doc = read(NATIVE)
    native = {e["id"]: e for e in native_doc["elements"]}
    owl = Graph().parse(OWL_FILE, format="turtle")
    shapes = Graph().parse(SHAPES, format="turtle")
    abox_bytes = gzip.decompress(base64.b64decode(ABOX.read_bytes().strip(), validate=True))
    abox = Graph().parse(source=io.BytesIO(abox_bytes), format="nt")
    isolated = read(ISOLATE)
    register = read(HERE / "relation-register.json")
    impabs = read(IMPABS)["ImpAbs"]["rows"]
    reprel = read(REPREL)["rows"]
    focal = read(FOCAL)["rows"]
    g3c = read(G3C)
    g3d = read(G3D)
    catalogue = read(CATALOGUE)
    inventory = read(HERE / "domain-inventory.json")
    definitions = read(HERE / "isolate-definitions.json")
    native_rel = {e["name"]["en"]: e for e in native.values() if e["type"] == "BinaryRelation"}
    owl_props = {str(e)[len(NS):] for e in owl.subjects(RDF.type, OWL.ObjectProperty)
                 if isinstance(e, URIRef) and str(e).startswith(NS)}
    typed_abox = Counter(str(c)[len(NS):] for _, _, c in abox.triples((None, RDF.type, None))
                         if isinstance(c, URIRef) and str(c).startswith(NS))
    abox_predicates = Counter(str(p)[len(NS):] for _, p, _ in abox
                              if isinstance(p, URIRef) and str(p).startswith(NS))
    shape_paths = defaultdict(set)
    for shape in shapes.subjects(RDF.type, SH.NodeShape):
        for pshape in shapes.objects(shape, SH.property):
            path = shapes.value(pshape, SH.path)
            if isinstance(path, URIRef) and str(path).startswith(NS):
                shape_paths[str(path)[len(NS):]].add(str(shape))
    suite = {
        "full_candidate_shacl_expected": [g3c["full_candidate_shacl"]["pass_count"], g3c["full_candidate_shacl"]["case_count"]],
        "hermit_expected": [g3c["owl_dl_reasoner"]["pass_count"], g3c["owl_dl_reasoner"]["case_count"]],
        "real_source_rows": g3d["input"]["sampled_rows"],
        "real_source_full_graph_conforms": g3d["full_candidate_pyshacl"]["conforms"],
        "real_source_injected_negative_passes": g3d["negative_sensitivity"]["passed"],
        "official_20_pattern_detector_executed": catalogue["official_detector_executed"],
    }
    assert suite["full_candidate_shacl_expected"] == [11, 11]
    assert suite["hermit_expected"] == [8, 8]
    assert suite["real_source_rows"] == 768 and suite["real_source_full_graph_conforms"]
    assert suite["real_source_injected_negative_passes"] == 5
    assert len(catalogue["entries"]) == 20 and not catalogue["official_detector_executed"]

    def relation_ref(name):
        e = native_rel.get(name)
        if e:
            endpoints = [native[p].get("propertyType") for p in e["properties"]]
            return {"id": e["id"], "stereotype": e.get("stereotype"), "typed_ends": endpoints}
        return None

    def formal(name):
        return {
            "owl_object_property_declared": name in owl_props,
            "direct_shacl_path_shapes": sorted(shape_paths.get(name, [])),
            "direct_P1_abox_assertions": abox_predicates[name],
            "interpretation": "A path declaration/fixture pass is not evidence for a relation's scientific truthmaker or uniqueness policy.",
        }

    relation_rows = []
    for item in register["records"]:
        if item["scientific_author_status"] != "PENDING":
            continue
        name = item["name"]
        relation_rows.append({
            "decision_id": item["id"],
            "subject": name,
            "scientific_question": item.get("question"),
            "recommended_bounded_action": item.get("preferred_bounded_action"),
            "negative_acceptance": item.get("negative_acceptance_condition"),
            "native": relation_ref(name),
            "formal": formal(name),
            "source_anchors": item.get("source_anchors", []),
            "owner": "scientific author(s)",
            "gate": "P3 author disposition then targeted native/OWL/SHACL positive and negative regression",
            "status": "PENDING_AUTHOR",
        })
    assert len(relation_rows) == 29
    isolate_rows = []
    for item in isolated["isolate_proposals"]:
        name = item["class"]
        prop = item["proposed_relation"]
        isolate_rows.append({
            "subject": name,
            "domain": next(d["domain"] for d in inventory["domains"] if any(c["id"] == name for c in d["concepts"])),
            "proposed_relation": prop,
            "proposed_target": item["proposed_target"],
            "native_class": name in native,
            "native_relation": relation_ref(prop),
            "formal": formal(prop),
            "sample_direct_source_instances": item["sample_direct_instances_of_source"],
            "sample_direct_target_instances": item["sample_direct_instances_of_target"],
            "truthmaker_required": item["truthmaker_required"],
            "negative_acceptance": item["negative_acceptance_condition"],
            "owner": "scientific author(s); source curator for witness acquisition",
            "gate": "P3 domain decision with actual relation witness; optional module may remain isolated",
            "status": "PENDING_SOURCE_AND_AUTHOR",
        })
    assert len(isolate_rows) == 14
    impabs_rows = []
    for item in impabs:
        name = item["relation"]
        impabs_rows.append({
            "subject": name, "end": item["end"], "type": item["type"],
            "cardinality": item["cardinality"],
            "subtypes": item["descendants"],
            "native": relation_ref(name),
            "formal": formal(name),
            "known_enforcement": item["known_enforcement"],
            "owner": "scientific author(s)",
            "gate": "P5 subtype-specific multiplicity/metaproperty adjudication and focused counterexample",
            "status": "PENDING_SCIENTIFIC_ADJUDICATION",
        })
    assert len(impabs_rows) == 10
    focal_by_name = {r["relator"]: r for r in focal}
    reprel_rows = []
    for item in reprel:
        name = item["relator"]
        f = focal_by_name[name]
        reprel_rows.append({
            "subject": name,
            "native_class_present": name in native,
            "OWL_named_class_present": (URIRef(NS + name), RDF.type, OWL.Class) in owl,
            "P1_direct_relator_instances": typed_abox[name],
            "mediation_properties": item["mediations"],
            "tier": item["tier"],
            "fixture_evidence": item["fixture_evidence"],
            "focal_duplicate_fixture": f["focal_shacl_duplicate_fixture"],
            "focal_missing_end_fixture": f["focal_shacl_missing_end_fixture"],
            "recommended_interim_rule": item["recommended_interim_rule"],
            "author_question": item["author_question"],
            "owner": "scientific author(s)",
            "gate": "P5 choose contextual/temporal tuple key or explicitly allow repeated distinct relators; test both cases",
            "status": "PENDING_TUPLE_POLICY",
        })
    assert len(reprel_rows) == 19 and len(focal_by_name) == 19
    assert all(x["native_class_present"] and x["OWL_named_class_present"] for x in reprel_rows)
    assert len(definitions["rows"]) == 14
    summary = {
        "scope": "Traceability handoff for the G3 candidate. Families overlap: do not add 29+14+10+19 into a count of distinct scientific decisions.",
        "inputs_sha256": {str(p.relative_to(BASE)): sha(p) for p in [NATIVE, OWL_FILE, SHAPES, ABOX, ISOLATE, IMPABS, REPREL, FOCAL, G3C, G3D, CATALOGUE]},
        "author_register_sha256": sha(HERE / "relation-register.json"),
        "suite": suite,
        "counts": {
            "bounded_author_approved_relation_recommendations": 13,
            "relation_pending": len(relation_rows),
            "isolates_pending": len(isolate_rows),
            "ImpAbs_endpoint_questions": len(impabs_rows),
            "RepRel_tuple_policies": len(reprel_rows),
            "official_catalogue_entries_prefiltered_only": len(catalogue["entries"]),
            "crosswalk_active_elements": inventory["counts"]["active_elements"],
            "provisional_primary_domain_assignments": inventory["counts"]["candidate_additions_provisional_domain"],
            "intentional_deferred_gate_d_concepts": inventory["counts"]["gate_d_deferred"],
        },
        "remaining_gates": [
            {
                "id": "SCIENTIFIC",
                "owner": "scientific author(s)",
                "accept": "Decide each pending relation, isolate, ImpAbs end and RepRel tuple policy in context; preserve negative acceptance and run focused regressions.",
                "reject": "Do not convert target-only observations or graph aesthetics into new semantic relations."
            },
            {
                "id": "SUPPLY_CAPACITY",
                "owner": "ontology engineer and scientific author(s)",
                "accept": "Implement two typed Organization/Facility bearer routes, exactly one bearer per SupplyCapacity Mode; test positives and negatives in native, OWL and SHACL.",
                "reject": "A capacity measurement alone cannot instantiate Mode or require every bearer to have capacity."
            },
            {
                "id": "OFFICIAL_ANTIPATTERN",
                "owner": "ontology verification",
                "accept": "Run complete official 20-pattern detector on the authoritative native model; triage each finding with witness and author disposition.",
                "reject": "Prefilters, schema parsing and legacy verifier passes are not a complete certificate."
            },
            {
                "id": "EMPIRICAL_AND_CONTRACT",
                "owner": "source curator and ontology engineer",
                "accept": "Resolve issue #307, verify published P1 file/header/checksum contract and extend real-source/external validation with declared scope.",
                "reject": "Do not claim a full-source download or generalizability from five nonrandom slices."
            },
            {
                "id": "DOMAIN_CROSSWALK",
                "owner": "scientific author(s)",
                "accept": "Review 60 editorial primary-domain assignments and confirm the S-04/S-05 deferrals; align wiki/visuals after acceptance.",
                "reject": "Do not present W4's 87-element domain counts as counts of the 144-element candidate."
            },
        ],
        "release_state": "REVIEW_CANDIDATE_ONLY",
        "human_review_ready": "Decision packet ready for review; ontology acceptance and G3 closure pending",
    }
    (HERE / "traceability-matrix.json").write_text(json.dumps({
        "summary": summary,
        "pending_relation_decisions": relation_rows,
        "isolate_decisions": isolate_rows,
        "ImpAbs_end_questions": impabs_rows,
        "RepRel_tuple_questions": reprel_rows,
    }, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"counts": summary["counts"], "gates": [x["id"] for x in summary["remaining_gates"]], "suite": suite}, indent=2))


if __name__ == "__main__":
    main()
