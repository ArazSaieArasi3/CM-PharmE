#!/usr/bin/env python3
import argparse, csv, html, json, re, textwrap
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
WIKI=ROOT/"wiki-src"
PAGES=WIKI/"pages"
DIAG=WIKI/"diagrams"
INVENTORY=WIKI/"page-inventory.csv"
BT=chr(96)

AUTH_REF="v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999"
EXPECTED_TABLES=24

PURPOSES={
"dataset":"Registered dataset identity and source-level metadata used by the reproducible ingestion/provenance layer.",
"dataset_release":"Version/release identity for a dataset, including source filename and retrieval time.",
"transformation_run":"Auditable transformation/provenance activity for an adapter execution.",
"source_record":"Row-level source evidence with deterministic hash and transformation lineage.",
"geography":"Canonical geographic entity table with optional PostGIS geometry and supported geography subtype.",
"geography_alias":"Source-specific geographic names/codes and auditable normalization/resolution confidence.",
"regulatory_jurisdiction":"Regulatory jurisdiction identity kept explicitly separate from physical geography.",
"organization":"Canonical organization identity used by ecosystem and facility-operation relations.",
"facility":"Canonical physical/operational facility identity with optional geographic location.",
"facility_operation":"Associative/relator realization connecting Organization and Facility with validity dates.",
"pharmaceutical_substance":"Canonical pharmaceutical substance identity.",
"medicinal_product":"Canonical medicinal-product identity with a bounded primary-substance hook.",
"product_presentation":"Presentation/package-level medicinal-product identity and packaging/concentration fields.",
"identifier_scheme":"Identifier-scheme identity kept separate from identifier lexical values.",
"identifier_assignment":"Auditable assignment of an identifier value/scheme to a supported entity type.",
"product_classification_scheme":"Classification-scheme identity such as ATC or another product classification system.",
"classification_entry":"Code/label entry within a product classification scheme.",
"product_classification_assignment":"Associative mapping between a medicinal product and a classification entry, with provenance hook.",
"diagnosis_reference":"Diagnosis-classification reference used by market-access/observation data.",
"assertion":"Canonical assertion target for evidence/provenance linkage.",
"evidence_support":"Relator/associative evidence link from SourceRecord to Assertion.",
"observation_result":"Polymorphic aggregate observation-result realization covering selected implemented observation kinds and measures.",
"entity_match_assertion":"Auditable entity-matching decision between two source records, including method, confidence and status.",
"medicine_shortage_situation":"Contextual medicine-shortage situation with optional product/presentation/jurisdiction/source evidence links."
}

PROVENANCE_ROLES={
"dataset":"root source identity",
"dataset_release":"versioned source provenance",
"transformation_run":"transformation activity provenance",
"source_record":"row-level provenance anchor",
"geography_alias":"normalization evidence via source_record_id",
"identifier_assignment":"identifier provenance via source_record_id",
"product_classification_assignment":"classification provenance via source_record_id",
"evidence_support":"evidence-to-assertion provenance bridge",
"observation_result":"observation provenance via source_record_id + assertion_id",
"entity_match_assertion":"matching provenance across two source records",
"medicine_shortage_situation":"shortage evidence via source_record_id"
}

SUBJECTS={
"provenance-ingestion":{
 "title":"Dataset, Release, Source and Transformation",
 "tables":["dataset","dataset_release","transformation_run","source_record"],
 "purpose":"Show the source-ingestion and execution-provenance backbone."
},
"organization-place":{
 "title":"Organization, Facility, Geography and Jurisdiction",
 "tables":["geography","geography_alias","regulatory_jurisdiction","organization","facility","facility_operation"],
 "purpose":"Show organization/facility identities, geographic normalization and regulatory-jurisdiction separation."
},
"product-classification":{
 "title":"Product, Substance, Presentation and Classification",
 "tables":["pharmaceutical_substance","medicinal_product","product_presentation","product_classification_scheme","classification_entry","product_classification_assignment"],
 "purpose":"Show product/substance/presentation identity and product-classification realization."
},
"identity-match":{
 "title":"Identifier, Identity and Entity Match",
 "tables":["identifier_scheme","identifier_assignment","entity_match_assertion","source_record"],
 "purpose":"Show identifier assignment and auditable entity matching without collapsing identifier values into entity identity."
},
"evidence-provenance":{
 "title":"Assertion, Evidence and Provenance",
 "tables":["dataset","dataset_release","transformation_run","source_record","assertion","evidence_support"],
 "purpose":"Show traceability from dataset/release/source row and transformation activity to assertions/evidence support."
},
"observation":{
 "title":"Observation",
 "tables":["observation_result","product_presentation","facility","geography","diagnosis_reference","source_record","assertion"],
 "purpose":"Show the implemented observation aggregate and its contextual/provenance foreign keys."
},
"shortage-resilience":{
 "title":"Shortage and Implemented Resilience-Related Data",
 "tables":["medicine_shortage_situation","medicinal_product","product_presentation","regulatory_jurisdiction","source_record"],
 "purpose":"Show the implemented shortage realization. Dedicated SupplyDependency, Vulnerability and risk-treatment tables are not present in the current schema."
}
}

def code(x): return BT+str(x)+BT

