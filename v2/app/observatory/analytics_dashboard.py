#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

EXPECTED = ["QREP-01", "QREP-02", "QREP-03", "QREP-04"]


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--report", required=True)
    p.add_argument("--json-out", required=True)
    p.add_argument("--html-out", required=True)
    return p.parse_args()


def main():
    a = parse_args()
    report = json.loads(Path(a.report).read_text(encoding="utf-8"))
    results = report.get("results", [])
    ids = [r.get("id") for r in results]
    if ids != EXPECTED:
        raise SystemExit(f"Unexpected benchmark set/order: {ids!r}")
    if not report.get("passed") or report.get("benchmarks_passed") != 4 or report.get("benchmarks_total") != 4:
        raise SystemExit("Frozen four-pair benchmark gate is not fully passing")

    cards = []
    for r in results:
        if not r.get("passed"):
            raise SystemExit(f"Benchmark {r.get('id')} is not passing")
        cards.append({
            "id": r["id"],
            "purpose": r["purpose"],
            "passed": True,
            "sql_rows": r["sql_rows"],
            "sparql_rows": r["sparql_rows"],
            "provenance_state": "source-backed-fixture",
        })

    out = {
        "schema_version": 1,
        "capability": "C4 Ecosystem analytics",
        "tasks": ["T04", "T05"],
        "analytics_candidate": "AN-08",
        "benchmarks": cards,
        "benchmark_registry": "v2/data/queries/sql-sparql-benchmarks.json",
        "comparison_tool": "tools/v2_data/compare_sql_sparql.py",
        "semantic_source_boundary": "Ontology/RDB/KG mappings remain authoritative; dashboard presentation does not create semantic identity.",
        "interpretation_boundary": report.get("interpretation_boundary"),
        "not_claimed": [
            "arbitrary SQL/SPARQL equivalence",
            "global pharmaceutical-market completeness",
            "production deployment",
            "usability or effectiveness",
            "predictive or causal performance",
            "AI performance or novelty",
        ],
    }
    Path(a.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    rows = "\n".join(
        f"<tr><td>{html.escape(c['id'])}</td><td>{html.escape(c['purpose'])}</td><td>PASS</td><td>{c['sql_rows']}</td><td>{c['sparql_rows']}</td><td>{c['provenance_state']}</td></tr>"
        for c in cards
    )
    page = f"""<!doctype html><html><head><meta charset='utf-8'><title>CM-PharmE V2-080 bounded analytics</title></head><body>
<h1>CM-PharmE V2-080 bounded ecosystem analytics</h1>
<p>Capability C4; tasks T04/T05; admitted analytics candidate AN-08 only.</p>
<table border='1'><thead><tr><th>ID</th><th>Purpose</th><th>State</th><th>SQL rows</th><th>SPARQL rows</th><th>Provenance</th></tr></thead><tbody>{rows}</tbody></table>
<p><strong>Interpretation boundary:</strong> {html.escape(str(out['interpretation_boundary']))}</p>
<p><strong>Semantic boundary:</strong> {html.escape(out['semantic_source_boundary'])}</p>
</body></html>"""
    Path(a.html_out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.html_out).write_text(page, encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
