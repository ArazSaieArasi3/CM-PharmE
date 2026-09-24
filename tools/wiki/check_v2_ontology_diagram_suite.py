#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
WIKI=ROOT/"wiki-src"
PAGES=WIKI/"pages"
MANIFEST=WIKI/"diagrams"/"manifest.json"
COVERAGE=WIKI/"ontology-reference"/"ontology-diagram-coverage.json"
REVIEW=WIKI/"ontology-reference"/"ontology-diagram-semantic-review.md"

EXPECTED_IDS=[f"DGM-ONT-{i:03d}" for i in range(2,12)]
AUTH_REF="v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999"

def main():
    errors=[]
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_id={d["id"]:d for d in manifest.get("diagrams",[])}
    cov=json.loads(COVERAGE.read_text(encoding="utf-8"))
    review=REVIEW.read_text(encoding="utf-8")
    suite=(PAGES/"V2-Ontology-Diagram-Suite.md").read_text(encoding="utf-8")
    guide=(PAGES/"Ontology-and-Conceptual-Model-Guide.md").read_text(encoding="utf-8")
    ufo=(PAGES/"V2-UFO-and-OntoUML-Architecture.md").read_text(encoding="utf-8")
    ref=(PAGES/"V2-Ontology-Reference.md").read_text(encoding="utf-8")

    for did in EXPECTED_IDS:
        if did not in by_id:
            errors.append(f"manifest missing {did}")
            continue
        d=by_id[did]
        if d.get("notation")!="OntoUML/UFO-aware conceptual notation":
            errors.append(f"{did}: wrong notation")
        if d.get("checked_ref")!=AUTH_REF:
            errors.append(f"{did}: stale/wrong checked_ref {d.get('checked_ref')}")
        for field in ["source_path","rendered_path","purpose","caption","alt_text"]:
            if not d.get(field):
                errors.append(f"{did}: missing {field}")
        for field in ["source_path","rendered_path"]:
            p=ROOT/d.get(field,"")
            if not p.exists():
                errors.append(f"{did}: missing {field} file {p}")
        if did not in suite:
            errors.append(f"{did}: absent from reader-facing suite page")

    if cov.get("diagram_count")!=10:
        errors.append(f"diagram_count expected 10 got {cov.get('diagram_count')}")
    if cov.get("required_family_count")!=10:
        errors.append("required_family_count must be 10")
    if cov.get("domain_coverage")!="17/17":
        errors.append(f"domain coverage must be 17/17, got {cov.get('domain_coverage')}")
    if len(cov.get("represented_domains",[]))!=17:
        errors.append("represented_domains must contain 17 domains")
    if cov.get("semantic_validation_errors")!=0:
        errors.append("semantic validation errors must be zero")
    if cov.get("unique_concept_nodes",0)<60:
        errors.append("unexpected regression: fewer than 60 unique concept nodes represented")
    if cov.get("unique_object_properties",0)<30:
        errors.append("unexpected regression: fewer than 30 unique object properties represented")

    required_review=[
        "10/10 diagram specifications",
        "zero semantic validation errors",
        "every concept node resolves",
        "every displayed stereotype",
        "every object-property edge",
        "all 17 V2 domains",
        "does not constitute semantic approval",
    ]
    for phrase in required_review:
        if phrase not in review:
            errors.append(f"semantic-review checklist missing phrase: {phrase}")

    if "[[V2 Ontology Diagram Suite]]" not in guide:
        errors.append("Ontology Guide lacks V2 Ontology Diagram Suite link")
    if "[[V2 Ontology Diagram Suite]]" not in ufo:
        errors.append("V2 UFO/OntoUML page lacks suite link")
    if "DGM-ONT-002--v2-ontology-architecture-core-x-infra-and-extensions.svg" not in ufo:
        errors.append("V2 UFO/OntoUML page lacks architecture embed")
    if "[[V2 Ontology Diagram Suite]]" not in ref:
        errors.append("V2 Ontology Reference lacks suite link")
    if "DGM-ONT-002--v2-ontology-architecture-core-x-infra-and-extensions.svg" not in ref:
        errors.append("V2 Ontology Reference lacks architecture embed")

    module_pages=list(PAGES.glob("V2-Module-*.md"))
    if len(module_pages)!=17:
        errors.append(f"expected 17 V2 module pages, got {len(module_pages)}")
    for p in module_pages:
        text=p.read_text(encoding="utf-8")
        if "[[V2 Ontology Diagram Suite]]" not in text:
            errors.append(f"{p.name}: missing suite cross-link")
        if "governed separately by #235" in text:
            errors.append(f"{p.name}: stale pre-suite placeholder remains")

    report={
      "expected_diagram_ids":EXPECTED_IDS,
      "manifest_diagrams_present":sum(1 for x in EXPECTED_IDS if x in by_id),
      "domain_coverage":cov.get("domain_coverage"),
      "unique_concept_nodes":cov.get("unique_concept_nodes"),
      "unique_object_properties":cov.get("unique_object_properties"),
      "module_pages_checked":len(module_pages),
      "semantic_validation_errors":cov.get("semantic_validation_errors"),
      "errors":errors,
    }
    print(json.dumps(report,indent=2,sort_keys=True))
    if errors:
        raise SystemExit(1)

if __name__=="__main__":
    main()
