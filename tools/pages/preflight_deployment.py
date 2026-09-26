#!/usr/bin/env python3
"""Preflight a complete CM-PharmE GitHub Pages deployment candidate."""
from __future__ import annotations
import argparse, hashlib, json, os, re, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
REGISTRY=ROOT/"docs/documentation/ontology-version-registry.json"
POLICY=ROOT/"docs/documentation/pages-deployment-policy.json"
WIDOCO=ROOT/"docs/documentation/widoco-adapter.json"

SECRET_PATTERNS=[
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(rb"ghp_[A-Za-z0-9]{20,}"),
    re.compile(rb"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(rb"AKIA[0-9A-Z]{16}"),
]
FORBIDDEN_TEXT=[
    b"private expert response",
    b"begin private",
]

def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--site",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    ap.add_argument("--build-sha",default=os.environ.get("GITHUB_SHA","unknown"))
    ap.add_argument("--event-name",default=os.environ.get("GITHUB_EVENT_NAME","local"))
    ap.add_argument("--v2-trigger-sha",default="")
    args=ap.parse_args()

    site=args.site.resolve()
    reg=load(REGISTRY); policy=load(POLICY); widoco=load(WIDOCO)
    errors=[]; warnings=[]
    if not (site/"index.html").is_file(): errors.append("missing top-level index.html")
    if not (site/".nojekyll").is_file(): errors.append("missing .nojekyll")
    if policy["public_deploy_enabled"] is not False:
        warnings.append("public deployment policy is already enabled; this preflight slice expected staged=false")

    # V2 workflow bridge may only build a registered exact ref.
    if args.v2_trigger_sha:
        v2=next(v for v in reg["versions"] if v["id"]=="v2")
        registered=v2["semantic_source_ref"].rsplit("@",1)[1]
        if args.v2_trigger_sha != registered:
            errors.append(f"V2 workflow trigger SHA {args.v2_trigger_sha} is not the registered exact source SHA {registered}")

    # No symlinks and no obvious secrets/restricted markers.
    scanned=0
    for p in site.rglob("*"):
        if p.is_symlink():
            errors.append(f"symlink prohibited in Pages artifact: {p.relative_to(site)}")
        if not p.is_file(): continue
        scanned+=1
        if p.stat().st_size > 20*1024*1024:
            warnings.append(f"large public file >20MiB: {p.relative_to(site)}")
        data=p.read_bytes()
        for pat in SECRET_PATTERNS:
            if pat.search(data): errors.append(f"secret-like token detected: {p.relative_to(site)}")
        low=data.lower()
        for marker in FORBIDDEN_TEXT:
            if marker in low: errors.append(f"restricted marker detected: {p.relative_to(site)}")

    inventory=load(site/"route-inventory.json")
    for item in inventory["routes"]:
        route=item["route"].strip("/")
        path=site/route/"index.html" if route else site/"index.html"
        if not path.is_file(): errors.append(f"route inventory target missing: /{route}/")

    versions=[]
    for v in reg["versions"]:
        route=(v.get("immutable_version_path") or v.get("current_path")).strip("/")
        root=site/route
        for required in ("index.html","reference/index.html","downloads/index.html","provenance/index.html","citation/index.html"):
            if not (root/required).is_file(): errors.append(f"{v['id']}: missing {route}/{required}")
        # The public reference route must serve actual WIDOCO output, not the shell placeholder.
        ref=root/"reference"
        if not (ref/"index-en.html").is_file():
            errors.append(f"{v['id']}: missing WIDOCO index-en.html")
        elif sha256(ref/"index.html") != sha256(ref/"index-en.html"):
            errors.append(f"{v['id']}: reference/index.html is not the deterministic alias of WIDOCO index-en.html")
        else:
            text=(ref/"index.html").read_text(encoding="utf-8",errors="replace")
            if v["semantic_source_ref"] not in text: errors.append(f"{v['id']}: WIDOCO entry lacks exact source ref")
            if "Generated reference projection" not in text: errors.append(f"{v['id']}: WIDOCO entry lacks non-authority boundary")
        d=root/"downloads"
        for required in ("download-manifest.json","provenance.json","SHA256SUMS.txt"):
            if not (d/required).is_file(): errors.append(f"{v['id']}: missing download evidence {required}")
        versions.append({
          "id":v["id"],"route":"/"+route+"/","lifecycle_state":v["lifecycle_state"],
          "semantic_source_ref":v["semantic_source_ref"],
          "documentation_fingerprint":v["documentation_input"]["fingerprint"],
          "reference_entry_sha256":sha256(ref/"index.html") if (ref/"index.html").is_file() else None,
          "download_manifest_sha256":sha256(d/"download-manifest.json") if (d/"download-manifest.json").is_file() else None,
        })

    # Stable/current lifecycle safety.
    v1=next(v for v in reg["versions"] if v["id"]=="v1")
    v2=next(v for v in reg["versions"] if v["id"]=="v2")
    if v1["lifecycle_state"]!="stable" or v1["immutable_version_path"]!="ontology/v1.0.0/":
        errors.append("V1 immutable stable route contract violated")
    if v2["lifecycle_state"]!="evolving" or v2["current_path"]!="ontology/v2/current/" or v2["semantic_release"] is not None:
        errors.append("V2 evolving/current route contract violated")
    if (site/"ontology/latest").exists(): errors.append("generic latest ontology path prohibited")

    manifest={
      "schema_version":1,
      "issue":275,
      "result":"PASS" if not errors else "FAIL",
      "build_commit_sha":args.build_sha,
      "event_name":args.event_name,
      "version_registry_sha256":sha256(REGISTRY),
      "deployment_policy_sha256":sha256(POLICY),
      "authority_model":reg["authority_model"],
      "generator_versions":{
        "widoco":widoco["adapter_version"],
        "widoco_jar_sha256":widoco["release_asset"]["sha256"],
        "configure_pages":policy["toolchain"]["configure_pages"],
        "upload_pages_artifact":policy["toolchain"]["upload_pages_artifact"],
        "deploy_pages":policy["toolchain"]["deploy_pages"],
      },
      "public_deploy_enabled":policy["public_deploy_enabled"],
      "webvowl_status":"DEFERRED_TO_ISSUE_272",
      "rendered_public_verification_status":"DEFERRED_UNTIL_PUBLIC_DEPLOYMENT",
      "scanned_public_file_count":scanned,
      "versions":versions,
      "errors":errors,
      "warnings":warnings,
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(args.output.read_text())
    return 0 if not errors else 1

if __name__=="__main__":
    raise SystemExit(main())
