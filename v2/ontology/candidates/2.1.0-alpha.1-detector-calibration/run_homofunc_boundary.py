"""Targeted threshold mutation prompted by Sales 2014 Table 38, p.144."""
import json,subprocess,tempfile,xml.etree.ElementTree as ET,hashlib,re,sys
from pathlib import Path
from make_fixtures import REF,XMI,XSI
H=Path(__file__).resolve().parent;P=H.parent/'2.1.0-alpha.1-content-event-policy';A=Path(sys.argv[1]);ECJ=Path(sys.argv[2]);PIN='42b926f6c2859dc87e49a96b8482eae28d02e7d5'
assert subprocess.check_output(['git','-C',str(A),'rev-parse','HEAD'],text=True).strip()==PIN
assert not subprocess.check_output(['git','-C',str(A),'status','--porcelain','--untracked-files=no'],text=True).strip()
jars=list(A.glob('br.ufes.inf.nemo.common/lib/**/*.jar'))+list(A.glob('br.ufes.inf.nemo.antipattern/lib/*.jar'));rows=[]
with tempfile.TemporaryDirectory() as td:
 cls=Path(td)/'classes';cls.mkdir();cp=':'.join([str(cls)]+[str(j) for j in jars]);sp=':'.join(str(A/d/'src') for d in ['br.ufes.inf.nemo.ontouml','br.ufes.inf.nemo.common','br.ufes.inf.nemo.antipattern'])
 subprocess.run(['java','-jar',str(ECJ),'-nowarn','-d',str(cls),'-classpath',cp,'-sourcepath',sp,str(P/'RuntimeCatalogue.java'),str(H/'InspectLegacy.java')],capture_output=True,check=True,timeout=180)
 for low in [1,2]:
  root=ET.parse(H/'fixtures/HomoFunc-positive.refontouml').getroot();part=next(e for e in root.findall('.//ownedEnd') if e.attrib['name']=='componentAB');part.find('lowerValue').set('value',str(low));name='HomoFunc-lower-'+str(low);f=H/'fixtures'/(name+'.refontouml');ET.indent(root,space='  ');ET.ElementTree(root).write(f,encoding='utf-8',xml_declaration=True)
  inspected=subprocess.check_output(['java','-cp',cp,'InspectLegacy',str(f)],text=True);expected=f'END|componentA|1|componentAB|PartA|{low}|-1|none|';assert expected in inspected.splitlines()
  run=subprocess.run(['java','-cp',cp,'RuntimeCatalogue','HomoFunc',str(f)],capture_output=True,text=True,timeout=45);m=re.search(r'occurrences=(\d+)',run.stdout);count=int(m[1]) if m else None;clean=run.returncode==0 and m and not re.search(r'exception|could not create|error|does not characterize',run.stdout+run.stderr,re.I)
  rows.append({'name':name,'part_end_lower_bound':low,'part_end_upper_bound':-1,'parsed_field':expected,'fields_preserved':True,'expected_engine':1,'actual':count,'engine_expectation_pass':bool(clean) and count==1,'literal_thesis_expected':0 if low==1 else 1,'literal_thesis_matches':count==(0 if low==1 else 1),'fixture_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'output':run.stdout+run.stderr})
r={'scope':'Thesis Table 38 requires part-end lower bound >=2; pinned engine detects both lower=1 and lower=2 with identical other fields. Source-policy disagreement, not a final finding that the ontology or source is wrong.','source':'https://nemo.inf.ufes.br/wp-content/papercite-data/pdf/ontology_validation_for_managers_2014.pdf','source_locator':'Table 38, printed page 144','archive_commit':PIN,'total':2,'engine_expectation_pass':sum(x['engine_expectation_pass'] for x in rows),'thesis_matches':sum(x['literal_thesis_matches'] for x in rows),'rows':rows}
(H/'homofunc-boundary-results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='rows'}));assert all(x['engine_expectation_pass'] for x in rows)
