"""Three isolated alternatives for existing participant shortcuts; no baseline edits."""
import copy,hashlib,json,sys,subprocess,tempfile
from pathlib import Path
H=Path(__file__).resolve().parent
P=H.parent/'2.1.0-alpha.1-four-domain-refinement'
A=H.parent/'2.1.0-alpha.1-native-fidelity-audit'
sys.path.insert(0,str(A))
from native_specialization import audit
from run_native_audit import structural_fragment
RELATIONS={
 'contextClassificationEntry':('classificationEntry','ContextualMedicineClassificationAssignment','AppliedClassificationEntryRole'),
 'contextClassificationProduct':('classificationEntity','ContextualMedicineClassificationAssignment','ClassifiedMedicinalProductRole'),
 'evidenceRecord':('evidenceItem','EvidenceSupport','EvidenceSourceRecordRole')}
VARIANTS={
 'A-prior-cards':{'inverse':'0..*','targets':['1','1','0..1'],'derived':False},
 'B-mandatory-mediations':{'inverse':'1..*','targets':['1','1','1'],'derived':False},
 'C-derived-projections':{'inverse':'0..*','targets':['1','0..1','0..1'],'derived':True}}

def write(name,obj):
 p=H/name;p.parent.mkdir(exist_ok=True,parents=True);p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')

def variant(base,key):
 m=copy.deepcopy(base);d={e['id']:e for e in m['elements']};changes=[]
 def setfield(e,k,v,why):
  old=e.get(k)
  if old!=v:changes.append({'id':e['id'],'field':k,'before':old,'after':v,'basis':why});e[k]=v
 config=VARIANTS[key]
 for i,(name,(parent,source,target)) in enumerate(RELATIONS.items()):
  r=d['rel-'+name];e1,e2=[d[x] for x in r['properties']]
  setfield(e1,'cardinality',config['inverse'],'EXPERIMENTAL alternative; not author accepted')
  setfield(e2,'cardinality',config['targets'][i],'EXPERIMENTAL alternative; not author accepted')
  setfield(e1,'isReadOnly',False,'Inverse participant population may change; proposal only')
  setfield(e2,'isReadOnly',True,'Frozen participant identity hypothesis; proposal tested on bounded traces')
  setfield(d['end-'+parent+'-target'],'isReadOnly',True,'Primary mediation profile requires immutable mediated end; proposal changes prior false')
  if config['derived']:
   setfield(r,'stereotype',None,'Derived typed association, classification unaccepted; not a primitive mediation')
   setfield(r,'isDerived',True,'Explicit source/target-filtered projection of existing primitive mediation')
 return m,changes

def source_profile(m):
 d={e['id']:e for e in m['elements']};rows=[]
 # Narrow, explicit checks from pinned Ecore. Not complete UML/OntoUML validation.
 for name in RELATIONS:
  r=d['rel-'+name]
  if r['stereotype']!='mediation':rows.append({'relation':name,'status':'NOT_APPLICABLE_TO_DERIVED_ASSOCIATION'});continue
  so,ta=[d[x] for x in r['properties']]
  rules={'DependencyRelationshipConstraint1':int(so['cardinality'].split('..')[0])>=1,
         'MediationConstraint2':int(ta['cardinality'].split('..')[0])>=1,
         'DependencyRelationshipConstraint2':ta['isReadOnly'] is True}
  rows.append({'relation':name,'rules':rules,'status':'PASS' if all(rules.values()) else 'FAIL'})
 return rows

def main():
 raw=(P/'ontouml-experimental.json').read_bytes();base=json.loads(raw);rows=[]
 with tempfile.TemporaryDirectory() as td:
  for key in VARIANTS:
   m,changes=variant(base,key);p=Path(td)/'model.json';p.write_text(json.dumps(m));out=Path(td)/'native.json'
   subprocess.run(['node',str(H.parent/'2.1.0-alpha.1-g3-p4a-supply-capacity/check_native.cjs'),str(p),sys.argv[1],str(out)],capture_output=True,check=True,timeout=30)
   native=json.loads(out.read_text());bounds=audit(m)
   selected=[r for r in bounds['rows'] if r['relation'] in {'rel-'+n for n in RELATIONS}]
   assert len(selected)==6 and all(r['overall']=='PASS' for r in selected)
   row={'variant':key,'patch':changes,'native_schema_parser':native,'bounded_subsetting':selected,'mediation_source_profile':source_profile(m),
        'full_candidate_validated':False,'scientific_acceptance':False}
   rows.append(row)
   for name in RELATIONS:
    fragment,ids=structural_fragment(m,'rel-'+name)
    write('fragments/'+key+'-'+name+'.json',fragment)
    # Exclusion manifest is inherited from the prior actual-fragment audit.
    row.setdefault('fragments',[]).append({'file':'fragments/'+key+'-'+name+'.json','included_ids':ids,
       'omission_scope':'Structural projection only: full original Notes, external relations and modern nature are not validated by legacy conversion.'})
 write('native-alternatives.json',{'source_sha256':hashlib.sha256(raw).hexdigest(),'status':'ISOLATED_UNACCEPTED_ALTERNATIVES','new_classes':0,'new_relations':0,'variants':rows})
 assert (P/'ontouml-experimental.json').read_bytes()==raw
 print(json.dumps({'variants':len(rows),'native_pass':sum(r['native_schema_parser']['pass'] for r in rows),'selected_subsetting_checks':18,'source_profiles':[{'variant':r['variant'],'rows':r['mediation_source_profile']} for r in rows]}))

if __name__=='__main__':main()
