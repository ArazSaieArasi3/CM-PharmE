#!/usr/bin/env python3
import argparse, csv, json, re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki-src"
PAGES = WIKI / "pages"
INVENTORY = WIKI / "page-inventory.csv"
BT = chr(96)

def slugify(text):
    s = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-")
    return s or "item"

def frontmatter(text):
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    out = {}
    for line in parts[1].splitlines():
        if ":" in line:
            k,v=line.split(":",1)
            out[k.strip()] = v.strip()
    return out

def section(text, heading):
    pat = re.compile(r"^##\s+"+re.escape(heading)+r"\s*$", re.M)
    m=pat.search(text)
    if not m:
        return ""
    start=m.end()
    n=re.search(r"^##\s+", text[start:], re.M)
    end=start+n.start() if n else len(text)
    return text[start:end].strip()

def bullet(sec, label):
    m=re.search(r"^-\s+\*\*"+re.escape(label)+r":\*\*\s*(.+)$", sec, re.M)
    return m.group(1).strip() if m else "—"

def blockquote(sec):
    vals=[]
    for line in sec.splitlines():
        if line.startswith(">"):
            vals.append(line[1:].strip())
    return " ".join(vals).strip() or "—"

def md_table_rows(text):
    rows=[]
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells=[c.strip() for c in line.strip().strip("|").split("|")]
        if cells and re.fullmatch(r"\d+", cells[0]):
            rows.append(cells)
    return rows

def parse_domains(path):
    rows=md_table_rows(path.read_text(encoding="utf-8"))
    out=[]
    for c in rows:
        if len(c) < 7:
            continue
        out.append({
            "number":int(c[0]),"name":c[1],"layer":c[2],
            "definition":c[3],"count":int(c[4]),"review":c[5]
        })
    return out

def parse_passports(root):
    out=[]
    for path in sorted((root/"v2/review/concepts/passports").glob("[0-9][0-9][0-9]-*.md")):
        text=path.read_text(encoding="utf-8")
        fm=frontmatter(text)
        out.append({
            "number":int(path.name[:3]),
            "path":path.relative_to(root).as_posix(),
            "concept_id":fm.get("concept_id",""),
            "label":fm.get("canonical_label",""),
            "iri":fm.get("iri",""),
            "domain":fm.get("domain",""),
            "stereotype":fm.get("stereotype",""),
            "ontology_version":fm.get("ontology_version",""),
            "review_status":fm.get("review_status",""),
            "evidence_status":fm.get("evidence_status",""),
            "definition":blockquote(section(text,"Canonical definition")),
            "review_focus":bullet(section(text,"Ontological commitments"),"Review focus"),
            "dataset":bullet(section(text,"Evidence"),"Dataset"),
            "held_out":bullet(section(text,"Evidence"),"Held-out"),
            "other_support":bullet(section(text,"Evidence"),"Other support"),
            "migration":bullet(section(text,"Previous-version lineage"),"Migration treatment"),
            "owl":bullet(section(text,"Formal representation"),"OWL"),
            "disposition":bullet(section(text,"Human review"),"Disposition"),
        })
    return out

def parse_relations(path):
    text=path.read_text(encoding="utf-8")
    layer=None
    out=[]
    for line in text.splitlines():
        if line.startswith("## Core relations"):
            layer="Core"
        elif line.startswith("## Cross-cutting infrastructure relations"):
            layer="X-INFRA"
        elif line.startswith("## Extension relations"):
            layer="Extension"
        elif layer and line.startswith("|"):
            cells=[c.strip() for c in line.strip().strip("|").split("|")]
            if cells and re.fullmatch(r"\d+",cells[0]) and len(cells)>=6:
                out.append({
                    "layer":layer,
                    "property":cells[1].strip(BT),
                    "domain":cells[2],
                    "range":cells[3],
                    "note":cells[4],
                    "status":cells[5],
                })
    return out

