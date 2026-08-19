#!/usr/bin/env python3
"""Execute frozen W7-E4 competency questions against ontology/KG artifacts."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from rdflib import Graph


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--registry", required=True)
    p.add_argument("--kg", required=True)
    p.add_argument("--ontology", required=True)
    p.add_argument("--output-json", required=True)
    p.add_argument("--output-md", required=True)
    return p.parse_args()


def load_graph(path: str) -> Graph:
    return Graph().parse(path)


def execute_one(cq: dict[str, Any], graphs: dict[str, Graph]) -> dict[str, Any]:
    graph_name = cq["graph"]
    g = graphs[graph_name]
    result = g.query(cq["sparql"])
    expected = cq["expected"]
    qtype = cq["query_type"].upper()

    if qtype == "ASK":
        actual = bool(getattr(result, "askAnswer", bool(result)))
        passed = actual == bool(expected["boolean"])
        actual_payload = {"boolean": actual}
    elif qtype == "SELECT":
        rows = list(result)
        actual_count = len(rows)
        passed = actual_count == int(expected["row_count"])
        sample = []
        for row in rows[:5]:
            sample.append([None if v is None else str(v) for v in row])
        actual_payload = {"row_count": actual_count, "sample_rows": sample}
    else:
        raise ValueError(f"Unsupported query type: {qtype}")

    return {
        "id": cq["id"],
        "polarity": cq["polarity"],
        "question": cq["question"],
        "graph": graph_name,
        "query_type": qtype,
        "expected": expected,
        "actual": actual_payload,
        "status": "PASS" if passed else "FAIL",
    }


def main():
    a = parse_args()
    registry = json.loads(Path(a.registry).read_text(encoding="utf-8"))
    if registry.get("status") != "FROZEN_BEFORE_FIRST_EXECUTION":
        raise SystemExit("CQ registry is not marked as frozen before execution")
    if registry.get("held_out_used") is not False:
        raise SystemExit("W7-E4 registry must not use held-out sources")

    graphs = {
        "kg": load_graph(a.kg),
        "ontology": load_graph(a.ontology),
    }

    results = [execute_one(cq, graphs) for cq in registry["competency_questions"]]
    positive = [r for r in results if r["polarity"] == "positive"]
    negative = [r for r in results if r["polarity"] == "negative"]
    failed = [r for r in results if r["status"] != "PASS"]

    report = {
        "family": "W7-E4",
        "registry_status": registry["status"],
        "registry_issue": registry.get("issue"),
        "scope": registry.get("evaluation_scope"),
        "held_out_used": False,
        "total": len(results),
        "passed": len(results) - len(failed),
        "failed": len(failed),
        "positive_total": len(positive),
        "positive_passed": sum(r["status"] == "PASS" for r in positive),
        "negative_total": len(negative),
        "negative_passed": sum(r["status"] == "PASS" for r in negative),
        "status": "PASS" if not failed else "FAIL",
        "negative_cq_interpretation": registry["negative_cq_interpretation"],
        "results": results,
    }

    out_json = Path(a.output_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# CM-PharmE 2.0 — W7-E4 Competency-Question Evaluation",
        "",
        f"**Status:** {report['status']}",
        "",
        f"- Frozen CQs executed: **{report['total']}**",
        f"- Passed: **{report['passed']}/{report['total']}**",
        f"- Positive: **{report['positive_passed']}/{report['positive_total']}**",
        f"- Negative: **{report['negative_passed']}/{report['negative_total']}**",
        "- Held-out H1–H3 used: **false**",
        "",
        "## Results",
        "",
        "| ID | Polarity | Expected | Actual | Status |",
        "|---|---|---|---|---|",
    ]
    for r in results:
        exp = json.dumps(r["expected"], sort_keys=True)
        actual = json.dumps({k: v for k, v in r["actual"].items() if k != "sample_rows"}, sort_keys=True)
        lines.append(f"| {r['id']} | {r['polarity']} | `{exp}` | `{actual}` | **{r['status']}** |")
    lines += [
        "",
        "## Interpretation boundary",
        "",
        registry["negative_cq_interpretation"],
        "",
        "E4 evaluates the frozen Gate-E schema-faithful fixture KG and asserted ontology only. It does not establish global domain completeness, held-out generalizability, real-world data quality, or application effectiveness.",
    ]
    Path(a.output_md).write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({k: report[k] for k in ["family", "status", "total", "passed", "failed", "positive_passed", "negative_passed"]}, indent=2))
    if failed:
        raise SystemExit(f"{len(failed)} frozen competency question(s) failed")


if __name__ == "__main__":
    main()
