#!/usr/bin/env python3
"""Execute SHACL validation and compare the bounded findings with registered expectations."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from pyshacl import validate
from rdflib import Graph, RDF
from rdflib.namespace import SH

ROOT = Path(__file__).resolve().parents[2]


def resolve(path: str) -> Path:
    p = Path(path)
    return p if p.is_absolute() else ROOT / p


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ontology", required=True)
    parser.add_argument("--data", default="evaluation/samples/vaccine-distribution.ttl")
    parser.add_argument("--shapes", required=True)
    parser.add_argument("--expectations", default="evaluation/assertions/shacl-expectations.json")
    parser.add_argument("--summary", required=True)
    parser.add_argument("--report-ttl", required=True)
    parser.add_argument("--report-text", required=True)
    args = parser.parse_args()

    ontology = resolve(args.ontology)
    data = resolve(args.data)
    shapes = resolve(args.shapes)
    expectations = json.loads(resolve(args.expectations).read_text(encoding="utf-8"))

    conforms, report_graph, report_text = validate(
        data_graph=str(data),
        shacl_graph=str(shapes),
        ont_graph=str(ontology),
        inference="none",
        abort_on_first=False,
        allow_infos=False,
        allow_warnings=False,
        meta_shacl=True,
        advanced=False,
        debug=False,
    )

    results = list(report_graph.subjects(RDF.type, SH.ValidationResult))
    severity_counts = Counter()
    details = []
    for result in results:
        severity = report_graph.value(result, SH.resultSeverity)
        severity_name = str(severity).rsplit("#", 1)[-1] if severity else "Unknown"
        severity_counts[severity_name] += 1
        details.append(
            {
                "severity": severity_name,
                "focus_node": str(report_graph.value(result, SH.focusNode) or ""),
                "source_shape": str(report_graph.value(result, SH.sourceShape) or ""),
                "result_path": str(report_graph.value(result, SH.resultPath) or ""),
                "message": str(report_graph.value(result, SH.resultMessage) or ""),
            }
        )

    checks = {
        "conforms_matches_expected": bool(conforms) == bool(expectations["expected_conforms"]),
        "result_count_matches_expected": len(results) == int(expectations["expected_result_count"]),
        "severity_counts_match_expected": dict(sorted(severity_counts.items()))
        == dict(sorted(expectations["expected_severity_counts"].items())),
    }
    summary = {
        "schema_version": 1,
        "profile": expectations["profile"],
        "execution_status": "PASS" if all(checks.values()) else "FAIL",
        "data_conforms": bool(conforms),
        "result_count": len(results),
        "severity_counts": dict(sorted(severity_counts.items())),
        "checks": checks,
        "results": sorted(details, key=lambda item: (item["severity"], item["focus_node"], item["source_shape"])),
        "boundary": expectations["boundary"],
    }

    summary_path = resolve(args.summary)
    ttl_path = resolve(args.report_ttl)
    text_path = resolve(args.report_text)
    for path in (summary_path, ttl_path, text_path):
        path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    ttl_path.write_text(report_graph.serialize(format="turtle"), encoding="utf-8")
    text_path.write_text(report_text, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if summary["execution_status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
