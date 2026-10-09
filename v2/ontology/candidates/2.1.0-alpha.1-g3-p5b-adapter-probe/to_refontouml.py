#!/usr/bin/env python3
"""Strict prototype: typed/known-cardinality flat OntoUML subset -> legacy XMI.

Deliberately refuses unsupported elements instead of manufacturing semantics.
This is a structural bridge probe, NOT a full-fidelity converter.
"""
import copy
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

XMI = "http://www.omg.org/XMI"
XSI = "http://www.w3.org/2001/XMLSchema-instance"
REF = "http://nemo.inf.ufes.br/ontouml/refontouml"
ET.register_namespace("xmi", XMI)
ET.register_namespace("xsi", XSI)
ET.register_namespace("RefOntoUML", REF)
STEREOTYPES = {"kind": "Kind", "subkind": "SubKind", "role": "Role",
               "roleMixin": "RoleMixin", "relator": "Relator", "mode": "Mode",
               "quality": "Quality", "datatype": "DataType"}
RELATIONS = {None: "Association", "mediation": "Mediation",
             "characterization": "Characterization", "material": "MaterialAssociation"}


def xid(original):
    assert re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]*", original), original
    return "_cmpe_" + original


def typ(name):
    return "RefOntoUML:" + name


def card(value):
    if value is None:
        raise ValueError("Unspecified cardinality cannot safely become an EMF default")
    m = re.fullmatch(r"(\d+)(?:\.\.(\d+|\*))?", value)
    if not m:
        raise ValueError(f"Unsupported cardinality {value!r}")
    lo = int(m.group(1))
    hi = m.group(2) or m.group(1)
    hi = -1 if hi == "*" else int(hi)
    if hi != -1 and hi < lo:
        raise ValueError(f"Inverted cardinality {value!r}")
    return lo, hi


def name(e):
    n = e.get("name")
    return n.get("en") or next(iter(n.values()), e["id"]) if isinstance(n, dict) else n or e["id"]


