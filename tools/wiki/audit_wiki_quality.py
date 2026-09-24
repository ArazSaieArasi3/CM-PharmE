#!/usr/bin/env python3
import argparse
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAGES = ROOT / "wiki-src" / "pages"
INVENTORY = ROOT / "wiki-src" / "page-inventory.csv"
RUBRIC = ROOT / "wiki-src" / "quality" / "wiki-quality-rubric-v1.0.json"
BASELINE = ROOT / "wiki-src" / "quality" / "WB-2026.09.1-baseline-assessment.json"

def collect_metrics():
    files = sorted(PAGES.glob("*.md"))
    result = {
        "page_files": len(files),
        "words": 0,
        "headings": 0,
        "table_lines": 0,
        "links": 0,
        "image_links": 0,
        "mermaid_blocks": 0,
        "metadata_lines": 0,
        "gate_pages": 0,
        "gate_occurrences": 0,
        "wave_pages": 0,
        "wave_occurrences": 0,
        "human_review_pages": 0,
        "human_review_occurrences": 0,
    }
    for path in files:
        text = path.read_text(encoding="utf-8")
        result["words"] += len(re.findall(r"\b[\w’'-]+\b", text))
        result["headings"] += len(re.findall(r"^#{1,6}\s+", text, re.M))
        result["table_lines"] += len(re.findall(r"^\|.*\|$", text, re.M))
        result["links"] += len(re.findall(r"\[[^\]]+\]\([^)]+\)|\[\[[^\]]+\]\]", text))
        result["image_links"] += len(re.findall(r"!\[[^\]]*\]\([^)]+\)", text))
        result["mermaid_blocks"] += text.count(chr(96) * 3 + "mermaid")
        result["metadata_lines"] += len(re.findall(r"^> \*\*", text, re.M))

        gate = len(re.findall(r"\bGate\b", text))
        wave = len(re.findall(r"\bW[0-8]\b|\bWave\b", text))
        human = len(re.findall(r"Human Review|Human Ontology Review|human review", text, re.I))
        result["gate_occurrences"] += gate
        result["wave_occurrences"] += wave
        result["human_review_occurrences"] += human
        result["gate_pages"] += int(gate > 0)
        result["wave_pages"] += int(wave > 0)
        result["human_review_pages"] += int(human > 0)

    with INVENTORY.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    result["inventory_entries"] = len(rows)
    result["source_complete"] = sum(row["source_status"] == "source-complete" for row in rows)
    result["published"] = sum(row["publish_status"] == "published" for row in rows)
    result["planned"] = [row["page"] for row in rows if row["source_status"] != "source-complete"]
    result["metadata_lines_per_page"] = round(result["metadata_lines"] / len(files), 2) if files else 0
    return result

def validate_rubric_and_baseline():
    rubric = json.loads(RUBRIC.read_text(encoding="utf-8"))
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))

    quantitative_weight = sum(item["weight"] for item in rubric["quantitative"]["criteria"])
    qualitative_weight = sum(item["weight"] for item in rubric["qualitative"]["criteria"])
    if quantitative_weight != 100 or qualitative_weight != 100:
        raise SystemExit(f"FAIL rubric weights: quantitative={quantitative_weight}, qualitative={qualitative_weight}")

    q_ids = {item["id"] for item in rubric["quantitative"]["criteria"]}
    l_weights = {item["id"]: item["weight"] for item in rubric["qualitative"]["criteria"]}
    if set(baseline["quantitative"]["scores"]) != q_ids:
        raise SystemExit("FAIL quantitative criterion IDs do not match frozen rubric")
    if set(baseline["qualitative"]["ratings"]) != set(l_weights):
        raise SystemExit("FAIL qualitative criterion IDs do not match frozen rubric")

    q_total = sum(baseline["quantitative"]["scores"].values())
    if q_total != baseline["quantitative"]["total"]:
        raise SystemExit("FAIL quantitative total mismatch")

    l_total = round(sum(l_weights[key] * rating / 5 for key, rating in baseline["qualitative"]["ratings"].items()), 2)
    if l_total != baseline["qualitative"]["total"]:
        raise SystemExit(f"FAIL qualitative total mismatch: calculated={l_total}")

    if q_total != 70 or l_total != 72.0:
        raise SystemExit(f"FAIL frozen baseline changed unexpectedly: quantitative={q_total}, qualitative={l_total}")

    return {
        "rubric_id": rubric["rubric_id"],
        "quantitative_weight": quantitative_weight,
        "qualitative_weight": qualitative_weight,
        "baseline_quantitative": q_total,
        "baseline_qualitative": l_total,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()

    payload = {"metrics": collect_metrics()}
    if args.validate:
        payload["validation"] = validate_rubric_and_baseline()

    if args.output:
        Path(args.output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(payload, sort_keys=True))

if __name__ == "__main__":
    main()
