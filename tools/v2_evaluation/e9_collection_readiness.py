#!/usr/bin/env python3
"""Validate W7-E9 protocol/package integrity before real expert collection.

This tool never creates or infers expert responses. It checks that the frozen
instrument and empty collection templates remain structurally compatible with
the operational participant package.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

FROZEN_INSTRUMENT = Path("v2/evaluation/protocol/e9-expert-instrument.csv")
PARTICIPANT_TEMPLATE = Path("v2/evaluation/templates/e9-participant-register-template.csv")
RESPONSE_TEMPLATE = Path("v2/evaluation/templates/e9-expert-response-template.csv")
FINDING_TEMPLATE = Path("v2/evaluation/templates/e9-finding-register-template.csv")
DEVIATION_TEMPLATE = Path("v2/evaluation/templates/e9-deviation-log-template.csv")
FREEZE_RECORD = Path("v2/evaluation/protocol/e9-protocol-freeze.md")
REVIEW_BRIEF = Path("v2/evaluation/e9-participant-package/review-brief.md")
RECRUITMENT_MESSAGE = Path("v2/evaluation/e9-participant-package/recruitment-message.md")
RUNBOOK = Path("v2/evaluation/e9-participant-package/collection-runbook.md")

EXPECTED_INSTRUMENT_COLUMNS = [
    "item_id", "section", "audience", "dimension", "statement_or_prompt",
    "response_type", "scale_or_options", "confidence_required", "comment_policy",
]
EXPECTED_PARTICIPANT_COLUMNS = [
    "participant_id", "expertise_stratum", "role_category", "experience_band",
    "relevant_qualification_category", "country_or_region", "conflict_of_interest",
    "eligibility_basis", "consent_recorded", "consent_date", "response_status", "notes",
]
EXPECTED_RESPONSE_COLUMNS = [
    "participant_id", "item_id", "rating_or_choice", "confidence_1_to_5",
    "comment", "submitted_at_utc", "instrument_version",
]
EXPECTED_FINDING_COLUMNS = [
    "finding_id", "participant_id", "expertise_stratum", "finding_type",
    "affected_terms", "severity", "confidence_1_to_5", "comment_summary",
    "adjudication_status", "decision", "post_review_action", "decision_rationale",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def header(path: Path) -> list[str]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        return next(reader)


def row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as fh:
        return max(sum(1 for _ in csv.reader(fh)) - 1, 0)


def check(condition: bool, check_id: str, message: str) -> dict:
    return {"id": check_id, "passed": bool(condition), "message": message}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="build/w7-e9/e9-readiness.json")
    parser.add_argument("--summary", default="build/w7-e9/e9-readiness.md")
    args = parser.parse_args()

    required = [
        FROZEN_INSTRUMENT, PARTICIPANT_TEMPLATE, RESPONSE_TEMPLATE,
        FINDING_TEMPLATE, DEVIATION_TEMPLATE, FREEZE_RECORD,
        REVIEW_BRIEF, RECRUITMENT_MESSAGE, RUNBOOK,
    ]

    checks: list[dict] = []
    for path in required:
        checks.append(check(path.exists(), f"FILE:{path}", f"Required E9 artifact exists: {path}"))

    if not all(p.exists() for p in required):
        report = {
            "family": "W7-E9-READINESS",
            "status": "FAIL",
            "expert_responses_created": 0,
            "checks": checks,
        }
    else:
        with FROZEN_INSTRUMENT.open(newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))

        ids = [r["item_id"] for r in rows]
        audiences = {r["audience"] for r in rows}
        response_types = {r["response_type"] for r in rows}
        rating_rows = [r for r in rows if r["response_type"] == "rating"]
        open_rows = [r for r in rows if r["response_type"] == "open_text"]
        choice_rows = [r for r in rows if r["response_type"] == "single_choice"]

        checks.extend([
            check(header(FROZEN_INSTRUMENT) == EXPECTED_INSTRUMENT_COLUMNS, "SCHEMA:instrument", "Frozen instrument schema matches expected columns."),
            check(len(rows) == 23, "INSTRUMENT:count", "Frozen instrument contains exactly 23 items."),
            check(len(ids) == len(set(ids)), "INSTRUMENT:unique_ids", "Instrument item IDs are unique."),
            check(ids == [f"E9-{i:02d}" for i in range(1, 24)], "INSTRUMENT:ordered_ids", "Instrument contains ordered E9-01..E9-23 items."),
            check(audiences == {"all", "pharma", "ontology"}, "INSTRUMENT:audiences", "Instrument preserves all/pharma/ontology audience strata."),
            check(response_types == {"rating", "open_text", "single_choice"}, "INSTRUMENT:response_types", "Instrument preserves the three frozen response types."),
            check(len(rating_rows) == 19, "INSTRUMENT:rating_count", "Instrument contains 19 ordinal rating items."),
            check(len(open_rows) == 3, "INSTRUMENT:open_count", "Instrument contains 3 open-text gap/distinction items."),
            check(len(choice_rows) == 1 and choice_rows[0]["item_id"] == "E9-23", "INSTRUMENT:choice", "E9-23 is the frozen disposition choice item."),
            check(header(PARTICIPANT_TEMPLATE) == EXPECTED_PARTICIPANT_COLUMNS, "SCHEMA:participant", "Participant-register template schema is unchanged."),
            check(header(RESPONSE_TEMPLATE) == EXPECTED_RESPONSE_COLUMNS, "SCHEMA:response", "Expert-response template schema is unchanged."),
            check(header(FINDING_TEMPLATE) == EXPECTED_FINDING_COLUMNS, "SCHEMA:finding", "Finding-register template schema is unchanged."),
            check(row_count(PARTICIPANT_TEMPLATE) == 0, "STATE:participants_empty", "Public participant template contains zero participant records."),
            check(row_count(RESPONSE_TEMPLATE) == 0, "STATE:responses_empty", "Public response template contains zero expert responses."),
            check("7eb6be02b0acbf77f391813f616ab483d0018b86" in FREEZE_RECORD.read_text(encoding="utf-8"), "FREEZE:anchor", "Freeze record retains the pre-collection anchor commit."),
            check("does not modify" in REVIEW_BRIEF.read_text(encoding="utf-8").lower(), "PACKAGE:brief_boundary", "Review brief explicitly states that it does not modify the frozen protocol."),
            check("outside the public repository" in RECRUITMENT_MESSAGE.read_text(encoding="utf-8").lower(), "PACKAGE:privacy", "Recruitment template preserves the public-repository privacy boundary."),
            check("completion requires real eligible expert responses" in RUNBOOK.read_text(encoding="utf-8").lower(), "PACKAGE:completion_boundary", "Runbook preserves the E9 completion boundary."),
        ])

        passed = all(c["passed"] for c in checks)
        report = {
            "family": "W7-E9-READINESS",
            "status": "PASS" if passed else "FAIL",
            "expert_responses_created": 0,
            "real_expert_results_claimed": False,
            "instrument_items": len(rows),
            "rating_items": len(rating_rows),
            "open_text_items": len(open_rows),
            "single_choice_items": len(choice_rows),
            "frozen_instrument_sha256": sha256(FROZEN_INSTRUMENT),
            "freeze_anchor": "7eb6be02b0acbf77f391813f616ab483d0018b86",
            "checks_passed": sum(1 for c in checks if c["passed"]),
            "checks_total": len(checks),
            "checks": checks,
            "interpretation_boundary": (
                "PASS means the pre-collection E9 package is operationally and structurally ready. "
                "It does not mean expert recruitment, collection, analysis, or E9 completion has occurred."
            ),
        }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    summary = Path(args.summary)
    summary.parent.mkdir(parents=True, exist_ok=True)
    failed = [c for c in report["checks"] if not c["passed"]]
    summary.write_text(
        "# W7-E9 Collection Readiness\n\n"
        f"- Readiness status: **{report['status']}**\n"
        f"- Checks: **{report.get('checks_passed', 0)}/{report.get('checks_total', len(report['checks']))}**\n"
        f"- Expert responses created by this check: **{report.get('expert_responses_created', 0)}**\n"
        f"- Real expert-result claims created: **{str(report.get('real_expert_results_claimed', False)).lower()}**\n"
        f"- Freeze anchor: `{report.get('freeze_anchor', 'unavailable')}`\n\n"
        "## Boundary\n"
        f"{report.get('interpretation_boundary', 'Readiness only; no expert result is created.')}\n\n"
        + ("## Failed checks\n" + "\n".join(f"- {c['id']}: {c['message']}" for c in failed) + "\n" if failed else ""),
        encoding="utf-8",
    )

    print(json.dumps({
        "status": report["status"],
        "checks_passed": report.get("checks_passed", 0),
        "checks_total": report.get("checks_total", len(report["checks"])),
        "expert_responses_created": report.get("expert_responses_created", 0),
    }))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
