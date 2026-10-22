"""Bounded ORSD FR-01..03 witnesses on a pinned CM-PharmE 2.1 candidate."""
import hashlib
import json
import platform
from pathlib import Path

import rdflib
from owlrl import DeductiveClosure, OWLRL_Semantics
from pyshacl import validate
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
SPEC = ROOT / "v2/requirements/2.1/orsd/0.2.0"
MODEL = ROOT / "v2/ontology/candidates/2.1.0-alpha.1-g3-p4a-supply-capacity"
C = Namespace("https://w3id.org/cm-pharme/2.1/")
E = Namespace("https://example.org/orsd-a1/")
ORACLES = json.loads((HERE / "fixed-oracles.json").read_text())
INPUTS = {"ontouml.json": MODEL / "ontouml.json", "active.ttl": MODEL / "active.ttl",
          "constraints.ttl": MODEL / "constraints.ttl", "requirements.json": SPEC / "requirements.json",
          "acceptance-contracts.json": SPEC / "acceptance-contracts.json"}
for name, path in INPUTS.items():
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    assert actual == ORACLES["input_sha256"][name], (name, actual)

owl = Graph().parse(MODEL / "active.ttl")
shapes = Graph().parse(MODEL / "constraints.ttl")

def graph(triples):
    g = Graph()
    for s, p, o in triples:
        g.add((s, p, o))
    return g

def typed(subject, kind):
    return (subject, RDF.type, kind)

def operation(relator, org, site):
    return [typed(relator, C.FacilityOperation), (relator, C.operationOrganization, org),
            (relator, C.operationFacility, site)]

def count(g, query):
    return len(list(g.query(query)))

Q_PAIR = """PREFIX c: <https://w3id.org/cm-pharme/2.1/>
SELECT DISTINCT ?org ?site WHERE {
 ?org a c:Organization . ?site a c:Facility .
 ?rel a c:FacilityOperation ; c:operationOrganization ?org ; c:operationFacility ?site .
}"""
Q_CONTEXT = """PREFIX c: <https://w3id.org/cm-pharme/2.1/>
SELECT DISTINCT ?org ?role ?rel WHERE {
 ?org a c:Organization, c:ManufacturerRole .
 ?rel a c:ManufacturingResponsibility ; c:manufacturingResponsibilityHolder ?org ;
      c:manufacturingResponsibilityCounterpart ?product .
 ?product a c:ManufacturingResponsibilitySubjectRole .
 BIND(c:ManufacturerRole AS ?role)
}"""

org, a, b, product = E.org, E.siteA, E.siteB, E.product
common = [typed(org, C.Organization), typed(a, C.Facility), typed(b, C.Facility)]
ops = operation(E.opA, org, a) + operation(E.opB, org, b)
fr1_positive = graph(common + [typed(org, C.OperatingOrganizationRole),
    typed(a, C.OperatedFacilityRole), typed(b, C.OperatedFacilityRole)] + ops)
fr1_negative = graph([typed(E.sameLabelOrg, C.Organization),
    typed(E.sameLabelSite, C.Facility), (E.sameLabelOrg, RDFS.label, Literal("Shared")),
    (E.sameLabelSite, RDFS.label, Literal("Shared"))])
fr1_boundary = graph([typed(org, C.Organization), typed(org, C.OperatingOrganizationRole),
    typed(E.opUnknown, C.FacilityOperation), (E.opUnknown, C.operationOrganization, org)])
fr2_positive = graph([typed(org, C.Organization), typed(org, C.ManufacturerRole),
    typed(product, C.MedicinalProduct), typed(product, C.ManufacturingResponsibilitySubjectRole),
    typed(E.resp, C.ManufacturingResponsibility), (E.resp, C.manufacturingResponsibilityHolder, org),
    (E.resp, C.manufacturingResponsibilityCounterpart, product)])
fr2_negative = graph([typed(E.namedOnly, C.Organization),
    (E.namedOnly, RDFS.label, Literal("Manufacturer Limited"))])
fr2_boundary = graph([typed(E.holder, C.Organization), typed(E.respIncomplete, C.ManufacturingResponsibility),
    (E.respIncomplete, C.manufacturingResponsibilityHolder, E.holder)])
fr3_positive = graph([typed(org, C.Organization), typed(org, C.OperatingOrganizationRole),
    typed(a, C.Facility), typed(a, C.OperatedFacilityRole)] + operation(E.opA, org, a))
fr3_negative = graph([typed(org, C.Organization), typed(a, C.Facility),
    typed(E.place, C.GeographicFeature), (org, C.locatedIn, E.place),
    (a, C.locatedIn, E.place)])
fr3_boundary = fr1_boundary

def conforms(g):
    return bool(validate(data_graph=g, shacl_graph=shapes, ont_graph=owl,
                         inference="none", advanced=True, abort_on_first=False)[0])

