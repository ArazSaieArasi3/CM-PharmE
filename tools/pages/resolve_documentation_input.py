#!/usr/bin/env python3
"""Resolve and verify a governed ontology documentation input for Pages."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "docs/documentation/ontology-documentation-build-contract.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--build-root", type=Path, required=True)
    parser.add_argument("--source-ref", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    entry = next((v for v in contract["versions"] if v["id"] == args.version), None)
    if entry is None:
        print(f"ERROR: no build contract for {args.version}", file=sys.stderr)
        return 2

    if args.source_ref != entry["semantic_source_ref"]:
        print(
            f"ERROR: source ref mismatch for {args.version}: "
            f"{args.source_ref} != {entry['semantic_source_ref']}",
            file=sys.stderr,
        )
        return 3

    build_root = args.build_root.resolve()
    manifest_path = build_root / entry["build"]["build_manifest"]
    artifact_path = build_root / entry["build"]["documentation_input_artifact"]
    if not manifest_path.is_file():
        print(f"ERROR: missing build manifest: {manifest_path}", file=sys.stderr)
        return 4
    if not artifact_path.is_file():
        print(f"ERROR: missing documentation input artifact: {artifact_path}", file=sys.stderr)
        return 5

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if args.version == "v1":
        actual_fp = manifest.get("source_graph_sha256_canonical_nt")
    elif args.version == "v2":
        actual_fp = manifest.get("canonical_graph_sha256")
    else:
        actual_fp = manifest.get("canonical_graph_sha256") or manifest.get("source_graph_sha256_canonical_nt")

    expected_fp = entry["expected_fingerprint"]["value"]
    if actual_fp != expected_fp:
        print(
            f"ERROR: canonical graph fingerprint mismatch for {args.version}: "
            f"{actual_fp} != {expected_fp}",
            file=sys.stderr,
        )
        return 6

    evidence = {
        "schema_version": 1,
        "version_id": args.version,
        "semantic_source_ref": args.source_ref,
        "lifecycle_state": entry["lifecycle_state"],
        "documentation_input_artifact": entry["build"]["documentation_input_artifact"],
        "documentation_input_sha256": sha256_file(artifact_path),
        "build_manifest": entry["build"]["build_manifest"],
        "build_manifest_sha256": sha256_file(manifest_path),
        "canonical_graph_sha256": actual_fp,
        "expected_canonical_graph_sha256": expected_fp,
        "publication_gate": "PASS",
        "pages_status_label": entry["validation_boundary"]["pages_status_label"],
    }

    payload = json.dumps(evidence, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
