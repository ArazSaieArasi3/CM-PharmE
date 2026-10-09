"""Build selected-signature interface projections; NOT a locality extractor.

Build-time dependencies are repository labs. Exported module runtime is local.
Preserves complete blank-node axiom trees. Omits cross-signature axioms explicitly.
"""
from pathlib import Path
import importlib.util,json,re,shutil,hashlib
from rdflib import Graph,Dataset,URIRef,BNode,Literal,RDF,RDFS,OWL,Namespace
H=Path(__file__).resolve().parent;P=H.parent
spec=importlib.util.spec_from_file_location('coherence_lab',P/'2.1.0-alpha.1-domain-coherence-lab/lab.py');lab=importlib.util.module_from_spec(spec);spec.loader.exec_module(lab)
C,L,R,D,SH=lab.C,lab.L,lab.R,lab.D,lab.SH
G=Namespace('https://w3id.org/cm-pharme/experimental/source-group/')
lab.full+=Graph().parse(H/'pv-group-delta.ttl');lab.shapes+=Graph().parse(H/'pv-group-shapes.ttl')
OLD=P/'2.1.0-alpha.1-four-domain-lab';REF=P/'2.1.0-alpha.1-four-domain-refinement'
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def save(p,g):p.write_text(g.serialize(format='turtle'))
def tree(g,node,out):
 if any(out.triples((node,None,None))):return
 for t in g.triples((node,None,None)):
  out.add(t)
  if isinstance(t[2],BNode):tree(g,t[2],out)
  elif t[1] in (SH.property,SH.node,SH.sparql,SH.target,SH['not'],SH.qualifiedValueShape) and isinstance(t[2],URIRef):tree(g,t[2],out)
def uris(g):
 found={x for t in g for x in t if isinstance(x,URIRef)}
 prefixes={'c':C,'l':L,'r':R,'d':D,'prov':Namespace('http://www.w3.org/ns/prov#')}
 for t in g:
  if isinstance(t[2],Literal):
   s=str(t[2]);found.update(URIRef(x) for x in re.findall(r'<(https?://[^>]+)>',s))
   found.update(prefixes[a][b] for a,b in re.findall(r'\b(c|l|r|d|prov):([A-Za-z][\w-]*)',s))
 return found
def local(x):return isinstance(x,URIRef) and (str(x).startswith('https://w3id.org/cm-pharme/') or str(x).startswith('http://www.w3.org/ns/prov#'))
PROFILES={
 'RM':'risk-scenario risk-assessment risk-result risk-plan risk-treatment risk-review',
 'PV':'safety-reporting safety-signal signal-assessment signal-result pv-requirement pv-surveillance report-carrier report-claim attributed-signal-assessment source-group-scope source-group-entry',
 'BA':'ba-service ba-view ba-partnership pharma-service documented-partnership commitment-assertion capability-logistics logistics',
 'DS':'deployment digital-activity digital-record digital-service manufacturing-data-activity manufacturing-context manufacturing-digital-service digital-logistics logistics'}
EXCLUDES={
 'RM':['Patient-level clinical risk prediction','All enterprise risk categories','Plan existence implying execution or effectiveness'],
 'PV':['Patient event invention from a recommendation','Signal implying established causality','A complete ICSR/E2B implementation'],
 'BA':['Complete enterprise architecture framework','Every outsourcing agreement being a strategic partnership','Capability implying exercised capacity'],
 'DS':['Full software architecture or cybersecurity ontology','A record implying regulatory authorization','Digital activity being identical to physical manufacturing/logistics']}
