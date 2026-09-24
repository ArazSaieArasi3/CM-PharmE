#!/usr/bin/env python3
import json
from pathlib import Path
from xml.etree import ElementTree as ET

ET.register_namespace("", "http://www.w3.org/2000/svg")

ROOT=Path(__file__).resolve().parents[2]
MANIFEST=ROOT/"wiki-src"/"diagrams"/"manifest.json"

BG_ID="diagram-background"
FG="#24292f"
BG="#ffffff"

def normalize(path: Path):
    text=path.read_text(encoding="utf-8")
    root=ET.fromstring(text)
    if root.tag.split("}")[-1]!="svg":
        raise ValueError(f"{path}: root is not svg")

    root.set("data-theme-safe","true")
    root.set("style",f"color:{FG};background:{BG}")

    children=list(root)
    has_bg=any(ch.tag.split("}")[-1]=="rect" and ch.attrib.get("id")==BG_ID for ch in children)
    if not has_bg:
        ns=""
        if root.tag.startswith("{"):
            ns=root.tag.split("}")[0].strip("{")
        tag=(f"{{{ns}}}rect" if ns else "rect")
        bg=ET.Element(tag,{
            "id":BG_ID,"x":"0","y":"0","width":"100%","height":"100%",
            "fill":BG,"stroke":"none","pointer-events":"none"
        })
        insert_at=0
        for i,ch in enumerate(children):
            if ch.tag.split("}")[-1] in {"title","desc"}:
                insert_at=i+1
        root.insert(insert_at,bg)

    # Preserve currentColor semantics, but anchor currentColor on the SVG itself.
    out=ET.tostring(root,encoding="unicode")
    if not out.startswith("<svg") and "<svg" in out:
        out=out[out.index("<svg"):]
    path.write_text(out+"\n",encoding="utf-8")

def main():
    data=json.loads(MANIFEST.read_text(encoding="utf-8"))
    paths=[]
    for d in data.get("diagrams",[]):
        p=ROOT/d["rendered_path"]
        if p.suffix.lower()==".svg":
            paths.append(p)
    for p in paths:
        normalize(p)
    print(json.dumps({"normalized_svg_count":len(paths),"foreground":FG,"background":BG},indent=2))

if __name__=="__main__":
    main()