def extract_create_blocks(sql):
    out=[]
    pat=re.compile(r"CREATE TABLE\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(",re.I)
    for m in pat.finditer(sql):
        name=m.group(1)
        open_pos=sql.find("(",m.start())
        depth=0; quote=None; i=open_pos
        while i<len(sql):
            ch=sql[i]
            if quote:
                if ch==quote and (i==0 or sql[i-1]!="\\"):
                    quote=None
            else:
                if ch in ("'",'"'): quote=ch
                elif ch=="(": depth+=1
                elif ch==")":
                    depth-=1
                    if depth==0:
                        out.append((name,sql[open_pos+1:i],m.start(),i+1)); break
            i+=1
    return out

def split_top_level(text):
    parts=[]; start=0; depth=0; quote=None
    for i,ch in enumerate(text):
        if quote:
            if ch==quote and (i==0 or text[i-1]!="\\"): quote=None
        else:
            if ch in ("'",'"'): quote=ch
            elif ch=="(": depth+=1
            elif ch==")": depth-=1
            elif ch=="," and depth==0:
                parts.append(text[start:i].strip()); start=i+1
    tail=text[start:].strip()
    if tail: parts.append(tail)
    return parts

def parse_schema(sql):
    tables={}
    for name,body,_,_ in extract_create_blocks(sql):
        cols=[]; table_unique=[]; table_checks=[]
        for item in split_top_level(body):
            clean=" ".join(item.split())
            up=clean.upper()
            if up.startswith("UNIQUE"):
                mm=re.search(r"UNIQUE\s*\(([^)]+)\)",clean,re.I)
                if mm: table_unique.append([x.strip() for x in mm.group(1).split(",")])
                continue
            if up.startswith("CHECK"):
                mm=re.search(r"CHECK\s*\((.*)\)\s*$",clean,re.I|re.S)
                if mm: table_checks.append(mm.group(1).strip())
                continue
            mm=re.match(r"([A-Za-z_][A-Za-z0-9_]*)\s+(.+)$",clean)
            if not mm: continue
            col,rest=mm.groups()
            marker=re.search(r"\s+(PRIMARY KEY|NOT NULL|UNIQUE|REFERENCES|DEFAULT|CHECK)\b",rest,re.I)
            ctype=(rest[:marker.start()] if marker else rest).strip()
            pk=bool(re.search(r"\bPRIMARY KEY\b",rest,re.I))
            notnull=bool(re.search(r"\bNOT NULL\b",rest,re.I)) or pk
            unique=bool(re.search(r"\bUNIQUE\b",rest,re.I))
            fk=None
            fm=re.search(r"\bREFERENCES\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]+)\)",rest,re.I)
            if fm: fk={"table":fm.group(1),"column":fm.group(2).strip()}
            default=None
            dm=re.search(r"\bDEFAULT\s+(.+?)(?=\s+(?:CHECK|REFERENCES|UNIQUE|NOT NULL|PRIMARY KEY)\b|$)",rest,re.I)
            if dm: default=dm.group(1).strip()
            inline_check=None
            cm=re.search(r"\bCHECK\s*\((.*)\)\s*$",rest,re.I|re.S)
            if cm: inline_check=cm.group(1).strip()
            cols.append({"name":col,"type":ctype,"pk":pk,"not_null":notnull,"unique":unique,"fk":fk,"default":default,"check":inline_check})
        tables[name]={"name":name,"columns":cols,"unique":table_unique,"checks":table_checks,"indexes":[]}
    idx_pat=re.compile(r"CREATE INDEX\s+([A-Za-z_][A-Za-z0-9_]*)\s+ON\s+([A-Za-z_][A-Za-z0-9_]*)\s*(?:USING\s+([A-Za-z]+)\s*)?\(([^)]+)\)(?:\s+WHERE\s+([^;]+))?\s*;",re.I)
    for m in idx_pat.finditer(sql):
        idx={"name":m.group(1),"method":m.group(3) or "btree(default)","columns":m.group(4).strip(),"where":m.group(5).strip() if m.group(5) else None}
        if m.group(2) in tables: tables[m.group(2)]["indexes"].append(idx)
    return tables

def parse_views(sql):
    out=[]
    pat=re.compile(r"CREATE OR REPLACE VIEW\s+([A-Za-z_][A-Za-z0-9_]*)\s+AS\s+(.*?);",re.I|re.S)
    for m in pat.finditer(sql):
        q=" ".join(m.group(2).split())
        refs=sorted(set(re.findall(r"\b(?:FROM|JOIN)\s+([A-Za-z_][A-Za-z0-9_]*)",q,re.I)))
        out.append({"name":m.group(1),"tables":refs,"query":q})
    return out

def parse_mapping(path):
    rows=list(csv.DictReader(path.open(encoding="utf-8",newline="")))
    by_table=defaultdict(list)
    for r in rows:
        t=(r.get("rdb_table") or "").strip()
        if t: by_table[t].append(r)
    return rows,by_table

def fk_list(tables):
    out=[]
    for t,meta in tables.items():
        for c in meta["columns"]:
            if c["fk"]:
                out.append({
                  "child_table":t,"child_column":c["name"],
                  "parent_table":c["fk"]["table"],"parent_column":c["fk"]["column"],
                  "nullable":not c["not_null"],
                  "cardinality":"0..1 parent / 0..* children" if not c["not_null"] else "1 parent / 0..* children"
                })
    return out

