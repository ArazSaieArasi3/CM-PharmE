#!/usr/bin/env python3
"""Verify that current V2 drift from frozen W5 is limited to governed label annotations."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from rdflib import Graph
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


def stripped(g: Graph) -> set[tuple]:
    return {(s,p,o) for s,p,o in g if p not in IGNORED}


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
    old_core = stripped(old)
    cur_core = stripped(cur)
    added = cur_core - old_core
    removed = old_core - cur_core

    report = {
        "schema_version": 1,
        "result": "PASS" if not added and not removed else "FAIL",
        "ignored_predicates": sorted(str(x) for x in IGNORED),
        "w5_inventory": inventory(old),
        "current_inventory": inventory(cur),
        "non_annotation_added_triples": len(added),
        "non_annotation_removed_triples": len(removed),
        "interpretation": (
            "Current V2 differs from frozen W5 only in rdfs:label/skos:altLabel triples."
            if not added and not removed
            else "Current V2 contains non-annotation graph changes relative to frozen W5."
        ),
    }
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
