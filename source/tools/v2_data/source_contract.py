"""Explicit P1 discovery/header contract. Metadata checks are not full-file checksums."""
from __future__ import annotations
import csv,hashlib
from pathlib import Path

class ContractError(ValueError):
    pass

def require(ok: bool, code: str):
    if not ok: raise ContractError(code)

def validate_discovery(spec: dict, metadata: dict) -> dict:
    lock=spec['published_contract']
    require(str(metadata.get('id'))==str(lock['record_id']), 'RECORD_ID_MISMATCH')
    require(metadata.get('doi')==spec['doi'], 'DOI_MISMATCH')
    require(metadata.get('metadata',{}).get('license',{}).get('id')==lock['license_id'], 'LICENSE_METADATA_MISMATCH')
    found=[f for f in metadata.get('files',[]) if f.get('key')==spec['file_contract']]
    require(len(found)==1, 'PUBLISHED_FILENAME_NOT_UNIQUE_OR_MISSING')
    file=found[0]
    require(file.get('checksum')==lock['checksum'], 'PUBLISHED_CHECKSUM_METADATA_MISMATCH')
    require(file.get('size')==lock['size_bytes'], 'PUBLISHED_SIZE_METADATA_MISMATCH')
    return {'record_id':lock['record_id'],'filename':file['key'],'checksum_metadata':file['checksum'],
            'size_metadata':file['size'],'license_id':lock['license_id'],'full_file_checksum_verified':False}

def validate_header(spec: dict, header: list[str]):
    require(header==spec['required_columns'], 'ORDERED_HEADER_MISMATCH')

def validate_local_csv(spec: dict, path: str|Path, mode: str, metadata: dict|None=None) -> dict:
    path=Path(path)
    if mode=='synthetic-fixture':
        fixture=spec['synthetic_fixture']
        require(path.name==fixture['filename'], 'FIXTURE_ALIAS_MISMATCH')
        require(hashlib.sha256(path.read_bytes()).hexdigest()==fixture['sha256'], 'FIXTURE_HASH_MISMATCH')
        discovery=None
    elif mode=='published-file':
        require(metadata is not None, 'METADATA_REQUIRED')
        discovery=validate_discovery(spec,metadata)
        require(path.name==spec['file_contract'], 'LOCAL_PUBLISHED_FILENAME_MISMATCH')
        require(path.stat().st_size==spec['published_contract']['size_bytes'], 'LOCAL_PUBLISHED_SIZE_MISMATCH')
        h=hashlib.md5()
        with path.open('rb') as f:
            for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
        require('md5:'+h.hexdigest()==spec['published_contract']['checksum'], 'LOCAL_FULL_CHECKSUM_MISMATCH')
        discovery['full_file_checksum_verified']=True
    else:
        raise ContractError('UNKNOWN_INPUT_MODE')
    with path.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f);validate_header(spec,reader.fieldnames or [])
        rows=sum(1 for row in reader if _valid_row(row))
    return {'mode':mode,'input_filename':path.name,'rows':rows,'header_columns':len(spec['required_columns']),
            'discovery':discovery,'synthetic_fixture':mode=='synthetic-fixture'}

def _valid_row(row):
    require(None not in row and all(v is not None for v in row.values()),'ROW_WIDTH_MISMATCH')
    return True

def validate_slice_manifest(spec: dict, metadata: dict, manifest: dict, folder: Path) -> dict:
    discovery=validate_discovery(spec,metadata)
    require(manifest['record_url']==spec['record_url'],'SLICE_RECORD_MISMATCH')
    require(manifest['published_filename']==spec['file_contract'],'SLICE_FILENAME_MISMATCH')
    require(manifest['published_size_bytes']==spec['published_contract']['size_bytes'],'SLICE_SIZE_MISMATCH')
    require('md5:'+manifest['published_md5_from_Zenodo_metadata_unverified_locally']==spec['published_contract']['checksum'],'SLICE_CHECKSUM_METADATA_MISMATCH')
    validate_header(spec,manifest['columns'])
    total=0
    for entry in manifest['strata']:
        p=folder/entry['selected_file'];b=p.read_bytes()
        require(hashlib.sha256(b).hexdigest()==entry['selected_file_sha256'],'SLICE_SHA256_MISMATCH')
        with p.open(encoding='utf-8-sig',newline='') as f:
            reader=csv.DictReader(f);validate_header(spec,reader.fieldnames or []);n=sum(1 for row in reader if _valid_row(row))
        require(n==entry['selected_rows'],'SLICE_ROW_COUNT_MISMATCH');total+=n
    require(total==manifest['selected_rows_total'],'SLICE_TOTAL_MISMATCH')
    return {'discovery':discovery,'rows':total,'slices':len(manifest['strata']),'header_columns':len(spec['required_columns']),
            'local_slice_hashes_verified':True,'full_published_file_downloaded_or_hashed':False}
