#!/usr/bin/env python3
"""Independent WholeOver frame/profile and unchanged archived-runtime comparison."""
import argparse
import copy
import hashlib
import importlib.util
import json
import platform
import re
import subprocess
import tempfile
from pathlib import Path

from frame_policy import evaluate_frame, PROFILE, XMI, XSI
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OLD = HERE.parent / "2.1.0-alpha.1-detector-calibration"
SOURCES = json.loads((HERE / "sources.json").read_text())
ORACLES = json.loads((HERE / "fixed-oracles.json").read_text())
ORACLE_SHA256 = "8e899db1240fe26e2f690e5708efed260eac5d708b3ec74f200df9054441e166"
spec = importlib.util.spec_from_file_location("wholeover_witness_factory", OLD / "make_fixtures.py")
factory = importlib.util.module_from_spec(spec); spec.loader.exec_module(factory)


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def command(args, timeout=60):
    result = subprocess.run([str(x) for x in args],capture_output=True,text=True,timeout=timeout)
    if result.returncode: raise RuntimeError(result.stdout[-1000:]+result.stderr[-3000:])
    if re.search(r'exception|error|failed', result.stderr, re.I):
        raise RuntimeError("Runtime stderr requires investigation: " + result.stderr[-3000:])
    return result.stdout


def model_for(case):
    model=factory.overlap('WholeOver')
    model['sets'][0]['disjoint']=case['disjoint']
    for i,relation in enumerate(model['relations']):
        relation['ends'][1].update(lower=case['lowers'][i],upper=case['uppers'][i])
        if case['mutation']=='whole-plural':relation['ends'][0].update(lower=0,upper=5)
        if case['mutation']=='reordered':relation['ends'].reverse()
    return model


def expected_parsed_fields(model):
    rows=['CLASS|'+c['name']+'|'+c['type']+'|'+str(c['abstract']).lower() for c in model['classes']]
    for relation in model['relations']:
        rows.append('REL|'+relation['name']+'|'+relation['type'])
        for i,end in enumerate(relation['ends']):
            rows.append('|'.join(['END',relation['name'],str(i),end['name'],end['type'],str(end['lower']),str(end['upper']),end['aggregation'],','.join(sorted(end['subset']))]))
    rows += ['GEN|'+g['specific']+'|'+g['general'] for g in model['generalizations']]
    rows += ['SET|'+g['name']+'|'+str(g['disjoint']).lower()+'|'+str(g['complete']).lower()+'|'+','.join(sorted(x['specific']+'>'+x['general'] for x in model['generalizations'] if x['name'] in g['generalizations'])) for g in model['sets']]
    return sorted(rows)


def refusal_checks(base, output):
    def trial(name, mutate):
        root=ET.parse(base).getroot();mutate(root)
        path=output/(name+'.refontouml');ET.ElementTree(root).write(path,encoding='utf-8',xml_declaration=True)
        try: evaluate_frame(path)
        except ValueError as error:
            if str(error)!=name:raise AssertionError((name,str(error)))
            return {'refused':True,'reason':str(error),'sha256':sha(path)}
        raise AssertionError('Malformed/unsupported input admitted: '+name)
    def part(root):return root.find("packagedElement[@name='r1']/ownedEnd[@name='r1B']")
    operations={
        'missing_lower':lambda r:part(r).remove(part(r).find('lowerValue')),
        'missing_upper':lambda r:part(r).remove(part(r).find('upperValue')),
        'negative_lower':lambda r:part(r).find('lowerValue').set('value','-1'),
        'invalid_interval':lambda r:part(r).find('upperValue').set('value','0'),
        'untyped_end':lambda r:part(r).attrib.pop('type'),
        'duplicate_id':lambda r:r.append(copy.deepcopy(r.find("packagedElement[@name='Parent']"))),
        'unsupported_subsetting':lambda r:part(r).set('subsettedProperty','r2B'),
        'missing_disjoint':lambda r:r.find("packagedElement[@name='Overlap']").attrib.pop('isDisjoint'),
        'ambiguous_aggregation':lambda r:part(r).set('aggregation','shared'),
        'unsupported_ancestry':lambda r:r.find("packagedElement[@name='A']/generalization").set('general','Base'),
    }
    assert set(operations)==set(ORACLES['refused_inputs'])
    return {name:trial(name,fn) for name,fn in operations.items()}


