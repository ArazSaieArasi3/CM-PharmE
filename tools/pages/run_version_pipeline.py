#!/usr/bin/env python3
"""Run shared publication stages for every configured registry version."""
from __future__ import annotations
import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path
import build_shell
import validate_version_registry as validator

ROOT = Path(__file__).resolve().parents[2]

def load(path): return json.loads(Path(path).read_text())

def make_plan(registry, contract, widoco, webvowl, downloads):
    errors = validator.validate(registry)
    entries = {v['id']:v for v in contract['versions']}; plan=[]
    for v in registry['versions']:
        vid = v['id']; cfg = entries.get(vid)
        if not cfg:
            errors.append(f'{vid}: missing semantic build contract'); continue
        if cfg['semantic_source_ref'] != v['semantic_source_ref']:
            errors.append(f'{vid}: build source mismatch')
        if cfg['expected_fingerprint']['value'] != v['documentation_input']['fingerprint']:
            errors.append(f'{vid}: fingerprint mismatch')
        route=build_shell.route_for(v)
        for adapter, enabled, suffix, ref_field in [(widoco,v['generated_reference_enabled'],'reference','source_ref'),
            (webvowl,v['webvowl_enabled'],'explore','semantic_source_ref'),(downloads,True,'downloads','source_ref')]:
            item=adapter['versions'].get(vid)
            if enabled and (not item or item[ref_field]!=v['semantic_source_ref'] or item['target_subpath']!=route+'/'+suffix+'/'):
                errors.append(f'{vid}: incomplete or inconsistent {suffix} adapter')
        if v['generated_reference_enabled'] and not cfg['build'].get('reference_authority'):
            errors.append(f'{vid}: missing reference coverage authority')
        if '<OUTPUT_ROOT>' not in cfg['build']['command']:
            errors.append(f'{vid}: build output is not isolated')
        plan.append({'id':vid,'route':route,'source_ref':v['semantic_source_ref'],
            'source_sha':v['semantic_source_ref'].rsplit('@',1)[1],
            'build':cfg['build'],'reference':v['generated_reference_enabled'],'explore':v['webvowl_enabled']})
    if errors: raise ValueError('; '.join(errors))
    return plan

def run(argv, cwd=ROOT): subprocess.run([str(x) for x in argv],cwd=cwd,check=True)

def execute(stage, plan):
    for v in plan:
        vid=v['id']; source=ROOT/('source-'+vid); output=ROOT/'build/input'/vid
        artifact=output/v['build']['documentation_input_artifact']; site=ROOT/'build/site'; target=site/v['route']
        values={'<OUTPUT_ROOT>':str(output),'<PAGES_CURRENT_BASELINE>':str(ROOT/'docs/documentation/v2-current-pages-baseline.json'),
                '<SOURCE_ROOT>':str(source),'<PUBLICATION_ROOT>':str(ROOT)}
        def expand(s):
            for a,b in values.items(): s=s.replace(a,b)
            if '<' in s or '>' in s: raise ValueError('unresolved build placeholder: '+s)
            return s
        if stage=='checkout':
            run(['git','fetch','--depth=1','origin',v['source_sha']])
            run(['git','worktree','add','--detach',source,v['source_sha']])
        elif stage=='inputs':
            argv=[expand(x) for x in shlex.split(v['build']['command'])]
            argv[0]=sys.executable
            run(argv,source)
            run([sys.executable,'tools/pages/resolve_documentation_input.py','--version',vid,'--build-root',output,
                 '--source-ref',v['source_ref'],'--output',ROOT/'build/evidence'/f'{vid}-input.json'])
        elif stage=='references' and v['reference']:
            run([sys.executable,'tools/pages/run_widoco.py','--version',vid,'--jar',ROOT/'build/tools/widoco.jar',
                 '--ontology',artifact,'--output',target/'reference','--manifest-output',ROOT/'build/evidence'/f'{vid}-widoco.json'])
            run([sys.executable,'tools/pages/audit_widoco_candidate.py','--version',vid,'--ontology',artifact,
                 '--candidate',target/'reference','--authority',expand(v['build']['reference_authority']),
                 '--output',ROOT/'build/evidence'/f'{vid}-widoco-qa.json'])
        elif stage=='downloads':
            run([sys.executable,'tools/pages/package_download_bundle.py','--version',vid,'--build-root',output,
                 '--source-ref',v['source_ref'],'--output-root',site])
        elif stage=='convert' and v['explore']:
            (ROOT/'build/vowl').mkdir(parents=True,exist_ok=True)
            run(['java','-jar','external/owl2vowl/target/OWL2VOWL-0.3.7-shaded.jar','-file',artifact,
                 '-output',ROOT/'build/vowl'/f'{vid}.json'])
        elif stage=='explorers' and v['explore']:
            run([sys.executable,'tools/pages/build_webvowl_explorer.py','--version',vid,
                 '--frontend-root','external/webvowl/deploy','--vowl-json',ROOT/'build/vowl'/f'{vid}.json',
                 '--ontology-input',artifact,'--source-ref',v['source_ref'],'--output-root',site])
        elif stage=='aliases' and v['reference']:
            (target/'reference/index.html').write_bytes((target/'reference/index-en.html').read_bytes())

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('stage',choices=['plan','checkout','inputs','references','downloads','convert','explorers','aliases'])
    ap.add_argument('--output',type=Path); args=ap.parse_args()
    folder=ROOT/'docs/documentation'
    plan=make_plan(*(load(folder/p) for p in ['ontology-version-registry.json','ontology-documentation-build-contract.json',
                    'widoco-adapter.json','webvowl-adapter.json','download-bundle-contract.json']))
    if args.stage!='plan': execute(args.stage,plan)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(plan,indent=2,sort_keys=True)+'\n')
    print(f'PASS: {args.stage}, {len(plan)} registry versions')

if __name__=='__main__': main()
