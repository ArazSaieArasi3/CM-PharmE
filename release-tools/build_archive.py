#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Build the curated M1 distribution twice from exact pinned bytes, without Git."""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import tarfile
from pathlib import Path, PurePosixPath

HERE=Path(__file__).resolve().parent
SUPPORT='v2/release/2.1/support/0.1.0'
TOOLS=('build_archive.py','verify_archive.py','bundle-contract.json')


def require(ok,message):
    if not ok:raise ValueError(message)


def digest(data):return hashlib.sha256(data).hexdigest()


def safe(path):
    p=PurePosixPath(path)
    require(isinstance(path,str) and not p.is_absolute() and '..' not in p.parts
            and str(p)==path and path not in ('','.'),'Unsafe member path: '+str(path))
    return path


def read_regular(root,path):
    safe(path);root=Path(root).resolve();p=root/path
    require(p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(root),'Missing/unsafe file: '+path)
    return p.read_bytes()


def contract():
    data=read_regular(HERE,'bundle-contract.json');c=json.loads(data)
    require(tuple(c['tool_files'])==TOOLS,'Tool contract differs')
    require(c['archive_manifest']=='package-manifest.json','Package manifest contract differs')
    safe(c['archive_root']);require('/' not in c['archive_root'],'Archive root must be one directory')
    require(c['support_manifest_path']==SUPPORT+'/manifest.json','Unsupported support contract path')
    return c,data


def metadata(c):
    pins=c['metadata_sha256']
    actual={str(p.relative_to(HERE/'metadata')) for p in (HERE/'metadata').rglob('*') if p.is_file()}
    require(actual==set(pins),'Metadata file set differs')
    result={}
    for p,h in pins.items():
        b=read_regular(HERE,'metadata/'+safe(p));require(digest(b)==h,'Metadata drift: '+p)
        result[p]=b
    return result


def support_entries(data,c):
    require(digest(data)==c['support_manifest_sha256'],'Support manifest drift')
    m=json.loads(data);require(m['target_distribution']=='2.1.0','Wrong target distribution')
    rows={}
    for row in m['files']:
        p=safe(row['path']);require(p not in rows,'Duplicate support path: '+p);rows[p]=row
    require(c['support_manifest_path'] not in rows,'Self-hashed support manifest')
    return rows


def root_mapping(c):
    return c['root_files']


def contents(root):
    c,cb=contract();md=metadata(c)
    support=read_regular(root,c['support_manifest_path']);rows=support_entries(support,c)
    result={'source/'+c['support_manifest_path']:support}
    for p,row in rows.items():
        b=read_regular(root,p)
        require(digest(b)==row['sha256'] and len(b)==row['bytes'],'Support payload drift: '+p)
        result['source/'+p]=b
    for dest,src in root_mapping(c).items():
        safe(dest)
        if src.startswith('metadata/'):
            key=src[len('metadata/'):];require(key in md,'Unpinned root metadata: '+src);b=md[key]
        else:
            require(src in rows,'Root source outside support cut: '+src);b=result['source/'+src]
        result[dest]=b
    for p in TOOLS:result['release-tools/'+p]=read_regular(HERE,p)
    for p,b in md.items():result['release-tools/metadata/'+p]=b
    require(len(result)==len(set(result)),'Duplicate member')
    manifest=dict(schema_version='CMPE-CuratedPackageManifest/0.1.0',
        support_manifest_sha256=c['support_manifest_sha256'],
        member_count=len(result),members_sha256={p:digest(b) for p,b in sorted(result.items())})
    result['package-manifest.json']=(json.dumps(manifest,indent=2,sort_keys=True)+'\n').encode()
    return c,result


def tar_bytes(c,members):
    out=io.BytesIO()
    with tarfile.open(fileobj=out,mode='w',format=tarfile.USTAR_FORMAT) as archive:
        for p,b in sorted(members.items()):
            name=c['archive_root']+'/'+safe(p);info=tarfile.TarInfo(name)
            info.type=tarfile.REGTYPE;info.size=len(b);info.mode=0o644
            info.uid=info.gid=0;info.uname=info.gname='';info.mtime=c['mtime']
            archive.addfile(info,io.BytesIO(b))
    return out.getvalue()


def build(root):
    c,members=contents(root);return c,members,tar_bytes(c,members)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=HERE.parents[4])
    p.add_argument('--output-dir',type=Path,required=True)
    args=p.parse_args();out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    c,members,first=build(args.root.resolve());other,second_members,second=build(args.root.resolve())
    require(first==second and members==second_members and c==other,'Independent builds differ')
    name=c['archive_name'];require('/' not in name and name.endswith('.tar'),'Unsafe archive name')
    (out/name).write_bytes(first);h=digest(first)
    (out/(name+'.sha256')).write_text(h+'  '+name+'\n')
    report=dict(schema_version='CMPE-CuratedBuild/0.1.0',passed=True,archive=name,
        archive_sha256=h,archive_bytes=len(first),member_count=len(members),
        support_manifest_sha256=c['support_manifest_sha256'],bundle_contract_sha256=digest((HERE/'bundle-contract.json').read_bytes()),
        independent_builds=2,byte_identical=True,git_used=False,ga_ready=False,stable_published=False)
    (out/'build-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':main()
