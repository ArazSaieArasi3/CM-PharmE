#!/usr/bin/env python3
"""Deterministic tar builder for an immutable research snapshot and scope."""
import argparse,io,os,tarfile,tempfile,sys
from pathlib import Path
sys.dont_write_bytecode=True
import verify_bundle as v
HERE=Path(__file__).resolve().parent


def collect(root):
    files={}
    for base,dirs,names in os.walk(root):
        dirs[:]=sorted(x for x in dirs if x!='.git')
        for name in dirs:v.require(not (Path(base)/name).is_symlink(),'input-symlink')
        for name in sorted(names):
            if name=='.git':continue
            path=Path(base)/name;v.require(path.is_file() and not path.is_symlink(),'input-symlink');files[path.relative_to(root).as_posix()]=path.read_bytes()
    return files


def write_tar(path,c,files):
    modes={'source/'+r['path']:int(r['mode'][-3:],8) for r in __import__('json').loads(files['scope/payload-manifest.json'])['files']}
    with tarfile.open(path,'w:',format=tarfile.PAX_FORMAT,encoding='utf-8') as tar:
        for name,raw in sorted(files.items()):
            info=tarfile.TarInfo(c['top_directory']+'/'+name);info.size=len(raw);info.mode=modes.get(name,0o644);info.uid=info.gid=info.mtime=0;info.uname=info.gname='';tar.addfile(info,io.BytesIO(raw))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source-root',required=True,type=Path);ap.add_argument('--scope-root',required=True,type=Path);ap.add_argument('--output-dir',required=True,type=Path);args=ap.parse_args();c=v.load_contract()
    source=collect(args.source_root.resolve());scope=collect(args.scope_root.resolve());v.require(set(scope)==set(c['scope_files_sha256']),'scope-file-set')
    files={'source/'+p:raw for p,raw in source.items()};files.update({'scope/'+p:raw for p,raw in scope.items()})
    for name in c['metadata_sha256']:files[name]=((HERE/'metadata'/name) if (HERE/'metadata').is_dir() else HERE/name).read_bytes()
    for name in c['code_files']+['bundle-contract.json','requirements.lock','decision.md']:files[name]=(HERE/name).read_bytes()
    files['PROVENANCE.json']=v.encoded(v.provenance(c,files));files['CONTENTS.sha256']=v.checksums(files);v.validate_files(c,files)
    out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=False);archive=out/c['archive_name'];write_tar(archive,c,files)
    with tempfile.TemporaryDirectory(prefix='rc02-repeat-',dir=out.parent) as directory:
        repeat=Path(directory)/archive.name;write_tar(repeat,c,files);v.require(archive.read_bytes()==repeat.read_bytes(),'non-deterministic-build')
    sidecar=out/(archive.name+'.sha256');sidecar.write_text(v.sha(archive.read_bytes())+'  '+archive.name+'\n')
    _,report=v.inspect_archive(archive,sidecar);report.update(repeat_build_equal=True,compression='none');(out/'build-results.json').write_bytes(v.encoded(report));print(v.encoded({k:report[k] for k in ['passed','archive_sha256','archive_bytes','bundle_files','repeat_build_equal']}).decode())


if __name__=='__main__':main()
