#!/usr/bin/env python3
"""Read-only staging/published release verification; never creates a tag or release."""
import argparse,copy,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
CONTRACT_SHA='d0f6859900cc6512b313ed6f6ba13b08bafaa3565a929a14bc1e6bdbf30e1de4'
FREEZE='05a43dd43e8efcd11251b876b85d5dbd3c3b39be'
def require(ok,why):
    if not ok:raise ValueError(why)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def encoded(obj):return (json.dumps(obj,indent=2,sort_keys=True)+'\n').encode()
def load():
    require(sha((HERE/'publication-contract.json').read_bytes())==CONTRACT_SHA,'contract-drift');c=json.loads((HERE/'publication-contract.json').read_text())
    for name,digest in c['frozen_metadata_sha256'].items():require(sha((HERE/name).read_bytes())==digest,'frozen-metadata-drift')
    return c,json.loads((HERE/'release-plan.json').read_text()),json.loads((HERE/'target-ci.json').read_text()),(HERE/'release-notes.md').read_text()
def validate(c,p,ci,notes,assets):
    require(p['tag']==c['tag'] and p['repository']==c['repository'] and p['title']==c['title'],'release-identity')
    require(p['assembly_commit']==c['assembly_commit'] and p['release_branch']==c['release_branch'] and p['payload_source_commit']=='64edf150db8a78579928fd99b5a381f665c1afdf' and p['scope_source_commit']=='a0a9a539c3891476847b52fed4c65d9ccae8d485' and p['builder_implementation_commit']=='f58a935f5c8455cce7df1338d0d380cb6d7a0a3b' and p['native_sha256']=='d97d7a7f42e3fc903181d6d4ed0a2bd4e159afe4a1a3bb685e3c821a93791a91','source-agreement')
    claims=p['claims'];require(all(claims[k] is False for k in ['full_20_family_candidate_execution','independent_scientific_acceptance','complete_native_to_owl_alignment','ga_ready']) and claims['source_policy_scientific_acceptances']==claims['orsd_author_accepted_rows']==0 and p['held_gates']==c['held_gates'],'unsupported-claim')
    require(p['publication_request']==dict(draft=False,prerelease=True,stable_latest=False),'release-policy')
    require(claims['original_after_matches']==88 and claims['prospective_after_matches']==89 and claims['witness_contract_transitions']==1,'claim-boundary')
    workflows=ci['workflows'];require(ci['target_commit']==c['assembly_commit'] and len(workflows)==len({x['name'] for x in workflows})==ci['workflow_families']==c['expected_target_workflow_families']==25 and all(x['head_sha']==c['assembly_commit'] and x['conclusion']=='success' for x in workflows),'ci-provenance')
    require(sha(notes.encode())==c['frozen_metadata_sha256']['release-notes.md'],'metadata-drift')
    require(set(assets)=={x['name'] for x in c['expected_assets']},'asset-integrity')
    for item in c['expected_assets']:require(len(assets[item['name']])==item['bytes'] and sha(assets[item['name']])==item['sha256'],'asset-integrity')
def controls(c,p,ci,notes,assets):
    rows=[]
    for oracle in c['negative_controls']:
        plan=copy.deepcopy(p);cohort=copy.deepcopy(ci);body=notes;trial=dict(assets);name=oracle['id']
        if name=='wrong-tag':plan['tag']='2.1.0'
        elif name=='wrong-assembly':plan['assembly_commit']='0'*40
        elif name=='ga-ready':plan['claims']['ga_ready']=True
        elif name=='stable-label':plan['publication_request']['prerelease']=False
        elif name=='suppressed-transition':plan['claims']['original_after_matches']=89
        elif name=='missing-ci-family':cohort['workflows'].pop()
        elif name=='tampered-asset':trial[c['expected_assets'][0]['name']]+=b'\n'
        elif name=='edited-notes':body+='Approved GA\n'
        try:validate(c,plan,cohort,body,trial)
        except ValueError as error:
            require(str(error)==oracle['reason'],'unexpected-control: '+name);rows.append(dict(id=name,refused=True,reason=str(error)))
        else:raise ValueError('negative-control-admitted: '+name)
    return rows

def published(c,release,tag,latest,notes):
    require(release['tag_name']==c['tag'] and release['name']==c['title'],'published-identity')
    require(release['html_url']=='https://github.com/'+c['repository']+'/releases/tag/'+c['tag'],'published-url')
    require(release['draft'] is False and release['prerelease'] is True and bool(release['published_at']),'published-status')
    require(release['body'].replace('\r\n','\n')==notes,'published-body')
    require(tag['ref']=='refs/tags/'+c['tag'] and tag['object']['type']=='commit' and tag['object']['sha']==c['assembly_commit'],'published-tag-target')
    require(latest['latest_tag']!=c['tag'] and latest['http_status'] in {200,404},'stable-latest')
    expected={x['name']:x for x in c['expected_assets']};actual={x['name']:x for x in release['assets']};require(len(actual)==len(release['assets']) and set(actual)==set(expected),'published-asset-set')
    for name,item in expected.items():
        asset=actual[name];require(asset['state']=='uploaded' and asset['size']==item['bytes'],'published-asset-metadata')
        if asset.get('digest'):require(asset['digest']=='sha256:'+item['sha256'],'published-asset-digest')
    return dict(release_id=release['id'],release_url=release['html_url'],published_at=release['published_at'],tag=c['tag'],tag_target=tag['object']['sha'],prerelease=True,draft=False,stable_latest=False,downloaded_assets_verified=True,release_body_newline_normalization='CRLF_TO_LF_ONLY',assets=[dict(name=x['name'],id=actual[x['name']]['id'],bytes=x['bytes'],sha256=x['sha256'],browser_download_url=actual[x['name']]['browser_download_url']) for x in c['expected_assets']])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--assets-dir',required=True,type=Path);ap.add_argument('--output',required=True,type=Path);ap.add_argument('--release-json',type=Path);ap.add_argument('--tag-json',type=Path);ap.add_argument('--latest-json',type=Path);a=ap.parse_args();c,p,ci,notes=load()
    assets={x.name:x.read_bytes() for x in a.assets_dir.iterdir() if x.is_file()};validate(c,p,ci,notes,assets)
    report=dict(schema_version=1,profile=c['profile'],passed=True,publication_contract_sha256=CONTRACT_SHA,publication_freeze_commit=FREEZE,assembly_commit=c['assembly_commit'],payload_source_commit=p['payload_source_commit'],scope_source_commit=p['scope_source_commit'],builder_implementation_commit=p['builder_implementation_commit'],staged_assets_verified=True,target_ci_families=25,negative_controls=controls(c,p,ci,notes,assets),release_published=False,tag_created=False,ga_ready=False,claims=p['claims'],held_gates=c['held_gates'])
    if a.release_json:
        require(a.tag_json is not None and a.latest_json is not None,'missing-publication-snapshot');report.update(published(c,json.loads(a.release_json.read_text()),json.loads(a.tag_json.read_text()),json.loads(a.latest_json.read_text()),notes));report.update(release_published=True,tag_created=True)
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(encoded(report));print(encoded(report).decode())
if __name__=='__main__':main()
