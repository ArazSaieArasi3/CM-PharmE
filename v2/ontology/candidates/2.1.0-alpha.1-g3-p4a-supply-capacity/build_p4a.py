#!/usr/bin/env python3
"""Build a scoped SupplyCapacity bearer candidate from frozen G3-C/B2 inputs."""
import copy
import hashlib
import json
from pathlib import Path

from rdflib import Graph, Namespace, OWL, RDF, RDFS, URIRef

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
NATIVE = BASE / "g3-3-b2-focused-adjudication/ontouml-b2-review-overlay.json"
OWL_FILE = BASE / "g3-3-c-integrated-validation/active.ttl"
SHAPES_FILE = BASE / "g3-3-c-integrated-validation/constraints.ttl"
CM = Namespace("https://w3id.org/cm-pharme/2.1/")

ROUTES = [
    ("organizationHasSupplyCapacity", "Organization", "SupplyCapacity", "characterization", False, "0..1", "0..*", "Primary bearer-to-Mode Characterization; each Mode may have at most one Organization bearer in this branch."),
    ("facilityHasSupplyCapacity", "Facility", "SupplyCapacity", "characterization", False, "0..1", "0..*", "Primary bearer-to-Mode Characterization; each Mode may have at most one Facility bearer in this branch."),
    ("capacityOrganizationBearer", "SupplyCapacity", "Organization", None, True, "0..*", "0..1", "Derived inverse query view of organizationHasSupplyCapacity; do not independently assert in admitted RDF."),
    ("capacityFacilityBearer", "SupplyCapacity", "Facility", None, True, "0..*", "0..1", "Derived inverse query view of facilityHasSupplyCapacity; do not independently assert in admitted RDF."),
]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def common(id, type, name):
    return {"id": id, "type": type, "name": {"en": name},
            "created": "2026-10-09", "modified": "2026-10-09",
            "alternativeNames": [], "description": None, "editorialNotes": [],
            "creators": [], "contributors": [], "customProperties": None}

def prop(relation, suffix, type, cardinality):
    e = common("end-" + relation + "-" + suffix, "Property", "end-" + relation + "-" + suffix)
    e.update({"stereotype": None, "isDerived": False, "subsettedProperties": [],
              "redefinedProperties": [], "aggregationKind": "NONE",
              "cardinality": cardinality, "isOrdered": False, "isReadOnly": None,
              "propertyType": type})
    return e

def relation(name, source, target, stereotype, derived, source_card, target_card, desc):
    e = common("rel-" + name, "BinaryRelation", name)
    e.update({"description": {"en": desc},
              "stereotype": stereotype, "isDerived": derived, "isAbstract": False,
              "properties": ["end-" + name + "-source", "end-" + name + "-target"]})
    return [e, prop(name, "source", source, source_card),
            prop(name, "target", target, target_card)]

native = json.loads(NATIVE.read_text())
assert len(native["elements"]) == 523
all_ids = {e["id"] for e in native["elements"]}
root = next(e for e in native["elements"] if e["id"] == native["root"])
assert next(e for e in native["elements"] if e["id"] == "SupplyCapacity")["restrictedTo"] == ["intrinsic-mode"]
broad = next(e for e in native["elements"] if e["id"] == "rel-capacityBearer")
assert broad["stereotype"] is None and broad["properties"] == ["end-capacityBearer-source", "end-capacityBearer-target"]
assert next(e for e in native["elements"] if e["id"] == "end-capacityBearer-target")["propertyType"] is None
broad["description"] = {"en": "Common derived Mode-to-bearer query surface over typed Organization/Facility Characterization routes. Native exact-one-across-routes is documented in p4a-capacity-xor-note and enforced in OWL DL/SHACL; a broad-only ABox assertion is not admitted."}
broad["isDerived"] = True
broad["modified"] = "2026-10-09"
added = []
for args in ROUTES:
    added.extend(relation(*args))
note = common("p4a-capacity-xor-note", "Note", "p4a-capacity-xor-note")
note["text"] = {"en": "SupplyCapacity is an intrinsic Mode. Each Mode inheres in exactly one bearer, either an Organization via organizationHasSupplyCapacity or a Facility via facilityHasSupplyCapacity, never both. Both bearer-to-Mode associations are Characterization. The inverse routes and capacityBearer are derived query views; native per-route bounds 0..1 do not themselves express the XOR. OWL exact-one on common property plus typed existential union and SHACL explicit inverse-path XOR enforce the combined policy. No Organization/Facility must possess capacity; SupplyCapacityObservationResult is an independent observation."}
added.append(note)
assert not (all_ids & {e["id"] for e in added})
assert len({e["id"] for e in added}) == len(added) == 13
native["elements"].extend(added)
root["contents"].extend(e["id"] for e in added)
(HERE / "ontouml.json").write_text(json.dumps(native, indent=2, ensure_ascii=False) + "\n")

