#!/usr/bin/env python3
"""Build the registry-driven static GitHub Pages shell for CM-PharmE."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY = ROOT / "docs/documentation/ontology-version-registry.json"
DEFAULT_CSS = ROOT / "pages-src/site.css"

REPO_URL = "https://github.com/ArazSaieArasi3/CM-PharmE"
WIKI_URL = REPO_URL + "/wiki"

VERSION_SUBROUTES = (
    ("reference", "Formal reference", "Generated formal ontology reference will be populated by PAGES-04 / #271."),
    ("explore", "Interactive exploration", "Interactive WebVOWL exploration will be populated by PAGES-05 / #272."),
    ("downloads", "Downloads & serializations", "Version-bound serializations and downloads will be populated by PAGES-06 / #273."),
    ("provenance", "Provenance & build metadata", "Build provenance and traceability will be populated by PAGES-06 / #273."),
    ("history", "Version history", "Version-specific change history and lifecycle context."),
    ("citation", "Citation guidance", "Citation status and links to the curated research Wiki."),
)


def read_registry(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def route_for(version: dict) -> str:
    route = version.get("immutable_version_path") or version.get("current_path")
    if not route:
        raise ValueError(f"{version.get('id')}: no public route")
    route = route.strip("/")
    if not route.startswith("ontology/"):
        raise ValueError(f"{version.get('id')}: route must be under ontology/: {route}")
    return route


def validate_routes(registry: dict) -> dict[str, str]:
    routes: dict[str, str] = {}
    for version in registry["versions"]:
        route = route_for(version)
        if route in routes:
            raise ValueError(f"route collision: {route} used by {routes[route]} and {version['id']}")
        routes[route] = version["id"]
    return routes


def rel_href(from_file: Path, to_file: Path) -> str:
    return os.path.relpath(to_file, start=from_file.parent).replace(os.sep, "/")


def exact_source_url(version: dict) -> str:
    _, sha = version["semantic_source_ref"].rsplit("@", 1)
    return f"{REPO_URL}/tree/{sha}"


def exact_source_path_url(version: dict, source_path: str) -> str:
    _, sha = version["semantic_source_ref"].rsplit("@", 1)
    clean = source_path.strip("/")
    return f"{REPO_URL}/tree/{sha}/{clean}"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def page(
    *,
    output_root: Path,
    file_path: Path,
    title: str,
    body: str,
    version_root: Path | None = None,
) -> str:
    home = rel_href(file_path, output_root / "index.html")
    chooser = rel_href(file_path, output_root / "ontology/index.html")
    about = rel_href(file_path, output_root / "about/index.html")
    version_link = (
        f'<a href="{esc(rel_href(file_path, version_root / "index.html"))}">Version overview</a>'
        if version_root else ""
    )
    version_sep = " · " if version_link else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="CM-PharmE version-aware generated ontology reference portal.">
  <title>{esc(title)} · CM-PharmE</title>
  <link rel="stylesheet" href="{esc(rel_href(file_path, output_root / "assets/site.css"))}">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to main content</a>
  <header class="site-header">
    <div class="shell">
      <a class="brand" href="{esc(home)}">CM-PharmE</a>
      <nav aria-label="Primary navigation">
        <a href="{esc(chooser)}">Ontology versions</a>
        <a href="{esc(about)}">About</a>
        {version_link}{version_sep}
        <a href="{esc(WIKI_URL)}">Research Wiki</a>
        <a href="{esc(REPO_URL)}">Repository</a>
      </nav>
    </div>
  </header>
  <main id="main-content" class="shell">
    {body}
  </main>
  <footer class="site-footer">
    <div class="shell">
      <p><strong>Authority boundary:</strong> generated Pages content is a projection. Canonical semantic source in the repository remains authoritative.</p>
      <p><a href="{esc(WIKI_URL)}">Research Wiki</a> · <a href="{esc(REPO_URL)}">Repository / semantic source</a></p>
    </div>
  </footer>
</body>
</html>
"""


def write_page(output_root: Path, relative: str, title: str, body: str, version_root: Path | None = None) -> Path:
    path = output_root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(page(output_root=output_root, file_path=path, title=title, body=body, version_root=version_root), encoding="utf-8")
    return path


