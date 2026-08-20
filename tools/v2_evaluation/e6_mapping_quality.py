#!/usr/bin/env python3
"""W7-E6 dataset-to-ontology mapping quality evaluator.

This evaluator checks the professional source-field mapping registry against the
frozen source contracts and ontology. It reports mapping quality descriptively
and does not interpret field coverage as domain completeness.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from rdflib import Graph, URIRef

CMPE = "https://w3id.org/cm-pharme/2.0/"


def args():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", required=True)
    p.add_argument("--registry", required=True)
    p.add_argument("--coverage-index", required=True)
    p.add_argument("--rules", required=True)
    p.add_argument("--ontology", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--summary", required=True)
    return p.parse_args()


def read_csv(path: str) -> list[dict[str, str]]:
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def as_bool(value: str) -> bool:
    return value.strip().lower() in {"true", "1", "yes"}


def nonempty(value: str | None) -> bool:
    return bool((value or "").strip())


def cmpe_terms(text: str) -> list[str]:
    return sorted(set(re.findall(r"cmpe:([A-Za-z][A-Za-z0-9_]*)", text or "")))


def main():
    a = args()
    manifest = json.loads(Path(a.manifest).read_text(encoding="utf-8"))
    rules = json.loads(Path(a.rules).read_text(encoding="utf-8"))
    rows = read_csv(a.registry)
    coverage_rows = read_csv(a.coverage_index)
    ontology = Graph().parse(a.ontology)

    specs = {s["id"]: s for s in manifest["sources"]}
    evaluated = rules["evaluated_sources"]
    allowed_statuses = set(rules["allowed_statuses"])
    mapped_statuses = set(rules["mapped_statuses"])
    allowed_loss = set(rules["allowed_semantic_loss"])

    failures: list[str] = []
    warnings: list[str] = []
    per_source: dict[str, dict] = {}
    registry_by_source = defaultdict(list)
    ids = {}

    for row in rows:
        mid = row["mapping_id"]
        if mid in ids:
            failures.append(f"Duplicate mapping_id: {mid}")
        ids[mid] = row
        registry_by_source[row["source_id"]].append(row)
        if row["mapping_status"] not in allowed_statuses:
            failures.append(f"{mid}: invalid mapping_status {row['mapping_status']}")
        if row["semantic_loss"] not in allowed_loss:
            failures.append(f"{mid}: invalid semantic_loss {row['semantic_loss']}")
        if not nonempty(row.get("provenance_rule")):
            failures.append(f"{mid}: missing provenance_rule")
        if not nonempty(row.get("rationale")):
            failures.append(f"{mid}: missing rationale")

        in_scope = as_bool(row["in_scope"])
        critical = as_bool(row["critical_for_principal_claim"])
        status = row["mapping_status"]
        if in_scope:
            if not nonempty(row.get("semantic_interpretation")):
                failures.append(f"{mid}: in-scope field missing semantic_interpretation")
            if status != "unmapped" and not nonempty(row.get("ontology_targets")):
                failures.append(f"{mid}: in-scope mapped field missing ontology_targets")
            if not nonempty(row.get("rdb_targets")):
                failures.append(f"{mid}: in-scope field missing rdb_targets")
        else:
            if status != "out_of_scope":
                failures.append(f"{mid}: out-of-scope field must use mapping_status=out_of_scope")
        if critical and status == "unmapped":
            failures.append(f"{mid}: critical field is unmapped")
        if critical and status == "ambiguous":
            warnings.append(f"{mid}: critical field is ambiguous; principal claim must be narrowed")

        for local in cmpe_terms(row.get("ontology_targets", "")):
            uri = URIRef(CMPE + local)
            if not any(ontology.triples((uri, None, None))):
                failures.append(f"{mid}: ontology target does not resolve in frozen ontology: cmpe:{local}")

    # Exact source-contract coverage for evaluated field-level sources.
    for source_id in evaluated:
        if source_id not in specs:
            failures.append(f"Evaluated source missing from source manifest: {source_id}")
            continue
        spec = specs[source_id]
        required = list(spec.get("required_columns", []))
        source_rows = registry_by_source[source_id]
        fields = [r["source_field"] for r in source_rows]
        dup_fields = [f for f, n in Counter(fields).items() if n > 1]
        if dup_fields:
            failures.append(f"{source_id}: duplicate field mapping decisions: {dup_fields}")
        missing = sorted(set(required) - set(fields))
        extra = sorted(set(fields) - set(required))
        if missing:
            failures.append(f"{source_id}: required fields without mapping decisions: {missing}")
        if extra:
            failures.append(f"{source_id}: mapping fields not present in frozen contract: {extra}")

        status_counts = Counter(r["mapping_status"] for r in source_rows)
        loss_counts = Counter(r["semantic_loss"] for r in source_rows)
        in_scope_rows = [r for r in source_rows if as_bool(r["in_scope"])]
        mapped_rows = [r for r in in_scope_rows if r["mapping_status"] in mapped_statuses]
        ambiguous_rows = [r for r in in_scope_rows if r["mapping_status"] == "ambiguous"]
        unmapped_rows = [r for r in in_scope_rows if r["mapping_status"] == "unmapped"]
        critical_rows = [r for r in source_rows if as_bool(r["critical_for_principal_claim"])]
        critical_status = Counter(r["mapping_status"] for r in critical_rows)
        per_source[source_id] = {
            "source_role": spec.get("role"),
            "required_field_count": len(required),
            "registry_field_count": len(source_rows),
            "contract_coverage": len(set(fields) & set(required)) / len(required) if required else None,
            "status_counts": dict(sorted(status_counts.items())),
            "semantic_loss_counts": dict(sorted(loss_counts.items())),
            "in_scope_fields": len(in_scope_rows),
            "mapped_fields": len(mapped_rows),
            "mapped_field_proportion": len(mapped_rows) / len(in_scope_rows) if in_scope_rows else None,
            "ambiguous_fields": [r["source_field"] for r in ambiguous_rows],
            "unmapped_fields": [r["source_field"] for r in unmapped_rows],
            "critical_field_count": len(critical_rows),
            "critical_status_counts": dict(sorted(critical_status.items())),
        }

    # Source coverage index must be explicit and truthful.
    coverage_index = {r["source_id"]: r for r in coverage_rows}
    for source_id in evaluated:
        cr = coverage_index.get(source_id)
        if cr is None:
            failures.append(f"{source_id}: missing from source-mapping-coverage.csv")
            continue
        if cr["field_level_mapping_status"] != "complete":
            failures.append(f"{source_id}: coverage index does not mark field mapping complete")
        expected_count = len(specs[source_id].get("required_columns", []))
        if int(cr["field_count"]) != expected_count:
            failures.append(f"{source_id}: coverage index field_count does not match frozen contract")

    # Manual audit sample was frozen in the E6 rules before evaluator execution.
    audit_results = []
    for mid in rules["manual_audit_sample"]:
        row = ids.get(mid)
        if row is None:
            failures.append(f"Manual audit sample mapping missing: {mid}")
            audit_results.append({"mapping_id": mid, "status": "MISSING"})
            continue
        passed = row.get("manual_audit") == "PASS"
        if not passed:
            failures.append(f"Manual audit sample did not pass: {mid}")
        audit_results.append({
            "mapping_id": mid,
            "source_id": row["source_id"],
            "source_field": row["source_field"],
            "mapping_status": row["mapping_status"],
            "status": row.get("manual_audit"),
        })

    # Aggregate descriptive statistics only across evaluated field-level sources.
    evaluated_rows = [r for sid in evaluated for r in registry_by_source[sid]]
    in_scope_all = [r for r in evaluated_rows if as_bool(r["in_scope"])]
    mapped_all = [r for r in in_scope_all if r["mapping_status"] in mapped_statuses]
    ambiguous_all = [r for r in in_scope_all if r["mapping_status"] == "ambiguous"]
    unmapped_all = [r for r in in_scope_all if r["mapping_status"] == "unmapped"]
    critical_all = [r for r in evaluated_rows if as_bool(r["critical_for_principal_claim"])]

    overall_status = Counter(r["mapping_status"] for r in evaluated_rows)
    overall_loss = Counter(r["semantic_loss"] for r in evaluated_rows)
    critical_status = Counter(r["mapping_status"] for r in critical_all)

    if ambiguous_all:
        warnings.append(
            f"{len(ambiguous_all)} in-scope field decisions remain explicitly ambiguous: "
            + ", ".join(f"{r['source_id']}:{r['source_field']}" for r in ambiguous_all)
        )
    bounded_all = [r for r in in_scope_all if r["mapping_status"] == "bounded"]
    if bounded_all:
        warnings.append(f"{len(bounded_all)} in-scope field decisions are bounded/partial by design")
    deferred_sources = [r["source_id"] for r in coverage_rows if r["field_level_mapping_status"] == "deferred"]
    if deferred_sources:
        warnings.append("Contract-only authoritative sources not quantified in E6: " + ", ".join(deferred_sources))

    gate = "PASS" if not failures else "FAIL"
    family = "PASS_WITH_WARNING" if gate == "PASS" and warnings else gate

    report = {
        "schema_version": 1,
        "evidence_family": "W7-E6",
        "evidence_class": "formal/computational+fixture-mapping-documentation",
        "mandatory_gate_status": gate,
        "family_status": family,
        "evaluated_sources": evaluated,
        "overall": {
            "field_decisions": len(evaluated_rows),
            "in_scope_fields": len(in_scope_all),
            "mapped_fields": len(mapped_all),
            "mapped_field_proportion": len(mapped_all) / len(in_scope_all) if in_scope_all else None,
            "ambiguous_fields": len(ambiguous_all),
            "unmapped_fields": len(unmapped_all),
            "status_counts": dict(sorted(overall_status.items())),
            "semantic_loss_counts": dict(sorted(overall_loss.items())),
            "critical_fields": len(critical_all),
            "critical_status_counts": dict(sorted(critical_status.items())),
            "critical_unmapped": sum(1 for r in critical_all if r["mapping_status"] == "unmapped"),
            "critical_ambiguous": sum(1 for r in critical_all if r["mapping_status"] == "ambiguous"),
            "provenance_rule_documented": sum(1 for r in evaluated_rows if nonempty(r.get("provenance_rule"))),
            "manual_audit_sample_passed": sum(1 for x in audit_results if x.get("status") == "PASS"),
            "manual_audit_sample_total": len(audit_results),
        },
        "per_source": per_source,
        "manual_audit_sample": audit_results,
        "warnings": warnings,
        "failures": failures,
        "held_out_used": False,
        "full_external_dataset_execution_required_for_this_check": False,
        "boundary": "E6 quantifies field-level mapping documentation for the two frozen NHIF source contracts. It does not establish ontology/domain completeness, full external dataset integration, or field-level coverage of contract-only FDA/openFDA/EMA sources."
    }

    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    o = report["overall"]
    lines = [
        "# W7-E6 Dataset-to-Ontology Mapping Quality Summary",
        "",
        f"- Mandatory gate: **{gate}**",
        f"- Family status: **{family}**",
        f"- Evaluated field decisions: **{o['field_decisions']}**",
        f"- In-scope fields: **{o['in_scope_fields']}**",
        f"- Direct/derived/bounded mapped fields: **{o['mapped_fields']}/{o['in_scope_fields']} ({o['mapped_field_proportion']*100:.2f}%)**",
        f"- Explicitly ambiguous: **{o['ambiguous_fields']}**",
        f"- Explicitly unmapped: **{o['unmapped_fields']}**",
        f"- Critical fields: **{o['critical_fields']}**; unmapped: **{o['critical_unmapped']}**; ambiguous: **{o['critical_ambiguous']}**",
        f"- Provenance rules documented: **{o['provenance_rule_documented']}/{o['field_decisions']}**",
        f"- Frozen author-side manual audit sample: **{o['manual_audit_sample_passed']}/{o['manual_audit_sample_total']} PASS**",
        "- Held-out H1–H3 used: **false**",
        "",
        "## Per-source results",
    ]
    for source_id in evaluated:
        s = per_source[source_id]
        lines += [
            f"### {source_id}",
            f"- Contract fields classified: **{s['registry_field_count']}/{s['required_field_count']}**",
            f"- In-scope mapped: **{s['mapped_fields']}/{s['in_scope_fields']} ({s['mapped_field_proportion']*100:.2f}%)**",
            f"- Ambiguous fields: **{len(s['ambiguous_fields'])}** ({', '.join(s['ambiguous_fields']) if s['ambiguous_fields'] else 'none'})",
            f"- Unmapped fields: **{len(s['unmapped_fields'])}** ({', '.join(s['unmapped_fields']) if s['unmapped_fields'] else 'none'})",
            f"- Status counts: `{json.dumps(s['status_counts'], sort_keys=True)}`",
            "",
        ]
    if warnings:
        lines += ["## Warnings"] + [f"- {w}" for w in warnings] + [""]
    if failures:
        lines += ["## Failures"] + [f"- {f}" for f in failures] + [""]
    lines += [
        "## Boundary",
        report["boundary"],
        "",
        "A high mapping proportion is descriptive evidence for the evaluated source contracts; it is not a domain-completeness score. Explicit ambiguous and bounded decisions are retained as research findings."
    ]
    Path(a.summary).parent.mkdir(parents=True, exist_ok=True)
    Path(a.summary).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))

    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
