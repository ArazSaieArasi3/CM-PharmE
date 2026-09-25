#!/usr/bin/env python3
import csv
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
WIKI=ROOT/"wiki-src"
PAGES=WIKI/"pages"
DBREF=WIKI/"database-reference"
MANIFEST=WIKI/"diagrams"/"manifest.json"
INVENTORY=WIKI/"page-inventory.csv"

EXPECTED_TABLES=24
EXPECTED_ERDS=9
EXPECTED_SUBJECT_ERDS=7
EXPECTED_VIEWS=4
EXPECTED_IDS=["DGM-ERD-%03d"%i for i in range(2,11)]

def main():
    errors=[]
    cov=json.loads((DBREF/"coverage.json").read_text(encoding="utf-8"))
    erd=json.loads((DBREF/"erd-coverage.json").read_text(encoding="utf-8"))
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_id={d["id"]:d for d in manifest.get("diagrams",[])}

    if cov.get("tables")!=EXPECTED_TABLES:
        errors.append("table count is not 24")
    if cov.get("table_pages")!=EXPECTED_TABLES:
        errors.append("table page count is not 24")
    if cov.get("views")!=EXPECTED_VIEWS:
        errors.append("view count is not 4")
    if cov.get("primary_keys")!=EXPECTED_TABLES:
        errors.append("expected one primary key per base table")
    if cov.get("foreign_keys")!=cov.get("foreign_keys_documented"):
        errors.append("foreign-key documentation coverage mismatch")
    if cov.get("postgis_extension")!=1:
        errors.append("PostGIS extension not detected")

    if erd.get("erd_count")!=EXPECTED_ERDS:
        errors.append("ERD count is not 9")
    if erd.get("subject_area_erds")!=EXPECTED_SUBJECT_ERDS:
        errors.append("subject-area ERD count is not 7")
    if erd.get("physical_tables")!=EXPECTED_TABLES:
        errors.append("physical ERD does not report 24 tables")
    if erd.get("physical_fk_edges")!=erd.get("authoritative_fk_edges"):
        errors.append("physical ERD FK coverage mismatch")
    if not erd.get("all_tables_in_physical_erd"):
        errors.append("not all tables appear in physical ERD")

    for did in EXPECTED_IDS:
        if did not in by_id:
            errors.append("manifest missing "+did)
            continue
        item=by_id[did]
        for field in ["source_path","rendered_path","purpose","checked_ref"]:
            if not item.get(field):
                errors.append(did+" missing "+field)
        for field in ["source_path","rendered_path"]:
            path=ROOT/item.get(field,"")
            if not path.exists():
                errors.append(did+" missing file "+str(path))
        svg=ROOT/item.get("rendered_path","")
        if svg.exists():
            text=svg.read_text(encoding="utf-8")
            if 'data-theme-safe="true"' not in text:
                errors.append(did+" SVG is not theme-safe")
            if 'id="diagram-background"' not in text:
                errors.append(did+" SVG lacks internal background")

    required_pages=[
      "V2-Database-Reference.md",
      "V2-Database-ERD-Suite.md",
      "V2-Database-Data-Dictionary.md",
      "V2-Database-Views.md",
    ]
    for page in required_pages:
        if not (PAGES/page).exists():
            errors.append("missing page "+page)

    table_pages=list(PAGES.glob("V2-Table-*.md"))
    if len(table_pages)!=EXPECTED_TABLES:
        errors.append("expected 24 V2 table pages, got "+str(len(table_pages)))

    master=(PAGES/"V2-Database-Reference.md").read_text(encoding="utf-8")
    for phrase in [
      "base tables: **24**",
      "PostGIS",
      "Reference/research",
      "V2 Database ERD Suite",
      "V2 Database Data Dictionary",
      "production",
    ]:
        if phrase.lower() not in master.lower():
            errors.append("master database reference missing phrase "+phrase)

    suite=(PAGES/"V2-Database-ERD-Suite.md").read_text(encoding="utf-8")
    for did in EXPECTED_IDS:
        if did not in suite:
            errors.append("ERD suite page missing "+did)

    with INVENTORY.open(encoding="utf-8-sig",newline="") as fh:
        rows=list(csv.DictReader(fh))
    r236=[r for r in rows if r["primary_issue"]=="236"]
    if len(r236)!=28:
        errors.append("expected 28 #236 inventory pages, got "+str(len(r236)))
    if any(r["source_status"]!="source-complete" for r in r236):
        errors.append("one or more #236 inventory rows are not source-complete")

    fk_rows=list(csv.DictReader((DBREF/"fk-coverage.csv").open(encoding="utf-8",newline="")))
    if len(fk_rows)!=cov.get("foreign_keys"):
        errors.append("fk-coverage.csv row count mismatch")
    if any(r["documented"]!="yes" for r in fk_rows):
        errors.append("undocumented FK in fk-coverage.csv")

    constraint_rows=list(csv.DictReader((DBREF/"constraint-coverage.csv").open(encoding="utf-8",newline="")))
    expected_constraints=cov.get("unique_constraints",0)+cov.get("check_constraints",0)+cov.get("explicit_indexes",0)
    if len(constraint_rows)!=expected_constraints:
        errors.append("constraint/index coverage row count mismatch")
    if any(r["documented"]!="yes" for r in constraint_rows):
        errors.append("undocumented constraint/index row")

    geography=(PAGES/"V2-Table-geography.md").read_text(encoding="utf-8")
    for phrase in ["geometry(Geometry,4326)","GiST","geography_geom_gix"]:
        if phrase not in geography:
            errors.append("geography page missing PostGIS detail "+phrase)

    report={
      "tables":cov.get("tables"),
      "table_pages":len(table_pages),
      "inventory_issue_236_pages":len(r236),
      "foreign_keys":cov.get("foreign_keys"),
      "foreign_keys_documented":len(fk_rows),
      "constraints_indexes_documented":len(constraint_rows),
      "erds":erd.get("erd_count"),
      "physical_tables":erd.get("physical_tables"),
      "physical_fk_edges":erd.get("physical_fk_edges"),
      "views":cov.get("views"),
      "errors":errors,
    }
    print(json.dumps(report,indent=2,sort_keys=True))
    if errors:
        raise SystemExit(1)

if __name__=="__main__":
    main()
