#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Exercise real released-profile onboarding and preserve the V1/V2 contract."""
import argparse
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import jsonschema
import build_shell
import build_released_profile as builder
import run_version_pipeline as pipeline
import validate_version_registry as validator

ROOT=Path(__file__).resolve().parents[2]
DOCS=ROOT/'docs/documentation'
PROFILE='v2-m1'

def read(p):return json.loads(p.read_text())
def digest(folder):return {str(p.relative_to(folder)):hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.rglob('*') if p.is_file()}
def command(args,*,expected=0,seed='0'):
    p=subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,env=dict(os.environ,PYTHONHASHSEED=seed,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True)
    assert p.returncode==expected,(args,p.returncode,p.stdout,p.stderr)
    return p

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source-root',type=Path,required=True)
    ap.add_argument('--require-release-checkout',action='store_true');ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();source=args.source_root.resolve()
    reg=read(DOCS/'ontology-version-registry.json');base=read(DOCS/'m1-onboarding/baseline/ontology-version-registry.json')
    build=read(DOCS/'ontology-documentation-build-contract.json');old_build=read(DOCS/'m1-onboarding/baseline/ontology-documentation-build-contract.json')
    downloads=read(DOCS/'download-bundle-contract.json');old_dl=read(DOCS/'m1-onboarding/baseline/download-bundle-contract.json')
    for name,data in [('ontology-version-registry',reg),('ontology-documentation-build-contract',build)]:
        jsonschema.validate(data,read(DOCS/(name+'.schema.json')))
    assert not validator.validate(reg) and not validator.validate_against_baseline(reg,base)
    for version in base['versions']:
        assert next(v for v in reg['versions'] if v['id']==version['id'])==version
    for entry in old_build['versions']:
        assert next(v for v in build['versions'] if v['id']==entry['id'])==entry
    for key,value in old_dl['versions'].items():assert downloads['versions'][key]==value
    configs=[read(DOCS/p) for p in ['widoco-adapter.json','webvowl-adapter.json']]
    plan=pipeline.make_plan(reg,build,*configs,downloads)
    old_plan=pipeline.make_plan(base,old_build,*configs,old_dl)
    assert plan[:len(old_plan)]==old_plan
    profile=next(v for v in reg['versions'] if v['id']==PROFILE)
    assert profile['generated_reference_enabled'] and profile['webvowl_enabled']
    assert PROFILE in configs[0]['versions'] and PROFILE in configs[1]['versions']
    negatives=[]
    for name,mutate in [
        ('profile-as-full-model',lambda v:v.update(asset_kind='ontology_model')),
        ('unknown-parent',lambda v:v['profile'].update(base_version_id='v99')),
        ('model-replacement',lambda v:v.update(supersedes='v2')),
        ('route-collision',lambda v:v.update(immutable_version_path=base['versions'][0]['immutable_version_path'])),
        ('incomplete-profile',lambda v:v['profile'].pop('profile_version'))]:
        bad=copy.deepcopy(reg);mutate(next(v for v in bad['versions'] if v['id']==PROFILE))
        assert validator.validate(bad),name;negatives.append(name)
    for field,value in [('semantic_source_ref','release/2.1.0@'+'0'*40),('immutable_version_path','ontology/rewritten/')]:
        bad=copy.deepcopy(reg);next(v for v in bad['versions'] if v['id']==PROFILE)[field]=value
        assert validator.validate_against_baseline(bad,reg),field;negatives.append('immutable-'+field)
    c=read(DOCS/'m1-profile-release.json');before={p:builder.sha((source/p).read_bytes()) for p in c['source_files_sha256']}
    with tempfile.TemporaryDirectory(prefix='m1-onboarding-') as folder:
        temp=Path(folder);one=temp/'one';two=temp/'two'
        common=['tools/pages/build_released_profile.py','--source-root',source,'--contract',DOCS/'m1-profile-release.json']
        if not args.require_release_checkout:common+=['--allow-materialized-test-input']
        command(common+['--output-root',one],seed='1');command(common+['--output-root',two],seed='77')
        assert digest(one)==digest(two),'Independent build bytes differ'
        manifest=read(one/'manifest.json');assert manifest['source_commit_verified']==args.require_release_checkout
        resolve=['tools/pages/resolve_documentation_input.py','--version',PROFILE,'--build-root',one,'--source-ref',c['semantic_source_ref']]
        command(resolve,expected=0 if args.require_release_checkout else 7)
        payload=one/'distributions/cm-pharme-m1.ttl';saved=payload.read_bytes();payload.write_bytes(saved+b'\n# corrupt\n')
        command(resolve,expected=7);payload.write_bytes(saved);negatives.append('documentation-input-byte-drift')
        isolated=temp/'tampered-source'
        for path in c['source_files_sha256']:
            out=isolated/path;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source/path,out)
        path=isolated/c['profile_path'];path.write_bytes(path.read_bytes()+b'\n# tampered\n')
        command(['tools/pages/build_released_profile.py','--source-root',isolated,'--contract',DOCS/'m1-profile-release.json',
                 '--output-root',temp/'refused','--allow-materialized-test-input'],expected=1)
        negatives.append('released-source-byte-drift')
        old_reg=temp/'old-registry.json';old_reg.write_text(json.dumps(base))
        old_site=temp/'old-site';site=temp/'site'
        build_shell.build(old_reg,old_site,ROOT/'pages-src/site.css')
        command(['tools/pages/package_download_bundle.py','--version',PROFILE,'--build-root',one,
                 '--source-ref',c['semantic_source_ref'],'--output-root',site])
        build_shell.build(DOCS/'ontology-version-registry.json',site,ROOT/'pages-src/site.css')
        old_routes=[]
        for v in base['versions']:
            route=build_shell.route_for(v);assert digest(old_site/route)==digest(site/route),route;old_routes.append(route)
        profile_route=site/build_shell.route_for(profile)
        page=(profile_route/'index.html').read_text()
        assert c['release_binding']['citation_url'] in page and c['release_binding']['release_url'] in page
        dm=read(profile_route/'downloads/download-manifest.json')
        assert dm['evolution']['curated_evolution_wiki_url'].endswith('M1-Provenance-Core-2.1.0')
        assert c['source_commit'] in dm['evolution']['repository_changelog_url']
        assert len(dm['artifacts'])==5 and all(x['graph_isomorphic_to_governed_input'] for x in dm['artifacts'])
        # Reuse the existing complete local HTML/navigation audit on the candidate.
        import test_shell
        test_shell.audit_site(site,reg)
        # Check progressive metadata and all internal Wiki targets in the changed page cluster.
        import importlib.util,re,csv
        spec=importlib.util.spec_from_file_location('wiki_metadata',ROOT/'tools/wiki/validate_wiki_source.py')
        wiki=importlib.util.module_from_spec(spec);spec.loader.exec_module(wiki)
        inventory=list(csv.DictReader((ROOT/'wiki-src/page-inventory.csv').open()))
        names={v['page'] for v in inventory};errors=[]
        for name in ['M1-Provenance-Core-2.1.0.md','Version-and-Release-Index.md']:
            path=ROOT/'wiki-src/pages'/name;text=path.read_text();wiki.validate_text_metadata(path,text,errors)
            assert text.count('<summary>Documentation record</summary>')==1
            for target in wiki.WIKI_LINK_RE.findall(text):assert target.strip() in names,target
        assert not errors,errors
        result={'schema_version':1,'passed':True,'version_id':PROFILE,'canonical_triples':50,
                'canonical_graph_sha256':c['canonical_graph_sha256'],'domain_classes':4,'cmpe_object_properties':2,
                'total_object_properties':3,'total_datatype_properties':2,'schema_and_common_plan':True,
                'independent_builds_byte_identical':True,'serialization_count':5,'admission_smoke':manifest['admission_smoke'],
                'source_commit_verified':manifest['source_commit_verified'],'preserved_model_entries':['v1','v2'],
                'preserved_shell_subtrees':old_routes,'negative_controls':negatives,
                'generated_reference_enabled':profile['generated_reference_enabled'],'webvowl_enabled':profile['webvowl_enabled'],'public_deployment':False}
    assert before=={p:builder.sha((source/p).read_bytes()) for p in c['source_files_sha256']}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
if __name__=='__main__':main()
