#!/usr/bin/env python3
"""Render the bounded W8 C5 resilience/risk view from frozen W7-E12 evidence.

This consumer never mutates ontology semantics. It re-runs the frozen E12 evaluator,
checks the frozen scenario contract, then emits deterministic JSON and HTML views for
article-scope task T06.
"""
from __future__ import annotations

import argparse
import html
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
E12 = ROOT / "tools/v2_evaluation/e12_resilience_scenarios.py"
REGISTRY = ROOT / "v2/evaluation/protocol/e12-resilience-scenario-registry.json"
SCENARIOS = ROOT / "v2/evaluation/protocol/e12-resilience-scenarios.ttl"

EXPECTED_IDS = ["RES-01", "RES-02", "RES-03", "RES-04", "RES-05"]
RETAINED_GAPS = [
    "Recovery semantics: no explicit RecoveryEvent/RecoveredState semantic element.",
    "Risk-treatment linkage: no explicit RiskTreatmentPlan→RiskTreatmentActivity property.",
    "Vulnerability grounding: no explicit bearer/domain property for Vulnerability.",
]
CLAIM_BOUNDARY = (
    "Scenario-level representational adequacy only. This view does not establish "
    "prediction accuracy, causal validity, intervention effectiveness, stockout prevention, "
    "recovery performance, operational resilience, complete real-world supply-chain "
    "reconstruction, or validated risk scoring."
)


def run_e12(tmp: Path) -> dict:
    out = tmp / "e12.json"
    summary = tmp / "e12.md"
    cmd = [
        sys.executable,
        str(E12),
        "--registry",
        str(REGISTRY),
        "--scenarios",
        str(SCENARIOS),
        "--output",
        str(out),
        "--summary",
        str(summary),
    ]
    subprocess.run(cmd, cwd=ROOT, check=True)
    return json.loads(out.read_text(encoding="utf-8"))


def build_view(e12: dict) -> dict:
    results = e12.get("scenario_results", [])
    ids = [row.get("id") for row in results]
    if ids != EXPECTED_IDS:
        raise ValueError(f"Frozen scenario order/identity drift: expected {EXPECTED_IDS}, got {ids}")
    if e12.get("scenario_count") != 5:
        raise ValueError("W8 C5 is frozen to exactly five E12 scenarios")
    if e12.get("scenario_queries_matching_frozen_expectations") != 5:
        raise ValueError("Not all frozen E12 query expectations reproduced")
    if e12.get("scenario_provenance_complete") != 5:
        raise ValueError("Not all frozen E12 provenance checks reproduced")
    sensitivity = e12.get("missing_evidence_sensitivity", {})
    if sensitivity.get("interpretation") != "INSUFFICIENT_EVIDENCE_NOT_RESILIENCE":
        raise ValueError("RES-05 evidence-insufficiency interpretation drifted")

    rows = []
    for row in results:
        sid = row["id"]
        limitation_flags = []
        if row.get("expected_representability") == "PARTIAL":
            limitation_flags.append("PARTIAL_REPRESENTABILITY")
        if row.get("expected_gap"):
            limitation_flags.append("RETAINED_EXTENSION_GAP")
        if sid == "RES-05":
            limitation_flags.append("OPEN_WORLD_EVIDENCE_SENSITIVITY")
        rows.append(
            {
                "scenario_id": sid,
                "expected_representability": row.get("expected_representability"),
                "observed_query_result": row.get("baseline_query_result"),
                "matches_frozen_expectation": row.get("query_matches_frozen_expectation"),
                "provenance_complete": row.get("provenance_complete"),
                "expected_gap": row.get("expected_gap"),
                "limitation_flags": limitation_flags,
            }
        )

    return {
        "schema_version": 1,
        "capability": "W8-C5 Resilience and Risk View",
        "representative_task": "T06",
        "source_family": "W7-E12",
        "scenario_count": 5,
        "all_queries_reproduced": True,
        "all_provenance_reproduced": True,
        "missing_evidence_sensitivity": sensitivity,
        "retained_extension_gaps": RETAINED_GAPS,
        "ontology_goalpost_changes": 0,
        "claim_boundary": CLAIM_BOUNDARY,
        "scenarios": rows,
    }


def render_html(view: dict) -> str:
    rows = []
    for s in view["scenarios"]:
        flags = ", ".join(s["limitation_flags"]) or "—"
        gap = s["expected_gap"] or "—"
        rows.append(
            "<tr>"
            f"<td>{html.escape(s['scenario_id'])}</td>"
            f"<td>{html.escape(str(s['expected_representability']))}</td>"
            f"<td>{html.escape(str(s['observed_query_result']))}</td>"
            f"<td>{'PASS' if s['matches_frozen_expectation'] else 'FAIL'}</td>"
            f"<td>{'PASS' if s['provenance_complete'] else 'FAIL'}</td>"
            f"<td>{html.escape(flags)}</td>"
            f"<td>{html.escape(gap)}</td>"
            "</tr>"
        )
    sensitivity = view["missing_evidence_sensitivity"]
    gap_items = "".join(f"<li>{html.escape(g)}</li>" for g in view["retained_extension_gaps"])
    return f"""<!doctype html>
<html lang=\"en\"><head><meta charset=\"utf-8\"><title>CM-PharmE V2 W8 C5</title>
<style>body{{font-family:system-ui,sans-serif;max-width:1200px;margin:2rem auto;padding:0 1rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #bbb;padding:.5rem;vertical-align:top}}th{{text-align:left}}.boundary{{border-left:4px solid #777;padding-left:1rem}}</style></head>
<body><h1>CM-PharmE 2.0 — Bounded Resilience and Risk View</h1>
<p><strong>Representative task:</strong> T06. <strong>Evidence family:</strong> W7-E12.</p>
<table><thead><tr><th>Scenario</th><th>Frozen representability</th><th>Observed query</th><th>Expectation</th><th>Provenance</th><th>Limitation flags</th><th>Retained gap</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
<h2>Missing-evidence sensitivity</h2><p>Baseline: <strong>{sensitivity.get('baseline_exposure_query')}</strong>; after provider-edge removal: <strong>{sensitivity.get('after_dependency_provider_removed')}</strong>; interpretation: <strong>{html.escape(str(sensitivity.get('interpretation')))}</strong>.</p>
<h2>Retained extension gaps</h2><ul>{gap_items}</ul>
<h2>Claim boundary</h2><p class=\"boundary\">{html.escape(view['claim_boundary'])}</p>
<p><strong>Ontology goal-post changes made for this view:</strong> 0.</p></body></html>"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--html-output", required=True)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="cmpe-w8-c5-") as td:
        e12 = run_e12(Path(td))
    view = build_view(e12)
    json_path = ROOT / args.json_output
    html_path = ROOT / args.html_output
    json_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(view, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    html_path.write_text(render_html(view), encoding="utf-8")
    print(f"W8 C5 PASS: {view['scenario_count']}/5 frozen scenarios reproduced with provenance; retained gaps remain visible.")


if __name__ == "__main__":
    main()
