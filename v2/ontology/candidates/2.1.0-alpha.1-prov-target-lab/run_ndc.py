"""Source-bounded NDC package observations. No global identity or approval inference.

Product fields stay product-level; package dates stay package-level. A source record
is the API product row. Its package projections are separately identified derived
records with JSON pointers, and are never counted as independent product rows.
"""
from common import *
from datetime import datetime
raw=(H/'sources/ndc-response.json').read_bytes()
meta=json.loads((H/'sources/ndc-source.json').read_text())
assert hashlib.sha256(raw).hexdigest()==meta['sha256']
data=json.loads(raw);g=graph();mapping=[]
snapshot=Q['ndc-response-'+meta['sha256'][:16]]
release=Q['ndc-extract-'+meta['sha256'][:16]]
dataset=Q['ndc-query-dataset'];activity=Q['ndc-package-projection-'+meta['sha256'][:16]]
typ(g,snapshot,C.SourceRecord);typ(g,release,C.DatasetRelease);typ(g,dataset,C.Dataset);typ(g,activity,C.ProvenanceActivity)
g.add((dataset,C.hasDatasetRelease,release));g.add((activity,PROV.used,snapshot))
g.add((snapshot,Q.retrievalURL,Literal(meta['requested_url'])))
g.add((snapshot,Q.sourceSHA256,Literal(meta['sha256'])))
g.add((snapshot,Q.sourceLastUpdated,Literal(data['meta']['last_updated'],datatype=XSD.date)))
g.add((release,Q.releaseKind,Literal('query-extract-not-full-directory')))
jurisdiction=Q['us'];typ(g,jurisdiction,C.RegulatoryJurisdiction)
def date(raw_value):return datetime.strptime(raw_value,'%Y%m%d').date().isoformat()
for i,row in enumerate(data['results']):
 product=Q['source-product-'+row['product_ndc']]
 reporter=Q['source-labeler-row-'+str(i)]
 source=Q['source-row-'+meta['sha256'][:16]+'-'+str(i)]
 typ(g,source,C.SourceRecord);typ(g,product,C.MedicinalProduct)
 typ(g,reporter,C.Organization);typ(g,reporter,C.ListingResponsibleOrganizationRole)
 g.add((reporter,RDFS.label,Literal(row['labeler_name'])))
 g.add((source,Q.jsonPointer,Literal('/results/'+str(i))))
 g.add((source,PROV.wasDerivedFrom,snapshot));g.add((source,PROV.wasAttributedTo,reporter))
 g.add((source,Q.sourceProductId,Literal(row['product_id'])))
 # Raw category is retained as a claim field; it does not decide approval.
 g.add((source,Q.rawMarketingCategory,Literal(row['marketing_category'])))
 if row.get('marketing_start_date'):g.add((source,Q.productMarketingStart,Literal(date(row['marketing_start_date']),datatype=XSD.date)))
 if row.get('marketing_end_date'):g.add((source,Q.productMarketingEnd,Literal(date(row['marketing_end_date']),datatype=XSD.date)))
 for j,pack in enumerate(row.get('packaging',[])):
  record=Q['package-record-'+meta['sha256'][:16]+'-'+str(i)+'-'+str(j)]
  presentation=Q['source-presentation-'+pack['package_ndc']]
  fact=Q['source-listing-'+meta['sha256'][:16]+'-'+str(i)+'-'+str(j)]
  typ(g,record,C.SourceRecord);typ(g,presentation,C.MedicinalProductPresentation);typ(g,presentation,C.ListedPresentationRole);typ(g,fact,C.MarketListing)
  g.add((presentation,C.presentationOf,product));g.add((presentation,RDFS.label,Literal(pack['description'])))
  g.add((record,P.profile,Literal('registry-record')));g.add((record,P.recordKind,Literal('listing')))
  g.add((record,P.recordSubject,presentation));g.add((record,P.representsFact,fact));g.add((record,P.release,release));g.add((release,C.containsSourceRecord,record))
  g.add((fact,C.listingPresentation,presentation));g.add((fact,C.listingResponsibleOrganization,reporter));g.add((fact,C.listingJurisdiction,jurisdiction))
  g.add((record,P.externalKey,Literal(row['product_id']+'#'+pack['package_ndc'])))
  g.add((record,P.approvalConclusion,Literal('unknown')))
  g.add((record,P.retrievedAt,Literal(meta['retrieved_at'],datatype=XSD.dateTime)))
  g.add((record,PROV.wasAttributedTo,reporter));g.add((record,PROV.wasDerivedFrom,source));g.add((record,L.recordDigitalActivity,activity))
  pointer='/results/'+str(i)+'/packaging/'+str(j);g.add((record,Q.jsonPointer,Literal(pointer)))
  for raw_key,pred in [('marketing_start_date',P.marketingStart),('marketing_end_date',P.marketingEnd)]:
   if pack.get(raw_key):g.add((record,pred,Literal(date(pack[raw_key]),datatype=XSD.date)))
  mapping.append({'row':i,'package_index':j,'json_pointer':pointer,'product_id':row['product_id'],
   'product_ndc':row['product_ndc'],'package_ndc':pack['package_ndc'],'record':str(record),
   'product_date':row.get('marketing_start_date'),'package_date':pack.get('marketing_start_date'),
   'same_labeler_name_does_not_merge_organizations':True,'source_asserted_listing_not_independent_approval':True})
