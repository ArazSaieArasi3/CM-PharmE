#!/usr/bin/env python3
"""Audit assembled Pages candidate download integration."""
from __future__ import annotations
import argparse, hashlib, json
from html.parser import HTMLParser
from pathlib import Path

def sha(path):
    h=hashlib.sha256(path.read_bytes()).hexdigest()
    return h

class P(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="a" and a.get("href"): self.links.append(a["href"])

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--site",type=Path,required=True); args=ap.parse_args()
    versions=["ontology/v1.0.0","ontology/v2/current"]
    checked=0
    for route in versions:
        d=args.site/route/"downloads"
        manifest=json.loads((d/"download-manifest.json").read_text())
        html=(d/"index.html").read_text()
        p=P(); p.feed(html)
        assert "Generated-artifact boundary" in html
        assert "does not replace the curated research-evolution narrative" in html
        for item in manifest["artifacts"]:
            path=d/item["filename"]
            assert path.is_file(), path
            assert sha(path)==item["sha256"], item["filename"]
            assert item["filename"] in p.links, (route,item["filename"])
            checked+=1
        for name in ("download-manifest.json","provenance.json","SHA256SUMS.txt"):
            assert name in p.links
            assert (d/name).is_file()
        prov=(args.site/route/"provenance"/"index.html").read_text()
        assert manifest["semantic_source_ref"] in prov
    print(f"PASS: assembled Pages candidate exposes and checksum-verifies {checked} sample downloads across V1/V2.")

if __name__=="__main__":
    main()
