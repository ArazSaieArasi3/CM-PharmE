#!/usr/bin/env python3
"""Negative and future-version tests for the Pages version registry."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "docs/documentation/ontology-version-registry.json"
VALIDATOR_PATH = ROOT / "tools/pages/validate_version_registry.py"

spec = importlib.util.spec_from_file_location("registry_validator", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)

with REGISTRY_PATH.open("r", encoding="utf-8") as handle:
    BASE = json.load(handle)


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


# 1) Baseline registry must pass.
check(not validator.validate(BASE), "baseline registry must validate")

# 2) Hypothetical V3 dry-run: registry-driven, unpublished, common pipeline.
v3_registry = copy.deepcopy(BASE)
v3_registry["versions"].append({
    "id": "v3",
    "version_family": "CM-PharmE 3.x",
    "reader_label": "CM-PharmE 3.x dry-run",
    "lifecycle_state": "evolving",
    "semantic_source_ref": "dry-run-only@" + ("3" * 40),
    "semantic_source_paths": ["dry-run/not-published/ontology/source/modules/"],
    "assembly_rule": "Dry-run only: use the common deterministic assembly contract; do not publish scientific content.",
    "documentation_input": {
        "kind": "deterministic_assembled_ontology",
        "source_family": "dry-run/not-published/ontology/source/modules/",
        "build_contract_issue": 269,
        "resolved_artifact": None,
        "fingerprint": None
    },
    "generated_reference_enabled": False,
    "webvowl_enabled": False,
    "immutable_version_path": None,
    "current_path": "ontology/v3/current/",
    "documentation_baseline_binding": None,
    "citation_status": "dry_run_not_publishable",
    "supersedes": "v2",
    "superseded_by": None,
    "public_status_label": "DRY RUN ONLY — no scientific content may be published."
})
check(not validator.validate(v3_registry), "hypothetical V3 entry should validate without workflow duplication")
resolved_v3 = validator.resolve(v3_registry, "v3")
check(resolved_v3["output_path"] == "ontology/v3/current/", "V3 route must be registry-derived")

# 3) Route collision must fail.
collision = copy.deepcopy(v3_registry)
collision["versions"][-1]["current_path"] = "ontology/v2/current/"
collision_errors = validator.validate(collision)
check(any("route collision" in e for e in collision_errors), "route collision must be rejected")

# 4) Silent overwrite/change of stable V1 immutable route must fail against baseline.
changed_path = copy.deepcopy(BASE)
changed_path["versions"][0]["immutable_version_path"] = "ontology/v1.0.0-rewritten/"
path_errors = validator.validate_against_baseline(changed_path, BASE)
check(any("immutable immutable_version_path changed" in e for e in path_errors),
      "stable V1 path mutation must be rejected")

# 5) Silent rebinding of stable V1 exact source ref must fail against baseline.
changed_ref = copy.deepcopy(BASE)
changed_ref["versions"][0]["semantic_source_ref"] = "main@" + ("9" * 40)
ref_errors = validator.validate_against_baseline(changed_ref, BASE)
check(any("immutable semantic_source_ref changed" in e for e in ref_errors),
      "stable V1 source ref mutation must be rejected")

# 6) Removing stable V1 must fail.
removed = copy.deepcopy(BASE)
removed["versions"] = [v for v in removed["versions"] if v["id"] != "v1"]
remove_errors = validator.validate_against_baseline(removed, BASE)
check(any("cannot be removed" in e for e in remove_errors), "stable V1 removal must be rejected")

print("PASS: baseline + V3 dry-run + collision guard + immutable V1 path/ref/removal guards.")
