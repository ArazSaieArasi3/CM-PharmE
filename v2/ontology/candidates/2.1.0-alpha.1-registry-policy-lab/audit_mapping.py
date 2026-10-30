"""Inventory actual reuse and remaining native gaps without inventing alignments."""
import base64,gzip,hashlib,json
from collections import Counter
from lab import *
native_path=OLD/'ontouml-experimental.json';native=json.loads(native_path.read_text());index={e['id']:e for e in native['elements']}
results=json.loads((H/'shacl-results.json').read_text())['cases']
positive=graph()
for row in results:
 if row['expected_conforms'] and row['actual_conforms']:positive+=Graph().parse(H/row['fixture'])
predicates=[]
for p in sorted(set(positive.predicates()),key=str):
 if p in [RDF.type,OWL.differentFrom,OWL.sameAs]:continue
 native_ids=[]
 for prefix,start in [(C,'rel-'),(L,'lab-rel-'),(R,'refine-rel-')]:
  if str(p).startswith(str(prefix)):
   candidate=start+str(p)[len(str(prefix)):]
   if candidate in index:native_ids.append(candidate)
 category='EXISTING_NATIVE_RELATION' if native_ids else 'EXPERIMENTAL_PROFILE_FIELD' if str(p).startswith(str(P)) else 'EXTERNAL_PROV_WITHOUT_FORMAL_ALIGNMENT' if str(p).startswith(str(PROV)) else 'EXISTING_RDF_FIELD_NATIVE_MAPPING_UNVERIFIED'
 predicates.append({'iri':str(p),'category':category,'native_relation_ids':native_ids,
  'owl_declared_object_property':(p,RDF.type,OWL.ObjectProperty) in ontology,
  'owl_declared_datatype_property':(p,RDF.type,OWL.DatatypeProperty) in ontology,
  'native_acceptance':False})
observed_classes=sorted({str(t) for t in positive.objects(None,RDF.type) if str(t).startswith(str(C))})
sources=[]
for folder,filename in [(H.parent/'2.1.0-alpha.1-four-domain-lab','shacl-results.json'),(OLD,'refinement-shacl-results.json'),(POLICY,'shacl-results.json')]:
 data=json.loads((folder/filename).read_text());rows=data['cases'] if isinstance(data,dict) else data
 for row in rows:
  if row['expected_conforms']:sources.append((folder.name+'/'+row['fixture'],Graph().parse(folder/row['fixture'])))
for row in results:
 if row['expected_conforms']:sources.append((H.name+'/'+row['fixture'],Graph().parse(H/row['fixture'])))
encoded=H.parent/'2.1.0-alpha.1-g3-3-d-real-source-migration/real-source-abox.nt.gz.b64'
raw=gzip.decompress(base64.b64decode(encoded.read_text()));real=Graph().parse(data=raw.decode(),format='nt');sources.append(('prior-real-source-768-rows',real))
parents=[]
for name in ['disruptionAffects','observationResultAbout','riskAssessmentConcerns']:
 p=C[name];r=index['rel-'+name];ends=[index[x] for x in r['properties']]
 children=list(ontology.subjects(RDFS.subPropertyOf,p));observations=[]
 for source,g in sources:
  for predicate in [p]+children:
   triples=list(g.subject_objects(predicate))
   if triples:observations.append({'source':source,'predicate':str(predicate),'triple_count':len(triples),
    'explicit_target_types':dict(Counter(str(t) for _,target in triples for t in g.objects(target,RDF.type)))})
 parents.append({'relation':name,'native_ends':[{'id':e['id'],'type':e.get('propertyType'),'cardinality':e.get('cardinality')} for e in ends],
  'owl_ranges':[str(x) for x in ontology.objects(p,RDFS.range)],'declared_children':[str(x) for x in children],
  'observations':observations,'observation_count':sum(x['triple_count'] for x in observations),
  'sufficient_to_freeze_universal_target_range':False,
  'next_decision':'Establish intended subject universe from independent requirements; positive fixture types alone cannot justify a complete union or a new generic native Entity.'})
write('mapping-audit.json',{'native_source_sha256':hashlib.sha256(native_path.read_bytes()).hexdigest(),
 'native_file_modified':False,'new_native_classes':0,'new_native_relations':0,'new_owl_disjointness_proposals':2,
 'positive_fixture_classes':observed_classes,'predicate_inventory':predicates,'predicate_categories':dict(Counter(r['category'] for r in predicates)),
 'broad_parent_usage_audit':parents,'positive_fixture_graphs_examined':len(sources)-1,'prior_real_graph':{'rows':768,'triples':len(real),'sha256':hashlib.sha256(raw).hexdigest(),'new_profile_empirical_validation':False},
 'remaining_native_isolates_unchanged':['DistributionLogisticsActivity','ProcurementActivity','RegulatoryRequirement','StockoutSituation'],
 'scope_limit':'Occurrence counts include repeated scenario witnesses and are not counts of unique empirical entities. Profile and external predicates are not newly accepted native domain relations.'})
print(json.dumps({'native_relations_reused':sum(bool(r['native_relation_ids']) for r in predicates),'predicate_categories':dict(Counter(r['category'] for r in predicates)),'positive_graphs':len(sources)-1,'broad_parents':[{'name':p['relation'],'witness_triples':p['observation_count']} for p in parents]}))
