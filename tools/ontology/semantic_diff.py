#!/usr/bin/env python3
"""Compare RDF-compatible ontology artifacts by canonical graph rather than text layout."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from rdflib import Dataset, Graph
from rdflib.compare import to_canonical_graph, to_isomorphic


def load(path: Path, fmt: str | None = None) -> Graph:
    suffix = path.suffix.lower()
    fmt = fmt or {
        ".ttl": "turtle",
        ".owl": "xml",
        ".rdf": "xml",
        ".jsonld": "json-ld",
        ".nt": "nt",
        ".trig": "trig",
        ".nq": "nquads",
    }.get(suffix)
    if fmt in {"trig", "nquads"}:
        ds = Dataset()
        ds.parse(path, format=fmt)
        graph = Graph()
        for s, p, o, _ctx in ds.quads((None, None, None, None)):
            graph.add((s, p, o))
        return graph
    graph = Graph()
    graph.parse(path, format=fmt)
    return graph


def canonical_lines(graph: Graph) -> list[str]:
    cg = to_canonical_graph(graph)
    return sorted(f"{s.n3()} {p.n3()} {o.n3()} ." for s, p, o in cg)


def fingerprint(lines: list[str]) -> str:
    return hashlib.sha256(("\n".join(lines) + "\n").encode("utf-8")).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--left", required=True)
    parser.add_argument("--right", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--max-examples", type=int, default=20)
    args = parser.parse_args()

    left_path = Path(args.left)
    right_path = Path(args.right)
    left = load(left_path)
    right = load(right_path)
    left_lines = canonical_lines(left)
    right_lines = canonical_lines(right)
    left_set, right_set = set(left_lines), set(right_lines)
    report = {
        "schema_version": 1,
        "left": str(left_path),
        "right": str(right_path),
        "isomorphic": to_isomorphic(left) == to_isomorphic(right),
        "left_triples": len(left),
        "right_triples": len(right),
        "left_canonical_sha256": fingerprint(left_lines),
        "right_canonical_sha256": fingerprint(right_lines),
        "removed_count": len(left_set - right_set),
        "added_count": len(right_set - left_set),
        "removed_examples": sorted(left_set - right_set)[: args.max_examples],
        "added_examples": sorted(right_set - left_set)[: args.max_examples],
    }
    report["status"] = "PASS" if report["isomorphic"] else "DIFF"
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    if not report["isomorphic"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
