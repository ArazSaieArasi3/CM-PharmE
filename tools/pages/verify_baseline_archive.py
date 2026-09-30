#!/usr/bin/env python3
"""Read back committed baseline archives and reconcile every recorded file digest."""
import hashlib
import json
import zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
    count=0
    for path in sorted((ROOT/'docs/documentation/baselines').glob('*.json')):
        record=json.loads(path.read_text());archive=ROOT/record['archive_path']
        assert hashlib.sha256(archive.read_bytes()).hexdigest()==record['archive_sha256'],path
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            assert len(z.namelist())==len(set(z.namelist())), 'duplicate archive entries'
            manifest=json.loads(z.read('BASELINE-MANIFEST.json'))
            assert manifest['published_build_commit']==record['published_build_commit']
            assert manifest['baseline_id']==record['baseline_id']
            for name,digest in manifest['file_sha256_inventory'].items():
                assert hashlib.sha256(z.read(name)).hexdigest()==digest,name
                count+=1
        print(f"PASS: {record['baseline_id']}, archive SHA-256 and complete manifest read-back")
    assert count>0,'no declared archive to verify'
    print(f'PASS: {count} frozen file digests')
if __name__=='__main__':main()
