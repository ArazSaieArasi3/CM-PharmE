#!/usr/bin/env python3
import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "wiki-src" / "diagrams" / "manifest.json"

ALLOWED_NOTATIONS = {
    "OntoUML/UFO-aware conceptual notation",
    "Crow's Foot ERD",
    "Data-flow / architecture flow",
    "C4",
    "Process/activity/flow",
    "Lineage / evolution graph",
}
ALLOWED_STATUS = {"Authoritative", "Authoritative projection", "Illustrative"}
SOURCE_EXTS = {".puml", ".plantuml", ".mmd", ".mermaid", ".dot", ".gv", ".drawio"}

def main():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    diagrams = data.get("diagrams", [])
    errors = []
    ids = set()
    notation_families = set()

    for d in diagrams:
        did = d.get("id")
        if not did:
            errors.append("diagram missing id")
            continue
        if did in ids:
            errors.append(f"duplicate diagram id: {did}")
        ids.add(did)

        notation = d.get("notation")
        notation_families.add(notation)
        if notation not in ALLOWED_NOTATIONS:
            errors.append(f"{did}: unsupported notation '{notation}'")
        if d.get("artifact_status") not in ALLOWED_STATUS:
            errors.append(f"{did}: invalid artifact_status '{d.get('artifact_status')}'")

        for field in [
            "title","purpose","version_scope","notation","artifact_status",
            "source_path","rendered_path","generation_method","authoritative_source",
            "last_updated","checked_ref","related_pages","alt_text","caption"
        ]:
            if not d.get(field):
                errors.append(f"{did}: missing required manifest field '{field}'")

        src = ROOT / d.get("source_path","")
        out = ROOT / d.get("rendered_path","")
        if not src.exists():
            errors.append(f"{did}: source missing: {src}")
        elif src.suffix.lower() not in SOURCE_EXTS:
            errors.append(f"{did}: unsupported source extension: {src.suffix}")
        if not out.exists():
            errors.append(f"{did}: rendered artifact missing: {out}")
            continue
        if out.suffix.lower() != ".svg":
            errors.append(f"{did}: new governed diagrams must publish SVG, got {out.suffix}")

        if did not in src.name or did not in out.name:
            errors.append(f"{did}: ID must appear in both source and rendered filenames")
        if "/source/" not in d.get("source_path","") or "/rendered/" not in d.get("rendered_path",""):
            errors.append(f"{did}: source/rendered folder convention violated")

        try:
            root = ET.fromstring(out.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"{did}: invalid SVG/XML: {e}")
            continue

        if root.tag.split("}")[-1] != "svg":
            errors.append(f"{did}: rendered artifact root is not svg")
        if not root.attrib.get("viewBox"):
            errors.append(f"{did}: SVG missing viewBox")
        if root.attrib.get("data-theme-safe") != "true":
            errors.append(f"{did}: SVG missing data-theme-safe=true")
        style = root.attrib.get("style","")
        if "color:#24292f" not in style or "background:#ffffff" not in style:
            errors.append(f"{did}: SVG root must pin foreground/background colors")

        bg_nodes = [
            child for child in root
            if child.tag.split("}")[-1] == "rect"
            and child.attrib.get("id") == "diagram-background"
        ]
        if not bg_nodes:
            errors.append(f"{did}: SVG missing diagram-background canvas")
        else:
            bg = bg_nodes[0]
            if bg.attrib.get("fill") != "#ffffff":
                errors.append(f"{did}: diagram-background must use #ffffff fill")

        children = {child.tag.split("}")[-1] for child in root}
        if "title" not in children:
            errors.append(f"{did}: SVG missing <title>")
        if "desc" not in children:
            errors.append(f"{did}: SVG missing <desc>")

        if not isinstance(d.get("related_pages"), list) or not d["related_pages"]:
            errors.append(f"{did}: related_pages must be a non-empty list")

    if len(diagrams) < 3:
        errors.append("at least three governed sample diagrams are required")
    if len(notation_families) < 3:
        errors.append("at least three notation families are required")

    legacy = data.get("legacy_inventory", [])
    grandfathered_missing = [x["id"] for x in legacy if x.get("status") == "grandfathered-source-missing"]
    for item in legacy:
        if item.get("status") == "grandfathered-source-missing" and item.get("source_path"):
            errors.append(f"{item.get('id')}: source-missing legacy item unexpectedly has source_path")
        if item.get("source_path") and not item.get("source_branch"):
            if not (ROOT / item["source_path"]).exists():
                errors.append(f"{item.get('id')}: local legacy source path missing")
        if item.get("rendered_path") and not item.get("source_branch"):
            if not (ROOT / item["rendered_path"]).exists():
                errors.append(f"{item.get('id')}: local legacy rendered path missing")

    report = {
        "governed_diagrams": len(diagrams),
        "notation_families": sorted(notation_families),
        "legacy_inventory_entries": len(legacy),
        "grandfathered_source_missing": grandfathered_missing,
        "errors": errors,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
