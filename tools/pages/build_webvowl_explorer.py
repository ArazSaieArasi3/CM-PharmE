#!/usr/bin/env python3
"""Package a governed, version-bound static WebVOWL explorer."""
from __future__ import annotations
import argparse, hashlib, json, re, shutil, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
REGISTRY=ROOT/"docs/documentation/ontology-version-registry.json"
CONFIG=ROOT/"docs/documentation/webvowl-adapter.json"

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))

def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def tree_digest(root:Path)->str:
    h=hashlib.sha256()
    for p in sorted(x for x in root.rglob("*") if x.is_file()):
        rel=str(p.relative_to(root)).replace("\\","/")
        h.update(rel.encode()); h.update(b"\0"); h.update(sha256_file(p).encode()); h.update(b"\n")
    return h.hexdigest()

def route(v):
    return (v.get("immutable_version_path") or v.get("current_path")).strip("/")+"/explore/"

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--version",required=True)
    ap.add_argument("--frontend-root",type=Path,required=True)
    ap.add_argument("--vowl-json",type=Path,required=True)
    ap.add_argument("--ontology-input",type=Path,required=True)
    ap.add_argument("--source-ref",required=True)
    ap.add_argument("--output-root",type=Path,required=True)
    args=ap.parse_args()

    reg=load(REGISTRY); cfg=load(CONFIG)
    rv=next((v for v in reg["versions"] if v["id"]==args.version),None)
    vc=cfg["versions"].get(args.version)
    if rv is None or vc is None:
        print("ERROR: missing registry/WebVOWL version entry",file=sys.stderr); return 2
    if args.source_ref != rv["semantic_source_ref"] or args.source_ref != vc["semantic_source_ref"]:
        print("ERROR: source-ref mismatch",file=sys.stderr); return 3
    expected_route=route(rv)
    if vc["target_subpath"] != expected_route:
        print(f"ERROR: explorer route mismatch {vc['target_subpath']} != {expected_route}",file=sys.stderr); return 4

    actual_frontend_tree=tree_digest(args.frontend_root)
    expected_frontend_tree=cfg["webvowl"].get("expected_frontend_tree_sha256")
    if not expected_frontend_tree or actual_frontend_tree != expected_frontend_tree:
        print(f"ERROR: WebVOWL frontend tree drift {actual_frontend_tree} != {expected_frontend_tree}",file=sys.stderr); return 41

    actual_vowl_sha=sha256_file(args.vowl_json)
    expected_vowl_sha=vc.get("expected_vowl_json_sha256")
    if not expected_vowl_sha or actual_vowl_sha != expected_vowl_sha:
        print(f"ERROR: VOWL JSON drift for {args.version}: {actual_vowl_sha} != {expected_vowl_sha}",file=sys.stderr); return 42

    for p in (args.frontend_root/"index.html",args.frontend_root/"js/webvowl.js",args.frontend_root/"js/webvowl.app.js",args.vowl_json,args.ontology_input):
        if not p.is_file():
            print(f"ERROR: missing required input {p}",file=sys.stderr); return 5

    out=args.output_root/vc["target_subpath"]
    web=out/"webvowl"
    if out.exists() and any(out.iterdir()):
        print(f"ERROR: refusing to overwrite non-empty explorer route {out}",file=sys.stderr); return 6
    web.mkdir(parents=True,exist_ok=True)
    for item in args.frontend_root.iterdir():
        dst=web/item.name
        if item.is_dir(): shutil.copytree(item,dst)
        else: shutil.copy2(item,dst)

    # The pinned legacy release imports an HTTP Google font. Remove the optional
    # remote font so HTTPS Pages has no mixed-content request or network font dependency.
    app_css=web/"css/webvowl.app.css"
    css=app_css.read_text(encoding="utf-8")
    insecure_font="@import url(http://fonts.googleapis.com/css?family=Open+Sans);"
    if css.count(insecure_font)!=1:
        print("ERROR: unexpected WebVOWL font import contract",file=sys.stderr); return 44
    app_css.write_text(css.replace(insecure_font,"",1),encoding="utf-8")

    # Remove bundled sample ontologies. This route must contain only the governed dataset.
    data=web/"data"
    data.mkdir(parents=True,exist_ok=True)
    for p in data.iterdir():
        if p.is_file(): p.unlink()
        elif p.is_dir(): shutil.rmtree(p)
    target_data=data/vc["vowl_data_filename"]
    shutil.copy2(args.vowl_json,target_data)

    # Freeze source switching in the embedded app while retaining search/zoom/navigation.
    inner=web/"index.html"
    html=inner.read_text(encoding="utf-8",errors="replace")
    inject="""<style id="cmpe-webvowl-route-lock">
#c_select, #m_select, #converter-option { display: none !important; }
</style>
<meta name="cmpe-webvowl-route-lock" content="true">
"""
    if "</head>" not in html:
        print("ERROR: WebVOWL index has no </head>",file=sys.stderr); return 7
    html=html.replace("</head>",inject+"</head>",1)
    inner.write_text(html,encoding="utf-8")

    vowl=load(target_data)
    classes=vowl.get("class",[])
    props=vowl.get("property",[])
    if not isinstance(classes,list) or not classes:
        print("ERROR: VOWL JSON has no classes",file=sys.stderr); return 8
    if not isinstance(props,list):
        print("ERROR: VOWL property collection malformed",file=sys.stderr); return 9

    expected_counts=vc.get("expected_vowl_projection_counts") or {}
    actual_counts={"classes":len(classes),"properties":len(props)}
    if expected_counts and actual_counts != expected_counts:
        print(f"ERROR: VOWL projection counts drift for {args.version}: {actual_counts} != {expected_counts}",file=sys.stderr); return 43

    manifest={
      "schema_version":1,
      "version_id":args.version,
      "reader_label":rv["reader_label"],
      "lifecycle_state":rv["lifecycle_state"],
      "public_status_label":rv["public_status_label"],
      "semantic_source_ref":rv["semantic_source_ref"],
      "documentation_fingerprint":rv["documentation_input"]["fingerprint"],
      "explorer_route":"/"+vc["target_subpath"],
      "iframe_entry":"webvowl/index.html#cmpe",
      "vowl_data_path":"webvowl/data/"+vc["vowl_data_filename"],
      "vowl_json_sha256":actual_vowl_sha,
      "ontology_input_sha256":sha256_file(args.ontology_input),
      "webvowl_version":cfg["webvowl"]["version"],
      "webvowl_source_commit":cfg["webvowl"]["exact_source_commit"],
      "owl2vowl_version":cfg["owl2vowl"]["version"],
      "owl2vowl_source_commit":cfg["owl2vowl"]["exact_source_commit"],
      "frontend_tree_sha256_before_version_data":actual_frontend_tree,
      "packaged_explorer_tree_sha256":tree_digest(web),
      "vowl_counts":actual_counts,
      "bundled_dataset_count":len(list(data.glob("*.json"))),
      "ontology_selector_disabled":True,
      "generated_artifacts_are_authority":False,
      "interpretation":"Interactive exploration only; use the formal reference and canonical semantic source for complete specification."
    }
    (out/"explorer-manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(manifest,indent=2,sort_keys=True))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
