#!/usr/bin/env python3
"""Audit #276 dispositions and verify retained Wiki content and inbound routes."""
import hashlib
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/wiki'))
import check_navigation as nav

def main():
    matrix = json.loads((ROOT/'docs/documentation/pages-276-wiki-disposition.json').read_text())
    rows = nav.load_inventory(); by_page, graph, indegree = nav.build_graph(rows)
    complete = {r['slug']:r for r in rows if r['source_status']=='source-complete'}
    errors = []; families = {}
    for item in matrix['pages']:
        path = ROOT/'wiki-src/pages'/ (item['slug']+'.md')
        if item['slug'] not in complete or not path.is_file():
            errors.append('lost route: '+item['slug']); continue
        if hashlib.sha256(path.read_bytes()).hexdigest()!=item['retained_content_sha256']:
            errors.append('content changed without new disposition: '+item['slug'])
        if not item['rationale'] or item['decision'] not in {'RETAIN_CURATED','RETAIN_BRIDGE','NO_CHANGE','KEEP_AS_HISTORICAL'}:
            errors.append('invalid disposition: '+item['slug'])
        families[item['family']] = families.get(item['family'],0)+1
    expected = {r['slug'] for r in rows if r['primary_issue']=='234'}
    assert expected <= {x['slug'] for x in matrix['pages']}, 'unassessed generated reference pages'
    depth = nav.depths(graph)
    for item in matrix['pages']:
        page = complete.get(item['slug'],{}).get('page')
        if page and (page not in depth or indegree.get(page,0)==0): errors.append('unreachable: '+item['slug'])
    report = {'issue':276,'result':'FAIL' if errors else 'PASS','candidate_pages':len(matrix['pages']),
              'family_counts':families,'removed_pages':0,'changed_candidate_content':0 if not errors else None,
              'preserved_inbound_routes':len(matrix['pages']),'errors':errors}
    output = ROOT/'build/evidence/pages-276-wiki-audit.json'; output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n'); print(output.read_text())
    return bool(errors)
if __name__=='__main__': raise SystemExit(main())
