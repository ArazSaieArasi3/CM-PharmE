#!/usr/bin/env python3
"""Validate the Pages ontology documentation build contract against the version registry."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "docs/documentation/ontology-version-registry.json"
CONTRACT = ROOT / "docs/documentation/ontology-documentation-build-contract.json"
SHA = re.compile(r"^.+@[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def fail(msg: str, errors: list[str]) -> None:
    errors.append(msg)


def main() -> int:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    errors: list[str] = []

    reg = {v["id"]: v for v in registry["versions"]}
    seen: set[str] = set()

    policy = contract.get("policy", {})
    for key in (
        "arbitrary_ttl_input_prohibited",
        "semantic_validation_failure_blocks_publication",
        "generated_documentation_must_consume_resolved_artifact",
        "generated_distributions_are_not_authoring_authority",
        "version_specific_validation_boundaries_must_be_preserved",
    ):
        if policy.get(key) is not True:
            fail(f"policy.{key} must be true", errors)

    for item in contract.get("versions", []):
        vid = item.get("id")
        if vid in seen:
            fail(f"{vid}: duplicate build contract", errors)
        seen.add(vid)
        if vid not in reg:
            fail(f"{vid}: no matching registry entry", errors)
            continue
        rv = reg[vid]

        if item.get("registry_version_id") != vid:
            fail(f"{vid}: registry_version_id mismatch", errors)
        if item.get("lifecycle_state") != rv.get("lifecycle_state"):
            fail(f"{vid}: lifecycle state differs from registry", errors)
        if item.get("semantic_source_ref") != rv.get("semantic_source_ref"):
            fail(f"{vid}: exact semantic source ref differs from registry", errors)
        if not SHA.fullmatch(item.get("semantic_source_ref", "")):
            fail(f"{vid}: semantic_source_ref must be exact SHA-bound ref", errors)

        source_root = item.get("canonical_source_root", "")
        reg_paths = rv.get("semantic_source_paths", [])
        if not any(p == source_root or p.startswith(source_root) for p in reg_paths):
            fail(f"{vid}: canonical source root not represented in registry source paths", errors)

        module = item.get("module_selection", {})
        if module.get("ordering") != "lexicographic_path_order":
            fail(f"{vid}: module ordering must be deterministic lexicographic_path_order", errors)

        build = item.get("build", {})
        for required in ("tool","command","documentation_input_artifact","build_manifest"):
            if not build.get(required):
                fail(f"{vid}: build.{required} is required", errors)
        if "<OUTPUT_ROOT>" not in build.get("command", ""):
            fail(f"{vid}: build command must parameterize isolated <OUTPUT_ROOT>", errors)

        fp = item.get("expected_fingerprint", {})
        if fp.get("algorithm") != "sha256" or fp.get("representation") != "canonical_ntriples":
            fail(f"{vid}: fingerprint must be SHA-256 over canonical N-Triples", errors)
        if not HEX64.fullmatch(fp.get("value", "")):
            fail(f"{vid}: expected fingerprint must be 64 lowercase hex chars", errors)

        boundary = item.get("validation_boundary", {})
        if boundary.get("required_before_pages") is not True:
            fail(f"{vid}: semantic validation must be required before Pages publication", errors)
        if not boundary.get("pages_status_label"):
            fail(f"{vid}: Pages lifecycle/status label is required", errors)

    missing = set(reg) - seen
    if missing:
        fail("registry versions missing build contracts: " + ", ".join(sorted(missing)), errors)

    if contract.get("future_version_contract", {}).get("copied_pages_workflow_allowed") is not False:
        fail("future versions must not require copied Pages workflows", errors)

    if errors:
        for e in errors:
            print("ERROR:", e, file=sys.stderr)
        return 1

    print(f"PASS: {len(seen)} registry versions have deterministic, SHA-bound documentation build contracts.")
    for item in contract["versions"]:
        print(f"{item['id']}: {item['build']['tool']} -> {item['build']['documentation_input_artifact']} @ {item['expected_fingerprint']['value']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
