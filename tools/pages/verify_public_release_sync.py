#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Verify fresh deployed identity and checksum every publicly advertised download."""
import argparse,hashlib,json,time
from pathlib import Path
from urllib.request import Request,urlopen
ROOT=Path(__file__).resolve().parents[2]
BASE='https://arazsaiearasi3.github.io/CM-PharmE/'
def get(url):
 with urlopen(Request(url,headers={'User-Agent':'CM-PharmE-Release-Sync/1.0','Cache-Control':'no-cache'}),timeout=40) as r:
  assert r.status==200,(url,r.status)
  return r.read()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build-sha',required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 registry=json.loads((ROOT/'docs/documentation/ontology-version-registry.json').read_text())
 manifest=None
 for attempt in range(12):
  manifest=json.loads(get(BASE+'pages-deployment-manifest.json?build='+a.build_sha))
  if manifest['build_commit_sha']==a.build_sha:break
  time.sleep(5)
 assert manifest['build_commit_sha']==a.build_sha,'Public deployment identity is stale'
 assert b'2.1.0/m1' in get(BASE) and b'2.1.0/m1' in get(BASE+'ontology/')
 checked=[]
 for v in registry['versions']:
  route=v.get('immutable_version_path') or v['current_path'];root=BASE+route
  m=json.loads(get(root+'downloads/download-manifest.json'))
  assert m['semantic_source_ref']==v['semantic_source_ref']
  assert m['canonical_graph_fingerprint_sha256']==v['documentation_input']['fingerprint']
  assert len(m['artifacts'])==5
  for x in m['artifacts']:
   url=root+'downloads/'+x['filename'];data=get(url);digest=hashlib.sha256(data).hexdigest();assert digest==x['sha256'],url
   if v['id']=='v2-m1' and x['filename'].endswith('.ttl'):assert digest=='a8dca6788eff03570b4911b8b7f0933a5420fcde9945272543da86934539ce9b'
   checked.append({'version':v['id'],'url':url,'sha256':digest,'bytes':len(data)})
  assert b'citation' in get(root+'citation/').lower()
 assert b'M1-Provenance-Core-2.1.0' in get('https://github.com/ArazSaieArasi3/CM-PharmE/wiki')
 assert b'releases/tag/2.1.0' in get('https://github.com/ArazSaieArasi3/CM-PharmE')
 result={'issue':339,'result':'PASS','deployed_build_commit':a.build_sha,'public_serializations_checked':len(checked),'downloads':checked,'repository_and_wiki_m1_entry_links':True,'semantic_release':'2.1.0'}
 a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
