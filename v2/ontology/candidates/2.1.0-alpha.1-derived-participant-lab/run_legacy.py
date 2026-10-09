"""Official archived OCL checks and RelSpec on explicitly proposed real fragments."""
import copy,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H.parent/'2.1.0-alpha.1-native-fidelity-audit'))
from adapter_readonly_guard import convert
from native_specialization import audit
from build_lab import RELATIONS,write
A=Path(sys.argv[1]);ECJ=Path(sys.argv[2]);PIN='42b926f6c2859dc87e49a96b8482eae28d02e7d5'
assert subprocess.check_output(['git','-C',str(A),'rev-parse','HEAD'],text=True).strip()==PIN
assert not subprocess.check_output(['git','-C',str(A),'status','--porcelain','--untracked-files=no'],text=True).strip()
cal=H.parent/'2.1.0-alpha.1-detector-calibration';policy=H.parent/'2.1.0-alpha.1-content-event-policy'
rows=[];ocl=[]
with tempfile.TemporaryDirectory() as td:
 cls=Path(td)/'classes';cls.mkdir();jars=list(A.glob('br.ufes.inf.nemo.common/lib/**/*.jar'))+list(A.glob('br.ufes.inf.nemo.antipattern/lib/*.jar'))
 cp=':'.join([str(cls)]+[str(j) for j in jars]);sp=':'.join(str(A/d/'src') for d in ['br.ufes.inf.nemo.ontouml','br.ufes.inf.nemo.common','br.ufes.inf.nemo.antipattern'])
 comp=subprocess.run(['java','-jar',str(ECJ),'-nowarn','-d',str(cls),'-classpath',cp,'-sourcepath',sp,str(H/'InspectMediationRules.java'),str(policy/'RuntimeCatalogue.java'),str(cal/'InspectSpecialization.java')],capture_output=True,text=True,timeout=180)
 (H/'legacy-compile.log').write_text(comp.stdout+comp.stderr);comp.check_returncode()
 for variant in ['A-prior-cards','B-mandatory-mediations','C-derived-projections']:
  for name in RELATIONS:
   file=H/'fragments'/(variant+'-'+name+'.json');base=json.loads(file.read_text());raw,loss=convert(base);xml=Path(td)/'fragment.refontouml';xml.write_bytes(raw)
   run=subprocess.run(['java','-cp',cp,'InspectMediationRules',str(xml)],capture_output=True,text=True,timeout=40)
   observed=[line for line in run.stdout.splitlines() if line.startswith('RULE|')]
   expected=[]
   for e in base['elements']:
    if e['type']=='BinaryRelation' and e['stereotype']=='mediation':
     d={x['id']:x for x in base['elements']};so,ta=[d[x] for x in e['properties']];rn=e['name']['en']
     vals={'source-lower':int(so['cardinality'].split('..')[0])>=1,'target-readonly':ta['isReadOnly'] is True,'target-lower':int(ta['cardinality'].split('..')[0])>=1}
     expected.extend('RULE|'+rn+'|'+k+'|'+str(v).lower() for k,v in vals.items())
   ocl.append({'variant':variant,'relation':name,'expected':sorted(expected),'actual':sorted(observed),'exit':run.returncode,'stderr':run.stderr,'pass':run.returncode==0 and sorted(expected)==sorted(observed),'conversion_losses':loss['known_semantic_losses']})
   if variant!='C-derived-projections':continue
   for mutation,expected_count in [('declared',0),('both-references-removed',1),('one-reference-removed',0),('one-reference-crossed',0)]:
    m=copy.deepcopy(base);d={e['id']:e for e in m['elements']};ends=d['rel-'+name]['properties']
    if mutation=='both-references-removed':
     for end in ends:d[end]['subsettedProperties']=[]
    if mutation=='one-reference-removed':d[ends[1]]['subsettedProperties']=[]
    if mutation=='one-reference-crossed':d[ends[0]]['subsettedProperties']=copy.copy(d[ends[1]]['subsettedProperties'])
    raw,loss=convert(m);xml.write_bytes(raw)
    run=subprocess.run(['java','-cp',cp,'RuntimeCatalogue','RelSpec',str(xml)],capture_output=True,text=True,timeout=45)
    hit=re.search(r'occurrences=(\d+)',run.stdout);actual=int(hit[1]) if hit else None
    clean=run.returncode==0 and not re.search('exception|could not create|error',run.stdout+run.stderr,re.I)
    refs=[d[end]['subsettedProperties'] for end in ends];paired=all(len(ref)==1 for ref in refs) and refs[0][0]!=refs[1][0]
    native=audit(m);selected=[r for r in native['rows'] if r['relation']=='rel-'+name]
    native_ok=paired and len(selected)==2 and all(r['overall']=='PASS' for r in selected)
    expected_native=mutation=='declared'
    rows.append({'relation':name,'mutation':mutation,'expected_engine':expected_count,'actual_engine':actual,
      'paired_native_contract_expected':expected_native,'paired_native_contract_actual':native_ok,
      'pass':clean and actual==expected_count and native_ok==expected_native,'output':run.stdout+run.stderr,
      'known_loss_count':len(loss['known_semantic_losses']),'full_model_claim':False})
result={'scope':'Three proposed structural fragments, nine OCL runs for three selected constraints, and twelve bounded RelSpec mutation runs. Does not certify full model or modern nature.',
 'archive_commit':PIN,'official_ocl':ocl,'ocl_pass':sum(r['pass'] for r in ocl),'ocl_total':len(ocl),
 'relspec':rows,'relspec_pass':sum(r['pass'] for r in rows),'relspec_total':len(rows)}
write('legacy-results.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ['official_ocl','relspec']}))
assert all(r['pass'] for r in rows+ocl)
