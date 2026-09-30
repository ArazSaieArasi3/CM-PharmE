#!/usr/bin/env python3
"""Archive exact verified Pages bytes and release evidence with fixed ZIP metadata."""
from __future__ import annotations
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
import audit_widoco_candidate as links

ROOT=Path(__file__).resolve().parents[2]

def sha(data):return hashlib.sha256(data).hexdigest()
def load(p):return json.loads(Path(p).read_text())

def archive(files,path):
    path.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,data in sorted(files.items()):
            info=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            info.create_system=3;info.external_attr=0o100644<<16
            z.writestr(info,data,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--site',type=Path,required=True);ap.add_argument('--evidence',type=Path,required=True)
    ap.add_argument('--release-input',type=Path,required=True);ap.add_argument('--archive',type=Path,required=True);ap.add_argument('--report',type=Path,required=True)
    args=ap.parse_args(); release=load(args.release_input)
    assert release['baseline_id']=='PB-2026.09.1'
    site=load(args.site/'pages-deployment-manifest.json')
    assert site['result']=='PASS' and not site['errors'] and site['build_commit_sha']==release['published_build_commit']
    required={'public-verification.json':'result','public-navigation.json':'result',
              'pages-277-onboarding.json':'result','pages-276-wiki-audit.json':'result',
              'pages-273-final-audit.json':'result','v1-widoco-qa.json':'overall','v2-widoco-qa.json':'overall'}
    reports={}
    for filename,field in required.items():
        data=load(args.evidence/filename);assert data[field]=='PASS',filename;reports[filename]=data
    assert reports['pages-277-onboarding.json']['fictional_v3_published'] is False
    assert reports['public-navigation.json']['broken_cross_surface_links']==0
    assert reports['public-verification.json']['browser_errors']==[]
    wiki=load(args.evidence/'wiki-publish-verification.json')
    assert not wiki['failures'] and wiki['verified_urls']==wiki['expected_source_complete_pages']
    assert wiki['wiki_commit']==release['published_wiki_commit']
    checked,broken=links.audit_links(args.site)
    # These hashes are WebVOWL application route commands, not HTML element IDs.
    app_routes=[x for x in broken if x['reason'].startswith('missing fragment') and
                ((x['source'].endswith('/explore/index.html') and x['target']=='webvowl/index.html#cmpe') or
                 (x['source'].endswith('/explore/webvowl/index.html') and x['target']=='#opts=editorMode=true;#new_ontology1'))]
    broken=[x for x in broken if x not in app_routes]
    assert not broken,broken
    registry=load(ROOT/'docs/documentation/ontology-version-registry.json')
    assert sha((ROOT/'docs/documentation/ontology-version-registry.json').read_bytes())==site['version_registry_sha256']
    assert [v['id'] for v in registry['versions']]==['v1','v2'], 'fictional version in production registry'
    files={}
    for prefix,root in [('site',args.site),('evidence',args.evidence)]:
        for p in sorted(root.rglob('*')):
            assert not p.is_symlink(),p
            if p.is_file(): files[prefix+'/'+p.relative_to(root).as_posix()]=p.read_bytes()
    for directory in ['docs/documentation','pages-src/widoco','tools/pages']:
        for p in sorted((ROOT/directory).rglob('*')):
            if p.is_file() and 'baselines' not in p.parts and '__pycache__' not in p.parts:
                files['source/'+p.relative_to(ROOT).as_posix()]=p.read_bytes()
    files['source/.github/workflows/pages-deploy.yml']=(ROOT/'.github/workflows/pages-deploy.yml').read_bytes()
    files['RELEASE-INPUT.json']=args.release_input.read_bytes()
    inventory={name:sha(data) for name,data in sorted(files.items())}
    record={**release,'decision':'PASS — DECLARE PB-2026.09.1',
            'identity':'Pages/documentation baseline; not an ontology semantic or research release',
            'authority_model':registry['authority_model'],'deployment_manifest':site,
            'route_inventory':load(args.site/'route-inventory.json'),
            'coverage':{v:reports[v+'-widoco-qa.json'] for v in ['v1','v2']},
            'cross_surface_link_audit':reports['public-navigation.json'],
            'wiki_disposition_audit':reports['pages-276-wiki-audit.json'],
            'future_version_proof':reports['pages-277-onboarding.json']['prior_version_isolation'],
            'local_link_audit':{'checked_links_assets':len(checked),'broken_links':0,'application_fragment_routes':app_routes},
            'public_exposure_review':{'result':'PASS','scope':'All exact published files scanned by mandatory deployment preflight; no symlinks or detected private-key/token/restricted-response markers. Only registered public semantic inputs are admitted.', 'scanned_files':site['scanned_public_file_count']},
            'limitations':['V2 current is evolving; use this archived snapshot for immutable documentation evidence.',
                'WebVOWL is a visualization projection; its visible node count and collapsing filter do not establish formal entity coverage.',
                'V1 recorded OWL-profile hygiene limitations remain; documentation publication does not establish OWL 2 DL conformance.',
                'Semantic human review and expert evaluation remain pending in their research issues.',
                'External semantic IRIs are identifiers, not a guarantee of deployed w3id redirects.',
                'Future-version dry-run is architecture evidence only; no real V3 scientific content is claimed.'],
            'file_sha256_inventory':inventory}
    files['BASELINE-MANIFEST.json']=(json.dumps(record,indent=2,sort_keys=True)+'\n').encode()
    archive(files,args.archive)
    replay=args.archive.with_suffix('.replay.zip');archive(files,replay)
    assert args.archive.read_bytes()==replay.read_bytes(),'archive is not reproducible from frozen inputs';replay.unlink()
    with zipfile.ZipFile(args.archive) as z:
        assert z.testzip() is None
        for name,digest in inventory.items():assert sha(z.read(name))==digest,name
    record.pop('file_sha256_inventory')
    record.update(archive_path=args.archive.resolve().relative_to(ROOT).as_posix(),archive_sha256=sha(args.archive.read_bytes()),
                  archived_files=len(files),archive_rebuild_readback='PASS')
    args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'decision':record['decision'],'archive_sha256':record['archive_sha256'],'files':len(files),'links_checked':len(checked)}))
if __name__=='__main__':main()
