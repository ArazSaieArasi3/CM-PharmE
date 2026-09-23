#!/usr/bin/env python3
import argparse, hashlib, json, os, subprocess, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki-src"
DIST = ROOT / "dist"
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()

def git_head():
    try:
        return subprocess.check_output(["git","rev-parse","HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return None

def collect_files():
    selected = []
    for p in sorted((WIKI / "pages").glob("*.md")):
        selected.append(p)
    for rel in ["README.md","page-inventory.csv","baseline-manifest.json","SNAPSHOT.md"]:
        p = WIKI / rel
        if p.exists():
            selected.append(p)
    return selected

def build(baseline):
    out = DIST / f"wiki-{baseline}"
    out.mkdir(parents=True, exist_ok=True)
    entries = []
    for src in collect_files():
        rel = src.relative_to(WIKI)
        dst = out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        data = src.read_bytes()
        dst.write_bytes(data)
        entries.append({"path": rel.as_posix(), "sha256": sha256_bytes(data), "bytes": len(data)})

    baseline_meta = json.loads((WIKI / "baseline-manifest.json").read_text(encoding="utf-8"))
    manifest = {
        "archive_schema": 1,
        "wiki_baseline": baseline,
        "documentation_maturity": baseline_meta.get("maturity"),
        "declared": baseline_meta.get("declared"),
        "publication_state": baseline_meta.get("wiki_publication_state"),
        "source_repository_commit": git_head(),
        "published_wiki_commit": None,
        "files": entries,
    }
    manifest_data = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    (out / "ARCHIVE-MANIFEST.json").write_bytes(manifest_data)

    zip_path = DIST / f"wiki-{baseline}.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        all_files = sorted([p for p in out.rglob("*") if p.is_file()])
        for p in all_files:
            rel = p.relative_to(out).as_posix()
            data = p.read_bytes()
            info = zipfile.ZipInfo(rel, FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, data)
    print(json.dumps({"archive": str(zip_path), "files": len(entries), "sha256": sha256_bytes(zip_path.read_bytes())}))
    return 0

def verify(archive):
    archive = Path(archive)
    with zipfile.ZipFile(archive, "r") as z:
        names = set(z.namelist())
        if "ARCHIVE-MANIFEST.json" not in names:
            raise SystemExit("VERIFY FAIL: ARCHIVE-MANIFEST.json missing")
        manifest = json.loads(z.read("ARCHIVE-MANIFEST.json"))
        failures = []
        for item in manifest["files"]:
            path = item["path"]
            if path not in names:
                failures.append(f"missing: {path}")
                continue
            digest = sha256_bytes(z.read(path))
            if digest != item["sha256"]:
                failures.append(f"checksum mismatch: {path}")
        if failures:
            for f in failures:
                print("ERROR:", f)
            raise SystemExit(f"VERIFY FAIL: {len(failures)} problem(s)")
        print(json.dumps({"verified": True, "files": len(manifest["files"]), "wiki_baseline": manifest["wiki_baseline"]}))
    return 0

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--baseline", required=True)
    v = sub.add_parser("verify")
    v.add_argument("--archive", required=True)
    args = ap.parse_args()
    if args.cmd == "build":
        return build(args.baseline)
    return verify(args.archive)

if __name__ == "__main__":
    sys.exit(main())
