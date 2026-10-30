import json, pathlib, hashlib, collections, platform
import rdflib
HERE=pathlib.Path(__file__).resolve().parent
ROOT=next(p for p in [HERE,*HERE.parents] if (p/'v2/ontology/candidates').exists()) if any((p/'v2/ontology/candidates').exists() for p in [HERE,*HERE.parents]) else HERE/'cm-pharme'
OUT=ROOT/'v2/requirements/2.1/orsd/0.1.0'
d=json.loads((OUT/'requirements.json').read_text())
checks=[]
def check(name,ok,detail=None):checks.append(dict(name=name,pass_=bool(ok),detail=detail))
r=d['requirements'];ids=[x['id'] for x in r]
check('requirement IDs unique',len(ids)==len(set(ids)))
check('83 tracked rows not semantic uniqueness',len(r)==83)
fields=['id','kind','domain','statement_fa','origin','priority','source_ids','positive_acceptance','negative_acceptance','acceptance_status','comparison_status','coverage_limit']
check('mandatory metadata',all(all(x.get(k) for k in fields) for x in r))
check('functional CQ and expected response',all(x.get('cq_id') and x.get('cq') and x.get('expected_answer') for x in r if x['kind']=='functional'))
check('no invented author approval',all(x['acceptance_status']=='PENDING_REVIEW' for x in r))
check('source IDs resolve',all(set(x['source_ids'])<={s['id'] for s in d['sources']} for x in r))
check('source hashes pinned files',all(hashlib.sha256((ROOT/s['path']).read_bytes()).hexdigest()==s['sha256'] for s in d['sources']))
check('13 refinements not counted as requirements',len(d['refinements'])==13 and not set(z['id'] for z in d['refinements'])&set(ids))
check('historical inventories separate',len(d['historical_source_inventories']['discovery'])==97 and len(d['historical_source_inventories']['held_out'])==51)
check('39 canonical IDs preserved',len([x for x in r if x['id'].startswith(('R-','B2-'))])==39)
check('B2 DS07 merge preserved','B2-DS-07' not in ids and 'R-DS-04' in ids)
queries=[]
for m in ['RM','PV','BA','DS']:
 home=ROOT/f'v2/ontology/candidates/2.1.0-alpha.1-module-contract-lab/modules/{m}'
 contract=json.loads((home/'contract.json').read_text())
 for q in contract['queries']:
  g=rdflib.Graph().parse(home/q['fixture'])
  actual=sorted([[str(v) for v in row] for row in g.query(q['query'])])
  queries.append(dict(module=m,id=q['id'],actual=actual,expected=q['expected'],passed=actual==q['expected'],fixture=q['fixture']))
check('23 bounded module query replays',len(queries)==23 and all(q['passed'] for q in queries))
out=dict(document_version=d['document_version'],baseline_commit=d['baseline_commit'],checks=checks,query_replays=queries,summary=dict(checks_pass=sum(x['pass_'] for x in checks),checks_total=len(checks),queries_pass=sum(x['passed'] for x in queries),queries_total=len(queries)),runtime=dict(python=platform.python_version(),rdflib=rdflib.__version__),limits=['Only the 23 module SELECT queries were rerun; their historical frozen fixtures are not independent real data.','No fresh HermiT or SHACL execution is claimed.','Metadata checks do not prove semantic validity, atomicity or completeness.'])
(OUT/'validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps(out['summary']))
assert all(x['pass_'] for x in checks)