ADMIT=json.loads((OLD/'shacl-results.json').read_text())['cases'];REFAD=json.loads((REF/'refinement-shacl-results.json').read_text())
Q1=json.loads((OLD/'cq-results.json').read_text());Q2=json.loads((REF/'cq-results.json').read_text())
modules=json.loads((P/'2.1.0-alpha.1-domain-coherence-lab/domain-coherence.json').read_text())['modules']
catalog=[]
for mod in modules:
 m=mod['id'];out=H/'modules'/m;out.mkdir(parents=True,exist_ok=True);(out/'fixtures').mkdir(exist_ok=True)
 profiles=PROFILES[m].split();owned={C[x] for x in mod['proposed_core_classes']};signature=set(owned);fixtures=[];queries=[]
 for origin,rows in [(OLD,ADMIT),(REF,REFAD)]:
  for case in rows:
   if not (case.get('scenario','').startswith('SC-'+m+'-') or case.get('requirement','').startswith('X-'+m+'-')):continue
   name=origin.name.split('four-domain-')[-1]+'-'+Path(case['fixture']).name;dst=out/'fixtures'/name;shutil.copyfile(origin/case['fixture'],dst)
   g=Graph().parse(dst);signature.update(x for x in uris(g) if local(x))
   fixtures.append({'id':name,'fixture':'fixtures/'+name,'expected':case['expected_conforms'],'marker':case.get('expected_marker',case.get('expected_failure_marker'))})
 for q in Q1:
  if not q['id'].startswith('CQ-'+m+'-'):continue
  number=int(q['id'][-2:]);boundary=(m,number) in [('RM',3),('PV',1),('PV',2),('DS',1),('DS',2),('DS',3)]
  queries.append({'id':q['id'],'query':q['query'],'expected':q['expected'],'fixture':f'fixtures/lab-{m}-{2 if boundary else 1}-'+('boundary' if boundary else 'positive')+'.ttl'})
 for q in Q2:
  req=q['requirement']
  if not req.startswith('X-'+m+'-'):continue
  name='boundary' if req in ['X-RM-CONTEXT','X-PV-CARRIER','X-PV-ACTOR'] else 'positive'
  queries.append({'id':req,'query':q['query'],'expected':q['expected'],'fixture':f'fixtures/refinement-{req}-{name}.ttl'})
 if m=='PV':
  ds=Dataset().parse(H/'pv-group-fixtures.trig',format='trig');group_results=json.loads((H/'pv-group-results.json').read_text())
  for case in group_results['checks']:
   if case['kind']!='admission':continue
   g=ds.graph(URIRef('urn:cmpe-group-case:'+case['id']));name='group-'+case['id']+'.ttl';save(out/'fixtures'/name,g)
   signature.update(x for x in uris(g) if local(x));fixtures.append({'id':name,'fixture':'fixtures/'+name,'expected':case['expected'],'marker':None})
  qprefix=f'PREFIX g: <{G}> PREFIX t: <urn:cmpe-group:> '
  for name,q,expected in [('group-entry-count','SELECT (COUNT(?entry) AS ?count) WHERE { t:scope g:scopeEntry ?entry }',[['28']]),('group-combination-label','SELECT ?label WHERE { t:entry-1 g:sourceLabel ?label }',[['chlormadinone/ethinylestradiol']]),('group-source-version','SELECT ?version WHERE { t:scope g:scopeVersion ?version }',[['EMA-PRAC-183502-2026-EPITT20300-footnote4']])]:queries.append({'id':name,'query':qprefix+q,'expected':expected,'fixture':'fixtures/group-complete-documentary-scope.ttl'})
 # Select profile contracts and triggered shared interface contracts to fixed point.
 shapes=Graph();roots=set();schema=Graph()
 for k,v in [('c',C),('l',L),('r',R),('d',D),('sh',SH)]:schema.bind(k,v);shapes.bind(k,v)
 changed=True
 while changed:
  before=(len(signature),len(shapes),len(schema))
  for root in lab.shapes.subjects(RDF.type,SH.NodeShape):
   sels=[str(s) for t in lab.shapes.objects(root,SH.target) for s in lab.shapes.objects(t,SH.select)]
   chosen=any('"'+tag+'"' in s for tag in profiles for s in sels)
   chosen=chosen or any(x in signature for pred in (SH.targetClass,SH.targetSubjectsOf,SH.targetObjectsOf) for x in lab.shapes.objects(root,pred))
   if chosen:roots.add(root);tree(lab.shapes,root,shapes)
  signature.update(x for x in uris(shapes) if local(x))
  for subject in list(signature):
   for t in lab.full.triples((subject,None,None)):
    _,p,o=t
    # Disjointness and equivalence to external signatures are interface omissions.
    if p in (OWL.disjointWith,OWL.equivalentClass,OWL.equivalentProperty,OWL.inverseOf) and isinstance(o,URIRef) and o not in signature:continue
    if p==OWL.imports:continue
    schema.add(t)
    if isinstance(o,BNode):tree(lab.full,o,schema)
  signature.update(x for x in uris(schema) if local(x))
  changed=before!=(len(signature),len(shapes),len(schema))
 # N-ary disjointness only when all members are in the selected signature.
 from rdflib.collection import Collection
 omitted_nary=[]
 for node in lab.full.subjects(RDF.type,OWL.AllDisjointClasses):
  head=lab.full.value(node,OWL.members);members=list(Collection(lab.full,head))
  if set(members)<=signature:tree(lab.full,node,schema)
  elif set(members)&signature:omitted_nary.append({'members':[str(x) for x in members],'reason':'cross-signature n-ary disjointness omitted'})
 omitted=[]
 for s,p,o in lab.full:
  if s in signature and (s,p,o) not in schema and not isinstance(o,BNode):omitted.append([str(s),str(p),str(o)])
 # Inbound binary disjoint axioms among included classes must also be retained.
 for s,p,o in lab.full:
  if p==OWL.disjointWith and s in signature and o in signature:schema.add((s,p,o))
 hier=Graph()
 for s,p,o in schema.triples((None,RDFS.subClassOf,None)):
  if isinstance(s,URIRef) and isinstance(o,URIRef):hier.add((s,p,o))
 ontology=URIRef('https://w3id.org/cm-pharme/experimental/modules/'+m+'/2026-10-09')
 schema.add((ontology,RDF.type,OWL.Ontology));schema.add((ontology,RDFS.comment,Literal('Bounded selected-signature interface projection. Not an approved replacement or a locality module. Dependencies flattened; no remote imports.')))
 save(out/'ontology.ttl',schema);save(out/'shapes.ttl',shapes);save(out/'hierarchy.ttl',hier)
 classes=sorted(str(x) for x in schema.subjects(RDF.type,OWL.Class) if isinstance(x,URIRef));imports=sorted(set(classes)-set(map(str,owned)))
 properties=sorted(str(x) for typ in (OWL.ObjectProperty,OWL.DatatypeProperty) for x in schema.subjects(RDF.type,typ))
 reasoncases=[{'id':m+'-schema-satisfiable','expected':True},{'id':m+'-positive-consistent','expected':True,'fixture':f'fixtures/lab-{m}-2-boundary.ttl'}]
 collision={'RM':'result-is-assessment','PV':'reporting-is-record','BA':'view-is-organization','DS':'record-is-component'}[m]
 reasoncases.append({'id':m+'-identity-collision-rejected','expected':False,'fixture':f'fixtures/lab-{m}-3-{collision}.ttl'})
 if m=='PV':
  reasoncases.append({'id':'PV-source-scope-positive','expected':True,'fixture':'fixtures/group-complete-documentary-scope.ttl'})
  g=Graph().parse(out/'fixtures/group-complete-documentary-scope.ttl');g.add((URIRef('urn:cmpe-group:scope'),RDF.type,C.SourceRecord));save(out/'fixtures/group-scope-is-source-collision.ttl',g)
  reasoncases.append({'id':'PV-source-scope-is-not-carrier','expected':False,'fixture':'fixtures/group-scope-is-source-collision.ttl'})
 contract={'module':m,'name':mod['name'],'mission_fa':mod['goal_fa'],'direction':'RETAIN_ACCEPTED_BY_USER','detailed_model_acceptance':'PENDING','owned_classes':sorted(map(str,owned)),'imported_interface_classes':imports,'profiles':profiles,'properties':properties,'excluded_scope':EXCLUDES[m],'admission_cases':fixtures,'queries':queries,'reasoner_cases':reasoncases,'limits':['Selected-signature projection; no proof of entailment preservation outside listed witnesses','Import interfaces are not counted as owned classes','SHACL profile requirements are not global OWL cardinalities','No native OntoUML module export is claimed','Source model semantic decisions, including PROV projection, remain pending']}
 if m=='PV':
  contract['source_scope_lookups']=[{k:case[k] for k in ['id','input','expected']} for case in group_results['checks'] if case['kind']=='lookup']
  for name in ['pv_group.py','pv-group-source.json']:shutil.copyfile(H/name,out/name)
 dump(out/'contract.json',contract);dump(out/'omissions.json',{'outbound_triples':sorted(omitted),'nary':omitted_nary,'omitted_shape_roots':sorted(str(x) for x in set(lab.shapes.subjects(RDF.type,SH.NodeShape))-roots)})
 shutil.copyfile(H/'runner.py',out/'runner.py')
 (out/'requirements.txt').write_text('rdflib==7.6.0\npyshacl==0.30.1\nowlready2==0.49\n')
 (out/'README.md').write_text('# '+mod['name']+' — bounded standalone module\n\n'+mod['goal_fa']+'\n\nCopy this directory anywhere. Install requirements and Java 17; run `python runner.py`. No sibling repository file or network ontology fetch is used by the runner. Inspect contract.json for ownership, imported interfaces, profiles, fixed queries and witnesses. Inspect omissions.json before relying on semantics outside those witnesses. All dependencies are flattened into ontology.ttl.\n\nRetention direction is accepted by the user. Detailed ontology acceptance remains pending. This is a selected-signature interface projection, not a formally certified locality module.\n')
 catalog.append({'id':m,'owned_class_count':len(owned),'interface_class_count':len(imports),'schema_triples':len(schema),'shape_triples':len(shapes),'admission_cases':len(fixtures),'queries':len(queries),'reasoner_cases':len(reasoncases),'omitted_outbound_triples':len(omitted)})
dump(H/'module-catalog.json',catalog)
dump(H/'direction-decision.json',{'decision':'RETAIN_AND_DEVELOP_FOUR_PURPOSEFUL_MINIMUM_VIABLE_ONTOLOGIES','accepted_by':'user','source':'current conversation instruction','replaces':'HOLD on removal or transfer','scope':'retention/design direction only','not_accepted_by_this_decision':['all relation proposals','all stereotypes/cardinalities','PROV projection','release/merge'],'execution_owner':'assistant','scientific_review_owner':'Araz'})
print(json.dumps(catalog),flush=True)
