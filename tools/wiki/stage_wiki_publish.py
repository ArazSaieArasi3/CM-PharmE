#!/usr/bin/env python3
import argparse, csv, json, shutil
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-root", required=True)
    ap.add_argument("--wiki-dir", required=True)
    ap.add_argument("--source-repository", required=True)
    ap.add_argument("--source-commit", required=True)
    args = ap.parse_args()

    src = Path(args.source_root)
    wiki = Path(args.wiki_dir)
    inventory = src / "page-inventory.csv"
    baseline = json.loads((src / "baseline-manifest.json").read_text(encoding="utf-8"))

    rows = list(csv.DictReader(inventory.open(encoding="utf-8", newline="")))
    current_files = []
    pages = []

    for row in rows:
        if row["source_status"] != "source-complete":
            continue
        slug = row["slug"].strip()
        src_file = src / "pages" / f"{slug}.md"
        if not src_file.exists():
            raise SystemExit(f"source-complete page missing: {src_file}")
        dst = wiki / f"{slug}.md"
        shutil.copyfile(src_file, dst)
        current_files.append(dst.name)
        pages.append({
            "page": row["page"],
            "slug": slug,
            "file": dst.name,
            "primary_issue": row["primary_issue"],
        })

    sidebar = src / "pages" / "_Sidebar.md"
    if sidebar.exists():
        shutil.copyfile(sidebar, wiki / "_Sidebar.md")
        current_files.append("_Sidebar.md")

    manifest_path = wiki / ".cm-pharme-managed-pages.json"
    previous = {}
    if manifest_path.exists():
        try:
            previous = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            previous = {}

    previous_files = set(previous.get("managed_files", []))
    now = set(current_files)
    for stale in sorted(previous_files - now):
        p = wiki / stale
        if p.exists() and p.is_file():
            p.unlink()

    publish_manifest = {
        "schema_version": 1,
        "source_repository": args.source_repository,
        "source_commit": args.source_commit,
        "candidate_wiki_baseline": baseline.get("candidate_baseline_id"),
        "baseline_declared": baseline.get("declared"),
        "documentation_maturity": baseline.get("maturity"),
        "managed_files": sorted(current_files),
        "managed_page_count": len(pages),
        "pages": pages,
    }
    manifest_path.write_text(
        json.dumps(publish_manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "managed_pages": len(pages),
        "managed_files": len(current_files),
        "candidate_baseline": baseline.get("candidate_baseline_id"),
    }))

if __name__ == "__main__":
    main()
