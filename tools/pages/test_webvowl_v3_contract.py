#!/usr/bin/env python3
"""Exercise a hypothetical V3 explorer without publishing fictional content."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
from pathlib import Path

import build_shell
import build_webvowl_explorer as explorer


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def run_builder(args: list[str]) -> int:
    previous = sys.argv
    try:
        sys.argv = ["build_webvowl_explorer.py", *args]
        return explorer.main()
    finally:
        sys.argv = previous


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        registry = copy.deepcopy(explorer.load(explorer.REGISTRY))
        config = copy.deepcopy(explorer.load(explorer.CONFIG))
        v3 = copy.deepcopy(registry["versions"][-1])
        v3.update(id="v3", reader_label="Synthetic V3 test only",
                  semantic_source_ref="test@" + "a" * 40,
                  immutable_version_path="ontology/v3.0.0/", current_path=None)
        registry["versions"].append(v3)
        frontend = root / "frontend"
        (frontend / "js").mkdir(parents=True)
        (frontend / "css").mkdir(parents=True)
        (frontend / "index.html").write_text("<html><head></head><body></body></html>")
        (frontend / "js/webvowl.js").write_text("test")
        (frontend / "js/webvowl.app.js").write_text("test")
        (frontend / "css/webvowl.app.css").write_text("@import url(http://fonts.googleapis.com/css?family=Open+Sans);body{font-family:sans-serif}")
        data = root / "synthetic.json"
        write_json(data, {"class": [{"id": "synthetic"}], "property": []})
        ontology = root / "synthetic.ttl"
        ontology.write_text("# synthetic test input; never published\n")
        config["versions"]["v3"] = {
            "semantic_source_ref": v3["semantic_source_ref"],
            "target_subpath": "ontology/v3.0.0/explore/",
            "vowl_data_filename": "cmpe.json",
            "expected_vowl_json_sha256": explorer.sha256_file(data),
            "expected_vowl_projection_counts": {"classes": 1, "properties": 0},
        }
        config["webvowl"]["expected_frontend_tree_sha256"] = explorer.tree_digest(frontend)
        registry_path, config_path = root / "registry.json", root / "adapter.json"
        write_json(registry_path, registry)
        write_json(config_path, config)
        old_registry, old_config = explorer.REGISTRY, explorer.CONFIG
        explorer.REGISTRY, explorer.CONFIG = registry_path, config_path
        try:
            args = ["--version", "v3", "--frontend-root", str(frontend),
                    "--vowl-json", str(data), "--ontology-input", str(ontology),
                    "--source-ref", v3["semantic_source_ref"], "--output-root", str(root / "site")]
            assert run_builder(args) == 0, "V3 onboarding failed"
            manifest = explorer.load(root / "site/ontology/v3.0.0/explore/explorer-manifest.json")
            assert manifest["version_id"] == "v3"
            assert manifest["vowl_json_sha256"] == explorer.sha256_file(data)
            assert "http://fonts.googleapis.com" not in (root / "site/ontology/v3.0.0/explore/webvowl/css/webvowl.app.css").read_text()
            assert run_builder(args) == 6, "existing route was silently overwritten"
            assert run_builder(args[:args.index("--source-ref") + 1] + ["wrong@ref"] + args[args.index("--output-root"):]) == 3
            assert len(build_shell.validate_routes(registry)) > 0
            collision = copy.deepcopy(registry)
            collision["versions"][-1]["immutable_version_path"] = registry["versions"][0]["immutable_version_path"]
            try:
                build_shell.validate_routes(collision)
            except ValueError:
                pass
            else:
                raise AssertionError("route collision was accepted")
        finally:
            explorer.REGISTRY, explorer.CONFIG = old_registry, old_config
    print("PASS: synthetic V3 onboarding, source binding, overwrite and route collision guards")


if __name__ == "__main__":
    main()
