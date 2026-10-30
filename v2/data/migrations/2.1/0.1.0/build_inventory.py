"""Read-only, pinned 2.0 W6 versus 2.1 candidate term/mapping inventory."""
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from rdflib import Graph, OWL, RDF, RDFS, SH, BNode, URIRef

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
BASE = ROOT / "v2/ontology/source/modules"
CAND = ROOT / "v2/ontology/candidates/2.1.0-alpha.1-g3-p4a-supply-capacity"
W6 = ROOT / "v2/data"
ORSD = ROOT / "v2/requirements/2.1/orsd/0.2.0/requirements.json"
OLD_NS = "https://w3id.org/cm-pharme/2.0/"
NEW_NS = "https://w3id.org/cm-pharme/2.1/"
PIN = json.loads((HERE / "pinned-inputs.json").read_text())
for path, expected in PIN["sha256"].items():
    actual = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
    assert actual == expected, (path, actual)

g0, g1 = Graph(), Graph().parse(CAND / "active.ttl")
for source in sorted(BASE.glob("*.ttl")):
    g0.parse(source)
s0, s1 = Graph().parse(ROOT / "v2/ontology/shapes/cm-pharme-v2.shacl.ttl"), Graph().parse(CAND / "constraints.ttl")
TYPES = {"class": OWL.Class, "object_property": OWL.ObjectProperty,
         "datatype_property": OWL.DatatypeProperty}

def local(uri, ns):
    value = str(uri)
    return value[len(ns):] if value.startswith(ns) else None

def normalize(term):
    return str(term).replace(OLD_NS, "cmpe:").replace(NEW_NS, "cmpe:")

def signature(g, term):
    """Named domain/range/parent and direct OWL restrictions; not a proof of equivalence."""
    attrs = []
    for predicate in (RDFS.domain, RDFS.range, RDFS.subClassOf, RDFS.subPropertyOf,
                      OWL.inverseOf, OWL.propertyDisjointWith, OWL.disjointWith):
        for value in g.objects(term, predicate):
            if isinstance(value, URIRef):
                attrs.append(f"{normalize(predicate)}={normalize(value)}")
            elif isinstance(value, BNode) and predicate == RDFS.subClassOf:
                op = g.value(value, OWL.onProperty)
                if isinstance(op, BNode): op = g.value(op, OWL.inverseOf)
                card = [(normalize(p), str(v)) for p, v in g.predicate_objects(value)
                        if p in {OWL.minQualifiedCardinality, OWL.maxQualifiedCardinality,
                                 OWL.qualifiedCardinality, OWL.someValuesFrom, OWL.allValuesFrom, OWL.onClass}]
                if op: attrs.append(f"restriction:{normalize(op)}:{sorted(card)}")
    return sorted(set(attrs))

with (W6 / "mappings/ontology-rdb-mapping.csv").open(newline="", encoding="utf-8-sig") as f:
    mappings = list(csv.DictReader(f))
requirements = json.loads(ORSD.read_text())["requirements"]
ids_by_anchor = {}
for req in requirements:
    for anchor in req.get("anchors", []):
        ids_by_anchor.setdefault(anchor, set()).add(req["id"])
mapping_by_term = {}
for m in mappings:
    mapping_by_term.setdefault(local(m["ontology_iri"], OLD_NS), []).append(m["mapping_id"])
schema = (W6 / "db/schema.sql").read_text()
tables = set(re.findall(r"CREATE TABLE\s+(\w+)\s*\(", schema, flags=re.I))

terms = []
counts = {}
for kind, rdf_type in TYPES.items():
    old = {local(x, OLD_NS) for x in g0.subjects(RDF.type, rdf_type)} - {None}
    new = {local(x, NEW_NS) for x in g1.subjects(RDF.type, rdf_type)} - {None}
    counts[kind] = {"w6_2_0": len(old), "candidate_2_1": len(new),
                    "retained_local_name": len(old & new), "added": len(new - old),
                    "absent_in_candidate": len(old - new)}
    for name in sorted(old | new):
        a, b = signature(g0, URIRef(OLD_NS + name)) if name in old else [], signature(g1, URIRef(NEW_NS + name)) if name in new else []
        state = "ADDED_CANDIDATE" if name not in old else "ABSENT_IN_CANDIDATE" if name not in new else "RETAINED_SIGNATURE_CHANGED" if a != b else "RETAINED_SIGNATURE_SAME"
        mids = mapping_by_term.get(name, [])
        terms.append({"kind": kind, "local_name": name, "w6_2_0_iri": OLD_NS + name if name in old else "",
                      "candidate_2_1_iri": NEW_NS + name if name in new else "",
                      "lexical_delta": state, "w6_mapping_ids": ";".join(mids),
                      "orsd_ids_exact_anchor": ";".join(sorted(ids_by_anchor.get(name, []))),
                      "w6_signature": " | ".join(a), "candidate_signature": " | ".join(b),
                      "migration_disposition": "HOLD_SCIENTIFIC_DECISION" if name in new - old or state == "RETAINED_SIGNATURE_CHANGED" else "NO_AUTOMATIC_DROP" if name not in new else "VERIFY_PROJECTION" if mids else "NO_DIRECT_W6_MAPPING"})

