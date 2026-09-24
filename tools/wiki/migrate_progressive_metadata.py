#!/usr/bin/env python3
import csv
import json
import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki-src"
PAGES = WIKI / "pages"
INVENTORY = WIKI / "page-inventory.csv"
REPORT = WIKI / "quality" / "metadata-migration-report.json"

COMPACT_CLASSES = {
    "Narrative / Navigation",
    "Narrative / Research",
    "Concept / Domain / Model",
    "Evaluation / Evidence",
    "Cross-Version Evolution",
    "Reference / Index",
}
META_RE = re.compile(r"^> \*\*([^*]+):\*\*\s*(.*?)\s*$")

def default_authority(scope):
    s = scope.lower()
    if "v1" in s and "v2" not in s:
        return "main"
    if "v2" in s and "cross" not in s:
        return "v2/research-program"
    if "cross" in s or ("v1" in s and "v2" in s):
        return "V1: main; V2: v2/research-program"
    return "main / wiki-src documentation controls"

def default_ref(scope):
    s = scope.lower()
    if "v1" in s and "v2" not in s:
        return "main (see linked authoritative V1 artifacts)"
    if "v2" in s and "cross" not in s:
        return "v2/research-program (see linked authoritative V2 artifacts)"
    if "cross" in s or ("v1" in s and "v2" in s):
        return "V1: main; V2: v2/research-program"
    return "main (documentation source)"

def parse_header(lines):
    start = None
    for i, line in enumerate(lines[:25]):
        if META_RE.match(line):
            start = i
            break
        if i > 0 and line.startswith("## "):
            break
    if start is None:
        return None, None, OrderedDict()

    end = start
    records = OrderedDict()
    while end < len(lines):
        m = META_RE.match(lines[end])
        if not m:
            break
        records[m.group(1).strip()] = m.group(2).strip()
        end += 1
    return start, end, records

def ensure_record_fields(records, row):
    scope = records.get("Page scope", row["scope"])
    records.setdefault("Page scope", scope)
    records.setdefault("Documentation maturity", "Stable-to-date / Evolving" if "V2" in scope else "Stable")
    records.setdefault("Authoritative source", default_authority(scope))
    records.setdefault("Last synchronized", "2026-09-24")
    records.setdefault("Last synchronized ref", default_ref(scope))
    if not any(k.startswith("Related issue") for k in records):
        records["Related issues/PRs"] = f"#{row['primary_issue']}"
    records.setdefault(
        "Evidence status",
        "Documentation/navigation page; substantive evidence remains in linked authoritative artifacts",
    )
    records.setdefault("Future refresh", "See #211–#214 as applicable")
    records.setdefault("Wiki baseline", "WB-2026.09.1")
    return records

def render_record(records):
    out = [
        "<details>",
        "<summary>Documentation record</summary>",
        "",
    ]
    for key, value in records.items():
        out.append(f"- **{key}:** {value}")
    out.extend(["", "</details>"])
    return "\n".join(out)

def migrate_page(path, row):
    text = path.read_text(encoding="utf-8")
    if "<summary>Documentation record</summary>" in text and "**Version scope:**" in text:
        return False, "already-compact"

    lines = text.splitlines()
    start, end, records = parse_header(lines)
    if start is None:
        return False, "no-expanded-metadata"

    records = ensure_record_fields(records, row)
    scope = records["Page scope"]
    status = records["Documentation maturity"]
    updated = records["Last synchronized"]

    compact = [
        f"> **Version scope:** {scope}  ",
        f"> **Status:** {status}  ",
        f"> **Updated:** {updated}",
    ]

    # Replace expanded block, preserving surrounding blank-line structure.
    new_lines = lines[:start] + compact + lines[end:]
    body = "\n".join(new_lines).rstrip()

    if "<summary>Documentation record</summary>" not in body:
        body += "\n\n---\n\n" + render_record(records)
    path.write_text(body + "\n", encoding="utf-8")
    return True, "migrated"

def main():
    with INVENTORY.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    result = {
        "schema_version": 1,
        "issue": 231,
        "migrated": [],
        "already_compact": [],
        "skipped_governance_or_status": [],
        "skipped_other": [],
    }

    for row in rows:
        if row["source_status"] != "source-complete":
            continue
        page_class = row["class"]
        path = PAGES / f"{row['slug']}.md"
        if not path.exists() or path.name in {"Home.md", "_Sidebar.md"}:
            result["skipped_other"].append(row["page"])
            continue
        if page_class not in COMPACT_CLASSES:
            result["skipped_governance_or_status"].append(row["page"])
            continue
        changed, reason = migrate_page(path, row)
        if changed:
            result["migrated"].append(row["page"])
        elif reason == "already-compact":
            result["already_compact"].append(row["page"])
        else:
            result["skipped_other"].append(row["page"])

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "migrated": len(result["migrated"]),
        "already_compact": len(result["already_compact"]),
        "governance_status_retained": len(result["skipped_governance_or_status"]),
        "other_skipped": len(result["skipped_other"]),
        "report": str(REPORT.relative_to(ROOT)),
    }))

if __name__ == "__main__":
    main()