save('ndc-abox.ttl',g);write('ndc-traceability.json',mapping)
s=shacl(g);h=hermit(full+g)
checks=[]
def check(name,actual,expected):checks.append({'name':name,'expected':expected,'actual':actual,'pass':actual==expected})
def approval(g,record):
 q='ASK { ?record p:approvalEvidence ?e ; p:recordSubject ?subject . ?e a c:SourceRecord ; p:recordKind "regulatory-decision" ; p:recordSubject ?subject . FILTER(?e != ?record) FILTER NOT EXISTS { ?record (owl:sameAs|^owl:sameAs)+ ?e } }'
 return 'SOURCE_DECISION_AVAILABLE_NOT_VERIFIED' if bool(g.query(reg.PREFIX+q,initBindings={'record':record})) else 'UNKNOWN'
def window(g,record,on_date):
 start=g.value(record,P.marketingStart);end=g.value(record,P.marketingEnd)
 if start is None or end is None:return 'UNKNOWN'
 d=datetime.strptime(on_date,'%Y-%m-%d').date()
 return 'WITHIN_DECLARED_WINDOW' if start.toPython()<=d<end.toPython() else 'OUTSIDE_DECLARED_WINDOW'
check('api-product-rows',len(data['results']),5)
check('all-packages-projected',len(mapping),sum(len(r.get('packaging',[])) for r in data['results']))
check('all-projections-traceable',sum(1 for x in mapping if data['results'][x['row']]['packaging'][x['package_index']]['package_ndc']==x['package_ndc']),len(mapping))
for item in mapping:
 rec=URIRef(item['record'])
 check('approval-unknown-'+item['package_ndc'],approval(g,rec),'UNKNOWN')
 check('window-unknown-'+item['package_ndc'],window(g,rec,'2026-10-09'),'UNKNOWN')
check('no-authorization-assertion',len(list(g.subjects(RDF.type,C.RegulatoryAuthorization))),0)
check('contains-product-package-date-difference',any(x['product_date']!=x['package_date'] for x in mapping),True)
check('native-plus-profile-shacl',s['conforms'],True)
check('full-prov-hermit-consistent',h['consistent'] and not h['unsatisfiable_named_classes'],True)
# An independent countermodel for every source listing and source record.
negative=g+Graph()
for x in list(g.subjects(RDF.type,C.MarketListing))+list(g.subjects(RDF.type,C.SourceRecord)):
 not_type(negative,x,C.RegulatoryAuthorization)
counter=hermit(full+negative);check('no-approval-countermodel',counter['consistent'],True)
# Malformed real-record mutation must be caught without weakening shapes.
mut=g+Graph();rec=URIRef(mapping[0]['record']);mut.set((rec,P.approvalConclusion,Literal('source-asserted-approved')))
mutation=shacl(mut);check('unsupported-approval-mutation-rejected',mutation['conforms'],False)
save('fixtures/ndc-unsupported-approval.ttl',mut)
# Synthetic additions test that the parameterized queries actually select the record.
control=g+Graph();rec=URIRef(mapping[0]['record']);control.add((rec,P.marketingEnd,Literal('2027-01-01',datatype=XSD.date)))
check('synthetic-end-boundary-control',window(control,rec,'2026-10-09'),'WITHIN_DECLARED_WINDOW')
check('synthetic-end-exclusive-control',window(control,rec,'2027-01-01'),'OUTSIDE_DECLARED_WINDOW')
typ(control,T.syntheticDecision,C.SourceRecord);control.add((T.syntheticDecision,P.recordKind,Literal('regulatory-decision')))
control.add((T.syntheticDecision,P.recordSubject,g.value(rec,P.recordSubject)));control.add((rec,P.approvalEvidence,T.syntheticDecision))
check('synthetic-decision-detection-control',approval(control,rec),'SOURCE_DECISION_AVAILABLE_NOT_VERIFIED')
save('fixtures/ndc-synthetic-query-controls.ttl',control)
out={'source_rows':len(data['results']),'package_projections':len(mapping),'triples':len(g),
 'source_last_updated':data['meta']['last_updated'],'source_sha256':meta['sha256'],
 'shacl':s,'hermit':h,'approval_countermodel':counter,'mutation':mutation,
 'checks':checks,'pass':sum(x['pass'] for x in checks),'total':len(checks),
 'sampling':'First five API results with no randomization or representativeness claim.',
 'identity':'Source-scoped product/package/labeler references; no cross-source sameAs, labeler name deduplication or independently verified identity.',
 'provenance':'Projection activity is this local transformation, not the historical FDA/labeler submission event. wasAttributedTo identifies the source-reported labeler; no FDA verification claim.',
 'coverage':'Real listing/package/attribution/derived-record paths only. No establishment-registration, independent approval, ESMP, revision or risk-event witness.'}
out['query_fix']='Previous lab helpers use fixed fixture IRIs; these checks use explicit record bindings. The initial helper run is preserved but is not valid real-data query evidence.'
write('ndc-results.json',out);print(json.dumps({k:out[k] for k in ['source_rows','package_projections','triples','pass','total']}),flush=True)
assert all(x['pass'] for x in checks)
