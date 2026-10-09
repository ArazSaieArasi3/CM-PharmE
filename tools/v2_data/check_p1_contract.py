"""Replay pinned discovery, negative contracts, W6 fixture preflight and real-slice migration."""
import argparse,copy,csv,json,subprocess,sys
from pathlib import Path
from tempfile import TemporaryDirectory
from source_contract import validate_discovery,validate_header,validate_local_csv,validate_slice_manifest,ContractError
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',default='build/w6/source-contract');a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
 spec=next(x for x in json.loads((ROOT/'v2/data/sources/source-manifest.json').read_text())['sources'] if x['id']=='P1-NHIF-OUTPATIENT')
 metadata=json.loads((ROOT/spec['published_contract']['metadata_snapshot']).read_text());source=ROOT/'v2/ontology/candidates/2.1.0-alpha.1-g3-3-d-real-source-migration';slices=json.loads((source/'source-slice-manifest.json').read_text())
 discovery=validate_discovery(spec,metadata);slice_result=validate_slice_manifest(spec,metadata,slices,source)
 fixture=ROOT/spec['synthetic_fixture']['path'];fixture_result=validate_local_csv(spec,fixture,'synthetic-fixture');cases=[]
 def reject(name,fn,expected):
  try:fn();actual='ACCEPTED'
  except ContractError as e:actual=str(e)
  cases.append({'name':name,'expected':expected,'actual':actual,'pass':actual==expected})
 stale=copy.deepcopy(spec);stale['file_contract']='nhif_outpatient_pharmacy_combined.csv'
 reject('stale-description-filename',lambda:validate_discovery(stale,metadata),'PUBLISHED_FILENAME_NOT_UNIQUE_OR_MISSING')
 for key,value,code in [('checksum','md5:00000000000000000000000000000000','PUBLISHED_CHECKSUM_METADATA_MISMATCH'),('size',17,'PUBLISHED_SIZE_METADATA_MISMATCH')]:
  altered=copy.deepcopy(metadata);next(f for f in altered['files'] if f['key']==spec['file_contract'])[key]=value
  reject(key+'-metadata-mismatch',lambda:validate_discovery(spec,altered),code)
 altered=copy.deepcopy(metadata);altered['id']=19160826;reject('wrong-record',lambda:validate_discovery(spec,altered),'RECORD_ID_MISMATCH')
 altered=copy.deepcopy(metadata);altered['metadata']['license']['id']='unknown';reject('wrong-license',lambda:validate_discovery(spec,altered),'LICENSE_METADATA_MISMATCH')
 reject('missing-header-column',lambda:validate_header(spec,spec['required_columns'][:-1]),'ORDERED_HEADER_MISMATCH')
 reject('reordered-header',lambda:validate_header(spec,list(reversed(spec['required_columns']))),'ORDERED_HEADER_MISMATCH')
 altered=copy.deepcopy(slices);altered['published_filename']='lookalike.csv';reject('slice-lookalike-source',lambda:validate_slice_manifest(spec,metadata,altered,source),'SLICE_FILENAME_MISMATCH')
 altered=copy.deepcopy(slices);altered['strata'][0]['selected_file_sha256']='0'*64;reject('slice-tampering',lambda:validate_slice_manifest(spec,metadata,altered,source),'SLICE_SHA256_MISMATCH')
 with TemporaryDirectory() as td:
  temp=Path(td);fake=temp/fixture.name;fake.write_bytes(fixture.read_bytes()+b'\n');reject('tampered-fixture',lambda:validate_local_csv(spec,fake,'synthetic-fixture'),'FIXTURE_HASH_MISMATCH')
  fake=temp/spec['file_contract'];fake.write_bytes(fixture.read_bytes());reject('fixture-renamed-as-published',lambda:validate_local_csv(spec,fake,'published-file',metadata),'LOCAL_PUBLISHED_SIZE_MISMATCH')
  reject('unrecognized-mode',lambda:validate_local_csv(spec,fixture,'automatic'),'UNKNOWN_INPUT_MODE')
  report=temp/'w6-preflight.json';subprocess.run([sys.executable,str(ROOT/'tools/v2_data/bootstrap_ingest.py'),'--contract-only','--report',str(report)],cwd=ROOT,check=True,capture_output=True,text=True)
  adapter=json.loads(report.read_text())
  migration=temp/'migration';cmd=[sys.executable,str(source/'migrate_g3d.py'),str(source/'source-slice-manifest.json'),str(ROOT/'v2/ontology/candidates/2.1.0-alpha.1-four-domain-refinement/combined.shacl.ttl'),str(migration)]
  run=subprocess.run(cmd,cwd=ROOT,check=True,capture_output=True,text=True)
  migrated=json.loads((migration/'migration-results.json').read_text());(out/'migration-results.json').write_text(json.dumps(migrated,ensure_ascii=False,indent=2)+'\n')
  before=json.loads((source/'migration-results.json').read_text())
  exact=migrated['abox']['sha256']==before['abox']['sha256']
 result={'status':'CONTRACT_REPAIRED_WITH_BOUNDED_REPLAY','metadata_scope':'archived official API excerpt; pinned HTML filename/MD5 rechecked this run; API refresh timed out',
  'published_discovery':discovery,'real_slice_contract':slice_result,'synthetic_fixture_contract':fixture_result,'bootstrap_contract_only':adapter,
  'negative_cases':cases,'negative_pass':sum(x['pass'] for x in cases),'negative_total':len(cases),'replayed_rows':migrated['input']['schema_accepted'],'replayed_triples':migrated['mapped']['rdf_triples'],
  'migration_negative_pass':migrated['negative_sensitivity']['passed'],'migration_full_shapes_conform':migrated['full_candidate_pyshacl']['conforms'],'canonical_abox_unchanged':exact,
  'full_W6_database_execution':'PENDING_GITHUB_CI','full_file_downloaded_or_locally_checksummed':False}
 result['local_checks_pass']=all(x['pass'] for x in cases) and exact and result['migration_full_shapes_conform']
 (out/'contract-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ['local_checks_pass','negative_pass','negative_total','replayed_rows','replayed_triples','canonical_abox_unchanged','full_W6_database_execution']}))
 if not result['local_checks_pass']:raise SystemExit(1)
if __name__=='__main__':main()