def verify_inputs(archive,ecj):
    assert sha(HERE/'fixed-oracles.json')==ORACLE_SHA256,'Frozen oracle bytes changed'
    assert command(['git','-C',archive,'rev-parse','HEAD']).strip()==SOURCES['archive']['commit']
    assert not command(['git','-C',archive,'status','--porcelain','--untracked-files=no']).strip()
    assert sha(ecj)==SOURCES['compiler']['sha256']
    for path,digest in SOURCES['archive']['files'].items():assert sha(archive/path)==digest,path
    for path,digest in SOURCES['historical_inputs_sha256'].items():assert sha(ROOT/path)==digest,path


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--archive',required=True,type=Path);ap.add_argument('--ecj',required=True,type=Path)
    ap.add_argument('--output-dir',default='build/wholeover-policy');a=ap.parse_args()
    archive=a.archive.resolve();ecj=a.ecj.resolve();output=ROOT/a.output_dir;output.mkdir(parents=True,exist_ok=True)
    fixtures=output/'fixtures';fixtures.mkdir(exist_ok=True)
    verify_inputs(archive,ecj)
    old=json.loads((OLD/'calibration-results.json').read_text())
    jars=[archive/path for path in old['jar_order']];assert len(jars)>=70 and all(x.is_file() for x in jars)
    rows=[];historical=[]
    with tempfile.TemporaryDirectory() as temp:
        classes=Path(temp)/'classes';classes.mkdir()
        cp=':'.join([str(classes)]+[str(x) for x in jars])
        sourcepath=':'.join(str(archive/p/'src') for p in ['br.ufes.inf.nemo.ontouml','br.ufes.inf.nemo.common','br.ufes.inf.nemo.antipattern'])
        compile_args=['java','-jar',ecj,'-nowarn','-d',classes,'-classpath',cp,'-sourcepath',sourcepath,HERE/'WholeOverRuntime.java',OLD/'InspectLegacy.java']
        compiled=command(compile_args,180);(output/'compile.log').write_text(compiled)
        def run_fixture(path, expected_fields):
            inspected=command(['java','-cp',cp,'InspectLegacy',path],45)
            actual=sorted(line for line in inspected.splitlines() if line.startswith(('CLASS|','REL|','END|','GEN|','SET|')))
            assert actual==expected_fields,('Parser field mismatch',str(path),actual,expected_fields)
            raw=command(['java','-cp',cp,'WholeOverRuntime',path],45)
            match=re.search(r'CMPE_WHOLEOVER_COUNT=(\d+)',raw)
            assert match and not re.search(r'exception|error|failed',raw,re.I),raw
            return int(match[1]),actual,raw
        for case in ORACLES['cases']:
            model=model_for(case);path=fixtures/(case['id']+'.refontouml')
            path.write_bytes(factory.serialize(model,case['id']))
            count,parsed,raw=run_fixture(path,expected_parsed_fields(model))
            policy=evaluate_frame(path)
            assert count==case['expected_archived_occurrences'],(case['id'],count)
            assert policy['frame_match']==case['expected_profile_frame_match'],(case['id'],policy)
            disposition=('BOTH_MATCH_REQUIRES_DOMAIN_REVIEW' if count and policy['frame_match'] else
                         'ENGINE_ONLY_REVIEW_REQUIRED' if count else
                         'SOURCE_ONLY_REVIEW_REQUIRED' if policy['frame_match'] else
                         'NO_MATCH_IN_THIS_FRAME_NOT_CLEAN_CERTIFICATE')
            rows.append({'id':case['id'],'expected_archived_occurrences':case['expected_archived_occurrences'],
                         'archived_occurrences':count,'expected_profile_frame_match':case['expected_profile_frame_match'],
                         'profile':policy,'disposition':disposition,'pass':True,'fixture_sha256':sha(path),
                         'parsed_fields':parsed,'engine_output':raw.strip()})
        for name in ['positive','negative','upper-sum-two']:
            prior=next(r for r in old['rows'] if r['family']=='WholeOver' and r['name']==name)
            path=OLD/'fixtures'/('WholeOver-'+name+'.refontouml')
            count,parsed,raw=run_fixture(path,prior['expected_parsed_fields'])
            assert count==prior['actual_occurrences'] and sha(path)==prior['sha256']
            historical.append({'id':name,'pass':True,'unchanged_sha256':sha(path),'archived_occurrences':count,
                               'profile_frame_match':evaluate_frame(path)['frame_match'],'engine_output':raw.strip()})
    refusals=refusal_checks(fixtures/'sum-two-mandatory.refontouml',fixtures)
    verify_inputs(archive,ecj)
    report={'schema_version':1,'passed':True,'profile':PROFILE,'slice':'P5e-2 source-internal threshold conflict',
            'oracle_commit':'a689d3e93bc2ab8c16a05c9f5719b8d2c12ce62a','archive_commit':SOURCES['archive']['commit'],
            'frozen_oracles_sha256':ORACLE_SHA256,'runtime_error_stderr_rejected':True,
            'archive_tracked_source_unchanged':True,'compiler_sha256':sha(ecj),'historical_inputs_unchanged':True,
            'software':{'python':platform.python_version(),'java':subprocess.check_output(['java','-version'],stderr=subprocess.STDOUT,text=True).strip()},
            'runtime_jar_order_sha256':{str(x.relative_to(archive)):sha(x) for x in jars},
            'cases':rows,'case_count':len(rows),'cases_passed':len(rows),'historical_replays':historical,
            'refused_inputs':refusals,'engine_only_review_cases':[r['id'] for r in rows if r['disposition']=='ENGINE_ONLY_REVIEW_REQUIRED'],
            'source_only_review_cases':[r['id'] for r in rows if r['disposition']=='SOURCE_ONLY_REVIEW_REQUIRED'],
            'source_internal_threshold_conflict':True,
            'full_candidate_executed':False,'modern_adapter_fidelity_claimed':False,'author_scientific_acceptance_claimed':False,
            'boundary':'Independent declared-frame predicate and unchanged archived runtime compared on synthetic witnesses. A profile non-match is not absence of domain error; whole-model applicability and scientific/author release gates remain open.'}
    (output/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed':True,'cases':len(rows),'historical_replays':len(historical),'refused':len(refusals),
                      'source_only_review_cases':report['source_only_review_cases'],'full_candidate_executed':False},indent=2))


if __name__=='__main__':main()
