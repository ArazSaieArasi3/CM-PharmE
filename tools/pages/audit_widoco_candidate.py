#!/usr/bin/env python3
"""Audit WIDOCO candidate coverage and local link/asset integrity."""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from rdflib import Graph
from rdflib.namespace import RDF, OWL

EXTERNAL_SCHEMES = {"http", "https", "mailto", "tel", "data"}
CSS_URL_RE = re.compile(r"url\(([^)]+)\)", re.I)


class DocParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        ident = a.get("id") or a.get("name")
        if ident:
            self.ids.add(ident)
        if "href" in a and a["href"]:
            self.links.append(("href", a["href"]))
        if "src" in a and a["src"]:
            self.links.append(("src", a["src"]))


def load_graph(path: Path) -> Graph:
    g = Graph()
    g.parse(path, format="turtle")
    return g


def inventory(g: Graph) -> dict[str, set[str]]:
    return {
        "classes": {str(s) for s in g.subjects(RDF.type, OWL.Class)},
        "object_properties": {str(s) for s in g.subjects(RDF.type, OWL.ObjectProperty)},
        "datatype_properties": {str(s) for s in g.subjects(RDF.type, OWL.DatatypeProperty)},
    }


def expected_counts(version: str, authority: dict) -> tuple[dict[str, int | None], dict[str, str]]:
    if version == "v1":
        ec = authority["expected_counts"]
        return (
            {
                "classes": int(ec["concept_class_count"]),
                "object_properties": int(ec["relation_object_property_count"]),
                "datatype_properties": None,
            },
            {
                "classes": "ontology/validation/validation-report.json::expected_counts.concept_class_count",
                "object_properties": "ontology/validation/validation-report.json::expected_counts.relation_object_property_count",
                "datatype_properties": "No independently frozen V1 datatype-property count in the authoritative validation report; reconciled directly against the governed exact-ref ontology input and WIDOCO HTML.",
            },
        )
    if version == "v2":
        return (
            {
                "classes": int(authority["expected_owl_classes"]),
                "object_properties": int(authority["expected_object_properties"]),
                "datatype_properties": int(authority["expected_datatype_properties"]),
            },
            {
                "classes": "docs/documentation/v2-current-pages-baseline.json::expected_owl_classes",
                "object_properties": "docs/documentation/v2-current-pages-baseline.json::expected_object_properties",
                "datatype_properties": "docs/documentation/v2-current-pages-baseline.json::expected_datatype_properties",
            },
        )
    raise ValueError(f"unsupported version {version}")


def html_documents(root: Path) -> dict[Path, DocParser]:
    out: dict[Path, DocParser] = {}
    for path in sorted(root.rglob("*.html")):
        parser = DocParser()
        parser.feed(path.read_text(encoding="utf-8", errors="replace"))
        out[path.resolve()] = parser
    return out


def entry_page(root: Path) -> Path:
    for name in ("index-en.html", "index.html"):
        p = root / name
        if p.is_file():
            return p
    raise FileNotFoundError(f"no WIDOCO entry page under {root}")


def local_target(root: Path, source: Path, raw: str) -> tuple[Path | None, str | None, str | None]:
    value = html.unescape(raw).strip()
    if not value:
        return None, None, None
    parts = urlsplit(value)
    scheme = parts.scheme.lower()
    if scheme in EXTERNAL_SCHEMES or parts.netloc:
        return None, None, None
    if scheme:
        return None, None, f"unsupported local scheme {scheme}: {value}"
    path_part = unquote(parts.path)
    fragment = unquote(parts.fragment) if parts.fragment else None
    if not path_part:
        return source.resolve(), fragment, None
    if path_part.startswith("/"):
        target = (root / path_part.lstrip("/")).resolve()
    else:
        target = (source.parent / path_part).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        return None, None, f"path escapes candidate root: {value}"
    if target.is_dir():
        if (target / "index-en.html").exists():
            target = target / "index-en.html"
        elif (target / "index.html").exists():
            target = target / "index.html"
    return target, fragment, None


