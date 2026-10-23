"""Integrated, bounded G3-3-C validation on the aligned OWL/SHACL review files."""
import hashlib
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from rdflib import BNode, Graph, Namespace, RDF, RDFS, OWL
from rdflib.namespace import XSD
from owlready2 import World, sync_reasoner
from owlready2.entity import OwlReadyInconsistentOntologyError
from owlrl import DeductiveClosure, OWLRL_Semantics
from pyshacl import validate

owl_path, shapes_path, base_owl_path, base_shapes_path, native_path, out_path = map(Path, sys.argv[1:7])
CM = Namespace("https://w3id.org/cm-pharme/2.1/")
SH = Namespace("http://www.w3.org/ns/shacl#")
owl = Graph().parse(owl_path, format="turtle")
shapes = Graph().parse(shapes_path, format="turtle")
baseline = Graph().parse(base_owl_path, format="turtle")
base_shapes = Graph().parse(base_shapes_path, format="turtle")
native = json.loads(native_path.read_text())
shape_triples_at_parse, base_shape_triples_at_parse = len(shapes), len(base_shapes)

def type_(g, s, c):
    g.add((CM[s], RDF.type, CM[c]))

def obj(g, s, p, o):
    g.add((CM[s], CM[p], CM[o]))

def fixture():
    g = Graph()
    for s, typ in [("p", "MedicinalProduct"), ("s", "PharmaceuticalSubstance"),
                   ("p2", "MedicinalProduct"), ("org", "Organization"),
                   ("org2", "Organization"), ("cap", "EnterpriseCapability"),
                   ("a", "EntityMatchAssertion"), ("a2", "EntityMatchAssertion"),
                   ("conf", "MatchConfidence")]:
        type_(g, s, typ)
    for s, prop, o in [("p", "productHasActiveSubstance", "s"),
                       ("cap", "capabilityBearer", "org"),
                       ("a", "hasMatchConfidence", "conf")]:
        obj(g, s, prop, o)
    return g

def shacl_status(data, shape_graph):
    conform, report, _ = validate(data_graph=data, shacl_graph=shape_graph,
                                  advanced=True, inference="none", abort_on_first=False)
    results = list(report.subjects(RDF.type, SH.ValidationResult))
    def display_path(path):
        if isinstance(path, BNode):
            inverse = report.value(path, SH.inversePath)
            return "^" + str(inverse) if inverse is not None else "blank_node_path"
        return str(path)
    paths = sorted({display_path(x) for r in results for x in report.objects(r, SH.resultPath)})
    return bool(conform), len(results), paths

shacl = []
def case(name, mutator, expected):
    g = fixture()
    mutator(g)
    found, count, paths = shacl_status(g, shapes)
    baseline_found, baseline_count, _ = shacl_status(g, base_shapes)
    shacl.append({"name": name, "expected_conforms": expected, "conforms": found,
                  "pass": found == expected, "validation_results": count,
                  "result_paths": paths, "base_shapes_conforms": baseline_found,
                  "base_shapes_results": baseline_count, "fixture_triples": len(g)})

case("valid_product_capability_confidence_and_unscored_assertion", lambda g: None, True)
case("product_without_active_substance_allowed", lambda g: type_(g, "p3", "MedicinalProduct"), True)
case("presentation_on_product_only_property_rejected", lambda g: (type_(g, "pres", "MedicinalProductPresentation"), obj(g, "pres", "productHasActiveSubstance", "s")), False)
case("untyped_active_substance_rejected", lambda g: obj(g, "p", "productHasActiveSubstance", "s2"), False)
case("capability_with_no_bearer_rejected", lambda g: type_(g, "cap2", "EnterpriseCapability"), False)
case("capability_with_two_bearers_rejected", lambda g: obj(g, "cap", "capabilityBearer", "org2"), False)
case("capability_with_untyped_bearer_rejected", lambda g: (obj(g, "cap", "capabilityBearer", "untyped"), obj(g, "cap", "capabilityBearer", "org")), False)
case("confidence_with_no_assertion_rejected", lambda g: type_(g, "conf2", "MatchConfidence"), False)
case("confidence_with_two_assertions_rejected", lambda g: obj(g, "a2", "hasMatchConfidence", "conf"), False)
case("confidence_with_wrong_bearer_rejected", lambda g: (type_(g, "wrong", "Organization"), obj(g, "wrong", "hasMatchConfidence", "conf")), False)
case("supply_capacity_without_bearer_current_gap", lambda g: type_(g, "supplyCap", "SupplyCapacity"), True)

def reasoner_case(name, triples, expected_consistency, check_unsats=False, tbox=None):
    data = Graph()
    for t in triples:
        data.add(t)
    combined = (tbox if tbox is not None else owl) + data
    with TemporaryDirectory() as tmp:
        p = Path(tmp) / "full.rdf"
        combined.serialize(destination=p, format="xml")
        world = World()
        world.get_ontology(p.as_uri()).load()
        nclasses = len(list(world.classes()))
        try:
            sync_reasoner(world, debug=0)
            consistent = True
            unsats = sorted(str(c.iri) for c in world.inconsistent_classes()
                             if str(c.iri) != str(OWL.Nothing)) if check_unsats else []
        except OwlReadyInconsistentOntologyError:
            consistent = False
            unsats = []
    return {"name":name, "expected_consistent":expected_consistency,
            "consistent":consistent,"unsatisfiable_classes":unsats,
            "classes_imported":nclasses,"ontology_triples":len(tbox) if tbox is not None else len(owl),
            "asserted_fixture_triples":len(data),
            "pass":consistent == expected_consistency and len(unsats) == 0}

