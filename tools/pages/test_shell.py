#!/usr/bin/env python3
"""Acceptance tests for the registry-driven CM-PharmE Pages shell."""
from __future__ import annotations

import copy
import json
import re
import tempfile
from html.parser import HTMLParser
from pathlib import Path

import build_shell

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "docs/documentation/ontology-version-registry.json"
CSS = ROOT / "pages-src/site.css"

REQUIRED_SUBROUTES = {"reference", "explore", "downloads", "provenance", "history", "citation"}
FORBIDDEN_PUBLIC = (
    "password=",
    "api_key",
    "secret=",
    "token=",
    "begin private",
    "private expert response",
)


class AuditParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.has_h1 = False
        self.has_main = False
        self.has_viewport = False
        self.has_primary_nav = False
        self.has_skip = False
        self.has_script = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
            if a["href"] == "#main-content":
                self.has_skip = True
        if tag == "h1":
            self.has_h1 = True
        if tag == "main" and a.get("id") == "main-content":
            self.has_main = True
        if tag == "meta" and a.get("name") == "viewport":
            self.has_viewport = True
        if tag == "nav" and a.get("aria-label") == "Primary navigation":
            self.has_primary_nav = True
        if tag == "script":
            self.has_script = True


def html_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*.html"))


def resolve_internal(page: Path, href: str) -> Path | None:
    if href.startswith(("http://", "https://", "mailto:", "#")):
        return None
    target = (page.parent / href).resolve()
    if href.endswith("/"):
        target /= "index.html"
    return target


def audit_site(site: Path, registry: dict) -> None:
    files = html_files(site)
    assert files, "no HTML generated"
    for page in files:
        text = page.read_text(encoding="utf-8")
        p = AuditParser()
        p.feed(text)
        assert p.has_h1, f"{page}: missing h1"
        assert p.has_main, f"{page}: missing main#main-content"
        assert p.has_viewport, f"{page}: missing viewport"
        assert p.has_primary_nav, f"{page}: missing labelled primary nav"
        assert p.has_skip, f"{page}: missing keyboard skip link"
        assert not p.has_script, f"{page}: JavaScript navigation is prohibited"
        low = text.lower()
        assert not any(x in low for x in FORBIDDEN_PUBLIC), f"{page}: forbidden public marker"
        for href in p.links:
            assert not href.lower().startswith("javascript:"), f"{page}: javascript link"
            target = resolve_internal(page, href)
            if target is not None:
                assert target.exists(), f"{page}: broken internal link {href} -> {target}"

    root_text = (site / "index.html").read_text(encoding="utf-8")
    chooser_text = (site / "ontology/index.html").read_text(encoding="utf-8")
    routes = []
    for version in registry["versions"]:
        route = build_shell.route_for(version)
        routes.append(route)
        vroot = site / route
        assert (vroot / "index.html").is_file(), f"{version['id']}: missing version root"
        assert version["reader_label"] in root_text
        assert version["reader_label"] in chooser_text
        assert version["lifecycle_state"].title() in root_text
        vtext = (vroot / "index.html").read_text(encoding="utf-8")
        assert version["semantic_source_ref"] in vtext
        assert "Research Wiki" in vtext
        assert "Generated-reference boundary" in vtext
        expected_kind = "Immutable version path" if version.get("immutable_version_path") else "Mutable current path"
        assert expected_kind in vtext

        actual_subroutes = {p.parent.name for p in vroot.glob("*/index.html")}
        assert REQUIRED_SUBROUTES <= actual_subroutes, f"{version['id']}: missing required subroutes"
        for slug in REQUIRED_SUBROUTES:
            sub = vroot / slug / "index.html"
            subtext = sub.read_text(encoding="utf-8")
            assert "Back to version overview" in subtext, f"{sub}: stranded reader"

    assert len(routes) == len(set(routes)), "version route collision"
    inventory = json.loads((site / "route-inventory.json").read_text())
    assert inventory["version_routes"] == {build_shell.route_for(v): v["id"] for v in registry["versions"]}


def make_v3(registry: dict) -> dict:
    candidate = copy.deepcopy(registry)
    base = copy.deepcopy(candidate["versions"][-1])
    base.update({
        "id": "v3",
        "version_family": "CM-PharmE 3.x",
        "reader_label": "CM-PharmE 3.x dry-run",
        "lifecycle_state": "evolving",
        "semantic_release": None,
        "semantic_source_ref": "dry-run-only@" + "3" * 40,
        "semantic_source_paths": ["dry-run/not-published/ontology/source/modules/"],
        "generated_reference_enabled": False,
        "webvowl_enabled": False,
        "immutable_version_path": None,
        "current_path": "ontology/v3/current/",
        "documentation_baseline_binding": None,
        "citation_status": "dry_run_not_publishable",
        "supersedes": "v2",
        "superseded_by": None,
        "public_status_label": "DRY RUN ONLY — no scientific content may be published.",
    })
    base["documentation_input"] = {
        "kind": "deterministic_assembled_ontology",
        "source_family": "dry-run/not-published/ontology/source/modules/",
        "build_contract_issue": 269,
        "resolved_artifact": None,
        "fingerprint": None,
    }
    candidate["versions"][-1]["superseded_by"] = "v3"
    candidate["versions"].append(base)
    return candidate


def main() -> int:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "prod"
        build_shell.build(REGISTRY, out, CSS)
        audit_site(out, registry)

        # Future-version simulation: one registry entry, no copied navigation/workflow.
        v3 = make_v3(registry)
        v3_file = Path(td) / "v3-registry.json"
        v3_file.write_text(json.dumps(v3, indent=2) + "\n", encoding="utf-8")
        v3_out = Path(td) / "v3"
        build_shell.build(v3_file, v3_out, CSS)
        audit_site(v3_out, v3)
        assert (v3_out / "ontology/v3/current/index.html").is_file()
        assert "CM-PharmE 3.x dry-run" in (v3_out / "index.html").read_text()

        # Negative route-collision test.
        collision = copy.deepcopy(v3)
        collision["versions"][-1]["current_path"] = build_shell.route_for(collision["versions"][1]) + "/"
        collision_file = Path(td) / "collision.json"
        collision_file.write_text(json.dumps(collision), encoding="utf-8")
        try:
            build_shell.build(collision_file, Path(td) / "collision", CSS)
        except ValueError as exc:
            assert "route collision" in str(exc)
        else:
            raise AssertionError("route collision was not rejected")

    print("PASS: shell routes, accessibility/link audit, V1/V2 walkthrough, V3 simulation and collision guard.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
