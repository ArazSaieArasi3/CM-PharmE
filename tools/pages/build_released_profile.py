#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Resolve a byte-pinned released profile into the common Pages build interface."""
import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

from rdflib import Graph, OWL, RDF
from rdflib.compare import isomorphic, to_canonical_graph

def sha(data):return hashlib.sha256(data).hexdigest()
def require(ok,message):
    if not ok:raise ValueError(message)
def canonical(graph):
    return ''.join(sorted(f'{s.n3()} {p.n3()} {o.n3()} .\n' for s,p,o in to_canonical_graph(graph))).encode()
def safe_file(root,path):
    relative=Path(path);file=root/relative
    require(not relative.is_absolute() and '..' not in relative.parts,'Unsafe source path')
    require(file.is_file() and not file.is_symlink() and file.resolve().is_relative_to(root),'Missing/unsafe source file: '+path)
    return file
def stable_json(value):
    if isinstance(value,dict):return {k:stable_json(v) for k,v in sorted(value.items())}
    if isinstance(value,list):return sorted((stable_json(x) for x in value),key=lambda x:json.dumps(x,sort_keys=True))
    return value
def stable_xml(graph):
    root=ET.fromstring(graph.serialize(format='xml'))
    def order(node):
        if node.text and not node.text.strip():node.text=None
        node.tail=None
        for child in node:order(child)
        node[:]=sorted(node,key=lambda n:(n.tag,tuple(sorted(n.attrib.items())),n.text or '',ET.tostring(n)))
    order(root)
    return (ET.canonicalize(ET.tostring(root,encoding='unicode'),rewrite_prefixes=True)+'\n').encode()

def build(source_root,contract_path,output_root,allow_materialized=False):
    source_root=source_root.resolve();output_root=output_root.resolve()
    c=json.loads(contract_path.read_text())
    require(not output_root.is_relative_to(source_root),'Output must be isolated from the released source')
    require(not output_root.exists() or not any(output_root.iterdir()),'Refusing to overwrite a build output')
    verified=False
    if (source_root/'.git').exists():
        actual=subprocess.check_output(['git','-C',str(source_root),'rev-parse','HEAD'],text=True).strip()
        require(actual==c['source_commit'],'Released source commit mismatch');verified=True
    else:require(allow_materialized,'Exact source checkout required; materialized mode is explicit and test-only')
    source_files={}
    for path,expected in c['source_files_sha256'].items():
        data=safe_file(source_root,path).read_bytes()
        require(sha(data)==expected,'Released source hash mismatch: '+path);source_files[path]=data
    profile_path=safe_file(source_root,c['profile_path'])
    graph=Graph().parse(profile_path,format='turtle')
    nt=canonical(graph)
    require(sha(nt)==c['canonical_graph_sha256'],'Released profile graph mismatch')
    require(len(graph)==c['expected_triples'] and not list(graph.triples((None,OWL.imports,None))),'Profile scope/import mismatch')
    namespace=c['domain_namespace']
    classes=sorted(str(x) for x in graph.subjects(RDF.type,OWL.Class))
    objects=sorted(str(x) for x in graph.subjects(RDF.type,OWL.ObjectProperty))
    data_properties=sorted(str(x) for x in graph.subjects(RDF.type,OWL.DatatypeProperty))
    require(classes==c['domain_classes'],'Released class signature changed')
    require([x for x in objects if x.startswith(namespace)]==c['domain_object_properties'],'Released object-property signature changed')
    require(len(objects)==c['expected_total_object_properties'] and len(data_properties)==c['expected_total_datatype_properties'],'Infrastructure signature changed')
    spec=importlib.util.spec_from_file_location('released_m1_admission',safe_file(source_root,c['runtime_path']))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    shapes=Graph().parse(safe_file(source_root,c['shapes_path']))
    smoke=[]
    for witness in c['admission_witnesses']:
        result=module.admit(Graph().parse(safe_file(source_root,witness['path'])),graph,shapes)
        require(result['stage']==witness['expected_stage'],'Released admission smoke differs')
        smoke.append({'id':witness['id'],'stage':result['stage']})
    dist=output_root/'distributions';dist.mkdir(parents=True)
    stem=c['artifact_stem'];xml=stable_xml(graph)
    artifacts={stem+'.ttl':source_files[c['profile_path']],stem+'.nt':nt,stem+'.owl':xml,stem+'.rdf':xml,
               stem+'.jsonld':(json.dumps(stable_json(json.loads(graph.serialize(format='json-ld'))),sort_keys=True,indent=2)+'\n').encode()}
    hashes={}
    for name,payload in artifacts.items():
        path=dist/name;path.write_bytes(payload)
        fmt='turtle' if name.endswith('.ttl') else 'nt' if name.endswith('.nt') else 'json-ld' if name.endswith('.jsonld') else 'xml'
        require(isomorphic(graph,Graph().parse(path,format=fmt)),'Serialization changed the source graph: '+name)
        hashes['distributions/'+name]=sha(payload)
    manifest={'schema_version':1,'asset_kind':'released_profile','source_commit':c['source_commit'],
              'source_commit_verified':verified,'canonical_graph_sha256':sha(nt),'canonical_triples':len(graph),
              'source_files_sha256':c['source_files_sha256'],'artifacts_sha256':hashes,
              'profile_version':c['profile_version'],'distribution_version':c['distribution_version'],
              'domain_classes':classes,'domain_object_properties':c['domain_object_properties'],
              'total_object_properties':len(objects),'total_datatype_properties':len(data_properties),
              'admission_smoke':smoke,'new_formal_reasoner_run_claimed':False,
              'scope':'Pinned released M1 profile only; external vocabulary is counted separately; no full-model acceptance.'}
    (output_root/'manifest.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n')
    return manifest

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-root',type=Path,required=True);p.add_argument('--contract',type=Path,required=True)
    p.add_argument('--output-root',type=Path,required=True)
    p.add_argument('--allow-materialized-test-input',action='store_true')
    a=p.parse_args();m=build(a.source_root,a.contract,a.output_root,a.allow_materialized_test_input)
    print(json.dumps({'passed':True,'canonical_graph_sha256':m['canonical_graph_sha256'],
                      'source_commit_verified':m['source_commit_verified'],'triples':m['canonical_triples']}))
if __name__=='__main__':main()
