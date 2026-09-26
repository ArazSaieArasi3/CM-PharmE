#!/usr/bin/env python3
"""Verify that current V2 drift from frozen W5 is limited to governed label annotations."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from rdflib import Graph
from rdflib.compare import isomorphic, to_canonical_graph
from rdflib.namespace import RDF, RDFS, OWL, SKOS

IGNORED = {RDFS.label, SKOS.altLabel}


def load(root: Path) -> Graph:
    g = Graph()
    files = sorted(root.glob("*.ttl"))
    if not files:
        raise SystemExit(f"No Turtle modules found in {root}")
    for p in files:
        g.parse(p, format="turtle")
    return g


def stripped_graph(g: Graph) -> Graph:
    out = Graph()
    for s, p, o in g:
        if p not in IGNORED:
            out.add((s, p, o))
    return out


def canonical_lines(g: Graph) -> list[str]:
    cg = to_canonical_graph(g)
    return sorted(f"{s.n3()} {p.n3()} {o.n3()} ." for s, p, o in cg)


def inventory(g: Graph) -> dict:
    return {
        "triples": len(g),
        "owl_classes": len(set(g.subjects(RDF.type, OWL.Class))),
        "rdfs_datatypes": len(set(g.subjects(RDF.type, RDFS.Datatype))),
        "object_properties": len(set(g.subjects(RDF.type, OWL.ObjectProperty))),
        "datatype_properties": len(set(g.subjects(RDF.type, OWL.DatatypeProperty))),
        "labels": len(list(g.triples((None, RDFS.label, None)))),
        "alt_labels": len(list(g.triples((None, SKOS.altLabel, None)))),
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--w5-dir", type=Path, required=True)
    p.add_argument("--current-dir", type=Path, required=True)
    p.add_argument("--output", type=Path)
    args = p.parse_args()

    old = load(args.w5_dir)
    cur = load(args.current_dir)
    old_core = stripped_graph(old)
    cur_core = stripped_graph(cur)

    equivalent = isomorphic(old_core, cur_core)
    old_lines = set(canonical_lines(old_core))
    cur_lines = set(canonical_lines(cur_core))
    added = sorted(cur_lines - old_lines)
    removed = sorted(old_lines - cur_lines)

    report = {
        "schema_version": 1,
        "result": "PASS" if equivalent else "FAIL",
        "comparison_method": "RDF graph isomorphism after removing governed label predicates",
        "ignored_predicates": sorted(str(x) for x in IGNORED),
        "w5_inventory": inventory(old),
        "current_inventory": inventory(cur),
        "non_annotation_graph_isomorphic": bool(equivalent),
        "non_annotation_added_triples": len(added),
        "non_annotation_removed_triples": len(removed),
        "non_annotation_added_sample": added[:50],
        "non_annotation_removed_sample": removed[:50],
        "interpretation": (
            "Current V2 differs from frozen W5 only in rdfs:label/skos:altLabel triples; blank-node identity is compared isomorphically."
            if equivalent
            else "Current V2 contains non-annotation graph changes relative to frozen W5."
        ),
    }
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if equivalent else 1


if __name__ == "__main__":
    raise SystemExit(main())
