#!/usr/bin/env python3
import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

from db_schema_model import parse_schema

ROOT=Path(__file__).resolve().parents[2]
WIKI=ROOT/"wiki-src"
PAGES=WIKI/"pages"
DBREF=WIKI/"database-reference"
INVENTORY=WIKI/"page-inventory.csv"
AUTH_REF="v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999"

def code(value):
    q=chr(96)
    return q+str(value)+q

def wiki(page,label=None):
    return "[["+page+("|"+label if label else "")+"]]"

def titleize(name):
    return " ".join(x.capitalize() for x in name.split("_"))

def read_csv(path):
    with path.open(encoding="utf-8-sig",newline="") as fh:
        return list(csv.DictReader(fh))

def parse_views(text):
    import re
    out=[]
    pattern=re.compile(r"CREATE OR REPLACE VIEW\s+([A-Za-z0-9_]+)\s+AS\s+(.*?);",re.I|re.S)
    for m in pattern.finditer(text):
        name,sql=m.groups()
        refs=sorted(set(re.findall(r"\b(?:FROM|JOIN)\s+([A-Za-z0-9_]+)",sql,re.I)))
        out.append({"name":name,"tables":refs})
    return out

def mapping_by_table(rows):
    out=defaultdict(list)
    for row in rows:
        table=(row.get("rdb_table") or "").strip()
        if table:
            out[table].append(row)
    return out

def incoming_fks(tables):
    out=defaultdict(list)
    for table in tables.values():
        for fk in table["fks"]:
            out[fk["ref_table"]].append({
                "child":table["name"],
                "column":fk["column"],
                "ref_column":fk["ref_column"],
                "nullable":fk["nullable"],
            })
    return out

def synthetic_value(table,col):
    name=col["name"]
    typ=col["type"].upper()
    if col["fk"]:
        return "<"+col["fk"]["ref_table"]+"."+col["fk"]["ref_column"]+">"
    if name=="public_id":
        return "example:"+table+":001"
    if name=="ontology_iri":
        return "https://w3id.org/cm-pharme/2.0/Example"
    if "TIMESTAMP" in typ:
        return "2026-01-01T00:00:00Z"
    if typ.startswith("DATE"):
        return "2026-01-01"
    if "JSONB" in typ:
        return '{"example": true}'
    if "CHAR(64)" in typ:
        return "0"*64
    if "CHAR(2)" in typ:
        return "EX"
    if "CHAR(3)" in typ:
        return "EUR"
    if "NUMERIC" in typ:
        return "0.9500" if "confidence" in name else "1"
    if "BIGINT" in typ or "SERIAL" in typ or "INTEGER" in typ:
        return "101"
    if "GEOMETRY" in typ:
        return "POINT(0 0), SRID 4326"
    if name in {"preferred_name","canonical_name","name","title","label","scheme_name","release_label"}:
        return "Example "+titleize(name)
    samples={
        "source_role":"fixture",
        "status":"completed" if table=="transformation_run" else "accepted",
        "geography_type":"administrative_region",
        "observation_kind":"availability",
        "entity_type":"facility",
        "row_number":"1",
    }
    return samples.get(name,"example")

def important_columns(table):
    selected=[]
    preferred={
        "public_id","preferred_name","canonical_name","source_hash","status",
        "confidence","observation_kind","reporting_period","ontology_iri",
        "entity_type","matched_public_id","predicate_key","geography_type"
    }
    for col in table["columns"]:
        if col["pk"] or col["fk"] or col["name"] in preferred:
            selected.append(col)
    for col in table["columns"]:
        if col not in selected:
            selected.append(col)
        if len(selected)>=7:
            break
    return selected[:10]

