#!/usr/bin/env python3
import argparse
import csv
import json
import re
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki-src"
PAGES = WIKI / "pages"
INVENTORY = WIKI / "page-inventory.csv"

TOP_LEVEL = [
    "Research Guide",
    "Ontology and Conceptual Model Guide",
    "Data and Database Guide",
    "Knowledge Graph and Queries Guide",
    "Evaluation and Reproducibility Guide",
    "Applications Guide",
    "Publications and Citation Guide",
    "Reference Guide",
    "Documentation History and Governance",
]

LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")

def links(path):
    text = path.read_text(encoding="utf-8")
    return [x.strip() for x in LINK_RE.findall(text)]

def load_inventory():
    with INVENTORY.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))

def build_graph(rows):
    by_page = {r["page"]: r for r in rows}
    graph = {r["page"]: [] for r in rows}
    indegree = {r["page"]: 0 for r in rows}

    for row in rows:
        if row["source_status"] != "source-complete":
            continue
        path = PAGES / f"{row['slug']}.md"
        if not path.exists():
            continue
        for target in links(path):
            if target in by_page:
                graph[row["page"]].append(target)
                indegree[target] += 1
    return by_page, graph, indegree

def depths(graph, start="Home"):
    out = {start: 0}
    q = deque([start])
    while q:
        current = q.popleft()
        for nxt in graph.get(current, []):
            if nxt not in out:
                out[nxt] = out[current] + 1
                q.append(nxt)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output")
    args = ap.parse_args()

    rows = load_inventory()
    by_page, graph, indegree = build_graph(rows)
    depth = depths(graph)

    required = [r["page"] for r in rows if r["source_status"] == "source-complete"]
    unreachable = sorted([p for p in required if p not in depth])
    too_deep = sorted([{"page": p, "depth": depth[p]} for p in required if p in depth and depth[p] > 2], key=lambda x:(x["depth"],x["page"]))
    orphans = sorted([p for p in required if p != "Home" and indegree.get(p, 0) == 0])

    home_links = set(links(PAGES / "Home.md"))
    sidebar_links = set(links(PAGES / "_Sidebar.md"))
    missing_home = [p for p in TOP_LEVEL if p not in home_links]
    missing_sidebar = [p for p in TOP_LEVEL if p not in sidebar_links]

    planned = [r["page"] for r in rows if r["source_status"] != "source-complete"]
    planned_depth = {p: depth.get(p) for p in planned}

    report = {
        "inventory_entries": len(rows),
        "source_complete_pages": len(required),
        "top_level_landing_pages": len(TOP_LEVEL),
        "max_source_complete_depth": max((depth[p] for p in required if p in depth), default=None),
        "unreachable_source_complete": unreachable,
        "source_complete_too_deep": too_deep,
        "orphan_source_complete": orphans,
        "missing_home_landings": missing_home,
        "missing_sidebar_landings": missing_sidebar,
        "planned_pages": planned_depth,
        "depth_histogram": {
            str(d): sum(1 for p in required if depth.get(p) == d)
            for d in sorted(set(depth.get(p) for p in required if p in depth))
        },
    }

    errors = []
    if unreachable:
        errors.append(f"unreachable source-complete pages: {unreachable}")
    if too_deep:
        errors.append(f"source-complete pages deeper than 2 steps: {too_deep}")
    if orphans:
        errors.append(f"orphan source-complete pages: {orphans}")
    if missing_home:
        errors.append(f"Home missing landing pages: {missing_home}")
    if missing_sidebar:
        errors.append(f"Sidebar missing landing pages: {missing_sidebar}")

    report["errors"] = errors

    if args.output:
        Path(args.output).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
