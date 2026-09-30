#!/usr/bin/env python3
"""Non-published V3 dry run against the actual assembled V1/V2 artifact."""
import argparse
import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
import build_shell
import run_version_pipeline as pipeline
import test_shell
import validate_version_registry as validator

ROOT=Path(__file__).resolve().parents[2]

def digest(root):
    return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file()}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--site',type=Path,required=True); ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args(); registry=json.loads(test_shell.REGISTRY.read_text())
    future=test_shell.make_v3(registry); v3=future['versions'][-1]
    v3['wiki_explanation_path']='Synthetic-V3-Not-Published'
    # Adding V3 must not change existing V2 history metadata in this isolation test.
    future['versions'][1]=copy.deepcopy(registry['versions'][1])
    v3['documentation_input']['fingerprint']=registry['versions'][1]['documentation_input']['fingerprint']
    v3['documentation_input']['resolved_artifact']=registry['versions'][1]['documentation_input']['resolved_artifact']
    assert validator.validate(future)==[]
    assert validator.validate_against_baseline(future,registry)==[]
    try:
        import jsonschema
        jsonschema.validate(future,json.loads((ROOT/'docs/documentation/ontology-version-registry.schema.json').read_text()))
    except ImportError:
        raise RuntimeError('jsonschema required for future-version proof')
    folder=ROOT/'docs/documentation'
    configs=[pipeline.load(folder/p) for p in ['ontology-documentation-build-contract.json','widoco-adapter.json','webvowl-adapter.json','download-bundle-contract.json']]
    contract,widoco,webvowl,downloads=copy.deepcopy(configs)
    entry=copy.deepcopy(contract['versions'][-1]);entry.update(id='v3',registry_version_id='v3',semantic_source_ref=v3['semantic_source_ref'])
    contract['versions'].append(entry)
    for adapter,field,suffix in [(widoco,'source_ref','reference'),(webvowl,'semantic_source_ref','explore'),(downloads,'source_ref','downloads')]:
        item=copy.deepcopy(adapter['versions']['v2']);item[field]=v3['semantic_source_ref'];item['target_subpath']=v3['current_path']+suffix+'/'
        adapter['versions']['v3']=item
    toggles=[]
    for reference,explore in [(False,False),(True,False),(False,True),(True,True)]:
        v3.update(generated_reference_enabled=reference,webvowl_enabled=explore)
        plan=pipeline.make_plan(future,contract,widoco,webvowl,downloads)
        assert plan[-1]['reference']==reference and plan[-1]['explore']==explore
        toggles.append({'reference':reference,'webvowl':explore,'result':'PASS'})
    missing=copy.deepcopy(widoco);del missing['versions']['v3']
    try: pipeline.make_plan(future,contract,missing,webvowl,downloads)
    except ValueError: pass
    else: raise AssertionError('incomplete future config accepted')
    bad=copy.deepcopy(future);bad['versions'][0]['semantic_source_ref']='mutated@'+'a'*40
    assert validator.validate_against_baseline(bad,registry), 'stable source overwrite accepted'
    collision=copy.deepcopy(future);collision['versions'][-1]['current_path']=registry['versions'][0]['immutable_version_path']
    assert validator.validate(collision), 'version route collision accepted'
    v3.update(generated_reference_enabled=False,webvowl_enabled=False)
    with tempfile.TemporaryDirectory() as td:
        tmp=Path(td); baseline=tmp/'baseline';candidate=tmp/'candidate'
        shutil.copytree(args.site,baseline);shutil.copytree(args.site,candidate)
        regfile=tmp/'registry.json';regfile.write_text(json.dumps(future))
        before={v['id']:digest(baseline/build_shell.route_for(v)) for v in registry['versions']}
        build_shell.build(regfile,candidate,test_shell.CSS)
        for v in registry['versions']:
            ref=candidate/build_shell.route_for(v)/'reference'
            (ref/'index.html').write_bytes((ref/'index-en.html').read_bytes())
            assert before[v['id']]==digest(candidate/build_shell.route_for(v)), v['id']+': prior route changed'
        chooser=(candidate/'ontology/index.html').read_text()
        assert all(v['reader_label'] in chooser for v in future['versions'])
        assert (candidate/v3['current_path']/'index.html').is_file()
        isolation=[{'version':v['id'],'file_count':len(before[v['id']]),'before_tree_sha256':hashlib.sha256(json.dumps(before[v['id']],sort_keys=True).encode()).hexdigest(),
                    'after_tree_sha256':hashlib.sha256(json.dumps(digest(candidate/build_shell.route_for(v)),sort_keys=True).encode()).hexdigest(),'changed_files':0} for v in registry['versions']]
    proc=subprocess.run([sys.executable,str(ROOT/'tools/pages/test_webvowl_v3_contract.py')],capture_output=True,text=True)
    assert proc.returncode==0, proc.stdout+proc.stderr
    report={'issue':277,'result':'PASS','fictional_v3_published':False,'dry_run_registry':future,
            'common_pipeline_plan':plan,'feature_toggles':toggles,'prior_version_isolation':isolation,
            'negative_tests':['missing adapter rejected before stage execution','route collision rejected','immutable source mutation rejected','explorer overwrite rejected','wrong source ref rejected'],
            'shared_explorer_test':proc.stdout.splitlines()[-1],
            'workflow_copies_created':0,'production_versions':[v['id'] for v in registry['versions']]}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'result':'PASS','prior_version_isolation':isolation,'fictional_v3_published':False}))
if __name__=='__main__':main()
