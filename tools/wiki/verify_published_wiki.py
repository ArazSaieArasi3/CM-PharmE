#!/usr/bin/env python3
import argparse, csv, json, os, time, urllib.error, urllib.request
from pathlib import Path

def check(url, attempts=8, delay=3):
    last = None
    headers = {"User-Agent": "CM-PharmE-Wiki-Publisher/1.0"}
    for _ in range(attempts):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as r:
                code = r.getcode()
                if 200 <= code < 400:
                    return code
                last = f"HTTP {code}"
        except Exception as e:
            last = str(e)
        time.sleep(delay)
    raise RuntimeError(f"{url}: {last}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-root", required=True)
    ap.add_argument("--repository", required=True)
    ap.add_argument("--wiki-commit", required=True)
    ap.add_argument("--report", required=True)
    args = ap.parse_args()

    src = Path(args.source_root)
    rows = list(csv.DictReader((src / "page-inventory.csv").open(encoding="utf-8", newline="")))
    published = [r for r in rows if r["source_status"] == "source-complete"]

    base = f"https://github.com/{args.repository}/wiki"
    results = []
    failures = []

    # Home surface.
    try:
        code = check(base)
        results.append({"page": "Home", "url": base, "http_status": code})
    except Exception as e:
        failures.append(str(e))

    for row in published:
        slug = row["slug"].strip()
        if slug == "Home":
            continue
        url = f"{base}/{slug}"
        try:
            code = check(url)
            results.append({"page": row["page"], "slug": slug, "url": url, "http_status": code})
        except Exception as e:
            failures.append(str(e))

    report = {
        "source_repository": args.repository,
        "wiki_commit": args.wiki_commit,
        "expected_source_complete_pages": len(published),
        "verified_urls": len(results),
        "failures": failures,
        "results": results,
    }
    Path(args.report).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "wiki_commit": args.wiki_commit,
        "expected_pages": len(published),
        "verified_urls": len(results),
        "failures": len(failures),
    }))
    if failures:
        for f in failures:
            print("ERROR:", f)
        raise SystemExit(1)

if __name__ == "__main__":
    main()
