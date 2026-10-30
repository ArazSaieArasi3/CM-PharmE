#!/usr/bin/env python3
"""Verify the frozen experimental archive without running its ontology tooling."""
import argparse,copy,hashlib,json,tarfile
from pathlib import Path,PurePosixPath
HERE=Path(__file__).resolve().parent
CONTRACT_SHA='af43da6949e0db60438682d9ed362cd9a25dff327756e09663754bca96c36ff1'
FREEZE='56e5138a25866c9b23b3d966549ee9a41c1d4653'


def require(ok,reason):
    if not ok:raise ValueError(reason)
def sha(data):return hashlib.sha256(data).hexdigest()
def encoded(value):return (json.dumps(value,indent=2,sort_keys=True)+'\n').encode()
def canonical_sha(value):return sha(json.dumps(value,sort_keys=True,separators=(',',':')).encode())
def load_contract():
    raw=(HERE/'bundle-contract.json').read_bytes();require(sha(raw)==CONTRACT_SHA,'packaging-contract-drift');return json.loads(raw)
def blob_sha(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def checksums(files):return ''.join(sha(raw)+'  '+name+'\n' for name,raw in sorted(files.items()) if name!='CONTENTS.sha256').encode()
def provenance(c,files):
    return dict(schema_version=1,profile=c['profile'],version=c['target'],kind=c['kind'],payload_source_commit=c['payload_source_commit'],payload_git_tree=c['payload_git_tree'],scope_source_commit=c['scope_source_commit'],scope_contract_sha256=c['scope_contract_sha256'],packaging_contract_sha256=CONTRACT_SHA,packaging_contract_commit=FREEZE,code_sha256={name:sha(files[name]) for name in c['code_files']},compression=c['compression'],publication_at_build=c['publication'],claim_boundary='Prepared experimental bundle; no publication, tag, complete validation, scientific or GA acceptance.')


def validate_files(c,files,modes=None):
    for name,digest in c['scope_files_sha256'].items():require('scope/'+name in files and sha(files['scope/'+name])==digest,'scope-integrity')
    manifest=json.loads(files['scope/payload-manifest.json']);rows=manifest['files'];source_names={'source/'+x['path'] for x in rows}
    require({n for n in files if n.startswith('source/')}==source_names,'payload-files')
    for row in rows:
        name='source/'+row['path'];raw=files[name]
        require(len(raw)==row['bytes'] and sha(raw)==row['sha256'] and blob_sha(raw)==row['git_blob_sha'],'payload-integrity')
        if modes is not None:require(modes[name]==int(row['mode'][-3:],8),'payload-mode')
    require(len(rows)==manifest['source_files']==c['expected']['source_files'] and sum(len(files[n]) for n in source_names)==manifest['source_bytes']==c['expected']['source_bytes'],'payload-integrity')
    expected=source_names|{'scope/'+name for name in c['scope_files_sha256']}|set(c['root_files'])
    require(set(files)==expected and len(files)==c['expected']['bundle_files'],'bundle-files')
    require(manifest['source_commit']==c['payload_source_commit'] and manifest['git_tree_sha']==c['payload_git_tree'],'payload-provenance')
    for name,digest in c['metadata_sha256'].items():require(sha(files[name])==digest,'metadata-drift')
    require(sha(files['requirements.lock'])==c['requirements_sha256'] and sha(files['decision.md'])==c['decisions_sha256'] and sha(files['bundle-contract.json'])==CONTRACT_SHA,'metadata-drift')
    prov=json.loads(files['PROVENANCE.json'])
    require(prov.get('kind')=='EXPERIMENTAL_RESEARCH_CHECKPOINT' and prov.get('publication_at_build')==dict(ga_ready=False,release_published=False,tag_created=False),'release-policy')
    require(prov==provenance(c,files),'build-provenance')
    require(files['CONTENTS.sha256']==checksums(files),'checksum-file')
    groups=json.loads(files['scope/artifacts.json'])['groups'];selected=sum(x['review_group'] is not None for x in rows)
    require(len(groups)==c['expected']['review_groups'] and selected==c['expected']['selected_review_files'],'artifact-groups')
    return dict(passed=True,source_files=len(rows),source_bytes=c['expected']['source_bytes'],scope_files=len(c['scope_files_sha256']),bundle_files=len(files),review_groups=len(groups),selected_review_files=selected,metadata_version=c['target'],payload_source_commit=c['payload_source_commit'],scope_source_commit=c['scope_source_commit'],scope_contract_sha256=c['scope_contract_sha256'],packaging_contract_sha256=CONTRACT_SHA,packaging_contract_commit=FREEZE)


def safe_member(member,c,seen):
    name=member.name;p=PurePosixPath(name)
    require(not p.is_absolute() and '..' not in p.parts and p.as_posix()==name and len(p.parts)>1 and p.parts[0]==c['top_directory'] and '\n' not in name and '\r' not in name,'unsafe-archive-path')
    require(member.isreg() and member.mode in {0o644,0o755} and member.uid==member.gid==member.mtime==0 and member.uname==member.gname=='','unsafe-member')
    relative='/'.join(p.parts[1:]);require(relative not in seen,'duplicate-member');seen.add(relative);return relative


def controls(c,files):
    result=[];current='source/'+json.loads(files['scope/scope-contract.json'])['current_native_path']
    for oracle in c['negative_controls']:
        name=oracle['id'];trial=dict(files)
        try:
            if name in {'unsafe-path','symlink-member','duplicate-member'}:
                member=tarfile.TarInfo(c['top_directory']+'/README.md');member.mode=0o644;member.mtime=member.uid=member.gid=0;member.uname=member.gname='';seen=set()
                if name=='unsafe-path':member.name=c['top_directory']+'/../../outside'
                elif name=='symlink-member':member.type=tarfile.SYMTYPE;member.linkname='/outside'
                else:seen.add('README.md')
                safe_member(member,c,seen)
            else:
                if name=='missing-source':trial.pop(current)
                elif name=='tampered-source':trial[current]+=b'\n'
                elif name=='extra-unmanifested':trial['unindexed.txt']=b'extra'
                elif name=='historical-citation':trial['CITATION.cff']=trial['CITATION.cff'].replace(b'2.1.0-rc.1',b'1.0.0')
                elif name=='suppressed-transition':trial['README.md']=trial['README.md'].replace(b'88/89',b'89/89')
                elif name=='ga-claim':
                    prov=json.loads(trial['PROVENANCE.json']);prov['kind']='FINAL_GA';trial['PROVENANCE.json']=encoded(prov)
                elif name=='checksum-tamper':trial['CONTENTS.sha256']=b'0'*64+trial['CONTENTS.sha256'][64:]
                validate_files(c,trial)
        except ValueError as error:
            require(str(error)==oracle['expected_reason'],'unexpected-control: '+name+': '+str(error));result.append(dict(id=name,refused=True,reason=str(error)))
        else:raise ValueError('negative-control-admitted: '+name)
    return result


def inspect_archive(archive,sidecar):
    c=load_contract();require(archive.name==c['archive_name'],'archive-name')
    fields=sidecar.read_text().strip().split();require(len(fields)==2 and fields[1]==archive.name and fields[0]==sha(archive.read_bytes()),'archive-checksum')
    files={};modes={};seen=set()
    with tarfile.open(archive,'r:') as tar:
        members=tar.getmembers();require(len(members)==c['expected']['bundle_files'],'bundle-files')
        for member in members:
            relative=safe_member(member,c,seen);stream=tar.extractfile(member);require(stream is not None,'unsafe-member');files[relative]=stream.read();modes[relative]=member.mode
    summary=validate_files(c,files,modes);summary.update(archive_name=archive.name,archive_sha256=fields[0],archive_bytes=archive.stat().st_size,negative_controls=controls(c,files),archive_created=True,release_published=False,tag_created=False,ga_ready=False,clean_replay_completed=False)
    return files,summary


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--archive',required=True,type=Path);ap.add_argument('--sha256-file',required=True,type=Path);ap.add_argument('--output',required=True,type=Path);args=ap.parse_args()
    _,report=inspect_archive(args.archive.resolve(),args.sha256_file.resolve());args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(encoded(report));print(json.dumps(report,sort_keys=True))


if __name__=='__main__':main()
