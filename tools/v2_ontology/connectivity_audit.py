#!/usr/bin/env python3
"""Reproducible *diagram* connectivity audit for the Gate-D review projection.

This is an undirected graph diagnostic. It does not infer OWL semantics, verify
OntoUML constraints, or approve any candidate relation.
"""

from __future__ import annotations

import csv
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUML = ROOT / "v2/research/w4/integrated-ontouml-overview.puml"
REGISTRY = ROOT / "v2/ontouml/cm-pharme-v2.conceptual-model.json"
CANDIDATES = ROOT / "v2/research/w4/connection-candidates.csv"
MODULES = ROOT / "v2/ontology/source/modules"
PROJECTION = ROOT / "v2/research/w4/integrated-ontouml-review-projection.puml"

CLASS = re.compile(r'\b(?:abstract )?class\s+(?:"([^"]+)"|(\w+))(?:\s+as\s+(\w+))?\s+<<')
EDGE = re.compile(r"^\s*(\w+)\s+(<\|--|-->|--)\s+(\w+)(?:\s*:.*)?$")


def components(nodes: set[str], edges: list[tuple[str, str]]) -> list[list[str]]:
    adjacency = {n: set() for n in nodes}
    for a, b in edges:
        if a not in nodes or b not in nodes:
            raise ValueError(f"Unregistered graph endpoint: {a} -> {b}")
        adjacency[a].add(b)
        adjacency[b].add(a)
    seen: set[str] = set()
    groups = []
    for node in sorted(nodes):
        if node in seen:
            continue
        stack, group = [node], []
        seen.add(node)
        while stack:
            current = stack.pop()
            group.append(current)
            for neighbor in sorted(adjacency[current] - seen):
                seen.add(neighbor)
                stack.append(neighbor)
        groups.append(sorted(group))
    return sorted(groups, key=lambda group: (-len(group), group))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-review-projection", action="store_true", help="Generate a diagram containing only already documented missing relations")
    args = parser.parse_args()
    lines = PUML.read_text(encoding="utf-8").splitlines()
    aliases = {}
    datatypes = set()
    for line in lines:
        match = CLASS.search(line)
        if match:
            alias = match.group(3) or match.group(2)
            aliases[alias] = match.group(1) or match.group(2)
            if "<<Datatype>>" in line:
                datatypes.add(alias)
    edges = []
    for line in lines:
        match = EDGE.match(line)
        if match:
            edges.append((match.group(1), match.group(3)))

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    declared = sum(len(group) for group in registry["modules"].values())
    if len(aliases) != declared or declared != registry["counts"]["total"]:
        raise ValueError("Concept count differs between overview and conceptual registry")

    with CANDIDATES.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    statuses = {"documented_missing_from_overview", "candidate_requires_review", "defer_pending_evidence"}
    if len({r["id"] for r in rows}) != len(rows) or any(r["status"] not in statuses for r in rows):
        raise ValueError("Duplicate candidate ID or unknown disposition")
    for row in rows:
        if row["source"] not in aliases or row["target"] not in aliases:
            raise ValueError(f"Unknown candidate endpoint in {row['id']}")
    existing_endpoints = {frozenset(edge) for edge in edges}
    for row in rows:
        if frozenset((row["source"], row["target"])) in existing_endpoints:
            raise ValueError(f"Candidate edge already shown in overview: {row['id']}")
    existing = [(r["source"], r["target"]) for r in rows if r["status"] == "documented_missing_from_overview"]
    proposed = [(r["source"], r["target"]) for r in rows if r["status"] == "candidate_requires_review"]
    owl_text = "\n".join(f.read_text(encoding="utf-8") for f in sorted(MODULES.glob("*.ttl")))
    for row in rows:
        if row["status"] == "documented_missing_from_overview" and f"cmpe:{row['relation']} a owl:ObjectProperty" not in owl_text:
            raise ValueError(f"Documented edge lacks W5 object property: {row['id']}")
    if args.write_review_projection:
        if lines[-1] != "@enduml":
            raise ValueError("Unexpected PlantUML end marker")
        added = [
            "",
            "' Corrected visualization of existing W5 relations only; not new 2.1 semantics.",
            *(f"{r['source']} --> {r['target']} : {r['relation']}" for r in rows if r["status"] == "documented_missing_from_overview"),
            "",
        ]
        PROJECTION.write_text("\n".join([lines[0].replace("W4_Overview", "W4_Review_Projection"), *lines[1:-1], *added, "@enduml", ""]), encoding="utf-8")
    stages = {
        "w4_overview": edges,
        "with_documented_edges_shown": edges + existing,
        "hypothetical_all_review_candidates": edges + existing + proposed,
    }
    graph = {}
    for name, stage_edges in stages.items():
        for scope, nodes in (("all_elements", set(aliases)), ("classes_only", set(aliases) - datatypes)):
            scoped_edges = [(a, b) for a, b in stage_edges if a in nodes and b in nodes]
            groups = components(nodes, scoped_edges)
            graph[f"{name}_{scope}"] = {
                "nodes": len(nodes),
                "edge_instances": len(scoped_edges),
                "components": len(groups),
                "component_sizes": [len(g) for g in groups],
                "isolates": [aliases[g[0]] for g in groups if len(g) == 1],
            }

    props, partial = 0, []
    for file in sorted(MODULES.glob("*.ttl")):
        for line in file.read_text(encoding="utf-8").splitlines():
            if " a owl:ObjectProperty" not in line:
                continue
            props += 1
            if "rdfs:domain" not in line or "rdfs:range" not in line:
                partial.append(line.split(" ", 1)[0].removeprefix("cmpe:"))
    result = {
        "scope": "W4 PlantUML overview connectivity; candidate stage is not an ontology revision",
        "source_registry_version": registry["model_version"],
        "overview_datatypes": sorted(aliases[d] for d in datatypes),
        "owl_object_properties": props,
        "owl_properties_without_both_explicit_domain_and_range": partial,
        "candidate_status_counts": {s: sum(r["status"] == s for r in rows) for s in sorted({r["status"] for r in rows})},
        "graph": graph,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