def write_csv(path, rows, columns):
    with (HERE / path).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columns)
        w.writeheader()
        w.writerows(rows)

write_csv("term-delta.csv", terms, list(terms[0]))
mapped = []
term_lookup = {(r["kind"], r["local_name"]): r for r in terms}
for m in mappings:
    name = local(m["ontology_iri"], OLD_NS)
    # W6 registry calls M023 a "quality" representation, while the OWL
    # declaration of MatchConfidence is an owl:Class with a Quality stereotype.
    row = term_lookup.get(("class" if m["entity_kind"] == "quality" else m["entity_kind"], name))
    mapped.append({"mapping_id": m["mapping_id"], "w6_iri": m["ontology_iri"],
                   "candidate_iri_by_local_name": NEW_NS + name if row and row["candidate_2_1_iri"] else "",
                   "candidate_term_declared": bool(row and row["candidate_2_1_iri"]),
                   "w6_mapping_status": m["mapping_status"], "rdb_table": m["rdb_table"],
                   "rdb_field_or_join": m["rdb_field_or_join"],
                   "rdb_table_declared": bool(m["rdb_table"] and m["rdb_table"] in tables),
                   "orsd_ids_exact_anchor": ";".join(sorted(ids_by_anchor.get(name, []))),
                   "candidate_signature_delta": row["lexical_delta"] if row else "QUALITY_OR_UNDECLARED_TERM",
                   "migration_disposition": "DEFERRED_NO_TABLE" if not m["rdb_table"] else "REVIEW_SEMANTIC_PROJECTION" if row and row["lexical_delta"] == "RETAINED_SIGNATURE_CHANGED" else "NAMESPACE_AND_REGRESSION_REVIEW"})
write_csv("w6-mapping-crosswalk.csv", mapped, list(mapped[0]))

def shape_rows(g, ns):
    result = set()
    for shape in g.subjects(RDF.type, SH.NodeShape):
        target = g.value(shape, SH.targetClass)
        if not target or not local(target, ns): continue
        for p in g.objects(shape, SH.property):
            path = g.value(p, SH.path)
            if isinstance(path, BNode): path = g.value(path, SH.inversePath)
            if not path: continue
            result.add((local(target, ns), local(path, ns) or normalize(path),
                        str(g.value(p, SH.minCount) or ""), str(g.value(p, SH.maxCount) or ""),
                        normalize(g.value(p, SH["class"])) if g.value(p, SH["class"]) else ""))
    return result

old_shapes, new_shapes = shape_rows(s0, OLD_NS), shape_rows(s1, NEW_NS)
shape_delta = [{"target": t, "path": p, "min_count": mn, "max_count": mx, "value_class": cl,
                "w6_2_0": item in old_shapes, "candidate_2_1": item in new_shapes,
                "disposition": "REVIEW_PROFILE_DELTA"}
               for item in sorted(old_shapes ^ new_shapes) for t, p, mn, mx, cl in [item]]
write_csv("simple-shape-delta.csv", shape_delta, ["target","path","min_count","max_count","value_class","w6_2_0","candidate_2_1","disposition"])

summary = {"schema_version": "1.0", "pinned_w6_commit": PIN["w6_commit"],
           "pinned_candidate_commit": PIN["candidate_commit"],
           "source_module_triples": len(g0), "candidate_owl_triples": len(g1),
           "term_counts": counts, "term_rows": len(terms), "mapping_rows": len(mapped),
           "mapping_2_1_term_declared": sum(x["candidate_term_declared"] for x in mapped),
           "mapping_rdb_table_declared": sum(x["rdb_table_declared"] for x in mapped),
           "changed_simple_shape_records": len(shape_delta),
           "shape_scope_limit": "Simple property constraints only; inverse paths reduced to local name; sh:sparql, qualified constraints, blank-node combinations and full profile equivalence are not compared.",
           "term_scope_limit": "Same local name is a candidate crosswalk only; signatures cover selected explicit OWL predicates and restrictions, not semantic equivalence or accepted version migration.",
           "mapping_scope_limit": "W6 registry rows are asserted design mappings. Table declaration checks do not certify an exporter path, a full SQL schema parse or executed relational coverage."}
(HERE / "inventory-results.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
print(json.dumps(summary["term_counts"], ensure_ascii=False))
