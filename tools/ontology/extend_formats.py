#!/usr/bin/env python3
"""Generate deterministic application/data serializations from a CM-PharmE build artifact."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from rdflib import Dataset, Graph
from rdflib.compare import to_canonical_graph, to_isomorphic

CONTEXT = {
    "@version": 1.1,
    "c": "https://w3id.org/cm-pharme/concept/",
    "r": "https://w3id.org/cm-pharme/relation/",
    "d": "https://w3id.org/cm-pharme/domain/",
    "meta": "https://w3id.org/cm-pharme/meta/",
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "dcterms": "http://purl.org/dc/terms/",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_nt_bytes(graph: Graph) -> bytes:
    cg = to_canonical_graph(graph)
    lines = sorted(f"{s.n3()} {p.n3()} {o.n3()} .\n" for s, p, o in cg)
    return "".join(lines).encode("utf-8")


def stable_json(value, parent_key=None):
    """Canonicalize JSON-LD document order without reordering @list values."""
    if isinstance(value, dict):
        return {key: stable_json(value[key], key) for key in sorted(value)}
    if isinstance(value, list):
        items = [stable_json(item, parent_key) for item in value]
        if parent_key == "@list":
            return items
        return sorted(
            items,
            key=lambda item: json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
        )
    return value


def write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def collapse_dataset(path: Path, fmt: str) -> Graph:
    dataset = Dataset()
    dataset.parse(path, format=fmt)
    graph = Graph()
    for subject, predicate, obj, _context in dataset.quads((None, None, None, None)):
        graph.add((subject, predicate, obj))
    return graph


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", required=True)
    args = parser.parse_args()

    root = Path(args.artifact_root)
    source = root / "source/cm-pharme.ttl"
    graph = Graph()
    graph.parse(source, format="turtle")

    context_bytes = (
        json.dumps({"@context": CONTEXT}, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    write(root / "distributions/cm-pharme.context.json", context_bytes)

    canonical = Graph()
    for triple in to_canonical_graph(graph):
        canonical.add(triple)
    raw_compact = canonical.serialize(
        format="json-ld", context=CONTEXT, auto_compact=True, indent=2
    )
    compact = stable_json(json.loads(raw_compact))
    compact_bytes = (
        json.dumps(compact, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    write(root / "distributions/cm-pharme.compact.jsonld", compact_bytes)

    # Turtle is valid as the default graph in TriG. Reuse deterministic build bytes.
    write(
        root / "distributions/cm-pharme.trig",
        (root / "distributions/cm-pharme.ttl").read_bytes(),
    )
    # N-Triples statements are valid default-graph N-Quads statements.
    write(root / "distributions/cm-pharme.nq", canonical_nt_bytes(graph))

    parsed = {
        "distributions/cm-pharme.compact.jsonld": Graph(),
        "distributions/cm-pharme.trig": collapse_dataset(
            root / "distributions/cm-pharme.trig", "trig"
        ),
        "distributions/cm-pharme.nq": collapse_dataset(
            root / "distributions/cm-pharme.nq", "nquads"
        ),
    }
    parsed["distributions/cm-pharme.compact.jsonld"].parse(
        root / "distributions/cm-pharme.compact.jsonld", format="json-ld"
    )

    equivalence = {
        relative: to_isomorphic(candidate) == to_isomorphic(graph)
        for relative, candidate in parsed.items()
    }
    artifact_paths = [
        "distributions/cm-pharme.context.json",
        "distributions/cm-pharme.compact.jsonld",
        "distributions/cm-pharme.trig",
        "distributions/cm-pharme.nq",
    ]
    report = {
        "schema_version": 1,
        "profile": "CM-PharmE-extended-formats-v1",
        "status": "PASS" if all(equivalence.values()) else "FAIL",
        "source_triples": len(graph),
        "source_canonical_nt_sha256": sha256(canonical_nt_bytes(graph)),
        "graph_equivalence": equivalence,
        "artifacts": {
            relative: {
                "bytes": (root / relative).stat().st_size,
                "sha256": sha256((root / relative).read_bytes()),
            }
            for relative in artifact_paths
        },
    }
    write(
        root / "validation/extended-formats-report.json",
        (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    if report["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
