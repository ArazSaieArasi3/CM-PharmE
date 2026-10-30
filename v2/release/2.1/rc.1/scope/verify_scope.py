#!/usr/bin/env python3
"""RC-01 source inclusion and claim-boundary checks; no ontology/DB execution."""
import argparse,copy,csv,hashlib,io,json,re,subprocess
from pathlib import Path,PurePosixPath
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
CONTRACT_SHA='95f4ed0eeec7eceea3df1f03fdb4a4b28c7b9c50431f6679dac36fd054b3482a'
FREEZE_COMMIT='c3f8f3ee4c4dbe3ee43827a9ae18d104bce57ff2'


def sha(data):return hashlib.sha256(data).hexdigest()
def require(ok,reason):
    if not ok:raise ValueError(reason)
def git(source,*args):return subprocess.check_output(['git','-C',str(source),*args],text=True).strip()
def load_scope():
    require(sha((HERE/'scope-contract.json').read_bytes())==CONTRACT_SHA,'scope-contract-drift')
    contract=json.loads((HERE/'scope-contract.json').read_text())
    for name,digest in contract['pinned_metadata_sha256'].items():require(sha((HERE/name).read_bytes())==digest,'frozen-metadata-drift: '+name)
    data={key:json.loads((HERE/name).read_text()) for key,name in [('manifest','payload-manifest.json'),('artifacts','artifacts.json'),('claims','claims.json'),('limits','known-limits.json'),('ci','payload-ci.json')]}
    data['index']=list(csv.DictReader((HERE/'artifact-index.csv').open()))
    return contract,data


def read_source(source,contract):
    require(git(source,'rev-parse','HEAD')==contract['payload_source_commit'],'source-revision')
    require(git(source,'rev-parse','HEAD^{tree}')==contract['payload_git_tree'],'source-tree')
    require(not git(source,'status','--porcelain','--untracked-files=no'),'source-working-tree-dirty')
    tree={};files={}
    raw=subprocess.check_output(['git','-C',str(source),'ls-tree','-r','-z','-l','HEAD'])
    for record in raw.split(b'\0'):
        if not record:continue
        meta,path=record.split(b'\t',1);mode,kind,blob,size=meta.decode().split();path=path.decode();p=PurePosixPath(path)
        require(not p.is_absolute() and '..' not in p.parts and '.git' not in p.parts and kind=='blob' and mode in {'100644','100755'},'unsafe-source-entry')
        require((source/path).is_file() and not (source/path).is_symlink(),'unsafe-source-entry')
        tree[path]=dict(mode=mode,blob=blob,bytes=int(size));files[path]=(source/path).read_bytes()
    return tree,files


