#!/usr/bin/env python3
"""Build and inspect a non-release CM-PharmE 2.1 design candidate.

The candidate is a full, separate namespace snapshot. No 2.0 module, frozen
evaluation result, mapping, or production endpoint is modified.
"""
from __future__ import annotations

import json
from pathlib import Path

from rdflib import Graph, Namespace, OWL, RDF, RDFS, URIRef

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "v2/ontology/source/modules"
TARGET = ROOT / "v2/ontology/candidates/2.1.0-alpha.0-review/modules"
BASE_REGISTRY = ROOT / "v2/ontouml/cm-pharme-v2.conceptual-model.json"
REGISTRY = ROOT / "v2/ontology/candidates/2.1.0-alpha.0-review/conceptual-model.json"
BASE_PUML = ROOT / "v2/research/w4/integrated-ontouml-review-projection.puml"
PUML = ROOT / "v2/ontology/candidates/2.1.0-alpha.0-review/model-review.puml"
OLD = "https://w3id.org/cm-pharme/2.0/"
NEW = "https://w3id.org/cm-pharme/2.1/"
CMPE = Namespace(NEW)
CMMETA = Namespace(NEW + "meta/")


def once(content: str, old: str, new: str) -> str:
    if content.count(old) != 1:
        raise ValueError(f"Expected exactly one source fragment: {old[:100]}")
    return content.replace(old, new)


