from lab import *
import base64,gzip
cases=[]
for folder,filename in [('2.1.0-alpha.1-four-domain-lab','shacl-results.json'),('2.1.0-alpha.1-four-domain-refinement','refinement-shacl-results.json'),('2.1.0-alpha.1-content-event-policy','shacl-results.json'),('2.1.0-alpha.1-registry-policy-lab','shacl-results.json')]:
 root=H.parent/folder;data=json.loads((root/filename).read_text());rows=data['cases'] if isinstance(data,dict) else data
 for row in rows:
  r=admission(Graph().parse(root/row['fixture']));marker=row.get('expected_failure_marker',row.get('expected_marker',row.get('marker')))
  cases.append({'source':folder+'/'+row['fixture'],'expected':row['expected_conforms'],**r,'pass':r['conforms']==row['expected_conforms'] and (marker is None or marker in str(r['violations']))})
data=json.loads((PREV/'test-results.json').read_text());fixtures=Dataset().parse(PREV/'test-fixtures.trig',format='trig')
for row in data['shacl']:
 g=fixtures.graph(URIRef('urn:cmpe-context-case:'+row['name']));assert len(g)
 r=admission(g);cases.append({'source':'reporting-context/'+row['name'],'expected':row['expected'],**r,'pass':r['conforms']==row['expected'] and (row['marker'] is None or row['marker'] in str(r['violations']))})
positive=Graph().parse(ctx.PREV/'combined-positive-abox.ttl')+Graph().parse(H/'positive-abox.ttl')+Graph().parse(H/'prac-claims.ttl')+Graph().parse(PREV/'ndc-claims.ttl')+Graph().parse(PREV/'esmp-guidance.ttl')
combined=ctx.prev.hermit(full+positive)
raw=gzip.decompress(base64.b64decode((H.parent/'2.1.0-alpha.1-g3-3-d-real-source-migration/real-source-abox.nt.gz.b64').read_text()));assert hashlib.sha256(raw).hexdigest()=='939a80c8f3d4342e81c74c193cd9e65dc61b1b7e271ba99856edfd988daebfa9'
old=Graph().parse(data=raw.decode(),format='nt');old_check=admission(old);old_logic=ctx.prev.hermit(full+old)
out={'cases':cases,'pass':sum(x['pass'] for x in cases),'total':len(cases),'combined_positive_graph_triples':len(positive),'combined_hermit':combined,'old_real':{'rows':768,'triples':len(old),'shacl':old_check,'hermit':old_logic},'scope':'130 asserted-data admission expectations, combined positive HermiT and historical data non-regression; not full native or materialized C-contract validation.'}
write('regression-results.json',out);print(json.dumps({k:v for k,v in out.items() if k!='cases'}),flush=True)
assert all(x['pass'] for x in cases) and old_check['conforms']
assert all(x['consistent'] and not x['unsatisfiable_named_classes'] for x in [combined,old_logic])