reasoner = []
reasoner.append(reasoner_case("baseline_TBox_coherent", [], True, check_unsats=True, tbox=baseline))
reasoner.append(reasoner_case("candidate_TBox_coherent", [], True, check_unsats=True))
reasoner.append(reasoner_case("valid_unscored_assertion_and_unfilled_product", [
    (CM.a2,RDF.type,CM.EntityMatchAssertion),(CM.p2,RDF.type,CM.MedicinalProduct)], True))
reasoner.append(reasoner_case("product_and_presentation_disjoint", [
    (CM.x,RDF.type,CM.MedicinalProduct),(CM.x,RDF.type,CM.MedicinalProductPresentation)], False))
cap_pair = [(CM.cap,RDF.type,CM.EnterpriseCapability),(CM.o1,RDF.type,CM.Organization),
            (CM.o2,RDF.type,CM.Organization),(CM.cap,CM.capabilityBearer,CM.o1),
            (CM.cap,CM.capabilityBearer,CM.o2)]
reasoner.append(reasoner_case("two_capability_bearers_no_inequality_consistent_OWA", cap_pair, True))
reasoner.append(reasoner_case("two_explicitly_distinct_capability_bearers_inconsistent", cap_pair+[(CM.o1,OWL.differentFrom,CM.o2)], False))
conf_pair = [(CM.conf,RDF.type,CM.MatchConfidence),
             (CM.a1,RDF.type,CM.EntityMatchAssertion),(CM.a2,RDF.type,CM.EntityMatchAssertion),
             (CM.a1,CM.hasMatchConfidence,CM.conf),(CM.a2,CM.hasMatchConfidence,CM.conf)]
reasoner.append(reasoner_case("two_explicitly_distinct_confidence_bearers_inconsistent", conf_pair+[(CM.a1,OWL.differentFrom,CM.a2)], False))
reasoner.append(reasoner_case("supply_capacity_without_asserted_bearer_consistent_OWA", [
    (CM.sc,RDF.type,CM.SupplyCapacity)], True))

rl_graph = owl + Graph()
rl_graph.add((CM.p,RDF.type,CM.MedicinalProduct))
rl_graph.add((CM.p,CM.productHasActiveSubstance,CM.s))
assert (CM.p,CM.hasActiveSubstance,CM.s) not in rl_graph
DeductiveClosure(OWLRL_Semantics).expand(rl_graph)
rl_pass = (CM.p,CM.hasActiveSubstance,CM.s) in rl_graph

assert len(shacl) == 11 and len(reasoner) == 8
assert all(x["pass"] for x in shacl), [x for x in shacl if not x["pass"]]
assert all(x["pass"] for x in reasoner), [x for x in reasoner if not x["pass"]]
assert rl_pass
assert len(owl) == len(baseline) + 10
new_rejections = [x for x in shacl if not x["conforms"] and x["base_shapes_conforms"]]
assert len(new_rejections) == 8

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

result = {
    "scope":"G3-3-C integrated review candidate: actual full candidate SHACL shapes on synthetic graphs; HermiT OWL DL on converted RDF/XML; OWL RL subproperty entailment; not a full anti-pattern or real-data certificate",
    "versions":{"rdflib":__import__("rdflib").__version__,"pyshacl":__import__("pyshacl").__version__,
                "owlready2":__import__("owlready2").VERSION,"owlrl":__import__("owlrl").__version__,
                "reasoner":"HermiT bundled with Owlready2"},
    "inputs":{"native_elements":len(native["elements"]),"owl_triples":len(owl),"base_owl_triples":len(baseline),
              "shacl_triples":shape_triples_at_parse,"base_shacl_triples":base_shape_triples_at_parse,
              "sha256":{"native":sha(native_path),"owl":sha(owl_path),"shapes":sha(shapes_path),
                        "base_owl":sha(base_owl_path),"base_shapes":sha(base_shapes_path)}},
    "full_candidate_shacl":{"case_count":len(shacl),"pass_count":sum(x["pass"] for x in shacl),
                            "new_rejections_vs_baseline_shapes":len(new_rejections),"cases":shacl},
    "owl_dl_reasoner":{"case_count":len(reasoner),"pass_count":sum(x["pass"] for x in reasoner),"cases":reasoner},
    "owl_rl_subproperty_entailment":{"case":"productHasActiveSubstance entails hasActiveSubstance", "pass":rl_pass},
    "known_limits":["SHACL closed-world missing-value checks must not be read as OWL DL inconsistency under the open-world assumption.",
                    "Two bearer IRIs need explicit inequality for OWL exact-one inconsistency; SHACL rejects two explicit nodes without it.",
                    "SupplyCapacity typed Organization/Facility exactly-one-of-two bearer route is not formalized.",
                    "No compatible official 20-pattern detector, full mapped baseline regression, or real-source migration in this run."]
}
out_path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
print(json.dumps({"SHACL":f"{result['full_candidate_shacl']['pass_count']}/{len(shacl)}",
                  "HermiT":f"{result['owl_dl_reasoner']['pass_count']}/{len(reasoner)}",
                  "OWL_RL_subproperty":rl_pass,"shacl_baseline_differences":[x["name"] for x in shacl if x["conforms"] != x["base_shapes_conforms"]]}))