def generate() -> None:
    TARGET.mkdir(parents=True, exist_ok=True)
    for source in sorted(SOURCE.glob("*.ttl")):
        content = source.read_text(encoding="utf-8").replace(OLD, NEW)
        if source.name == "00-metadata.ttl":
            content = content.replace("2.0.0-alpha.1", "2.1.0-alpha.0-review")
            content = content.replace("CM-PharmE 2.0 Formal Ontology", "CM-PharmE 2.1 Design Candidate")
            content = content.replace("Gate-D-preserving formalization of the CM-PharmE 2.0 pharmaceutical ecosystem conceptual model.", "Non-release review snapshot derived from the frozen CM-PharmE 2.0 baseline; semantics remain provisional.")
            content = content.replace('"W5 Formal Gate candidate"', '"2.1 design candidate; human gate pending"')
            content = content.replace('"2026-08-19"^^xsd:date', '"2026-10-04"^^xsd:date')
        if source.name in {"10-core.ttl", "20-xinfra.ttl"}:
            content = content.replace('"Gate-D-2026-08-19"', '"2.1.0-alpha.0-review"')
        if source.name == "20-xinfra.ttl":
            for name in ("withinRegion", "withinCountry"):
                content = once(content, f"cmpe:{name} a owl:ObjectProperty ;",
                               f"cmpe:{name} a owl:ObjectProperty, owl:IrreflexiveProperty ;")
        if source.name == "30-extensions.ttl":
            content = once(content,
                "cmpe:AlternativeMedicinalProductRole a owl:Class ; rdfs:subClassOf cmpe:MedicinalProduct, cmpe:EcosystemParticipant ;",
                "cmpe:AlternativeMedicinalProductRole a owl:Class ; rdfs:subClassOf cmpe:MedicinalProduct ;")
            content += '''
# 2.1 review-only corrections: W4 already describes these participant/bearer patterns.
# These are candidate commitments. Missing concrete role specializations and governed
# target typing still require author decisions before an OntoUML release claim.
cmpe:vulnerabilityBearer a owl:ObjectProperty ; rdfs:domain cmpe:Vulnerability ; rdfs:range cmpe:AssetAtRisk .
cmpe:capabilityBearer a owl:ObjectProperty ; rdfs:domain cmpe:EnterpriseCapability ; rdfs:range cmpe:Organization .
cmpe:oversightAuthorityRole a owl:ObjectProperty ; rdfs:domain cmpe:RegulatoryOversight ; rdfs:range cmpe:RegulatoryAuthorityRole .
cmpe:oversightGovernedEntity a owl:ObjectProperty ; rdfs:domain cmpe:RegulatoryOversight .
cmpe:partnershipParticipant a owl:ObjectProperty ; rdfs:domain cmpe:StrategicPartnershipAgreement ; rdfs:range cmpe:Organization .

cmpe:Vulnerability rdfs:subClassOf [ a owl:Restriction ; owl:onProperty cmpe:vulnerabilityBearer ; owl:qualifiedCardinality "1"^^xsd:nonNegativeInteger ; owl:onClass cmpe:AssetAtRisk ] .
cmpe:EnterpriseCapability rdfs:subClassOf [ a owl:Restriction ; owl:onProperty cmpe:capabilityBearer ; owl:qualifiedCardinality "1"^^xsd:nonNegativeInteger ; owl:onClass cmpe:Organization ] .
cmpe:StrategicPartnershipAgreement rdfs:subClassOf [ a owl:Restriction ; owl:onProperty cmpe:partnershipParticipant ; owl:minQualifiedCardinality "2"^^xsd:nonNegativeInteger ; owl:onClass cmpe:Organization ] .
'''
        (TARGET / source.name).write_text(content, encoding="utf-8")

    model = json.loads(BASE_REGISTRY.read_text(encoding="utf-8"))
    model.update(model_id="cm-pharme-2.1-review-candidate", model_version="2.1.0-alpha.0-review", namespace=NEW,
                 representation_note="Separate project-native design candidate, not official OntoUML JSON. Human approval and formal validation remain pending.")
    REGISTRY.write_text(json.dumps(model, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    puml = BASE_PUML.read_text(encoding="utf-8")
    puml = once(puml, "@startuml CM_PharmE_V2_W4_Review_Projection", "@startuml CM_PharmE_V21_Design_Candidate")
    puml = once(puml, "IdAssignment -- IdValue : <<mediation>>", "IdAssignment --> IdValue : hasIdentifierValue <<value>>")
    puml = once(puml, "ContextClass --> Product : contextClassificationProduct", "ContextClass -- Product : <<mediation>> contextClassificationProduct")
    puml = once(puml, "EvidenceSupport --> SourceRecord : evidenceRecord", "EvidenceSupport -- SourceRecord : <<mediation>> evidenceRecord")
    puml = once(puml, "ContextClass -- Product : <<mediation>> contextClassificationProduct",
                 "ContextClass -- Product : <<mediation>> contextClassificationProduct\nContextClass -- ClassEntry : <<mediation>> contextClassificationEntry")
    puml = once(puml, "Partnership -- Organization : <<mediation>>", "Partnership \"1\" -- \"2..*\" Organization : <<mediation>> partnershipParticipant")
    puml = once(puml, "RegulatoryOversight -- RegAuthorityRole : <<mediation>>", "RegulatoryOversight -- RegAuthorityRole : <<mediation>> oversightAuthorityRole")
    puml = once(puml, "Organization -- Capability : <<characterization>>", "Organization \"1\" -- Capability : <<characterization>> capabilityBearer")
    puml = once(puml, "AssetAtRisk -- Vulnerability : <<characterization>>", "AssetAtRisk \"1\" -- Vulnerability : <<characterization>> vulnerabilityBearer")
    puml = once(puml, "Product <|-- AlternativeRole", "Product <|-- AlternativeRole\n' AlternativeRole does not specialize EcosystemParticipant in the formal candidate.")
    puml = once(puml, "' Corrected visualization of existing W5 relations only; not new 2.1 semantics.",
                "' Existing W5 links omitted from the original overview are shown here.")
    puml = once(puml, "@enduml", """note right of IdAssignment
  identifierEntity must mediate a concrete identified bearer;
  its polymorphic end and multiplicity await author review.
  Identifier Value is a value, never a mediated individual.
end note

note right of RegulatoryOversight
  Governed end is polymorphic; two distinct mediated
  individuals and their types require author review.
end note

@enduml""")
    PUML.write_text(puml, encoding="utf-8")


def validate() -> dict:
    g = Graph()
    files = sorted(TARGET.glob("*.ttl"))
    if len(files) != 6:
        raise ValueError("Candidate must contain six full modules")
    for path in files:
        g.parse(path, format="turtle")
    model = json.loads(REGISTRY.read_text(encoding="utf-8"))
    concepts = {CMPE[name]: stereotype for pairs in model["modules"].values() for name, stereotype in pairs}
    if len(concepts) != 87:
        raise ValueError("Concept inventory must remain unchanged pending review")
    for concept, stereotype in concepts.items():
        if (concept, CMMETA.ontoumlStereotype, None) not in g:
            raise ValueError(f"No stereotype: {concept}")
        if stereotype not in {str(v) for v in g.objects(concept, CMMETA.ontoumlStereotype)}:
            raise ValueError(f"Stereotype mismatch: {concept}")
    if (CMPE.AlternativeMedicinalProductRole, RDFS.subClassOf, CMPE.EcosystemParticipant) in g:
        raise ValueError("Product role must not inherit actor participation")
    if (CMPE.AlternativeMedicinalProductRole, RDFS.subClassOf, CMPE.MedicinalProduct) not in g:
        raise ValueError("Product role lost its identity provider")
    expected = {
        "vulnerabilityBearer": ("Vulnerability", "AssetAtRisk"),
        "capabilityBearer": ("EnterpriseCapability", "Organization"),
        "oversightAuthorityRole": ("RegulatoryOversight", "RegulatoryAuthorityRole"),
        "oversightGovernedEntity": ("RegulatoryOversight", None),
        "partnershipParticipant": ("StrategicPartnershipAgreement", "Organization"),
    }
    for property_name, (domain, range_) in expected.items():
        prop = CMPE[property_name]
        if (prop, RDF.type, OWL.ObjectProperty) not in g or (prop, RDFS.domain, CMPE[domain]) not in g:
            raise ValueError(f"Property definition missing: {property_name}")
        if range_ and (prop, RDFS.range, CMPE[range_]) not in g:
            raise ValueError(f"Property range missing: {property_name}")
        if not range_ and any(g.objects(prop, RDFS.range)):
            raise ValueError(f"Do not invent a universal governed entity range: {property_name}")
    for name in ("withinRegion", "withinCountry"):
        if (CMPE[name], RDF.type, OWL.IrreflexiveProperty) not in g:
            raise ValueError(f"Missing BinOver self-containment guard: {name}")
    for concept, prop, bound, filler, value in (
        ("Vulnerability", "vulnerabilityBearer", OWL.qualifiedCardinality, "AssetAtRisk", 1),
        ("EnterpriseCapability", "capabilityBearer", OWL.qualifiedCardinality, "Organization", 1),
        ("StrategicPartnershipAgreement", "partnershipParticipant", OWL.minQualifiedCardinality, "Organization", 2),
    ):
        restrictions = [r for r in g.objects(CMPE[concept], RDFS.subClassOf)
                        if (r, RDF.type, OWL.Restriction) in g and (r, OWL.onProperty, CMPE[prop]) in g]
        if not any(str(g.value(r, bound)) == str(value) and (r, OWL.onClass, CMPE[filler]) in g for r in restrictions):
            raise ValueError(f"Missing bearer/participant restriction for {concept}")
    for left, right in model["protected_distinctions"]:
        a, b = CMPE[left], CMPE[right]
        direct = (a, OWL.disjointWith, b) in g or (b, OWL.disjointWith, a) in g
        if not direct:
            from rdflib.collection import Collection
            direct = any(a in vals and b in vals for n in g.subjects(RDF.type, OWL.AllDisjointClasses)
                         if (members := g.value(n, OWL.members)) is not None
                         for vals in [set(Collection(g, members))])
        if not direct:
            raise ValueError(f"Protected distinction lost: {left}!={right}")
    counts = {"classes": sum((c, RDF.type, OWL.Class) in g for c in concepts),
              "datatypes": sum((c, RDF.type, RDFS.Datatype) in g for c in concepts),
              "object_properties": len(set(g.subjects(RDF.type, OWL.ObjectProperty)))}
    if counts != {"classes": 81, "datatypes": 6, "object_properties": 57}:
        raise ValueError(f"Unexpected candidate quantity: {counts}")
    return {"candidate_version": model["model_version"], "namespace": model["namespace"],
            "counts": counts, "files_parsed": len(files), "review_status": "provisional; not OntoUML certified or released"}


if __name__ == "__main__":
    generate()
    print(json.dumps(validate(), indent=2))
