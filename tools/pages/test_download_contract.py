#!/usr/bin/env python3
"""Validate download-contract isolation and future-version pattern."""
from __future__ import annotations
import copy, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
REG=ROOT/"docs/documentation/ontology-version-registry.json"
CON=ROOT/"docs/documentation/download-bundle-contract.json"

def route(v):
    return (v.get("immutable_version_path") or v.get("current_path")).strip("/") + "/downloads/"

def validate(registry, contract):
    errors=[]
    seen={}
    versions={v["id"]:v for v in registry["versions"]}
    for vid,d in contract["versions"].items():
        if vid not in versions:
            errors.append(f"{vid}: missing registry version"); continue
        expected=route(versions[vid])
        if d["target_subpath"] != expected:
            errors.append(f"{vid}: target {d['target_subpath']} != {expected}")
        prior=seen.get(d["target_subpath"])
        if prior and prior != vid:
            errors.append(f"{vid}: route collision with {prior}: {d['target_subpath']}")
        seen[d["target_subpath"]]=vid
        if d["source_ref"] != versions[vid]["semantic_source_ref"]:
            errors.append(f"{vid}: source-ref mismatch")
        if d.get("evolution",{}).get("generated_changelog_replaces_curated_evolution") is not False:
            errors.append(f"{vid}: changelog boundary must remain false")
    return errors

def main():
    reg=json.loads(REG.read_text())
    con=json.loads(CON.read_text())
    assert not validate(reg,con), validate(reg,con)

    v3=copy.deepcopy(reg["versions"][-1])
    v3.update({
        "id":"v3","version_family":"CM-PharmE 3.x","reader_label":"CM-PharmE 3.x dry-run",
        "lifecycle_state":"evolving","semantic_release":None,
        "semantic_source_ref":"dry-run-only@"+"3"*40,
        "semantic_source_paths":["dry-run/not-published/ontology/source/modules/"],
        "immutable_version_path":None,"current_path":"ontology/v3/current/",
        "citation_status":"dry_run_not_publishable","supersedes":"v2","superseded_by":None,
        "public_status_label":"DRY RUN ONLY — no scientific content may be published."
    })
    vr=copy.deepcopy(reg); vr["versions"].append(v3)
    vc=copy.deepcopy(con)
    vc["versions"]["v3"]={
        "source_ref":v3["semantic_source_ref"],
        "target_subpath":"ontology/v3/current/downloads/",
        "files":copy.deepcopy(con["versions"]["v2"]["files"]),
        "evolution":{
            "repository_changelog":"CHANGELOG.md",
            "curated_wiki_page":"V1-to-V2-Research-Evolution",
            "generated_changelog_replaces_curated_evolution":False
        }
    }
    assert not validate(vr,vc), validate(vr,vc)

    collision=copy.deepcopy(vc)
    collision["versions"]["v3"]["target_subpath"]="ontology/v2/current/downloads/"
    errs=validate(vr,collision)
    assert any("collision" in e or "target" in e for e in errs), errs

    print("PASS: production isolation + V3 common-pattern dry run + collision negative test.")

if __name__=="__main__":
    main()
