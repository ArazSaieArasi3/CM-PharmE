"""Bounded source-graph checks for G3-3-B3; never an official anti-pattern verdict."""
import collections
import itertools
import json
import sys
from pathlib import Path

BASE = Path(__file__).parent
MODEL_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else BASE / "b2-nature-overlay.json"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else BASE / "g3-3-b3-pattern-closure"
OUT.mkdir(exist_ok=True)
model = json.loads(MODEL_PATH.read_text())
elements = {x["id"]: x for x in model["elements"]}
classes = {k: v for k, v in elements.items() if v["type"] == "Class"}
parents = collections.defaultdict(set)
children = collections.defaultdict(set)
for x in model["elements"]:
    if x["type"] == "Generalization" and x["specific"] in classes and x["general"] in classes:
        parents[x["specific"]].add(x["general"])
        children[x["general"]].add(x["specific"])

def closure(start, links):
    seen, pending = set(), list(links[start])
    while pending:
        item = pending.pop()
        if item not in seen:
            seen.add(item)
            pending.extend(links[item])
    return seen

def is_a(child, parent):
    return child == parent or parent in closure(child, parents)

def bounds(card):
    if card is None:
        return None
    halves = card.split("..")
    lo = int(halves[0]) if len(halves) > 1 else int(card)
    hi = float("inf") if halves[-1] == "*" else int(halves[-1])
    return lo, hi

rels = []
for x in model["elements"]:
    if x["type"] == "BinaryRelation":
        a, b = (elements[p] for p in x["properties"])
        rels.append({"name": x["name"]["en"], "id": x["id"], "stereotype": x["stereotype"],
                     "source": a["propertyType"], "target": b["propertyType"],
                     "source_card": a["cardinality"], "target_card": b["cardinality"]})
rels_by_name = {r["name"]: r for r in rels}

# ImpAbs: a trigger is an invitation to ask which subtype-specific multiplicity
# or meta-property is warranted. An existing subsetting relation is evidence,
# not proof that the whole general association is sufficiently constrained.
impabs = []
for r in rels:
    for end in ("source", "target"):
        typ = r[end]
        b = bounds(r[end + "_card"])
        if typ not in classes or b is None or b[1] <= 1:
            continue
        descendants = sorted(closure(typ, children))
        if len(descendants) < 2:
            continue
        specializing = []
        for s in rels:
            if s is r or s["source"] not in classes or s["target"] not in classes:
                continue
            if is_a(s["source"], r["source"]) and is_a(s["target"], r["target"]):
                if s["source"] != r["source"] or s["target"] != r["target"]:
                    specializing.append({"relation": s["name"], "source": s["source"],
                                         "target": s["target"], "cardinality_at_end": s[end + "_card"]})
        impabs.append({"relation": r["name"], "end": end, "type": typ,
                       "cardinality": r[end + "_card"], "descendants": descendants,
                       "specializing_associations": specializing,
                       "known_enforcement": "base RDF SHACL checks endpoint class; no subtype-specific cardinality for this broad association"
                           if r["stereotype"] is None else
                           "focal mediation SHACL checks relator's required end; specialized contextual subset may apply",
                       "recommendation": "Keep broad relation provisionally; decide subtype-specific lower/upper bounds and meta-properties from source examples, then encode only supported restrictions.",
                       "decision": "PENDING_SCIENTIFIC_ADJUDICATION"})
assert len(impabs) == 10

# RelComp: exactly the published *structural precondition* for ordered A,B,
# with the B endpoints specializing either A end. Unknown cardinalities are
# tracked separately, never interpreted as 0 or as unbounded.
comp = []
possible_unknown_a = []
for a in rels:
    if a["source"] not in classes or a["target"] not in classes:
        continue
    card = bounds(a["target_card"])
    if card is not None and not (card[0] > 0 and card[1] > 1):
        continue
    for b in rels:
        if a is b or b["source"] not in classes or b["target"] not in classes:
            continue
        side = [end for end in ("source", "target")
                if is_a(b["source"], a[end]) and is_a(b["target"], a[end])]
        if not side:
            continue
        entry = {"A": a["name"], "A_source": a["source"], "A_target": a["target"],
                 "A_target_card": a["target_card"], "B": b["name"],
                 "B_source": b["source"], "B_target": b["target"], "same_side": side}
        (possible_unknown_a if card is None else comp).append(entry)

