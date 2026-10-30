"""Actual archived detector runtime smoke test; no claim of full-model fidelity or sensitivity."""
import json,sys,subprocess,tempfile,hashlib,re
from pathlib import Path
H=Path(__file__).resolve().parent
A=Path(sys.argv[1]);ECJ=Path(sys.argv[2]);PIN='42b926f6c2859dc87e49a96b8482eae28d02e7d5'
assert subprocess.check_output(['git','-C',str(A),'rev-parse','HEAD'],text=True).strip()==PIN
names='BinOver DecInt DepPhase FreeRole GSRig HetColl HomoFunc ImpAbs MixIden MixRig MultiDep PartOver RelComp RelOver RelRig RelSpec RepRel UndefFormal UndefPhase WholeOver'.split()
jars=list(A.glob('br.ufes.inf.nemo.common/lib/**/*.jar'))+list(A.glob('br.ufes.inf.nemo.antipattern/lib/*.jar'))
sample=A/'br.ufes.inf.nemo.antipattern/models/The Internship Model.refontouml'
rows=[]
with tempfile.TemporaryDirectory() as td:
 cls=Path(td)/'classes';cls.mkdir();cp=':'.join([str(cls)]+[str(j) for j in jars])
 sp=':'.join(str(A/d/'src') for d in ['br.ufes.inf.nemo.ontouml','br.ufes.inf.nemo.common','br.ufes.inf.nemo.antipattern'])
 compile=subprocess.run(['java','-jar',str(ECJ),'-nowarn','-d',str(cls),'-classpath',cp,'-sourcepath',sp,str(H/'RuntimeCatalogue.java')],capture_output=True,text=True,timeout=180)
 (H/'catalogue-compile.log').write_text(compile.stdout+compile.stderr)
 assert compile.returncode==0,(compile.stdout+compile.stderr)[-6000:]
 for name in names:
  try:
   p=subprocess.run(['java','-cp',cp,'RuntimeCatalogue',name,str(sample)],capture_output=True,text=True,timeout=60)
   output=p.stdout+'\nSTDERR:\n'+p.stderr
   m=re.search(r'CMPE_RESULT detector=(\w+) classes=(\d+) associations=(\d+) occurrences=(\d+)',p.stdout)
   hidden=bool(re.search(r'exception|could not create|error|failed',output,re.I))
   row={'detector':name,'exit_code':p.returncode,'clean_runtime':p.returncode==0 and m is not None and not hidden,'occurrences':int(m[4]) if m else None,'reported_exception_or_error':hidden,'output':output}
  except subprocess.TimeoutExpired:row={'detector':name,'clean_runtime':False,'timeout_seconds':60}
  rows.append(row);print(json.dumps({k:v for k,v in row.items() if k!='output'}),flush=True)
 report={'scope':'Historical bundled sample runtime smoke only. Not detector sensitivity validation; NOT full candidate execution.','archive_commit':PIN,'sample_path':str(sample.relative_to(A)),'sample_sha256':hashlib.sha256(sample.read_bytes()).hexdigest(),'ecj_sha256':hashlib.sha256(ECJ.read_bytes()).hexdigest(),'jar_order':[str(j.relative_to(A)) for j in jars],'total':len(rows),'clean_runtime_count':sum(x['clean_runtime'] for x in rows),'full_candidate_executed':False,'rows':rows}
 (H/'catalogue-results.json').write_text(json.dumps(report,indent=2)+'\n')
