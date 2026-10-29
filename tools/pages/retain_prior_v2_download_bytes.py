#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Retain governed old serialization bytes only after strict identity/graph checks."""
import copy,hashlib,json,shutil
from pathlib import Path
from rdflib import Graph
from rdflib.compare import isomorphic
ROOT=Path(__file__).resolve().parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tree(p):return {str(x.relative_to(p)):sha(x) for x in p.rglob('*') if x.is_file()}
def read(p):return json.loads(p.read_text())
def main():
 relative=Path('ontology/v2/current');old=ROOT/'build/prior-site-341/site'/relative;new=ROOT/'build/site'/relative
 receipt=read(ROOT/'docs/documentation/converter-identity-341/ci-evidence.json');expected=next(x for x in receipt['future_onboarding_proof']['prior_version_isolation'] if x['version']=='v2')['before_tree_sha256']
 a,b=tree(old),tree(new);assert hashlib.sha256(json.dumps(a,sort_keys=True).encode()).hexdigest()==expected,'Prior artifact identity drift'
 changed=[n for n in sorted(set(a)|set(b)) if a.get(n)!=b.get(n)]
 allowed={'downloads/'+n for n in ['cm-pharme-v2.owl','cm-pharme-v2.rdf','cm-pharme-v2.jsonld','download-manifest.json','SHA256SUMS.txt','index.html']}
 assert set(changed)<=allowed,changed
 registry=read(ROOT/'docs/documentation/ontology-version-registry.json');v=next(x for x in registry['versions'] if x['id']=='v2')
 manifests=[read(p/'downloads/download-manifest.json') for p in [old,new]]
 def stable(m):
  m=copy.deepcopy(m)
  for x in m['artifacts']:x.pop('sha256',None);x.pop('bytes',None)
  return m
 assert stable(manifests[0])==stable(manifests[1]),'Download metadata changed beyond serialization checksums'
 graph=Graph().parse(ROOT/'build/input/v2/distributions/cm-pharme-v2.ttl',format='turtle')
 formats={'.ttl':'turtle','.nt':'nt','.owl':'xml','.rdf':'xml','.jsonld':'json-ld'}
 for folder,m in zip([old,new],manifests):
  assert m['semantic_source_ref']==v['semantic_source_ref']
  assert m['canonical_graph_fingerprint_sha256']==v['documentation_input']['fingerprint']
  sums=dict((name,digest) for digest,name in (line.split('  ',1) for line in (folder/'downloads/SHA256SUMS.txt').read_text().splitlines() if line))
  for name,digest in sums.items():assert sha(folder/'downloads'/name)==digest,name
  assert len(m['artifacts'])==5
  for artifact in m['artifacts']:
   path=folder/'downloads'/artifact['filename'];assert sha(path)==artifact['sha256']
   assert isomorphic(graph,Graph().parse(path,format=formats[path.suffix])),path
 old_html=(old/'downloads/index.html').read_text();current_html=(new/'downloads/index.html').read_text()
 for before,after in zip(manifests[0]['artifacts'],manifests[1]['artifacts']):
  assert before['filename']==after['filename']
  current_html=current_html.replace(after['sha256'],before['sha256'])
 assert current_html==old_html,'Rendered page differs beyond verified checksums'
 for name in changed:shutil.copyfile(old/name,new/name)
 assert tree(new)==a,'Old byte identity was not retained'
 result={'result':'PASS','prior_run':40954904319,'artifact_id':12934165079,'source_ref':v['semantic_source_ref'],'reused_changed_paths':changed,'all_ten_serializations_isomorphic_to_fresh_governed_input':True,'all_old_and_new_checksums_verified':True,'prior_subtree_sha256':expected,'semantic_source_changed':False}
 (ROOT/'build/evidence/retained-v2-serialization-bytes.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