def synthetic_value(table,col):
    n=col["name"]; typ=col["type"].lower()
    if col["pk"] or n.endswith("_id") and ("bigserial" in typ or "bigint" in typ): return "1001"
    if n=="public_id": return "syn-"+table.replace("_","-")+"-001"
    if n=="ontology_iri": return "https://w3id.org/cm-pharme/2.0/Example"
    if "timestamp" in typ: return "2026-01-15T10:00:00Z"
    if typ=="date": return "2026-01-15"
    if "jsonb" in typ: return '{"synthetic": true}'
    if "geometry" in typ: return "POINT(8.68 50.11) [synthetic]"
    if "numeric" in typ: return "1.0"
    if "bigint" in typ or "integer" in typ: return "1001"
    if "char(64)" in typ: return "0000000000000000000000000000000000000000000000000000000000000000"
    if "char(2)" in typ: return "ZZ"
    if "char(3)" in typ: return "XXX"
    if "text" in typ:
        choices={
          "source_role":"fixture","status":"accepted" if table=="entity_match_assertion" else "completed",
          "geography_type":"other","entity_type":"organization","observation_kind":"availability"
        }
        return choices.get(n,"synthetic-"+n.replace("_","-"))
    return "synthetic-value"

def ontology_links(rows):
    return [(r["ontology_iri"],r["entity_kind"],r["mapping_status"],r["rdb_field_or_join"],r["representation_note"]) for r in rows]

def puml_table(table):
    lines=[f'entity "{table["name"]}" as {table["name"]} {{']
    for c in table["columns"]:
        marks=[]
        if c["pk"]: marks.append("PK")
        if c["fk"]: marks.append("FK")
        suffix=(" ["+",".join(marks)+"]") if marks else ""
        lines.append(f'  {c["name"]} : {c["type"]}{suffix}')
    lines.append("}")
    return lines

def mermaid_erd(name,tables,selected=None):
    selected=set(selected or tables.keys())
    lines=["erDiagram"]
    for t in selected:
        if t not in tables: continue
        for c in tables[t]["columns"]:
            if c["fk"] and c["fk"]["table"] in selected:
                parent=c["fk"]["table"]; child=t
                lhs="o|" if not c["not_null"] else "||"
                lines.append(f'    {parent} {lhs}--o{{ {child} : "{c["name"]}"')
    for t in selected:
        if t not in tables: continue
        lines.append(f"    {t} {{")
        for c in tables[t]["columns"]:
            typ=re.sub(r"[^A-Za-z0-9_]","_",c["type"])
            key=" PK" if c["pk"] else (" FK" if c["fk"] else "")
            lines.append(f"      {typ} {c['name']}{key}")
        lines.append("    }")
    return "\n".join(lines)+"\n"

def svg_erd(diagram_id,title,purpose,tables,selected=None,physical=True):
    selected=[t for t in (selected or list(tables)) if t in tables]
    cols=4 if len(selected)>12 else (3 if len(selected)>6 else 2)
    boxw=310
    colgap=55
    margin=35
    positions={}
    heights={}
    for i,t in enumerate(selected):
        rows=len(tables[t]["columns"]) if physical else min(4,len(tables[t]["columns"]))
        heights[t]=70+rows*18
    grid_rows=(len(selected)+cols-1)//cols
    row_max=[]
    for r in range(grid_rows):
        names=selected[r*cols:(r+1)*cols]
        row_max.append(max([heights[n] for n in names] or [100])+70)
    ystarts=[]; y=100
    for h in row_max: ystarts.append(y); y+=h
    width=margin*2+cols*boxw+(cols-1)*colgap
    height=y+100
    for i,t in enumerate(selected):
        r=i//cols; c=i%cols
        positions[t]=(margin+c*(boxw+colgap),ystarts[r])

    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
         f'<title id="title">{html.escape(diagram_id+" "+title)}</title>',
         f'<desc id="desc">{html.escape(purpose)}</desc>',
         '<defs><marker id="fk" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z"/></marker><style>text{font-family:sans-serif}.box{fill:white;stroke:currentColor}.fk{stroke-dasharray:4 3}.head{font-weight:bold}</style></defs>']
    # edges first using centers/boundaries
    for child in selected:
        for c in tables[child]["columns"]:
            if not c["fk"] or c["fk"]["table"] not in positions: continue
            parent=c["fk"]["table"]
            cx,cy=positions[child]; px,py=positions[parent]
            ccenter=(cx+boxw/2,cy+heights[child]/2); pcenter=(px+boxw/2,py+heights[parent]/2)
            dx=pcenter[0]-ccenter[0]; dy=pcenter[1]-ccenter[1]
            if abs(dx)>=abs(dy):
                x1=cx+(boxw if dx>0 else 0); y1=ccenter[1]
                x2=px+(0 if dx>0 else boxw); y2=pcenter[1]
            else:
                x1=ccenter[0]; y1=cy+(heights[child] if dy>0 else 0)
                x2=pcenter[0]; y2=py+(0 if dy>0 else heights[parent])
            out.append(f'<line class="fk" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="currentColor" marker-end="url(#fk)"/>')
            mx=(x1+x2)/2; my=(y1+y2)/2-4
            card="0..1 → 1" if not c["not_null"] else "1 → 1"
            out.append(f'<text x="{mx}" y="{my}" text-anchor="middle" font-size="9">{html.escape(c["name"]+" · "+card)}</text>')
    # boxes
    for t in selected:
        x,y=positions[t]; h=heights[t]
        out.append(f'<rect class="box" x="{x}" y="{y}" width="{boxw}" height="{h}" rx="6"/>')
        out.append(f'<text class="head" x="{x+boxw/2}" y="{y+22}" text-anchor="middle" font-size="14">{html.escape(t)}</text>')
        out.append(f'<line x1="{x}" y1="{y+34}" x2="{x+boxw}" y2="{y+34}" stroke="currentColor"/>')
        cols_to_show=tables[t]["columns"] if physical else tables[t]["columns"][:4]
        for j,c in enumerate(cols_to_show):
            marks=[]
            if c["pk"]: marks.append("PK")
            if c["fk"]: marks.append("FK")
            label=("["+"/".join(marks)+"] " if marks else "")+c["name"]+" : "+c["type"]
            if len(label)>43: label=label[:40]+"..."
            out.append(f'<text x="{x+10}" y="{y+54+j*18}" font-size="10">{html.escape(label)}</text>')
    out.append(f'<text x="{margin}" y="{height-45}" font-size="10">Crow&apos;s-foot semantics are expressed by FK direction/cardinality labels: each child FK points to its parent; nullable FKs permit 0..1 parent. Parent-side child multiplicity is 0..* unless constrained otherwise.</text>')
    out.append('</svg>')
    return "\n".join(out)+"\n"

