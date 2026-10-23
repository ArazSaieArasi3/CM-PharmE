"""Expose the old adapter's concrete null default and test the stricter entry point."""
import copy, hashlib, json, subprocess, sys, tempfile, xml.etree.ElementTree as ET
from pathlib import Path
from adapter_readonly_guard import convert, prior_convert
H=Path(__file__).resolve().parent
P=H.parent/'2.1.0-alpha.1-detector-calibration/adapter-toys/subsetting.json'
original=json.loads(P.read_text());base=copy.deepcopy(original)
# New synthetic controls specify every boolean deliberately. The archived fixture
# contains FOUR null booleans; it and all real candidate values remain unchanged.
for e in base['elements']:
    if e['type']=='Property':e['isReadOnly']=False
probe=copy.deepcopy(base);next(e for e in probe['elements'] if e['id']=='special-a')['isReadOnly']=None
old,report=prior_convert(probe);root=ET.fromstring(old)
prop=next(e for e in root.iter() if e.attrib.get('{http://www.omg.org/XMI}id')=='_cmpe_special-a')
counterexample={'input_end':'special-a','input_readonly':None,'previous_adapter_accepted':True,
    'old_output_readonly_attribute':prop.get('isReadOnly'),'consequence':'Absent legacy Boolean attribute uses the legacy false default; source unknown is not represented.',
    'old_xmi_sha256':hashlib.sha256(old).hexdigest()}
cases=[]
outputs={'old-unknown-null':old}
try:convert(original);refused=False;message=None
except ValueError as e:refused=True;message=str(e)
cases.append({'name':'unchanged-prior-fixture-has-four-unknowns','expected_accepted':False,'accepted':not refused,'error':message,'pass':refused})
for name,val,expected in [('known-false',False,True),('known-true',True,True),('unknown-null',None,False)]:
    m=copy.deepcopy(base);next(e for e in m['elements'] if e['id']=='special-a')['isReadOnly']=val
    try:
        raw,report=convert(m);accepted=True;error=None
        outputs[name]=raw
        p=next(e for e in ET.fromstring(raw).iter() if e.attrib.get('{http://www.omg.org/XMI}id')=='_cmpe_special-a')
        output_value=p.get('isReadOnly','false')=='true';preserved=output_value is val
    except ValueError as e:accepted=False;error=str(e);preserved=None
    cases.append({'name':name,'input':val,'expected_accepted':expected,'accepted':accepted,'error':error,
                  'known_boolean_preserved':preserved,'pass':accepted==expected and (not accepted or preserved)})
A=Path(sys.argv[1]);ECJ=Path(sys.argv[2]);PIN='42b926f6c2859dc87e49a96b8482eae28d02e7d5'
assert subprocess.check_output(['git','-C',str(A),'rev-parse','HEAD'],text=True).strip()==PIN
assert not subprocess.check_output(['git','-C',str(A),'status','--porcelain','--untracked-files=no'],text=True).strip()
parser_rows=[]
with tempfile.TemporaryDirectory() as td:
    work=Path(td);classes=work/'classes';classes.mkdir()
    jars=list(A.glob('br.ufes.inf.nemo.common/lib/**/*.jar'))+list(A.glob('br.ufes.inf.nemo.antipattern/lib/*.jar'))
    cp=':'.join([str(classes)]+[str(j) for j in jars]);sp=':'.join(str(A/d/'src') for d in ['br.ufes.inf.nemo.ontouml','br.ufes.inf.nemo.common'])
    subprocess.run(['java','-jar',str(ECJ),'-nowarn','-d',str(classes),'-classpath',cp,'-sourcepath',sp,str(H.parent/'2.1.0-alpha.1-detector-calibration/InspectReadOnly.java')],capture_output=True,check=True,timeout=90)
    for name,raw in outputs.items():
        file=work/(name+'.refontouml');file.write_bytes(raw)
        result=subprocess.run(['java','-cp',cp,'InspectReadOnly',str(file)],capture_output=True,text=True,check=True,timeout=30)
        fields=[line for line in result.stdout.splitlines() if line.startswith('special-a|')]
        assert len(fields)==1
        expected=name=='known-true';actual=fields[0].split('|')[-1]=='true'
        parser_rows.append({'name':name,'official_parser_line':fields[0],'expected_boolean':expected,'actual_boolean':actual,'pass':actual==expected,'stderr':result.stderr})
result={'scope':'Prior four-null fixture, one isolated null counterexample, and two explicitly known-Boolean controls. Structural probe only; no full-model claim.',
    'initial_probe':'guard-initial-probe.json records two expected-accept failures because three other end flags were also null; fixed the synthetic control setup, not the rejection rule or original fixture.',
    'source_fixture_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'counterexample':counterexample,
    'cases':cases,'pass':sum(c['pass'] for c in cases),'total':len(cases),'official_library_or_archive_changed':False,
    'archive_commit':PIN,'official_parser_cases':parser_rows,'official_parser_pass':sum(r['pass'] for r in parser_rows),'official_parser_total':len(parser_rows)}
(H/'readonly-guard-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['cases','counterexample']}))
assert all(c['pass'] for c in cases+parser_rows)
