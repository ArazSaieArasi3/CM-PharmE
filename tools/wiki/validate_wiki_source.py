#!/usr/bin/env python3
import argparse, csv, json, re, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki-src"
PAGES = WIKI / "pages"
INVENTORY = WIKI / "page-inventory.csv"
MANIFEST = WIKI / "baseline-manifest.json"

REQUIRED_META = [
    "Page scope:",
    "Documentation maturity:",
    "Last synchronized:",
    "Related issue",
]

WIKI_LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")

def load_inventory(path=INVENTORY):
    with path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    return rows

def page_file_for(row):
    return PAGES / f"{row['slug']}.md"

def validate_text_metadata(path, text, errors):
    if path.name in {"Home.md", "_Sidebar.md"}:
        return

    # Reader-facing pages may use the progressive-disclosure contract:
    # three compact header fields plus a complete Documentation record.
    if "**Version scope:**" in text:
        for marker in ["Version scope:", "Status:", "Updated:"]:
            if marker not in text:
                errors.append(f"{path}: missing compact metadata marker '{marker}'")
        if "<summary>Documentation record</summary>" not in text:
            errors.append(f"{path}: compact metadata requires a Documentation record")
        for marker in REQUIRED_META:
            if marker not in text:
                errors.append(f"{path}: Documentation record missing required provenance marker '{marker}'")
        return

    # Governance/status pages and not-yet-migrated pages retain the legacy
    # expanded header during the controlled transition.
    for marker in REQUIRED_META:
        if marker not in text:
            errors.append(f"{path}: missing required metadata marker '{marker}'")

def validate(root=WIKI, strict=False):
    errors, warnings = [], []
    inv_path = root / "page-inventory.csv"
    pages_dir = root / "pages"
    manifest_path = root / "baseline-manifest.json"

    if not inv_path.exists():
        return ["missing page-inventory.csv"], warnings
    if not manifest_path.exists():
        return ["missing baseline-manifest.json"], warnings

    rows = list(csv.DictReader(inv_path.open(encoding="utf-8", newline="")))
    names, slugs = {}, {}
    for i, row in enumerate(rows, start=2):
        name, slug = row["page"].strip(), row["slug"].strip()
        if name in names:
            errors.append(f"inventory:{i}: duplicate page name '{name}'")
        if slug in slugs:
            errors.append(f"inventory:{i}: duplicate slug '{slug}'")
        names[name] = row
        slugs[slug] = row

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    declared = bool(manifest.get("declared"))
    v2_frozen_allowed = declared and manifest.get("v2",{}).get("documentation_status") == "Frozen"

    source_complete = {r["page"] for r in rows if r["source_status"] == "source-complete"}
    planned = {r["page"] for r in rows if r["source_status"] == "planned"}

    for row in rows:
        status = row["source_status"]
        path = pages_dir / f"{row['slug']}.md"
        if status == "source-complete" and not path.exists():
            errors.append(f"inventory marks source-complete but file missing: {path}")
        if strict and status != "source-complete":
            errors.append(f"strict mode requires source-complete: {row['page']} ({status})")

    referenced = {"Home"}
    for path in sorted(pages_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        validate_text_metadata(path, text, errors)

        for target in WIKI_LINK_RE.findall(text):
            target = target.strip()
            referenced.add(target)
            if target == "Home":
                continue
            if target not in names:
                errors.append(f"{path}: internal Wiki link target absent from inventory: [[{target}]]")

        scope_m = re.search(r"\*\*Page scope:\*\*\s*([^\n]+)", text)
        maturity_m = re.search(r"\*\*Documentation maturity:\*\*\s*([^\n]+)", text)
        if scope_m and "V2" in scope_m.group(1) and maturity_m:
            maturity = maturity_m.group(1).strip().lower()
            if ("frozen" in maturity or maturity == "final") and not v2_frozen_allowed:
                errors.append(f"{path}: V2 page prematurely marked {maturity_m.group(1).strip()}")

    for row in rows:
        if row["source_status"] == "source-complete" and row["page"] not in referenced:
            # Governance/index pages may be intentionally linked from README before end-user navigation.
            if row["page"] not in {"Wiki Update Register"}:
                warnings.append(f"source-complete page may be orphaned from Wiki links: {row['page']}")

    # Basic foundation invariants.
    home = pages_dir / "Home.md"
    sidebar = pages_dir / "_Sidebar.md"
    if not home.exists():
        errors.append("Home.md missing")
    if not sidebar.exists():
        errors.append("_Sidebar.md missing")
    if home.exists():
        ht = home.read_text(encoding="utf-8")
        for required in [
            "CM-PharmE 1.x",
            "CM-PharmE 2.0",
            "Research Guide",
            "Ontology and Conceptual Model Guide",
            "Data and Database Guide",
            "Knowledge Graph and Queries Guide",
            "Evaluation and Reproducibility Guide",
            "Applications Guide",
            "Publications and Citation Guide",
            "Reference Guide",
            "Documentation History and Governance",
        ]:
            if required not in ht:
                errors.append(f"Home.md missing required navigation section: {required}")

    return errors, warnings

def self_test():
    # Prove at least one blocking defect is detected.
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "pages").mkdir()
        (root / "baseline-manifest.json").write_text('{"declared": false, "v2": {"documentation_status":"Stable-to-date / Evolving"}}', encoding="utf-8")
        (root / "page-inventory.csv").write_text(
            "page,slug,class,scope,source_status,publish_status,primary_issue\n"
            "Broken,Broken,Narrative / Research,V2,source-complete,pending,999\n",
            encoding="utf-8",
        )
        (root / "pages" / "Broken.md").write_text("# Broken\n\nNo metadata.\n", encoding="utf-8")
        errs, _ = validate(root=root, strict=False)
        if not errs:
            raise SystemExit("SELF-TEST FAILED: invalid fixture was not rejected")
        print("SELF-TEST PASS: invalid fixture rejected")
        for e in errs:
            print("  expected:", e)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="require every inventory page to be source-complete")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        self_test()
        return
    errors, warnings = validate(strict=args.strict)
    for w in warnings:
        print("WARNING:", w)
    if errors:
        for e in errors:
            print("ERROR:", e)
        print(f"FAIL: {len(errors)} error(s), {len(warnings)} warning(s)")
        raise SystemExit(1)
    print(f"PASS: 0 errors, {len(warnings)} warning(s)")

if __name__ == "__main__":
    main()
