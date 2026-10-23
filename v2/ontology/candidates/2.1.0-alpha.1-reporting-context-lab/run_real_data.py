"""A claim-only projection of the pinned purposive NDC sample.
Source rows, not projections, are the empirical counting unit.
"""
from lab import *
from collections import Counter
manifest=json.loads((H/'sources/ndc-manifest.json').read_text());g=graph();trace=[];unique={};checks=[];snapshots=[]
def check(name,actual,want):checks.append({'name':name,'actual':actual,'expected':want,'pass':actual==want})
for source in manifest['strata']:
 if 'file' not in source:continue
 raw=(H/'sources'/source['file']).read_bytes();assert hashlib.sha256(raw).hexdigest()==source['sha256']
 data=json.loads(raw);snapshots.append((source,data))
 snapshot=B['ndc-'+source['sha256'][:20]];typ(g,snapshot,C.SourceRecord)
 value(g,snapshot,B.sourceURL,source['requested_url'],XSD.anyURI);value(g,snapshot,B.sourceSHA256,source['sha256'])
 for i,row in enumerate(data['results']):
  pid=row['product_id'];fingerprint=hashlib.sha256(json.dumps(row,sort_keys=True).encode()).hexdigest()
  if pid in unique:
   check('duplicate-row-content-'+pid,unique[pid]['fingerprint']==fingerprint,True);unique[pid]['occurrences'].append({'file':source['file'],'pointer':'/results/'+str(i)});continue
  unique[pid]={'row':row,'fingerprint':fingerprint,'occurrences':[{'file':source['file'],'pointer':'/results/'+str(i)}]}
  record=B['ndc-row-'+fingerprint[:20]];typ(g,record,C.SourceRecord);g.add((record,PROV.wasDerivedFrom,snapshot))
  value(g,record,B.evidencePointer,source['file']+'#/results/'+str(i))
  product=B['ndc-product-'+pid];reporter=B['ndc-labeler-'+fingerprint[:20]]
  typ(g,product,C.MedicinalProduct);typ(g,reporter,C.Organization);value(g,reporter,RDFS.label,row['labeler_name'])
  g.add((record,PROV.wasAttributedTo,reporter))
  claim(g,B['category-'+fingerprint[:20]],record,product,B.rawMarketingCategory,Literal(row['marketing_category']),pointer=source['file']+'#/results/'+str(i)+'/marketing_category',origin='source-extracted')
  # JSON dates are strings. Preserve the exact YYYYMMDD lexical value; validate
  # its calendar interpretation in Python. Do not invent a time or timezone.
  for field in ['marketing_start_date','marketing_end_date']:
   if row.get(field):
    parsed=datetime.strptime(row[field],'%Y%m%d')
    check('product-date-lexical-'+pid+'-'+field,parsed.strftime('%Y%m%d'),row[field])
    claim(g,B['date-'+fingerprint[:20]+'-product-'+field],record,product,B['product_'+field],Literal(row[field],datatype=XSD.string),pointer=source['file']+'#/results/'+str(i)+'/'+field,origin='source-extracted')
  for j,pack in enumerate(row.get('packaging',[])):
   key=fingerprint[:20]+'-'+str(j);listing=B['described-listing-'+key];presentation=B['ndc-package-'+pack['package_ndc']]
   typ(g,presentation,C.MedicinalProductPresentation);g.add((presentation,C.presentationOf,product))
   pointer=source['file']+'#/results/'+str(i)+'/packaging/'+str(j)
   # Five propositions about the source-described listing. No asserted MarketListing or ListedPresentationRole.
   facts=[(listing,RDF.type,C.MarketListing),(listing,C.listingPresentation,presentation),
          (listing,C.listingResponsibleOrganization,reporter),(presentation,RDF.type,C.ListedPresentationRole),
          (presentation,B.packageNDC,Literal(pack['package_ndc']))]
   for k,(sub,pred,obj) in enumerate(facts):claim(g,B['claim-'+key+'-'+str(k)],record,sub,pred,obj,pointer=pointer+('/package_ndc' if k==4 else ''),origin='source-extracted' if k==4 else 'mapping-interpretation')
   # Product and package dates are separate source propositions, never collapsed.
   for unit,entity,objdict in [('package',presentation,pack)]:
    for field in ['marketing_start_date','marketing_end_date']:
     if objdict.get(field):
      parsed=datetime.strptime(objdict[field],'%Y%m%d')
      check('package-date-lexical-'+pack['package_ndc']+'-'+field,parsed.strftime('%Y%m%d'),objdict[field])
      claim(g,B['date-'+key+'-'+unit+'-'+field],record,entity,B[unit+'_'+field],Literal(objdict[field],datatype=XSD.string),pointer=source['file']+'#/results/'+str(i)+'/packaging/'+str(j)+'/'+field,origin='source-extracted')
   trace.append({'product_id':pid,'package_ndc':pack['package_ndc'],'source_file':source['file'],'json_pointer':'/results/'+str(i)+'/packaging/'+str(j),'record':str(record),'listing_reference':str(listing),'presentation':str(presentation),'product':str(product),'category':row['marketing_category'],'product_start':row.get('marketing_start_date'),'package_start':pack.get('marketing_start_date'),'product_end':row.get('marketing_end_date'),'package_end':pack.get('marketing_end_date')})