cases = {
    "FR-01": {"positive": fr1_positive, "negative": fr1_negative, "boundary": fr1_boundary},
    "FR-02": {"positive": fr2_positive, "negative": fr2_negative, "boundary": fr2_boundary},
    "FR-03": {"positive": fr3_positive, "negative": fr3_negative, "boundary": fr3_boundary},
}
observed = {
    "FR-01": {"positive_pairs": count(fr1_positive, Q_PAIR),
              "negative_pairs": count(fr1_negative, Q_PAIR),
              "boundary_pairs": count(fr1_boundary, Q_PAIR),
              "boundary_admission_conforms": conforms(fr1_boundary)},
    "FR-02": {"positive_contexts": count(fr2_positive, Q_CONTEXT),
              "negative_contexts": count(fr2_negative, Q_CONTEXT),
              "boundary_contexts": count(fr2_boundary, Q_CONTEXT),
              "incomplete_admission_conforms": conforms(fr2_boundary)},
    "FR-03": {"positive_operations": count(fr3_positive, Q_PAIR),
              "negative_operations": count(fr3_negative, Q_PAIR),
              "boundary_operations": count(fr3_boundary, Q_PAIR),
              "boundary_admission_conforms": conforms(fr3_boundary)},
}

# This is a direct check of the actual OWL AllDisjointClasses axiom. It is not a
# closed-world assertion that every unrecorded class membership is false.
disjoint_sets = [set(owl.items(members)) for _, _, members in owl.triples((None, OWL.members, None))]
identity_countermodel = graph([typed(E.collapsedIdentity, C.Organization),
                               typed(E.collapsedIdentity, C.Facility)])
asserted_kinds = set(identity_countermodel.objects(E.collapsedIdentity, RDF.type))
observed["FR-01"]["negative_identity_inconsistent"] = any(
    len(asserted_kinds & members) > 1 for members in disjoint_sets)
inferred = Graph()
inferred += owl
inferred += fr2_boundary
DeductiveClosure(OWLRL_Semantics).expand(inferred)
observed["FR-02"]["inferred_holder_role"] = (E.holder, RDF.type, C.ManufacturerRole) in inferred
materialized = Graph()
materialized += owl
materialized += fr1_positive
DeductiveClosure(OWLRL_Semantics).expand(materialized)

native = json.loads((MODEL / "ontouml.json").read_text())
native_ids = set()
def collect(node):
    if isinstance(node, dict):
        if "id" in node: native_ids.add(node["id"])
        for val in node.values(): collect(val)
    elif isinstance(node, list):
        for val in node: collect(val)
collect(native)
crosswalk = {
    "FR-01": ["Organization", "Facility", "FacilityOperation", "rel-operates",
              "rel-operationOrganization", "rel-operationFacility"],
    "FR-02": ["Organization", "ManufacturerRole", "ImporterRole", "WholesaleDistributorRole",
              "ManufacturingResponsibility", "rel-manufacturingResponsibilityHolder"],
    "FR-03": ["FacilityOperation", "OperatingOrganizationRole", "OperatedFacilityRole",
              "rel-operationOrganization", "rel-operationFacility"],
}
native_presence = {key: {n: n in native_ids for n in ids} for key, ids in crosswalk.items()}

result = {"source_commit": ORACLES["source_commit"], "oracle_commit": "bbfbd92",
          "versions": {"python": platform.python_version(), "rdflib": rdflib.__version__,
                       "pyshacl": __import__("pyshacl").__version__,
                       "owlrl": __import__("owlrl").__version__},
          "model_sha256": ORACLES["input_sha256"],
          "synthetic_witnesses": {k: {kind: len(g) for kind, g in v.items()} for k, v in cases.items()},
          "native_ids_present": native_presence,
          "supplemental_diagnostics": {
              "positive_admission_conforms": {"FR-01": conforms(fr1_positive),
                                               "FR-02": conforms(fr2_positive),
                                               "FR-03": conforms(fr3_positive)},
              "negative_no_relation_admission_conforms": {"FR-01": conforms(fr1_negative),
                                                          "FR-02": conforms(fr2_negative),
                                                          "FR-03": conforms(fr3_negative)},
              "identity_countermodel_triples": len(identity_countermodel),
              "operates_materialization_from_two_relators": (org, C.operates, a) in materialized,
          },
          "outcomes": {k: {"expected": v["expected"], "observed": observed[k],
                          "all_expected_met": observed[k] == v["expected"]}
                       for k, v in ORACLES["requirements"].items()}}
(HERE / "results.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({k: v["all_expected_met"] for k, v in result["outcomes"].items()}))
if not all(v["all_expected_met"] for v in result["outcomes"].values()):
    raise SystemExit(1)
