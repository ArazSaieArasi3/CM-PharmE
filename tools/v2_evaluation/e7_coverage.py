#!/usr/bin/env python3
"""W7-E7 concept and relation coverage evaluator.

Quantifies source-semantic requirements against the frozen Gate-D/W5 ontology.
Coverage is source-bounded evidence, not proof of global pharmaceutical-domain
completeness. Held-out H1-H3 are intentionally excluded until W7-E8.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

from rdflib import Graph, URIRef

CMPE = "https://w3id.org/cm-pharme/2.0/"


def args():
    p = argparse.ArgumentParser()
    p.add_argument("--registry", required=True)
    p.add_argument("--rules", required=True)
    p.add_argument("--ontology", required=True)
    p.add_argument("--conceptual-model", required=True)
    p.add_argument("--migration-matrix", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--summary", required=True)
    return p.parse_args()


def pct(n, d):
    return round((100.0 * n / d), 2) if d else None


def expand_target(token: str) -> URIRef:
    if token.startswith("cmpe:"):
        return URIRef(CMPE + token.split(":", 1)[1])
    if token.startswith("http://") or token.startswith("https://"):
        return URIRef(token)
    raise ValueError(f"Unsupported ontology target token: {token}")


def local_name(token: str) -> str | None:
    if token.startswith("cmpe:"):
        return token.split(":", 1)[1]
    if token.startswith(CMPE):
        return token[len(CMPE):]
    return None


def main():
    a = args()
    registry_text = Path(a.registry).read_text(encoding="utf-8")
    with open(a.registry, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    rules = json.loads(Path(a.rules).read_text(encoding="utf-8"))
    conceptual = json.loads(Path(a.conceptual_model).read_text(encoding="utf-8"))
    migration_text = Path(a.migration_matrix).read_text(encoding="utf-8")
    ontology = Graph().parse(a.ontology)

    errors = []
    warnings = []
    allowed_status = set(rules["allowed_statuses"])
    allowed_types = {"concept", "relation"}
    seen_ids = set()
    by_source = defaultdict(list)

    for r in rows:
        rid = r["requirement_id"].strip()
        if not rid or rid in seen_ids:
            errors.append(f"duplicate-or-empty requirement_id: {rid!r}")
        seen_ids.add(rid)
        if r["coverage_status"] not in allowed_status:
            errors.append(f"{rid}: invalid coverage_status {r['coverage_status']}")
        if r["requirement_type"] not in allowed_types:
            errors.append(f"{rid}: invalid requirement_type {r['requirement_type']}")
        by_source[r["source_id"]].append(r)
        targets = [x.strip() for x in r["ontology_targets"].split(";") if x.strip()]
        if r["coverage_status"] in {"represented", "partial"} and not targets:
            errors.append(f"{rid}: {r['coverage_status']} row has no ontology target")
        for t in targets:
            iri = expand_target(t)
            if t.startswith("cmpe:") and not any(ontology.triples((iri, None, None))):
                errors.append(f"{rid}: unresolved CM-PharmE ontology target {t}")

    for source in rules["source_order"]:
        if source not in by_source:
            errors.append(f"source_order entry has no requirements: {source}")
    unexpected_sources = sorted(set(by_source) - set(rules["source_order"]))
    if unexpected_sources:
        errors.append(f"registry sources missing from source_order: {unexpected_sources}")

    contamination = [tok for tok in rules["held_out_forbidden_tokens"] if tok.lower() in registry_text.lower()]
    if contamination:
        errors.append(f"held-out token contamination in E7 registry: {contamination}")

    status_counts = Counter(r["coverage_status"] for r in rows)
    type_counts = Counter(r["requirement_type"] for r in rows)
    represented = status_counts["represented"]
    partial = status_counts["partial"]
    not_rep = status_counts["not_represented"]

    per_source = []
    for source in rules["source_order"]:
        rs = by_source[source]
        sc = Counter(r["coverage_status"] for r in rs)
        tc = Counter(r["requirement_type"] for r in rs)
        per_source.append({
            "source_id": source,
            "source_family": rs[0]["source_family"],
            "evidence_basis": sorted(set(r["evidence_basis"] for r in rs)),
            "requirements": len(rs),
            "concept_denominator": tc["concept"],
            "relation_denominator": tc["relation"],
            "represented": sc["represented"],
            "partial": sc["partial"],
            "not_represented": sc["not_represented"],
            "exact_coverage_pct": pct(sc["represented"], len(rs)),
            "bounded_coverage_pct": pct(sc["represented"] + sc["partial"], len(rs)),
            "gaps": [r["normalized_semantic"] for r in rs if r["coverage_status"] == "not_represented"],
        })

    # Separate concept/relation coverage denominators.
    by_type = {}
    for typ in ["concept", "relation"]:
        rs = [r for r in rows if r["requirement_type"] == typ]
        sc = Counter(r["coverage_status"] for r in rs)
        by_type[typ] = {
            "denominator": len(rs),
            "represented": sc["represented"],
            "partial": sc["partial"],
            "not_represented": sc["not_represented"],
            "exact_coverage_pct": pct(sc["represented"], len(rs)),
            "bounded_coverage_pct": pct(sc["represented"] + sc["partial"], len(rs)),
        }

    # Gate-D conceptual-element evidence coverage. This is deliberately a
    # different denominator from source-requirement coverage.
    module_terms = {m: [x[0] for x in vals] for m, vals in conceptual["modules"].items()}
    supported_terms = set()
    supported_property_terms = set()
    for r in rows:
        if r["coverage_status"] not in {"represented", "partial"}:
            continue
        for t in [x.strip() for x in r["ontology_targets"].split(";") if x.strip()]:
            local = local_name(t)
            if not local:
                continue
            if any(local in vals for vals in module_terms.values()):
                supported_terms.add(local)
            else:
                supported_property_terms.add(local)

    module_coverage = {}
    unsupported_by_module = {}
    for module, terms in module_terms.items():
        supported = sorted(set(terms) & supported_terms)
        unsupported = sorted(set(terms) - supported_terms)
        module_coverage[module] = {
            "denominator": len(terms),
            "evidenced": len(supported),
            "evidenced_pct": pct(len(supported), len(terms)),
            "evidenced_terms": supported,
        }
        unsupported_by_module[module] = unsupported

    # Incremental unique ontology-target contribution in frozen source order.
    seen_targets = set()
    incremental = []
    for source in rules["source_order"]:
        source_targets = set()
        for r in by_source[source]:
            if r["coverage_status"] not in {"represented", "partial"}:
                continue
            for t in [x.strip() for x in r["ontology_targets"].split(";") if x.strip()]:
                if t.startswith("cmpe:"):
                    source_targets.add(t)
        new = sorted(source_targets - seen_targets)
        incremental.append({
            "source_id": source,
            "unique_supported_targets": len(source_targets),
            "new_targets_in_frozen_order": len(new),
            "new_target_terms": new,
        })
        seen_targets |= source_targets

    critical_gaps = [
        {
            "requirement_id": r["requirement_id"],
            "source_id": r["source_id"],
            "semantic": r["normalized_semantic"],
            "status": r["coverage_status"],
        }
        for r in rows
        if r["critical"].strip().lower() == "yes" and r["coverage_status"] != "represented"
    ]
    if critical_gaps:
        warnings.append(f"critical requirements not exactly represented: {len(critical_gaps)}")
    if partial:
        warnings.append(f"partial source-semantic requirements retained: {partial}")
    if not_rep:
        warnings.append(f"not-represented source-semantic requirements retained: {not_rep}")

    v1_summary = {
        "comparison_mode": "qualitative_migration_boundary",
        "matrix_path": a.migration_matrix,
        "matrix_present": bool(migration_text.strip()),
        "source_level_v1_percentage_computed": False,
        "boundary": rules["v1_comparison_boundary"],
        "documented_material_v2_advances": 10 if "10. Prospective held-out evaluation design" in migration_text else None,
    }

    gate_pass = not errors
    family_status = "FAIL" if errors else ("PASS_WITH_WARNING" if warnings else "PASS")
    report = {
        "schema_version": 1,
        "evidence_family": "W7-E7",
        "evidence_class": "formal/computational+source-schema-evidence",
        "mandatory_gate": "PASS" if gate_pass else "FAIL",
        "family_status": family_status,
        "requirements": {
            "total": len(rows),
            "status_counts": dict(status_counts),
            "type_counts": dict(type_counts),
            "exact_coverage_pct": pct(represented, len(rows)),
            "bounded_coverage_pct": pct(represented + partial, len(rows)),
            "by_type": by_type,
        },
        "per_source": per_source,
        "gate_d_conceptual_term_evidence": {
            "denominator": conceptual["counts"]["total"],
            "evidenced": len(supported_terms),
            "evidenced_pct": pct(len(supported_terms), conceptual["counts"]["total"]),
            "by_module": module_coverage,
            "unsupported_by_module": unsupported_by_module,
            "note": "Unsupported here means not evidenced by this evaluated source-semantic registry; it does not mean the ontology term is invalid or absent from the domain."
        },
        "evidenced_nonconcept_property_terms": sorted(supported_property_terms),
        "incremental_source_contribution": incremental,
        "critical_gaps": critical_gaps,
        "v1_comparison": v1_summary,
        "held_out_used": False,
        "errors": errors,
        "warnings": warnings,
        "boundary": "E7 measures coverage of normalized semantics extracted from admitted discovery/conditional/secondary source families. It is not a global pharmaceutical-domain completeness metric and is not a held-out generalizability result."
    }

    Path(a.output).parent.mkdir(parents=True, exist_ok=True)
    Path(a.output).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# W7-E7 Concept and Relation Coverage Summary",
        "",
        f"- Mandatory gate: **{report['mandatory_gate']}**",
        f"- Family status: **{family_status}**",
        f"- Normalized source-semantic requirements: **{len(rows)}**",
        f"- Exact represented: **{represented}/{len(rows)} = {pct(represented, len(rows))}%**",
        f"- Represented or partial: **{represented + partial}/{len(rows)} = {pct(represented + partial, len(rows))}%**",
        f"- Not represented: **{not_rep}**",
        f"- Concept requirements: **{by_type['concept']['represented']}/{by_type['concept']['denominator']} exact; {by_type['concept']['represented'] + by_type['concept']['partial']}/{by_type['concept']['denominator']} bounded**",
        f"- Relation requirements: **{by_type['relation']['represented']}/{by_type['relation']['denominator']} exact; {by_type['relation']['represented'] + by_type['relation']['partial']}/{by_type['relation']['denominator']} bounded**",
        f"- Gate-D conceptual elements evidenced by evaluated sources: **{len(supported_terms)}/{conceptual['counts']['total']} = {pct(len(supported_terms), conceptual['counts']['total'])}%**",
        f"- Core evidenced: **{module_coverage['core']['evidenced']}/{module_coverage['core']['denominator']}**",
        f"- X-INFRA evidenced: **{module_coverage['x_infra']['evidenced']}/{module_coverage['x_infra']['denominator']}**",
        f"- Extension evidenced: **{module_coverage['extensions']['evidenced']}/{module_coverage['extensions']['denominator']}**",
        f"- Critical non-exact requirements: **{len(critical_gaps)}**",
        "- Held-out H1-H3 used: **false**",
        "",
        "## Per-source denominators and coverage",
    ]
    for s in per_source:
        lines.append(
            f"- **{s['source_id']}**: {s['represented']}/{s['requirements']} exact ({s['exact_coverage_pct']}%); "
            f"{s['represented'] + s['partial']}/{s['requirements']} represented-or-partial ({s['bounded_coverage_pct']}%); "
            f"concept n={s['concept_denominator']}, relation n={s['relation_denominator']}, gaps={s['not_represented']}"
        )
    if warnings:
        lines += ["", "## Warnings"] + [f"- {w}" for w in warnings]
    lines += [
        "",
        "## V1 comparison boundary",
        rules["v1_comparison_boundary"],
        "",
        "## Interpretation boundary",
        report["boundary"],
        "Evidence absence in a source family is not interpreted as proof that a concept or relation is absent from the pharmaceutical domain."
    ]
    Path(a.summary).parent.mkdir(parents=True, exist_ok=True)
    Path(a.summary).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))

    if not gate_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
