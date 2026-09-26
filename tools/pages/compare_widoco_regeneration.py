#!/usr/bin/env python3
"""Compare two WIDOCO candidate trees for reproducible governed regeneration."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def digest(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()


def tree(root: Path) -> dict[str, Path]:
    return {str(p.relative_to(root)).replace("\\","/"): p for p in root.rglob("*") if p.is_file()}


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--version", required=True)
    ap.add_argument("--first", type=Path, required=True)
    ap.add_argument("--second", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args=ap.parse_args()

    a=tree(args.first)
    b=tree(args.second)
    only_a=sorted(set(a)-set(b))
    only_b=sorted(set(b)-set(a))
    common=sorted(set(a)&set(b))
    differing=[]
    same=0
    for rel in common:
        da,db=digest(a[rel]),digest(b[rel])
        if da==db:
            same+=1
        else:
            differing.append({"path":rel,"first_sha256":da,"second_sha256":db})

    report={
        "schema_version":1,
        "version_id":args.version,
        "comparison_policy":"raw byte-for-byte candidate-tree comparison; no volatile fields ignored in this discovery run",
        "first_file_count":len(a),
        "second_file_count":len(b),
        "same_file_count":same,
        "only_in_first":only_a,
        "only_in_second":only_b,
        "differing_files":differing,
        "differing_file_count":len(differing),
        "result":"PASS" if not only_a and not only_b and not differing else "FAIL"
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(args.output.read_text(encoding="utf-8"))
    return 0 if report["result"]=="PASS" else 1

if __name__=="__main__":
    raise SystemExit(main())
