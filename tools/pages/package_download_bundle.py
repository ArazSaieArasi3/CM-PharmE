#!/usr/bin/env python3
"""Package governed CM-PharmE ontology serializations for Pages downloads."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

from rdflib import Graph
from rdflib.compare import isomorphic

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "docs/documentation/ontology-version-registry.json"
BUILD_CONTRACT = ROOT / "docs/documentation/ontology-documentation-build-contract.json"
DOWNLOAD_CONTRACT = ROOT / "docs/documentation/download-bundle-contract.json"
REPO_URL = "https://github.com/ArazSaieArasi3/CM-PharmE"
WIKI_URL = REPO_URL + "/wiki"

FORMATS = {
    "turtle": "turtle",
    "rdfxml_owl": "xml",
    "rdfxml_rdf": "xml",
    "jsonld": "json-ld",
    "canonical_ntriples": "nt",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def exact_source_url(source_ref: str) -> str:
    _, sha = source_ref.rsplit("@", 1)
    return f"{REPO_URL}/tree/{sha}"


def version_route(version: dict) -> str:
    route = version.get("immutable_version_path") or version.get("current_path")
    if not route:
        raise ValueError(f"{version['id']}: no version route")
    return route.strip("/") + "/"


def ensure_empty(path: Path) -> None:
    if path.exists() and any(path.iterdir()):
        raise SystemExit(f"ERROR: refusing to overwrite non-empty download bundle: {path}")
    path.mkdir(parents=True, exist_ok=True)


def parse(path: Path, fmt: str) -> Graph:
    return Graph().parse(path, format=fmt)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--version", required=True)
    p.add_argument("--build-root", type=Path, required=True)
    p.add_argument("--source-ref", required=True)
    p.add_argument("--output-root", type=Path, required=True)
    args = p.parse_args()

    registry = load_json(REGISTRY)
    builds = load_json(BUILD_CONTRACT)
    downloads = load_json(DOWNLOAD_CONTRACT)

    rv = next((v for v in registry["versions"] if v["id"] == args.version), None)
    bv = next((v for v in builds["versions"] if v["id"] == args.version), None)
    dv = downloads["versions"].get(args.version)
    if not rv or not bv or not dv:
        print(f"ERROR: incomplete registry/build/download contract for {args.version}", file=sys.stderr)
        return 2

    if args.source_ref != rv["semantic_source_ref"] or args.source_ref != bv["semantic_source_ref"] or args.source_ref != dv["source_ref"]:
        print("ERROR: source-ref mismatch across registry/build/download contract", file=sys.stderr)
        return 3

    expected_route = version_route(rv) + "downloads/"
    if dv["target_subpath"] != expected_route:
        print(f"ERROR: download route mismatch: {dv['target_subpath']} != {expected_route}", file=sys.stderr)
        return 4

    bundle = args.output_root / dv["target_subpath"]
    ensure_empty(bundle)

    ref_rel = bv["build"]["documentation_input_artifact"]
    ref_path = args.build_root / ref_rel
    if not ref_path.is_file():
        print(f"ERROR: governed reference artifact missing: {ref_path}", file=sys.stderr)
        return 5
    reference = parse(ref_path, "turtle")

    artifacts = []
    equivalence = {}
    seen_names = set()
    for role in downloads["common"]["required_serialization_roles"]:
        rel = dv["files"].get(role)
        if not rel:
            print(f"ERROR: missing contracted serialization role {role}", file=sys.stderr)
            return 6
        src = args.build_root / rel
        if not src.is_file():
            print(f"ERROR: build output missing contracted artifact {src}", file=sys.stderr)
            return 7
        dest = bundle / src.name
        if dest.name in seen_names:
            print(f"ERROR: duplicate advertised download filename {dest.name}", file=sys.stderr)
            return 8
        seen_names.add(dest.name)
        shutil.copyfile(src, dest)
        parsed = parse(dest, FORMATS[role])
        same = isomorphic(reference, parsed)
        equivalence[dest.name] = same
        if not same:
            print(f"ERROR: {dest.name} is not graph-isomorphic to governed reference input", file=sys.stderr)
            return 9
        artifacts.append({
            "role": role,
            "filename": dest.name,
            "sha256": sha256_file(dest),
            "bytes": dest.stat().st_size,
            "graph_isomorphic_to_governed_input": True,
            "generated_not_authority": True,
        })

    source_sha = args.source_ref.rsplit("@", 1)[1]
    build_manifest = args.build_root / bv["build"]["build_manifest"]
    if not build_manifest.is_file():
        print(f"ERROR: upstream build manifest missing: {build_manifest}", file=sys.stderr)
        return 10

    route = version_route(rv)
    manifest = {
        "schema_version": 1,
        "version_id": rv["id"],
        "version_family": rv["version_family"],
        "reader_label": rv["reader_label"],
        "lifecycle_state": rv["lifecycle_state"],
        "public_status_label": rv["public_status_label"],
        "semantic_release": rv["semantic_release"],
        "semantic_source_ref": rv["semantic_source_ref"],
        "semantic_source_url": exact_source_url(rv["semantic_source_ref"]),
        "canonical_graph_fingerprint_sha256": rv["documentation_input"]["fingerprint"],
        "download_route": "/" + dv["target_subpath"],
        "version_root": "/" + route,
        "citation_guidance_path": "/" + route + "citation/",
        "research_wiki_url": WIKI_URL,
        "repository_url": REPO_URL,
        "generated_artifacts_are_authority": False,
        "generated_artifacts_label": "Generated publication artifacts derived from governed semantic source.",
        "artifacts": artifacts,
        "serialization_equivalence": equivalence,
    }
    (bundle / "download-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    provenance = {
        "schema_version": 1,
        "version_id": rv["id"],
        "semantic_source_ref": rv["semantic_source_ref"],
        "semantic_source_commit_sha": source_sha,
        "semantic_source_paths": rv["semantic_source_paths"],
        "build_tool": bv["build"]["tool"],
        "build_contract_issue": 269,
        "download_contract_issue": 273,
        "upstream_build_manifest": bv["build"]["build_manifest"],
        "upstream_build_manifest_sha256": sha256_file(build_manifest),
        "governed_documentation_input": ref_rel,
        "governed_documentation_input_sha256": sha256_file(ref_path),
        "canonical_graph_fingerprint_sha256": bv["expected_fingerprint"]["value"],
        "lifecycle_state": rv["lifecycle_state"],
        "citation_status": rv["citation_status"],
        "authority_statement": "Semantic Source defines; Pages downloads are generated projections.",
    }
    (bundle / "provenance.json").write_text(json.dumps(provenance, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    checksum_targets = sorted(
        [p for p in bundle.iterdir() if p.is_file() and p.name != "SHA256SUMS.txt"],
        key=lambda p: p.name,
    )
    lines = [f"{sha256_file(path)}  {path.name}\n" for path in checksum_targets]
    (bundle / "SHA256SUMS.txt").write_text("".join(lines), encoding="utf-8")

    # Verify the emitted checksum manifest immediately.
    for line in (bundle / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        expected, filename = line.split("  ", 1)
        actual = sha256_file(bundle / filename)
        if actual != expected:
            print(f"ERROR: emitted checksum mismatch for {filename}", file=sys.stderr)
            return 11

    summary = {
        "result": "PASS",
        "version_id": rv["id"],
        "download_route": "/" + dv["target_subpath"],
        "artifact_count": len(artifacts),
        "graph_equivalence_pass_count": sum(1 for v in equivalence.values() if v),
        "bundle_file_count": len([p for p in bundle.iterdir() if p.is_file()]),
        "checksums_verified": True,
        "source_ref": rv["semantic_source_ref"],
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
