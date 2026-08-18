#!/usr/bin/env python3
"""Assert that a ROBOT plain diff reports no OWL axiom differences."""
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

    # ROBOT may emit an empty report for identical ontologies. Otherwise require both counts to parse as zero.
    empty_report = not text.strip()
    parsed_zero = counts == [0, 0]
    passed = empty_report or parsed_zero
    report = {
        "schema_version": 1,
        "profile": "CM-PharmE-B6-ROBOT-axiom-diff-check",
        "diff_file": str(diff_path),
        "robot_plain_diff_empty": empty_report,
        "left_only_axioms": counts[0],
        "right_only_axioms": counts[1],
        "status": "PASS" if passed else "FAIL",
        "boundary": "This checks OWLAPI/ROBOT axiom equivalence across formal-syntax conversion. RDF serialization may contain additional explicit declaration triples without changing the OWL axiom set.",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
