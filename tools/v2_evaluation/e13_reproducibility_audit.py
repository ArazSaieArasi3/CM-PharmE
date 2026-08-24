#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def add_check(checks: list[dict], name: str, passed: bool, detail: str) -> None:
    checks.append({"name": name, "passed": bool(passed), "detail": detail})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", default="v2/evaluation/protocol/e13-reproducibility-baseline.json")
    ap.add_argument("--build-root", default="build/w7-e13")
    ap.add_argument("--environment", default="build/w7-e13/environment.txt")
    ap.add_argument("--output", default="build/w7-e13/e13-reproducibility-audit.json")
    ap.add_argument("--summary", default="build/w7-e13/e13-reproducibility-audit.md")
    args = ap.parse_args()

    root = Path(args.build_root)
    baseline_path = Path(args.baseline)
    baseline = load_json(baseline_path)
    expected = baseline["expected_fingerprints"]

    checks: list[dict] = []
    generated_files: dict[str, dict] = {}

    formal_a_manifest = root / "formal-a/manifest.json"
    formal_b_manifest = root / "formal-b/manifest.json"
    formal_a_nt = root / "formal-a/distributions/cm-pharme-v2.nt"
    formal_b_nt = root / "formal-b/distributions/cm-pharme-v2.nt"
    kg_a_manifest = root / "kg-a/kg-manifest.json"
    kg_b_manifest = root / "kg-b/kg-manifest.json"
    kg_a_nt = root / "kg-a/cm-pharme-v2-fixture-kg.nt"
    kg_b_nt = root / "kg-b/cm-pharme-v2-fixture-kg.nt"

    required = {
        "formal_a_manifest": formal_a_manifest,
        "formal_b_manifest": formal_b_manifest,
        "formal_a_nt": formal_a_nt,
        "formal_b_nt": formal_b_nt,
        "kg_a_manifest": kg_a_manifest,
        "kg_b_manifest": kg_b_manifest,
        "kg_a_nt": kg_a_nt,
        "kg_b_nt": kg_b_nt,
        "w6_ingest": root / "w6/ingest-report.json",
        "w6_validation": root / "w6/validation-report.json",
        "w6_sql_sparql": root / "w6/sql-sparql-equivalence.json",
        "e1": root / "e1/structural-quality.json",
        "e2": root / "e2/e2-logical-report.json",
        "e3": root / "e3/e3-ontouml-pattern-report.json",
        "e4": root / "e4/e4-cq-results.json",
        "e5": root / "e5/e5-conformance-results.json",
        "e6": root / "e6/e6-mapping-quality.json",
        "e7": root / "e7/e7-coverage.json",
        "e8": root / "e8/e8-generalizability.json",
        "e10": root / "e10/e10-semantic-consistency.json",
        "e11": root / "e11/e11-analytics-ai-evaluation.json",
        "e12": root / "e12/e12-resilience-evaluation.json",
        "environment": Path(args.environment),
        "pip_freeze": root / "pip-freeze.txt",
        "robot_version": root / "robot/robot-version.txt",
        "java_version": root / "java-version.txt",
        "postgres_version": root / "postgres-version.txt",
    }

    for key, path in required.items():
        exists = path.exists() and path.stat().st_size > 0
        add_check(checks, f"artifact:{key}", exists, str(path))
        if exists:
            generated_files[key] = {
                "path": str(path),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }

    if all(p.exists() for p in (formal_a_manifest, formal_b_manifest, formal_a_nt, formal_b_nt)):
        fa = load_json(formal_a_manifest)
        fb = load_json(formal_b_manifest)
        fa_hash = fa.get("canonical_graph_sha256")
        fb_hash = fb.get("canonical_graph_sha256")
        add_check(checks, "formal:fingerprint_pass_a_equals_pass_b", fa_hash == fb_hash, f"A={fa_hash}; B={fb_hash}")
        add_check(checks, "formal:fingerprint_equals_frozen_w5", fa_hash == expected["w5_canonical_ontology_sha256"], f"observed={fa_hash}")
        add_check(checks, "formal:canonical_nt_byte_identical", formal_a_nt.read_bytes() == formal_b_nt.read_bytes(), "canonical N-Triples pass A versus pass B")
        add_check(checks, "formal:manifest_byte_identical", formal_a_manifest.read_bytes() == formal_b_manifest.read_bytes(), "manifest pass A versus pass B")

    if all(p.exists() for p in (kg_a_manifest, kg_b_manifest, kg_a_nt, kg_b_nt)):
        ka = load_json(kg_a_manifest)
        kb = load_json(kg_b_manifest)
        ka_hash = ka.get("canonical_ntriples_sha256")
        kb_hash = kb.get("canonical_ntriples_sha256")
        add_check(checks, "kg:fingerprint_pass_a_equals_pass_b", ka_hash == kb_hash, f"A={ka_hash}; B={kb_hash}")
        add_check(checks, "kg:fingerprint_equals_frozen_w6", ka_hash == expected["w6_canonical_kg_sha256"], f"observed={ka_hash}")
        add_check(checks, "kg:canonical_nt_byte_identical", kg_a_nt.read_bytes() == kg_b_nt.read_bytes(), "canonical N-Triples pass A versus pass B")
        add_check(checks, "kg:manifest_byte_identical", kg_a_manifest.read_bytes() == kg_b_manifest.read_bytes(), "manifest pass A versus pass B")

    e2_path = required["e2"]
    if e2_path.exists():
        e2 = load_json(e2_path)
        add_check(checks, "e2:mandatory_logical_gate", e2.get("mandatory_logical_gate") == "PASS", str(e2.get("mandatory_logical_gate")))
        agreement = e2.get("agreement", {})
        add_check(checks, "e2:reasoner_named_subclass_agreement", agreement.get("named_subclass_pairs_equal") is True, str(agreement.get("named_subclass_pairs_equal")))

    for key in ("e1", "e3", "e4", "e5", "e6", "e7", "e8", "e10", "e11", "e12", "w6_validation", "w6_sql_sparql"):
        path = required[key]
        if path.exists():
            try:
                load_json(path)
                add_check(checks, f"json:{key}:parse", True, str(path))
            except Exception as exc:
                add_check(checks, f"json:{key}:parse", False, f"{path}: {exc}")

    protocol_integrity_files = [
        baseline_path,
        Path("v2/evaluation/protocol/e9-protocol-freeze.md"),
        Path("v2/evaluation/protocol/e9-expert-instrument.csv"),
        Path("v2/evaluation/protocol/e9-analysis-plan.md"),
        Path("v2/evaluation/protocol/e9-consent-ethics-data-governance.md"),
    ]
    for path in protocol_integrity_files:
        add_check(checks, f"protocol_integrity:{path.name}", path.exists() and path.stat().st_size > 0, str(path))
        if path.exists():
            generated_files[f"protocol:{path.name}"] = {"path": str(path), "bytes": path.stat().st_size, "sha256": sha256(path)}

    failed = [c for c in checks if not c["passed"]]
    warnings = [
        "E9 human expert evidence is intentionally not regenerated; only the frozen pre-collection protocol package is integrity-checked.",
        "This is an independent clean CI rebuild in a fresh GitHub-hosted environment, not an independent replication by a separate research team.",
        "Python/Java/package/ROBOT versions are pinned; GitHub Action and PostGIS service references use versioned tags rather than immutable commit/image digests, so infrastructure immutability is bounded and runtime versions are captured.",
    ]

    result = {
        "family": "W7-E13",
        "issue": 102,
        "mandatory_gate": "PASS" if not failed else "FAIL",
        "family_status": "PASS_WITH_WARNING" if not failed else "FAIL",
        "checks_total": len(checks),
        "checks_passed": len(checks) - len(failed),
        "checks_failed": len(failed),
        "checks": checks,
        "generated_file_manifest": generated_files,
        "warnings": warnings,
        "claim_boundary": baseline["boundary"],
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# W7-E13 Reproducibility and Independent Clean Rebuild Audit",
        "",
        f"- Mandatory gate: **{result['mandatory_gate']}**",
        f"- Family status: **{result['family_status']}**",
        f"- Checks: **{result['checks_passed']}/{result['checks_total']} PASS**",
        f"- Generated/checksummed artifacts: **{len(generated_files)}**",
        "- E9 human evidence regenerated: **false by design**",
        "",
        "## Deterministic baselines",
        f"- W5 ontology SHA-256: `{expected['w5_canonical_ontology_sha256']}`",
        f"- W6 KG SHA-256: `{expected['w6_canonical_kg_sha256']}`",
        "",
        "## Warnings / interpretation boundary",
    ]
    lines.extend(f"- {w}" for w in warnings)
    if failed:
        lines += ["", "## Failed checks"] + [f"- `{c['name']}` — {c['detail']}" for c in failed]
    lines += ["", "## Claim boundary", baseline["boundary"], ""]
    Path(args.summary).write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps({"mandatory_gate": result["mandatory_gate"], "checks_passed": result["checks_passed"], "checks_total": result["checks_total"]}, sort_keys=True))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
