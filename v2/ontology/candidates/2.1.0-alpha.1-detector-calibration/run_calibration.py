"""Compile unchanged official detectors; inspect all fixture fields after official parsing.
Expected counts are declared before execution; disagreements are retained, not converted to pass.
"""
import json,subprocess,tempfile,hashlib,re,sys
from pathlib import Path
from make_fixtures import CASES,serialize
H=Path(__file__).resolve().parent;P=H.parent/'2.1.0-alpha.1-content-event-policy'
A=Path(sys.argv[1]);ECJ=Path(sys.argv[2]);PIN='42b926f6c2859dc87e49a96b8482eae28d02e7d5'
assert subprocess.check_output(['git','-C',str(A),'rev-parse','HEAD'],text=True).strip()==PIN
# Modifications to source would invalidate use of the official detector label.
assert not subprocess.check_output(['git','-C',str(A),'status','--porcelain','--untracked-files=no'],text=True).strip()
JARS=list(A.glob('br.ufes.inf.nemo.common/lib/**/*.jar'))+list(A.glob('br.ufes.inf.nemo.antipattern/lib/*.jar'))
assert len(JARS)>=70
(H/'fixtures').mkdir(exist_ok=True)
def expected_lines(m):
 out=['CLASS|'+c['name']+'|'+c['type']+'|'+str(c['abstract']).lower() for c in m['classes']]
 for r in m['relations']:
  out.append('REL|'+r['name']+'|'+r['type'])
  for i,e in enumerate(r['ends']):out.append('|'.join(['END',r['name'],str(i),e['name'],e['type'],str(e['lower']),str(e['upper']),e['aggregation'],','.join(sorted(e['subset']))]))
 out+=['GEN|'+g['specific']+'|'+g['general'] for g in m['generalizations']]
 gens={g['name']:g['specific']+'>'+g['general'] for g in m['generalizations']}
 out+=['SET|'+s['name']+'|'+str(s['disjoint']).lower()+'|'+str(s['complete']).lower()+'|'+','.join(sorted(gens[x] for x in s['generalizations'])) for s in m['sets']]
 return sorted(out)
rows=[];replays=[]
with tempfile.TemporaryDirectory() as td:
 cls=Path(td)/'classes';cls.mkdir();cp=':'.join([str(cls)]+[str(j) for j in JARS]);sp=':'.join(str(A/d/'src') for d in ['br.ufes.inf.nemo.ontouml','br.ufes.inf.nemo.common','br.ufes.inf.nemo.antipattern'])
 c=subprocess.run(['java','-jar',str(ECJ),'-nowarn','-d',str(cls),'-classpath',cp,'-sourcepath',sp,str(P/'RuntimeCatalogue.java'),str(H/'InspectLegacy.java')],capture_output=True,text=True,timeout=180)
 (H/'compile.log').write_text(c.stdout+c.stderr);assert c.returncode==0,(c.stdout+c.stderr)[-4000:]
 for case in CASES:
  stem=case['family']+'-'+case['name'];file=H/'fixtures'/(stem+'.refontouml');file.write_bytes(serialize(case['model'],stem))
  inspection=subprocess.run(['java','-cp',cp,'InspectLegacy',str(file)],capture_output=True,text=True,timeout=30)
  actual_lines=sorted(x for x in inspection.stdout.splitlines() if x.startswith(('CLASS|','REL|','END|','GEN|','SET|')))
  expected=expected_lines(case['model']);fidelity=inspection.returncode==0 and actual_lines==expected
  try:
   run=subprocess.run(['java','-cp',cp,'RuntimeCatalogue',case['family'],str(file)],capture_output=True,text=True,timeout=45);out=run.stdout+'\nSTDERR:\n'+run.stderr;match=re.search(r'occurrences=(\d+)',run.stdout);count=int(match[1]) if match else None
   clean=run.returncode==0 and match is not None and not re.search(r'exception|could not create|does not characterize|error|failed',out,re.I)
   result={'family':case['family'],'name':case['name'],'category':case['category'],'expected_engine_occurrences':case['expected_engine_occurrences'],'actual_occurrences':count,'clean_process':bool(clean),'fixture_fields_preserved':fidelity,'engine_expectation_pass':bool(clean) and fidelity and count==case['expected_engine_occurrences'],'documentation_expected_occurrences':case['documentation_expected_occurrences'],'documentation_expectation_matches':None if case['documentation_expected_occurrences'] is None else count==case['documentation_expected_occurrences'],'fixture':str(file.relative_to(H)),'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'expected_parsed_fields':expected,'actual_parsed_fields':actual_lines,'parser_stderr':inspection.stderr,'detector_output':out}
  except subprocess.TimeoutExpired:result={'family':case['family'],'name':case['name'],'category':case['category'],'engine_expectation_pass':False,'timeout':45}
  rows.append(result);print(json.dumps({k:v for k,v in result.items() if k not in ['expected_parsed_fields','actual_parsed_fields','parser_stderr','detector_output']}),flush=True)
 # Only eight prior controlled fixtures, no optional rerun of the historical sample.
 for old in json.loads((P/'sensitivity-results.json').read_text())['rows']:
  f=P/'detector-toys'/(old['detector']+'-'+old['name']+'.refontouml');r=subprocess.run(['java','-cp',cp,'RuntimeCatalogue',old['detector'],str(f)],capture_output=True,text=True,timeout=45);match=re.search(r'occurrences=(\d+)',r.stdout);count=int(match[1]) if match else None
  clean=r.returncode==0 and match is not None and not re.search(r'exception|could not create|does not characterize|error|failed',r.stdout+r.stderr,re.I)
  replays.append({'family':old['detector'],'name':old['name'],'expected':old['expected'],'actual':count,'pass':bool(clean) and count==old['expected'],'fixture_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'output':r.stdout+r.stderr})
families=sorted(set(c['family'] for c in CASES));paired=[r for r in rows if r['category']=='paired']
coverage={f:all(r['engine_expectation_pass'] for r in paired if r['family']==f) and len([r for r in paired if r['family']==f])==2 for f in families}
report={'scope':'Direct legacy fixture detector sensitivity; NOT native JSON conversion and NOT full current CM-PharmE execution.','archive_commit':PIN,'archive_tracked_source_unchanged':True,'ecj_sha256':hashlib.sha256(ECJ.read_bytes()).hexdigest(),'java_version':subprocess.check_output(['java','-version'],stderr=subprocess.STDOUT,text=True).strip(),'jar_order':[str(j.relative_to(A)) for j in JARS],'paired_cases':len(paired),'paired_cases_pass':sum(r['engine_expectation_pass'] for r in paired),'new_families_with_passing_pair':sum(coverage.values()),'family_pair_status':coverage,'prior_replay_cases':len(replays),'prior_replay_pass':sum(r['pass'] for r in replays),'documentation_discrepancy_probes':[r for r in rows if r['category']!='paired'],'rows':rows,'prior_replays':replays,'full_candidate_executed':False,'modern_adapter_fidelity_proven':False}
(H/'calibration-results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if isinstance(v,(int,bool))}),flush=True)

assert all(r['engine_expectation_pass'] for r in rows) and all(r['pass'] for r in replays), 'Preserved calibration failures require investigation'