def lifecycle_badge(version: dict) -> str:
    return f'<span class="badge lifecycle-{esc(version["lifecycle_state"])}">{esc(version["lifecycle_state"].replace("_", " ").title())}</span>'


def path_kind(version: dict) -> str:
    return "Immutable version path" if version.get("immutable_version_path") else "Mutable current path"


def version_card(output_root: Path, from_file: Path, version: dict) -> str:
    route = route_for(version)
    root_file = output_root / route / "index.html"
    return f"""
<article class="version-card">
  <div class="eyebrow">{esc(version["version_family"])}</div>
  <h2><a href="{esc(rel_href(from_file, root_file))}">{esc(version["reader_label"])}</a></h2>
  <p>{lifecycle_badge(version)} <span class="path-kind">{esc(path_kind(version))}</span></p>
  <p>{esc(version["public_status_label"])}</p>
  <p><code>/{esc(route)}/</code></p>
  <p><a href="{esc(rel_href(from_file, root_file))}">Open this version</a></p>
</article>
"""


def build(registry_path: Path, output_root: Path, css_path: Path) -> dict:
    registry = read_registry(registry_path)
    routes = validate_routes(registry)
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "assets").mkdir(parents=True, exist_ok=True)
    (output_root / "assets/site.css").write_text(css_path.read_text(encoding="utf-8"), encoding="utf-8")

    root_file = output_root / "index.html"
    cards = "".join(version_card(output_root, root_file, v) for v in registry["versions"])
    write_page(
        output_root, "index.html", "Home",
        f"""
<section class="hero">
  <p class="eyebrow">Pharmaceutical ecosystem ontology documentation</p>
  <h1>CM-PharmE formal reference portal</h1>
  <p>This public shell separates ontology versions by lifecycle and URL. Use the Research Wiki for rationale, research journey, evaluation interpretation and tutorials; use this portal for generated formal reference and version-bound technical artifacts.</p>
  <p class="authority">Semantic Source defines → Wiki explains → Pages exposes generated/exhaustive reference.</p>
</section>
<section aria-labelledby="versions-heading">
  <h2 id="versions-heading">Choose an ontology version</h2>
  <div class="version-grid">{cards}</div>
</section>
<section>
  <h2>Reader paths</h2>
  <ul>
    <li><a href="{esc(rel_href(root_file, output_root / "ontology/index.html"))}">Choose a version</a></li>
    <li><a href="{esc(WIKI_URL)}">Read the research Wiki</a></li>
    <li><a href="{esc(REPO_URL)}">Inspect canonical semantic source</a></li>
    <li><a href="{esc(rel_href(root_file, output_root / "history/index.html"))}">Review version history</a></li>
    <li><a href="{esc(rel_href(root_file, output_root / "citation/index.html"))}">Citation guidance</a></li>
  </ul>
</section>
"""
    )

    chooser_file = output_root / "ontology/index.html"
    chooser_cards = "".join(version_card(output_root, chooser_file, v) for v in registry["versions"])
    write_page(output_root, "ontology/index.html", "Ontology versions", f"""
<h1>Ontology versions</h1>
<p>Each version family is isolated by route and lifecycle. Stable/frozen paths are immutable; <code>current</code> paths are mutable convenience routes and are not equivalent to scholarly frozen releases.</p>
<div class="version-grid">{chooser_cards}</div>
""")

    write_page(output_root, "about/index.html", "About", """
<h1>About CM-PharmE</h1>
<p>CM-PharmE is documented across three governed surfaces: semantic source, Research Wiki and this generated/static Pages portal.</p>
<h2>Use the right surface</h2>
<ul>
  <li><strong>Semantic Source:</strong> ontology modules, constraints, mappings, evidence and release identities.</li>
  <li><strong>Research Wiki:</strong> rationale, research process, interpretation, diagrams, limitations and tutorials.</li>
  <li><strong>Pages:</strong> generated formal reference, exploration, serializations and build provenance.</li>
</ul>
""")
    write_page(output_root, "history/index.html", "Version history", """
<h1>Version history</h1>
<p>Version families and lifecycle states are generated from the governed ontology version registry. Historical and frozen versions remain discoverable without being presented as current.</p>
""")
    write_page(output_root, "citation/index.html", "Citation guidance", f"""
<h1>Citation guidance</h1>
<p>Do not cite a mutable <code>current</code> route as if it were an immutable semantic release. Use the version-specific citation status and the curated <a href="{esc(WIKI_URL)}">Research Wiki</a> guidance.</p>
""")

    inventory: list[dict] = []
    for version in registry["versions"]:
        route = route_for(version)
        version_root = output_root / route
        version_root.mkdir(parents=True, exist_ok=True)
        root_path = version_root / "index.html"
        source_links = "".join(
            f'<li><a href="{esc(exact_source_path_url(version, p))}">{esc(p)}</a></li>'
            for p in version["semantic_source_paths"]
        )
        subnav = "".join(
            f'<li><a href="{esc(rel_href(root_path, version_root / slug / "index.html"))}">{esc(label)}</a></li>'
            for slug, label, _ in VERSION_SUBROUTES
        )
        write_page(
            output_root,
            f"{route}/index.html",
            version["reader_label"],
            f"""
<p class="eyebrow">{esc(version["version_family"])}</p>
<h1>{esc(version["reader_label"])}</h1>
<p>{lifecycle_badge(version)} <span class="path-kind">{esc(path_kind(version))}</span></p>
<p>{esc(version["public_status_label"])}</p>
<div class="notice"><strong>Generated-reference boundary:</strong> this Pages route is not the semantic authority. Exact repository source remains authoritative.</div>
<dl class="metadata">
  <dt>Route</dt><dd><code>/{esc(route)}/</code></dd>
  <dt>Lifecycle</dt><dd>{esc(version["lifecycle_state"])}</dd>
  <dt>Exact semantic source ref</dt><dd><code>{esc(version["semantic_source_ref"])}</code></dd>
  <dt>Citation status</dt><dd>{esc(version["citation_status"])}</dd>
  <dt>Documentation fingerprint</dt><dd><code>{esc(version["documentation_input"].get("fingerprint") or "pending")}</code></dd>
</dl>
<h2>Reference paths</h2>
<ul>{subnav}</ul>
<h2>Canonical semantic source</h2>
<p><a href="{esc(exact_source_url(version))}">Open exact source commit</a></p>
<ul>{source_links}</ul>
<h2>Research context</h2>
<p><a href="{esc(WIKI_URL)}">Open the curated Research Wiki</a></p>
""",
            version_root=version_root,
        )
        inventory.append({"route": f"/{route}/", "kind": "version_root", "version_id": version["id"]})

        for slug, label, note in VERSION_SUBROUTES:
            subfile = version_root / slug / "index.html"
            write_page(
                output_root,
                f"{route}/{slug}/index.html",
                f"{version['reader_label']} — {label}",
                f"""
<p class="eyebrow">{esc(version["reader_label"])}</p>
<h1>{esc(label)}</h1>
<p>{lifecycle_badge(version)} {esc(version["public_status_label"])}</p>
<div class="notice">{esc(note)}</div>
<p><a class="back-link" href="{esc(rel_href(subfile, root_path))}">Back to version overview</a></p>
<p><a href="{esc(exact_source_url(version))}">Exact semantic source</a> · <a href="{esc(WIKI_URL)}">Research Wiki</a></p>
""",
                version_root=version_root,
            )
            inventory.append({"route": f"/{route}/{slug}/", "kind": slug, "version_id": version["id"]})

    inventory.extend([
        {"route": "/", "kind": "landing", "version_id": None},
        {"route": "/about/", "kind": "about", "version_id": None},
        {"route": "/ontology/", "kind": "version_chooser", "version_id": None},
        {"route": "/history/", "kind": "history", "version_id": None},
        {"route": "/citation/", "kind": "citation", "version_id": None},
    ])
    inventory.sort(key=lambda x: x["route"])
    registry_hash = hashlib.sha256(registry_path.read_bytes()).hexdigest()
    (output_root / "route-inventory.json").write_text(
        json.dumps({
            "schema_version": 1,
            "authority_model": registry["authority_model"],
            "registry_sha256": registry_hash,
            "version_routes": routes,
            "routes": inventory,
        }, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {"versions": len(registry["versions"]), "routes": len(inventory), "registry_sha256": registry_hash}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    p.add_argument("--css", type=Path, default=DEFAULT_CSS)
    p.add_argument("--output", type=Path, default=ROOT / "build/pages-shell")
    args = p.parse_args()
    result = build(args.registry, args.output, args.css)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
