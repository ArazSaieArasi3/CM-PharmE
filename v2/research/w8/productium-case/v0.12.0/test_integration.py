import json, hashlib, sqlite3
from pathlib import Path
from rdflib import Graph, RDF, URIRef, Literal, Namespace
from rdflib.compare import isomorphic
from pyshacl import validate
import integrate_case as m
R=m.R;payload=json.loads((R/'generated/explorer-data.json').read_text())
g=Graph().parse(R/'generated/case.nt',format='nt')
shape=Graph().parse(m.I/'2.1.0-alpha.1-candidate/constraints.ttl')
raw=json.loads((m.I/'2.1.0-alpha.1-prov-target-lab/sources/ndc-response.json').read_text())
checks=[]
def check(name,value):
 checks.append({'name':name,'pass':bool(value)});assert value,name
check('exact-publisher-extract-hash',m.sha(m.I/'2.1.0-alpha.1-prov-target-lab/sources/ndc-response.json')==payload['policy']['raw_source_sha256'])
check('five-source-rows-seven-package-projections',len(payload['products'])==5 and sum(len(x['packages']) for x in payload['products'])==7)
check('upstream-graph-retained-isomorphically',isomorphic(g,Graph().parse(m.I/'2.1.0-alpha.1-prov-target-lab/ndc-abox.ttl')))
check('all-original-product-fields-preserved',all(x['source_envelope']==raw['results'][i] for i,x in enumerate(payload['products'])))
check('all-package-pointers-resolve-exact-source-envelope',all(p['source_envelope']==raw['results'][i]['packaging'][j] and p['source_pointer']==f'/results/{i}/packaging/{j}' for i,x in enumerate(payload['products']) for j,p in enumerate(x['packages'])))
similar_names=[p for p in payload['products'] if 'Advanced Rx' in p['organization_name']]
check('similar-labeler-names-retain-distinct-row-organization-references',len(similar_names)==2 and len(set(x['organization_id'] for x in similar_names))==2)
check('manufacturer-distributor-not-inferred',not list(g.subjects(RDF.type,m.C.ManufacturerRole)) and not list(g.subjects(RDF.type,m.C.WholesaleDistributorRole)))
check('approval-not-inferred',not list(g.subjects(RDF.type,m.C.RegulatoryAuthorization)) and all(p['approval_status']=='UNKNOWN' for x in payload['products'] for p in x['packages']))
check('no-cross-source-sameAs-merge',not list(g.triples((None,__import__('rdflib').OWL.sameAs,None))))
check('product-and-package-dates-not-collapsed',any(x['product_marketing_start']!=p['package_marketing_start'] for x in payload['products'] for p in x['packages']))
check('complete-native-shacl-profile-positive',validate(g,shacl_graph=shape,advanced=True,inference='none')[0])
listing=URIRef(payload['products'][0]['packages'][0]['listing'])
org=URIRef(payload['products'][0]['organization_id'])
mutations=[]
for name,predicate in [('missing-organization',m.C.listingResponsibleOrganization),('missing-presentation',m.C.listingPresentation)]:
 bad=Graph();bad+=g;bad.remove((listing,predicate,None));mutations.append((name,bad))
bad=Graph();bad+=g;bad.add((listing,m.C.listingResponsibleOrganization,URIRef(payload['products'][1]['organization_id'])));mutations.append(('two-responsible-organizations',bad))
bad=Graph();bad+=g;bad.set((listing,m.C.listingResponsibleOrganization,URIRef(payload['products'][0]['id'])));mutations.append(('product-used-as-organization',bad))
for name,bad in mutations:check('native-shacl-rejects-'+name,not validate(bad,shacl_graph=shape,advanced=True,inference='none')[0])
with sqlite3.connect(R/'generated/explorer.sqlite') as c:
 c.execute('PRAGMA foreign_keys=ON')
 check('sqlite-integrity-and-fks',c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall())
 exported=Graph().parse(data='\n'.join(' '.join(x)+' .' for x in c.execute('SELECT s,p,o FROM triple')),format='nt')
 check('sqlite-rdf-exact-roundtrip',isomorphic(g,exported))
 try:c.execute("UPDATE listing SET approval_status='APPROVED'");rejected=False
 except sqlite3.IntegrityError:rejected=True
 check('sql-rejects-unsupported-approval',rejected)
 try:c.execute("UPDATE listing SET organization_id='missing'");rejected=False
 except sqlite3.IntegrityError:rejected=True
 check('sql-rejects-dangling-organization',rejected)
 c.rollback()
relations=json.loads((m.I/'2.1.0-alpha.1-candidate/ontouml.json').read_text())['elements'];index={x['id']:x for x in relations}
check('native-listing-mediations-and-exact-target-multiplicities',all(index['rel-'+p]['stereotype']=='mediation' and index['end-'+p+'-target']['cardinality']=='1' and index['end-'+p+'-source']['cardinality']=='1..*' for p in ['listingPresentation','listingResponsibleOrganization']))
out={'version':'0.12.0','passed':len(checks),'checks':checks,'scope':'Source fidelity, identity boundaries, native profile mutations and lossless local projection. No independent expert or user effectiveness evaluation.'}
m.write('results/Integration_Tests_v0_12_0.json',out);print('Integration checks passed:',len(checks))