def wiki_record(authority,evidence):
    return f"""
---

<details>
<summary>Documentation record</summary>

- **Page scope:** V2
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative source:** {authority}
- **Last synchronized:** 2026-09-24
- **Last synchronized ref:** {AUTH_REF}
- **Related issues/PRs:** #205, #236
- **Evidence status:** {evidence}
- **Future refresh:** Re-run after authoritative schema changes
- **Wiki baseline:** WB-2026.09.1

</details>
"""

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--authority-root",required=True)
    args=ap.parse_args()
    auth=Path(args.authority_root).resolve()
    schema_path=auth/"v2/data/db/schema.sql"
    views_path=auth/"v2/data/db/views.sql"
    mapping_path=auth/"v2/data/mappings/ontology-rdb-mapping.csv"
    sql=schema_path.read_text(encoding="utf-8")
    vsql=views_path.read_text(encoding="utf-8")
    tables=parse_schema(sql)
    views=parse_views(vsql)
    mapping_rows,mapping_by_table=parse_mapping(mapping_path)
    fks=fk_list(tables)

    errors=[]
    if len(tables)!=EXPECTED_TABLES: errors.append(f"expected {EXPECTED_TABLES} tables got {len(tables)}")
    if not re.search(r"CREATE EXTENSION IF NOT EXISTS postgis",sql,re.I): errors.append("PostGIS extension declaration missing")
    for fk in fks:
        if fk["parent_table"] not in tables: errors.append("FK target missing: "+repr(fk))
        else:
            parent_cols={c["name"] for c in tables[fk["parent_table"]]["columns"]}
            if fk["parent_column"] not in parent_cols: errors.append("FK target column missing: "+repr(fk))
    if errors:
        print(json.dumps({"errors":errors},indent=2)); raise SystemExit(1)

    total_columns=sum(len(x["columns"]) for x in tables.values())
    checks=[]
    unique=[]
    indexes=[]
    postgis=[]
    for t,meta in tables.items():
        for c in meta["columns"]:
            if c["check"]: checks.append({"table":t,"scope":"column","expression":c["check"]})
            if c["unique"]: unique.append({"table":t,"columns":[c["name"]],"scope":"column"})
            if "geometry" in c["type"].lower(): postgis.append({"table":t,"column":c["name"],"type":c["type"]})
        for x in meta["checks"]: checks.append({"table":t,"scope":"table","expression":x})
        for x in meta["unique"]: unique.append({"table":t,"columns":x,"scope":"table"})
        for x in meta["indexes"]: indexes.append({"table":t,**x})

    # Field dictionary.
    outdir=WIKI/"database-reference"
    outdir.mkdir(parents=True,exist_ok=True)
    with (outdir/"field-dictionary.csv").open("w",encoding="utf-8",newline="") as fh:
        cols=["table","column","type","primary_key","foreign_key","nullable","unique","default","check","ontology_mapping"]
        w=csv.DictWriter(fh,fieldnames=cols);w.writeheader()
        for t,meta in tables.items():
            maps="; ".join(sorted({r["ontology_iri"] for r in mapping_by_table.get(t,[])}))
            for c in meta["columns"]:
                fk=(c["fk"]["table"]+"."+c["fk"]["column"]) if c["fk"] else ""
                w.writerow({"table":t,"column":c["name"],"type":c["type"],"primary_key":c["pk"],"foreign_key":fk,
                            "nullable":not c["not_null"],"unique":c["unique"],"default":c["default"] or "",
                            "check":c["check"] or "","ontology_mapping":maps})
    with (outdir/"fk-coverage.csv").open("w",encoding="utf-8",newline="") as fh:
        w=csv.DictWriter(fh,fieldnames=["child_table","child_column","parent_table","parent_column","nullable","cardinality"])
        w.writeheader();w.writerows(fks)
    with (outdir/"constraint-coverage.csv").open("w",encoding="utf-8",newline="") as fh:
        w=csv.writer(fh);w.writerow(["kind","table","detail"])
        for x in checks:w.writerow(["CHECK",x["table"],x["expression"]])
        for x in unique:w.writerow(["UNIQUE",x["table"],", ".join(x["columns"])])
        for x in indexes:w.writerow(["INDEX",x["table"],x["name"]+" / "+x["method"]+" / "+x["columns"]+(" WHERE "+x["where"] if x["where"] else "")])
        for x in postgis:w.writerow(["POSTGIS",x["table"],x["column"]+" / "+x["type"]])

    catalog={
      "issue":236,"authority_ref":AUTH_REF,
      "schema_sha256_note":"Git blob/source ref is authoritative; publication tooling records Git refs rather than inventing a content digest here.",
      "table_count":len(tables),"column_count":total_columns,"foreign_key_count":len(fks),
      "check_count":len(checks),"unique_constraint_count":len(unique),
      "explicit_index_count":len(indexes),"view_count":len(views),
      "postgis_enabled":True,"geometry_columns":postgis,
      "tables":tables,"views":views,"errors":[]
    }
    (outdir/"schema-catalog.json").write_text(json.dumps(catalog,indent=2,sort_keys=True)+"\n",encoding="utf-8")

    # Table pages and inventory rows.
    page_rows=[]
    table_names={}
    for t in tables:
        table_names[t]="V2 DB Table "+t

    for t,meta in tables.items():
        maprows=mapping_by_table.get(t,[])
        col_lines=["| Column | Type | Null? | Key / constraint | Default |","|---|---|---|---|---|"]
        for c in meta["columns"]:
            tags=[]
            if c["pk"]: tags.append("PK")
            if c["fk"]: tags.append("FK → "+c["fk"]["table"]+"."+c["fk"]["column"])
            if c["unique"]: tags.append("UNIQUE")
            if c["check"]: tags.append("CHECK")
            col_lines.append("| %s | %s | %s | %s | %s |"%(
              code(c["name"]),code(c["type"]),"No" if c["not_null"] else "Yes","; ".join(tags) or "—",code(c["default"]) if c["default"] else "—"))
        cons=[]
        for u in meta["unique"]: cons.append("UNIQUE ("+", ".join(u)+")")
        for q in meta["checks"]: cons.append("CHECK ("+q+")")
        for c in meta["columns"]:
            if c["check"]: cons.append("CHECK "+c["name"]+" ("+c["check"]+")")
        idx_lines=["| Index | Method | Columns | Predicate |","|---|---|---|---|"]
        for ix in meta["indexes"]:
            idx_lines.append("| %s | %s | %s | %s |"%(code(ix["name"]),ix["method"],code(ix["columns"]),code(ix["where"]) if ix["where"] else "—"))
        map_lines=["| Ontology IRI | Kind | Status | RDB field/join | Representation note |","|---|---|---|---|---|"]
        for r in maprows:
            map_lines.append("| %s | %s | %s | %s | %s |"%(code(r["ontology_iri"]),r["entity_kind"],r["mapping_status"],code(r["rdb_field_or_join"]),r["representation_note"]))
        join_lines=[]
        for c in meta["columns"]:
            if c["fk"]:
                join_lines.append("- "+code(t+"."+c["name"])+" → "+code(c["fk"]["table"]+"."+c["fk"]["column"]))
        example={c["name"]:synthetic_value(t,c) for c in meta["columns"][:min(8,len(meta["columns"]))]}
        page=f"""# {t}

> **Version scope:** V2  
> **Status:** Reference implementation / Stable-to-date  
> **Updated:** 2026-09-24

> Generated physical-table reference from the authoritative PostgreSQL/PostGIS schema. It documents a research/reference realization and does **not** imply production deployment or production-scale performance.

## Purpose
{PURPOSES.get(t,"Reference-schema table in the V2 relational realization.")}

## Keys and structure
- **Primary key:** {', '.join(code(c['name']) for c in meta['columns'] if c['pk'])}
- **Foreign keys:** {sum(1 for c in meta['columns'] if c['fk'])}
- **Provenance role:** {PROVENANCE_ROLES.get(t,'No dedicated provenance role; provenance is reached through documented foreign-key paths where applicable.')}

## Columns
{chr(10).join(col_lines)}

## Table-level constraints
{chr(10).join('- '+code(x) for x in cons) if cons else 'No table-level UNIQUE/CHECK constraint beyond column-level key/nullability declarations.'}

## Explicit indexes
{chr(10).join(idx_lines) if meta['indexes'] else 'No explicit non-constraint index is declared for this table in the current schema.'}

## Ontology alignment
{chr(10).join(map_lines) if maprows else 'No direct row is currently registered for this table in the ontology↔RDB mapping registry. This absence must not be repaired by guessing.'}

See [[V2 Ontology Reference]] for semantic definitions. Mapping authority remains {code('v2/data/mappings/ontology-rdb-mapping.csv')}.

## Common joins
{chr(10).join(join_lines) if join_lines else 'No outgoing foreign-key join is declared from this table.'}

## Safe synthetic row fragment
{code(json.dumps(example,ensure_ascii=False))}

This example is synthetic and exists only to clarify field shape.

## Boundaries
- This table belongs to a reproducible **reference implementation**, not a production claim.
- Relational representation may be direct, bounded, polymorphic, relational-projection or deferred as stated in the mapping registry.
- The table definition does not redefine ontology semantics.
"""
        if t=="geography":
            page+=f"""
## PostGIS note
{code('geom')} is declared as {code('geometry(Geometry,4326)')}. SRID 4326 identifies the coordinate reference system. A GiST index {code('geography_geom_gix')} supports spatial access. The generic Geometry type does not imply that every row contains the same geometry subtype or that geospatial completeness is established.
"""
        page+=wiki_record("v2/data/db/schema.sql + ontology↔RDB mapping registry","Generated table reference; reference-implementation boundary preserved")
        slug="V2-DB-Table-"+t
        (PAGES/(slug+".md")).write_text(page,encoding="utf-8")
        page_rows.append([table_names[t],slug,"Reference / Data Model","V2","source-complete","pending-wiki-sync","236"])

    # Main database reference page.
    tlines=["| Table | Purpose | Columns | FKs | Ontology mapping |","|---|---|---:|---:|---|"]
    for t,meta in tables.items():
        maps=mapping_by_table.get(t,[])
        mapped=", ".join(sorted({r["mapping_status"] for r in maps})) if maps else "no direct registry row"
        tlines.append("| %s | %s | %d | %d | %s |"%(f"[[{table_names[t]}|{t}]]",PURPOSES.get(t,"Reference schema table."),len(meta["columns"]),sum(1 for c in meta["columns"] if c["fk"]),mapped))
    vlines=["| View | Source tables | Role |","|---|---|---|"]
    view_roles={
      "v_product_presentations":"Product/presentation/substance + identifier read model.",
      "v_observations":"Observation read model with product/facility/geography/diagnosis and source lineage.",
      "v_provenance_lineage":"Assertion→EvidenceSupport→SourceRecord→Release→Dataset→Transformation lineage.",
      "v_entity_matches":"Entity-match review surface joining both source-record endpoints."
    }
    for v in views:vlines.append("| %s | %s | %s |"%(code(v["name"]),", ".join(code(x) for x in v["tables"]),view_roles.get(v["name"],"Derived read model.")))
    refpage=f"""# V2 Database Reference

> **Version scope:** V2  
> **Status:** Reference implementation / Stable-to-date  
> **Updated:** 2026-09-24

This is the complete reader-facing reference for the current CM-PharmE PostgreSQL/PostGIS **research/reference realization**. It documents the implemented schema; it does not present the database as a deployed production system.

## Recomputed authoritative baseline
- **Tables:** {len(tables)}
- **Columns:** {total_columns}
- **Foreign keys:** {len(fks)}
- **CHECK constraints:** {len(checks)}
- **UNIQUE constraints:** {len(unique)}
- **Explicit indexes:** {len(indexes)}
- **SQL views:** {len(views)} (not included in the 24-table count)
- **PostGIS:** enabled
- **Geometry columns:** {len(postgis)}
- **Authority:** {code('v2/data/db/schema.sql')} at {code(AUTH_REF)}

## Purpose and scope
The schema provides an executable relational twin of selected V2 semantic commitments: source/provenance lineage, geography, organizations/facilities, medicinal-product identity, identifiers/entity matching, classification, assertions/evidence, observations and shortage situations.

It is designed for research reproducibility, mapping/evaluation and demonstration. It is not evidence of production deployment, operational scale, clinical use or complete realization of all 87 conceptual elements.

## PostgreSQL/PostGIS role
PostgreSQL provides relational integrity, auditable keys/constraints and queryable reference data. PostGIS is enabled for the canonical geography table. The current spatial realization uses {code('geometry(Geometry,4326)')} plus a GiST index and remains bounded to the implemented reference use cases.

## Ontology-alignment principles
- table names/foreign keys implement selected semantic elements but do not replace ontology definitions;
- mapping status is explicit in {code('v2/data/mappings/ontology-rdb-mapping.csv')};
- direct vs bounded/polymorphic/projection/deferred mappings remain distinguishable;
- Organization, Facility, Geography and RegulatoryJurisdiction remain separate;
- product/substance/presentation remain separate;
- identifiers are assignments, not identities;
- observations are aggregates and do not fabricate patient individuals.

## Provenance model
The principal lineage is:

Dataset → DatasetRelease → SourceRecord → TransformationRun / Assertion / EvidenceSupport → canonical/reference entities and observations.

See [[V2 Database ERD Suite]] and {code('v_provenance_lineage')}.

## Identity and entity-match model
IdentifierAssignment separates scheme/value assignment from real-world entity identity. EntityMatchAssertion records source-record pairs, method, confidence and status; it does not silently merge source rows.

## Implementation boundaries
The schema does **not** instantiate every V2 concept. Current Resilience/Risk implementation is especially bounded: {code('medicine_shortage_situation')} exists, while dedicated relational tables for SupplyDependency, Vulnerability, RiskAssessmentActivity or RiskTreatmentPlan/Activity are not present in this baseline.

## Table catalog — 24/24
{chr(10).join(tlines)}

## Derived SQL views — 4
{chr(10).join(vlines)}

Views are read/query surfaces and are not counted as physical tables.

## Data dictionary and mechanical evidence
- {code('wiki-src/database-reference/field-dictionary.csv')}
- {code('wiki-src/database-reference/fk-coverage.csv')}
- {code('wiki-src/database-reference/constraint-coverage.csv')}
- {code('wiki-src/database-reference/schema-catalog.json')}
- [[V2 Database ERD Suite]]

## Related semantic and query documentation
- [[V2 Ontology Reference]]
- [[V2 Data Infrastructure]]
- [[Knowledge Graph and Queries Guide]]
- [[V2 Evaluation E1-E13|CM-PharmE 2.0 Evaluation Framework]]
"""
    refpage+=wiki_record("v2/data/db/schema.sql, views.sql and ontology↔RDB mapping registry","Complete 24-table reference projection")
    (PAGES/"V2-Database-Reference.md").write_text(refpage,encoding="utf-8")
    page_rows.append(["V2 Database Reference","V2-Database-Reference","Reference / Data Model","V2","source-complete","pending-wiki-sync","236"])

    # ERDs.
    diagrams=[]
    diagrams.append(("DGM-ERD-002","V2 logical relational model","Logical model of major implemented subject areas and identities.",
      ["dataset","dataset_release","source_record","geography","organization","facility","medicinal_product","product_presentation","identifier_assignment","assertion","observation_result","medicine_shortage_situation"],False))
    diagrams.append(("DGM-ERD-003","V2 full physical ERD — 24 tables","Physical schema view of every implemented table, key columns and foreign keys.",list(tables),True))
    ids=4
    for key,spec in SUBJECTS.items():
        diagrams.append((f"DGM-ERD-{ids:03d}",spec["title"],spec["purpose"],spec["tables"],True));ids+=1

    manifest=json.loads((DIAG/"manifest.json").read_text(encoding="utf-8"))
    newids={d[0] for d in diagrams}
    manifest["diagrams"]=[x for x in manifest["diagrams"] if x["id"] not in newids]
    erdrows=[]
    for did,title,purpose,selected,physical in diagrams:
        stable=re.sub(r"[^a-z0-9]+","-",title.lower()).strip("-")
        src=f"wiki-src/diagrams/source/erd/{did}--{stable}.mmd"
        rend=f"wiki-src/diagrams/rendered/erd/{did}--{stable}.svg"
        (ROOT/src).parent.mkdir(parents=True,exist_ok=True);(ROOT/rend).parent.mkdir(parents=True,exist_ok=True)
        (ROOT/src).write_text(mermaid_erd(did,tables,selected),encoding="utf-8")
        (ROOT/rend).write_text(svg_erd(did,title,purpose,tables,selected,physical),encoding="utf-8")
        covered_fks=sum(1 for x in fks if x["child_table"] in selected and x["parent_table"] in selected)
        erdrows.append({"diagram_id":did,"title":title,"tables":len(selected),"internal_fks":covered_fks,"table_list":"; ".join(selected)})
        manifest["diagrams"].append({
          "id":did,"title":title,"purpose":purpose,"version_scope":"V2",
          "notation":"Crow's Foot ERD","artifact_status":"Authoritative projection" if physical else "Illustrative",
          "source_path":src,"rendered_path":rend,
          "generation_method":"Deterministic schema-derived Mermaid ER source plus SVG publication projection generated from v2/data/db/schema.sql.",
          "authoritative_source":"v2/data/db/schema.sql; ontology-rdb mapping registry provides semantic alignment context",
          "last_updated":"2026-09-24","checked_ref":AUTH_REF,
          "related_pages":["V2 Database ERD Suite","V2 Database Reference","Data and Database Guide"],
          "legend_required":True,"alt_text":purpose,
          "caption":did+" — "+title+". Generated from the current V2 reference schema; no production deployment claim."
        })
    (DIAG/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    with (outdir/"erd-coverage.csv").open("w",encoding="utf-8",newline="") as fh:
        w=csv.DictWriter(fh,fieldnames=["diagram_id","title","tables","internal_fks","table_list"]);w.writeheader();w.writerows(erdrows)

    # ERD suite page.
    suite=f"""# V2 Database ERD Suite

> **Version scope:** V2  
> **Status:** Reference implementation / Stable-to-date  
> **Updated:** 2026-09-24

This suite visualizes the current PostgreSQL/PostGIS reference schema. Logical and physical views are intentionally separate. The diagrams document an executable research/reference realization, not a production deployment.

## 1. Logical model — DGM-ERD-002

![Logical V2 relational model](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/erd/DGM-ERD-002--v2-logical-relational-model.svg)

A reader-oriented view of major implemented identities and lineage. It omits many physical columns/tables by design.

## 2. Full physical ERD — DGM-ERD-003

![Full physical V2 ERD](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/erd/DGM-ERD-003--v2-full-physical-erd-24-tables.svg)

All **24 physical tables** are represented. Every declared FK is represented in the source-derived physical model.

## Subject-area ERDs
"""
    for did,title,purpose,selected,physical in diagrams[2:]:
        stable=re.sub(r"[^a-z0-9]+","-",title.lower()).strip("-")
        suite+=f"""
### {title} — {did}

![{title}](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/erd/{did}--{stable}.svg)

{purpose}

[Source](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/source/erd/{did}--{stable}.mmd) · [SVG](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/wiki-src/diagrams/rendered/erd/{did}--{stable}.svg)
"""
    suite+=f"""
## Cardinality convention
The source is generated from physical FK nullability:
- a NOT NULL FK means each child row requires exactly one referenced parent;
- a nullable FK allows zero-or-one referenced parent;
- the parent side is zero-to-many child rows unless another constraint says otherwise.

No cardinality is invented beyond schema constraints.

## Resilience boundary
The shortage subject-area diagram shows only implemented relational structures. The current schema has {code('medicine_shortage_situation')} but no dedicated tables for SupplyDependency, Vulnerability, RiskAssessmentActivity or RiskTreatmentPlan/Activity.

## Mechanical coverage
- physical tables: **{len(tables)}/{EXPECTED_TABLES}**
- foreign keys: **{len(fks)}**
- subject-area diagrams: **{len(SUBJECTS)}**
- logical + physical + subject diagrams: **{len(diagrams)}**
- PostGIS geometry: {code('geography.geom geometry(Geometry,4326)')}
- explicit indexes: **{len(indexes)}**

See [[V2 Database Reference]] for the field/table catalog and mapping links.
"""
    suite+=wiki_record("v2/data/db/schema.sql","Nine schema-derived ERDs; logical/physical distinction preserved")
    (PAGES/"V2-Database-ERD-Suite.md").write_text(suite,encoding="utf-8")
    page_rows.append(["V2 Database ERD Suite","V2-Database-ERD-Suite","Concept / Data Model","V2","source-complete","pending-wiki-sync","236"])

    # coverage report.
    coverage={
      "issue":236,"authority_ref":AUTH_REF,"tables_expected":24,"tables_actual":len(tables),
      "columns":total_columns,"foreign_keys":len(fks),"checks":len(checks),
      "unique_constraints":len(unique),"explicit_indexes":len(indexes),"views":len(views),
      "postgis_enabled":True,"geometry_columns":postgis,
      "table_pages":len(tables),"erd_count":len(diagrams),"subject_erd_count":len(SUBJECTS),
      "uncovered_tables":[],"uncovered_foreign_keys":[],"errors":[]
    }
    (outdir/"database-coverage.json").write_text(json.dumps(coverage,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    (outdir/"MISSING-ITEMS.md").write_text(
      "# V2 database documentation missing-item register\n\n"
      "**No blocking physical-schema coverage gaps detected.**\n\n"
      f"- tables: {len(tables)}/24\n- table reference pages: {len(tables)}/24\n- FKs cataloged: {len(fks)}\n"
      f"- ERDs: {len(diagrams)}\n- explicit indexes: {len(indexes)}\n- SQL views cataloged: {len(views)}\n\n"
      "Semantic/implementation gaps such as unimplemented dedicated resilience/risk tables are documented as scope boundaries rather than hidden documentation gaps.\n",
      encoding="utf-8")

    # Inventory refresh for #236.
    with INVENTORY.open(encoding="utf-8",newline="") as fh: rows=list(csv.reader(fh))
    header=rows[0]
    kept=[header]+[r for r in rows[1:] if len(r)<7 or r[6]!="236"]
    with INVENTORY.open("w",encoding="utf-8",newline="") as fh: csv.writer(fh).writerows(kept+page_rows)

    # Home shortcut.
    home=PAGES/"Home.md"; ht=home.read_text(encoding="utf-8")
    shortcut="- **Open the complete V2 database reference:** [[V2 Database Reference]]\n"
    if shortcut not in ht:
        anchor="- **Understand datasets and the relational database:** [[Data and Database Guide]]\n"
        ht=ht.replace(anchor,anchor+shortcut);home.write_text(ht,encoding="utf-8")
    # Data guide links.
    dg=PAGES/"Data-and-Database-Guide.md"; dt=dg.read_text(encoding="utf-8")
    if "[[V2 Database Reference]]" not in dt:
        dt=dt.replace("## V2 data and database", "## Complete relational reference\n- [[V2 Database Reference]] — 24-table catalog, field dictionary, mappings and views.\n- [[V2 Database ERD Suite]] — logical, full physical and seven subject-area ERDs.\n\n## V2 data and database")
        dg.write_text(dt,encoding="utf-8")
    sidebar=PAGES/"_Sidebar.md"; st=sidebar.read_text(encoding="utf-8")
    if "[[V2 Database Reference]]" not in st:
        st=st.replace("**Data & Database**\n- [[Data and Database Guide]]","**Data & Database**\n- [[Data and Database Guide]]\n- [[V2 Database Reference]]\n- [[V2 Database ERD Suite]]")
        sidebar.write_text(st,encoding="utf-8")

    print(json.dumps(coverage,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
