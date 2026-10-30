#!/usr/bin/env python3
"""Executable scoped admission, reasoner, connectivity and real-source checks."""
import hashlib
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from rdflib import Graph, Namespace, RDF, OWL
from owlready2 import World, sync_reasoner
from owlready2.entity import OwlReadyInconsistentOntologyError
from owlrl import DeductiveClosure, OWLRL_Semantics
from pyshacl import validate

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
sys.path.insert(0, str(BASE / "g3-3-e-connectivity-evidence"))
from audit_g3e import native_graph, owl_graph, snapshot

CM = Namespace("https://w3id.org/cm-pharme/2.1/")
SH = Namespace("http://www.w3.org/ns/shacl#")
OWL_PATH = HERE / "active.ttl"
SHAPES_PATH = HERE / "constraints.ttl"
NATIVE_PATH = HERE / "ontouml.json"
ABOX_PATH = BASE / "g3-3-d-real-source-migration/real-source-abox.nt"
owl = Graph().parse(OWL_PATH, format="turtle")
shapes = Graph().parse(SHAPES_PATH, format="turtle")
old_shapes = Graph().parse(BASE / "g3-3-c-integrated-validation/constraints.ttl", format="turtle")


def type_(g, s, c):
    g.add((CM[s], RDF.type, CM[c]))


def obj(g, s, p, o):
    g.add((CM[s], CM[p], CM[o]))


def status(g, shape_graph=shapes):
    conforms, report, _ = validate(data_graph=g, shacl_graph=shape_graph,
                                   advanced=True, inference="none", abort_on_first=False)
    results = list(report.subjects(RDF.type, SH.ValidationResult))
    return bool(conforms), len(results)


cases = []


def case(name, types, facts, expected):
    g = Graph()
    for individual, cls in types:
        type_(g, individual, cls)
    for subject, prop, target in facts:
        obj(g, subject, prop, target)
    conforms, count = status(g)
    cases.append({"name": name, "expected": expected, "conforms": conforms,
                  "results": count, "pass": conforms == expected})


org = [("sc", "SupplyCapacity"), ("org", "Organization")]
fac = [("sc", "SupplyCapacity"), ("fac", "Facility")]
org_route = [("org", "organizationHasSupplyCapacity", "sc")]
fac_route = [("fac", "facilityHasSupplyCapacity", "sc")]
case("organization_bearer", org, org_route, True)
case("facility_bearer", fac, fac_route, True)
case("no_capacity_required_of_organization_or_facility",
     [("org", "Organization"), ("fac", "Facility")], [], True)
case("consistent_explicit_derived_query", org, org_route +
     [("sc", "capacityOrganizationBearer", "org"), ("sc", "capacityBearer", "org")], True)
case("missing_bearer", [("sc", "SupplyCapacity")], [], False)
case("both_typed_routes", org + [("fac", "Facility")], org_route + fac_route, False)
case("two_organization_bearers", org + [("org2", "Organization")], org_route +
     [("org2", "organizationHasSupplyCapacity", "sc")], False)
case("wrong_route_type", fac, [("fac", "organizationHasSupplyCapacity", "sc")], False)
case("untyped_bearer", [("sc", "SupplyCapacity")], org_route, False)
case("wrong_type_of_source", [("sc", "SupplyCapacity"), ("org", "Facility")], org_route, False)
case("broad_only_query", org, [("sc", "capacityBearer", "org")], False)
case("typed_inverse_only_query", org, [("sc", "capacityOrganizationBearer", "org")], False)
case("mismatched_broad_query", org + [("org2", "Organization")], org_route +
     [("sc", "capacityBearer", "org2")], False)
case("mismatched_typed_query", org + [("org2", "Organization")], org_route +
     [("sc", "capacityOrganizationBearer", "org2")], False)
case("observation_used_as_mode", [("obs", "SupplyCapacityObservationResult"),
     ("org", "Organization")], [("org", "organizationHasSupplyCapacity", "obs")], False)
case("observation_and_mode_collision", org + [("sc", "SupplyCapacityObservationResult")], org_route, False)

