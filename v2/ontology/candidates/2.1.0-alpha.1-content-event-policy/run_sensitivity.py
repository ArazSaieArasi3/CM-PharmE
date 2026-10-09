"""Positive/negative threshold probes for three families; not full 20-family validation."""
import json,copy,sys,subprocess,tempfile,re,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;B=H.parent/'2.1.0-alpha.1-g3-p5b-adapter-probe'
sys.path.insert(0,str(B));from to_refontouml import convert
A=Path(sys.argv[1]);ECJ=Path(sys.argv[2]);MODULES=Path(sys.argv[3])
assert subprocess.check_output(['git','-C',str(A),'rev-parse','HEAD'],text=True).strip()=='42b926f6c2859dc87e49a96b8482eae28d02e7d5'
(H/'detector-toys').mkdir(exist_ok=True)
base=json.loads((B/'toy-positive.json').read_text());templates={e['type']:e for e in base['elements']};original=json.loads((H.parent/'2.1.0-alpha.1-four-domain-refinement/ontouml-experimental.json').read_text());gt=next(e for e in original['elements'] if e['type']=='Generalization')
def common(t,i):
 e=copy.deepcopy(t);e.update(id=i,name={'en':i},description=None,editorialNotes=[]);return e
def cl(i,st='kind'):
 e=common(templates['Class'],i);e['stereotype']=st;e['restrictedTo']=['relator'] if st=='relator' else ['functional-complex'];return e
def rel(i,a,b,ca='0..1',cb='0..*',st=None):
 r=common(templates['BinaryRelation'],i);r['stereotype']=st;r['properties']=[i+'-a',i+'-b'];ends=[]
 for k,t,card in [('a',a,ca),('b',b,cb)]:
  e=common(templates['Property'],i+'-'+k);e.update(propertyType=t,cardinality=card);ends.append(e)
 return [r]+ends
def gen(i,sub,sup):
 e=common(gt,i);e.update(specific=sub,general=sup);return e
def model(name,elements):
 m=copy.deepcopy(base);m['name']={'en':name};m['description']=None;p=common(templates['Package'],m['root']);p['contents']=[e['id'] for e in elements];m['elements']=[p]+elements;return m
spec=[]
for name,children,upper,expected in [('two-subtypes-upper-two',2,'0..2',1),('two-subtypes-upper-one',2,'0..1',0),('one-subtype-unbounded',1,'0..*',0)]:
 els=[cl('Parent'),cl('Other')]+rel('association','Other','Parent','0..1',upper)
 for i in range(children):els += [cl('Child'+str(i),'subkind'),gen('g'+str(i),'Child'+str(i),'Parent')]
 spec.append(('ImpAbs',name,model(name,els),expected))
for name,meds,upper,expected in [('two-mediations-many-relators',2,'0..*',1),('two-mediations-one-relator',2,'0..1',0),('one-mediation-many-relators',1,'0..*',0)]:
 els=[cl('Agreement','relator'),cl('ActorA'),cl('ActorB')]
 for i in range(meds):els+=rel('mediation'+str(i),'Agreement','Actor'+('A' if i==0 else 'B'),upper,'1','mediation')
 spec.append(('RepRel',name,model(name,els),expected))
for name,expect in [('positive',1),('negative',0)]:spec.append(('BinOver','prior-'+name,json.loads((B/('toy-'+name+'.json')).read_text()),expect))
jars=list(A.glob('br.ufes.inf.nemo.common/lib/**/*.jar'))+list(A.glob('br.ufes.inf.nemo.antipattern/lib/*.jar'));rows=[]
with tempfile.TemporaryDirectory() as td:
 cls=Path(td)/'classes';cls.mkdir();cp=':'.join([str(cls)]+[str(j) for j in jars]);sp=':'.join(str(A/d/'src') for d in ['br.ufes.inf.nemo.ontouml','br.ufes.inf.nemo.common','br.ufes.inf.nemo.antipattern'])
 subprocess.run(['java','-jar',str(ECJ),'-nowarn','-d',str(cls),'-classpath',cp,'-sourcepath',sp,str(H/'RuntimeCatalogue.java')],check=True,capture_output=True,timeout=180)
 for detector,name,m,expected in spec:
  prefix=H/'detector-toys'/(detector+'-'+name);jp=prefix.with_suffix('.json');xp=prefix.with_suffix('.refontouml');np=prefix.with_suffix('.native.json');jp.write_text(json.dumps(m,indent=2)+'\n')
  subprocess.run(['node',str(H.parent/'2.1.0-alpha.1-g3-p4a-supply-capacity/check_native.cjs'),str(jp),str(MODULES),str(np)],check=True,capture_output=True,timeout=30)
  native=json.loads(np.read_text());assert native['pass']
  xml,conversion=convert(m);xp.write_bytes(xml)
  p=subprocess.run(['java','-cp',cp,'RuntimeCatalogue',detector,str(xp)],capture_output=True,text=True,timeout=60)
  match=re.search(r'occurrences=(\d+)',p.stdout);actual=int(match[1]) if match else None
  hidden=bool(re.search(r'exception|could not create|error|failed',p.stdout+p.stderr,re.I))
  row={'detector':detector,'name':name,'expected':expected,'actual':actual,'pass':p.returncode==0 and not hidden and actual==expected,'native_schema_parser_pass':native['pass'],'conversion':conversion,'source_sha256':hashlib.sha256(jp.read_bytes()).hexdigest(),'xmi_sha256':hashlib.sha256(xml).hexdigest(),'stdout':p.stdout,'stderr':p.stderr};rows.append(row);print(json.dumps({k:v for k,v in row.items() if k not in ['conversion','stdout','stderr']}),flush=True)
report={'scope':'Controlled bounded structural sensitivity probes; modern nature remains outside legacy fidelity.','archive_commit':'42b926f6c2859dc87e49a96b8482eae28d02e7d5','total':len(rows),'passed':sum(x['pass'] for x in rows),'families_with_positive_and_negative_probes':['BinOver','ImpAbs','RepRel'],'full_catalogue_sensitivity_validated':False,'full_candidate_executed':False,'rows':rows}
(H/'sensitivity-results.json').write_text(json.dumps(report,indent=2)+'\n');assert all(x['pass'] for x in rows)
