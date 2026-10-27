#!/usr/bin/env python3
"""Independent RelRig frame/profile and unchanged archived-runtime comparison."""
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
ORACLE_SHA256 = "f3dc9d725eb7846038405d12ee763569f7d05e9ca604b7142fe5baabf3cc9748"
spec = importlib.util.spec_from_file_location("relrig_witness_factory", OLD / "make_fixtures.py")
factory = importlib.util.module_from_spec(spec); spec.loader.exec_module(factory)


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def command(args, timeout=60):
    result = subprocess.run([str(x) for x in args],capture_output=True,text=True,timeout=timeout)
    if result.returncode: raise RuntimeError(result.stdout[-1000:]+result.stderr[-3000:])
    if re.search(r'exception|error|failed', result.stderr, re.I):
        raise RuntimeError("Runtime stderr requires investigation: " + result.stderr[-3000:])
    return result.stdout


def model_for(case):
    f=factory;st=case['mediated_stereotype']
    model=f.model([f.cls('Person'),f.cls('ParticipatingPerson',st),f.cls('Agreement','Relator')],
                  [f.rel('m','Agreement','ParticipatingPerson','Mediation',(1,1),(1,1))],
                  [] if st=='Kind' else [f.gen('ParticipatingPerson','Person')])
    for i,e in enumerate(model['relations'][0]['ends']):e['read_only']=case['relator_readonly'] if i==0 else case['mediated_readonly']
    mutation=case['mutation'];ends=model['relations'][0]['ends']
    if mutation=='reordered':ends.reverse()
    elif mutation=='relator-optional':ends[0]['lower']=0
    elif mutation=='mediated-optional':ends[1]['lower']=0
    elif mutation=='unlimited':ends[0]['upper']=-1;ends[1]['upper']=-1
    return model


def serialize_explicit(model,name):
    root=ET.fromstring(factory.serialize(model,name));by_id={e.get(XMI+'id'):e for e in root.iter()}
    for rel in model['relations']:
        for end in rel['ends']:by_id[end['name']].set('isReadOnly',str(end['read_only']).lower())
    ET.indent(root,space='  ')
    return ET.tostring(root,encoding='utf-8',xml_declaration=True)


def expected_readonly(model):
    return sorted('|'.join([e['name'],e['type'],str(e.get('read_only',False)).lower()]) for r in model['relations'] for e in r['ends'])


def expected_roles(model):
    e={x['name']:x for x in model['relations'][0]['ends']}
    return ['ROLES|m|mA|Agreement|'+str(e['mA'].get('read_only',False)).lower()+'|mB|ParticipatingPerson|'+str(e['mB'].get('read_only',False)).lower()]


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
    def r_end(root):return root.find("packagedElement[@name='m']/ownedEnd[@name='mA']")
    def m_end(root):return root.find("packagedElement[@name='m']/ownedEnd[@name='mB']")
    operations={
        'missing_relator_readonly':lambda r:r_end(r).attrib.pop('isReadOnly'),
        'missing_mediated_readonly':lambda r:m_end(r).attrib.pop('isReadOnly'),
        'invalid_readonly':lambda r:m_end(r).set('isReadOnly','null'),
        'missing_lower':lambda r:r_end(r).remove(r_end(r).find('lowerValue')),
        'missing_upper':lambda r:r_end(r).remove(r_end(r).find('upperValue')),
        'invalid_interval':lambda r:r_end(r).find('upperValue').set('value','0'),
        'untyped_end':lambda r:r_end(r).attrib.pop('type'),
        'duplicate_id':lambda r:r.append(copy.deepcopy(r.find("packagedElement[@name='Person']"))),
        'unsupported_subsetting':lambda r:m_end(r).set('subsettedProperty','mA'),
        'ambiguous_relator':lambda r:r.find("packagedElement[@name='ParticipatingPerson']").set(XSI+'type','RefOntoUML:Relator'),
        'unsupported_ancestry':lambda r:r.find("packagedElement[@name='ParticipatingPerson']/generalization").set('general','Agreement'),
        'unsupported_stereotype':lambda r:r.find("packagedElement[@name='ParticipatingPerson']").set(XSI+'type','RefOntoUML:Event'),
    }
    assert set(operations)==set(ORACLES['legacy_refused_inputs'])
    return {name:trial(name,fn) for name,fn in operations.items()}


def verify_inputs(archive,ecj):
    assert sha(HERE/'fixed-oracles.json')==ORACLE_SHA256,'Frozen oracle bytes changed'
    assert command(['git','-C',archive,'rev-parse','HEAD']).strip()==SOURCES['archive']['commit']
    assert not command(['git','-C',archive,'status','--porcelain','--untracked-files=no']).strip()
    assert sha(ecj)==SOURCES['compiler']['sha256']
    for path,digest in SOURCES['archive']['files'].items():assert sha(archive/path)==digest,path
    for path,digest in SOURCES['historical_inputs_sha256'].items():assert sha(ROOT/path)==digest,path