def convert(model):
    elements = {e["id"]: e for e in model["elements"]}
    assert len(elements) == len(model["elements"])
    classes = {k: e for k, e in elements.items() if e["type"] == "Class"}
    relations = {k: e for k, e in elements.items() if e["type"] == "BinaryRelation"}
    generals = [e for e in elements.values() if e["type"] == "Generalization"]
    sets = [e for e in elements.values() if e["type"] == "GeneralizationSet"]
    allowed = {"Package", "Class", "BinaryRelation", "Property", "Generalization", "GeneralizationSet"}
    unsupported = sorted((e["id"], e["type"]) for e in elements.values() if e["type"] not in allowed)
    if unsupported:
        raise ValueError(f"Unsupported element kinds: {unsupported[:4]}")
    if set(e.get("stereotype") for e in classes.values()) - set(STEREOTYPES):
        raise ValueError("Class stereotype is absent in archived RefOntoUML Ecore")
    if set(e.get("stereotype") for e in relations.values()) - set(RELATIONS):
        raise ValueError("Relation stereotype is absent in archived RefOntoUML Ecore")
    class_ids = set(classes)
    parent_of = defaultdict(list)
    for g in generals:
        if g["specific"] not in classes or g["general"] not in classes:
            raise ValueError(f"Unresolved generalization {g['id']}")
        parent_of[g["specific"]].append(g)
    sets_for = defaultdict(list)
    for gs in sets:
        for g in gs["generalizations"]:
            if g not in elements or elements[g]["type"] != "Generalization":
                raise ValueError(f"Unresolved generalization set member {g}")
            sets_for[g].append(gs["id"])
    if any(len(ids) > 1 for ids in sets_for.values()):
        raise ValueError("Generalization belongs to multiple sets, unsupported by this adapter")
    root = ET.Element(f"{{{REF}}}Package", {f"{{{XMI}}}version": "2.0",
                                            f"{{{XMI}}}id": xid(model["root"]),
                                            "name": name(elements[model["root"]]),
                                            "visibility": "public"})
    loss = []
    for c in classes.values():
        attributes = {f"{{{XSI}}}type": typ(STEREOTYPES[c['stereotype']]),
                      f"{{{XMI}}}id": xid(c["id"]), "name": name(c),
                      "visibility": "public"}
        if c.get("isAbstract"):
            attributes["isAbstract"] = "true"
        cls = ET.SubElement(root, "packagedElement", attributes)
        if c.get("restrictedTo"):
            loss.append({"id": c["id"], "field": "restrictedTo",
                         "values": c["restrictedTo"],
                         "reason": "Legacy RefOntoUML class does not encode modern nature restrictions"})
        for g in parent_of[c["id"]]:
            attrs = {f"{{{XMI}}}id": xid(g["id"]), "general": xid(g["general"])}
            if sets_for[g["id"]]:
                attrs["generalizationSet"] = xid(sets_for[g["id"]][0])
            ET.SubElement(cls, "generalization", attrs)
    for r in relations.values():
        ends = [elements[k] for k in r["properties"]]
        if len(ends) != 2 or any(e["type"] != "Property" or e["propertyType"] not in class_ids for e in ends):
            raise ValueError(f"Relation {r['id']} has an untyped or unresolved end")
        for e in ends:
            card(e["cardinality"])
            if e.get("subsettedProperties") or e.get("redefinedProperties"):
                raise ValueError(f"Relation {r['id']} has subsetting/redefinition not supported by this probe")
        attrs = {f"{{{XSI}}}type": typ(RELATIONS[r.get("stereotype")]),
                 f"{{{XMI}}}id": xid(r["id"]), "name": name(r),
                 "visibility": "public",
                 "memberEnd": " ".join(xid(e["id"]) for e in ends)}
        if r.get("isDerived"):
            attrs["isDerived"] = "true"
        relation = ET.SubElement(root, "packagedElement", attrs)
        for e in ends:
            props = {f"{{{XMI}}}id": xid(e["id"]),
                     "name": name(e), "visibility": "public",
                     "type": xid(e["propertyType"]),
                     "association": xid(r["id"])}
            if e.get("isReadOnly") is True:
                props["isReadOnly"] = "true"
            own = ET.SubElement(relation, "ownedEnd", props)
            lo, hi = card(e["cardinality"])
            ET.SubElement(own, "upperValue", {f"{{{XSI}}}type": typ("LiteralUnlimitedNatural"),
                                                f"{{{XMI}}}id": xid(e["id"] + "-upper"),
                                                "value": str(hi)})
            ET.SubElement(own, "lowerValue", {f"{{{XSI}}}type": typ("LiteralInteger"),
                                                f"{{{XMI}}}id": xid(e["id"] + "-lower"),
                                                "value": str(lo)})
    for gs in sets:
        attrs = {f"{{{XSI}}}type": typ("GeneralizationSet"),
                 f"{{{XMI}}}id": xid(gs["id"]), "name": name(gs),
                 "visibility": "public",
                 "generalization": " ".join(xid(k) for k in gs["generalizations"])}
        if gs.get("isDisjoint"):
            attrs["isDisjoint"] = "true"
        if gs.get("isComplete"):
            attrs["isCovering"] = "true"
        ET.SubElement(root, "packagedElement", attrs)
    ET.indent(root, space="  ")
    xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    return xml, {"classes": len(classes), "binary_relations": len(relations),
                 "generalizations": len(generals), "generalization_sets": len(sets),
                 "ends": len(relations) * 2, "known_semantic_losses": loss,
                 "scope": "Strict structural subset. Never claim full native or OWL equivalence."}


if __name__ == "__main__":
    native_path, xmi_path, report_path = map(Path, sys.argv[1:4])
    xml, report = convert(json.loads(native_path.read_text()))
    xmi_path.write_bytes(xml)
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report))
