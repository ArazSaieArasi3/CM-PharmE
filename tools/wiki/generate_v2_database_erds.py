#!/usr/bin/env python3
import argparse
import csv
import hashlib
import html
import json
import re
from pathlib import Path

from db_schema_model import parse_schema, foreign_key_edges

ROOT=Path(__file__).resolve().parents[2]
WIKI=ROOT/"wiki-src"
PAGES=WIKI/"pages"
DIAG=WIKI/"diagrams"
DBREF=WIKI/"database-reference"
INVENTORY=WIKI/"page-inventory.csv"
AUTH_REF="v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999"
RAW_PREFIX="https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/"

SUBJECT_IDS={
 "dataset-provenance":"DGM-ERD-004",
 "organization-geography":"DGM-ERD-005",
 "product-classification":"DGM-ERD-006",
 "identity-matching":"DGM-ERD-007",
 "assertion-evidence":"DGM-ERD-008",
 "observation":"DGM-ERD-009",
 "shortage-resilience":"DGM-ERD-010",
}

def code(value):
    q=chr(96)
    return q+str(value)+q

def important_columns(table):
    out=[]
    preferred={"public_id","preferred_name","canonical_name","source_hash","status","confidence","observation_kind","reporting_period","ontology_iri","entity_type","predicate_key","geography_type"}
    for col in table["columns"]:
        if col["pk"] or col["fk"] or col["name"] in preferred:
            out.append(col)
    for col in table["columns"]:
        if col not in out:
            out.append(col)
        if len(out)>=8:
            break
    return out[:8]

def mermaid_source(diagram_id,title,tables,selected,physical=False):
    lines=["%% "+diagram_id+" — "+title,"erDiagram"]
    for name in selected:
        table=tables[name]
        cols=table["columns"] if physical else important_columns(table)
        lines.append("  "+name.upper()+" {")
        for col in cols:
            flags=[]
            if col["pk"]: flags.append("PK")
            if col["fk"]: flags.append("FK")
            if col["unique"]: flags.append("UK")
            typ=re.sub(r"[^A-Za-z0-9_]","_",col["type"])
            suffix=(" "+" ".join(flags)) if flags else ""
            lines.append("    "+typ+" "+col["name"]+suffix)
        lines.append("  }")
    for edge in foreign_key_edges(tables,selected):
        parent=edge["ref_table"].upper()
        child=edge["child"].upper()
        parent_card="o|" if edge["nullable"] else "||"
        lines.append('  '+parent+" "+parent_card+'--o{ '+child+' : "'+edge["column"]+'"')
    return "\n".join(lines)+"\n"

