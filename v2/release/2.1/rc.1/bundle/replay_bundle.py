#!/usr/bin/env python3
"""Fresh extracted replay of two explicitly bounded existing verification scripts."""
import argparse,importlib.util,json,os,platform,re,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
import verify_bundle as v
import build_bundle as builder


def run(argv,log,env,timeout=300):
    with log.open('w') as stream:
        proc=subprocess.run([str(x) for x in argv],stdout=stream,stderr=subprocess.STDOUT,env=env,timeout=timeout)
    v.require(proc.returncode==0,'replay-command-failed; inspect '+str(log))
def version(argv):return subprocess.check_output(argv,text=True,stderr=subprocess.STDOUT).strip()


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--archive',required=True,type=Path);ap.add_argument('--sha256-file',required=True,type=Path);ap.add_argument('--work-root',required=True,type=Path);ap.add_argument('--output',required=True,type=Path);args=ap.parse_args();c=v.load_contract()
    v.require(list(sys.version_info[:2])==c['replay']['python_major_minor'],'Python 3.12 required')
    node=version(['node','--version']);java=version(['java','--version']);npm=version(['npm','--version'])
    v.require(node.startswith('v24.') and re.search(r'^(?:openjdk|java) 17[. ]',java),'Node 24 / Java 17 required')
    files,verified=v.inspect_archive(args.archive.resolve(),args.sha256_file.resolve());work=args.work_root.resolve();v.require(not work.exists() or not any(work.iterdir()),'replay-work-root-not-empty');work.mkdir(parents=True,exist_ok=True)
    extracted=work/'extracted'/c['top_directory'];extracted.mkdir(parents=True);source=extracted/'source';results=work/'results';results.mkdir();logs=results/'logs';logs.mkdir()
    modes={'source/'+row['path']:int(row['mode'][-3:],8) for row in json.loads(files['scope/payload-manifest.json'])['files']}
    for name,raw in files.items():
        path=extracted/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw);path.chmod(modes.get(name,0o644))
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONNOUSERSITE='1');env.pop('PYTHONPATH',None);env.pop('NODE_PATH',None)
    run([sys.executable,'-m','venv',work/'python-runtime'],logs/'venv.log',env)
    python=work/'python-runtime/bin/python';run([python,'-m','pip','install','--no-cache-dir','--disable-pip-version-check','-r',extracted/'requirements.lock'],logs/'pip.log',env)
    frozen=version([str(python),'-m','pip','freeze']);v.require(set(frozen.splitlines())==set(files['requirements.lock'].decode().splitlines()),'dependency-lock-drift')
    runtime=work/'node-runtime';runtime.mkdir();native=source/c['replay']['native']
    for name in ['package.json','package-lock.json']:shutil.copyfile(native/'runtime'/name,runtime/name)
    run(['npm','ci','--prefix',runtime,'--cache',work/'npm-cache','--ignore-scripts','--no-audit','--no-fund'],logs/'npm.log',env)
    environment=dict(python=platform.python_version(),node=node,npm=npm,java=java,python_packages=frozen.splitlines(),isolated_python=True,isolated_node=True,dependencies_downloaded=True)
    (work/'environment.json').write_bytes(v.encoded(environment))
    run([python,native/'verify_slice.py','--node-modules',runtime/'node_modules','--output-dir',results/'native'],logs/'native.log',env)
    native_report=json.loads((results/'native/report.json').read_text());expected_native=json.loads((native/'hosted-results.json').read_text());v.require(native_report==expected_native,'complete-native-report-mismatch')
    integration=source/c['replay']['integration'];run([python,integration/'verify_integration.py','--output',results/'integration.json'],logs/'integration.log',env)
    integration_report=json.loads((results/'integration.json').read_text());v.require(integration_report==json.loads((integration/'hosted-results.json').read_text()),'complete-integration-report-mismatch')
    scope=extracted/'scope';spec=importlib.util.spec_from_file_location('rc01_scope_replay',scope/'verify_scope.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);scope_contract,scope_data=module.load_scope()
    actual_source=builder.collect(source);manifest=json.loads(files['scope/payload-manifest.json']);tree={r['path']:dict(mode=r['mode'],blob=v.blob_sha(actual_source[r['path']]),bytes=len(actual_source[r['path']])) for r in manifest['files']}
    scope_report=module.validate(scope_data,scope_contract,tree,actual_source);expected_scope=json.loads(files['scope/hosted-results.json']);v.require(all(expected_scope[k]==value for k,value in scope_report.items()),'scope-replay-mismatch')
    actual_files=builder.collect(extracted);v.require(actual_files==files,'extracted-snapshot-modified');v.validate_files(c,actual_files)
    record=scope_report['evidence_record'];report=dict(schema_version=1,profile=c['profile'],passed=True,archive_sha256=verified['archive_sha256'],archive_bytes=verified['archive_bytes'],bundle_files=verified['bundle_files'],source_files=verified['source_files'],scope_source_commit=c['scope_source_commit'],payload_source_commit=c['payload_source_commit'],packaging_contract_sha256=v.CONTRACT_SHA,packaging_contract_commit=v.FREEZE,archive_negative_controls=verified['negative_controls'],clean_replay_completed=True,fresh_python_environment=True,fresh_npm_environment=True,existing_dependencies_reused=False,external_downloads_required=True,offline_reproduction_claimed=False,complete_native_report_equal=True,native_report_canonical_sha256=v.canonical_sha(native_report),native_profile=native_report['profile'],native_sha256=native_report['native']['candidate_sha256'],native_inventory=native_report['native']['inventory'],evidence_record=record,complete_integration_report_equal=True,integration_report_canonical_sha256=v.canonical_sha(integration_report),source_policy_totals=integration_report['totals'],source_scope_recheck_equal=True,extracted_snapshot_unchanged=True,database_reexecuted=False,all_policy_engines_reexecuted=False,full_20_family_candidate_execution=False,independent_scientific_acceptance=False,ga_ready=False,tag_created=False,release_published=False,claim_boundary='Fresh extracted bounded EvidenceRecord runtime replay plus committed four-policy dossier integration and scope/source integrity. No database/all-detector/full-model/scientific/GA acceptance or publication.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(v.encoded(report));print(v.encoded(report).decode())


if __name__=='__main__':main()