def native_checks(output,cp):
    from native_admission import convert
    def canonical(m):return json.dumps(m,sort_keys=True,separators=(',',':'))
    source=OLD/'adapter-toys/subsetting.json';original=json.loads(source.read_text());base=copy.deepcopy(original)
    for e in base['elements']:
        if e['type']=='Property':e['isReadOnly']=False
    candidate=HERE.parent/'2.1.0-alpha.1-p3-facility-operation/ontouml.json'
    target=json.loads(candidate.read_text());target_before=canonical(target)
    cases=[]
    for oracle in ORACLES['native_admission_oracles']:
        name=oracle['id'];model=copy.deepcopy(target if name=='unchanged-full-candidate' else base)
        prop=next((e for e in model['elements'] if e['id']=='special-a'),None)
        if name=='known-true':prop['isReadOnly']=True
        elif name=='unknown-null':prop['isReadOnly']=None
        elif name=='unknown-missing':del prop['isReadOnly']
        elif name=='invalid-string':prop['isReadOnly']='false'
        elif name=='invalid-integer':prop['isReadOnly']=0
        before=canonical(model);flags=None;message=None
        try:
            raw,adapter_report=convert(model);accepted=True
            path=output/(name+'.refontouml');path.write_bytes(raw)
            flags=sorted(command(['java','-cp',cp,'InspectReadOnly',path],45).strip().splitlines())
            properties=[e for e in model['elements'] if e['type']=='Property']
            assert len(flags)==len(properties)
            assert all(line.rsplit('|',1)[1]==('true' if name=='known-true' and line.startswith('special-a|') else 'false') for line in flags)
            assert sum(line.endswith('|true') for line in flags)==int(name=='known-true')
            assert adapter_report['full_fidelity'] is False
        except ValueError as err:
            accepted=False;message=str(err)
            assert message.startswith('invalid_native_readonly:' if name.startswith('invalid-') else 'unknown_native_readonly:')
        assert accepted==oracle['expected_accepted'],(name,accepted)
        assert canonical(model)==before,'Native input mutation'
        cases.append(dict(id=name,accepted=accepted,expected_accepted=oracle['expected_accepted'],pass_result=True,
                          source_unchanged=True,parsed_readonly=flags,rejection=message))
    props=[e for e in target['elements'] if e['type']=='Property'];by={e['id']:e for e in target['elements']}
    unknown=[e['id'] for e in props if e.get('isReadOnly') is None]
    mediation_unknown=[]
    for relation in target['elements']:
        if relation['type']=='BinaryRelation' and relation.get('stereotype')=='mediation':
            ends=[p for p in relation['properties'] if by[p].get('isReadOnly') is None]
            if ends:mediation_unknown.append(dict(relation=relation['id'],unknown_ends=ends))
    assert canonical(target)==target_before and sha(candidate)==SOURCES['historical_inputs_sha256'][str(candidate.relative_to(ROOT))]
    return dict(cases=cases,source_sha256=sha(candidate),source_elements=len(target['elements']),source_properties=len(props),
                unknown_readonly_properties=len(unknown),unknown_readonly_ids=unknown,mediations_with_unknown_readonly=mediation_unknown,
                source_unchanged=True,full_candidate_conversion_executed=False,full_candidate_detector_executed=False,
                counts_are_input_inventories_not_relrig_findings=True)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--archive',required=True,type=Path);ap.add_argument('--ecj',required=True,type=Path)
    ap.add_argument('--output-dir',default='build/relrig-policy');a=ap.parse_args()
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
        compile_args=['java','-jar',ecj,'-nowarn','-d',classes,'-classpath',cp,'-sourcepath',sourcepath,HERE/'RelRigRuntime.java',OLD/'InspectLegacy.java',OLD/'InspectReadOnly.java',HERE/'InspectEndpointRoles.java']
        compiled=command(compile_args,180);(output/'compile.log').write_text(compiled)
        def run_fixture(path, expected_fields, expected_flags, expected_role_fields):
            inspected=command(['java','-cp',cp,'InspectLegacy',path],45)
            actual=sorted(line for line in inspected.splitlines() if line.startswith(('CLASS|','REL|','END|','GEN|','SET|')))
            assert actual==expected_fields,('Parser field mismatch',str(path),actual,expected_fields)
            flags=sorted(command(['java','-cp',cp,'InspectReadOnly',path],45).strip().splitlines())
            assert flags==expected_flags,('ReadOnly parser mismatch',str(path),flags,expected_flags)
            roles=sorted(command(['java','-cp',cp,'InspectEndpointRoles',path],45).strip().splitlines())
            assert roles==expected_role_fields,('Role parser mismatch',roles,expected_role_fields)
            raw=command(['java','-cp',cp,'RelRigRuntime',path],45)
            match=re.search(r'CMPE_RELRIG_COUNT=(\d+)',raw)
            assert match and not re.search(r'exception|error|failed',raw,re.I),raw
            return int(match[1]),actual,flags,roles,raw
        for case in ORACLES['cases']:
            model=model_for(case);path=fixtures/(case['id']+'.refontouml')
            path.write_bytes(serialize_explicit(model,case['id']))
            count,parsed,flags,roles,raw=run_fixture(path,expected_parsed_fields(model),expected_readonly(model),expected_roles(model))
            policy=evaluate_frame(path)
            assert count==case['expected_archived_occurrences'],(case['id'],count)
            for k in ['published_frame_match','rigid_dependency_review_required','mediation_baseline_review_required']:
                assert policy[k]==case['expected_'+k],(case['id'],k,policy)
            comparison=('BOTH_MATCH' if count and policy['published_frame_match'] else
                        'ENGINE_ONLY_REVIEW_REQUIRED' if count else
                        'PUBLISHED_ONLY_REVIEW_REQUIRED' if policy['published_frame_match'] else
                        'NEITHER_SIGNATURE_NOT_CLEAN_CERTIFICATE')
            rows.append({'id':case['id'],'archived_occurrences':count,'published_frame_match':policy['published_frame_match'],
                         'profile':policy,'comparison':comparison,'pass':True,'fixture_sha256':sha(path),
                         'parsed_fields':parsed,'parsed_readonly':flags,'parsed_roles':roles,'engine_output':raw.strip()})
        boundary=json.loads((OLD/'readonly-boundary-results.json').read_text())
        for name in ['positive','negative','readonly-00','readonly-01','readonly-10','readonly-11']:
            path=OLD/'fixtures'/('RelRig-'+name+'.refontouml')
            basic=next(r for r in old['rows'] if r['family']=='RelRig' and r['name']==('negative' if name=='negative' else 'positive'))
            model=copy.deepcopy(next(c['model'] for c in factory.CASES if c['family']=='RelRig' and c['name']==('negative' if name=='negative' else 'positive')))
            prior=next((r for r in boundary['rows'] if r['name']=='RelRig-'+name),None)
            if prior:
                for e,v in zip(model['relations'][0]['ends'],[prior['relator_end_readonly'],prior['mediated_end_readonly']]):e['read_only']=v
            expected=prior['actual'] if prior else basic['actual_occurrences']
            digest=prior['fixture_sha256'] if prior else basic['sha256']
            count,parsed,flags,roles,raw=run_fixture(path,basic['expected_parsed_fields'],expected_readonly(model),expected_roles(model))
            assert count==expected and sha(path)==digest
            if prior:
                policy=evaluate_frame(path);assert policy['published_frame_match']==prior['literal_documentation_constraint_expected']
            else:
                try:evaluate_frame(path)
                except ValueError as err:assert str(err)=='missing_relator_readonly'
                else:raise AssertionError('Historical implicit defaults admitted to explicit profile')
                policy=None
            historical.append(dict(id=name,pass_result=True,unchanged_sha256=sha(path),archived_occurrences=count,
                                   parsed_fields=parsed,parsed_readonly=flags,parsed_roles=roles,
                                   readonly_source_attributes_explicit=prior is not None,
                                   parser_false_defaults_not_native_facts=prior is None,profile=policy,engine_output=raw.strip()))
        native=native_checks(output,cp)
    refusals=refusal_checks(fixtures/'rigid-01.refontouml',fixtures)
    verify_inputs(archive,ecj)
    report={'schema_version':1,'passed':True,'profile':PROFILE,'slice':'P5e-3 explicit endpoint review',
            'oracle_commit':'a7c48d75d76972190c9c76d2ba61dcbe64710aaf','archive_commit':SOURCES['archive']['commit'],
            'frozen_oracles_sha256':ORACLE_SHA256,'runtime_error_stderr_rejected':True,
            'archive_tracked_source_unchanged':True,'compiler_sha256':sha(ecj),'historical_inputs_unchanged':True,
            'software':{'python':platform.python_version(),'java':subprocess.check_output(['java','-version'],stderr=subprocess.STDOUT,text=True).strip()},
            'runtime_jar_order_sha256':{str(x.relative_to(archive)):sha(x) for x in jars},
            'cases':rows,'case_count':len(rows),'cases_passed':len(rows),'historical_replays':historical,
            'refused_inputs':refusals,'engine_only_review_cases':[r['id'] for r in rows if r['comparison']=='ENGINE_ONLY_REVIEW_REQUIRED'],
            'published_only_review_cases':[r['id'] for r in rows if r['comparison']=='PUBLISHED_ONLY_REVIEW_REQUIRED'],
            'native_admission':native,'semantic_endpoint_interpretation_not_automatically_resolved':True,
            'full_candidate_executed':False,'modern_adapter_fidelity_claimed':False,'author_scientific_acceptance_claimed':False,
            'boundary':'Independent declared-frame predicate and unchanged archived runtime compared on synthetic witnesses. A profile non-match is not absence of domain error; whole-model applicability and scientific/author release gates remain open.'}
    (output/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed':True,'cases':len(rows),'historical_replays':len(historical),'refused':len(refusals),
                      'published_only_review_cases':report['published_only_review_cases'],'native_admission_cases':len(native['cases']),'full_candidate_executed':False},indent=2))


if __name__=='__main__':main()