owl_extra = """
# G3-P4a: two primary bearer-to-Mode Characterizations and derived inverse query routes.
cmpe:organizationHasSupplyCapacity a owl:ObjectProperty ;
    rdfs:domain cmpe:Organization ; rdfs:range cmpe:SupplyCapacity ;
    owl:inverseOf cmpe:capacityOrganizationBearer .
cmpe:facilityHasSupplyCapacity a owl:ObjectProperty ;
    rdfs:domain cmpe:Facility ; rdfs:range cmpe:SupplyCapacity ;
    owl:inverseOf cmpe:capacityFacilityBearer .
cmpe:capacityOrganizationBearer a owl:ObjectProperty ;
    rdfs:domain cmpe:SupplyCapacity ; rdfs:range cmpe:Organization ;
    rdfs:subPropertyOf cmpe:capacityBearer .
cmpe:capacityFacilityBearer a owl:ObjectProperty ;
    rdfs:domain cmpe:SupplyCapacity ; rdfs:range cmpe:Facility ;
    rdfs:subPropertyOf cmpe:capacityBearer .
cmpe:capacityBearer rdfs:range [ a owl:Class ;
        owl:unionOf ( cmpe:Organization cmpe:Facility ) ] .
cmpe:SupplyCapacity rdfs:subClassOf
    [ a owl:Restriction ; owl:onProperty cmpe:capacityBearer ;
      owl:cardinality "1"^^xsd:nonNegativeInteger ],
    [ a owl:Class ; owl:unionOf (
        [ a owl:Restriction ; owl:onProperty cmpe:capacityOrganizationBearer ;
          owl:someValuesFrom cmpe:Organization ]
        [ a owl:Restriction ; owl:onProperty cmpe:capacityFacilityBearer ;
          owl:someValuesFrom cmpe:Facility ]
      ) ] .
"""
original_owl = OWL_FILE.read_text()
(HERE / "active.ttl").write_text(original_owl.rstrip() + "\n\n" + owl_extra.lstrip())