# Preserve the 11 fixture contracts from G3-C, changing the known capacity gap
# from accepted to rejected in the closed-world shapes.
def legacy_fixture():
    g = Graph()
    for s, c in [("p", "MedicinalProduct"), ("s", "PharmaceuticalSubstance"),
                 ("p2", "MedicinalProduct"), ("org", "Organization"),
                 ("org2", "Organization"), ("cap", "EnterpriseCapability"),
                 ("a", "EntityMatchAssertion"), ("a2", "EntityMatchAssertion"),
                 ("conf", "MatchConfidence")]:
        type_(g, s, c)
    for s, p, o in [("p", "productHasActiveSubstance", "s"),
                    ("cap", "capabilityBearer", "org"),
                    ("a", "hasMatchConfidence", "conf")]:
        obj(g, s, p, o)
    return g


legacy = []


def old(name, mutate, expected):
    g = legacy_fixture()
    mutate(g)
    conforms, count = status(g)
    old_conforms, _ = status(g, old_shapes)
    legacy.append({"name": name, "expected": expected, "conforms": conforms,
                   "old_conforms": old_conforms, "results": count,
                   "pass": conforms == expected})


old("valid_product_capability_confidence_and_unscored_assertion", lambda g: None, True)
old("product_without_active_substance_allowed", lambda g: type_(g, "p3", "MedicinalProduct"), True)
old("presentation_on_product_only_property_rejected", lambda g: (
    type_(g, "pres", "MedicinalProductPresentation"),
    obj(g, "pres", "productHasActiveSubstance", "s")), False)
old("untyped_active_substance_rejected", lambda g: obj(g, "p", "productHasActiveSubstance", "s2"), False)
old("capability_with_no_bearer_rejected", lambda g: type_(g, "cap2", "EnterpriseCapability"), False)
old("capability_with_two_bearers_rejected", lambda g: obj(g, "cap", "capabilityBearer", "org2"), False)
old("capability_with_untyped_bearer_rejected", lambda g: (
    obj(g, "cap", "capabilityBearer", "untyped"),
    obj(g, "cap", "capabilityBearer", "org")), False)
old("confidence_with_no_assertion_rejected", lambda g: type_(g, "conf2", "MatchConfidence"), False)
old("confidence_with_two_assertions_rejected", lambda g: obj(g, "a2", "hasMatchConfidence", "conf"), False)
old("confidence_with_wrong_bearer_rejected", lambda g: (
    type_(g, "wrong", "Organization"), obj(g, "wrong", "hasMatchConfidence", "conf")), False)
old("supply_capacity_without_bearer_gap_closed", lambda g: type_(g, "supplyCap", "SupplyCapacity"), False)


def reasoner_case(name, triples, expected, coherent=False):
    data = Graph()
    for triple in triples:
        data.add(triple)
    with TemporaryDirectory() as d:
        path = Path(d) / "combined.rdf"
        (owl + data).serialize(destination=path, format="xml")
        world = World()
        world.get_ontology(path.as_uri()).load()
        try:
            sync_reasoner(world, debug=0)
            consistent = True
            unsat = sorted(str(c.iri) for c in world.inconsistent_classes()
                           if str(c.iri) != str(OWL.Nothing)) if coherent else []
        except OwlReadyInconsistentOntologyError:
            consistent, unsat = False, []
    return {"name": name, "expected_consistent": expected,
            "consistent": consistent, "unsatisfiable_named_classes": unsat,
            "pass": consistent == expected and not unsat}


R = RDF.type
base = [(CM.sc, R, CM.SupplyCapacity)]
o = base + [(CM.org, R, CM.Organization),
            (CM.org, CM.organizationHasSupplyCapacity, CM.sc)]
f = base + [(CM.fac, R, CM.Facility),
            (CM.fac, CM.facilityHasSupplyCapacity, CM.sc)]
two_org = o + [(CM.org2, R, CM.Organization),
               (CM.org2, CM.organizationHasSupplyCapacity, CM.sc)]
reasoner = [reasoner_case("TBox_all_named_classes_satisfiable", [], True, coherent=True),
            reasoner_case("organization_bearer", o, True),
            reasoner_case("facility_bearer", f, True),
            reasoner_case("missing_explicit_bearer_consistent_under_OWA", base, True),
            reasoner_case("two_organizations_may_co_refer_under_no_UNA", two_org, True),
            reasoner_case("two_explicitly_distinct_organizations", two_org +
                          [(CM.org, OWL.differentFrom, CM.org2)], False),
            reasoner_case("organization_and_facility_routes", o + f[1:], False),
            reasoner_case("facility_on_organization_route", base +
                          [(CM.fac, R, CM.Facility),
                           (CM.fac, CM.organizationHasSupplyCapacity, CM.sc)], False),
            reasoner_case("observation_cannot_be_mode", o +
                          [(CM.sc, R, CM.SupplyCapacityObservationResult)], False)]

