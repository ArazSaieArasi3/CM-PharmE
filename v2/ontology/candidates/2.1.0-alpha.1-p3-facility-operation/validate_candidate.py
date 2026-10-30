"""Independent operation assignment fixtures and bounded full-profile regression."""
import base64
import gzip
import hashlib
import json
import tempfile
from pathlib import Path

from rdflib import Graph, Literal, Namespace, RDF, OWL, RDFS, URIRef
from owlrl import DeductiveClosure, OWLRL_Semantics
from owlready2 import World, sync_reasoner
from owlready2.entity import OwlReadyInconsistentOntologyError
from pyshacl import validate

HERE = Path(__file__).resolve().parent
C = Namespace("https://w3id.org/cm-pharme/2.1/")
E = Namespace("https://example.org/fo-decision/")
owl = Graph().parse(HERE / "active.ttl")
shapes = Graph().parse(HERE / "constraints.ttl")

def instance(subject, kind): return (subject, RDF.type, kind)
def relator(op, org, facility):
    return [instance(op, C.FacilityOperation), (op, C.operationOrganization, org),
            (op, C.operationFacility, facility)]
def graph(triples):
    g = Graph()
    for triple in triples: g.add(triple)
    return g
def admission(g):
    ok, report, _ = validate(data_graph=g, shacl_graph=shapes, advanced=True,
                             inference="none", abort_on_first=False)
    return bool(ok), len(list(report.subjects(RDF.type, URIRef("http://www.w3.org/ns/shacl#ValidationResult"))))

org1, org2, site1, site2 = E.org1, E.org2, E.site1, E.site2
identities = [instance(org1, C.Organization), instance(org1, C.OperatingOrganizationRole),
              instance(site1, C.Facility), instance(site1, C.OperatedFacilityRole)]
one = graph(identities + relator(E.op1, org1, site1))
two_sites = graph(identities + [instance(site2, C.Facility), instance(site2, C.OperatedFacilityRole)]
                  + relator(E.op1, org1, site1) + relator(E.op2, org1, site2))
joint = graph(identities + [instance(org2, C.Organization), instance(org2, C.OperatingOrganizationRole)]
              + relator(E.op1, org1, site1) + relator(E.op2, org2, site1))
two_operators_same_op = graph(list(one) + [instance(org2, C.Organization),
    instance(org2, C.OperatingOrganizationRole), (E.op1, C.operationOrganization, org2)])
two_facilities_same_op = graph(list(one) + [instance(site2, C.Facility),
    instance(site2, C.OperatedFacilityRole), (E.op1, C.operationFacility, site2)])
missing_operator = graph([instance(E.op1, C.FacilityOperation), instance(site1, C.Facility),
    instance(site1, C.OperatedFacilityRole), (E.op1, C.operationFacility, site1)])
missing_facility = graph([instance(E.op1, C.FacilityOperation), instance(org1, C.Organization),
    instance(org1, C.OperatingOrganizationRole), (E.op1, C.operationOrganization, org1)])
unbacked_direct = graph([instance(org1, C.Organization), instance(site1, C.Facility),
    (org1, C.operates, site1)])
backed_direct = graph(list(one) + [(org1, C.operates, site1)])
colocated = graph([instance(org1, C.Organization), instance(site1, C.Facility),
    instance(E.place, C.GeographicFeature), (org1, C.locatedIn, E.place),
    (site1, C.locatedIn, E.place)])
cases = {"one_operation": (one, True), "one_org_two_sites_two_relators": (two_sites, True),
         "two_orgs_two_relators_one_site": (joint, True),
         "two_orgs_one_relator": (two_operators_same_op, False),
         "two_sites_one_relator": (two_facilities_same_op, False),
         "missing_operator_admission": (missing_operator, False),
         "missing_facility_admission": (missing_facility, False),
         "direct_operates_without_mediator": (unbacked_direct, False),
         "direct_operates_with_mediator": (backed_direct, True),
         "same_place_without_operation": (colocated, True)}
outcomes = {}
for name, (abox, expected) in cases.items():
    got, n = admission(abox)
    outcomes[name] = {"expected_conforms": expected, "observed_conforms": got,
                      "validation_results": n, "pass": got == expected}

def entailed_operates(abox):
    g = owl + abox
    DeductiveClosure(OWLRL_Semantics).expand(g)
    return sorted((str(s), str(o)) for s, _, o in g.triples((None, C.operates, None)))

positive_pairs = entailed_operates(two_sites)
joint_pairs = entailed_operates(joint)
colocation_pairs = entailed_operates(colocated)
reasoning = {"two_sites_expected_2": len(positive_pairs) == 2,
             "joint_two_relators_expected_2": len(joint_pairs) == 2,
             "colocation_expected_0": len(colocation_pairs) == 0,
             "two_sites_pairs": positive_pairs, "joint_pairs": joint_pairs}

def dl_consistent(abox):
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "combined.rdf"
        (owl + abox).serialize(destination=path, format="xml")
        world = World()
        world.get_ontology(path.as_uri()).load()
        try:
            sync_reasoner(world, debug=0)
            return True, len([x for x in world.inconsistent_classes() if str(x.iri) != str(OWL.Nothing)])
        except OwlReadyInconsistentOntologyError:
            return False, 0

dl_positive, dl_unsat = dl_consistent(one)
dl_missing, _ = dl_consistent(missing_operator)
distinct = graph(list(two_operators_same_op) + [(org1, OWL.differentFrom, org2)])
dl_two_distinct, _ = dl_consistent(distinct)
dl = {"one_operation_consistent": dl_positive, "one_operation_unsatisfiable_named_classes": dl_unsat,
      "missing_operator_open_world_consistent": dl_missing,
      "two_explicitly_distinct_operators_one_relator_inconsistent": not dl_two_distinct}

compressed = HERE.parent / "2.1.0-alpha.1-g3-3-d-real-source-migration/real-source-abox.nt.gz.b64"
real = Graph()
real.parse(data=gzip.decompress(base64.b64decode(compressed.read_bytes())).decode(), format="nt")
assert len(real) == 39272
real_ok, real_violations = admission(real)
result = {"scope": "G3-P3 FacilityOperation bounded decision; synthetic witnesses plus unchanged 768-row mapped P1 ABox",
          "versions": {"rdflib": __import__("rdflib").__version__, "pyshacl": __import__("pyshacl").__version__,
                       "owlrl": __import__("owlrl").__version__, "owlready2": __import__("owlready2").VERSION,
                       "reasoner": "HermiT bundled with Owlready2"},
          "input_sha256": {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
                           for name in ("ontouml.json", "active.ttl", "constraints.ttl")},
          "witnesses": outcomes, "owl_rl": reasoning, "owl_dl": dl,
          "real_source_replay": {"source_file": str(compressed.relative_to(HERE.parents[2])),
                                 "abox_triples": len(real), "conforms": real_ok,
                                 "validation_results": real_violations,
                                 "facility_operation_instances": sum(1 for _ in real.triples((None, RDF.type, C.FacilityOperation)))}}
(HERE / "validation-results.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({"witnesses_passed": sum(x["pass"] for x in outcomes.values()),
                  "witnesses_total": len(outcomes), "owl_rl": {k:v for k,v in reasoning.items() if isinstance(v,bool)},
                  "owl_dl": dl, "real_source_conforms": real_ok, "real_results": real_violations}))
assert all(x["pass"] for x in outcomes.values()) and all(v for v in reasoning.values() if isinstance(v,bool))
assert dl_positive and dl_unsat == 0 and dl_missing and not dl_two_distinct
assert real_ok and real_violations == 0
