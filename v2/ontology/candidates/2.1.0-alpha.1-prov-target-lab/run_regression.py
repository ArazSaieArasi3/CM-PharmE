"""Replay historical admission contracts; separately test combined OWL semantics."""
from common import *
import base64,gzip
sources=[]
for folder,filename in [('2.1.0-alpha.1-four-domain-lab','shacl-results.json'),('2.1.0-alpha.1-four-domain-refinement','refinement-shacl-results.json'),('2.1.0-alpha.1-content-event-policy','shacl-results.json'),('2.1.0-alpha.1-registry-policy-lab','shacl-results.json')]:
 root=H.parent/folder;data=json.loads((root/filename).read_text());rows=data['cases'] if isinstance(data,dict) else data
 sources.extend((root,row) for row in rows)
results=[];positive=graph();positive_count=0
for i,(folder,row) in enumerate(sources):
 g=Graph().parse(folder/row['fixture']);r=shacl(g)
 marker=row.get('expected_failure_marker',row.get('expected_marker',row.get('marker')))
 want=row['expected_conforms'];passed=r['conforms']==want and (marker is None or any(marker in str(x) for x in r['violations']))
 results.append({'source':str(folder.name+'/'+row['fixture']),'expected':want,**r,'marker':marker,'pass':passed})
 if want:
  positive_count+=1
  individuals={n for n in g.subjects() if isinstance(n,URIRef) and not any(str(n).startswith(str(ns)) for ns in [C,L,R,P,RDF,RDFS,OWL,SH])}
  mapping={n:Q['regression-'+str(i)+'-'+hashlib.sha256(str(n).encode()).hexdigest()[:20]] for n in individuals}
  for s,p,o in g:positive.add((mapping.get(s,s),p,mapping.get(o,o)))
save('combined-positive-abox.ttl',positive)
combined=hermit(full+positive)
combined_with_prior_proposals=hermit(full+reg.delta()+positive)
encoded=H.parent/'2.1.0-alpha.1-g3-3-d-real-source-migration/real-source-abox.nt.gz.b64'
raw=gzip.decompress(base64.b64decode(encoded.read_text()));real=Graph().parse(data=raw.decode(),format='nt')
assert hashlib.sha256(raw).hexdigest()=='939a80c8f3d4342e81c74c193cd9e65dc61b1b7e271ba99856edfd988daebfa9'
real_result={'rows':768,'triples':len(real),'sha256':hashlib.sha256(raw).hexdigest(),'shacl':shacl(real),'hermit':hermit(full+real),'new_profile_witnesses':len(list(real.triples((None,P.profile,None))))}
out={'cases':results,'pass':sum(x['pass'] for x in results),'total':len(results),'positive_fixture_count':positive_count,
 'combined_positive_triples':len(positive),'combined_positive_hermit':combined,'combined_with_prior_two_disjointness_proposals':combined_with_prior_proposals,
 'old_real_sample':real_result,'C_materialization_applied':False,'C_regression_88_of_89_unresolved':True,
 'scope':'116 historical input admission cases, inference=none with explicit named-class hierarchy; not a claim that arbitrary reasoner-materialized graphs preserve closed-world validation outcomes. Full PROV reasoning is separately exercised with HermiT.'}
write('regression-results.json',out);print(json.dumps({'admission':str(out['pass'])+'/'+str(out['total']),'positive_fixtures':positive_count,'combined':combined,'prior_real':real_result}),flush=True)
assert all(x['pass'] for x in results)
assert all(x['consistent'] and not x['unsatisfiable_named_classes'] for x in [combined,combined_with_prior_proposals,real_result['hermit']])
assert real_result['shacl']['conforms']
