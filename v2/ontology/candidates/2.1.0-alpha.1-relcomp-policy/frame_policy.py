"""CMPE-RelComp-PositiveLowerBound/1.0.0: one explicit legacy witness frame.

This is an independent scoped predicate, not a full-model anti-pattern detector.
"""
from pathlib import Path
import xml.etree.ElementTree as ET

PROFILE = "CMPE-RelComp-PositiveLowerBound/1.0.0"
XMI = "{http://www.omg.org/XMI}"
XSI = "{http://www.w3.org/2001/XMLSchema-instance}"


def read_model(path):
    root = ET.parse(path).getroot()
    ids = {}
    for element in root.iter():
        key = element.get(XMI + "id")
        if key:
            if key in ids: raise ValueError("duplicate_id")
            ids[key] = element
        if element.get("subsettedProperty") or element.get("redefinedProperty"):
            raise ValueError("unsupported_subsetting")
    classes, relations, parents = {}, {}, {}
    for element in root.findall("packagedElement"):
        key = element.get(XMI + "id")
        kind = element.get(XSI + "type", "").removeprefix("RefOntoUML:")
        if not key: raise ValueError("missing_element_id")
        if kind in {"Kind", "SubKind"}:
            classes[key] = kind
            parents[key] = [g.get("general") for g in element.findall("generalization")]
        elif kind == "Association":
            ends = element.findall("ownedEnd")
            order = element.get("memberEnd", "").split()
            if len(ends) != 2 or len(order) != 2 or set(order) != {x.get(XMI+"id") for x in ends}:
                raise ValueError("unbound_binary_ends")
            parsed = {}
            for end in ends:
                lower, upper = end.find("lowerValue"), end.find("upperValue")
                if lower is None or lower.get("value") is None: raise ValueError("missing_lower")
                if upper is None or upper.get("value") is None: raise ValueError("missing_upper")
                lo, hi = int(lower.get("value")), int(upper.get("value"))
                if lo < 0: raise ValueError("negative_lower")
                if hi < -1 or (hi != -1 and hi < lo): raise ValueError("invalid_interval")
                if not end.get("type"): raise ValueError("untyped_end")
                parsed[end.get(XMI+"id")] = {"type": end.get("type"), "lower": lo, "upper": hi}
            relations[key] = {"order": order, "ends": parsed}
        else:
            raise ValueError("unsupported_legacy_element")
    if len(relations) != 2: raise ValueError("outside_two_association_scope")
    for node, direct in parents.items():
        if any(p not in classes for p in direct): raise ValueError("unresolved_parent")
    for relation in relations.values():
        if any(e["type"] not in classes for e in relation["ends"].values()): raise ValueError("untyped_end")
    closure = {}
    def ancestors(key, active):
        if key in active: raise ValueError("cyclic_generalization")
        if key not in closure:
            result = set()
            for parent in parents[key]:
                result.add(parent); result.update(ancestors(parent, active | {key}))
            closure[key] = result
        return closure[key]
    for key in classes: ancestors(key, set())
    return relations, closure


def evaluate_frame(path, outer="outer", inner="inner", shared_end="outerB"):
    relations, closure = read_model(Path(path))
    if outer == inner or outer not in relations or inner not in relations: raise ValueError("unbound_frame")
    if shared_end not in relations[outer]["ends"]: raise ValueError("unbound_shared_end")
    shared = relations[outer]["ends"][shared_end]
    inner_types = [end["type"] for end in relations[inner]["ends"].values()]
    subtype_match = all(t == shared["type"] or shared["type"] in closure[t] for t in inner_types)
    positive_lower = shared["lower"] > 0
    plural_upper = shared["upper"] == -1 or shared["upper"] > 1
    matches = subtype_match and positive_lower and plural_upper
    return {"profile": PROFILE, "outer": outer, "inner": inner, "shared_end": shared_end,
            "serialized_end_index": relations[outer]["order"].index(shared_end),
            "pattern_role_assignment": "selected shared end bound explicitly to ATarget",
            "shared_type": shared["type"], "lower": shared["lower"], "upper": shared["upper"],
            "inner_types": sorted(inner_types), "inner_types_within_shared_type": subtype_match,
            "positive_lower": positive_lower, "plural_upper": plural_upper,
            "frame_match": int(matches), "full_candidate_executed": False}
