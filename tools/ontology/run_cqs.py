#!/usr/bin/env python3
"""Execute CM-PharmE B4 competency questions as a reproducible CI quality gate."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from rdflib import Graph, Literal

ROOT = Path(__file__).resolve().parents[2]


def literal_value(value):
    if isinstance(value, Literal):
        return value.toPython()
    return str(value)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ontology", default="ontology/source/cm-pharme.ttl")
    parser.add_argument("--sample", default="evaluation/samples/vaccine-distribution.ttl")
    parser.add_argument("--queries", default="ontology/queries/competency")
    parser.add_argument("--expectations", default="evaluation/assertions/cq-expectations.json")
    parser.add_argument("--output", default="ontology/validation/cq-report.json")
    args = parser.parse_args()

    def resolve(path: str) -> Path:
        p = Path(path)
        return p if p.is_absolute() else ROOT / p

    graph = Graph()
    graph.parse(resolve(args.ontology), format="turtle")
    graph.parse(resolve(args.sample), format="turtle")
    expectations = json.loads(resolve(args.expectations).read_text(encoding="utf-8"))["queries"]
    query_dir = resolve(args.queries)

    reports = []
    all_pass = True
    for query_name in sorted(expectations):
        expectation = expectations[query_name]
        query_text = (query_dir / query_name).read_text(encoding="utf-8")
        result = graph.query(query_text)
        rows = list(result)
        variables = [str(v) for v in result.vars]
        row_dicts = [{variables[i]: literal_value(row[i]) for i in range(len(variables))} for row in rows]
        checks = {}
        if "min_rows" in expectation:
            checks["min_rows"] = len(rows) >= expectation["min_rows"]
        if "exact_rows" in expectation:
            checks["exact_rows"] = len(rows) == expectation["exact_rows"]
        if "first_row_equals" in expectation:
            first = row_dicts[0] if row_dicts else {}
            for key, expected in expectation["first_row_equals"].items():
                checks[f"first_row.{key}"] = first.get(key) == expected
        passed = all(checks.values()) if checks else False
        all_pass = all_pass and passed
        reports.append({
            "query": query_name,
            "rows": len(rows),
            "variables": variables,
            "first_row": row_dicts[0] if row_dicts else None,
            "checks": checks,
            "status": "PASS" if passed else "FAIL",
        })

    report = {
        "schema_version": 1,
        "profile": "CM-PharmE-B5-executable-competency-questions",
        "status": "PASS" if all_pass else "FAIL",
        "query_count": len(reports),
        "queries": reports,
        "boundary": "These executable CQs are bounded regression/evaluation tests over the constructed vaccine scenario, not empirical deployment validation.",
    }
    output = resolve(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    if not all_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
