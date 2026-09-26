#!/usr/bin/env python3
"""Audit the final Wiki ↔ Pages ↔ semantic-source navigation contract."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = json.loads((ROOT / "docs/documentation/ontology-version-registry.json").read_text())
SITE = ROOT / "build/site"
PAGES_BASE = "https://arazsaiearasi3.github.io/CM-PharmE"
WIKI_BASE = "https://github.com/ArazSaieArasi3/CM-PharmE/wiki"

REQUIRED_WIKI_PAGES = {
    "Ontology-and-Conceptual-Model-Guide.md",
    "V1-Formal-Ontology.md",
    "V2-Formal-Ontology-and-SHACL.md",
    "V2-Ontology-Diagram-Suite.md",
    "V2-Ontology-Reference.md",
    "Citation-and-Reuse.md",
    "Reference-Guide.md",
}


def route_for(version: dict) -> str:
    return (version.get("immutable_version_path") or version.get("current_path")).strip("/")


def read(path: Path) -> str:
    assert path.is_file(), f"missing: {path}"
    return path.read_text(encoding="utf-8", errors="replace")


def main() -> int:
    wiki_dir = ROOT / "wiki-src/pages"
    for name in REQUIRED_WIKI_PAGES:
        assert (wiki_dir / name).is_file(), f"missing governed Wiki page: {name}"

    guide = read(wiki_dir / "Ontology-and-Conceptual-Model-Guide.md")
    diagram = read(wiki_dir / "V2-Ontology-Diagram-Suite.md")
    assert "Choose the right ontology surface" in guide
    assert "Curated diagrams versus interactive exploration" in diagram

    evidence = {"result": "PASS", "versions": []}
    for version in REGISTRY["versions"]:
        vid = version["id"]
        route = route_for(version)
        wiki_slug = version["wiki_explanation_path"]
        wiki_url = f"{WIKI_BASE}/{wiki_slug}"
        _, sha = version["semantic_source_ref"].rsplit("@", 1)
        source_url = f"https://github.com/ArazSaieArasi3/CM-PharmE/tree/{sha}"
        root = SITE / route

        wiki_source = read(wiki_dir / f"{wiki_slug}.md")
        assert f"{PAGES_BASE}/{route}/reference/" in wiki_source
        assert f"{PAGES_BASE}/{route}/explore/" in wiki_source
        assert sha in wiki_source

        overview = read(root / "index.html")
        explore = read(root / "explore/index.html")
        reference = read(root / "reference/index.html")

        for rendered in (overview, explore, reference):
            assert wiki_url in rendered, f"{vid}: missing version-specific Wiki return link"
            assert sha in rendered, f"{vid}: missing exact semantic source ref"

        assert "Read curated" in explore
        assert "Exact semantic source" in explore
        assert "Explore interactively" in reference
        assert "View exact" in reference
        assert f"{PAGES_BASE}/{route}/" in reference

        other = [x for x in REGISTRY["versions"] if x["id"] != vid]
        for foreign in other:
            _, foreign_sha = foreign["semantic_source_ref"].rsplit("@", 1)
            assert foreign_sha not in overview, f"{vid}: foreign source leaked into version overview"
            assert foreign["wiki_explanation_path"] not in explore, f"{vid}: foreign Wiki explanation leaked into explorer"

        evidence["versions"].append({
            "id": vid,
            "route": f"/{route}/",
            "wiki": wiki_url,
            "semantic_source_ref": version["semantic_source_ref"],
            "reader_journey": "Wiki → version overview/reference/explore → exact source; Pages → curated Wiki/source",
        })

    out = ROOT / "build/evidence/pages-274-cross-surface-navigation.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    print(out.read_text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
