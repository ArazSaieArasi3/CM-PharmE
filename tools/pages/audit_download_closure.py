#!/usr/bin/env python3
"""Final acceptance audit for PAGES-06 / #273."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
REGISTRY=ROOT/"docs/documentation/ontology-version-registry.json"
BUILD=ROOT/"docs/documentation/ontology-documentation-build-contract.json"
DOWNLOAD=ROOT/"docs/documentation/download-bundle-contract.json"

def load(path:Path)->dict:
    return json.loads(path.read_text(encoding="utf-8"))

def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def version_route(v:dict)->str:
    return (v.get("immutable_version_path") or v.get("current_path")).strip("/")

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--site",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()

    reg=load(REGISTRY)
    build=load(BUILD)
    dl=load(DOWNLOAD)
    errors=[]
    urls=[]
    checks=[]

    reg_by={v["id"]:v for v in reg["versions"]}
    build_by={v["id"]:v for v in build["versions"]}

    if dl["common"].get("generic_latest_route_prohibited") is not True:
        errors.append("generic latest route is not prohibited")
    if dl["common"].get("verify_graph_isomorphism") is not True:
        errors.append("graph-isomorphism verification must be required")
    if dl["common"].get("verify_checksums") is not True:
        errors.append("checksum verification must be required")
    if dl["common"].get("evolution_boundary_required") is not True:
        errors.append("evolution boundary must be required")
    if reg.get("path_policy",{}).get("stable_version_paths_immutable") is not True:
        errors.append("stable version paths are not declared immutable")
    if reg.get("path_policy",{}).get("historical_overwrite_prohibited") is not True:
        errors.append("historical overwrite is not prohibited")

    for vid,dvc in dl["versions"].items():
        rv=reg_by.get(vid)
        bv=build_by.get(vid)
        if not rv or not bv:
            errors.append(f"{vid}: missing registry/build contract")
            continue
        route=version_route(rv)
        expected=f"{route}/downloads/"
        if dvc["target_subpath"] != expected:
            errors.append(f"{vid}: download target mismatch {dvc['target_subpath']} != {expected}")
        if dvc["source_ref"] != rv["semantic_source_ref"] or dvc["source_ref"] != bv["semantic_source_ref"]:
            errors.append(f"{vid}: source-ref contract mismatch")
        if dvc.get("evolution",{}).get("generated_changelog_replaces_curated_evolution") is not False:
            errors.append(f"{vid}: changelog/evolution boundary violated")

        bundle=args.site/route/"downloads"
        manifest_path=bundle/"download-manifest.json"
        prov_path=bundle/"provenance.json"
        sums_path=bundle/"SHA256SUMS.txt"
        page_path=bundle/"index.html"
        prov_page=args.site/route/"provenance"/"index.html"
        for p in (manifest_path,prov_path,sums_path,page_path,prov_page):
            if not p.is_file():
                errors.append(f"{vid}: missing assembled path {p.relative_to(args.site) if p.exists() else p}")
        if errors and not manifest_path.is_file():
            continue

        manifest=load(manifest_path)
        prov=load(prov_path)
        if manifest.get("version_id") != vid:
            errors.append(f"{vid}: manifest version mismatch")
        if manifest.get("semantic_source_ref") != rv["semantic_source_ref"]:
            errors.append(f"{vid}: manifest source ref mismatch")
        if manifest.get("canonical_graph_fingerprint_sha256") != rv["documentation_input"]["fingerprint"]:
            errors.append(f"{vid}: manifest fingerprint mismatch")
        if manifest.get("generated_artifacts_are_authority") is not False:
            errors.append(f"{vid}: generated artifacts incorrectly marked authoritative")
        if manifest.get("download_route") != "/"+expected:
            errors.append(f"{vid}: manifest route mismatch")
        if manifest.get("citation_guidance_path") != f"/{route}/citation/":
            errors.append(f"{vid}: citation path mismatch")
        if not manifest.get("repository_url") or not manifest.get("semantic_source_url"):
            errors.append(f"{vid}: repository/source links missing")
        evo=manifest.get("evolution",{})
        if "does not replace" not in evo.get("boundary",""):
            errors.append(f"{vid}: evolution boundary text missing")

        if prov.get("semantic_source_ref") != rv["semantic_source_ref"]:
            errors.append(f"{vid}: provenance source ref mismatch")
        if prov.get("canonical_graph_fingerprint_sha256") != bv["expected_fingerprint"]["value"]:
            errors.append(f"{vid}: provenance fingerprint mismatch")
        if prov.get("citation_status") != rv["citation_status"]:
            errors.append(f"{vid}: provenance citation status mismatch")

        sums={}
        for line in sums_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            digest,name=line.split("  ",1)
            sums[name]=digest

        advertised={a["filename"]:a for a in manifest["artifacts"]}
        expected_roles=set(dl["common"]["required_serialization_roles"])
        got_roles={a["role"] for a in manifest["artifacts"]}
        if got_roles != expected_roles:
            errors.append(f"{vid}: advertised serialization roles differ from contract")
        if not all(manifest.get("serialization_equivalence",{}).get(name) is True for name in advertised):
            errors.append(f"{vid}: one or more serialization equivalence results are not PASS")

        page=page_path.read_text(encoding="utf-8")
        prov_html=prov_page.read_text(encoding="utf-8")
        if rv["semantic_source_ref"] not in prov_html:
            errors.append(f"{vid}: provenance page lacks exact source ref")
        if "Generated-artifact boundary" not in page:
            errors.append(f"{vid}: download page lacks authority boundary")
        if "does not replace the curated research-evolution narrative" not in page:
            errors.append(f"{vid}: rendered evolution boundary missing")

        for name,item in sorted(advertised.items()):
            path=bundle/name
            if not path.is_file():
                errors.append(f"{vid}: missing advertised file {name}")
                continue
            actual=sha256(path)
            if item["sha256"] != actual:
                errors.append(f"{vid}: manifest checksum mismatch {name}")
            if sums.get(name) != actual:
                errors.append(f"{vid}: SHA256SUMS mismatch {name}")
            if name not in page:
                errors.append(f"{vid}: rendered download page does not advertise {name}")
            urls.append({
                "version_id":vid,
                "lifecycle_state":rv["lifecycle_state"],
                "path":f"/{route}/downloads/{name}",
                "kind":"serialization",
                "role":item["role"],
                "sha256":actual,
                "semantic_source_ref":rv["semantic_source_ref"],
                "canonical_graph_fingerprint_sha256":rv["documentation_input"]["fingerprint"],
                "citation_guidance_path":f"/{route}/citation/",
            })

        for name,kind in (
            ("download-manifest.json","download_manifest"),
            ("provenance.json","provenance"),
            ("SHA256SUMS.txt","checksums"),
        ):
            path=bundle/name
            urls.append({
                "version_id":vid,
                "lifecycle_state":rv["lifecycle_state"],
                "path":f"/{route}/downloads/{name}",
                "kind":kind,
                "sha256":sha256(path),
                "semantic_source_ref":rv["semantic_source_ref"],
            })

        checks.append({
            "version_id":vid,
            "target_subpath":dvc["target_subpath"],
            "lifecycle_state":rv["lifecycle_state"],
            "immutable_version_path":rv.get("immutable_version_path"),
            "current_path":rv.get("current_path"),
            "semantic_release":rv.get("semantic_release"),
            "semantic_source_ref":rv["semantic_source_ref"],
            "advertised_serialization_count":len(advertised),
            "all_serializations_graph_equivalent":all(manifest.get("serialization_equivalence",{}).get(name) is True for name in advertised),
            "checksums_verified":all(sums.get(name)==sha256(bundle/name) for name in advertised),
        })

    # Explicit lifecycle assertions for current supported families.
    v1=reg_by["v1"]; v2=reg_by["v2"]
    if v1["lifecycle_state"]!="stable" or v1.get("immutable_version_path")!="ontology/v1.0.0/":
        errors.append("v1 stable immutable-path contract violated")
    if v2["lifecycle_state"]!="evolving" or v2.get("current_path")!="ontology/v2/current/":
        errors.append("v2 evolving/current-path contract violated")
    if v2.get("semantic_release") is not None:
        errors.append("v2 evolving entry must not claim a semantic release")
    if "Evolving" not in v2.get("public_status_label",""):
        errors.append("v2 public status does not disclose evolving state")

    # No generic latest paths in assembled candidate or advertised inventory.
    if any("/latest/" in u["path"] for u in urls):
        errors.append("generic latest path detected")
    if any(p.name=="latest" for p in args.site.rglob("*") if p.is_dir()):
        errors.append("generic latest directory detected")

    # V1/V2 isolation.
    if dl["versions"]["v1"]["target_subpath"] == dl["versions"]["v2"]["target_subpath"]:
        errors.append("v1/v2 download routes collide")

    report={
        "schema_version":1,
        "issue":273,
        "result":"PASS" if not errors else "FAIL",
        "authority_model":reg["authority_model"],
        "acceptance_summary":{
            "every_download_registry_bound":not any("manifest version mismatch" in e or "missing registry" in e for e in errors),
            "v1_v2_isolation":dl["versions"]["v1"]["target_subpath"] != dl["versions"]["v2"]["target_subpath"],
            "checksums_exposed_and_verified":not any("checksum" in e.lower() for e in errors),
            "serialization_equivalence_verified":not any("equivalence" in e.lower() for e in errors),
            "generated_not_authority":not any("authoritative" in e.lower() for e in errors),
            "changelog_boundary_preserved":not any("evolution boundary" in e.lower() for e in errors),
            "v2_evolving_nonfrozen":v2["lifecycle_state"]=="evolving" and v2.get("semantic_release") is None,
            "stable_paths_immutable":reg["path_policy"]["stable_version_paths_immutable"] is True,
            "machine_metadata_source_and_citation_links":not any("repository/source" in e or "citation path" in e for e in errors),
            "future_version_common_pattern_contract":dl["future_version_contract"]["copied_workflow_allowed"] is False,
        },
        "versions":checks,
        "url_path_inventory":sorted(urls,key=lambda x:x["path"]),
        "advertised_public_artifact_count":len(urls),
        "errors":errors,
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(args.output.read_text(encoding="utf-8"))
    return 0 if report["result"]=="PASS" else 1

if __name__=="__main__":
    raise SystemExit(main())
