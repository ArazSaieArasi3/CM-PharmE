#!/usr/bin/env python3
"""Static acceptance audit for version-bound WebVOWL candidates."""
from __future__ import annotations
import argparse, hashlib, json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

class Parser(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        for key in ("href","src"):
            if a.get(key): self.links.append(a[key])

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def local_targets(root:Path,html:Path):
    p=Parser(); p.feed(html.read_text(encoding="utf-8",errors="replace"))
    broken=[]; checked=0
    for raw in p.links:
        parts=urlsplit(raw)
        if parts.scheme or parts.netloc or raw.startswith(("#","mailto:","tel:","data:")): continue
        target=(html.parent/unquote(parts.path)).resolve()
        try: target.relative_to(root.resolve())
        except ValueError: broken.append((str(html),raw,"escapes root")); continue
        if target.is_dir(): target=target/"index.html"
        checked+=1
        if not target.exists(): broken.append((str(html),raw,"missing"))
    return checked,broken

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--site",type=Path,required=True); ap.add_argument("--output",type=Path,required=True); args=ap.parse_args()
    routes={"v1":"ontology/v1.0.0","v2":"ontology/v2/current"}
    reports={}; errors=[]; hashes={}
    for vid,route in routes.items():
        root=args.site/route/"explore"
        mf=root/"explorer-manifest.json"; wrapper=root/"index.html"; inner=root/"webvowl/index.html"; data=root/"webvowl/data/cmpe.json"
        for p in (mf,wrapper,inner,data):
            if not p.is_file(): errors.append(f"{vid}: missing {p}")
        if not mf.is_file(): continue
        m=json.loads(mf.read_text())
        if m["version_id"]!=vid: errors.append(f"{vid}: manifest version mismatch")
        if m["bundled_dataset_count"]!=1: errors.append(f"{vid}: expected exactly one bundled dataset")
        if m["ontology_selector_disabled"] is not True: errors.append(f"{vid}: selector lock missing")
        if m["generated_artifacts_are_authority"] is not False: errors.append(f"{vid}: explorer marked authoritative")
        if m["vowl_counts"]["classes"]<=0: errors.append(f"{vid}: no VOWL classes")
        w=wrapper.read_text(encoding="utf-8",errors="replace") if wrapper.is_file() else ""
        for needle in (m["semantic_source_ref"],"Interactive exploration","Formal reference","Research Wiki","webvowl/index.html#cmpe"):
            if needle not in w: errors.append(f"{vid}: wrapper missing {needle}")
        ih=inner.read_text(encoding="utf-8",errors="replace") if inner.is_file() else ""
        if "cmpe-webvowl-route-lock" not in ih: errors.append(f"{vid}: inner route lock marker missing")
        datasets=list((root/"webvowl/data").glob("*.json"))
        if [p.name for p in datasets] != ["cmpe.json"]: errors.append(f"{vid}: sample/data leakage {[p.name for p in datasets]}")
        c1,b1=local_targets(root/"webvowl",inner) if inner.is_file() else (0,[])
        if b1: errors.extend(f"{vid}: broken asset {x}" for x in b1)
        hashes[vid]=sha(data) if data.is_file() else None
        reports[vid]={"vowl_json_sha256":hashes[vid],"classes":m["vowl_counts"]["classes"],"properties":m["vowl_counts"]["properties"],"local_assets_checked":c1,"broken_local_assets":len(b1),"source_ref":m["semantic_source_ref"]}
    if hashes.get("v1") and hashes.get("v2") and hashes["v1"]==hashes["v2"]:
        errors.append("V1 and V2 VOWL datasets are byte-identical; possible route/config leakage")
    result={"schema_version":1,"issue":272,"result":"PASS" if not errors else "FAIL","versions":reports,"version_dataset_isolation":hashes.get("v1")!=hashes.get("v2"),"errors":errors,"public_browser_verification":"DEFERRED_TO_#275"}
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(args.output.read_text())
    raise SystemExit(0 if not errors else 1)
if __name__=="__main__": main()