# RelOver: source-side relator mediations (including inherited) and a mediated
# pair with known overlap by identical/ancestor types, or a shared ancestor
# whose modeled generalization sets do not explicitly rule the pair out.
meds = [r for r in rels if r["stereotype"] == "mediation" and
        r["source"] in classes and r["target"] in classes]
disjoint_sets = []
for gs in model["elements"]:
    if gs["type"] == "GeneralizationSet" and gs["isDisjoint"]:
        disjoint_sets.append({elements[g]["specific"] for g in gs["generalizations"]})

def overlap_class(a, b):
    if is_a(a, b) or is_a(b, a):
        return "same_or_subtype"
    common = (closure(a, parents) | {a}) & (closure(b, parents) | {b})
    if not common:
        return None
    if any(any(is_a(a, x) for x in gs) and any(is_a(b, y) for y in gs)
           and not any(is_a(a, x) and is_a(b, x) for x in gs)
           for gs in disjoint_sets):
        return None
    return "possible_shared_ancestor_without_declared_disjointness"

over = []
for relator, c in classes.items():
    if c["stereotype"] != "relator":
        continue
    mm = [r for r in meds if is_a(relator, r["source"])]
    if len(mm) < 2:
        continue
    overlaps = [{"left": a["name"], "left_type": a["target"],
                 "right": b["name"], "right_type": b["target"], "basis": kind}
                for a,b in itertools.combinations(mm, 2)
                if (kind := overlap_class(a["target"], b["target"]))]
    if not overlaps:
        continue
    known = [bounds(r["target_card"])[1] for r in mm if bounds(r["target_card"]) is not None]
    unknown = [r["name"] for r in mm if bounds(r["target_card"]) is None]
    entry = {"relator": relator, "mediations": [{"name": r["name"],
              "mediated_type": r["target"], "mediated_end_card": r["target_card"]} for r in mm],
             "overlapping_pairs": overlaps, "known_upper_sum": "unbounded" if any(x == float("inf") for x in known) else sum(known),
             "unknown_upper_mediations": unknown,
             "upper_sum_gt_two": True if sum(known) > 2 else (None if unknown else False),
             "overlap_status": "potential only; individual co-instantiation and disjointness need semantic review"}
    over.append(entry)

out = {"scope": "B3 bounded structural checks on B2 native review overlay; not an official full anti-pattern detector",
       "model_elements": len(elements), "relations": len(rels),
       "typed_relations": sum(r["source"] in classes and r["target"] in classes for r in rels),
       "relation_missing_cardinality": sum(r["source_card"] is None or r["target_card"] is None for r in rels),
       "ImpAbs": {"trigger_end_count": len(impabs), "distinct_relations": len({r["relation"] for r in impabs}), "rows": impabs},
       "RelComp": {"known_cardinality_candidate_pairs": len(comp), "candidates": comp,
                   "unknown_A_target_cardinality_structural_pairs": len(possible_unknown_a),
                   "unknown_cardinality_pairs": possible_unknown_a},
       "RelOver": {"relators_with_potential_overlap": len(over),
                   "known_upper_sum_gt_two": sum(x["upper_sum_gt_two"] is True for x in over),
                   "unknown_upper_sum": sum(x["upper_sum_gt_two"] is None for x in over), "rows": over},
       "official_detector_status": "NOT_RUN", "scientific_signoff": "PENDING"}
(OUT / "structural-results.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({"ImpAbs": len(impabs), "RelComp": len(comp),
                  "RelComp_unknown_card": len(possible_unknown_a), "RelOver_overlap": len(over),
                  "RelOver_sum_gt_two": out["RelOver"]["known_upper_sum_gt_two"],
                  "RelOver_unknown_sum": out["RelOver"]["unknown_upper_sum"]}, indent=2))
