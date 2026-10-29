#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Audit released M1 entity coverage and compare retained prior subtree receipts."""
import hashlib,json
from pathlib import Path
from rdflib import Graph,RDF,OWL
ROOT=Path(__file__).resolve().parents[2]
def tree(folder):return {str(p.relative_to(folder)):hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.rglob('*') if p.is_file()}
def main():
 site=ROOT/'build/site';route=site/'ontology/2.1.0/m1';c=json.loads((ROOT/'docs/documentation/m1-profile-release.json').read_text())
 ttl=ROOT/'build/input/v2-m1/distributions/cm-pharme-m1.ttl';g=Graph().parse(ttl)
 vowl=json.loads((route/'explore/webvowl/data/cmpe.json').read_text())
 classes={x['iri'] for x in vowl.get('classAttribute',[]) if 'iri' in x};properties={x['iri'] for x in vowl.get('propertyAttribute',[]) if 'iri' in x}
 required_classes={str(x) for x in g.subjects(RDF.type,OWL.Class)}
 required_properties={str(x) for t in [OWL.ObjectProperty,OWL.DatatypeProperty] for x in g.subjects(RDF.type,t)}
 assert required_classes<=classes,required_classes-classes
 assert required_properties<=properties,required_properties-properties
 qa=json.loads((ROOT/'build/evidence/v2-m1-widoco-qa.json').read_text());assert qa['overall']=='PASS'
 assert all(x['missing_count']==0 for x in qa['generated_reference_coverage'].values())
 manifest=json.loads((route/'explore/explorer-manifest.json').read_text());assert manifest['semantic_source_ref']==c['semantic_source_ref']
 assert manifest['ontology_selector_disabled'] and manifest['bundled_dataset_count']==1
 old=json.loads((ROOT/'docs/documentation/converter-identity-341/ci-evidence.json').read_text())
 hashes=[]
 for v in old['future_onboarding_proof']['prior_version_isolation']:
  if v['version'] not in ['v1','v2']:continue
  sub='ontology/v1.0.0' if v['version']=='v1' else 'ontology/v2/current'
  digest=hashlib.sha256(json.dumps(tree(site/sub),sort_keys=True).encode()).hexdigest()
  assert digest==v['before_tree_sha256'],(v['version'],digest,v['before_tree_sha256'])
  hashes.append({'id':v['version'],'sha256':digest,'changed_files':0})
 result={'issue':338,'result':'PASS','source_ref':c['semantic_source_ref'],'tbox_triples':len(g),'domain_classes':len(c['domain_classes']),'domain_object_properties':len(c['domain_object_properties']),'formal_classes_covered':len(required_classes),'formal_properties_covered':len(required_properties),'vowl_counts':manifest['vowl_counts'],'vowl_json_sha256':manifest['vowl_json_sha256'],'vowl_extra_class_iris':sorted(classes-required_classes),'old_subtrees_unchanged':hashes,'public_deployment':False}
 p=ROOT/'build/evidence/m1-generated-338.json';p.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
