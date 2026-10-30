"""Execute exported packages from temporary directories outside the repository."""
from pathlib import Path
import tempfile,shutil,subprocess,json,sys,os
H=Path(__file__).resolve().parent
results=[]
for m in ['RM','PV','BA','DS']:
 with tempfile.TemporaryDirectory(prefix='cmpe-standalone-') as t:
  d=Path(t)/m;shutil.copytree(H/'modules'/m,d)
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None)
  r=subprocess.run([sys.executable,str(d/'runner.py')],cwd=t,capture_output=True,text=True,env=env)
  print(m,r.returncode,r.stdout,r.stderr[-1000:],flush=True)
  if (d/'results.json').exists():shutil.copyfile(d/'results.json',H/'modules'/m/'results.json')
  results.append({'module':m,'outside_repository':True,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
(H/'standalone-results.json').write_text(json.dumps(results,indent=2)+'\n')
assert all(x['exit_code']==0 for x in results)
