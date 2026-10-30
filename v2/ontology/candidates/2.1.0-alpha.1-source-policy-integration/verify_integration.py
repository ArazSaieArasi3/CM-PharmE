#!/usr/bin/env python3
"""Validate four pinned evidence dossiers and claim limits; never run a converter."""
import argparse,copy,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
CONTRACT_SHA256='b08542015e186dde9453205d942d16bc92fc166c23aa052139ebfe3a25059852'
FREEZE_COMMIT='a87639243f8924a447ebfc7fd062bc1654169309'


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def canonical_hash(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def require(condition,reason):
    if not condition:raise ValueError(reason)


def inventory(model):
    props=[e for e in model['elements'] if e['type']=='Property']
    ids={
        'unknown_cardinality':sorted(e['id'] for e in props if e.get('cardinality') is None),
        'untyped_properties':sorted(e['id'] for e in props if e.get('propertyType') is None),
        'specialized_properties':sorted(e['id'] for e in props if e.get('subsettedProperties') or e.get('redefinedProperties')),
        'unknown_readonly':sorted(e['id'] for e in props if e.get('isReadOnly') is None)}
    counts=dict(elements=len(model['elements']),properties=len(props),**{k:len(v) for k,v in ids.items()})
    return counts,ids


def validate(data,contract):
    rules={r['rule']:r for r in contract['rules']}
    require(set(data['rules'])==set(rules),'missing-rule')
    state=data['state']
    for key,value in contract['forbidden_claims'].items():require(state.get(key) is value,'fabricated-acceptance')
    require(len(state['rules'])==4 and {r['rule'] for r in state['rules']}==set(rules),'missing-rule')
    for row in state['rules']:
        require(row['status']==contract['required_review_status'] and row['approval_evidence'] is None,'fabricated-acceptance')
        require(row['profile']==rules[row['rule']]['profile'],'profile-drift')
    require(canonical_hash(data['snapshot'])==contract['target_canonical_sha256'],'snapshot-drift')
    counts,ids=inventory(data['snapshot']);require(counts==contract['expected_inventory'],'inventory-drift')
    totals=dict(case_rows=0,historical_replay_rows=0,legacy_refusal_rows=0,native_admission_rows=0)
    summaries=[];fingerprint=None
    for name,item in data['rules'].items():
        expected=rules[name];report=item['hosted'];local=item['local'];oracle=item['oracles'];ci=item['ci'];sources=item['sources']
        require(report['passed'] is True and report['profile']==expected['profile'],'report-status')
        require(report['archive_commit']==contract['archive_commit']==sources['archive']['commit'],'archive-drift')
        require(ci['oracle_commit']==report['oracle_commit']==expected['oracle_commit'] and ci['tested_commit']==expected['implementation_commit'] and ci['run_id']==expected['run_id'],'provenance-drift')
        require(ci['artifact']['digest']==expected['artifact_digest'] and ci['artifact']['workflow_run']['head_sha']==ci['tested_commit'],'artifact-drift')
        latest={}
        for workflow in ci['workflows']:latest.setdefault(workflow['name'],workflow)
        require(all(w['conclusion']=='success' and w['head_sha']==ci['tested_commit'] for w in latest.values()),'ci-drift')
        for key in ['cases','historical_replays','refused_inputs','runtime_jar_order_sha256']:
            require(local[key]==report[key],'local-hosted-drift')
        current=(report['archive_commit'],report['compiler_sha256'],report['runtime_jar_order_sha256'])
        require(report['compiler_sha256']==sources['compiler']['sha256'],'compiler-drift')
        if fingerprint is None:fingerprint=current
        require(current==fingerprint,'runtime-fingerprint-drift')
        for flag in ['full_candidate_executed','modern_adapter_fidelity_claimed','author_scientific_acceptance_claimed']:
            require(report.get(flag) is False,'fabricated-acceptance')
        by_id={x['id']:x for x in oracle['cases']}
        require(len(report['cases'])==len(by_id)==expected['expected_cases'] and {x['id'] for x in report['cases']}==set(by_id),'case-count')
        for row in report['cases']:
            o=by_id[row['id']];require(row['pass'] is True and row['archived_occurrences']==o['expected_archived_occurrences'],'case-oracle')
            if name=='RelRig':
                for key in ['published_frame_match','rigid_dependency_review_required','mediation_baseline_review_required']:
                    require(row['profile'][key]==o['expected_'+key],'case-oracle')
                require(row['profile']['domain_error_established'] is False,'fabricated-acceptance')
            else:require(row['profile']['frame_match']==o['expected_profile_frame_match'],'case-oracle')
        require(len(report['historical_replays'])==expected['expected_historical'] and all(x.get('pass',x.get('pass_result')) is True for x in report['historical_replays']),'historical-replay')
        refusal_names=oracle.get('refused_inputs',oracle.get('legacy_refused_inputs'))
        require(len(report['refused_inputs'])==expected['expected_refusals'] and set(report['refused_inputs'])==set(refusal_names) and all(x['refused'] is True for x in report['refused_inputs'].values()),'refusal-drift')
        native=report.get('native_admission');native_count=len(native['cases']) if native else 0
        require(native_count==expected['expected_native_admission'],'native-count')
        if native:
            require(native==local['native_admission'] and all(x['pass_result'] is True and x['source_unchanged'] is True for x in native['cases']),'native-drift')
            native_oracles={x['id']:x for x in oracle['native_admission_oracles']}
            require({x['id'] for x in native['cases']}==set(native_oracles),'native-count')
            require(all(x['accepted'] is native_oracles[x['id']]['expected_accepted'] for x in native['cases']),'native-oracle')
            require(native['unknown_readonly_properties']==counts['unknown_readonly'] and sorted(native['unknown_readonly_ids'])==ids['unknown_readonly'],'native-inventory-drift')
            require(native['full_candidate_conversion_executed'] is False and native['full_candidate_detector_executed'] is False,'fabricated-acceptance')
            require(next(x for x in native['cases'] if x['id']=='unchanged-full-candidate')['accepted'] is False,'fabricated-acceptance')
        totals['case_rows']+=len(report['cases']);totals['historical_replay_rows']+=len(report['historical_replays']);totals['legacy_refusal_rows']+=len(report['refused_inputs']);totals['native_admission_rows']+=native_count
        summaries.append(dict(rule=name,profile=report['profile'],implementation_commit=ci['tested_commit'],run_id=ci['run_id'],case_rows=len(report['cases']),historical_rows=len(report['historical_replays']),refusal_rows=len(report['refused_inputs']),native_rows=native_count,scientific_acceptance='PENDING_AUTHOR_SCIENTIFIC_REVIEW'))
    require(totals==contract['expected_totals'],'total-drift')
    return dict(totals=totals,inventory_counts=counts,inventory_ids=ids,rules=summaries)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='build/source-policy-integration/report.json');args=ap.parse_args()
    require(sha(HERE/'contract.json')==CONTRACT_SHA256,'contract-drift');contract=json.loads((HERE/'contract.json').read_text())
    data=dict(state=json.loads((HERE/'review-state.json').read_text()),snapshot=json.loads((ROOT/contract['target_snapshot_path']).read_text()),rules={})
    require(sha(ROOT/contract['target_snapshot_path'])==contract['target_snapshot_sha256'],'snapshot-byte-drift')
    for item in contract['rules']:
        for path,digest in item['files_sha256'].items():require(sha(ROOT/path)==digest,'file-drift: '+path)
        p=ROOT/item['package'];files={key:json.loads((p/name).read_text()) for key,name in [('hosted','hosted-results.json'),('local','local-results.json'),('oracles','fixed-oracles.json'),('sources','sources.json'),('ci','ci-evidence.json')]}
        require(sha(p/'fixed-oracles.json')==files['hosted']['frozen_oracles_sha256'],'oracle-byte-drift')
        for path,digest in files['sources']['historical_inputs_sha256'].items():require(sha(ROOT/path)==digest,'historical-input-drift: '+path)
        data['rules'][item['rule']]=files
    result=validate(data,contract);controls=[]
    for name in contract['negative_controls']:
        trial=copy.deepcopy(data)
        if name=='tampered_case_result':trial['rules']['HomoFunc']['hosted']['cases'][0]['archived_occurrences']=0;trial['rules']['HomoFunc']['local']['cases'][0]['archived_occurrences']=0
        elif name=='snapshot_unknown_defaulted':next(e for e in trial['snapshot']['elements'] if e['type']=='Property' and e.get('isReadOnly') is None)['isReadOnly']=False
        elif name=='fabricated_acceptance':trial['state']['scientific_gate_closed']=True
        elif name=='missing_rule':del trial['rules']['RelRig']
        try:validate(trial,contract)
        except ValueError as err:
            expected_reason={'tampered_case_result':'case-oracle','snapshot_unknown_defaulted':'snapshot-drift','fabricated_acceptance':'fabricated-acceptance','missing_rule':'missing-rule'}[name]
            require(str(err)==expected_reason,'unexpected-negative-control-reason: '+name)
            controls.append(dict(id=name,refused=True,reason=str(err)))
        else:raise ValueError('negative-control-admitted: '+name)
    result.update(schema_version=1,bundle=contract['bundle'],contract_sha256=CONTRACT_SHA256,contract_freeze_commit=FREEZE_COMMIT,passed=True,negative_controls=controls,original_snapshot_sha256=contract['target_snapshot_sha256'],full_candidate_executed=False,author_scientific_accepted=False,scientific_gate_closed=False,release_approved=False,claim_boundary='Consistency and provenance of four scoped synthetic evidence packages only; row totals are bookkeeping, overlapping native inventories are not anti-pattern findings.')
    output=ROOT/args.output;output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(passed=True,totals=result['totals'],inventory_counts=result['inventory_counts'],negative_controls=len(controls),scientific_gate_closed=False),indent=2))


if __name__=='__main__':main()
