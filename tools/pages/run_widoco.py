#!/usr/bin/env python3
"""Run the pinned WIDOCO adapter for one governed CM-PharmE version."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ADAPTER = ROOT / "docs/documentation/widoco-adapter.json"
REGISTRY = ROOT / "docs/documentation/ontology-version-registry.json"


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--version", required=True)
    p.add_argument("--jar", type=Path, required=True)
    p.add_argument("--ontology", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--manifest-output", type=Path, required=True)
    args=p.parse_args()

    adapter=json.loads(ADAPTER.read_text(encoding="utf-8"))
    registry=json.loads(REGISTRY.read_text(encoding="utf-8"))
    if args.version not in adapter["versions"]:
        print(f"ERROR: no WIDOCO adapter entry for {args.version}", file=sys.stderr); return 2
    cfg=adapter["versions"][args.version]
    reg=next((v for v in registry["versions"] if v["id"]==args.version), None)
    if reg is None:
        print(f"ERROR: version {args.version} missing from registry", file=sys.stderr); return 3
    if cfg["source_ref"] != reg["semantic_source_ref"]:
        print("ERROR: adapter source ref differs from registry", file=sys.stderr); return 4
    actual_jar=sha256(args.jar)
    expected_jar=adapter["release_asset"]["sha256"]
    if actual_jar != expected_jar:
        print(f"ERROR: WIDOCO JAR checksum mismatch {actual_jar} != {expected_jar}", file=sys.stderr); return 5
    if not args.ontology.is_file():
        print(f"ERROR: ontology input missing: {args.ontology}", file=sys.stderr); return 6

    config=ROOT / cfg["config"]
    if not config.is_file():
        print(f"ERROR: config missing: {config}", file=sys.stderr); return 7
    args.output.mkdir(parents=True, exist_ok=True)
    cmd=[
        "java","-jar",str(args.jar),
        "-ontFile",str(args.ontology),
        "-outFolder",str(args.output),
        "-confFile",str(config),
        "-rewriteAll",
        "-includeAnnotationProperties",
        "-noPlaceHolderText",
        "-uniteSections",
    ]
    proc=subprocess.run(cmd,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log=args.manifest_output.parent / f"widoco-{args.version}.log"
    log.parent.mkdir(parents=True,exist_ok=True)
    log.write_text(proc.stdout,encoding="utf-8")

    entry=None
    for candidate in ("index-en.html","index.html"):
        if (args.output/candidate).is_file():
            entry=candidate; break
    if entry is None:
        print(proc.stdout[-4000:], file=sys.stderr)
        print(f"ERROR: WIDOCO produced no index page (exit={proc.returncode})", file=sys.stderr)
        return 8

    marker=reg["semantic_source_ref"]
    html=(args.output/entry).read_text(encoding="utf-8",errors="replace")
    if marker not in html:
        print(f"ERROR: generated entry page does not disclose exact source ref {marker}", file=sys.stderr)
        return 9
    if "Generated reference projection" not in html:
        print("ERROR: generated entry page lacks non-authority projection boundary", file=sys.stderr)
        return 10

    evidence={
        "schema_version":1,
        "version_id":args.version,
        "semantic_source_ref":reg["semantic_source_ref"],
        "lifecycle_state":reg["lifecycle_state"],
        "target_subpath":cfg["target_subpath"],
        "widoco_version":adapter["adapter_version"],
        "widoco_jar_sha256":actual_jar,
        "config":cfg["config"],
        "ontology_input_sha256":sha256(args.ontology),
        "documentation_fingerprint":reg["documentation_input"]["fingerprint"],
        "widoco_process_exit_code":proc.returncode,
        "entry_page":entry,
        "generated_file_count":sum(1 for p in args.output.rglob("*") if p.is_file()),
        "manual_generated_html_edits_prohibited":adapter["invocation"]["manual_generated_html_edits_prohibited"],
        "webvowl_enabled":adapter["invocation"]["webvowl"],
        "oops_enabled":adapter["invocation"]["oops"],
        "generation_result":"PASS"
    }
    args.manifest_output.parent.mkdir(parents=True,exist_ok=True)
    args.manifest_output.write_text(json.dumps(evidence,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    (args.output/"cmpe-generation-manifest.json").write_text(json.dumps(evidence,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(evidence,indent=2,sort_keys=True))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