def ttl_entities(root):
    result={"class":{},"datatype":{},"object":{},"datatype_property":{}}
    files=sorted((root/"v2/ontology/source/modules").glob("*.ttl"))
    statement_re=re.compile(r"cmpe:([A-Za-z0-9_]+)\s+a\s+(owl:Class|rdfs:Datatype|owl:ObjectProperty|owl:DatatypeProperty)\s*;(.*?)\s*\.",re.S)
    for path in files:
        text=path.read_text(encoding="utf-8")
        for m in statement_re.finditer(text):
            local,kind,body=m.groups()
            target={"owl:Class":"class","rdfs:Datatype":"datatype","owl:ObjectProperty":"object","owl:DatatypeProperty":"datatype_property"}[kind]
            def one(pattern):
                x=re.search(pattern,body)
                return x.group(1) if x else None
            label=one(r'rdfs:label\s+"([^"]+)"') or local
            domain=one(r"rdfs:domain\s+cmpe:([A-Za-z0-9_]+)")
            rm=re.search(r"rdfs:range\s+(cmpe|xsd):([A-Za-z0-9_]+)",body)
            rangev=(rm.group(1)+":"+rm.group(2)) if rm else None
            sm=re.search(r"rdfs:subClassOf\s+([^;]+)",body)
            parents=re.findall(r"cmpe:([A-Za-z0-9_]+)",sm.group(1)) if sm else []
            module=one(r'cmmeta:conceptualModule\s+"([^"]+)"')
            derived=one(r'cmmeta:derivedFromRelator\s+"([^"]+)"')
            material=bool(re.search(r'cmmeta:materialRelation\s+"true"',body))
            result[target][local]={
                "local":local,"label":label,"domain":domain,"range":rangev,
                "parents":parents,"module":module,"source":path.relative_to(root).as_posix(),
                "derived":derived,"material":material
            }
    return result

def wiki(name, label=None):
    return "[["+name+("|"+label if label else "")+"]]"

def code(value):
    return BT+str(value)+BT

