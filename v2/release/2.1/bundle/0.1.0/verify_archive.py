#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Validate a curated archive against trusted external contract/tools, then replay."""
from __future__ import annotations
import argparse
import io
import json
import os
import subprocess
import sys
import tarfile
from pathlib import Path

import build_archive as build

HERE=Path(__file__).resolve().parent
PROFILE='v2/ontology/profiles/2.1/m1-provenance/0.1.0'
INTEGRATION='v2/data/integrations/2.1/m1-core/0.1.0'
SUPPORT='v2/release/2.1/support/0.1.0'


def validate(data,expected_sha256=None):
    c,_=build.contract();md=build.metadata(c)
    if expected_sha256 is not None:
        build.require(build.digest(data)==expected_sha256,'Archive SHA-256 differs from trusted receipt')
    members={};prefix=c['archive_root']+'/'
    with tarfile.open(fileobj=io.BytesIO(data),mode='r:') as archive:
        for info in archive:
            build.safe(info.name)
            build.require(info.name.startswith(prefix),'Wrong archive root: '+info.name)
            p=info.name[len(prefix):];build.safe(p)
            build.require(p not in members,'Duplicate archive member: '+p)
            build.require(info.type==tarfile.REGTYPE and info.isfile() and not info.linkname,
                          'Nonregular/link member refused: '+p)
            build.require(info.uid==info.gid==0 and info.uname==info.gname==''
                          and info.mode==0o644 and info.mtime==c['mtime'] and not info.pax_headers,
                          'Noncanonical archive metadata: '+p)
            build.require(0<=info.size<=64*1024*1024,'Member size outside selected cut: '+p)
            stream=archive.extractfile(info);build.require(stream is not None,'Unreadable member: '+p)
            members[p]=stream.read()
    support_name='source/'+c['support_manifest_path']
    build.require(support_name in members,'Missing support manifest')
    rows=build.support_entries(members[support_name],c)
    expected={support_name:members[support_name]}
    for p,row in rows.items():
        key='source/'+p;build.require(key in members,'Missing support member: '+key)
        b=members[key]
        build.require(build.digest(b)==row['sha256'] and len(b)==row['bytes'],'Pinned source hash/size differs: '+key)
        expected[key]=b
    for dest,src in build.root_mapping(c).items():
        if src.startswith('metadata/'):
            key=src[len('metadata/'):];build.require(key in md,'Unpinned root metadata');b=md[key]
        else:
            build.require(src in rows,'Root source outside cut');b=expected['source/'+src]
        expected[dest]=b
    for p in build.TOOLS:expected['release-tools/'+p]=build.read_regular(HERE,p)
    for p,b in md.items():expected['release-tools/metadata/'+p]=b
    package=dict(schema_version='CMPE-CuratedPackageManifest/0.1.0',
        support_manifest_sha256=c['support_manifest_sha256'],member_count=len(expected),
        members_sha256={p:build.digest(b) for p,b in sorted(expected.items())})
    expected['package-manifest.json']=(json.dumps(package,indent=2,sort_keys=True)+'\n').encode()
    build.require(set(members)==set(expected),'Archive member set differs: '+str(sorted(set(members)^set(expected))))
    for p,b in expected.items():build.require(members[p]==b,'Trusted root/tool/manifest bytes differ: '+p)
    build.require(data==build.tar_bytes(c,members),'Archive ordering/padding/format differs from deterministic USTAR')
    return c,members


def malformed(c,members,kind):
    changed=dict(members)
    if kind=='missing':changed.pop('source/tools/v2_ontology/CheckOWL2DL.java')
    elif kind=='unexpected':changed['unexpected.txt']=b'unexpected\n'
    elif kind in ('payload-tampering','tool-tampering'):
        path=('source/'+PROFILE+'/profile.ttl' if kind=='payload-tampering' else 'release-tools/build_archive.py')
        changed[path]+=b'\n# adversarial change\n'
        # Attacker also rewrites the untrusted package manifest: trusted pins must still refuse.
        pm=json.loads(changed['package-manifest.json']);pm['members_sha256'][path]=build.digest(changed[path])
        changed['package-manifest.json']=(json.dumps(pm,indent=2,sort_keys=True)+'\n').encode()
    else:
        stream=io.BytesIO()
        with tarfile.open(fileobj=stream,mode='w',format=tarfile.USTAR_FORMAT) as archive:
            for p,b in sorted(changed.items()):
                info=tarfile.TarInfo(c['archive_root']+'/'+p);info.size=len(b);info.mode=0o644;info.mtime=c['mtime']
                archive.addfile(info,io.BytesIO(b))
            if kind=='traversal':info=tarfile.TarInfo(c['archive_root']+'/../escape.txt')
            elif kind=='symlink':
                info=tarfile.TarInfo(c['archive_root']+'/link');info.type=tarfile.SYMTYPE;info.linkname='/tmp/outside'
            elif kind=='duplicate':
                info=tarfile.TarInfo(c['archive_root']+'/package-manifest.json')
            else:raise ValueError('Unknown control')
            info.mode=0o644;info.mtime=c['mtime'];archive.addfile(info)
        return stream.getvalue()
    return build.tar_bytes(c,changed)