rl = owl + Graph()
rl.add((CM.org, CM.organizationHasSupplyCapacity, CM.sc))
DeductiveClosure(OWLRL_Semantics).expand(rl)
inferred = all(x in rl for x in [
    (CM.sc, CM.capacityOrganizationBearer, CM.org),
    (CM.sc, CM.capacityBearer, CM.org),
    (CM.org, RDF.type, CM.Organization),
    (CM.sc, RDF.type, CM.SupplyCapacity)])

abox = Graph().parse(ABOX_PATH, format="nt")
assert len(abox) == 39272
real_conforms, real_count = status(abox)
capacity_source_nodes = sum(1 for _ in abox.triples((None, RDF.type, CM.SupplyCapacity)))
native = native_graph(NATIVE_PATH)
owl_model = owl_graph(OWL_PATH)
baseline = native_graph(BASE / "g3-3-b2-focused-adjudication/ontouml-b2-review-overlay.json")
before = snapshot(baseline[0], baseline[1], baseline[3], baseline[4])
after = snapshot(native[0], native[1], native[3], native[4])
out = {
    "scope": "G3-P4a SupplyCapacity typed bearer routes: native schema/parser separately verified; full candidate SHACL and bounded OWL DL; unchanged real-source mapped ABox",
    "versions": {"rdflib": __import__("rdflib").__version__,
                 "pyshacl": __import__("pyshacl").__version__,
                 "owlready2": __import__("owlready2").VERSION,
                 "reasoner": "HermiT bundled with Owlready2"},
    "inputs": {"owl_triples": len(owl), "shapes_triples": len(shapes),
               "native_elements": len(json.loads(NATIVE_PATH.read_text())["elements"]),
               "real_abox_triples": len(abox),
               "sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in (OWL_PATH, SHAPES_PATH, NATIVE_PATH, ABOX_PATH)}},
    "shacl_scoped": {"pass_count": sum(x["pass"] for x in cases),
                     "case_count": len(cases), "cases": cases},
    "shacl_g3c_regression": {"pass_count": sum(x["pass"] for x in legacy),
                            "case_count": len(legacy), "cases": legacy},
    "owl_dl": {"pass_count": sum(x["pass"] for x in reasoner),
               "case_count": len(reasoner), "cases": reasoner},
    "owl_rl_inverse_and_subproperty": inferred,
    "real_source_shacl": {"conforms": real_conforms, "validation_results": real_count,
                          "supply_capacity_nodes": capacity_source_nodes,
                          "coverage_note": "P1 source has no capacity witness; this is regression, not empirical bearer validation"},
    "native_connectivity": {"before": before, "after": after},
    "limits": ["SHACL closed-world requirements differ from OWL open-world existence; OWL exact-one requires explicit inequality to refute two untyped distinct IRIs.",
               "Official 20-antipattern detector, scientific reviewer decisions and cross-source full empirical coverage remain G3 gates."]
}
out["pass"] = (all(x["pass"] for x in cases + legacy + reasoner) and inferred and
               real_conforms and real_count == 0 and capacity_source_nodes == 0 and
               "SupplyCapacity" in before["isolates"] and
               "SupplyCapacity" not in after["isolates"])
(HERE / "validation-results.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps({"pass": out["pass"], "scoped_shacl": f"{out['shacl_scoped']['pass_count']}/{len(cases)}",
                  "g3c_regression": f"{out['shacl_g3c_regression']['pass_count']}/{len(legacy)}",
                  "owl_dl": f"{out['owl_dl']['pass_count']}/{len(reasoner)}",
                  "rl": inferred, "real_source": real_conforms,
                  "isolates_before_after": [len(before["isolates"]), len(after["isolates"])],
                  "components_before_after": [before["components"], after["components"]]}))
if not out["pass"]:
    raise SystemExit(1)
