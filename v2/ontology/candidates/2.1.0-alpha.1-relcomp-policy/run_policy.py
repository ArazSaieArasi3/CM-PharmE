#!/usr/bin/env python3
"""Independent RelComp frame/profile and unchanged archived-runtime comparison."""
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
ORACLE_SHA256 = "55b4956650c86e768cd0fd616ddb8f315ec9e71fa0e3dfb6c828772db62a7b16"
spec = importlib.util.spec_from_file_location("relcomp_witness_factory", OLD / "make_fixtures.py")
factory = importlib.util.module_from_spec(spec); spec.loader.exec_module(factory)


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def command(args, timeout=60):
    result = subprocess.run([str(x) for x in args],capture_output=True,text=True,timeout=timeout)
    if result.returncode: raise RuntimeError(result.stdout[-1000:]+result.stderr[-3000:])
    if re.search(r'exception|error|failed', result.stderr, re.I):
        raise RuntimeError("Runtime stderr requires investigation: " + result.stderr[-3000:])
    return result.stdout


def model_for(case):
    f = factory
    model = f.model([f.cls("Container"),f.cls("Person"),f.cls("A","SubKind"),f.cls("B","SubKind")],
                    [f.rel("outer","Container","Person",ca=(0,1),cb=(case['lower'],case['upper'])),
                     f.rel("inner","A","B",ca=(0,1),cb=(0,1))],
                    [f.gen("A","Person"),f.gen("B","Person")])
    mutation=case['mutation']
    if mutation=='unrelated-inner': model['generalizations'][1]=f.gen('B','Container')
    elif mutation=='transitive-inner':
        model['classes'].append(f.cls('Middle','SubKind'))
        model['generalizations'][0]=f.gen('A','Middle');model['generalizations'].append(f.gen('Middle','Person'))
    elif mutation=='nonshared-plural':
        model['relations'][0]['ends'][0].update(lower=1,upper=2)
    elif mutation.startswith('reordered-'):
        model['relations'][0]['ends'].reverse()
    return model


def expected_parsed_fields(model):
    rows=['CLASS|'+c['name']+'|'+c['type']+'|'+str(c['abstract']).lower() for c in model['classes']]
    for relation in model['relations']:
        rows.append('REL|'+relation['name']+'|'+relation['type'])
        for i,end in enumerate(relation['ends']):
            rows.append('|'.join(['END',relation['name'],str(i),end['name'],end['type'],str(end['lower']),str(end['upper']),end['aggregation'],','.join(sorted(end['subset']))]))
    rows += ['GEN|'+g['specific']+'|'+g['general'] for g in model['generalizations']]
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
    def outer_end(root):return root.find("packagedElement[@name='outer']/ownedEnd[@name='outerB']")
    def cycle(root):
        person=root.find("packagedElement[@name='Person']")
        ET.SubElement(person,'generalization',{XMI+'id':'cycleToA','general':'A'})
    operations={
        'missing_lower':lambda r:outer_end(r).remove(outer_end(r).find('lowerValue')),
        'missing_upper':lambda r:outer_end(r).remove(outer_end(r).find('upperValue')),
        'negative_lower':lambda r:outer_end(r).find('lowerValue').set('value','-1'),
        'invalid_interval':lambda r:outer_end(r).find('upperValue').set('value','0'),
        'untyped_end':lambda r:outer_end(r).attrib.pop('type'),
        'duplicate_id':lambda r:r.append(copy.deepcopy(r.find("packagedElement[@name='Person']"))),
        'cyclic_generalization':cycle,
        'unsupported_subsetting':lambda r:outer_end(r).set('subsettedProperty','innerB'),
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
    ap.add_argument('--output-dir',default='build/relcomp-policy');a=ap.parse_args()
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
        compile_args=['java','-jar',ecj,'-nowarn','-d',classes,'-classpath',cp,'-sourcepath',sourcepath,HERE/'RelCompRuntime.java',OLD/'InspectLegacy.java']
        compiled=command(compile_args,180);(output/'compile.log').write_text(compiled)
        def run_fixture(path, expected_fields):
            inspected=command(['java','-cp',cp,'InspectLegacy',path],45)
            actual=sorted(line for line in inspected.splitlines() if line.startswith(('CLASS|','REL|','END|','GEN|','SET|')))
            assert actual==expected_fields,('Parser field mismatch',str(path),actual,expected_fields)
            raw=command(['java','-cp',cp,'RelCompRuntime',path],45)
            match=re.search(r'CMPE_RELCOMP_COUNT=(\d+)',raw)
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
        for name in ['positive','negative','zero-lower-bound']:
            prior=next(r for r in old['rows'] if r['family']=='RelComp' and r['name']==name)
            path=OLD/'fixtures'/('RelComp-'+name+'.refontouml')
            count,parsed,raw=run_fixture(path,prior['expected_parsed_fields'])
            assert count==prior['actual_occurrences'] and sha(path)==prior['sha256']
            historical.append({'id':name,'pass':True,'unchanged_sha256':sha(path),'archived_occurrences':count,
                               'profile_frame_match':evaluate_frame(path)['frame_match'],'engine_output':raw.strip()})
    refusals=refusal_checks(fixtures/'finite-one-2.refontouml',fixtures)
    verify_inputs(archive,ecj)
    report={'schema_version':1,'passed':True,'profile':PROFILE,'slice':'P5e-1 lower-bound source-policy discrepancy',
            'oracle_commit':'e3d0aa0949738c2c6f19431d56d75a564eb53a2b','archive_commit':SOURCES['archive']['commit'],
            'frozen_oracles_sha256':ORACLE_SHA256,'runtime_error_stderr_rejected':True,
            'archive_tracked_source_unchanged':True,'compiler_sha256':sha(ecj),'historical_inputs_unchanged':True,
            'software':{'python':platform.python_version(),'java':subprocess.check_output(['java','-version'],stderr=subprocess.STDOUT,text=True).strip()},
            'runtime_jar_order_sha256':{str(x.relative_to(archive)):sha(x) for x in jars},
            'cases':rows,'case_count':len(rows),'cases_passed':len(rows),'historical_replays':historical,
            'refused_inputs':refusals,'engine_only_review_cases':[r['id'] for r in rows if r['disposition']=='ENGINE_ONLY_REVIEW_REQUIRED'],
            'full_candidate_executed':False,'modern_adapter_fidelity_claimed':False,'author_scientific_acceptance_claimed':False,
            'boundary':'Independent declared-frame predicate and unchanged archived runtime compared on synthetic witnesses. A profile non-match is not absence of domain error; whole-model applicability and scientific/author release gates remain open.'}
    (output/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed':True,'cases':len(rows),'historical_replays':len(historical),'refused':len(refusals),
                      'engine_only_review_cases':report['engine_only_review_cases'],'full_candidate_executed':False},indent=2))


if __name__=='__main__':main()
