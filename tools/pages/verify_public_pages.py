#!/usr/bin/env python3
"""Verify the deployed Pages surface and both interactive WebVOWL routes."""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import urlopen

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = json.loads((ROOT / "docs/documentation/ontology-version-registry.json").read_text())


def fetch(url: str, attempts: int = 8) -> bytes:
    for attempt in range(attempts):
        try:
            with urlopen(url, timeout=25) as response:
                if response.status != 200:
                    raise RuntimeError(f"HTTP {response.status}: {url}")
                return response.read()
        except (HTTPError, URLError, TimeoutError):
            if attempt == attempts - 1:
                raise
            time.sleep(min(5 * (attempt + 1), 20))
    raise AssertionError("unreachable")


def verify(base: str) -> dict:
    base = base.rstrip("/") + "/"
    assert b"CM-PharmE" in fetch(base), "portal entry missing"
    results = []
    errors = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        for version in REGISTRY["versions"]:
            route = version.get("immutable_version_path") or version.get("current_path")
            route = route.strip("/") + "/"
            root = urljoin(base, route)
            explore = urljoin(root, "explore/")
            manifest = json.loads(fetch(urljoin(explore, "explorer-manifest.json")))
            data = fetch(urljoin(explore, "webvowl/data/cmpe.json"))
            assert manifest["version_id"] == version["id"]
            assert manifest["semantic_source_ref"] == version["semantic_source_ref"]
            assert hashlib.sha256(data).hexdigest() == manifest["vowl_json_sha256"]
            assert manifest["bundled_dataset_count"] == 1
            assert b"Generated reference projection" in fetch(urljoin(root, "reference/"))
            assert b"download-manifest" in fetch(urljoin(root, "downloads/"))

            context = browser.new_context(viewport={"width": 1440, "height": 900})
            page = context.new_page()
            page.on("pageerror", lambda err, version=version: errors.append(f"{version['id']}: pageerror: {err}"))
            page.on("console", lambda msg, version=version: errors.append(f"{version['id']}: console: {msg.text}") if msg.type == "error" else None)
            page.on("requestfailed", lambda req, version=version: errors.append(f"{version['id']}: request failed: {req.url}"))
            response = page.goto(explore, wait_until="domcontentloaded", timeout=60000)
            assert response and response.status == 200, explore
            assert version["semantic_source_ref"] in page.locator("body").inner_text()
            assert page.get_by_role("link", name="Formal reference").count() >= 1
            frame = page.frame_locator("iframe.explorer-frame")
            frame.locator("#graph svg .nodeContainer .node").first.wait_for(timeout=90000)
            node_count = frame.locator("#graph svg .nodeContainer .node").count()
            assert node_count > 0, f"{version['id']}: graph contains no nodes"
            search = frame.locator("#search-input-text")
            search.fill("a")
            frame.locator("#m_search li").first.wait_for(timeout=10000)
            search_results = frame.locator("#m_search li").count()
            zoom = frame.locator("#zoomInButton")
            zoom.dispatch_event("mousedown")
            page.wait_for_timeout(400)
            zoom.dispatch_event("mouseup")
            assert frame.locator("#graph svg .nodeContainer .node").count() > 0
            page.screenshot(path=f"public-{version['id']}-explore.png", full_page=True)
            results.append({"version": version["id"], "url": explore, "source_ref": version["semantic_source_ref"], "dataset_sha256": manifest["vowl_json_sha256"], "graph_nodes": node_count, "search_results": search_results, "zoom_interaction": "PASS", "screenshot": f"public-{version['id']}-explore.png"})
            context.close()
        browser.close()
    assert results[0]["dataset_sha256"] != results[1]["dataset_sha256"], "version datasets identical"
    assert not errors, "; ".join(errors)
    return {"result": "PASS", "base_url": base, "versions": results, "browser_errors": errors}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = verify(args.base_url)
    except Exception as exc:
        result = {"result": "FAIL", "base_url": args.base_url, "error": repr(exc)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(args.output.read_text())
    raise SystemExit(0 if result["result"] == "PASS" else 1)
