"""Historical admission replay and combined proposed-schema consistency.

No acceptance or full native/OWL2-DL certification is inferred from these tests.
"""
from lab import *
import base64,gzip
hierarchy=prev.reg.hierarchy+Graph()
for a,b in (M+prev.alignment).subject_objects(RDFS.subClassOf):hierarchy.add((a,RDFS.subClassOf,b))
combined_shapes=prev.reg.base_shapes+prev.reg.shapes()+S
def admitted(g):
 ok,r,_=validate(g+hierarchy,shacl_graph=combined_shapes,advanced=True,inference='none')
 return {'conforms':bool(ok),'violations':[{'path':str(r.value(x,SH.resultPath) or ''),'constraint':str(r.value(x,SH.sourceConstraint) or ''),'component':str(r.value(x,SH.sourceConstraintComponent) or '')} for x in r.subjects(RDF.type,SH.ValidationResult)]}
rows=[]
for folder,filename in [('2.1.0-alpha.1-four-domain-lab','shacl-results.json'),('2.1.0-alpha.1-four-domain-refinement','refinement-shacl-results.json'),('2.1.0-alpha.1-content-event-policy','shacl-results.json'),('2.1.0-alpha.1-registry-policy-lab','shacl-results.json')]:
 root=H.parent/folder;data=json.loads((root/filename).read_text());cases=data['cases'] if isinstance(data,dict) else data
 for row in cases:
  g=Graph().parse(root/row['fixture']);r=admitted(g)
  marker=row.get('expected_failure_marker',row.get('expected_marker',row.get('marker')))
  rows.append({'source':folder+'/'+row['fixture'],'expected':row['expected_conforms'],**r,'marker':marker,'pass':r['conforms']==row['expected_conforms'] and (marker is None or marker in str(r['violations']))})
positive=Graph().parse(PREV/'combined-positive-abox.ttl')
context,_,_=fixture();ndc=Graph().parse(H/'ndc-claims.ttl');esmp=Graph().parse(H/'esmp-guidance.ttl')
new_admission=admitted(context+ndc+esmp)
integrated=full+positive+context+ndc+esmp
logical=prev.hermit(integrated)
with_prior=prev.hermit(integrated+prev.reg.delta())
encoded=H.parent/'2.1.0-alpha.1-g3-3-d-real-source-migration/real-source-abox.nt.gz.b64'
raw=gzip.decompress(base64.b64decode(encoded.read_text()))
assert hashlib.sha256(raw).hexdigest()=='939a80c8f3d4342e81c74c193cd9e65dc61b1b7e271ba99856edfd988daebfa9'
real=Graph().parse(data=raw.decode(),format='nt');old_admission=admitted(real);old_logic=prev.hermit(full+real)
out={'pass':sum(x['pass'] for x in rows),'total':len(rows),'cases':rows,'historical_positive_fixtures':45,'combined_graph_triples':len(integrated),'combined_hermit':logical,'combined_with_prior_two_disjointness_proposals':with_prior,'old_real':{'rows':768,'triples':len(real),'sha256':hashlib.sha256(raw).hexdigest(),'admission':old_admission,'hermit':old_logic,'new_claim_profile_witnesses':len(list(real.subjects(RDF.type,B.StructuredClaim)))},'limits':['Admission replay uses inference=none with explicit named-class hierarchy.','Combined consistency does not mean every historical closed-world shape accepts new descriptive claims.','Historical C materialization 88/89 contract remains unresolved and is not applied.','New official-guidance profiles are distinct from synthetic matching contexts.','No native model, baseline or earlier artifact is modified.']}
out['new_data_with_combined_historical_and_new_shapes']=new_admission
write('regression-results.json',out)
print(json.dumps({'admission':str(out['pass'])+'/'+str(out['total']),'combined':logical,'prior_proposals':with_prior,'old_real':out['old_real']}),flush=True)
assert all(x['pass'] for x in rows) and old_admission['conforms']
assert all(x['consistent'] and not x['unsatisfiable_named_classes'] for x in [logical,with_prior,old_logic])
