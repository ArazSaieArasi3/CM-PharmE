#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
WIKI=ROOT/"wiki-src"
PAGES=WIKI/"pages"
MANIFEST=WIKI/"diagrams"/"manifest.json"
RAW_PREFIX="https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/"

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--check",action="store_true")
    args=ap.parse_args()

    data=json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected={}
    for d in data.get("diagrams",[]):
        rel=d.get("rendered_path")
        if not rel or not rel.endswith(".svg"):
            continue
        p=ROOT/rel
        if not p.exists():
            continue
        base=RAW_PREFIX+rel
        expected[base]=digest(p)

    changed=[]
    stale=[]
    raw_pattern=re.compile(r"https://raw\.githubusercontent\.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/[^)\s]+\.svg(?:\?sha=[0-9a-f]{12})?")

    for page in sorted(PAGES.glob("*.md")):
        text=page.read_text(encoding="utf-8")
        original=text

        def repl(m):
            url=m.group(0)
            base=url.split("?sha=",1)[0]
            if base not in expected:
                return url
            wanted=base+"?sha="+expected[base]
            if url!=wanted:
                stale.append({
                    "page":page.name,
                    "url":url,
                    "expected":wanted,
                })
            return wanted

        text=raw_pattern.sub(repl,text)
        if text!=original:
            if args.check:
                continue
            page.write_text(text,encoding="utf-8")
            changed.append(page.name)

    report={
        "governed_svg_assets":len(expected),
        "stale_or_unversioned_image_urls":len(stale),
        "pages_changed":changed,
        "stale_examples":stale[:20],
    }
    print(json.dumps(report,indent=2,sort_keys=True))
    if args.check and stale:
        raise SystemExit(1)

if __name__=="__main__":
    main()