def controls(c,members):
    results=[]
    for kind in ['payload-tampering','tool-tampering','traversal','symlink','unexpected','missing','duplicate']:
        bad=malformed(c,members,kind)
        try:validate(bad)
        except ValueError as error:results.append(dict(control=kind,refused=True,reason=str(error)))
        else:raise ValueError('Malformed archive accepted: '+kind)
    return results


def extract(c,members,destination):
    build.require(not destination.exists(),'Extraction directory already exists: '+str(destination))
    destination.mkdir(parents=True)
    target=destination/c['archive_root'];target.mkdir()
    for p,b in sorted(members.items()):
        file=target/p;file.parent.mkdir(parents=True,exist_ok=True);file.write_bytes(b)
    return target


def replay(c,target,out,database_url):
    source=target/'source';env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');commands=[]
    def run(label,args,cwd=source):
        result=subprocess.run([sys.executable,*args],cwd=cwd,env=env,capture_output=True,text=True,timeout=900)
        (out/(label+'.log')).write_text(result.stdout+'\n'+result.stderr)
        build.require(result.returncode==0,'Extracted replay failed: '+label+'\n'+result.stdout+result.stderr)
        commands.append(dict(check=label,command=[('<explicit-fixture-url>' if a==database_url else a) for a in args],returncode=result.returncode))
    run('support-contract',[SUPPORT+'/verify_contract.py','--output-dir',str(out/'support')])
    run('profile',[PROFILE+'/verify_profile.py','--output-dir',str(out/'profile')])
    run('integration-preflight',[INTEGRATION+'/verify_integration.py','--preflight-only'])
    if database_url:
        # Guard the actual target before the historical bootstrap can execute --reset.
        run('database-target-guard',[INTEGRATION+'/verify_integration.py','--preflight-only','--database-url',database_url])
        run('database-bootstrap',['tools/v2_data/bootstrap_ingest.py','--database-url',database_url,'--reset',
                                  '--report',str(out/'integration-ingest.json')])
        run('database-integration',[INTEGRATION+'/verify_integration.py','--database-url',database_url,
                                   '--ingest-report',str(out/'integration-ingest.json'),'--output-dir',str(out/'integration')])
    rebuilt=out/'rebuild'
    run('extracted-archive-rebuild',[str(target/'release-tools/build_archive.py'),'--root',str(source),
                                   '--output-dir',str(rebuilt)])
    return commands,rebuilt/c['archive_name']


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive',type=Path,required=True)
    parser.add_argument('--expected-sha256')
    parser.add_argument('--output-dir',type=Path,required=True)
    parser.add_argument('--self-test',action='store_true')
    parser.add_argument('--cold-replay',action='store_true',help='Compatibility flag; cold replay is the default')
    parser.add_argument('--validate-only',action='store_true',help='Validate trusted bytes without extraction or replay')
    parser.add_argument('--database-url',help='Explicit disposable local fixture; activates full cold replay')
    args=parser.parse_args();out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    build.require(not (args.validate_only and (args.database_url or args.cold_replay)),'Validate-only cannot request replay')
    cold_replay=not args.validate_only
    data=args.archive.read_bytes();c,members=validate(data,args.expected_sha256)
    report=dict(schema_version='CMPE-CuratedArchiveVerification/0.1.0',passed=True,
        archive_sha256=build.digest(data),archive_bytes=len(data),member_count=len(members),
        expected_digest_checked=args.expected_sha256 is not None,
        support_manifest_sha256=c['support_manifest_sha256'],trusted_external_tools=True,
        ga_ready=False,stable_published=False,git_used=False,database_executed=False,profile_replayed=False)
    if args.self_test:report['malformed_archive_controls']=controls(c,members)
    if cold_replay:
        target=extract(c,members,out/'extracted')
        commands,rebuilt=replay(c,target,out,args.database_url)
        build.require(rebuilt.read_bytes()==data,'Extracted-source rebuild bytes differ')
        report.update(cold_replay_commands=commands,source_fallback_used=False,
                      extracted_rebuild_byte_identical=True,profile_replayed=True,database_executed=bool(args.database_url))
        if args.database_url:
            db=json.loads((out/'integration/report.json').read_text())
            report['database_summary']=dict(passed=db['passed'],source_rows=db['cases'][0]['query_rows'],
                legacy_pairs=db['legacy_after']['pairs_passed'],rollback_verified=db['optional_fixture_update_rolled_back'],
                schema_data_preserved=db['base_rows_schema_defaults_indexes_views_unchanged'])
    (out/'verification-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':main()
