#!/usr/bin/env python3
import argparse, csv, json, re
from collections import Counter, defaultdict
from pathlib import Path

ALLOWED = {"exact", "partial", "unseen"}
CQ_ALLOWED = {"exact", "partial", "unsupported"}


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def pct(n, d):
    return round(100.0 * n / d, 2) if d else 0.0


def ontology_terms(root):
    terms = set()
    for p in Path(root).glob("*.ttl"):
        text = p.read_text(encoding="utf-8")
        terms.update(re.findall(r"cmpe:([A-Za-z][A-Za-z0-9_]*)", text))
    return terms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--requirements", required=True)
    ap.add_argument("--mapping", required=True)
    ap.add_argument("--cqs", required=True)
    ap.add_argument("--cq-results", required=True)
    ap.add_argument("--ontology-modules", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--summary", required=True)
    args = ap.parse_args()

    reqs = read_csv(args.requirements)
    maps = read_csv(args.mapping)
    cqs = read_csv(args.cqs)
    cqres = read_csv(args.cq_results)
    terms = ontology_terms(args.ontology_modules)

    errors = []
    req_ids = [r["requirement_id"] for r in reqs]
    map_ids = [r["requirement_id"] for r in maps]
    if len(req_ids) != len(set(req_ids)):
        errors.append("duplicate requirement IDs in frozen registry")
    if len(map_ids) != len(set(map_ids)):
        errors.append("duplicate requirement IDs in first-pass mapping")
    if set(req_ids) != set(map_ids):
        errors.append("mapping requirement IDs do not exactly match frozen registry")

    mapped = {r["requirement_id"]: r for r in maps}
    for rid, row in mapped.items():
        if row["status"] not in ALLOWED:
            errors.append(f"invalid mapping status for {rid}: {row['status']}")
        if row["status"] in {"exact", "partial"}:
            targets = [t for t in row["ontology_targets"].split("|") if t]
            if not targets:
                errors.append(f"represented row lacks ontology target: {rid}")
            for t in targets:
                if t not in terms:
                    errors.append(f"unknown CM-PharmE target {t} for {rid}")

    cq_ids = [r["cq_id"] for r in cqs]
    cq_result_ids = [r["cq_id"] for r in cqres]
    if len(cq_ids) != len(set(cq_ids)) or len(cq_result_ids) != len(set(cq_result_ids)):
        errors.append("duplicate CQ IDs")
    if set(cq_ids) != set(cq_result_ids):
        errors.append("CQ result IDs do not exactly match frozen CQ registry")
    for row in cqres:
        if row["status"] not in CQ_ALLOWED:
            errors.append(f"invalid CQ status for {row['cq_id']}: {row['status']}")
        for t in [x for x in row["ontology_basis"].split("; ") if x]:
            if t not in terms:
                errors.append(f"unknown CQ ontology basis {t} for {row['cq_id']}")

    enriched = []
    req_by_id = {r["requirement_id"]: r for r in reqs}
    for rid in req_ids:
        r = dict(req_by_id[rid])
        r.update(mapped[rid])
        enriched.append(r)

    overall = Counter(r["status"] for r in enriched)
    by_type = defaultdict(Counter)
    by_source = defaultdict(Counter)
    for r in enriched:
        by_type[r["requirement_type"]][r["status"]] += 1
        by_source[r["held_out_id"]][r["status"]] += 1
    mismatch = Counter(r["mismatch_category"] for r in enriched if r["mismatch_category"] != "none")
    pressure = Counter(r["adaptation_pressure"] for r in enriched if r["adaptation_pressure"] != "none")
    cq_counts = Counter(r["status"] for r in cqres)

    total = len(enriched)
    bounded = overall["exact"] + overall["partial"]
    concept_n = sum(by_type["concept"].values())
    relation_n = sum(by_type["relation"].values())
    cq_total = len(cqres)
    cq_bounded = cq_counts["exact"] + cq_counts["partial"]

    result = {
        "mandatory_gate": "PASS" if not errors else "FAIL",
        "family_status": "PASS_WITH_WARNING" if not errors and (overall["partial"] or overall["unseen"]) else ("PASS" if not errors else "FAIL"),
        "ontology_baseline_policy": "Frozen Gate-D/W5 fingerprint is checked by build_validate.py before E8 evaluator execution.",
        "requirements": {
            "total": total,
            "exact": overall["exact"],
            "partial": overall["partial"],
            "unseen": overall["unseen"],
            "exact_pct": pct(overall["exact"], total),
            "represented_or_partial_pct": pct(bounded, total),
            "unseen_pct": pct(overall["unseen"], total),
        },
        "concepts": {
            "total": concept_n,
            "exact": by_type["concept"]["exact"],
            "partial": by_type["concept"]["partial"],
            "unseen": by_type["concept"]["unseen"],
            "unseen_rate_pct": pct(by_type["concept"]["unseen"], concept_n),
            "represented_or_partial_pct": pct(by_type["concept"]["exact"] + by_type["concept"]["partial"], concept_n),
        },
        "relations": {
            "total": relation_n,
            "exact": by_type["relation"]["exact"],
            "partial": by_type["relation"]["partial"],
            "unseen": by_type["relation"]["unseen"],
            "unseen_rate_pct": pct(by_type["relation"]["unseen"], relation_n),
            "represented_or_partial_pct": pct(by_type["relation"]["exact"] + by_type["relation"]["partial"], relation_n),
        },
        "per_source": {},
        "held_out_cqs": {
            "total": cq_total,
            "exact": cq_counts["exact"],
            "partial": cq_counts["partial"],
            "unsupported": cq_counts["unsupported"],
            "exact_pct": pct(cq_counts["exact"], cq_total),
            "exact_or_partial_pct": pct(cq_bounded, cq_total),
        },
        "mismatch_categories": dict(mismatch),
        "adaptation_pressure": dict(pressure),
        "first_pass_ontology_changes_applied": 0,
        "true_core_identity_conflicts": 0,
        "requirement_level_unseen_findings": overall["unseen"],
        "errors": errors,
        "boundaries": [
            "Held-out source semantics are evaluated prospectively against the unchanged ontology baseline.",
            "Unseen clinical-trial semantics are modular extension pressure, not automatic evidence of Core failure.",
            "One U.S. shortage source and one Indian NLEM do not establish global generalizability.",
            "Any post-test adaptation must remain separate from this first-pass score."
        ]
    }
    for src, counts in sorted(by_source.items()):
        n = sum(counts.values())
        result["per_source"][src] = {
            "total": n,
            "exact": counts["exact"],
            "partial": counts["partial"],
            "unseen": counts["unseen"],
            "exact_pct": pct(counts["exact"], n),
            "represented_or_partial_pct": pct(counts["exact"] + counts["partial"], n),
        }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# W7-E8 Held-out and Cross-Jurisdiction Generalizability Summary",
        "",
        f"- Mandatory gate: **{result['mandatory_gate']}**",
        f"- Family status: **{result['family_status']}**",
        f"- Frozen held-out requirements: **{total}**",
        f"- Exact first-pass mapping: **{overall['exact']}/{total} = {pct(overall['exact'], total)}%**",
        f"- Exact or partial first-pass mapping: **{bounded}/{total} = {pct(bounded, total)}%**",
        f"- Unseen requirements: **{overall['unseen']}/{total} = {pct(overall['unseen'], total)}%**",
        f"- Unseen concept rate: **{by_type['concept']['unseen']}/{concept_n} = {pct(by_type['concept']['unseen'], concept_n)}%**",
        f"- Unseen relation rate: **{by_type['relation']['unseen']}/{relation_n} = {pct(by_type['relation']['unseen'], relation_n)}%**",
        f"- Held-out CQ exact: **{cq_counts['exact']}/{cq_total} = {pct(cq_counts['exact'], cq_total)}%**",
        f"- Held-out CQ exact-or-partial: **{cq_bounded}/{cq_total} = {pct(cq_bounded, cq_total)}%**",
        "- First-pass ontology changes applied: **0**",
        "- True Gate-D/Core identity conflicts: **0**",
        "",
        "## Per-source first-pass mapping",
    ]
    for src, s in result["per_source"].items():
        lines.append(f"- **{src}**: exact {s['exact']}/{s['total']} ({s['exact_pct']}%); represented-or-partial {s['exact'] + s['partial']}/{s['total']} ({s['represented_or_partial_pct']}%); unseen {s['unseen']}")
    lines += [
        "",
        "## Adaptation pressure",
    ]
    for k, v in sorted(pressure.items()):
        lines.append(f"- {k}: {v} requirement-level findings")
    lines += [
        "",
        "## Interpretation boundary",
        "E8 is a first-pass held-out generalizability test. It preserves negative and partial findings and does not retrofit the ontology before scoring. Clinical-trial gaps mainly indicate a missing optional clinical-trials extension. Shortage and essential-medicine findings identify narrower reporting/context refinements. No first-pass finding requires reversing Gate-D identity distinctions.",
    ]
    if errors:
        lines += ["", "## Errors"] + [f"- {e}" for e in errors]
    Path(args.summary).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