def audit_links(root: Path) -> tuple[list[dict], list[dict]]:
    root = root.resolve()
    docs = html_documents(root)
    broken: list[dict] = []
    checked: list[dict] = []
    for source, parser in docs.items():
        for attr, raw in parser.links:
            if raw.lower().startswith("javascript:"):
                broken.append({"source": str(source.relative_to(root.resolve())), "target": raw, "reason": "javascript URI prohibited"})
                continue
            target, fragment, error = local_target(root, source, raw)
            if error:
                broken.append({"source": str(source.relative_to(root.resolve())), "target": raw, "reason": error})
                continue
            if target is None:
                continue
            checked.append({"source": str(source.relative_to(root.resolve())), "target": raw})
            if not target.exists():
                broken.append({"source": str(source.relative_to(root.resolve())), "target": raw, "reason": "missing local target"})
                continue
            if fragment and target.suffix.lower() in {".html", ".htm"}:
                tparser = docs.get(target.resolve())
                if tparser is None:
                    tparser = DocParser()
                    tparser.feed(target.read_text(encoding="utf-8", errors="replace"))
                    docs[target.resolve()] = tparser
                if fragment not in tparser.ids:
                    broken.append({"source": str(source.relative_to(root.resolve())), "target": raw, "reason": f"missing fragment #{fragment}"})

    # CSS asset references.
    for css in sorted(root.rglob("*.css")):
        text = css.read_text(encoding="utf-8", errors="replace")
        for match in CSS_URL_RE.finditer(text):
            raw = match.group(1).strip().strip("'\"")
            if not raw or raw.startswith("data:"):
                continue
            parts = urlsplit(raw)
            if parts.scheme in EXTERNAL_SCHEMES or parts.netloc:
                continue
            target = (css.parent / unquote(parts.path)).resolve()
            try:
                target.relative_to(root.resolve())
            except ValueError:
                broken.append({"source": str(css.relative_to(root.resolve())), "target": raw, "reason": "CSS asset escapes candidate root"})
                continue
            checked.append({"source": str(css.relative_to(root.resolve())), "target": raw})
            if not target.exists():
                broken.append({"source": str(css.relative_to(root.resolve())), "target": raw, "reason": "missing CSS asset"})
    return checked, broken


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--version", choices=["v1", "v2"], required=True)
    p.add_argument("--ontology", type=Path, required=True)
    p.add_argument("--candidate", type=Path, required=True)
    p.add_argument("--authority", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()

    g = load_graph(args.ontology)
    inv = inventory(g)
    authority = json.loads(args.authority.read_text(encoding="utf-8"))
    expected, sources = expected_counts(args.version, authority)

    count_checks = {}
    count_failures = []
    for kind, entities in inv.items():
        actual = len(entities)
        exp = expected[kind]
        status = "PASS"
        if exp is not None and actual != exp:
            status = "FAIL"
            count_failures.append(f"{kind}: actual {actual} != expected {exp}")
        elif exp is None:
            status = "PASS_WITH_DOCUMENTED_NON_FROZEN_COUNT"
        count_checks[kind] = {
            "actual_governed_input_count": actual,
            "expected_authoritative_count": exp,
            "authority": sources[kind],
            "status": status,
        }

    entry = entry_page(args.candidate)
    html_text = html.unescape(entry.read_text(encoding="utf-8", errors="replace"))
    coverage = {}
    missing_all = []
    for kind, entities in inv.items():
        missing = sorted(iri for iri in entities if iri not in html_text)
        coverage[kind] = {
            "governed_input_entities": len(entities),
            "represented_in_generated_entry": len(entities) - len(missing),
            "missing_count": len(missing),
            "missing_iris": missing,
            "status": "PASS" if not missing else "FAIL",
        }
        missing_all.extend((kind, iri) for iri in missing)

    checked, broken = audit_links(args.candidate)

    report = {
        "schema_version": 1,
        "version_id": args.version,
        "ontology_input": str(args.ontology),
        "candidate_root": str(args.candidate),
        "entry_page": str(entry.relative_to(args.candidate)),
        "inventory_reconciliation": count_checks,
        "generated_reference_coverage": coverage,
        "link_asset_audit": {
            "html_file_count": len(list(args.candidate.rglob("*.html"))),
            "local_targets_checked": len(checked),
            "broken_target_count": len(broken),
            "broken_targets": broken,
            "status": "PASS" if not broken else "FAIL",
        },
        "overall": "PASS" if not count_failures and not missing_all and not broken else "FAIL",
        "notes": [
            "V1 datatype-property count is not promoted to a frozen authority when the exact-ref V1 validation report does not independently declare one.",
            "Coverage means every governed OWL class/object-property/datatype-property IRI is present in the generated WIDOCO entry page.",
            "External HTTP(S) links are out of scope for this local candidate integrity audit; public rendered external-link checks belong to #275.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(args.output.read_text(encoding="utf-8"))

    if report["overall"] != "PASS":
        if count_failures:
            print("COUNT FAILURES:", *count_failures, sep="\n- ", file=sys.stderr)
        if missing_all:
            print(f"ERROR: {len(missing_all)} governed entities absent from generated entry", file=sys.stderr)
        if broken:
            print(f"ERROR: {len(broken)} broken local link/assets", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
