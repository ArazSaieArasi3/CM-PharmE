#!/usr/bin/env python3
import csv, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
WIKI=ROOT/"wiki-src"
PAGES=WIKI/"pages"
INV=WIKI/"page-inventory.csv"
COV=WIKI/"ontology-reference"/"coverage.json"

EXPECTED={
    "domains":17,
    "concepts":87,
    "classes":81,
    "datatypes":6,
    "object_properties":52,
    "datatype_properties":5,
}
EXPECTED_GENERATED={
    "module_pages":17,
    "concept_pages":87,
    "object_property_pages":52,
    "datatype_property_pages":5,
    "reference_index_pages":1,
    "total_generated_reference_pages":162,
}

def main():
    errors=[]
    cov=json.loads(COV.read_text(encoding="utf-8"))

    if cov.get("errors"):
        errors.append("coverage.json contains errors: "+repr(cov["errors"]))

    for k,v in EXPECTED.items():
        if cov.get("expected",{}).get(k)!=v:
            errors.append(f"coverage expected.{k} != {v}")
        if cov.get("actual",{}).get(k)!=v:
            errors.append(f"coverage actual.{k} != {v}")

    for k,v in EXPECTED_GENERATED.items():
        if cov.get("generated",{}).get(k)!=v:
            errors.append(f"coverage generated.{k} != {v}")

    if cov.get("unmatched_formal_concept_entities"):
        errors.append("unmatched formal conceptual entities are not empty")

    with INV.open(encoding="utf-8",newline="") as fh:
        rows=list(csv.DictReader(fh))
    r234=[r for r in rows if r["primary_issue"]=="234"]
    if len(r234)!=162:
        errors.append(f"inventory #234 rows expected 162 got {len(r234)}")
    if any(r["source_status"]!="source-complete" for r in r234):
        errors.append("one or more #234 inventory rows are not source-complete")

    ref=PAGES/"V2-Ontology-Reference.md"
    if not ref.exists():
        errors.append("V2-Ontology-Reference.md missing")
        ref_text=""
    else:
        ref_text=ref.read_text(encoding="utf-8")

    required_phrases=[
        "Conceptual elements:** 87",
        "OWL classes:** 81",
        "Declared conceptual/formal datatypes:** 6",
        "Object properties:** 52",
        "Datatype properties:** 5",
        "Review taxonomy:** 17",
        "87 conceptual elements are **not** 87 OWL classes",
        "Generated vs curated boundary",
        "Related implementation, mappings, diagrams and evaluation",
    ]
    for p in required_phrases:
        if p not in ref_text:
            errors.append("V2 Ontology Reference missing required phrase: "+p)

    page_names={r["page"]:r for r in r234}
    module=[r for r in r234 if r["page"].startswith("V2 Module ")]
    concepts=[r for r in r234 if r["page"].startswith("V2 Concept C")]
    obj=[r for r in r234 if r["page"].startswith("V2 Object Property ")]
    dtp=[r for r in r234 if r["page"].startswith("V2 Datatype Property ")]
    if len(module)!=17: errors.append(f"module inventory count {len(module)} != 17")
    if len(concepts)!=87: errors.append(f"concept inventory count {len(concepts)} != 87")
    if len(obj)!=52: errors.append(f"object-property inventory count {len(obj)} != 52")
    if len(dtp)!=5: errors.append(f"datatype-property inventory count {len(dtp)} != 5")

    for r in r234:
        path=PAGES/(r["slug"]+".md")
        if not path.exists():
            errors.append("generated reference page missing: "+str(path))
            continue
        text=path.read_text(encoding="utf-8")
        if r["page"]!="V2 Ontology Reference" and "Generated" not in text:
            errors.append(r["page"]+": generated/reference labeling missing")
        if r["page"] not in ref_text and r["page"]!="V2 Ontology Reference":
            # Wiki alias targets use the complete page name in the generated index.
            errors.append(r["page"]+": not directly linked from V2 Ontology Reference")

    home=(PAGES/"Home.md").read_text(encoding="utf-8")
    guide=(PAGES/"Ontology-and-Conceptual-Model-Guide.md").read_text(encoding="utf-8")
    if "[[V2 Ontology Reference]]" not in home:
        errors.append("Home lacks direct V2 Ontology Reference link")
    if "[[V2 Ontology Reference]]" not in guide:
        errors.append("Ontology guide lacks V2 Ontology Reference link")

    for required in [
        WIKI/"ontology-reference"/"ARCHITECTURE.md",
        WIKI/"ontology-reference"/"GENERATED-VS-CURATED.md",
        WIKI/"ontology-reference"/"SOURCE-OF-TRUTH.md",
        WIKI/"ontology-reference"/"MISSING-ITEMS.md",
        WIKI/"ontology-reference"/"coverage.csv",
    ]:
        if not required.exists():
            errors.append("required ontology-reference artifact missing: "+str(required.relative_to(ROOT)))

    report={
        "authority_ref":cov.get("authority_ref"),
        "inventory_issue_234_rows":len(r234),
        "module_pages":len(module),
        "concept_pages":len(concepts),
        "object_property_pages":len(obj),
        "datatype_property_pages":len(dtp),
        "coverage_actual":cov.get("actual"),
        "unmatched_formal_concept_entities":cov.get("unmatched_formal_concept_entities"),
        "errors":errors,
    }
    print(json.dumps(report,indent=2,sort_keys=True))
    if errors:
        raise SystemExit(1)

if __name__=="__main__":
    main()