def validate(data,contract,tree,files):
    manifest=data['manifest'];art=data['artifacts'];claims=data['claims'];limits=data['limits'];ci=data['ci']
    rows=manifest['files'];by={x['path']:x for x in rows}
    require(len(by)==len(rows) and set(by)==set(tree),'source-file-set')
    require(manifest['source_commit']==contract['payload_source_commit'] and manifest['git_tree_sha']==contract['payload_git_tree'],'source-revision')
    require(len(rows)==manifest['source_files']==contract['expected']['source_files'],'source-file-set')
    for path,row in by.items():
        require(row['destination']=='source/'+path and row['mode']==tree[path]['mode'] and row['git_blob_sha']==tree[path]['blob'] and row['bytes']==len(files[path])==tree[path]['bytes'] and row['sha256']==sha(files[path]),'source-file-integrity')
    total=sum(x['bytes'] for x in rows);require(total==manifest['source_bytes']==contract['expected']['source_bytes'],'source-file-integrity')
    groups=art['groups'];by_group={g['id']:g for g in groups}
    require(len(groups)==len(by_group)==contract['expected']['review_groups'],'artifact-group-drift')
    require([x['id'] for x in data['index']]==[g['id'] for g in groups],'artifact-index-drift')
    for g,index in zip(groups,data['index']):
        members=[x for x in rows if x['review_group']==g['id']]
        require(members and len(members)==g['file_count']==int(index['files']) and sum(x['bytes'] for x in members)==g['bytes']==int(index['bytes']),'artifact-index-drift')
        require(g['primary_path'] in by and by[g['primary_path']]['review_group']==g['id'] and index['primary_path']==g['primary_path'] and index['version']==g['version'] and index['role']==g['role'],'artifact-index-drift')
    for path,row in by.items():
        selected=next((g['id'] for g in groups if path.startswith(g['path'])),None)
        require(row['review_group']==selected and row['role']==('SELECTED_REVIEW_ASSET' if selected else 'ARCHIVAL_SOURCE_ONLY'),'artifact-role-drift')
    publication=claims['publication']
    require(publication['version']==contract['target']=='2.1.0-rc.1' and publication['kind']=='EXPERIMENTAL_RESEARCH_CHECKPOINT' and all(publication[k] is False for k in ['published','tag_created','ga_ready']),'release-policy')
    require(all(claims['native'][k] is False for k in ['complete_validator','complete_native_to_owl_translation','independent_scientific_acceptance']),'unsupported-claim')
    require(claims['source_policy']['scientific_acceptances']==0 and claims['source_policy']['full_candidate_executed'] is False and claims['orsd']['expert_approval'] is False and claims['orsd']['author_accepted_rows']==0,'unsupported-claim')
    require(claims['rdb']['production_migration'] is False and claims['rdb']['full_36_mapping_acceptance'] is False and claims['rdb']['copied_w6_only'] is True and claims['modules']['stable_semantic_acceptance'] is False,'unsupported-claim')
    require(limits['release_published'] is False and limits['tag_created'] is False and limits['full_20_family_candidate_execution'] is False and limits['complete_native_owl_alignment'] is False and limits['source_policy_scientific_acceptances']==0 and limits['final_ga_gate_issues']==contract['required_held_gates'],'unsupported-claim')
    native_path=contract['current_native_path'];require(claims['native']['path']==limits['current_native_path']==by_group['native-current']['primary_path']==native_path,'current-candidate-mismatch')
    require(sha(files[native_path])==limits['current_native_sha256']==contract['current_native_sha256'],'current-candidate-mismatch')
    model=json.loads(files[native_path]);props=[e for e in model['elements'] if e['type']=='Property']
    inventory=dict(elements=len(model['elements']),properties=len(props),unknown_readonly=sum(e.get('isReadOnly') is None for e in props),unknown_cardinality=sum(e.get('cardinality') is None for e in props),untyped_properties=sum(e.get('propertyType') is None for e in props),specialized_properties=sum(bool(e.get('subsettedProperties') or e.get('redefinedProperties')) for e in props))
    require(inventory==limits['input_inventories'] and limits['inventories_are_overlapping_not_detector_findings'] is True,'inventory-mismatch')
    er=json.loads(files[by_group['native-current']['path']+'hosted-results.json'])
    require(er['passed'] is True and er['profile']==claims['native']['profile']==by_group['native-current']['version'] and er['native']['candidate_sha256']==sha(files[native_path]),'native-evidence-drift')
    require(er['native']['schema_serialization']['guarded_roundtrip_equal'] is True and claims['native']['schema_and_guarded_roundtrip'] is True,'native-evidence-drift')
    history=er['historical_shacl_rows'];actual=dict(new_shacl_rows=len(er['shacl_cases']),contextclass_rows=len(er['contextclass_shacl_rows']),temporal_rows=len(er['temporal_cases']),hermit_rows=len(er['hermit_cases']),historical_before_matches=sum(x['before_pass'] for x in history),original_after_matches=sum(x['historical_oracle_matches'] for x in history),prospective_after_matches=sum(x['prospective_pass'] for x in history),declared_transitions=len(er['contract_transitions']),historical_oracles_rewritten=False,prospective_contract=er['prospective_contract'])
    require(actual==claims['evidence_record'] and er['historical_inputs_unchanged'] is True,'witness-transition-mismatch')
    integ=json.loads(files[by_group['policy-integration']['primary_path']]);pclaims=claims['source_policy']
    require(integ['passed'] is True and integ['bundle']==pclaims['bundle']==by_group['policy-integration']['version'] and integ['full_candidate_executed'] is False and integ['author_scientific_accepted'] is False,'policy-evidence-drift')
    require(integ['totals']==dict(case_rows=pclaims['case_rows'],historical_replay_rows=pclaims['historical_rows'],legacy_refusal_rows=pclaims['legacy_refusal_rows'],native_admission_rows=pclaims['native_admission_rows']),'policy-evidence-drift')
    for name in ['policy-relcomp','policy-wholeover','policy-relrig','policy-homofunc','contextclass-lineage']:
        rep=json.loads(files[by_group[name]['path']+'hosted-results.json']);require(rep['passed'] is True and rep['profile']==by_group[name]['version'],'profile-version-drift')
    orsd=json.loads(files[by_group['orsd']['primary_path']]);require(orsd['document_version']==claims['orsd']['document_version']==by_group['orsd']['version'] and orsd['metrics']['requirement_rows']==len(orsd['requirements'])==claims['orsd']['registered_rows']==83 and orsd['metrics']['author_accepted_rows']==claims['orsd']['author_accepted_rows']==0,'orsd-evidence-drift')
    for group_id in ['rdb-m3','rdb-m4']:
        report=json.loads(files[by_group[group_id]['path']+'hosted-results.json']);require(report['passed'] is True and report['database_executed'] is True and report['rollback_restored'] is True,'rdb-evidence-drift')
    require(ci['source_commit']==contract['payload_source_commit'],'source-ci-drift');cohort={w['name']:w for w in ci['workflows']}
    require(len(cohort)==ci['source_workflow_families']==23 and all(w['head_sha']==contract['payload_source_commit'] and w['conclusion']=='success' for w in cohort.values()),'source-ci-drift')
    require(all(any(('RDB-M'+str(n)+' ') in name for name in cohort) for n in range(1,5)),'source-ci-drift')
    citation=files['CITATION.cff'].decode();match=re.search(r'^version:\s*"?([^"\n]+)',citation,re.M)
    require(match and match.group(1).strip()==claims['citation']['root_version']==art['archival_citation_version']=='1.0.0' and claims['citation']['root_is_current_rc_citation'] is False and claims['citation']['generated_rc_citation_required'] is True and limits['source_root_citation_is_historical'] is True,'citation-scope')
    root_license=any(name in files for name in ['LICENSE','LICENSE.md','LICENSE.txt','LICENCE','COPYING']);require(limits['source_root_blanket_license_file_found']==root_license and limits['new_blanket_license_assumed'] is False,'license-scope')
    return dict(source_files=len(rows),source_bytes=total,review_groups=len(groups),selected_review_files=sum(x['review_group'] is not None for x in rows),native_sha256=sha(files[native_path]),native_inventory=inventory,evidence_record=actual,source_policy_case_rows=pclaims['case_rows'],orsd_registered_rows=83,source_workflow_families=23)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source-root',required=True,type=Path);ap.add_argument('--output',default='build/rc01-scope/report.json');args=ap.parse_args()
    contract,data=load_scope();source=args.source_root.resolve();tree,files=read_source(source,contract);result=validate(data,contract,tree,files);trials=[]
    for oracle in contract['expected']['negative_controls']:
        trial=copy.deepcopy(data);name=oracle['id'];path=contract['current_native_path']
        if name=='missing-current-asset':trial['manifest']['files']=[x for x in trial['manifest']['files'] if x['path']!=path]
        elif name=='tampered-file-digest':next(x for x in trial['manifest']['files'] if x['path']==path)['sha256']='0'*64
        elif name=='hidden-native-unknowns':trial['limits']['input_inventories']['unknown_readonly']=0
        elif name=='suppressed-witness-transition':trial['claims']['evidence_record']['original_after_matches']=89
        elif name=='full-validator-claim':trial['claims']['native']['complete_validator']=True
        elif name=='scientific-approval-claim':trial['claims']['native']['independent_scientific_acceptance']=True
        elif name=='complete-native-owl-claim':trial['claims']['native']['complete_native_to_owl_translation']=True
        elif name=='ga-release-label':trial['claims']['publication']['kind']='FINAL_GA'
        elif name=='historical-citation-promoted':trial['claims']['citation']['root_is_current_rc_citation']=True
        try:validate(trial,contract,tree,files)
        except ValueError as error:
            require(str(error)==oracle['expected_reason'],'unexpected-negative-control: '+name);trials.append(dict(id=name,refused=True,reason=str(error)))
        else:raise ValueError('unsupported-claim-or-manifest-admitted: '+name)
    result.update(schema_version=1,scope_id=contract['scope_id'],contract_sha256=CONTRACT_SHA,freeze_commit=FREEZE_COMMIT,payload_source_commit=contract['payload_source_commit'],payload_git_tree=contract['payload_git_tree'],passed=True,scope_frozen=True,negative_controls=trials,archive_created=False,clean_replay_completed=False,release_published=False,tag_created=False,ga_ready=False,claim_boundary='Source inclusion/provenance and scope/claim checks only. Scientific/GA acceptance, archive construction, cold replay and publication remain separate.')
    output=ROOT/args.output;output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:result[k] for k in ['passed','source_files','source_bytes','review_groups','selected_review_files','source_workflow_families','archive_created','release_published']},indent=2));print('Negative controls refused:',len(trials))


if __name__=='__main__':main()
