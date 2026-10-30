"""Additive coherence experiment; topology is not semantic acceptance."""
from pathlib import Path
import json,copy,hashlib,importlib.util
from rdflib import Graph,Dataset,Namespace,URIRef,BNode,Literal,RDF,RDFS,OWL,XSD
from pyshacl import validate
H=Path(__file__).resolve().parent
PREV=H.parent/'2.1.0-alpha.1-reporting-context-lab'
s=importlib.util.spec_from_file_location('context_lab',PREV/'lab.py');ctx=importlib.util.module_from_spec(s);s.loader.exec_module(ctx)
C,L,R,SH=ctx.C,ctx.prev.L,ctx.R,ctx.SH
D=Namespace('https://w3id.org/cm-pharme/experimental/coherence/')
T=Namespace('urn:cmpe-coherence:')
OLD=H.parent/'2.1.0-alpha.1-four-domain-refinement'
BASE=H.parent/'2.1.0-alpha.1-g3-p4a-supply-capacity'
RELS=[
 ('logisticsProduct','DistributionLogisticsActivity','MedicinalProduct','GDP','4.2, 5, 9'),
 ('logisticsFacility','DistributionLogisticsActivity','Facility','GDP','3, 9'),
 ('procurementProduct','ProcurementActivity','MedicinalProduct','GDP','4.2, 5.2'),
 ('procurementOrganization','ProcurementActivity','Organization','GDP','5.2'),
 ('stockoutProduct','StockoutSituation','MedicinalProduct','WHO-STOCKOUT','draft definition framework, printed p.10'),
 ('stockoutFacility','StockoutSituation','Facility','WHO-STOCKOUT','draft definition framework, printed p.10'),
 ('requirementSource','RegulatoryRequirement','SourceRecord','PROJECT-DEFINITION','normative information object; source trace'),
 ('requirementJurisdiction','RegulatoryRequirement','RegulatoryJurisdiction','PROJECT-DEFINITION','applicability context, not legal compliance'),
 ('capabilityRealizedInLogistics','EnterpriseCapability','DistributionLogisticsActivity','GDP','7.2–7.3, 9'),
 ('supportsLogistics','ProvenanceActivity','DistributionLogisticsActivity','GDP','4.2; combined with PROV activity distinction')]
