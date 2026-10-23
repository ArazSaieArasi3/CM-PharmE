"""Resolve a concrete third documentation/code discrepancy with a 2x2 mutation."""
import json,subprocess,tempfile,xml.etree.ElementTree as ET,hashlib,re,sys
from pathlib import Path
from make_fixtures import REF,XMI,XSI # Registers original XMI namespace prefixes before round-trip.
H=Path(__file__).resolve().parent;P=H.parent/'2.1.0-alpha.1-content-event-policy';A=Path(sys.argv[1]);ECJ=Path(sys.argv[2]);PIN='42b926f6c2859dc87e49a96b8482eae28d02e7d5'
assert subprocess.check_output(['git','-C',str(A),'rev-parse','HEAD'],text=True).strip()==PIN
assert not subprocess.check_output(['git','-C',str(A),'status','--porcelain','--untracked-files=no'],text=True).strip()
jars=list(A.glob('br.ufes.inf.nemo.common/lib/**/*.jar'))+list(A.glob('br.ufes.inf.nemo.antipattern/lib/*.jar'));rows=[]
with tempfile.TemporaryDirectory() as td:
 cls=Path(td)/'classes';cls.mkdir();cp=':'.join([str(cls)]+[str(j) for j in jars]);sp=':'.join(str(A/d/'src') for d in ['br.ufes.inf.nemo.ontouml','br.ufes.inf.nemo.common','br.ufes.inf.nemo.antipattern'])
 subprocess.run(['java','-jar',str(ECJ),'-nowarn','-d',str(cls),'-classpath',cp,'-sourcepath',sp,str(P/'RuntimeCatalogue.java'),str(H/'InspectReadOnly.java')],capture_output=True,check=True,timeout=180)
 for rr in [False,True]:
  for mr in [False,True]:
   root=ET.parse(H/'fixtures/RelRig-positive.refontouml').getroot();ends=root.findall('.//ownedEnd');assert len(ends)==2
   ends[0].set('isReadOnly',str(rr).lower());ends[1].set('isReadOnly',str(mr).lower());name=f'RelRig-readonly-{int(rr)}{int(mr)}';f=H/'fixtures'/(name+'.refontouml');ET.indent(root,space='  ');ET.ElementTree(root).write(f,encoding='utf-8',xml_declaration=True)
   inspected=subprocess.check_output(['java','-cp',cp,'InspectReadOnly',str(f)],text=True);expected=sorted([f'mA|Agreement|{str(rr).lower()}',f'mB|ParticipatingPerson|{str(mr).lower()}']);assert sorted(inspected.strip().splitlines())==expected
   p=subprocess.run(['java','-cp',cp,'RuntimeCatalogue','RelRig',str(f)],capture_output=True,text=True,timeout=45);m=re.search(r'occurrences=(\d+)',p.stdout);count=int(m[1]) if m else None;clean=p.returncode==0 and m and not re.search(r'exception|error|could not create',p.stdout+p.stderr,re.I)
   engine_expected=0 if rr else 1;docs_expected=1 if mr else 0
   rows.append({'name':name,'relator_end_readonly':rr,'mediated_end_readonly':mr,'parsed_fields':expected,'fields_preserved':True,'expected_engine':engine_expected,'actual':count,'engine_expectation_pass':bool(clean) and count==engine_expected,'literal_documentation_constraint_expected':docs_expected,'literal_documentation_constraint_matches':count==docs_expected,'fixture_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'output':p.stdout+p.stderr})
r={'scope':'Published RelRig constraint and implementation differ in both tested end and boolean polarity; catalogue prose also less specific. This is a source-adjudication issue, not an automatically diagnosed ontology defect.','documentation':'https://ontouml.readthedocs.io/en/latest/anti-patterns/RelRig/index.html','documentation_rule':'isReadOnly(mediatedEnd)=true','implementation_rule':'skip if isReadOnly(relatorEnd)=true','archive_commit':PIN,'total':4,'engine_expectation_pass':sum(x['engine_expectation_pass'] for x in rows),'documentation_matches':sum(x['literal_documentation_constraint_matches'] for x in rows),'rows':rows}
(H/'readonly-boundary-results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='rows'}));assert all(x['engine_expectation_pass'] for x in rows)
