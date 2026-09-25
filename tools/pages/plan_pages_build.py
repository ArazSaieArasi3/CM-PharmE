#!/usr/bin/env python3
"""Create the deterministic multi-version Pages build plan from the registry."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / "tools/pages/validate_version_registry.py"
DEFAULT_REGISTRY = ROOT / "docs/documentation/ontology-version-registry.json"

spec = importlib.util.spec_from_file_location("registry_validator", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    args = parser.parse_args()

    data = validator.load_registry(args.registry)
    errors = validator.validate(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    plan = []
    for version in data["versions"]:
        if not (version["generated_reference_enabled"] or version["webvowl_enabled"]):
            continue
        resolved = validator.resolve(data, version["id"])
        plan.append({
            "version_id": resolved["id"],
            "lifecycle_state": resolved["lifecycle_state"],
            "semantic_source_ref": resolved["semantic_source_ref"],
            "semantic_source_paths": resolved["semantic_source_paths"],
            "output_path": resolved["output_path"],
            "generate_reference": resolved["generated_reference_enabled"],
            "generate_webvowl": resolved["webvowl_enabled"],
            "publication_status": resolved["public_status_label"],
        })

    print(json.dumps({"pages_build_plan_schema_version": "1.0", "versions": plan}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