def physical_svg(diagram_id,title,tables,selected,physical=False):
    selected=list(selected)
    columns=4 if physical else 3
    box_w=310
    gap_x=40
    gap_y=50
    margin=40
    header=105

    heights={}
    for name in selected:
        cols=tables[name]["columns"] if physical else important_columns(tables[name])
        heights[name]=62+18*len(cols)+20

    rows=(len(selected)+columns-1)//columns
    row_heights=[]
    for r in range(rows):
        names=selected[r*columns:(r+1)*columns]
        row_heights.append(max([heights[n] for n in names] or [120]))

    row_y=[]
    y=header
    for h in row_heights:
        row_y.append(y)
        y+=h+gap_y

    width=margin*2+columns*box_w+(columns-1)*gap_x
    height=max(520,y+115)
    pos={}
    for i,name in enumerate(selected):
        c=i%columns
        r=i//columns
        pos[name]=(margin+c*(box_w+gap_x),row_y[r],heights[name])

    out=[
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-labelledby="title desc" data-theme-safe="true" style="color:#24292f;background:#ffffff">'%(width,height),
      '<title id="title">'+html.escape(diagram_id+" "+title)+'</title>',
      '<desc id="desc">ERD generated from the authoritative CM-PharmE V2 PostgreSQL/PostGIS schema.</desc>',
      '<rect id="diagram-background" x="0" y="0" width="100%" height="100%" fill="#ffffff" stroke="none" pointer-events="none"/>',
      '<defs><marker id="fkarr" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#57606a"/></marker></defs>',
      '<text x="%s" y="32" text-anchor="middle" font-family="sans-serif" font-size="20" font-weight="bold" fill="#24292f">%s</text>'%(width/2,html.escape(title)),
      '<text x="40" y="62" font-family="sans-serif" font-size="11" fill="#57606a">Generated from schema.sql. Arrow direction: FK table to referenced table. PK/FK/UK denote physical-schema roles.</text>'
    ]

    edges=foreign_key_edges(tables,selected)
    pair_groups={}
    for idx,edge in enumerate(edges):
        key=(edge["child"],edge["ref_table"])
        pair_groups.setdefault(key,[]).append(idx)
    offsets={}
    for key,idxs in pair_groups.items():
        center=(len(idxs)-1)/2
        for j,idx in enumerate(idxs):
            offsets[idx]=(j-center)*18

    for idx,edge in enumerate(edges):
        child=edge["child"]; parent=edge["ref_table"]
        if child not in pos or parent not in pos:
            continue
        cx,cy,ch=pos[child]
        px,py,ph=pos[parent]
        x1=cx+box_w/2; y1=cy+ch/2
        x2=px+box_w/2; y2=py+ph/2
        dx=x2-x1; dy=y2-y1
        dist=(dx*dx+dy*dy)**0.5 or 1.0
        perp_x=-dy/dist; perp_y=dx/dist
        off=offsets.get(idx,0)
        x1+=perp_x*off; y1+=perp_y*off
        x2+=perp_x*off; y2+=perp_y*off
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#8c959f" stroke-width="1.1" marker-end="url(#fkarr)"/>'%(x1,y1,x2,y2))
        mx=(x1+x2)/2+perp_x*5; my=(y1+y2)/2+perp_y*5
        out.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#57606a">%s</text>'%(mx,my-4,html.escape(edge["column"])))

    for name in selected:
        x,y,h=pos[name]
        table=tables[name]
        out.append('<rect x="%d" y="%d" width="%d" height="%d" rx="5" fill="#ffffff" stroke="#24292f" stroke-width="1.3"/>'%(x,y,box_w,h))
        out.append('<rect x="%d" y="%d" width="%d" height="38" rx="5" fill="#f6f8fa" stroke="#24292f" stroke-width="1.3"/>'%(x,y,box_w))
        out.append('<text x="%.1f" y="%d" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="#24292f">%s</text>'%(x+box_w/2,y+25,html.escape(name)))
        cols=table["columns"] if physical else important_columns(table)
        yy=y+58
        for col in cols:
            flags=[]
            if col["pk"]: flags.append("PK")
            if col["fk"]: flags.append("FK")
            if col["unique"]: flags.append("UK")
            prefix=("["+"/".join(flags)+"] ") if flags else ""
            label=prefix+col["name"]+" : "+col["type"]
            if len(label)>46:
                label=label[:43]+"..."
            out.append('<text x="%d" y="%d" font-family="monospace" font-size="10" fill="#24292f">%s</text>'%(x+10,yy,html.escape(label)))
            yy+=18

    out.append('<text x="40" y="%d" font-family="sans-serif" font-size="11" fill="#57606a">Reference implementation only. schema.sql remains authoritative; ontology semantics are not inferred from ERD layout.</text>'%(height-48))
    out.append("</svg>")
    return "\n".join(out)+"\n"

