#!/usr/bin/env python3
"""Check G1 coverage against the candidate trigger screen and cited project artifacts."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
W4 = ROOT / "v2/research/w4"
CANDIDATE = ROOT / "v2/ontology/candidates/2.1.0-alpha.0-review/modules"


def main() -> None:
    register = json.loads((W4 / "g1-relrig-decision-register.json").read_text())
    audit = json.loads((W4 / "pattern-audit-baseline.json").read_text())
    expected = {tuple(pair) for pair in audit["review_candidate_diagram"]["rigid_type_mediation_triggers"]}
    rows = register["cases"]
    actual = [(row["relator"], row["rigid_end"]) for row in rows]
    assert len(actual) == len(set(actual)) == len(expected) == 15
    assert set(actual) == expected, {"missing": sorted(expected - set(actual)), "extra": sorted(set(actual) - expected)}
    assert [row["id"] for row in rows] == [f"RR-{n:02}" for n in range(1, 16)]

    patterns = (W4 / "relator-material-patterns.md").read_text()
    relations = (ROOT / "v2/research/w3/candidate-relations-events.md").read_text()
    ttl = "\n".join(path.read_text() for path in sorted(CANDIDATE.glob("*.ttl")))
    for row in rows:
        assert re.search(rf"^### {re.escape(row['w4_pattern'])}\. ", patterns, re.M), row["id"]
        assert row["w3_relations"] and all(f"| {code} |" in relations for code in row["w3_relations"]), row["id"]
        assert f"cmpe:{row['candidate_property']} a owl:ObjectProperty" in ttl, row["id"]
        assert all(row[key].strip() for key in ("proposal", "counterexample", "decision_needed")), row["id"]
    assert register["status"] == "PROPOSED_NOT_APPROVED"
    print(f"G1 register OK: {len(rows)} of {len(expected)} candidate RelRig triggers; W3/W4/OWL citations found; 0 author decisions recorded")


if __name__ == "__main__":
    main()
