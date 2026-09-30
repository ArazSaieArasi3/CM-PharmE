#!/usr/bin/env python3
"""Check published Wiki ↔ Pages links and exact-ref reader journeys."""
import argparse
import concurrent.futures
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
PAGES = 'https://arazsaiearasi3.github.io/CM-PharmE/'
REPO = 'https://github.com/ArazSaieArasi3/CM-PharmE'
WIKI = REPO + '/wiki/'

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = set()
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = dict(attrs).get('href')
            if href: self.links.add(href)

def fetch(url):
    with urlopen(Request(url, headers={'User-Agent': 'CM-PharmE-Pages-Audit/1.0'}), timeout=45) as r:
        assert r.status == 200, (url, r.status)
        final = r.url.rstrip('/')
        assert final == url.rstrip('/'), ('unexpected redirect', url, final)
        content = r.read().decode('utf-8')
    p = Links(); p.feed(content)
    return content, p.links

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    registry = json.loads((ROOT/'docs/documentation/ontology-version-registry.json').read_text())
    required = {}; journeys = []
    for v in registry['versions']:
        route = v.get('immutable_version_path') or v['current_path']
        root = PAGES + route; wiki = WIKI + v['wiki_explanation_path']
        sha = v['semantic_source_ref'].rsplit('@', 1)[1]; source = REPO+'/tree/'+sha
        required[wiki] = {root+'reference/', root+'explore/', root+'downloads/', source}
        for sub in ['', 'reference/', 'explore/']:
            required[root+sub] = {wiki, source}
        required[source] = set()
        journeys.append({'version':v['id'], 'wiki':wiki, 'reference':root+'reference/',
                         'explore':root+'explore/', 'source':source, 'max_hops':2})
    required[WIKI+'Ontology-and-Conceptual-Model-Guide'] = {j[k] for j in journeys for k in ['reference','explore','source']}
    required[WIKI+'V2-Ontology-Diagram-Suite'] = {journeys[1]['reference'],journeys[1]['explore'],journeys[1]['source']}
    required[WIKI+'V2-Ontology-Reference'] = {journeys[1]['reference'],journeys[1]['explore']}
    required[WIKI+'Citation-and-Reuse'] = {PAGES+'citation/'}
    required[WIKI+'Reference-Guide'] = set()
    required[PAGES+'citation/'] = set()
    errors = []; checked = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(fetch, url):url for url in required}
        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            try:
                content, links = future.result()
                missing = [x for x in required[url] if not any(h == x or h.startswith(x+'/') for h in links)]
                assert not missing, ('missing published links', missing)
                # A GitHub missing-page fallback can return HTTP 200; check actual article title.
                if '/wiki/' in url:
                    assert 'wiki-body' in content and 'Create new page' not in content.split('wiki-body',1)[-1][:200], 'Wiki fallback'
                checked.append({'url':url,'required_links':sorted(required[url]),'result':'PASS'})
            except Exception as e: errors.append({'url':url,'error':repr(e)})
    report = {'issue':274,'result':'FAIL' if errors else 'PASS', 'checked_surfaces':sorted(checked,key=lambda x:x['url']),
              'reader_journeys':journeys, 'broken_cross_surface_links':len(errors), 'errors':errors}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'result':report['result'],'surfaces':len(checked),'errors':errors}))
    return bool(errors)

if __name__ == '__main__': raise SystemExit(main())