def logical_svg(tables,selected):
    svg=physical_svg("DGM-ERD-002","V2 logical relational model",tables,selected,False)
    labels={
      "dataset":"Dataset","dataset_release":"Dataset Release","source_record":"Source Record",
      "organization":"Organization","facility":"Facility","geography":"Geography",
      "regulatory_jurisdiction":"Regulatory Jurisdiction","pharmaceutical_substance":"Pharmaceutical Substance",
      "medicinal_product":"Medicinal Product","product_presentation":"Product Presentation",
      "identifier_assignment":"Identifier Assignment","assertion":"Assertion",
      "evidence_support":"Evidence Support","observation_result":"Observation Result",
      "entity_match_assertion":"Entity Match Assertion","medicine_shortage_situation":"Medicine Shortage Situation"
    }
    for source,label in labels.items():
        svg=svg.replace(">"+source+"<",">"+label+"<")
    return svg

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--authority-root",required=True)
    args=ap.parse_args()
    auth=Path(args.authority_root).resolve()

    schema=(auth/"v2/data/db/schema.sql").read_text(encoding="utf-8")
    tables,raw_counts,parsed_counts=parse_schema(schema)
    metadata=json.loads((DBREF/"table-metadata.json").read_text(encoding="utf-8"))
    subjects=metadata["subject_areas"]

    errors=[]
    if len(tables)!=24:
        errors.append("expected 24 tables")
    for key,area in subjects.items():
        for table in area["tables"]:
            if table not in tables:
                errors.append(key+" references unknown table "+table)
    if errors:
        print(json.dumps({"errors":errors},indent=2))
        raise SystemExit(1)

    logical=[
      "dataset","dataset_release","source_record",
      "organization","facility","geography","regulatory_jurisdiction",
      "pharmaceutical_substance","medicinal_product","product_presentation",
      "identifier_assignment","assertion","evidence_support","observation_result",
      "entity_match_assertion","medicine_shortage_situation"
    ]

    specs=[
      ("DGM-ERD-002","V2 logical relational model",logical,False,
       "Logical reader view of the principal V2 relational entities and implemented foreign-key structure."),
      ("DGM-ERD-003","V2 full physical ERD — 24 tables",list(tables),True,
       "Full physical ERD covering all 24 implemented base tables and every declared foreign key.")
    ]
    for key,area in subjects.items():
        specs.append((SUBJECT_IDS[key],area["title"],area["tables"],False,
                      "Readable subject-area ERD generated from the implemented V2 reference schema."))

    src_dir=DIAG/"source"/"erd"
    svg_dir=DIAG/"rendered"/"erd"
    src_dir.mkdir(parents=True,exist_ok=True)
    svg_dir.mkdir(parents=True,exist_ok=True)

    generated=[]
    for did,title,selected,physical,purpose in specs:
        stable=re.sub(r"[^a-z0-9]+","-",title.lower()).strip("-")
        src_rel="wiki-src/diagrams/source/erd/"+did+"--"+stable+".mmd"
        svg_rel="wiki-src/diagrams/rendered/erd/"+did+"--"+stable+".svg"
        (ROOT/src_rel).write_text(mermaid_source(did,title,tables,selected,physical),encoding="utf-8")
        svg=logical_svg(tables,selected) if did=="DGM-ERD-002" else physical_svg(did,title,tables,selected,physical)
        (ROOT/svg_rel).write_text(svg,encoding="utf-8")
        sha=hashlib.sha256((ROOT/svg_rel).read_bytes()).hexdigest()[:12]
        generated.append({
          "id":did,"title":title,"purpose":purpose,"source_path":src_rel,"rendered_path":svg_rel,
          "raw":RAW_PREFIX+svg_rel+"?sha="+sha,"tables":selected
        })

    manifest_path=DIAG/"manifest.json"
    manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
    ids={d["id"] for d in generated}
    manifest["diagrams"]=[d for d in manifest.get("diagrams",[]) if d["id"] not in ids]
    for d in generated:
        manifest["diagrams"].append({
          "id":d["id"],"title":d["title"],"purpose":d["purpose"],
          "version_scope":"V2",
          "notation":"Crow's Foot ERD",
          "artifact_status":"Authoritative projection",
          "source_path":d["source_path"],"rendered_path":d["rendered_path"],
          "generation_method":"Project-native deterministic generator parses v2/data/db/schema.sql and emits Mermaid ER source plus governed SVG.",
          "authoritative_source":"v2/data/db/schema.sql",
          "last_updated":"2026-09-25","checked_ref":AUTH_REF,
          "related_pages":["V2 Database Reference","V2 Database ERD Suite","V2 Data Infrastructure"],
          "legend_required":True,
          "alt_text":d["purpose"],
          "caption":d["id"]+" — "+d["title"]+". Generated from the checked V2 reference schema; reference implementation only."
        })
    manifest["diagrams"]=sorted(manifest["diagrams"],key=lambda x:x["id"])
    manifest_path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

    # Coverage rows
    with (DBREF/"erd-coverage.csv").open("w",encoding="utf-8",newline="") as fh:
        w=csv.writer(fh)
        w.writerow(["diagram_id","title","tables","table_count"])
        for d in generated:
            w.writerow([d["id"],d["title"],"; ".join(d["tables"]),len(d["tables"])])

    all_fk=len(foreign_key_edges(tables))
    physical_fk=len(foreign_key_edges(tables,list(tables)))
    summary={
      "issue":236,"authority_ref":AUTH_REF,
      "erd_count":len(generated),
      "logical_erd":1,
      "physical_erd":1,
      "subject_area_erds":len(subjects),
      "physical_tables":len(tables),
      "physical_fk_edges":physical_fk,
      "authoritative_fk_edges":all_fk,
      "all_tables_in_physical_erd":set(tables)==set(next(d["tables"] for d in generated if d["id"]=="DGM-ERD-003")),
      "errors":[]
    }
    (DBREF/"erd-coverage.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")

    # Reader-facing suite.
    lines=[
      "# V2 Database ERD Suite","",
      "> **Version scope:** V2  ",
      "> **Status:** Reference implementation  ",
      "> **Updated:** 2026-09-25","",
      "This suite documents the implemented V2 PostgreSQL/PostGIS reference schema at logical, full-physical and subject-area levels. The SQL DDL remains authoritative.","",
      "## Reading conventions",
      "- Logical ERD: orientation-level simplification.",
      "- Full physical ERD: all 24 base tables and every physical foreign key.",
      "- Subject-area ERDs: readable local views of the same physical schema.",
      "- Arrow direction: foreign-key table to referenced table.",
      "- PK/FK/UK labels are physical-schema markers.",
      "- No ERD layout creates ontology semantics.",""
    ]
    for i,d in enumerate(generated,1):
        lines += [
          "## "+str(i)+". "+d["title"]+" — "+d["id"],"",
          "!["+d["id"]+" "+d["title"]+"]("+d["raw"]+")","",
          d["purpose"],"",
          "Source: "+code(d["source_path"])+"  ",
          "Rendered SVG: "+code(d["rendered_path"]),""
        ]
    lines += [
      "## Coverage","",
      "- ERDs: **9/9**",
      "- full physical tables: **24/24**",
      "- full physical FK edges: **%d/%d**"%(physical_fk,all_fk),
      "- subject-area ERDs: **7/7**","",
      "## Boundary",
      "These diagrams document a reference/research implementation. They do not demonstrate production scalability, availability, full-source ingestion or semantic superiority of the relational representation.","",
      "---","",
      "<details>","<summary>Documentation record</summary>","",
      "- **Page scope:** V2",
      "- **Documentation maturity:** Stable-to-date / Evolving",
      "- **Authoritative source:** V2 PostgreSQL/PostGIS DDL",
      "- **Last synchronized:** 2026-09-25",
      "- **Last synchronized ref:** "+AUTH_REF,
      "- **Related issues/PRs:** #232, #236, #237",
      "- **Evidence status:** 9 governed ERDs generated from schema.sql",
      "- **Future refresh:** #212 / #213 / #214 as applicable",
      "- **Wiki baseline:** WB-2026.09.1","",
      "</details>"
    ]
    (PAGES/"V2-Database-ERD-Suite.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

    # Inventory row for suite, preserving other #236 rows.
    with INVENTORY.open(encoding="utf-8-sig",newline="") as fh:
        rows=list(csv.reader(fh))
    if not any(len(r)>=7 and r[6]=="236" and r[0]=="V2 Database ERD Suite" for r in rows[1:]):
        rows.append(["V2 Database ERD Suite","V2-Database-ERD-Suite","Data / Database","V2","source-complete","pending-wiki-sync","236"])
    with INVENTORY.open("w",encoding="utf-8",newline="") as fh:
        csv.writer(fh).writerows(rows)

    print(json.dumps(summary,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
