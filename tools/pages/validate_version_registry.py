#!/usr/bin/env python3
"""Validate and resolve the CM-PharmE multi-version Pages registry.

This is intentionally stdlib-only so the registry contract can be checked
before the heavier Pages/WIDOCO toolchain is introduced.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_REGISTRY = Path("docs/documentation/ontology-version-registry.json")
SHA_REF = re.compile(r"^.+@[0-9a-f]{40}$")
ID_RE = re.compile(r"^v[0-9]+$")

REQUIRED = {
    "id", "version_family", "reader_label", "lifecycle_state",
    "semantic_source_ref", "semantic_source_paths", "assembly_rule",
    "documentation_input", "generated_reference_enabled", "webvowl_enabled",
    "immutable_version_path", "current_path", "documentation_baseline_binding",
    "citation_status", "supersedes", "superseded_by", "public_status_label",
}
LIFECYCLES = {"evolving", "candidate", "stable", "frozen", "historical"}


def load_registry(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("registry_schema_version") != "1.0":
        errors.append("registry_schema_version must be 1.0")
    if data.get("repository") != "ArazSaieArasi3/CM-PharmE":
        errors.append("repository must identify ArazSaieArasi3/CM-PharmE")

    policy = data.get("path_policy") or {}
    for flag in (
        "stable_version_paths_immutable",
        "historical_overwrite_prohibited",
        "release_bound_requires_exact_source_ref",
    ):
        if policy.get(flag) is not True:
            errors.append(f"path_policy.{flag} must be true")

    versions = data.get("versions")
    if not isinstance(versions, list) or len(versions) < 2:
        errors.append("versions must contain at least V1 and V2")
        return errors

    ids: set[str] = set()
    paths: dict[str, str] = {}
    for version in versions:
        vid = version.get("id", "<missing>")
        missing = sorted(REQUIRED - set(version))
        if missing:
            errors.append(f"{vid}: missing required fields: {', '.join(missing)}")
        if not isinstance(vid, str) or not ID_RE.fullmatch(vid):
            errors.append(f"{vid}: id must match vN")
        if vid in ids:
            errors.append(f"{vid}: duplicate version id")
        ids.add(vid)

        lifecycle = version.get("lifecycle_state")
        if lifecycle not in LIFECYCLES:
            errors.append(f"{vid}: invalid lifecycle_state {lifecycle!r}")

        ref = version.get("semantic_source_ref")
        if not isinstance(ref, str) or not SHA_REF.fullmatch(ref):
            errors.append(f"{vid}: semantic_source_ref must end in an exact 40-char commit SHA")

        source_paths = version.get("semantic_source_paths")
        if not isinstance(source_paths, list) or not source_paths:
            errors.append(f"{vid}: semantic_source_paths must be non-empty")

        doc_input = version.get("documentation_input") or {}
        if doc_input.get("kind") != "deterministic_assembled_ontology":
            errors.append(f"{vid}: documentation_input.kind must be deterministic_assembled_ontology")
        if doc_input.get("build_contract_issue") != 269:
            errors.append(f"{vid}: documentation_input.build_contract_issue must be #269")

        immutable = version.get("immutable_version_path")
        current = version.get("current_path")
        if lifecycle in {"stable", "frozen", "historical"} and not immutable:
            errors.append(f"{vid}: stable/frozen/historical version requires immutable_version_path")
        if lifecycle == "evolving" and not current:
            errors.append(f"{vid}: evolving version requires current_path")

        for kind, value in (("immutable", immutable), ("current", current)):
            if value is None:
                continue
            if not isinstance(value, str) or not value.startswith("ontology/") or not value.endswith("/"):
                errors.append(f"{vid}: {kind} path must be an ontology/.../ directory path")
                continue
            previous = paths.get(value)
            if previous and previous != vid:
                errors.append(f"{vid}: route collision at {value!r} with {previous}")
            paths[value] = vid

    if "v1" not in ids or "v2" not in ids:
        errors.append("registry must contain explicit v1 and v2 entries")

    future = data.get("future_version_contract") or {}
    if future.get("onboarding_mechanism") != "add_registry_entry_then_common_pipeline":
        errors.append("future_version_contract must use common-pipeline registry onboarding")
    if future.get("copied_workflow_allowed") is not False:
        errors.append("future_version_contract.copied_workflow_allowed must be false")
    if future.get("fictional_or_unreleased_scientific_content_must_not_be_published") is not True:
        errors.append("future-version dry runs must prohibit publishing fictional scientific content")

    return errors


def resolve(data: dict, version_id: str) -> dict:
    for version in data["versions"]:
        if version["id"] == version_id:
            path = version["immutable_version_path"] or version["current_path"]
            return {
                "id": version["id"],
                "reader_label": version["reader_label"],
                "lifecycle_state": version["lifecycle_state"],
                "semantic_source_ref": version["semantic_source_ref"],
                "semantic_source_paths": version["semantic_source_paths"],
                "assembly_rule": version["assembly_rule"],
                "documentation_input": version["documentation_input"],
                "output_path": path,
                "generated_reference_enabled": version["generated_reference_enabled"],
                "webvowl_enabled": version["webvowl_enabled"],
                "citation_status": version["citation_status"],
                "public_status_label": version["public_status_label"],
            }
    raise KeyError(version_id)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--resolve", metavar="VERSION_ID")
    args = parser.parse_args()

    data = load_registry(args.registry)
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    if args.resolve:
        try:
            print(json.dumps(resolve(data, args.resolve), indent=2))
        except KeyError:
            print(f"ERROR: unknown version id: {args.resolve}", file=sys.stderr)
            return 2
    else:
        print(f"PASS: {len(data['versions'])} version entries; no route collisions; exact source refs present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
