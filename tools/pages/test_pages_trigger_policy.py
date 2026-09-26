#!/usr/bin/env python3
"""Test the source-controlled Pages trigger/cost policy."""
from __future__ import annotations
import fnmatch, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
POLICY=ROOT/"docs/documentation/pages-deployment-policy.json"

def matches(path, pattern):
    # GitHub-style ** patterns approximated for contract tests.
    if pattern.endswith("/**"):
        return path.startswith(pattern[:-3] + "/")
    if "**" in pattern:
        prefix=pattern.split("**",1)[0]
        suffix=pattern.split("**",1)[1]
        return path.startswith(prefix) and path.endswith(suffix.lstrip("*"))
    return fnmatch.fnmatch(path, pattern)

def relevant(path, policy):
    return any(matches(path,p) for p in policy["relevant_main_paths"])

def main():
    p=json.loads(POLICY.read_text())
    required_relevant=[
      "ontology/source/modules/00-ontology.ttl",
      "ontology/validation/validation-report.json",
      "tools/ontology/build.py",
      "docs/documentation/ontology-version-registry.json",
      "docs/documentation/widoco-adapter.json",
      "pages-src/site.css",
      "tools/pages/build_shell.py",
      ".github/workflows/pages-deploy.yml",
      "CHANGELOG.md",
    ]
    required_irrelevant=[
      "README.md",
      "LICENSE",
      "wiki-src/pages/Reader-Journey.md",
      ".github/ISSUE_TEMPLATE/bug.md",
    ]
    for path in required_relevant:
        assert relevant(path,p), f"expected relevant: {path}"
    for path in required_irrelevant:
        assert not relevant(path,p), f"expected cheap/irrelevant: {path}"

    bridge=p["v2_trigger_bridge"]
    assert bridge["workflow_name"]=="CM-PharmE 2.0 Formal Ontology CI"
    assert "equals the V2 exact source SHA" in bridge["rule"]
    guards=p["deployment_guards"]
    assert guards["manual_dispatch_only_until_public_enablement"] is (not p["public_deploy_enabled"])
    assert guards["build_job_separate_from_deploy_job"] is True
    assert isinstance(p["public_deploy_enabled"], bool)

    print(f"PASS: {len(required_relevant)} relevant paths trigger; {len(required_irrelevant)} unrelated examples stay on cheap/no Pages path; V2 bridge and deployment guards are explicit.")

if __name__=="__main__":
    main()
