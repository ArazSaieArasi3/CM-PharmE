"""Deterministic bounded FacilityOperation decision overlay on pinned G3-P4a."""
import hashlib
import json
from pathlib import Path

from rdflib import Graph

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "2.1.0-alpha.1-g3-p4a-supply-capacity"
PIN = {
    "ontouml.json": "264d26d263e5fa25e432dc65dd6b0402bf274958c9d18c32be2d2583634deaca",
    "active.ttl": "c62f0abb21df3aad36154ed6aa04ab0287bc7ce7a5fd6a04effc8cd338f6f304",
    "constraints.ttl": "510a65519ae0534c48c98250134bc8a4b2b658dd571e185c030af112ef461229",
}
for name, expected in PIN.items():
    assert hashlib.sha256((BASE / name).read_bytes()).hexdigest() == expected, name

native = json.loads((BASE / "ontouml.json").read_text())
changed = []
def visit(value):
    if isinstance(value, dict):
        if value.get("id") == "end-operationOrganization-target":
            assert value["propertyType"] == "OperatingOrganizationRole" and value["cardinality"] == "1..*"
            value["cardinality"] = "1"
            changed.append(value["id"])
        for nested in value.values(): visit(nested)
    elif isinstance(value, list):
        for nested in value: visit(nested)
visit(native)
assert changed == ["end-operationOrganization-target"]
(HERE / "ontouml.json").write_text(json.dumps(native, indent=2, ensure_ascii=False) + "\n")

owl = (BASE / "active.ttl").read_text()
old = 'owl:versionIRI cmpe:2.1.0-alpha.1-g3-2e-f-candidate'
assert owl.count(old) == 1
owl = owl.replace(old, 'owl:versionIRI cmpe:2.1.0-alpha.1-p3-facility-operation')
old = 'owl:versionInfo "2.1.0-alpha.1-g3-2e-f-candidate"'
assert owl.count(old) == 1
owl = owl.replace(old, 'owl:versionInfo "2.1.0-alpha.1-p3-facility-operation"')
owl += '''\n# DEC-21-01: one accountable operator role per independently identified relator.
cmpe:FacilityOperation rdfs:subClassOf [ a owl:Restriction ;
    owl:onProperty cmpe:operationOrganization ;
    owl:onClass cmpe:OperatingOrganizationRole ;
    owl:maxQualifiedCardinality "1"^^xsd:nonNegativeInteger ] .

# DEC-21-02: material relation is derived from the explicit relator truthmaker.
cmpe:operates owl:propertyChainAxiom (
    [ owl:inverseOf cmpe:operationOrganization ] cmpe:operationFacility ) .
'''
(HERE / "active.ttl").write_text(owl)

shapes = (BASE / "constraints.ttl").read_text()
shapes += '''\n# DEC-21-01: combine with existing minCount 1 on this path.
cmpe:FacilityOperationShape sh:property [ sh:path cmpe:operationOrganization ;
    sh:class cmpe:OperatingOrganizationRole ; sh:maxCount 1 ] .

# Asserted direct material edges require a witnessed mediator under admission.
cmpe:OperatesTruthmakerShape a sh:NodeShape ;
    sh:targetSubjectsOf cmpe:operates ;
    sh:sparql [ sh:message "Every asserted operates edge needs a FacilityOperation mediator" ;
        sh:select """SELECT $this WHERE {
  $this <https://w3id.org/cm-pharme/2.1/operates> ?facility .
  FILTER NOT EXISTS {
    ?op a <https://w3id.org/cm-pharme/2.1/FacilityOperation> ;
        <https://w3id.org/cm-pharme/2.1/operationOrganization> $this ;
        <https://w3id.org/cm-pharme/2.1/operationFacility> ?facility .
  }
}""" ] .
'''
(HERE / "constraints.ttl").write_text(shapes)
assert len(Graph().parse(HERE / "active.ttl")) == 1649
assert len(Graph().parse(HERE / "constraints.ttl")) == 764
manifest = {"schema_version": "1.0", "base_package": str(BASE.relative_to(HERE.parents[2])),
            "base_sha256": PIN, "native_changed_ids": changed,
            "decision_ids": ["DEC-21-01", "DEC-21-02"],
            "generated_sha256": {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
                                 for name in PIN}}
(HERE / "build-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps({"native_changes": changed, "owl_triples": 1649, "shape_triples": 764}))
