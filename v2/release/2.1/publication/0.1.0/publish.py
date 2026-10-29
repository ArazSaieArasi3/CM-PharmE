#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Publish only the reviewed exact M1 core; preserve any existing release or tag."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
BUNDLE=ROOT/'v2/release/2.1/bundle/0.1.0'
SECRETS=tuple(x for x in [os.environ.get('GH_TOKEN'),os.environ.get('GITHUB_TOKEN')] if x)


def clean(value):
    value=str(value)
    for secret in SECRETS:value=value.replace(secret,'<redacted>')
    return value


def require(ok,message):
    if not ok:raise ValueError(message)


def sha(data):return hashlib.sha256(data).hexdigest()


def write(path,value):path.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')


def command(args,*,cwd=ROOT,allow_failure=False):
    run=subprocess.run(args,cwd=cwd,capture_output=True,text=True,timeout=900,
                       env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    if not allow_failure:require(run.returncode==0,'Command failed: '+clean(' '.join(args))+'\n'+clean(run.stderr))
    return run


def api(path):
    run=command(['gh','api',path])
    return json.loads(run.stdout)


def absent(path):
    run=command(['gh','api',path],allow_failure=True)
    require(run.returncode!=0,'Existing GitHub resource preserved; refusing publication: '+path)
    require('HTTP 404' in run.stderr,'Could not establish resource absence: '+clean(run.stderr))
    try:body=json.loads(run.stdout)
    except json.JSONDecodeError:body={}
    require(body.get('message')=='Not Found','Non-404 API result cannot establish absence')


def releases(repo):
    raw=command(['gh','api','--paginate','--slurp','repos/'+repo+'/releases?per_page=100'])
    return [release for page in json.loads(raw.stdout) for release in page]


def release_identity(release,c,draft):
    require(release['tag_name']==c['tag'] and release['name']==c['title'],'Release identity differs')
    require(release['draft'] is draft and release['prerelease'] is False,'Release publication state differs')
    require(release['target_commitish']==c['target_commit'],'Release target differs')


def asset_metadata(release,expected):
    rows=release['assets'];require(len(rows)==len(expected),'Unexpected release asset count')
    require({x['name'] for x in rows}==set(expected),'Release asset names differ')
    for asset in rows:
        record=expected[asset['name']]
        require(asset['state']=='uploaded' and asset['size']==record['bytes'],'Asset size/state differs: '+asset['name'])
        require(asset.get('digest')=='sha256:'+record['sha256'],'GitHub asset digest differs: '+asset['name'])
    return [{k:x[k] for k in ['id','name','size','digest','browser_download_url']} for x in rows]


def downloads(c,folder,expected):
    require(not folder.exists(),'Download folder must be new: '+str(folder));folder.mkdir(parents=True)
    for name in sorted(expected):
        command(['gh','release','download',c['tag'],'--repo',c['repository'],
                 '--dir',str(folder),'--pattern',name])
    actual={x.name for x in folder.iterdir()}
    require(actual==set(expected),'Downloaded asset set differs')
    rows={}
    for name,record in expected.items():
        path=folder/name;require(path.is_file() and not path.is_symlink(),'Unsafe downloaded asset')
        data=path.read_bytes();require(sha(data)==record['sha256'] and len(data)==record['bytes'],
                                     'Downloaded asset differs: '+name)
        rows[name]=dict(sha256=sha(data),bytes=len(data))
    return rows


def peeled_tag(repo,tag):
    obj=api('repos/'+repo+'/git/ref/tags/'+tag)['object']
    for _ in range(5):
        if obj['type']=='commit':return obj['sha']
        require(obj['type']=='tag','Unexpected tag object type')
        obj=api('repos/'+repo+'/git/tags/'+obj['sha'])['object']
    raise ValueError('Tag nesting exceeds bounded peel')


def publish(out,report):
    require(bool(os.environ.get('GH_TOKEN')),'GH_TOKEN must be supplied through the Actions environment')
    cb=(HERE/'publication-contract.json').read_bytes();c=json.loads(cb)
    require(c['repository']=='ArazSaieArasi3/CM-PharmE' and c['tag']=='2.1.0','Wrong publication repository/tag')
    require(all(re.fullmatch('[0-9a-f]{40}',c[k]) for k in ['target_commit','target_tree','implementation_commit']),
            'Invalid pinned Git identity')
    notes=(HERE/'release-notes.md').read_bytes()
    require(sha(notes)==c['notes_sha256'],'Pinned release notes drift')
    require(sha((BUNDLE/'build_archive.py').read_bytes())==c['builder_sha256'],'Pinned builder drift')
    require(sha((BUNDLE/'verify_archive.py').read_bytes())==c['verifier_sha256'],'Pinned verifier drift')
    rb=(HERE/'technical-review.json').read_bytes()
    require(sha(rb)==c['technical_review_sha256'],'Pinned technical review drift')
    review=json.loads(rb)
    require(review['decision']=='ACCEPT_BOUNDED_PACKAGE_FOR_EXACT_STABLE_PUBLICATION','Package review is not accepted')
    require(review['archive_sha256']==c['archive_sha256'] and review['archive_bytes']==c['archive_bytes']
            and review['evidence']['package_implementation']==c['implementation_commit'],'Review/package identity differs')
    require(all(value is True for value in review['criteria'].values())
            and review['owner_exact_bytes_review_claimed'] is False,'Technical review criteria/authority differs')
    require(review['support_manifest_sha256']==json.loads((BUNDLE/'bundle-contract.json').read_text())['support_manifest_sha256'],
            'Reviewed support cut differs')
    require(c['stable_prerelease'] is False and c['overwrite_existing_release_or_tag'] is False
            and c['publish_only_after_draft_assets_download_verified'] is True
            and c['main_or_whole_candidate_merge'] is False,'Publication scope guards differ')
    require(c['archive_name']=='cm-pharme-2.1.0.tar','Wrong archive name')
    report.update(stage='validate-exact-package',repository=c['repository'],tag=c['tag'],
                  publication_contract_sha256=sha(cb),implementation_commit=c['implementation_commit'],
                  target_commit=c['target_commit'],target_tree=c['target_tree'])
    build_out=out/'built';validation=out/'prepublication-validation'
    run=command([sys.executable,str(BUNDLE/'build_archive.py'),'--root',str(ROOT),'--output-dir',str(build_out)])
    (out/'build.log').write_text(clean(run.stdout+'\n'+run.stderr))
    archive=build_out/'cm-pharme-2.1.0.tar';data=archive.read_bytes()
    require(sha(data)==c['archive_sha256'] and len(data)==c['archive_bytes'],'Exact reviewed archive differs')
    run=command([sys.executable,str(BUNDLE/'verify_archive.py'),'--archive',str(archive),
                 '--expected-sha256',c['archive_sha256'],'--output-dir',str(validation),'--validate-only'])
    (out/'prepublication-validation.log').write_text(clean(run.stdout+'\n'+run.stderr))
    commit=api('repos/'+c['repository']+'/git/commits/'+c['target_commit'])
    require(commit['sha']==c['target_commit'] and commit['tree']['sha']==c['target_tree'],'Target commit/tree differs')
    report['stage']='confirm-absence'
    absent('repos/'+c['repository']+'/git/ref/tags/'+c['tag'])
    absent('repos/'+c['repository']+'/releases/tags/'+c['tag'])
    # Also inspect drafts; never reuse or overwrite an existing draft with this tag.
    require(not any(x.get('tag_name')==c['tag'] for x in releases(c['repository'])),'Existing draft/release preserved')
    provenance=dict(schema_version='CMPE-PublishedCoreProvenance/0.1.0',repository=c['repository'],
        tag=c['tag'],target_commit=c['target_commit'],target_tree=c['target_tree'],
        implementation_commit=c['implementation_commit'],publication_contract_sha256=sha(cb),
        archive_sha256=c['archive_sha256'],archive_bytes=c['archive_bytes'],
        support_manifest_sha256=json.loads((BUNDLE/'bundle-contract.json').read_text())['support_manifest_sha256'],
        authority='Technical publication under the existing user authorization after exact reviewed checks; no additional personal owner or expert acceptance inferred.',
        scope='Curated M1 provenance core only; source-policy 1/4, historical ORSD 0/83, no new external expert responses; no full-candidate merge or RC mutation.')
    provenance_path=build_out/'provenance.json';write(provenance_path,provenance)
    paths=[archive,build_out/'cm-pharme-2.1.0.tar.sha256',provenance_path]
    require([p.name for p in paths]==c['assets'],'Authorized asset names/order differ')
    expected={p.name:dict(sha256=sha(p.read_bytes()),bytes=p.stat().st_size) for p in paths}
    require((build_out/'cm-pharme-2.1.0.tar.sha256').read_text()==c['archive_sha256']+'  cm-pharme-2.1.0.tar\n',
            'Checksum-file bytes differ')
    report['stage']='create-draft'
    command(['gh','release','create',c['tag'],'--repo',c['repository'],'--target',c['target_commit'],
             '--title',c['title'],'--notes-file',str(HERE/'release-notes.md'),'--draft'])
    report['draft_created']=True;report['stage']='upload-draft-assets'
    command(['gh','release','upload',c['tag'],*[str(p) for p in paths],'--repo',c['repository']])
    candidates=[x for x in releases(c['repository']) if x.get('tag_name')==c['tag']]
    require(len(candidates)==1,'Cannot identify the single newly created draft')
    draft=api('repos/'+c['repository']+'/releases/'+str(candidates[0]['id']));release_identity(draft,c,True)
    release_id=draft['id'];report['release_id']=release_id;report['release_url']=draft['html_url']
    report['draft_assets']=asset_metadata(draft,expected)
    report['stage']='download-draft-assets';report['draft_downloads']=downloads(c,out/'draft-download',expected)
    write(out/'draft-release.json',draft)
    report['stage']='publish-verified-draft';report['publication_attempted']=True
    command(['gh','release','edit',c['tag'],'--repo',c['repository'],'--draft=false','--latest'])
    published=api('repos/'+c['repository']+'/releases/'+str(release_id))
    report['publication_observed']=published.get('draft') is False
    report['stable_release_visible']=published.get('draft') is False and published.get('prerelease') is False
    release_identity(published,c,False)
    require(peeled_tag(c['repository'],c['tag'])==c['target_commit'],'Published tag points elsewhere')
    report['published_assets']=asset_metadata(published,expected)
    report['stage']='redownload-published-assets';report['published_downloads']=downloads(c,out/'published-download',expected)
    write(out/'published-release.json',published)
    report.update(stage='complete',passed=True,draft=False,prerelease=False,stable_published=True,
                  archive_sha256=c['archive_sha256'],archive_bytes=c['archive_bytes'],
                  target_tag_verified=True,existing_releases_modified=False,main_merged=False,
                  rc_modified=False,new_owner_acceptance_invented=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args();out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    require(not (out/'publication-report.json').exists(),'Refusing to overwrite a publication receipt')
    report=dict(schema_version='CMPE-PublicationReceipt/0.1.0',passed=False,stable_published=False,
                draft_created=False,publication_attempted=False,cleanup_performed=False)
    try:publish(out,report)
    except Exception as error:
        report['error']=clean(error);write(out/'publication-report.json',report)
        print(json.dumps({k:report.get(k) for k in ['passed','stage','release_id','draft_created','publication_attempted','error']}))
        raise SystemExit(1)
    write(out/'publication-report.json',report)
    print(json.dumps({k:report[k] for k in ['passed','release_id','release_url','target_commit','target_tree',
                                         'archive_sha256','archive_bytes','draft','prerelease','stable_published']}))

if __name__=='__main__':main()
