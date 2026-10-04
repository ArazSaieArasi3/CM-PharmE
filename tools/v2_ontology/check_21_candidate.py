#!/usr/bin/env python3
"""Run scoped positive/negative SHACL evidence for the 2.1 review candidate."""
from __future__ import annotations

import json
from pathlib import Path

from pyshacl import validate
from rdflib import Graph, Namespace, RDF

ROOT = Path(__file__).resolve().parents[2]
CANDIDATE = ROOT / "v2/ontology/candidates/2.1.0-alpha.0-review"
SH = Namespace("http://www.w3.org/ns/shacl#")


def main() -> None:
    ontology = Graph()
    for path in sorted((CANDIDATE / "modules").glob("*.ttl")):
        ontology.parse(path, format="turtle")
    shapes = Graph().parse(CANDIDATE / "review-constraints.ttl", format="turtle")
    result = {}
    for scenario, expected, count in (("positive", True, 0), ("negative", False, 4)):
        data = Graph().parse(CANDIDATE / f"smoke-{scenario}.ttl", format="turtle")
        conforms, report, _ = validate(data, shacl_graph=shapes, ont_graph=ontology,
                                       inference="rdfs", abort_on_first=False)
        violations = list(report.subjects(RDF.type, SH.ValidationResult))
        result[scenario] = {"conforms": bool(conforms), "violations": len(violations),
                            "components": sorted(str(report.value(v, SH.sourceConstraintComponent)).split("#")[-1]
                                                 for v in violations)}
        if bool(conforms) != expected or len(violations) != count:
            raise SystemExit(f"Unexpected {scenario} SHACL result: {result[scenario]}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
