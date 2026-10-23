#!/usr/bin/env python3
"""End-to-end narrow adapter test with the archived OLED parser and BinOver."""
import copy
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from to_refontouml import REF, XMI, XSI, convert

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
ARCHIVE=Path(sys.argv[1])
ECJ=Path(sys.argv[2])
MODULES=Path(sys.argv[3])
COMMIT='42b926f6c2859dc87e49a96b8482eae28d02e7d5'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(args):
    p=subprocess.run([str(a) for a in args],capture_output=True,text=True)
    if p.returncode:
        raise RuntimeError(f"{args[0]} exit {p.returncode}: {p.stderr[:800]} ... {p.stderr[-500:]} {p.stdout[-500:]}")
    return p.stdout.strip()


assert run(['git','-C',ARCHIVE,'rev-parse','HEAD']) == COMMIT
assert ECJ.exists() and MODULES.exists()
run(['python', HERE/'make_toys.py'])
run(['python', HERE/'audit_full.py'])

toy_results={}
for name in ('positive','negative','route'):
    source=HERE/f'toy-{name}.json'
    out=HERE/f'toy-{name}.refontouml'
    run(['node',BASE/'g3-p4a-supply-capacity/check_native.cjs',source,MODULES,
         HERE/f'toy-{name}-native.json'])
    official=json.loads((HERE/f'toy-{name}-native.json').read_text())
    assert official['pass']
    run(['python',HERE/'to_refontouml.py',source,out,HERE/f'toy-{name}-conversion.json'])
    converted=json.loads((HERE/f'toy-{name}-conversion.json').read_text())
    native=json.loads(source.read_text())
    elements={x['id']:x for x in native['elements']}
    xml=ET.parse(out).getroot()
    converted_classes=[]
    converted_rels=[]
    for item in xml.findall('packagedElement'):
        oldid=item.attrib[f'{{{XMI}}}id'].removeprefix('_cmpe_')
        if oldid in elements and elements[oldid]['type']=='Class':
            converted_classes.append(oldid)
        elif oldid in elements and elements[oldid]['type']=='BinaryRelation':
            converted_rels.append(oldid)
            original=elements[oldid]
            ends=item.findall('ownedEnd')
            assert len(ends)==2
            assert item.attrib['memberEnd'].split()==[f'_cmpe_{x}' for x in original['properties']]
            for end,origid in zip(ends,original['properties']):
                a=elements[origid]
                assert end.attrib['type']==f'_cmpe_{a["propertyType"]}'
                lo=a['cardinality'].split('..')[0]
                hi=a['cardinality'].split('..')[-1].replace('*','-1')
                assert end.find('lowerValue').attrib['value']==lo
                assert end.find('upperValue').attrib['value']==hi
    assert len(converted_classes)==converted['classes']
    assert len(converted_rels)==converted['binary_relations']==1
    toy_results[name]={"json_sha256":sha(source),"xmi_sha256":sha(out),
                       "native_schema_and_parser":official['pass'],
                       "xml_subset_structural_roundtrip":True,
                       "known_semantic_losses":converted['known_semantic_losses']}

model=json.loads((HERE/'toy-route.json').read_text())
def reject(mutator, expected):
    trial=copy.deepcopy(model)
    mutator(trial)
    try:convert(trial)
    except ValueError as exc:
        assert expected in str(exc), str(exc)
        return str(exc)
    raise AssertionError(f'Invalid model unexpectedly converted: {expected}')

guards={
    'missing_cardinality':reject(lambda m: next(x for x in m['elements'] if x['id']=='end-toy-source').update(cardinality=None),'Unspecified cardinality'),
    'untyped_end':reject(lambda m: next(x for x in m['elements'] if x['id']=='end-toy-target').update(propertyType=None),'untyped or unresolved'),
    'unsupported_event':reject(lambda m: next(x for x in m['elements'] if x['id']=='SupplyCapacity').update(stereotype='event'),'Class stereotype'),
    'unsupported_subsetting':reject(lambda m: next(x for x in m['elements'] if x['id']=='end-toy-source').update(subsettedProperties=['other']),'subsetting/redefinition')
}

java_dirs=['br.ufes.inf.nemo.ontouml','br.ufes.inf.nemo.common','br.ufes.inf.nemo.antipattern']
jars=list(ARCHIVE.glob('br.ufes.inf.nemo.common/lib/**/*.jar'))+list(ARCHIVE.glob('br.ufes.inf.nemo.antipattern/lib/*.jar'))
assert len(jars)>=70
with tempfile.TemporaryDirectory() as tmp:
    cls=Path(tmp)/'classes';cls.mkdir()
    cp=':'.join([str(cls)]+[str(p) for p in jars])
    sourcepath=':'.join(str(ARCHIVE/p/'src') for p in java_dirs)
    run(['java','-jar',ECJ,'-nowarn','-d',cls,'-classpath',cp,
         '-sourcepath',sourcepath,HERE/'ProbeParser.java',HERE/'ProbePatterns.java'])
    calibration=run(['java','-cp',cp,'ProbeParser',ARCHIVE/'br.ufes.inf.nemo.antipattern/models/The Internship Model.refontouml'])
    assert 'classes=26 associations=18' in calibration
    for name,expected in [('positive',1),('negative',0),('route',0)]:
        output=run(['java','-cp',cp,'ProbePatterns',HERE/f'toy-{name}.refontouml'])
        count=int(re.search(r'BinOver=(\d+)',output).group(1))
        assert count==expected,output
        if name=='route':
            assert 'characterizations=1' in output
            assert 'kind=CharacterizationImpl' in output
            assert 'end=end-toy-source type=Organization card=0..1' in output
            assert 'end=end-toy-target type=Supply Capacity card=0..-1' in output
        toy_results[name]['archived_oled_output']=output.splitlines()
        toy_results[name]['expected_bin_over']=expected

feasibility=json.loads((HERE/'full-feasibility.json').read_text())
assert feasibility['full_adapter_result'].startswith('REFUSED:')
report={
    'scope':'Narrow JSON→legacy-XMI structural adapter, actual OLED parser and BinOver detector. NOT a full 20-pattern or full ontology run.',
    'archived_oled_commit':COMMIT,'archived_sample_parser_calibration':calibration,
    'ecj_version':'3.39.0','ecj_sha256':sha(ECJ),
    'java_runtime':'OpenJDK 17; Java source compiled with Eclipse ECJ 3.39.0',
    'runtime_jar_order':[str(j.relative_to(ARCHIVE)) for j in jars],
    'model_sha256':feasibility['model_sha256'],
    'toy_cases':toy_results,'strict_rejection_guards':guards,
    'full_model_refused':True,
    'full_model_blockers':{k:feasibility[k]['count'] for k in
        ['unsupported_class_stereotypes','untyped_relation_ends','unspecified_cardinality_ends',
         'subsetted_or_redefined_ends','modern_nature_restrictions']},
    'official_20_detector_executed_on_full_candidate':False,
    'next_step':'Resolve or explicitly scope every fidelity blocker; verify more detector families on toy models; only then use complete engine on full candidate.'
}
(HERE/'probe-results.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'toy_bin_over':{k:v['expected_bin_over'] for k,v in toy_results.items()},
                  'full_refused':report['full_model_refused'],
                  'guard_count':len(guards),'official_full_run':False}))