check('five-predeclared-strata-retrieved',len(snapshots),5)
for source,data in snapshots:
 if source['stratum']!='dated-end':
  expected={'nda':'NDA','anda':'ANDA','otc':'OTC MONOGRAPH DRUG','unapproved':'UNAPPROVED DRUG OTHER'}[source['stratum']]
  check('exact-category-after-query-'+source['stratum'],all(r['marketing_category']==expected for r in data['results']),True)
 else:check('dated-end-present',all(r.get('marketing_end_date') for r in data['results']),True)
for entry in trace:
 sub=URIRef(entry['listing_reference']);obj=URIRef(entry['presentation'])
 answer=claim_answer(g,sub,C.listingPresentation,obj)
 check('proposed-listing-query-'+entry['package_ndc'],answer['status'],'MAPPING_PROPOSED')
check('zero-world-listing-types',len(list(g.subjects(RDF.type,C.MarketListing))),0)
check('zero-world-listed-role-types',len(list(g.subjects(RDF.type,C.ListedPresentationRole))),0)
check('zero-world-listing-relations',len(list(g.triples((None,C.listingPresentation,None)))),0)
check('zero-authorizations',len(list(g.subjects(RDF.type,C.RegulatoryAuthorization))),0)
sh=validate_graph(g);check('claim-profile-shacl',sh['conforms'],True)
hr=prev.hermit(full+g);check('source-claim-graph-hermit',hr['consistent'] and not hr['unsatisfiable_named_classes'],True)
counter=g+Graph()
for item in trace:
 listing=URIRef(item['listing_reference']);presentation=URIRef(item['presentation'])
 prev.not_type(counter,listing,C.MarketListing);prev.not_edge(counter,listing,C.listingPresentation,presentation)
 prev.not_type(counter,presentation,C.ListedPresentationRole)
for record in set(g.subjects(RDF.type,C.SourceRecord)):prev.not_type(counter,record,C.RegulatoryAuthorization)
nonentail=prev.hermit(full+counter);check('all-listings-remain-source-claims-countermodel',nonentail['consistent'],True)
previous=json.loads((PREV/'sources/ndc-response.json').read_text());old={x['product_id'] for x in previous['results']}
out={'strata_retrieved':len(snapshots),'received_rows':sum(len(d['results']) for _,d in snapshots),'unique_source_product_ids':len(unique),'prior_sample_overlap':len(old&set(unique)),'new_unique_product_ids_beyond_prior':len(set(unique)-old),'package_projections':len(trace),'structured_claims':len(list(g.subjects(RDF.type,B.StructuredClaim))),'triples':len(g),'category_counts':dict(Counter(x['row']['marketing_category'] for x in unique.values())),'product_end_present':sum(bool(x['row'].get('marketing_end_date')) for x in unique.values()),'product_package_start_disagreements':sum(x['product_start']!=x['package_start'] for x in trace),'shacl':sh,'hermit':hr,'countermodel':nonentail,'checks':checks,'pass':sum(x['pass'] for x in checks),'total':len(checks),'limits':['Purposive quota sample, not random or representative. Product_id is a source identifier, not a universal identity proof.','Classifying source-referenced products/presentations is a mapping proposal. Described listings and roles are kept as claims without world-fact materialization.','These counts do not validate actual approval, establishment registration, ESMP submissions or real risk incidents.','Prior seven-package graph is unchanged; this claim-only representation is a separate proposed migration target.']}
out['claim_origin_counts']=dict(Counter(str(g.value(n,B.claimOrigin)) for n in g.subjects(RDF.type,B.StructuredClaim)))
out['limits'].append('Four interpreted propositions per package, including listing responsibility, are mapping proposals; they are not explicit NDC source fields. RG-07 remains open.')
g.serialize(H/'ndc-claims.ttl',format='turtle');write('ndc-traceability.json',trace);write('ndc-results.json',out)
print(json.dumps({k:out[k] for k in ['unique_source_product_ids','prior_sample_overlap','new_unique_product_ids_beyond_prior','package_projections','structured_claims','pass','total']}),flush=True)
assert all(x['pass'] for x in checks)