def write(name,obj):(H/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def save(name,g):(H/name).write_text(g.serialize(format='trig' if name.endswith('.trig') else 'turtle').rstrip()+'\n')
def graph():
 g=Graph()
 for k,v in [('c',C),('d',D),('l',L),('r',R),('t',T),('b',ctx.B),('sh',SH)]:g.bind(k,v)
 return g
def typ(g,n,c):g.add((n,RDF.type,c))
M=graph()
for name,source,target,_,_ in RELS:
 typ(M,D[name],OWL.ObjectProperty);M.add((D[name],RDFS.domain,C[source]));M.add((D[name],RDFS.range,C[target]))
full=ctx.full+M
S=graph();PROFILES={}
for tag,cls,fields in [
 ('logistics','DistributionLogisticsActivity',['logisticsProduct','logisticsFacility']),
 ('procurement','ProcurementActivity',['procurementProduct','procurementOrganization']),
 ('stockout','StockoutSituation',['stockoutProduct','stockoutFacility']),
 ('requirement','RegulatoryRequirement',['requirementSource','requirementJurisdiction']),
 ('capability-logistics','EnterpriseCapability',['capabilityRealizedInLogistics']),
 ('digital-logistics','ProvenanceActivity',['supportsLogistics'])]:
 shape=D[tag+'Shape'];typ(S,shape,SH.NodeShape);S.add((shape,SH['class'],C[cls]));target=BNode();S.add((shape,SH.target,target));typ(S,target,SH.SPARQLTarget);S.add((target,SH.select,Literal('SELECT ?this WHERE { ?this <'+str(D.profile)+'> "'+tag+'" . }')))
 for name in fields:
  rule=next(x for x in RELS if x[0]==name);p=BNode();S.add((shape,SH.property,p));S.add((p,SH.path,D[name]));S.add((p,SH.minCount,Literal(1)));S.add((p,SH['class'],C[rule[2]]))
 PROFILES[tag]={'class':cls,'fields':fields}
hierarchy=ctx.prev.reg.hierarchy+Graph()
for a,b in (ctx.M+ctx.prev.alignment).subject_objects(RDFS.subClassOf):hierarchy.add((a,RDFS.subClassOf,b))
shapes=ctx.prev.reg.base_shapes+ctx.prev.reg.shapes()+ctx.S+S
def admission(g):
 ok,r,_=validate(g+hierarchy,shacl_graph=shapes,advanced=True,inference='none')
 return {'conforms':bool(ok),'violations':[{'path':str(r.value(n,SH.resultPath) or ''),'component':str(r.value(n,SH.sourceConstraintComponent) or ''),'constraint':str(r.value(n,SH.sourceConstraint) or '')} for n in r.subjects(RDF.type,SH.ValidationResult)]}
def fixture(tag):
 g=graph();node=T[tag];p=PROFILES[tag];typ(g,node,C[p['class']]);g.add((node,D.profile,Literal(tag)))
 for name in p['fields']:
  rel=next(x for x in RELS if x[0]==name);obj=T[rel[2]];typ(g,obj,C[rel[2]]);g.add((node,D[name],obj))
 if tag=='capability-logistics':typ(g,T.bearer,C.Organization);g.add((node,C.capabilityBearer,T.bearer))
 return g,node
def structure(n):
 by={x['id']:x for x in n['elements']};cl={k:v for k,v in by.items() if v['type']=='Class' and v['stereotype']!='datatype'};adj={k:set() for k in cl};relations=[]
 for e in by.values():
  ends=[e['general'],e['specific']] if e['type']=='Generalization' else [by[p]['propertyType'] for p in e['properties']] if e['type']=='BinaryRelation' else []
  if len(ends)==2 and all(x in cl for x in ends):a,b=ends;adj[a].add(b);adj[b].add(a);relations.append((e['id'],a,b))
 unseen=set(cl);comps=[]
 while unseen:
  todo=[min(unseen)];seen=set()
  while todo:
   x=todo.pop()
   if x not in seen:seen.add(x);todo.extend(adj[x]-seen)
  unseen-=seen;comps.append(sorted(seen))
 ps=[e for e in by.values() if e['type']=='Property'];rels=[e for e in by.values() if e['type']=='BinaryRelation']
 return {'elements':len(by),'named_classes':len(cl),'binary_relations':len(rels),'isolates':sorted(x for x in adj if not adj[x]),'components':len(comps),'largest_component':max(map(len,comps)),'untyped_ends':sum(x['propertyType'] is None for x in ps),'unknown_cardinality_ends':sum(x['cardinality'] is None for x in ps),'unclassified_relations':sum(x['stereotype'] is None for x in rels),'adjacency':{k:sorted(v) for k,v in adj.items()},'edges':relations}
def build_native():
 original=json.loads((OLD/'ontouml-experimental.json').read_text());n=copy.deepcopy(original);es=n['elements'];by={e['id']:e for e in es};root=next(e for e in es if e['type']=='Package');relt=next(e for e in es if e['type']=='BinaryRelation');endt=next(e for e in es if e['type']=='Property')
 for name,a,b,source,loc in RELS:
  rid='coherence-rel-'+name;ids=[]
  for side,cls in [('source',a),('target',b)]:
   p=copy.deepcopy(endt);p.update(id='coherence-end-'+name+'-'+side,name={'en':name+' '+side},propertyType=cls,cardinality='0..*',subsettedProperties=[],redefinedProperties=[],description={'en':'Provisional optional participation. Required fields apply only to opted-in data profiles.'});es.append(p);ids.append(p['id'])
  rel=copy.deepcopy(relt);rel.update(id=rid,name={'en':name},properties=ids,stereotype=None,description={'en':'Source-informed proposal: '+source+' '+loc+'. Null stereotype explicitly pending scientific review.'});es.append(rel);root['contents'].append(rid)
 n['id']='cm-pharme-domain-coherence-experiment';n['name']={'en':'CM-PharmE domain coherence experiment'};n['modified']='2026-10-10'
 assert all(e==next(x for x in es if x['id']==e['id']) for e in original['elements'] if e['type']!='Package')
 write('ontouml-experimental.json',n);save('proposed-delta.ttl',M);save('proposed-shapes.ttl',S)
 snapshots={name:structure(obj) for name,obj in [('baseline',json.loads((BASE/'ontouml.json').read_text())),('prior_experiment',original),('new_experiment',n)]}
 write('topology.json',snapshots)
 write('relation-proposals.json',{'relations':[{'property':name,'source':a,'target':b,'source_id':src,'locator':loc,'proposed_native_bounds':'0..* / 0..*','stereotype':'PENDING','accepted':False,'meaning':'Design inference from source and local scope; the source does not prescribe this ontology relation.'} for name,a,b,src,loc in RELS],'new_classes':0,'new_relations':len(RELS),'baseline_unchanged':True,'old_nonpackage_elements_unchanged':True})
 return snapshots