def record(source,evidence):
    return """

---

<details>
<summary>Documentation record</summary>

- **Page scope:** V2
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative source:** %s
- **Last synchronized:** 2026-09-25
- **Last synchronized ref:** %s
- **Related issues/PRs:** #236, #237
- **Evidence status:** %s
- **Future refresh:** #212 / #213 / #214 as applicable
- **Wiki baseline:** WB-2026.09.1

</details>
""" % (source,AUTH_REF,evidence)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--authority-root",required=True)
    args=ap.parse_args()
    auth=Path(args.authority_root).resolve()

    schema_text=(auth/"v2/data/db/schema.sql").read_text(encoding="utf-8")
    tables,raw_counts,parsed_counts=parse_schema(schema_text)
    views=parse_views((auth/"v2/data/db/views.sql").read_text(encoding="utf-8"))
    mappings=read_csv(auth/"v2/data/mappings/ontology-rdb-mapping.csv")
    map_by=mapping_by_table(mappings)
    metadata=json.loads((DBREF/"table-metadata.json").read_text(encoding="utf-8"))
    meta=metadata["tables"]
    incoming=incoming_fks(tables)

    errors=[]
    if len(tables)!=24:
        errors.append("expected 24 tables, got "+str(len(tables)))
    if raw_counts!=parsed_counts:
        errors.append("raw/parsed schema count mismatch")
    if set(tables)!=set(meta):
        errors.append("table metadata set differs from schema table set")
    if errors:
        print(json.dumps({"errors":errors,"raw":raw_counts,"parsed":parsed_counts},indent=2))
        raise SystemExit(1)

    DBREF.mkdir(parents=True,exist_ok=True)
    rows236=[]
    page_name={name:"V2 Table "+name for name in tables}

    def add_page(name,slug,content):
        (PAGES/(slug+".md")).write_text(content.rstrip()+"\n",encoding="utf-8")
        rows236.append([name,slug,"Data / Database","V2","source-complete","pending-wiki-sync","236"])

    for name,table in tables.items():
        col_lines=["| Column | SQL type | Nullable | Key / constraint | Default |","|---|---|---|---|---|"]
        for col in table["columns"]:
            tags=[]
            if col["pk"]:
                tags.append("PK")
            if col["fk"]:
                tags.append("FK to "+col["fk"]["ref_table"]+"."+col["fk"]["ref_column"])
            if col["unique"]:
                tags.append("UNIQUE")
            for check in col["checks"]:
                tags.append("CHECK "+check)
            col_lines.append("| %s | %s | %s | %s | %s |"%(
                code(col["name"]),code(col["type"]),
                "YES" if col["nullable"] else "NO",
                "<br>".join(tags) if tags else "—",
                code(col["default"]) if col["default"] else "—"
            ))

        map_lines=["| Mapping | Ontology target | Kind | Status | RDB realization | Note |","|---|---|---|---|---|---|"]
        for row in map_by.get(name,[]):
            target=(row.get("ontology_iri") or "").rsplit("/",1)[-1] or "—"
            map_lines.append("| %s | %s | %s | %s | %s | %s |"%(
                code(row["mapping_id"]),code(target),row["entity_kind"],row["mapping_status"],
                code(row["rdb_field_or_join"]),row["representation_note"]
            ))

        fk_lines=["| FK column | References | Nullable |","|---|---|---|"]
        for fk in table["fks"]:
            fk_lines.append("| %s | %s | %s |"%(code(fk["column"]),code(fk["ref_table"]+"."+fk["ref_column"]),"YES" if fk["nullable"] else "NO"))

        incoming_lines=["| Referencing table | FK column | Nullable |","|---|---|---|"]
        for inc in incoming.get(name,[]):
            incoming_lines.append("| %s | %s | %s |"%(wiki(page_name[inc["child"]],inc["child"]),code(inc["column"]),"YES" if inc["nullable"] else "NO"))

        unique_lines=["- "+", ".join(code(x) for x in u) for u in table["uniques"]]
        check_lines=["- "+code(x) for x in table["checks"]]
        index_lines=[]
        for idx in table["indexes"]:
            text="**"+idx["name"]+"** — "+idx["method"]+" on "+code(idx["columns"])
            if idx["where"]:
                text+=" WHERE "+code(idx["where"])
            index_lines.append("- "+text)

        ex=["| Field | Synthetic value |","|---|---|"]
        for col in important_columns(table):
            ex.append("| %s | %s |"%(code(col["name"]),code(synthetic_value(name,col))))

        joins=[]
        for fk in table["fks"]:
            joins.append("- Child to parent: "+code(name+"."+fk["column"])+" = "+code(fk["ref_table"]+"."+fk["ref_column"])+".")
        for inc in incoming.get(name,[])[:5]:
            joins.append("- Parent from child: "+code(name+"."+inc["ref_column"])+" = "+code(inc["child"]+"."+inc["column"])+".")
        if not joins:
            joins=["- No physical FK join is declared for this table."]

        postgis=""
        if name=="geography":
            postgis="""
## PostGIS representation
The geom column uses geometry(Geometry,4326), with WGS 84 / EPSG:4326 as the declared spatial reference. The geography_geom_gix GiST index supports spatial access. Geometry presence does not establish geocoding accuracy or geographic completeness.
"""

        content="# "+name+"""

> **Version scope:** V2  
> **Status:** Reference implementation  
> **Updated:** 2026-09-25

This page documents one implemented PostgreSQL/PostGIS table. It describes a research/reference realization and does not claim production deployment.

## Purpose
"""+meta[name]["purpose"]+"""

## Provenance role
"""+meta[name]["provenance"]+"""

## Physical structure
"""+("\n".join(col_lines))+"""

## Primary key
"""+(", ".join(code(x) for x in table["pk"]))+"""

## Foreign keys
"""+("\n".join(fk_lines) if table["fks"] else "No outgoing foreign key is declared.")+"""

## Incoming references
"""+("\n".join(incoming_lines) if incoming.get(name) else "No implemented table references this table through a physical FK.")+"""

## UNIQUE constraints
"""+("\n".join(unique_lines) if unique_lines else "No additional UNIQUE constraint is declared.")+"""

## CHECK constraints
"""+("\n".join(check_lines) if check_lines else "No CHECK constraint is declared.")+"""

## Explicit indexes
"""+("\n".join(index_lines) if index_lines else "No explicit non-constraint index is declared.")+postgis+"""

## Ontology to RDB mapping
"""+("\n".join(map_lines) if map_by.get(name) else "No direct row in the current ontology-to-RDB registry targets this table. No mapping is inferred from the table name.")+"""

See [[V2 Ontology Reference]] for semantic definitions. This page does not redefine ontology meaning.

## Safe synthetic example
The following values are illustrative only and are not empirical records.

"""+("\n".join(ex))+"""

## Common join paths
"""+("\n".join(joins))+"""

## Boundaries
- Reference/research realization only.
- Fixture rows are deterministic test data, not population evidence.
- Relational convenience must not collapse protected ontology distinctions.
- Missing mappings remain explicit rather than inferred.

## Authoritative sources
- v2/data/db/schema.sql
- v2/data/mappings/ontology-rdb-mapping.csv
- v2/data/mappings/source-field-ontology-mapping.csv
"""
        content+=record("V2 PostgreSQL/PostGIS DDL and mapping registry","Generated physical reference with curated purpose/provenance note")
        add_page(page_name[name],"V2-Table-"+name.replace("_","-"),content)

    # Data dictionary
    dd=["# V2 Database Data Dictionary","","> **Version scope:** V2  ","> **Status:** Generated physical reference  ","> **Updated:** 2026-09-25","",
        "This dictionary is generated from the authoritative V2 schema. It describes the physical database representation, not the domain ontology.",""]
    for name,table in tables.items():
        dd+=["## "+name,"","| Column | SQL type | Nullable | PK | FK | UNIQUE | Default / CHECK |","|---|---|---|---|---|---|---|"]
        for col in table["columns"]:
            fk=col["fk"]["ref_table"]+"."+col["fk"]["ref_column"] if col["fk"] else "—"
            extra=[]
            if col["default"]:
                extra.append("DEFAULT "+col["default"])
            for ck in col["checks"]:
                extra.append("CHECK "+ck)
            dd.append("| %s | %s | %s | %s | %s | %s | %s |"%(
                code(col["name"]),code(col["type"]),"YES" if col["nullable"] else "NO",
                "YES" if col["pk"] else "NO",code(fk) if fk!="—" else "—",
                "YES" if col["unique"] else "NO",
                "<br>".join(code(x) for x in extra) if extra else "—"
            ))
        dd+=["","Detailed table semantics: "+wiki(page_name[name]),""]
    dd.append(record("v2/data/db/schema.sql","Generated field-level physical dictionary"))
    add_page("V2 Database Data Dictionary","V2-Database-Data-Dictionary","\n".join(dd))

    # Views
    vp=["# V2 Database Views","","> **Version scope:** V2  ","> **Status:** Reference implementation  ","> **Updated:** 2026-09-25","",
        "The V2 database defines "+str(len(views))+" research/query views in addition to the 24 base tables. Views are not included in the table count.",""]
    for view in views:
        links=[wiki(page_name[t],t) if t in page_name else code(t) for t in view["tables"]]
        vp+=["## "+view["name"],"","**Referenced tables:** "+", ".join(links)+".","",
             "This view is a query projection over implemented tables; it does not create new ontology semantics.",""]
    vp+=["## Authority","- v2/data/db/views.sql","- v2/data/db/schema.sql",""]
    vp.append(record("V2 SQL views and DDL","Query views documented separately from the 24-table count"))
    add_page("V2 Database Views","V2-Database-Views","\n".join(vp))

    # Master reference
    cat=["| Table | Purpose | PK | FKs | UNIQUE | CHECK | Indexes | Mapping rows |","|---|---|---|---:|---:|---:|---:|---:|"]
    for name,table in tables.items():
        cat.append("| %s | %s | %s | %d | %d | %d | %d | %d |"%(
            wiki(page_name[name],name),meta[name]["purpose"],", ".join(code(x) for x in table["pk"]),
            len(table["fks"]),len(table["uniques"]),len(table["checks"]),len(table["indexes"]),len(map_by.get(name,[]))
        ))

    master="# V2 Database Reference\n\n"
    master+="> **Version scope:** V2  \n> **Status:** Stable-to-date / Reference implementation  \n> **Updated:** 2026-09-25\n\n"
    master+="This is the master reference for the implemented CM-PharmE V2 PostgreSQL/PostGIS research database.\n\n"
    master+="## Scope and authority\n"
    master+="- authoritative DDL: "+code("v2/data/db/schema.sql")+"\n"
    master+="- authoritative query views: "+code("v2/data/db/views.sql")+"\n"
    master+="- ontology-to-RDB registry: "+code("v2/data/mappings/ontology-rdb-mapping.csv")+"\n"
    master+="- source-field registry: "+code("v2/data/mappings/source-field-ontology-mapping.csv")+"\n"
    master+="- checked ref: "+code(AUTH_REF)+"\n\n"
    master+="The ontology remains semantic authority. The database is an implementation representation, not a replacement conceptual model.\n\n"
    master+="## Current physical baseline\n"
    master+="- base tables: **"+str(len(tables))+"**\n"
    master+="- query views: **"+str(len(views))+"**\n"
    master+="- primary keys: **"+str(parsed_counts["primary_keys"])+"**\n"
    master+="- foreign keys: **"+str(parsed_counts["foreign_keys"])+"**\n"
    master+="- UNIQUE constraints: **"+str(parsed_counts["unique_constraints"])+"**\n"
    master+="- CHECK constraints: **"+str(parsed_counts["check_constraints"])+"**\n"
    master+="- explicit indexes: **"+str(parsed_counts["indexes"])+"**\n"
    master+="- PostGIS extension: enabled in DDL\n"
    master+="- spatial column: "+code("geography.geom geometry(Geometry,4326)")+"\n\n"
    master+="## Navigation\n- "+wiki("V2 Database ERD Suite")+"\n- "+wiki("V2 Database Data Dictionary")+"\n- "+wiki("V2 Database Views")+"\n- "+wiki("V2 Data Infrastructure")+"\n- "+wiki("V2 Ontology Reference")+"\n\n"
    master+="## Table catalog\n"+("\n".join(cat))+"\n\n"
    master+="## PostgreSQL and PostGIS notes\nThe reference implementation uses PostgreSQL-specific BIGSERIAL, TIMESTAMPTZ, JSONB, partial indexes and PostGIS geometry. The GiST spatial index on geography supports spatial access. These choices do not establish production scalability, geocoding accuracy or operational service levels.\n\n"
    master+="## Provenance model\nDataset to DatasetRelease to SourceRecord is the primary lineage chain, with optional TransformationRun provenance. EvidenceSupport connects SourceRecord to Assertion. ObservationResult requires SourceRecord and Assertion references. EntityMatchAssertion retains both source-record endpoints.\n\n"
    master+="## Identity model\nIdentifierScheme and IdentifierAssignment keep lexical identifiers separate from entity identity. EntityMatchAssertion stores method, confidence and disposition rather than silently merging source records.\n\n"
    master+="## Protected distinctions preserved\n- Organization is not Facility.\n- Geography is not Regulatory Jurisdiction.\n- Medicinal Product, Pharmaceutical Substance and Product Presentation remain distinct.\n- Observation Result is not Source Record.\n- Identifier assignment/value is not entity identity.\n\n"
    master+="## Production boundary\nThe database is a reference/research realization. Deterministic fixtures do not demonstrate full-source ingestion, production deployment, real-world entity-resolution accuracy, global coverage or operational scalability.\n"
    master+=record("V2 data infrastructure and PostgreSQL/PostGIS DDL","Complete 24-table reference; ERD suite generated separately")
    add_page("V2 Database Reference","V2-Database-Reference",master)

    # Coverage artifacts
    fk_rows=[]
    constraints=[]
    for name,table in tables.items():
        for fk in table["fks"]:
            fk_rows.append({"table":name,"column":fk["column"],"ref_table":fk["ref_table"],"ref_column":fk["ref_column"],"nullable":fk["nullable"],"documented":"yes"})
        for unique in table["uniques"]:
            constraints.append({"table":name,"kind":"UNIQUE","definition":", ".join(unique),"documented":"yes"})
        for check in table["checks"]:
            constraints.append({"table":name,"kind":"CHECK","definition":check,"documented":"yes"})
        for idx in table["indexes"]:
            definition=idx["name"]+" "+idx["method"]+"("+idx["columns"]+")"
            if idx["where"]:
                definition+=" WHERE "+idx["where"]
            constraints.append({"table":name,"kind":"INDEX","definition":definition,"documented":"yes"})

    with (DBREF/"fk-coverage.csv").open("w",encoding="utf-8",newline="") as fh:
        w=csv.DictWriter(fh,fieldnames=["table","column","ref_table","ref_column","nullable","documented"])
        w.writeheader(); w.writerows(fk_rows)
    with (DBREF/"constraint-coverage.csv").open("w",encoding="utf-8",newline="") as fh:
        w=csv.DictWriter(fh,fieldnames=["table","kind","definition","documented"])
        w.writeheader(); w.writerows(constraints)

    coverage={
        "issue":236,
        "authority_ref":AUTH_REF,
        "tables":len(tables),
        "table_pages":len(tables),
        "views":len(views),
        "primary_keys":parsed_counts["primary_keys"],
        "foreign_keys":parsed_counts["foreign_keys"],
        "foreign_keys_documented":len(fk_rows),
        "unique_constraints":parsed_counts["unique_constraints"],
        "check_constraints":parsed_counts["check_constraints"],
        "explicit_indexes":parsed_counts["indexes"],
        "constraint_index_records_documented":len(constraints),
        "postgis_extension":parsed_counts["postgis_extensions"],
        "mapped_tables":len(map_by),
        "tables_without_mapping_rows":sorted(set(tables)-set(map_by)),
        "page_count_before_erd_suite":len(rows236),
        "errors":[]
    }
    (DBREF/"coverage.json").write_text(json.dumps(coverage,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    lines=["# V2 database documentation structural coverage","",
           "**PASS — all 24 implemented base tables are represented in the generated table reference and field dictionary.**","",
           "- tables: **24/24**",
           "- primary keys: **%d/%d**"%(parsed_counts["primary_keys"],parsed_counts["primary_keys"]),
           "- foreign keys: **%d/%d**"%(len(fk_rows),parsed_counts["foreign_keys"]),
           "- UNIQUE constraints documented: **%d**"%parsed_counts["unique_constraints"],
           "- CHECK constraints documented: **%d**"%parsed_counts["check_constraints"],
           "- explicit indexes documented: **%d**"%parsed_counts["indexes"],
           "- query views documented separately: **%d**"%len(views),
           "- PostGIS extension and geography geometry/GiST behavior documented.","",
           "Structural coverage does not imply production readiness or complete ontology mapping."]
    (DBREF/"COVERAGE.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

    # Inventory: replace #236 rows.
    with INVENTORY.open(encoding="utf-8-sig",newline="") as fh:
        all_rows=list(csv.reader(fh))
    header=all_rows[0]
    kept=[header]+[row for row in all_rows[1:] if len(row)<7 or row[6]!="236"]
    with INVENTORY.open("w",encoding="utf-8",newline="") as fh:
        csv.writer(fh).writerows(kept+rows236)

    # Navigation.
    home=PAGES/"Home.md"
    text=home.read_text(encoding="utf-8")
    link="- **Explore the V2 database reference:** [[V2 Database Reference]]\n"
    if link not in text:
        anchor="- **Open the exhaustive V2 ontology reference:** [[V2 Ontology Reference]]\n"
        text=text.replace(anchor,anchor+link) if anchor in text else text+"\n"+link
        home.write_text(text,encoding="utf-8")

    infra=PAGES/"V2-Data-Infrastructure.md"
    text=infra.read_text(encoding="utf-8")
    if "[[V2 Database Reference]]" not in text:
        insert="## Database documentation\n- [[V2 Database Reference]] — complete 24-table reference.\n- [[V2 Database ERD Suite]] — logical, physical and subject-area ERDs.\n- [[V2 Database Data Dictionary]] — field-level physical dictionary.\n- [[V2 Database Views]] — research/query views.\n\n"
        text=text.replace("## Representation architecture",insert+"## Representation architecture")
        text=text.replace("> **Updated:** 2026-09-23","> **Updated:** 2026-09-25")
        infra.write_text(text,encoding="utf-8")

    sidebar=PAGES/"_Sidebar.md"
    text=sidebar.read_text(encoding="utf-8")
    if "[[V2 Database Reference]]" not in text:
        text+="\n**Data & Database**\n- [[V2 Database Reference]]\n- [[V2 Database ERD Suite]]\n- [[V2 Database Data Dictionary]]\n"
        sidebar.write_text(text,encoding="utf-8")

    print(json.dumps(coverage,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
