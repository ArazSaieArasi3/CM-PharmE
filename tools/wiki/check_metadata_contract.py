#!/usr/bin/env python3
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki-src"
PAGES = WIKI / "pages"
INVENTORY = WIKI / "page-inventory.csv"

COMPACT_CLASSES = {
    "Narrative / Navigation",
    "Narrative / Research",
    "Concept / Domain / Model",
    "Evaluation / Evidence",
    "Cross-Version Evolution",
    "Reference / Index",
}

REQUIRED_RECORD_GROUPS = [
    ("Page scope",),
    ("Documentation maturity",),
    ("Authoritative source", "Authoritative sources", "V1 authority"),
    ("Last synchronized",),
    ("Last synchronized ref", "V1 ref", "Source refs checked"),
    ("Related issues/PRs", "Related issues", "Related issue"),
    ("Evidence status",),
    ("Future refresh",),
    ("Wiki baseline",),
]

def has_any(text, keys):
    return any(f"**{key}:**" in text for key in keys)

def count_top_metadata(text):
    lines = text.splitlines()
    count = 0
    for line in lines[:25]:
        if line.startswith("> **"):
            count += 1
        elif count and line.strip() and not line.startswith("> **"):
            break
    return count

def main():
    with INVENTORY.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    errors = []
    compact_pages = []
    governance_pages = []
    top_lines = 0
    record_pages = 0

    for row in rows:
        if row["source_status"] != "source-complete":
            continue
        path = PAGES / f"{row['slug']}.md"
        if not path.exists() or path.name in {"Home.md", "_Sidebar.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        top_lines += count_top_metadata(text)

        if row["class"] in COMPACT_CLASSES:
            compact_pages.append(row["page"])
            for key in ["Version scope", "Status", "Updated"]:
                if f"**{key}:**" not in text:
                    errors.append(f"{row['page']}: missing compact header field {key}")
            if "<summary>Documentation record</summary>" not in text:
                errors.append(f"{row['page']}: missing Documentation record")
                continue
            record_pages += 1
            for group in REQUIRED_RECORD_GROUPS:
                if not has_any(text, group):
                    errors.append(f"{row['page']}: Documentation record missing one of {group}")
        else:
            governance_pages.append(row["page"])
            for key in ["Page scope", "Documentation maturity", "Last synchronized"]:
                if f"**{key}:**" not in text:
                    errors.append(f"{row['page']}: governance/status metadata missing {key}")

    report = {
        "source_complete_inventory": sum(r["source_status"] == "source-complete" for r in rows),
        "compact_reader_pages": len(compact_pages),
        "documentation_record_pages": record_pages,
        "governance_status_pages_retaining_expanded_metadata": len(governance_pages),
        "top_metadata_lines_total": top_lines,
        "baseline_top_metadata_lines_total": 470,
        "baseline_top_metadata_lines_per_page": 8.25,
        "errors": errors,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
