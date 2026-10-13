"""Frozen source-scoped pharmaceutical adapter; no synthetic substitution."""
from pathlib import Path
import csv, hashlib, json, sqlite3
from rdflib import Graph, Namespace, URIRef, RDF, RDFS, OWL
from pyshacl import validate
R=Path(__file__).resolve().parent
I=R/'inputs/cm-pharme/v2/ontology/candidates'
C=Namespace('https://w3id.org/cm-pharme/2.1/')
Q=Namespace('https://w3id.org/cm-pharme/experimental/prov-target/')
P=Namespace('https://w3id.org/cm-pharme/experimental/registry-policy/')
PROV=Namespace('http://www.w3.org/ns/prov#')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):
 p=R/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def nt(g): return '\n'.join(sorted(g.serialize(format='nt').splitlines()))+'\n'
def csvwrite(p,rows):
 with (R/p).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def build():
 policy=json.loads((R/'source-policy.json').read_text())
 raw=I/'2.1.0-alpha.1-prov-target-lab/sources/ndc-response.json'
 assert sha(raw)==policy['raw_source_sha256']
 data=json.loads(raw.read_text());source=json.loads((raw.parent/'ndc-source.json').read_text())
 graph=Graph().parse(I/'2.1.0-alpha.1-prov-target-lab/ndc-abox.ttl')
 ontology=Graph().parse(I/'2.1.0-alpha.1-candidate/active.ttl')
 contract=json.loads((I/'2.1.0-alpha.1-candidate/contract.json').read_text())
 concepts=json.loads((I/'2.1.0-alpha.1-candidate/conceptual-model.json').read_text())['concepts']
 stereotype={x['iri']:x['stereotype'] for x in concepts}
 trace=json.loads((I/'2.1.0-alpha.1-prov-target-lab/ndc-traceability.json').read_text())
 schema=Graph().parse(I/'2.1.0-alpha.1-candidate/constraints.ttl')
 conforms,report,report_text=validate(graph,shacl_graph=schema,advanced=True,inference='none')
 assert conforms,report_text
 (R/'results/native-shacl.txt').write_text(report_text)
 products=[]
 for i,row in enumerate(data['results']):
  pid=str(Q['source-product-'+row['product_ndc']]);org=str(Q['source-labeler-row-'+str(i)])
  packages=[]
  for j,pack in enumerate(row.get('packaging',[])):
   t=next(x for x in trace if x['row']==i and x['package_index']==j)
   record=URIRef(t['record']);listing=graph.value(record,P.representsFact)
   presentation=graph.value(listing,C.listingPresentation)
   assert (presentation,C.presentationOf,URIRef(pid)) in graph
   assert (listing,C.listingResponsibleOrganization,URIRef(org)) in graph
   assert graph.value(record,Q.jsonPointer)==__import__('rdflib').Literal(t['json_pointer'])
   packages.append({'id':str(presentation),'ndc':pack['package_ndc'],'description':pack['description'],
    'listing':str(listing),'source_record':str(record),'source_pointer':t['json_pointer'],
    'package_marketing_start':pack.get('marketing_start_date'),'package_marketing_end':pack.get('marketing_end_date'),
    'approval_status':'UNKNOWN','relationship_status':'SOURCE_REPORTED_LISTING',
    'source_envelope':pack})
  products.append({'id':pid,'ndc':row['product_ndc'],'name':row.get('brand_name') or row['generic_name'],
   'generic_name':row['generic_name'],'organization_id':org,'organization_name':row['labeler_name'],
   'organization_type':str(C.Organization),'organization_role':str(C.ListingResponsibleOrganizationRole),
   'organization_stereotype':stereotype[str(C.ListingResponsibleOrganizationRole)],
   'source_pointer':'/results/'+str(i),'source_envelope':row,'packages':packages,
   'product_marketing_start':row.get('marketing_start_date'),'manufacturer_status':'NOT_ESTABLISHED',
   'distributor_status':'NOT_ESTABLISHED','approval_status':'UNKNOWN'})
 logical=Graph();excluded=Graph()
 declared_classes=set(ontology.subjects(RDF.type,OWL.Class));declared_props=set(ontology.subjects(RDF.type,OWL.ObjectProperty))|set(ontology.subjects(RDF.type,OWL.DatatypeProperty))
 for s,p,o in graph:
  (logical if (p==RDF.type and o in declared_classes) or p in declared_props else excluded).add((s,p,o))
 for name,g in [('case',graph),('native-logical-population',logical),('retained-source-metadata',excluded)]:
  (R/'generated'/f'{name}.nt').write_text(nt(g))
 # Lossless local application index. Domain semantics are defined by the pinned RDF,
 # not by these read-model table names; no new ontology concepts are introduced.
 db=R/'generated/explorer.sqlite';db.unlink(missing_ok=True);conn=sqlite3.connect(db);conn.execute('PRAGMA foreign_keys=ON')
 conn.executescript('''CREATE TABLE triple(s TEXT NOT NULL,p TEXT NOT NULL,o TEXT NOT NULL,PRIMARY KEY(s,p,o));
 CREATE TABLE medicine(id TEXT PRIMARY KEY,ndc TEXT NOT NULL,name TEXT NOT NULL,source_pointer TEXT NOT NULL);
 CREATE TABLE organization_context(id TEXT PRIMARY KEY,name TEXT NOT NULL,role TEXT NOT NULL);
 CREATE TABLE listing(id TEXT PRIMARY KEY,medicine_id TEXT NOT NULL REFERENCES medicine(id),organization_id TEXT NOT NULL REFERENCES organization_context(id),presentation_id TEXT NOT NULL UNIQUE,source_record TEXT NOT NULL,source_pointer TEXT NOT NULL,approval_status TEXT CHECK(approval_status='UNKNOWN'));
 ''')
 conn.executemany('INSERT INTO triple VALUES(?,?,?)',[(s.n3(),p.n3(),o.n3()) for s,p,o in graph])
 for prod in products:
  conn.execute('INSERT INTO medicine VALUES(?,?,?,?)',(prod['id'],prod['ndc'],prod['name'],prod['source_pointer']))
  conn.execute('INSERT INTO organization_context VALUES(?,?,?)',(prod['organization_id'],prod['organization_name'],prod['organization_role']))
  for pack in prod['packages']:conn.execute('INSERT INTO listing VALUES(?,?,?,?,?,?,?)',(pack['listing'],prod['id'],prod['organization_id'],pack['id'],pack['source_record'],pack['source_pointer'],'UNKNOWN'))
 conn.commit();assert not conn.execute('PRAGMA foreign_key_check').fetchall()
 exported=Graph().parse(data='\n'.join(' '.join(x)+' .' for x in conn.execute('SELECT s,p,o FROM triple')),format='nt')
 from rdflib.compare import isomorphic
 assert isomorphic(graph,exported)
 sql_rows=conn.execute('SELECT m.id,l.presentation_id,l.id,l.organization_id,l.source_record FROM listing l JOIN medicine m ON m.id=l.medicine_id ORDER BY l.id').fetchall()
 rdf_rows=sorted(tuple(map(str,x)) for x in graph.query('SELECT ?m ?p ?l ?o ?s WHERE { ?p <'+str(C.presentationOf)+'> ?m . ?l <'+str(C.listingPresentation)+'> ?p ; <'+str(C.listingResponsibleOrganization)+'> ?o . ?s <'+str(P.representsFact)+'> ?l . }'))
 assert sorted(sql_rows)==rdf_rows
 conn.close()
 policy.update({'cm_model_sha256':sha(I/'2.1.0-alpha.1-candidate/active.ttl'),
  'cm_native_sha256':sha(I/'2.1.0-alpha.1-candidate/ontouml.json'),
  'source_graph_sha256':sha(I/'2.1.0-alpha.1-prov-target-lab/ndc-abox.ttl'),
  'generated_graph_sha256':sha(R/'generated/case.nt')})
 payload={'schema_version':'0.12.0','policy':policy,'source_meta':data['meta'],'products':products,
  'native_market_listing_contract':contract['profiles']['MarketListing'],
  'statistics':{'source_rows':len(products),'package_projections':sum(len(p['packages']) for p in products),
  'organization_contexts':len(products),'typed_graph_subjects':len(set(graph.subjects(RDF.type,None))),
  'rdf_triples':len(graph),'native_logical_triples':len(logical),'retained_metadata_triples':len(excluded)},
  'graph':[[str(s),str(p),str(o),isinstance(o,__import__('rdflib').Literal)] for s,p,o in sorted(graph,key=lambda t:tuple(map(str,t)))]}
 write('generated/explorer-data.json',payload)
 decisions=[
 {'mapping_id':'XM01','conceptual_need':'Medicine entity','requirement':'FR-01','class_iris':str(C.MedicinalProduct)+';'+str(C.MedicinalProductPresentation),'relation_iris':str(C.presentationOf),'status':'IMPLEMENTED_SOURCE_SCOPED','decision':'Product and package references remain distinct; local NDC scope; no cross-source identity claim.','remaining':'Author/domain acceptance'},
 {'mapping_id':'XM02','conceptual_need':'Organization entity','requirement':'FR-01','class_iris':str(C.Organization)+';'+str(C.ListingResponsibleOrganizationRole),'relation_iris':'','status':'IMPLEMENTED_SOURCE_SCOPED','decision':'Keep row-scoped labeler references and listing role; do not merge by name or infer ManufacturerRole/WholesaleDistributorRole.','remaining':'Author/domain acceptance; external entity resolution'},
 {'mapping_id':'XM03','conceptual_need':'Medicine-to-organization relationship','requirement':'FR-01','class_iris':str(C.MarketListing),'relation_iris':' ; '.join(map(str,[C.presentationOf,C.listingPresentation,C.listingResponsibleOrganization])),'status':'PARTIAL_MANUFACTURER_DISTRIBUTOR_UNRESOLVED','decision':'Use source-reported listing chain via MarketListing relator. No unsupported manufactures/distributes predicate or world-fact verification.','remaining':'Identify authoritative manufacturer/distributor evidence and exact applicable CM pattern; preserve original FR-01'},
 {'mapping_id':'XM04','conceptual_need':'Claim evidence and provenance','requirement':'FR-02','class_iris':str(C.SourceRecord)+';'+str(C.DatasetRelease)+';'+str(C.Dataset),'relation_iris':str(C.containsSourceRecord)+';'+str(PROV.wasDerivedFrom),'status':'IMPLEMENTED_SOURCE_SCOPED','decision':'Reuse upstream source-record graph and exact JSON pointers. Experimental profile terms/PROV assertions are explicit adapter metadata, not newly approved native Product terms.','remaining':'Author/domain acceptance; stronger claim-to-world validation'},
 {'mapping_id':'XM05','conceptual_need':'Versioned research brief','requirement':'FR-03','class_iris':'','relation_iris':'','status':'IMPLEMENTED_APPLICATION_CONTRACT','decision':'Export versioned JSON brief with CM commit, model hash, source hash, product/organization/package references, pointers and explicit unknowns. Application schema, not new domain class.','remaining':'Independent user acceptance'}]
 csvwrite('External_Mapping_Decisions_v0_12_0.csv',decisions)
 write('results/Integration_Summary_v0_12_0.json',{'version':'0.12.0','statistics':payload['statistics'],'native_shacl_conforms':bool(conforms),'sql_rdf_tuple_agreement':len(sql_rows),'rdf_roundtrip_isomorphic':True,'mappings_reviewed':5,'mapping_contracts_implemented':4,'mapping_partial':1,'author_acceptance':'PENDING','effectiveness_user_study':'NOT_EXECUTED','new_product_ontology_concepts':0})
 print(json.dumps(payload['statistics']))
 return payload
if __name__=='__main__':build()