def doc_record(authority_ref, sources, evidence="Generated reference projection; semantic approval not implied"):
    return """
---

<details>
<summary>Documentation record</summary>

- **Page scope:** V2
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative source:** %s
- **Last synchronized:** 2026-09-24
- **Last synchronized ref:** %s
- **Related issues/PRs:** #213, #234
- **Evidence status:** %s
- **Future refresh:** #213 / #214 as applicable
- **Wiki baseline:** WB-2026.09.1

</details>
""" % (sources, authority_ref, evidence)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--authority-root",required=True)
    ap.add_argument("--authority-ref",required=True)
    args=ap.parse_args()
    auth=Path(args.authority_root).resolve()
    authority_ref=args.authority_ref

    baseline=json.loads((auth/"v2/ontology/baseline/formal-baseline.json").read_text(encoding="utf-8"))
    conceptual=json.loads((auth/"v2/ontouml/cm-pharme-v2.conceptual-model.json").read_text(encoding="utf-8"))
    domains=parse_domains(auth/"v2/review/domains/index.md")
    concepts=parse_passports(auth)
    relations=parse_relations(auth/"v2/review/relations/index.md")
    formal=ttl_entities(auth)
    shacl=(auth/"v2/ontology/shapes/cm-pharme-v2.shacl.ttl").read_text(encoding="utf-8")

    errors=[]
    expected={
        "concepts":87,"domains":17,"classes":81,"datatypes":6,
        "object_properties":52,"datatype_properties":5
    }
    actual={
        "concepts":len(concepts),"domains":len(domains),"classes":len(formal["class"]),
        "datatypes":len(formal["datatype"]),"object_properties":len(formal["object"]),
        "datatype_properties":len(formal["datatype_property"])
    }
    for k,v in expected.items():
        if actual[k]!=v:
            errors.append("%s expected %s got %s"%(k,v,actual[k]))
    if baseline.get("conceptual_type_count")!=87:
        errors.append("formal baseline conceptual_type_count != 87")
    if conceptual.get("counts",{}).get("total")!=87:
        errors.append("conceptual registry total != 87")

    concept_by_local={}
    concept_by_label={}
    for c in concepts:
        local=c["iri"].replace("cmpe:","")
        if local in formal["class"]:
            c["formal_type"]="OWL Class"
            c["formal"]=formal["class"][local]
        elif local in formal["datatype"]:
            c["formal_type"]="RDFS Datatype"
            c["formal"]=formal["datatype"][local]
        else:
            errors.append("concept has no formal class/datatype: "+c["label"]+" / "+local)
            c["formal_type"]="UNMAPPED"
            c["formal"]={"parents":[]}
        c["local"]=local
        concept_by_local[local]=c
        concept_by_label[c["label"]]=c

    formal_concept_locals=set(formal["class"])|set(formal["datatype"])
    unmatched_formal=sorted(formal_concept_locals-set(concept_by_local))
    if unmatched_formal:
        errors.append("formal conceptual entities without passport: "+", ".join(unmatched_formal))

    domain_by_name={d["name"]:d for d in domains}
    for c in concepts:
        if c["domain"] not in domain_by_name:
            errors.append("unknown domain for concept "+c["label"]+": "+c["domain"])

    rel_review={r["property"]:r for r in relations}
    if set(rel_review)!=set(formal["object"]):
        errors.append("relation catalog/object-property set mismatch")

    protected=conceptual.get("protected_distinctions",[])
    protected_by_local=defaultdict(list)
    for a,b in protected:
        protected_by_local[a].append(b); protected_by_local[b].append(a)

    page_rows=[]
    generated=[]

    ref_name="V2 Ontology Reference"
    ref_slug="V2-Ontology-Reference"

    def add_page(name,slug,klass,content):
        path=PAGES/(slug+".md")
        path.write_text(content.rstrip()+"\n",encoding="utf-8")
        generated.append(path)
        page_rows.append([name,slug,klass,"V2","source-complete","pending-wiki-sync","234"])

    # names first for cross-links
    module_names={}
    for d in domains:
        module_names[d["name"]]="V2 Module %02d %s"%(d["number"],d["name"])
    concept_names={}
    for c in concepts:
        concept_names[c["local"]]="V2 Concept C%03d %s"%(c["number"],c["label"])
    object_names={p:"V2 Object Property "+p for p in sorted(formal["object"])}
    datatype_names={p:"V2 Datatype Property "+p for p in sorted(formal["datatype_property"])}

    # module pages
    concepts_by_domain=defaultdict(list)
    for c in concepts:
        concepts_by_domain[c["domain"]].append(c)

    def relation_rows_for_domain(domain_name):
        locals_in={c["local"] for c in concepts_by_domain[domain_name]}
        rows=[]
        for p,e in formal["object"].items():
            rng=e["range"]
            rng_local=rng.split(":",1)[1] if rng and rng.startswith("cmpe:") else None
            if e["domain"] in locals_in or rng_local in locals_in:
                rows.append((p,e,rel_review.get(p,{})))
        return rows

    for d in domains:
        name=module_names[d["name"]]
        slug=slugify(name)
        clist=sorted(concepts_by_domain[d["name"]],key=lambda x:x["number"])
        rlist=relation_rows_for_domain(d["name"])
        concept_table=["| Concept | Stereotype | Formal entity | Review |","|---|---|---|---|"]
        for c in clist:
            concept_table.append("| %s | %s | %s | %s |"%(
                wiki(concept_names[c["local"]],c["label"]),c["stereotype"],c["formal_type"],c["review_status"]))
        rel_table=["| Property | Domain | Range | Review note |","|---|---|---|---|"]
        for p,e,rr in rlist:
            rng=e["range"] or "unspecified"
            rel_table.append("| %s | %s | %s | %s |"%(
                wiki(object_names[p],code(p)), e["domain"] or "unspecified", rng, rr.get("note","—")))
        pd=[]
        locals_in={c["local"] for c in clist}
        for a,b in protected:
            if a in locals_in or b in locals_in:
                pd.append(code(a)+" ≠ "+code(b))
        example="No explicit domain–range pair is selected as a module example."
        for p,e,rr in rlist:
            if e["domain"] and e["range"] and e["range"].startswith("cmpe:"):
                example=code(e["domain"])+" — "+code(p)+" → "+code(e["range"].split(":",1)[1])
                break
        content=f"""# {d['name']}

> **Version scope:** V2  
> **Status:** {d['review']} semantic review  
> **Updated:** 2026-09-24

> Generated module reference projection. Semantic authority remains in the linked V2 conceptual, formal and review artifacts.

## Purpose and scope
{d['definition']}

## Layer and architecture
- **Layer:** {d['layer']}
- **Concept count:** {len(clist)}
- **Ontology version:** 2.0.0-alpha.1
- **Authority ref:** {code(authority_ref)}

## Principal concepts
{chr(10).join(concept_table)}

## Relation patterns
{chr(10).join(rel_table) if rlist else 'No object property has an explicit formal endpoint in this module.'}

Properties with an unspecified OWL endpoint remain unspecified; this page does not infer the missing endpoint.

## Constraints and protected distinctions
{('; '.join(pd)) if pd else 'No Gate-D protected distinction is registered specifically for this module.'}

For executable constraints and validation evidence, see {wiki('V2 Formal Ontology and SHACL')} and {wiki('V2 Evaluation E1-E13','CM-PharmE 2.0 Evaluation Framework')}.

## Modeling decisions
This module belongs to the **{d['layer']}** layer in the approved 17-domain V2 review taxonomy. Its definition and concept ownership come from the V2 domain review catalog and integrated conceptual model. The generated page does not move, split, merge or approve concepts.

## Structural example
{example}

This is a structural relation example, not an instance-data claim.

## Evaluation and competency-question context
- {wiki('V2 Evaluation E1-E13','CM-PharmE 2.0 Evaluation Framework')}
- {wiki('V2 Formal Ontology and SHACL')}
- {wiki('V2 Human Ontology Review','CM-PharmE 2.0 Semantic Review')}

## Known boundaries
- Current domain review state: **{d['review']}**.
- Generated reference does not constitute human/author semantic approval.
- Coverage does not imply pharmaceutical-domain completeness.
- Future accepted findings are synchronized through #213.

## Authoritative sources
- V2 domain review catalog: {code('v2/review/domains/index.md')}
- conceptual registry: {code('v2/ontouml/cm-pharme-v2.conceptual-model.json')}
- formal ontology modules: {code('v2/ontology/source/modules/*.ttl')}
"""
        content+=doc_record(authority_ref,"V2 domain review catalog, conceptual registry and formal ontology")
        add_page(name,slug,"Concept / Domain / Model",content)

    # concept pages
    for c in concepts:
        name=concept_names[c["local"]]
        slug=slugify(name)
        fr=c["formal"]
        parents=fr.get("parents",[])
        rels=[]
        for p,e in formal["object"].items():
            rng=e["range"]
            rng_local=rng.split(":",1)[1] if rng and rng.startswith("cmpe:") else None
            if e["domain"]==c["local"]:
                rels.append(("Outgoing",p,rng or "unspecified", "explicit domain"+(" and range" if rng else "; range unspecified")))
            if rng_local==c["local"]:
                rels.append(("Incoming",p,e["domain"] or "unspecified","explicit range"+(" and domain" if e["domain"] else "; domain unspecified")))
        rel_table=["| Direction | Property | Other endpoint | Constraint status |","|---|---|---|---|"]
        for direction,p,other,status in rels:
            rel_table.append("| %s | %s | %s | %s |"%(direction,wiki(object_names[p],code(p)),other,status))
        shacl_ref=(f"cmpe:{c['local']}" in shacl)
        protected_links=protected_by_local.get(c["local"],[])
        boundary="No Gate-D protected distinction is registered for this concept."
        if protected_links:
            boundary="Protected conceptual distinction(s): "+", ".join(code(c["local"]+" ≠ "+x) for x in protected_links)+"."
        structural="No explicit object-property domain/range example is selected for this concept."
        for direction,p,other,status in rels:
            if other!="unspecified":
                structural=(code(c["local"])+" — "+code(p)+" → "+code(other)) if direction=="Outgoing" else (code(other)+" — "+code(p)+" → "+code(c["local"]))
                break
        content=f"""# {c['label']}

> **Version scope:** V2  
> **Status:** {c['review_status']} semantic review  
> **Updated:** 2026-09-24

> Generated concept reference from the V2 Concept Evidence Passport and formal ontology. This page does not create or approve semantics.

## Canonical definition
> {c['definition']}

## Ontological role
| Field | Value |
|---|---|
| Concept ID | {code(c['concept_id'])} |
| Domain | {wiki(module_names[c['domain']],c['domain'])} |
| Layer | {domain_by_name[c['domain']]['layer']} |
| OntoUML stereotype | {c['stereotype']} |
| Formal entity type | {c['formal_type']} |
| Formal IRI | {code(c['iri'])} |

## Generalization
{(', '.join(wiki(concept_names[p],p) if p in concept_names else code(p) for p in parents)) if parents else 'No explicit formal parent is declared in the parsed source statement.'}

## Principal formal relations
{chr(10).join(rel_table) if rels else 'No object property declares this concept as an explicit OWL domain or range endpoint.'}

Properties whose endpoint is formally unspecified are not inferred into this list.

## Constraints / SHACL relevance
- {boundary}
- Current SHACL source {'references' if shacl_ref else 'does not directly reference'} {code(c['iri'])}. This is a syntactic reference observation, not a completeness judgment.
- See {wiki('V2 Formal Ontology and SHACL')} for constraint semantics and validation scope.

## Evidence and provenance
- **Dataset/source evidence:** {c['dataset']}
- **Held-out evidence:** {c['held_out']}
- **Other support:** {c['other_support']}
- **Review focus:** {c['review_focus']}

## V1 lineage
- **Migration treatment:** {c['migration']}
- See {wiki('V1 to V2 Concept Migration')} and {wiki('V1 to V2 Research Evolution')} for cross-version interpretation.

## Structural example
{structural}

This is a structural example grounded in explicit formal endpoints, not an instance-data assertion.

## Boundary / non-example
{boundary}

A source record, identifier or label should not be treated as this domain entity unless the governing ontology/evidence relation explicitly supports that interpretation.

## Review state
- **Passport review state:** {c['review_status']}
- **Evidence status:** {c['evidence_status']}
- **Human/author disposition:** {c['disposition']}

Pending status remains pending until the governed semantic review records a disposition.

## Authoritative sources
- Concept Evidence Passport: {code(c['path'])}
- conceptual registry: {code('v2/ontouml/cm-pharme-v2.conceptual-model.json')}
- formal source: {code(fr.get('source','v2/ontology/source/modules/*.ttl'))}
- review/evolution package: {code('v2/review/version-evolution.md')}
"""
        content+=doc_record(authority_ref,"V2 Concept Evidence Passport, conceptual registry and formal ontology",
                            "Generated concept reference; registered review/evidence status preserved")
        add_page(name,slug,"Reference / Index",content)

    # object properties
    for p in sorted(formal["object"]):
        e=formal["object"][p]; rr=rel_review[p]
        name=object_names[p]; slug=slugify(name)
        dom=e["domain"] or "unspecified"; rng=e["range"] or "unspecified"
        def endpoint_link(v):
            if v.startswith("cmpe:"): v=v.split(":",1)[1]
            return wiki(concept_names[v],v) if v in concept_names else code(v)
        characteristics=[]
        if e.get("material"): characteristics.append("Explicitly marked as material relation.")
        if e.get("derived"): characteristics.append("Derived from relator "+code(e["derived"])+".")
        if not characteristics: characteristics.append("No inverse/material/derived characteristic is asserted by the parsed statement.")
        example=(endpoint_link(dom)+" — "+code(p)+" → "+endpoint_link(rng)) if dom!="unspecified" and rng!="unspecified" else "No complete domain→range structural example is asserted because at least one endpoint is formally unspecified."
        content=f"""# {p}

> **Version scope:** V2  
> **Status:** {rr['status']} relation review  
> **Updated:** 2026-09-24

> Generated object-property reference. Missing domain/range values remain **unspecified** and are never inferred by this page.

## Formal definition
| Field | Value |
|---|---|
| IRI | {code('cmpe:'+p)} |
| Property type | OWL ObjectProperty |
| Domain | {endpoint_link(dom)} |
| Range | {endpoint_link(rng)} |
| Formal layer | {rr['layer']} |

## Semantic / review note
{rr['note']}

## Related concepts
- **Domain/source:** {endpoint_link(dom)}
- **Range/target:** {endpoint_link(rng)}

## Formal characteristics
{chr(10).join('- '+x for x in characteristics)}

## Structural example
{example}

## Review boundary
- **Review state:** {rr['status']}
- Unspecified endpoints are review targets, not automatically defects.
- Catalog generation does not approve relation semantics.

## Authoritative sources
- formal source: {code(e['source'])}
- relation review catalog: {code('v2/review/relations/index.md')}
- integrated conceptual model: {code('v2/research/w4/integrated-ontouml-model.md')}
"""
        content+=doc_record(authority_ref,"V2 formal ontology and relation-review catalog",
                            "Generated object-property reference; missing constraints not inferred")
        add_page(name,slug,"Reference / Index",content)

    # datatype properties
    for p in sorted(formal["datatype_property"]):
        e=formal["datatype_property"][p]
        name=datatype_names[p]; slug=slugify(name)
        dom=e["domain"] or "unspecified"; rng=e["range"] or "unspecified"
        dom_display=wiki(concept_names[dom],dom) if dom in concept_names else code(dom)
        rng_display=code(rng)
        example=(dom_display+" — "+code(p)+" → "+rng_display) if dom!="unspecified" and rng!="unspecified" else "No complete domain→range structural example is asserted because at least one endpoint is formally unspecified."
        content=f"""# {p}

> **Version scope:** V2  
> **Status:** Formal baseline reference  
> **Updated:** 2026-09-24

> Generated datatype-property reference from the formal ontology. It is not counted among the 52 object-property relation-review records.

## Formal definition
| Field | Value |
|---|---|
| IRI | {code('cmpe:'+p)} |
| Property type | OWL DatatypeProperty |
| Domain | {dom_display} |
| Range | {rng_display} |
| Formal module | {code(e.get('source',''))} |

## Semantic role
This property connects a modeled entity to a literal value under the explicit formal domain/range constraints shown above.

## Related concepts
- **Domain:** {dom_display}
- **Literal range:** {rng_display}

## Structural example
{example}

## Review boundary
- No inverse semantics are inferred.
- Missing domain/range constraints remain unspecified.
- Datatype-property presence does not change the 87 conceptual-element count.

## Authoritative sources
- formal source: {code(e['source'])}
- formal baseline: {code('v2/ontology/baseline/formal-baseline.json')}
"""
        content+=doc_record(authority_ref,"V2 formal ontology",
                            "Generated datatype-property reference")
        add_page(name,slug,"Reference / Index",content)

    # reference index
    mod_lines=["| # | Module | Layer | Concepts | Review |","|---:|---|---|---:|---|"]
    for d in domains:
        mod_lines.append("| %d | %s | %s | %d | %s |"%(d["number"],wiki(module_names[d["name"]],d["name"]),d["layer"],len(concepts_by_domain[d["name"]]),d["review"]))
    con_lines=["| # | Concept | Domain | Stereotype | Formal type | Review |","|---:|---|---|---|---|---|"]
    for c in concepts:
        con_lines.append("| %d | %s | %s | %s | %s | %s |"%(c["number"],wiki(concept_names[c["local"]],c["label"]),c["domain"],c["stereotype"],c["formal_type"],c["review_status"]))
    op_lines=["| Property | Layer | Domain | Range | Review |","|---|---|---|---|---|"]
    for p in sorted(formal["object"]):
        rr=rel_review[p]; e=formal["object"][p]
        op_lines.append("| %s | %s | %s | %s | %s |"%(wiki(object_names[p],code(p)),rr["layer"],e["domain"] or "unspecified",e["range"] or "unspecified",rr["status"]))
    dp_lines=["| Property | Domain | Range |","|---|---|---|"]
    for p in sorted(formal["datatype_property"]):
        e=formal["datatype_property"][p]
        dp_lines.append("| %s | %s | %s |"%(wiki(datatype_names[p],code(p)),e["domain"] or "unspecified",e["range"] or "unspecified"))

    ref_content=f"""# V2 Ontology Reference

> **Version scope:** V2  
> **Status:** Stable-to-date / Evolving; semantic review pending  
> **Updated:** 2026-09-24

This is the exhaustive reader-facing reference projection for the current CM-PharmE 2.0 conceptual/formal baseline. It combines curated navigation with deterministic entity references generated from the V2 authority at {code(authority_ref)}.

## Purpose and scope
Use this reference to discover modules, conceptual elements and formal properties, then follow the authoritative source links for semantic/evidence decisions. The reference does not replace the ontology source or semantic-review process.

## Architecture
- **Conceptual elements:** 87
- **OWL classes:** 81
- **Declared conceptual/formal datatypes:** 6
- **Object properties:** 52
- **Datatype properties:** 5
- **Review taxonomy:** 17 domains/modules
- **Conceptual layers:** Core / X-INFRA / Extensions

The 87 conceptual elements are **not** 87 OWL classes: 81 formalize as OWL classes and 6 as declared datatypes.

## Namespace and version
- target namespace: {code('https://w3id.org/cm-pharme/2.0/')}
- formal development version: {code('2.0.0-alpha.1')}
- conceptual registry: {code('Gate-D-2026-08-19')}
- external w3id redirect deployment/registration remains outside the documentation claim.

## Formalization strategy
The conceptual registry preserves the UFO/OntoUML decisions. OWL/SHACL formalization may add implementation structure but may not silently reverse approved identity/dependence commitments. Generated reference pages report explicit formal constraints and do not infer absent endpoints.

## Relationship to V1
See {wiki('V1 to V2 Research Evolution')}, {wiki('V1 to V2 Concept Migration')} and {wiki('V1 to V2 Relation Migration')}. V2 is a controlled research evolution; predecessor semantics and V2-new distinctions are not conflated.

## How to use this reference
1. Start with a module below.
2. Open a concept page for definition, stereotype, formal entity, provenance and review state.
3. Follow principal object-property references for explicit formal relations.
4. Use datatype-property pages for literal-valued implementation properties.
5. Follow authority links when a semantic decision or review disposition matters.

## Module reference
{chr(10).join(mod_lines)}

## Concept reference — 87 conceptual elements
{chr(10).join(con_lines)}

## Object-property reference — 52 properties
{chr(10).join(op_lines)}

## Datatype-property reference — 5 properties
{chr(10).join(dp_lines)}

## Generated vs curated boundary
The exhaustive tables/pages are generated for discoverability and coverage. Curated interpretation remains in {wiki('V2 UFO and OntoUML Architecture')}, {wiki('V2 Formal Ontology and SHACL')}, {wiki('V2 Human Ontology Review','CM-PharmE 2.0 Semantic Review')} and cross-version research pages.

## Review boundary
Concept and relation review remains pending where the V2 review artifacts say pending. Generated presence is not approval. Accepted semantic findings later flow through #213 and trigger regeneration.

## Reference-generation evidence
See repository files:
- {code('wiki-src/ontology-reference/coverage.json')}
- {code('wiki-src/ontology-reference/coverage.csv')}
- {code('wiki-src/ontology-reference/MISSING-ITEMS.md')}
- {code('wiki-src/ontology-reference/GENERATED-VS-CURATED.md')}
- {code('wiki-src/ontology-reference/SOURCE-OF-TRUTH.md')}
"""
    ref_content+=doc_record(authority_ref,"V2 conceptual registry, review passports/catalogs and formal ontology",
                            "Generated exhaustive reference projection; semantic authority remains in V2 sources")
    add_page(ref_name,ref_slug,"Reference / Index",ref_content)

    # coverage
    coverage={
        "schema_version":1,
        "issue":234,
        "authority_ref":authority_ref,
        "expected":expected,
        "actual":actual,
        "generated":{
            "module_pages":len(domains),
            "concept_pages":len(concepts),
            "object_property_pages":len(formal["object"]),
            "datatype_property_pages":len(formal["datatype_property"]),
            "reference_index_pages":1,
            "total_generated_reference_pages":1+len(domains)+len(concepts)+len(formal["object"])+len(formal["datatype_property"])
        },
        "unmatched_formal_concept_entities":unmatched_formal,
        "errors":errors,
    }
    outdir=WIKI/"ontology-reference"
    outdir.mkdir(parents=True,exist_ok=True)
    (outdir/"coverage.json").write_text(json.dumps(coverage,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    with (outdir/"coverage.csv").open("w",encoding="utf-8",newline="") as fh:
        w=csv.writer(fh); w.writerow(["category","expected","actual","status"])
        for k in ["domains","concepts","classes","datatypes","object_properties","datatype_properties"]:
            w.writerow([k,expected[k],actual[k],"PASS" if expected[k]==actual[k] else "FAIL"])
    missing=["# V2 ontology reference missing-item register","","Authority ref: "+code(authority_ref),""]
    if errors:
        missing+=["## Blocking discrepancies"]+["- "+e for e in errors]
    else:
        missing+=["## Result","**No blocking coverage gaps detected.**","",
                  "- 87/87 conceptual elements have Concept Evidence Passports and generated reference pages.",
                  "- 87/87 conceptual elements map to the formal conceptual implementation: 81 OWL classes + 6 declared datatypes.",
                  "- 52/52 object properties have generated reference pages and relation-review records.",
                  "- 5/5 datatype properties have generated reference pages.",
                  "- 17/17 review domains/modules have generated landing pages.",
                  "",
                  "Pending human/author review is a semantic-review state, not a documentation coverage gap."]
    (outdir/"MISSING-ITEMS.md").write_text("\n".join(missing)+"\n",encoding="utf-8")

    if errors:
        print(json.dumps(coverage,indent=2))
        raise SystemExit("ontology reference coverage failed")

    # inventory: replace prior #234 generated rows
    with INVENTORY.open(encoding="utf-8",newline="") as fh:
        rows=list(csv.reader(fh))
    header=rows[0]
    kept=[header]+[r for r in rows[1:] if len(r)<7 or r[6]!="234"]
    all_rows=kept+page_rows
    with INVENTORY.open("w",encoding="utf-8",newline="") as fh:
        csv.writer(fh).writerows(all_rows)

    # Home direct shortcut -> keeps generated leaves within depth 2.
    home=PAGES/"Home.md"
    ht=home.read_text(encoding="utf-8")
    shortcut="- **Open the exhaustive V2 ontology reference:** [[V2 Ontology Reference]]\n"
    if shortcut not in ht:
        anchor="- **Explore the conceptual model and ontology:** [[Ontology and Conceptual Model Guide]]\n"
        ht=ht.replace(anchor,anchor+shortcut)
        home.write_text(ht,encoding="utf-8")

    guide=PAGES/"Ontology-and-Conceptual-Model-Guide.md"
    gt=guide.read_text(encoding="utf-8")
    if "[[V2 Ontology Reference]]" not in gt:
        gt=gt.replace("## V2 conceptual and formal architecture","## V2 exhaustive reference\n- [[V2 Ontology Reference]] — 17 modules, 87 conceptual elements, 52 object properties and 5 datatype properties.\n\n## V2 conceptual and formal architecture")
        guide.write_text(gt,encoding="utf-8")

    sidebar=PAGES/"_Sidebar.md"
    st=sidebar.read_text(encoding="utf-8")
    if "[[V2 Ontology Reference]]" not in st:
        st=st.replace("**Conceptual Model & Ontology**\n- [[Ontology and Conceptual Model Guide]]",
                      "**Conceptual Model & Ontology**\n- [[Ontology and Conceptual Model Guide]]\n- [[V2 Ontology Reference]]")
        sidebar.write_text(st,encoding="utf-8")

    print(json.dumps(coverage,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