shapes_extra = r'''
# G3-P4a: read the two primary Characterizations in the bearer-to-Mode direction.
cmpe:SupplyCapacityTypedBearerShape a sh:NodeShape ;
    sh:targetClass cmpe:SupplyCapacity ;
    sh:not [ sh:class cmpe:SupplyCapacityObservationResult ] ;
    sh:property [
        sh:path [ sh:alternativePath (
            [ sh:inversePath cmpe:organizationHasSupplyCapacity ]
            [ sh:inversePath cmpe:facilityHasSupplyCapacity ] ) ] ;
        sh:minCount 1 ; sh:maxCount 1 ;
        sh:xone ( [ sh:class cmpe:Organization ] [ sh:class cmpe:Facility ] )
    ] ;
    sh:xone (
        [ sh:property [ sh:path [ sh:inversePath cmpe:organizationHasSupplyCapacity ] ;
                        sh:minCount 1 ; sh:maxCount 1 ; sh:class cmpe:Organization ] ;
          sh:property [ sh:path [ sh:inversePath cmpe:facilityHasSupplyCapacity ] ;
                        sh:maxCount 0 ] ]
        [ sh:property [ sh:path [ sh:inversePath cmpe:facilityHasSupplyCapacity ] ;
                        sh:minCount 1 ; sh:maxCount 1 ; sh:class cmpe:Facility ] ;
          sh:property [ sh:path [ sh:inversePath cmpe:organizationHasSupplyCapacity ] ;
                        sh:maxCount 0 ] ]
    ) .

cmpe:OrganizationCapacitySubjectShape a sh:NodeShape ;
    sh:targetSubjectsOf cmpe:organizationHasSupplyCapacity ;
    sh:class cmpe:Organization ;
    sh:property [ sh:path cmpe:organizationHasSupplyCapacity ;
                  sh:class cmpe:SupplyCapacity ;
                  sh:not [ sh:class cmpe:SupplyCapacityObservationResult ] ] .
cmpe:FacilityCapacitySubjectShape a sh:NodeShape ;
    sh:targetSubjectsOf cmpe:facilityHasSupplyCapacity ;
    sh:class cmpe:Facility ;
    sh:property [ sh:path cmpe:facilityHasSupplyCapacity ;
                  sh:class cmpe:SupplyCapacity ;
                  sh:not [ sh:class cmpe:SupplyCapacityObservationResult ] ] .

# Explicit derived-query triples must reflect the primary graph. Typed-only
# primary assertions are admitted; OWL can infer the query properties.
cmpe:CapacityDerivedQueryAdmissionShape a sh:NodeShape ;
    sh:targetSubjectsOf cmpe:capacityBearer,
                        cmpe:capacityOrganizationBearer,
                        cmpe:capacityFacilityBearer ;
    sh:class cmpe:SupplyCapacity ;
    sh:sparql [
        sh:message "capacityBearer must be grounded in a typed primary Characterization" ;
        sh:select """
            PREFIX cmpe: <https://w3id.org/cm-pharme/2.1/>
            SELECT $this WHERE {
                $this cmpe:capacityBearer ?bearer .
                FILTER NOT EXISTS { ?bearer cmpe:organizationHasSupplyCapacity $this }
                FILTER NOT EXISTS { ?bearer cmpe:facilityHasSupplyCapacity $this }
            }
        """
    ] ;
    sh:sparql [
        sh:message "capacityOrganizationBearer must reflect organizationHasSupplyCapacity" ;
        sh:select """
            PREFIX cmpe: <https://w3id.org/cm-pharme/2.1/>
            SELECT $this WHERE {
                $this cmpe:capacityOrganizationBearer ?bearer .
                FILTER NOT EXISTS { ?bearer cmpe:organizationHasSupplyCapacity $this }
            }
        """
    ] ;
    sh:sparql [
        sh:message "capacityFacilityBearer must reflect facilityHasSupplyCapacity" ;
        sh:select """
            PREFIX cmpe: <https://w3id.org/cm-pharme/2.1/>
            SELECT $this WHERE {
                $this cmpe:capacityFacilityBearer ?bearer .
                FILTER NOT EXISTS { ?bearer cmpe:facilityHasSupplyCapacity $this }
            }
        """
    ] .
'''
(HERE / "constraints.ttl").write_text(SHAPES_FILE.read_text().rstrip() + "\n\n" + shapes_extra.lstrip())

before = Graph().parse(OWL_FILE, format="turtle")
after = Graph().parse(HERE / "active.ttl", format="turtle")
classes = {e["id"] for e in native["elements"] if e["type"] == "Class" and e["stereotype"] != "datatype"}
props = {e["name"]["en"] for e in native["elements"] if e["type"] == "BinaryRelation"}
owl_classes = {str(s)[len(str(CM)):] for s in after.subjects(RDF.type, OWL.Class)
               if isinstance(s, URIRef) and str(s).startswith(str(CM))}
owl_props = {str(s)[len(str(CM)):] for s in after.subjects(RDF.type, OWL.ObjectProperty)
             if isinstance(s, URIRef) and str(s).startswith(str(CM))}
assert classes == owl_classes and len(classes) == 138
assert props == owl_props and len(props) == 86
assert len(native["elements"]) == 536
assert len(Graph().parse(HERE / "constraints.ttl", format="turtle")) > len(Graph().parse(SHAPES_FILE, format="turtle"))
manifest = {
    "inputs": {"native_sha256": sha(NATIVE), "owl_sha256": sha(OWL_FILE), "shacl_sha256": sha(SHAPES_FILE)},
    "outputs": {"native_sha256": sha(HERE / "ontouml.json"), "owl_sha256": sha(HERE / "active.ttl"), "shacl_sha256": sha(HERE / "constraints.ttl")},
    "native_elements_before_after": [523, 536],
    "owl_named_classes": 138, "native_and_owl_object_property_names": 86,
    "native_additions": [e["id"] for e in added],
    "primary_routes": ["organizationHasSupplyCapacity", "facilityHasSupplyCapacity"],
    "derived_inverse_routes": ["capacityOrganizationBearer", "capacityFacilityBearer"],
    "common_query_surface": "capacityBearer",
    "closed_graph_xor": "SHACL two primary inverse paths, exactly one typed bearer, explicit query assertions grounded",
    "open_world_xor": "OWL exact-one common bearer with a disjunction of typed route existentials; missing explicit ABox bearer stays consistent under OWA"
}
(HERE / "integration-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps({k: v for k, v in manifest.items() if k != "inputs" and k != "outputs"}, indent=2))
