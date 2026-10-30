#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Verify exact #333 support bytes and dependency closure, optionally in a cold tree."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
PROFILE='v2/ontology/profiles/2.1/m1-provenance/0.1.0'
INTEGRATION='v2/data/integrations/2.1/m1-core/0.1.0'
SUPPORT='v2/release/2.1/support/0.1.0'

def require(ok,message):
    if not ok:raise ValueError(message)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def verify(root):
    manifest=json.loads((root/SUPPORT/'manifest.json').read_text())
    paths=set()
    for row in manifest['files']:
        p=PurePosixPath(row['path'])
        require(not p.is_absolute() and '..' not in p.parts and str(p)==row['path'],'Unsafe manifest path')
        require(row['path'] not in paths,'Duplicate path');paths.add(row['path'])
        f=root/row['path']
        require(f.is_file() and not f.is_symlink(),'Missing/unsafe included file: '+row['path'])
        require(sha(f)==row['sha256'] and f.stat().st_size==row['bytes'],'File drift: '+row['path'])
        require(row['license'] in ['MIT','CC-BY-4.0','UPSTREAM_TERMS_RETAINED'],'Unresolved rights: '+row['path'])
        require(bool(row['roles']) and bool(row['rights_effect']),'Missing role/rights')
    dependency=json.loads((root/SUPPORT/'dependency-review.json').read_text())
    required={x['path'] for x in dependency['files']}
    require(len(required)==manifest['computational_closure_count']==60,'Computational closure count changed')
    require(required<=paths,'Incomplete reviewed computational closure')
    # Validate all recursively declared frozen oracle and historical-source pins.
    for base in [PROFILE,INTEGRATION]:
        contract=json.loads((root/base/'contract.json').read_text())
        freeze=json.loads((root/base/'freeze.json').read_text())
        for p,h in contract['source_sha256'].items():
            require(p in paths and sha(root/p)==h,'Missing/drifted source dependency: '+p)
        for p,h in freeze['files_sha256'].items():
            full=str(PurePosixPath(base)/p)
            require(full in paths and sha(root/full)==h,'Missing/drifted frozen oracle: '+full)
    for path in dependency['requirement_file_closure']:
        require(path in paths,'Missing requirements file')
        for line in (root/path).read_text().splitlines():
            if line.startswith('-r '):
                target=str(PurePosixPath(path).parent/line[3:].strip())
                require(target in paths,'Missing requirements include: '+target)
    # Keep source fixture rights and exact approved scope separate from original code.
    rights={r['path']:r['license'] for r in manifest['files']}
    for p in ['v2/data/sources/source-manifest.json','v2/data/fixtures/nhif_outpatient_fixture.csv',
              'v2/data/fixtures/nhif_inpatient_fixture.csv','v2/data/fixtures/geography_alias_fixture.csv']:
        require(rights[p]=='UPSTREAM_TERMS_RETAINED','Upstream fixture relicense')
    require(sha(root/'CITATION.cff')==manifest['root_citation_sha256'],'Historical root citation changed')
    require('version: "1.0.0"' in (root/'CITATION.cff').read_text(),'Historical citation version changed')
    citation=(root/SUPPORT/'CITATION.cff').read_text()
    require('version: "2.1.0"' in citation and citation.count('orcid:')==3,'Release citation mismatch')
    claims=json.loads((root/SUPPORT/'claims.json').read_text())
    require(claims['source_policy_acceptance']=='1/4' and claims['historical_orsd_acceptance']=='0/83'
            and claims['new_external_expert_responses']==0 and not claims['stable_published'],'Claim limits drift')
    for claim in claims['claims']:
        require(claim['evidence'] in paths or claim['evidence']==SUPPORT+'/manifest.json','Missing claim evidence')
    links=0
    for doc in sorted(p for p in paths if p.endswith('.md')):
        text=(root/doc).read_text()
        for target in re.findall(r'\]\(([^)]+)\)',text):
            if '://' in target or target.startswith('#'):continue
            f=(root/doc).parent.joinpath(target.split('#')[0]).resolve()
            require(f.is_relative_to(root.resolve()) and f.is_file(),'Broken document link: '+target);links+=1
    excluded=list(csv.DictReader((root/SUPPORT/'excluded-files.csv').open()))
    require(not paths.intersection(x['path'] for x in excluded),'Included/excluded conflict')
    require(all(len(x['sha256'])==64 for x in excluded),'Unpinned exclusion')
    return dict(included_files=len(paths),computational_files=len(required),excluded_snapshot_files=len(excluded),
                checked_document_links=links,manifest_sha256=sha(root/SUPPORT/'manifest.json'))

def cold(root,out):
    manifest=json.loads((root/SUPPORT/'manifest.json').read_text())
    with tempfile.TemporaryDirectory(prefix='cmpe-support-cold-') as folder:
        target=Path(folder)
        for p in [x['path'] for x in manifest['files']]+[SUPPORT+'/manifest.json']:
            dest=target/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/p,dest)
        verify(target)
        # Real missing-dependency and corrupt-payload controls use the cold tree.
        missing=target/'tools/v2_ontology/CheckOWL2DL.java';saved=missing.read_bytes();missing.unlink()
        try:verify(target)
        except ValueError:missing_refused=True
        else:raise ValueError('Missing Java dependency accepted')
        missing.write_bytes(saved)
        altered=target/PROFILE/'profile.ttl';saved=altered.read_bytes();altered.write_bytes(saved+b'\n# changed\n')
        try:verify(target)
        except ValueError:corruption_refused=True
        else:raise ValueError('Corrupted profile accepted')
        altered.write_bytes(saved)
        runs=[]
        commands=[['v2/release/2.1/support/0.1.0/verify_contract.py'],
                  [PROFILE+'/verify_profile.py','--output-dir',str(out/'cold-profile')],
                  [INTEGRATION+'/verify_integration.py','--preflight-only']]
        for n,args in enumerate(commands):
            run=subprocess.run([sys.executable,*args],cwd=target,capture_output=True,text=True,timeout=600)
            (out/f'cold-{n}.log').write_text(run.stdout+'\n'+run.stderr)
            require(run.returncode==0,'Cold command failed: '+' '.join(args)+'\n'+run.stdout+run.stderr)
            runs.append(dict(command=args,returncode=run.returncode))
        return dict(git_metadata_copied=False,commands=runs,missing_dependency_refused=missing_refused,
                    corrupt_payload_refused=corruption_refused,profile_replayed=True,database_preflight_only=True,
                    database_executed=False,deterministic_archive_constructed=False)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cold-profile',action='store_true')
    p.add_argument('--output-dir',type=Path,default=ROOT/'build/support-contract')
    args=p.parse_args();out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    result=dict(schema_version='CMPE-SupportVerification/0.1.0',passed=True,**verify(ROOT),ga_ready=False,
                stable_published=False,database_executed=False)
    if args.cold_profile:result['cold']=cold(ROOT,out)
    (out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))

if __name__=='__main__':main()
