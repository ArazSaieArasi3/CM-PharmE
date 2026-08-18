#!/usr/bin/env python3
"""Validate a ROBOT axiom diff for formal-syntax conversion.

Manchester/Functional renderers may materialize explicit OWL Declaration axioms for
entities that were already used implicitly in the RDF source. Such declaration-only
normalization is recorded but is not treated as a semantic axiom change. Any removed
axiom or any added non-Declaration axiom fails the check.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

COUNT_PATTERNS = [
    re.compile(r"(?P<count>\d+) axioms? in left ontology but not in right ontology", re.I),
    re.compile(r"(?P<count>\d+) axioms? in right ontology but not in left ontology", re.I),
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--diff", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    diff_path = Path(args.diff)
    text = diff_path.read_text(encoding="utf-8") if diff_path.exists() else ""
    counts = []
    for pattern in COUNT_PATTERNS:
        match = pattern.search(text)
        counts.append(int(match.group("count")) if match else None)

    removed = [line[2:].strip() for line in text.splitlines() if line.startswith("- ")]
    added = [line[2:].strip() for line in text.splitlines() if line.startswith("+ ")]
    declaration_additions = [axiom for axiom in added if axiom.startswith("Declaration(")]
    nondeclaration_additions = [axiom for axiom in added if not axiom.startswith("Declaration(")]

    empty_report = not text.strip()
    counts_consistent = (
        empty_report
        or (counts[0] == len(removed) and counts[1] == len(added))
    )
    passed = empty_report or (
        counts_consistent
        and len(removed) == 0
        and len(nondeclaration_additions) == 0
    )

    report = {
        "schema_version": 2,
        "profile": "CM-PharmE-B6-ROBOT-axiom-diff-check",
        "diff_file": str(diff_path),
        "robot_plain_diff_empty": empty_report,
        "left_only_axioms": counts[0],
        "right_only_axioms": counts[1],
        "removed_axioms": removed,
        "declaration_only_additions": declaration_additions,
        "nondeclaration_additions": nondeclaration_additions,
        "counts_consistent_with_diff_lines": counts_consistent,
        "status": "PASS" if passed else "FAIL",
        "boundary": "ROBOT/OWLAPI may materialize explicit Declaration axioms when rendering Manchester or Functional Syntax. This check permits only those declaration additions; any removed axiom or added non-Declaration axiom is treated as a semantic round-trip failure.",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
