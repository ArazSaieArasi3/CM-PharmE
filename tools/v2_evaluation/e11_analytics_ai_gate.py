#!/usr/bin/env python3
"""W7-E11 analytics/AI eligibility and benchmark-evidence gate.

This evaluator is intentionally conservative: it promotes only candidates with
all four required elements (dataset, baseline, metric, ontology-dependent
hypothesis) and preserves deferrals as evidence rather than manufacturing AI
performance claims.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--registry", default="v2/evaluation/protocol/e11-analytics-ai-eligibility.json")
    p.add_argument("--sql-sparql-report", default="build/w7-e11/sql-sparql-equivalence.json")
    p.add_argument("--entity-resolution-note", default="v2/research/w6/provenance-entity-resolution.md")
    p.add_argument("--output", default="build/w7-e11/e11-analytics-ai-evaluation.json")
    p.add_argument("--summary", default="build/w7-e11/e11-analytics-ai-evaluation.md")
    return p.parse_args()


def main():
    a = parse_args()
    registry = json.loads(Path(a.registry).read_text(encoding="utf-8"))
    candidates = registry["candidates"]
    ids = [c["id"] for c in candidates]

    checks = {}
    checks["candidate_count_17"] = len(candidates) == 17
    checks["unique_candidate_ids"] = len(ids) == len(set(ids))
    checks["analytics_count_8"] = sum(c["kind"] == "analytics" for c in candidates) == 8
    checks["ai_count_9"] = sum(c["kind"] == "ai" for c in candidates) == 9
    checks["all_have_status_reason_or_evidence"] = all(c.get("status") and (c.get("reason") or c.get("evidence")) for c in candidates)

    eligible = [c for c in candidates if c["status"] == "ELIGIBLE_BENCHMARKED"]
    eligible_ai = [c for c in eligible if c["kind"] == "ai"]
    checks["only_an08_promoted"] = [c["id"] for c in eligible] == ["AN-08"]
    checks["no_ai_candidate_promoted"] = len(eligible_ai) == 0

    required_fields = ("baseline", "metric", "ontology_hypothesis")
    checks["eligible_has_required_design"] = all(c.get("dataset_ready") and all(c.get(f) for f in required_fields) for c in eligible)

    eq = json.loads(Path(a.sql_sparql_report).read_text(encoding="utf-8"))
    checks["an08_benchmark_report_passed"] = bool(eq.get("passed")) and eq.get("benchmarks_passed") == 4 and eq.get("benchmarks_total") == 4

    er_note = Path(a.entity_resolution_note).read_text(encoding="utf-8")
    checks["entity_resolution_accuracy_boundary_present"] = "not** a real-world precision/recall evaluation" in er_note or "not a real-world precision/recall evaluation" in er_note
    ai01 = next(c for c in candidates if c["id"] == "AI-01")
    checks["ai01_deferred_without_gold"] = ai01["status"] == "DEFERRED" and "gold" in ai01["reason"].lower()

    policy = registry["claim_policy"]
    checks["ai_novelty_claim_disabled"] = policy.get("ai_novelty_claim_allowed") is False
    checks["entity_resolution_accuracy_claim_disabled"] = policy.get("entity_resolution_accuracy_claim_allowed") is False
    checks["application_utility_claim_disabled"] = policy.get("application_utility_claim_allowed") is False

    mandatory_pass = all(checks.values())
    if not mandatory_pass:
        failed = [k for k, v in checks.items() if not v]
        raise SystemExit("W7-E11 mandatory gate failed: " + ", ".join(failed))

    deferred = [c for c in candidates if c["status"].startswith("DEFERRED")]
    report = {
        "schema_version": 1,
        "family": "W7-E11",
        "issue": 100,
        "mandatory_gate": "PASS",
        "family_status": "PASS_WITH_DEFERRED_AI",
        "candidate_counts": {
            "total": len(candidates),
            "analytics": sum(c["kind"] == "analytics" for c in candidates),
            "ai": sum(c["kind"] == "ai" for c in candidates),
            "benchmark_supported": len(eligible),
            "deferred": len(deferred),
            "ai_promoted": len(eligible_ai)
        },
        "benchmark_supported_candidates": [c["id"] for c in eligible],
        "deferred_candidates": [c["id"] for c in deferred],
        "an08_sql_sparql": {
            "passed": eq.get("passed"),
            "benchmarks_passed": eq.get("benchmarks_passed"),
            "benchmarks_total": eq.get("benchmarks_total")
        },
        "checks": checks,
        "claim_boundary": "E11 supports only the already benchmarked AN-08 cross-representation analytics claim. No AI novelty, real-world entity-resolution accuracy, forecasting, shortage-prediction, GraphRAG, graph-learning, pharmacovigilance-prediction or application-utility claim is supported by current W7 evidence.",
        "interpretation": "Deferral is a positive research-integrity outcome when mandatory benchmark prerequisites are absent; it is not evidence that the deferred methods are ineffective."
    }

    Path(a.output).parent.mkdir(parents=True, exist_ok=True)
    Path(a.output).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# W7-E11 Selected Analytics and AI Demonstrators",
        "",
        "- Mandatory gate: **PASS**",
        "- Family status: **PASS_WITH_DEFERRED_AI**",
        f"- Candidate registry: **{len(candidates)}** total = 8 analytics + 9 AI",
        f"- Benchmark-supported candidates: **{len(eligible)}** (`AN-08` only)",
        f"- Deferred candidates: **{len(deferred)}**",
        "- AI candidates promoted to novelty/performance claim: **0**",
        f"- AN-08 frozen SQL↔SPARQL benchmark: **{eq.get('benchmarks_passed')}/{eq.get('benchmarks_total')} PASS**",
        "- AI-01 entity-resolution accuracy: **DEFERRED** because no defensible real-world gold subset exists",
        "",
        "## Boundary",
        report["claim_boundary"],
        "",
        "Deferral does not mean a task is scientifically uninteresting; it means the current article/repository evidence is insufficient for a defensible measured claim."
    ]
    Path(a.summary).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
