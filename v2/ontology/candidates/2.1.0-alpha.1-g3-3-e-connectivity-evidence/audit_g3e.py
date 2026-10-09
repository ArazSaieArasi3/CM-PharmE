#!/usr/bin/env python3
"""Recompute bounded native/OWL named-class connectivity and NHIF P1 witnesses.

Run with PYTHONPATH containing rdflib, e.g. rdflib 7.6.0. This is a
structural/source audit, not an OntoUML anti-pattern verdict.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import io
import json
from collections import Counter
from pathlib import Path

from rdflib import Graph, OWL, RDF, RDFS, URIRef


HERE = Path(__file__).resolve().parent
BASE = HERE.parent
NS = "https://w3id.org/cm-pharme/2.1/"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def components(nodes: set[str], edges: set[tuple[str, str]]) -> list[list[str]]:
    adjacent = {n: set() for n in nodes}
    for a, b in edges:
        if a not in nodes or b not in nodes:
            raise ValueError(f"Unknown endpoint {a}--{b}")
        if a != b:
            adjacent[a].add(b)
            adjacent[b].add(a)
    found = set()
    groups = []
    for start in sorted(nodes):
        if start in found:
            continue
        stack = [start]
        found.add(start)
        group = []
        while stack:
            node = stack.pop()
            group.append(node)
            for neighbor in sorted(adjacent[node] - found):
                found.add(neighbor)
                stack.append(neighbor)
        groups.append(sorted(group))
    return sorted(groups, key=lambda group: (-len(group), group))


def pair(a: str, b: str) -> tuple[str, str]:
    return tuple(sorted((a, b)))


def native_graph(path: Path):
    source = json.loads(path.read_text())
    elements = {element["id"]: element for element in source["elements"]}
    classes = {k for k, v in elements.items() if v["type"] == "Class" and v["stereotype"] != "datatype"}
    generalizations = {
        (e["specific"], e["general"]) for e in elements.values()
        if e["type"] == "Generalization"
        and e["specific"] in classes and e["general"] in classes
    }
    relations = {}
    for e in elements.values():
        if e["type"] != "BinaryRelation":
            continue
        assert len(e["properties"]) == 2
        ends = [elements[k].get("propertyType") for k in e["properties"]]
        relations[e["name"]["en"]] = {
            "types": ends,
            "stereotype": e.get("stereotype"),
            "id": e["id"],
        }
    typed = {
        (name, types[0], types[1])
        for name, r in relations.items()
        if (types := r["types"]) and all(t in classes for t in types)
    }
    edges = {pair(a, b) for a, b in generalizations} | {
        pair(a, b) for _, a, b in typed
    }
    return classes, generalizations, relations, typed, edges


def owl_graph(path: Path):
    graph = Graph().parse(path, format="turtle")
    classes = {str(x)[len(NS):] for x in graph.subjects(RDF.type, OWL.Class)
               if isinstance(x, URIRef) and str(x).startswith(NS)}
    props = {str(x)[len(NS):] for x in graph.subjects(RDF.type, OWL.ObjectProperty)
             if isinstance(x, URIRef) and str(x).startswith(NS)}
    parents = {
        (str(a)[len(NS):], str(b)[len(NS):])
        for a, b in graph.subject_objects(RDFS.subClassOf)
        if isinstance(a, URIRef) and isinstance(b, URIRef)
        and str(a).startswith(NS) and str(b).startswith(NS)
        and str(a)[len(NS):] in classes and str(b)[len(NS):] in classes
    }
    named = set()
    declared = {}
    for p in props:
        iri = URIRef(NS + p)
        domains = sorted({str(x)[len(NS):] for x in graph.objects(iri, RDFS.domain)
                          if isinstance(x, URIRef) and str(x)[len(NS):] in classes})
        ranges = sorted({str(x)[len(NS):] for x in graph.objects(iri, RDFS.range)
                         if isinstance(x, URIRef) and str(x)[len(NS):] in classes})
        declared[p] = {"domains": domains, "ranges": ranges}
        named.update((p, a, b) for a in domains for b in ranges)
    edges = {pair(a, b) for a, b in parents} | {
        pair(a, b) for _, a, b in named
    }
    return classes, parents, props, named, edges, declared, len(graph)


def load_abox(path: Path):
    raw = path.read_bytes()
    if path.name.endswith(".gz.b64"):
        decoded = gzip.decompress(base64.b64decode(raw.strip(), validate=True))
    else:
        decoded = raw
    graph = Graph().parse(source=io.BytesIO(decoded), format="nt")
    return graph, hashlib.sha256(decoded).hexdigest()


def snapshot(classes, subclass_edges, typed_edges, edges):
    groups = components(classes, edges)
    return {
        "classes": len(classes),
        "named_subclass_edges": len(subclass_edges),
        "typed_object_property_edges": len(typed_edges),
        "distinct_undirected_class_edges": len(edges),
        "components": len(groups),
        "component_sizes": [len(x) for x in groups],
        "largest_component": len(groups[0]),
        "isolates": sorted(x[0] for x in groups if len(x) == 1),
        "nontrivial_components": [x for x in groups if len(x) > 1],
    }


def evaluate(review, abox: Graph, native, owl):
    native_classes, _, native_rels, _, _ = native
    owl_classes, _, owl_props, _, _, declared, _ = owl
    typed_counts = Counter(str(c)[len(NS):] for _, _, c in abox.triples((None, RDF.type, None))
                           if isinstance(c, URIRef) and str(c).startswith(NS))
    rows = []
    for item in review["records"]:
        source, target = item["name"], item["candidate_target"]
        src_count, dst_count = typed_counts[source], typed_counts[target]
        relation = item["candidate_relation"].split(" (")[0]
        current_native = native_rels.get(relation)
        current_owl = declared.get(relation)
        relation_assertions = sum(1 for _ in abox.triples((None, URIRef(NS + relation), None)))
        # A class/type occurrence is insufficient to establish the relation's
        # truthmaker. No row may be promoted on destination instances alone.
        rows.append({
            "class": source,
            "module_from_prior_review": item["module"],
            "prior_review_status": item["review_status"],
            "proposed_relation": relation,
            "proposed_target": target,
            "source_class_in_native_and_OWL": source in native_classes and source in owl_classes,
            "target_class_in_native_and_OWL": target in native_classes and target in owl_classes,
            "sample_direct_instances_of_source": src_count,
            "sample_direct_instances_of_target": dst_count,
            "sample_assertions_of_proposed_property": relation_assertions,
            "existing_native_relation": current_native,
            "existing_OWL_named_endpoints": current_owl,
            "truthmaker_required": item["truthmaker_required"],
            "negative_acceptance_condition": item["negative_acceptance_condition"],
            "real_source_disposition": "NO_RELATION_WITNESS_IN_P1_SAMPLE",
            "ontology_edit_authorized_by_this_audit": False,
        })
    return rows, dict(sorted(typed_counts.items()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--native", type=Path, default=BASE / "g3-3-b2-focused-adjudication/ontouml-b2-review-overlay.json")
    parser.add_argument("--owl", type=Path, default=BASE / "g3-3-c-integrated-validation/active.ttl")
    parser.add_argument("--abox", type=Path, default=BASE / "g3-3-d-real-source-migration/real-source-abox.nt.gz.b64")
    parser.add_argument("--review", type=Path, default=HERE / "source-isolate-review.json")
    parser.add_argument("--out", type=Path, default=HERE / "connectivity-evidence.json")
    args = parser.parse_args()
    native = native_graph(args.native)
    owl = owl_graph(args.owl)
    abox, abox_sha = load_abox(args.abox)
    review = json.loads(args.review.read_text())
    nclasses, nparents, nrels, ntyped, nedges = native
    oclasses, oparents, oprops, otyped, oedges, declared, owl_size = owl
    rows, type_counts = evaluate(review, abox, native, owl)
    nshot = snapshot(nclasses, nparents, ntyped, nedges)
    oshot = snapshot(oclasses, oparents, otyped, oedges)
    assert len(review["records"]) == len(rows) == 14
    assert len({r["class"] for r in rows}) == 14
    assert nclasses == oclasses and len(nclasses) == 138
    assert set(nrels) == oprops and len(nrels) == 82
    assert nparents == oparents and len(nparents) == 99
    assert nshot["isolates"] == oshot["isolates"]
    assert nshot["isolates"] == sorted(r["class"] for r in rows)
    assert all(r["source_class_in_native_and_OWL"] and r["target_class_in_native_and_OWL"] for r in rows)
    assert all(r["sample_direct_instances_of_source"] == 0 and r["sample_assertions_of_proposed_property"] == 0 for r in rows)
    assert len(abox) == 39272 and abox_sha == "939a80c8f3d4342e81c74c193cd9e65dc61b1b7e271ba99856edfd988daebfa9"
    broad_untyped = sorted([
        {"relation": name, "source": r["types"][0], "untyped_target": r["types"][1]}
        for name, r in nrels.items()
        if r["types"][0] in nshot["isolates"] and r["types"][1] is None
    ], key=lambda r: r["relation"])
    assert {x["relation"] for x in broad_untyped} == {
        "baViewRepresents", "capacityBearer", "riskTreatmentAddresses"
    }
    hypothetical = components(nclasses, nedges | {
        pair(r["class"], r["proposed_target"]) for r in rows
    })
    modules = {}
    for module in sorted({r["module_from_prior_review"] for r in rows}):
        group = [r for r in rows if r["module_from_prior_review"] == module]
        modules[module] = {
            "isolated_proposals": len(group),
            "source_class_witnessed": sum(r["sample_direct_instances_of_source"] > 0 for r in group),
            "proposed_relation_witnessed": sum(r["sample_assertions_of_proposed_property"] > 0 for r in group),
            "target_class_witnessed": sum(r["sample_direct_instances_of_target"] > 0 for r in group),
            "classes": [r["class"] for r in group],
        }
    result = {
        "scope": "Named-class topology from direct named subclass and explicit named domain/range object-property edges only; ABox direct rdf:type and proposed predicate assertions only. No inferred edges, anonymous unions, datatype links or source representativeness.",
        "inputs": {
            "native_sha256": sha(args.native),
            "owl_sha256": sha(args.owl),
            "abox_decoded_sha256": abox_sha,
            "prior_review_sha256": sha(args.review),
            "owl_triples": owl_size,
            "abox_triples": len(abox),
        },
        "native": nshot,
        "owl": oshot,
        "comparison": {
            "class_name_sets_equal": nclasses == oclasses,
            "object_property_name_sets_equal": set(nrels) == oprops,
            "named_subclass_edges_equal": nparents == oparents,
            "typed_property_triples_native_only": sorted([list(t) for t in ntyped - otyped]),
            "typed_property_triples_OWL_only": sorted([list(t) for t in otyped - ntyped]),
            "class_graph_edges_native_only": sorted([list(t) for t in nedges - oedges]),
            "class_graph_edges_OWL_only": sorted([list(t) for t in oedges - nedges]),
        },
        "sample": {
            "direct_type_counts": type_counts,
            "sampled_rows": 768,
            "nonrandom_regions_and_periods": 5,
            "no_source_or_proposed_link_witnesses": sum(r["sample_direct_instances_of_source"] == 0 and r["sample_assertions_of_proposed_property"] == 0 for r in rows),
            "target_only_witnesses": sum(r["sample_direct_instances_of_target"] > 0 for r in rows),
        },
        "isolate_proposals": rows,
        "isolate_review_module_coverage": modules,
        "existing_broad_untyped_ends_not_counted_in_named_graph": broad_untyped,
        "counterfactual_all_fourteen_proposals_only_not_a_model_edit": {
            "components": len(hypothetical),
            "isolates": sorted(g[0] for g in hypothetical if len(g) == 1),
            "reason_not_implemented": "Every proposed relation lacks an NHIF P1 truthmaking witness; separate scientific/source acceptance required."
        },
        "topology_edit": {"new_edges": 0, "deleted_edges": 0, "model_unchanged": True},
        "interpretation": "A named-class isolate is not necessarily an ontological error. P1 data cannot authorize these event, normative, situation, mode, or optional BA connectors. Even target instances do not establish a truthmaking relation.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({
        "native": {k: nshot[k] for k in ("classes", "components", "largest_component", "isolates")},
        "owl": {k: oshot[k] for k in ("components", "largest_component", "isolates")},
        "comparison": result["comparison"],
        "sample": {k: v for k, v in result["sample"].items() if k != "direct_type_counts"},
    }, indent=2))


if __name__ == "__main__":
    main()
