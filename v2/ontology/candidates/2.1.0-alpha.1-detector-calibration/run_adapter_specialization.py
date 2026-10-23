"""Native JSON -> XMI -> official parser -> actual RelSpec, including refusal guards."""
import copy,json,sys,subprocess,tempfile,hashlib,re
from pathlib import Path
from adapter_specialization import convert
H=Path(__file__).resolve().parent;P=H.parent/'2.1.0-alpha.1-content-event-policy';A=Path(sys.argv[1]);ECJ=Path(sys.argv[2]);MODS=Path(sys.argv[3]);PIN='42b926f6c2859dc87e49a96b8482eae28d02e7d5'
assert subprocess.check_output(['git','-C',str(A),'rev-parse','HEAD'],text=True).strip()==PIN
assert not subprocess.check_output(['git','-C',str(A),'status','--porcelain','--untracked-files=no'],text=True).strip()
base=json.loads((P/'detector-toys/ImpAbs-two-subtypes-upper-two.json').read_text());by={e['id']:e for e in base['elements']};relation=by['association'];relation['description']=None
# Original Other -> Parent association, plus a relation to one explicit subtype.
rr=copy.deepcopy(relation);rr.update(id='special',name={'en':'special'},properties=['special-a','special-b']);base['elements'].append(rr)
for i,oldid in enumerate(relation['properties']):
 end=copy.deepcopy(by[oldid]);end.update(id=rr['properties'][i],name={'en':rr['properties'][i]});end['propertyType']='Other' if i==0 else 'Child0';base['elements'].append(end)
root=next(e for e in base['elements'] if e['type']=='Package');root['contents']=[e['id'] for e in base['elements'] if e['type']!='Package']
def variant(key=None):
 m=copy.deepcopy(base)
 if key:
  d={e['id']:e for e in m['elements']}
  for i in range(2):d[rr['properties'][i]][key]=[relation['properties'][i]]
 return m
spec=[('undeclared',variant(),1),('subsetting',variant('subsettedProperties'),0),('redefinition',variant('redefinedProperties'),0)]
guards=[]
def reject(name,mutate,needle):
 m=variant('subsettedProperties');d={e['id']:e for e in m['elements']};mutate(m,d)
 try:convert(m)
 except (ValueError,AssertionError) as e:
  ok=needle in str(e);guards.append({'name':name,'refused':True,'message':str(e),'expected_marker':needle,'pass':ok});return
 guards.append({'name':name,'refused':False,'pass':False})
reject('missing-target',lambda m,d:d['special-a'].update(subsettedProperties=['Missing']),'Unresolved')
reject('class-as-target',lambda m,d:d['special-a'].update(subsettedProperties=['Parent']),'non-end')
reject('self-reference',lambda m,d:d['special-a'].update(subsettedProperties=['special-a']),'Self')
reject('cycle',lambda m,d:d['association-a'].update(subsettedProperties=['special-a']),'Cyclic')
reject('unknown-cardinality',lambda m,d:d['special-b'].update(cardinality=None),'Unspecified cardinality')
reject('untyped-end',lambda m,d:d['special-b'].update(propertyType=None),'untyped')
reject('event-remains-unsupported',lambda m,d:d['Parent'].update(stereotype='event'),'Class stereotype')
reject('duplicate-target',lambda m,d:d['special-a'].update(subsettedProperties=['association-a','association-a']),'Duplicate specialization')
(H/'adapter-toys').mkdir(exist_ok=True);rows=[];jars=list(A.glob('br.ufes.inf.nemo.common/lib/**/*.jar'))+list(A.glob('br.ufes.inf.nemo.antipattern/lib/*.jar'))
with tempfile.TemporaryDirectory() as td:
 cls=Path(td)/'classes';cls.mkdir();cp=':'.join([str(cls)]+[str(j) for j in jars]);sp=':'.join(str(A/d/'src') for d in ['br.ufes.inf.nemo.ontouml','br.ufes.inf.nemo.common','br.ufes.inf.nemo.antipattern'])
 subprocess.run(['java','-jar',str(ECJ),'-nowarn','-d',str(cls),'-classpath',cp,'-sourcepath',sp,str(P/'RuntimeCatalogue.java'),str(H/'InspectSpecialization.java')],capture_output=True,check=True,timeout=180)
 for name,m,expected in spec:
  js=H/'adapter-toys'/(name+'.json');xm=js.with_suffix('.refontouml');nr=js.with_suffix('.native.json');js.write_text(json.dumps(m,indent=2)+'\n')
  subprocess.run(['node',str(H.parent/'2.1.0-alpha.1-g3-p4a-supply-capacity/check_native.cjs'),str(js),str(MODS),str(nr)],check=True,capture_output=True,timeout=30)
  native=json.loads(nr.read_text());assert native['pass'];before=copy.deepcopy(m);raw,report=convert(m);assert m==before;xm.write_bytes(raw)
  fields=subprocess.check_output(['java','-cp',cp,'InspectSpecialization',str(xm)],text=True).strip().splitlines();d={e['id']:e for e in m['elements']};wanted=[]
  for e in m['elements']:
   if e['type']=='Property':
    lo,hi=e['cardinality'].split('..');hi='-1' if hi=='*' else hi
    wanted.append('|'.join(['END',e['name']['en'],d[e['propertyType']]['name']['en'],lo,hi,','.join(sorted(d[z]['name']['en'] for z in e.get('subsettedProperties',[]))),','.join(sorted(d[z]['name']['en'] for z in e.get('redefinedProperties',[])))]))
  parsed=sorted(fields)==sorted(wanted)
  run=subprocess.run(['java','-cp',cp,'RuntimeCatalogue','RelSpec',str(xm)],capture_output=True,text=True,timeout=45);match=re.search(r'occurrences=(\d+)',run.stdout);actual=int(match[1]) if match else None;clean=run.returncode==0 and match and not re.search(r'exception|could not create|error',run.stdout+run.stderr,re.I)
  rows.append({'name':name,'expected_relspec':expected,'actual_relspec':actual,'native_schema_parser_pass':native['pass'],'official_parser_fields_preserved':parsed,'expected_fields':sorted(wanted),'actual_fields':sorted(fields),'source_unmodified':m==before,'pass':bool(clean) and parsed and actual==expected,'conversion':report,'source_sha256':hashlib.sha256(js.read_bytes()).hexdigest(),'xmi_sha256':hashlib.sha256(raw).hexdigest(),'output':run.stdout+run.stderr})
full=json.loads((H.parent/'2.1.0-alpha.1-four-domain-refinement/ontouml-experimental.json').read_text())
try:convert(full);refusal='UNEXPECTEDLY_ACCEPTED'
except (ValueError,AssertionError) as e:refusal='REFUSED: '+str(e)
report={'scope':'Specialization reference serialization and bounded detector sensitivity only; 14 actual specialized ends are NOT adjudicated or fully validated.','archive_commit':PIN,'cases':rows,'refusal_guards':guards,'case_pass':sum(r['pass'] for r in rows),'case_total':len(rows),'guard_pass':sum(r['pass'] for r in guards),'guard_total':len(guards),'full_candidate_result':refusal,'full_candidate_executed':False}
(H/'adapter-results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['cases','refusal_guards']}));assert all(r['pass'] for r in rows+guards) and refusal.startswith('REFUSED:')
