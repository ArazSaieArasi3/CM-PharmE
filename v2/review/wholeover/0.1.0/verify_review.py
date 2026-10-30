#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Recheck the bounded review card without rerunning the historical Java engine."""
import csv
import hashlib
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
SOURCE=ROOT/'v2/ontology/candidates/2.1.0-alpha.1-wholeover-policy'

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,message):
    if not ok:raise ValueError(message)

def main():
    pins=json.loads((HERE/'input-pins.json').read_text())
    for path,expected in pins['files_sha256'].items():
        require(digest(ROOT/path)==expected,'Pinned review input changed: '+path)
    sys.path.insert(0,str(SOURCE))
    spec=importlib.util.spec_from_file_location('wholeover_review_existing_policy',SOURCE/'run_policy.py')
    original=importlib.util.module_from_spec(spec);spec.loader.exec_module(original)
    frozen=json.loads((SOURCE/'fixed-oracles.json').read_text())
    local=json.loads((SOURCE/'local-results.json').read_text())
    hosted=json.loads((SOURCE/'hosted-results.json').read_text())
    fields=['cases','refused_inputs','historical_replays','runtime_jar_order_sha256',
            'frozen_oracles_sha256','profile','case_count','cases_passed',
            'full_candidate_executed','author_scientific_acceptance_claimed']
    for field in fields:require(local[field]==hosted[field],'Prior local/hosted mismatch: '+field)
    observed={x['id']:x for x in hosted['cases']}
    matrix=list(csv.DictReader((HERE/'boundary-matrix.csv').open()))
    require(len(matrix)==len(observed)==len(frozen['cases'])==16,'Missing or duplicate case')
    require(len({r['case_id'] for r in matrix})==16,'Duplicate matrix case')
    decisions=json.loads((HERE/'decision-card.json').read_text())
    require(decisions['author_disposition']=='PENDING' and decisions['source_policy_acceptances']=='1/4',
            'Invented scientific acceptance')
    require(decisions['full_candidate_executed'] is False,'Invented target execution')
    fresh=[]
    with tempfile.TemporaryDirectory(prefix='wholeover-card-') as folder:
        folder=Path(folder)
        for case in frozen['cases']:
            model=original.model_for(case);path=folder/(case['id']+'.refontouml')
            path.write_bytes(original.factory.serialize(model,case['id']))
            result=original.evaluate_frame(path);prior=observed[case['id']]
            require(result==prior['profile'],'Fresh predicate differs: '+case['id'])
            require(digest(path)==prior['fixture_sha256'],'Fresh fixture differs: '+case['id'])
            require(original.expected_parsed_fields(model)==prior['parsed_fields'],'Prior parsed-field witness differs')
            require(result['frame_match']==case['expected_profile_frame_match'],'Frozen oracle differs')
            require(prior['archived_occurrences']==case['expected_archived_occurrences'],'Prior archive observation differs')
            row=next(x for x in matrix if x['case_id']==case['id'])
            require(int(row['archived_observation'])==prior['archived_occurrences']
                    and int(row['named_profile_match'])==result['frame_match']
                    and row['disposition']==prior['disposition'],'Decision matrix differs')
            fresh.append(case['id'])
        refusals=original.refusal_checks(folder/'sum-two-mandatory.refontouml',folder)
        require(refusals==hosted['refused_inputs'],'Fresh refusal witnesses differ')
    source_only=[x['id'] for x in hosted['cases'] if x['disposition']=='SOURCE_ONLY_REVIEW_REQUIRED']
    require(source_only==decisions['source_only_review_cases'] and len(source_only)==4,'Review boundary drift')
    for path,expected in pins['files_sha256'].items():require(digest(ROOT/path)==expected,'Input mutation')
    result=dict(schema_version='CMPE-WholeOverDecisionCardCheck/0.1.0',passed=True,
        input_files_checked=len(pins['files_sha256']),fresh_profile_cases=len(fresh),fresh_refusal_controls=len(refusals),
        prior_local_hosted_fields_compared=len(fields),prior_historical_replay_records=len(hosted['historical_replays']),
        source_only_review_cases=source_only,archived_engine_rerun=False,new_primary_pdf_inspection=False,
        full_candidate_executed=False,author_disposition='PENDING',source_policy_acceptances='1/4',
        current_stable_distribution='2.1.0',new_semantic_release_created=False)
    (HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))

if __name__=='__main__':main()
