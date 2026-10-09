"""Reproducible documentary group-scope proposal and boundary tests."""
from pathlib import Path
import importlib.util,json,copy
from rdflib import Graph,Namespace,URIRef,Literal,BNode,RDF,RDFS,OWL,XSD,Dataset
from pyshacl import validate
from pv_group import lookup
H=Path(__file__).resolve().parent;P=H.parent
s=importlib.util.spec_from_file_location('coh',P/'2.1.0-alpha.1-domain-coherence-lab/lab.py');coh=importlib.util.module_from_spec(s);s.loader.exec_module(coh)
C,L,B,SH=coh.C,coh.L,coh.ctx.B,coh.SH
G=Namespace('https://w3id.org/cm-pharme/experimental/source-group/');T=Namespace('urn:cmpe-group:')
LABELS='''chlormadinone/ethinylestradiol
cyproterone acetate/estradiol valerate
cyproterone/ethinylestradiol
dienogest
dienogest/estradiol
dienogest/ethinylestradiol
drospirenone
drospirenone/estetrol
drospirenone/estradiol
drospirenone/ethinylestradiol
dydrogesterone
dydrogesterone/estradiol
estradiol/levonorgestrel
estradiol/norethisterone
estradiol/progesterone
estradiol valerate/norgestrel
ethinylestradiol/gestodene
ethinylestradiol/levonorgestrel
ethinylestradiol/norelgestromin
ethinylestradiol/norethisterone
ethinylestradiol/norgestimate
levonorgestrel
lynestrenol
medroxyprogesterone <100 mg oral formulations
megestrol
nomegestrol acetate/estradiol
norethisterone
progesterone'''.splitlines()
def dump(name,x):(H/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def save(name,g):(H/name).write_text(g.serialize(format='turtle'))
source=json.loads((P/'2.1.0-alpha.1-domain-coherence-lab/source-manifest.json').read_text())
entries=[{'ordinal':i,'source_label':label,'origin':'source-extracted','proposed_label_kind':'qualified-label' if '<' in label else 'combination-label' if '/' in label else 'unqualified-name'} for i,label in enumerate(LABELS,1)]
data={'scope_version':'EMA-PRAC-183502-2026-EPITT20300-footnote4','group_label':'Progestogens','epitt':'20300','source':source,'locator':'printed page 6, footnote 4','fresh_verification':'Official PDF text reopened successfully after an earlier HTTP 429; footnote read in this execution. Prior byte hash retained, not recomputed.','entries':entries,'extraction_complete_for_footnote':True,'chemical_universe_complete':False,'normalization':'case and whitespace only; no component, synonym or combination-order closure','limits':['Label-kind parsing and amount/route interpretation are proposed mappings','No brand, patient event, causal assertion, authorization or clinical advice generated','No-action-at-this-stage is not no-risk','Document header date was labelled expected publication date; independent publication-date verification remains separate']}
dump('pv-group-source.json',data)
g=Graph();delta=Graph();shapes=Graph()
for gr in [g,delta,shapes]:
 for prefix,ns in [('c',C),('g',G),('b',B),('sh',SH),('t',T)]:gr.bind(prefix,ns)
# Information profiles reuse Assertion; no invented single chemical substance.
for prop,target in [('scopeEntry',C.Assertion),('scopeSource',C.SourceRecord),('entrySource',C.SourceRecord)]:
 delta.add((G[prop],RDF.type,OWL.ObjectProperty));delta.add((G[prop],RDFS.domain,C.Assertion));delta.add((G[prop],RDFS.range,target))
# The description/entry is not its documentary carrier. Restrict only this
# proposed vocabulary; do not change the global Assertion class definition.
not_carrier=BNode();delta.add((not_carrier,RDF.type,OWL.Class));delta.add((not_carrier,OWL.complementOf,C.SourceRecord))
for prop in [G.scopeSource,G.entrySource]:delta.add((prop,RDFS.domain,not_carrier))
for prop,dt in [('scopeVersion',XSD.string),('sourceLabel',XSD.string),('entryOrdinal',XSD.integer),('evidencePointer',XSD.string),('labelKindProposal',XSD.string)]:
 delta.add((G[prop],RDF.type,OWL.DatatypeProperty));delta.add((G[prop],RDFS.domain,C.Assertion));delta.add((G[prop],RDFS.range,dt))
def shape(tag,fields):
 root=G[tag+'Shape'];shapes.add((root,RDF.type,SH.NodeShape));shapes.add((root,SH['class'],C.Assertion));target=BNode();shapes.add((root,SH.target,target));shapes.add((target,RDF.type,SH.SPARQLTarget));shapes.add((target,SH.select,Literal('SELECT ?this WHERE { ?this <'+str(G.profile)+'> "'+tag+'" }')))
 for prop,cls,dt,maximum in fields:
  n=BNode();shapes.add((root,SH.property,n));shapes.add((n,SH.path,G[prop]));shapes.add((n,SH.minCount,Literal(1)))
  if maximum:shapes.add((n,SH.maxCount,Literal(maximum)))
  if cls:shapes.add((n,SH['class'],cls))
  if dt:shapes.add((n,SH.datatype,dt))
  if dt==XSD.string:shapes.add((n,SH.minLength,Literal(1)))
 forbidden=BNode();shapes.add((root,SH['not'],forbidden));shapes.add((forbidden,SH['class'],C.SourceRecord))
 return root
scopeShape=shape('source-group-scope',[('scopeEntry',C.Assertion,None,None),('scopeSource',C.SourceRecord,None,1),('scopeVersion',None,XSD.string,1),('sourceLabel',None,XSD.string,1)])
entryShape=shape('source-group-entry',[('entrySource',C.SourceRecord,None,1),('scopeVersion',None,XSD.string,1),('sourceLabel',None,XSD.string,1),('entryOrdinal',None,XSD.integer,1),('evidencePointer',None,XSD.string,1),('labelKindProposal',None,XSD.string,1)])
# Validate nested entries even if a producer forgets their opt-in tag.
for p in shapes.objects(scopeShape,SH.property):
 if shapes.value(p,SH.path)==G.scopeEntry:shapes.add((p,SH.node,entryShape))
constraint=BNode();shapes.add((scopeShape,SH.sparql,constraint));shapes.add((constraint,SH.message,Literal('Scope entries must share source/version and distinct positive ordinal.')))
shapes.add((constraint,SH.select,Literal(f'''SELECT $this WHERE {{
 $this <{G.scopeEntry}> ?e ; <{G.scopeSource}> ?src ; <{G.scopeVersion}> ?v .
 ?e <{G.entrySource}> ?es ; <{G.scopeVersion}> ?ev ; <{G.entryOrdinal}> ?n .
 FILTER (?src != ?es || ?v != ?ev || ?n < 1 || EXISTS {{ $this <{G.scopeEntry}> ?other . ?other <{G.entryOrdinal}> ?n . FILTER (?other != ?e) }}) }}''')))
g.add((T.scope,RDF.type,C.Assertion));g.add((T.scope,G.profile,Literal('source-group-scope')));g.add((T.scope,G.scopeVersion,Literal(data['scope_version'])));g.add((T.scope,G.sourceLabel,Literal('Progestogens')));g.add((T.scope,G.scopeSource,T.document));g.add((T.document,RDF.type,C.SourceRecord))
g.add((T.document,B.sourceURL,Literal(source['url'],datatype=XSD.anyURI)));g.add((T.document,B.sourceSHA256,Literal(source['sha256'])))
for row in entries:
 e=T['entry-'+str(row['ordinal'])];g.add((T.scope,G.scopeEntry,e));g.add((e,RDF.type,C.Assertion));g.add((e,G.profile,Literal('source-group-entry')))
 for prop,value in [('sourceLabel',row['source_label']),('scopeVersion',data['scope_version']),('evidencePointer','EMA/PRAC/183502/2026#page=6&footnote=4'),('labelKindProposal',row['proposed_label_kind'])]:g.add((e,G[prop],Literal(value)))
 g.add((e,G.entryOrdinal,Literal(row['ordinal'])));g.add((e,G.entrySource,T.document))
 # All classifications are lexical proposals, not chemical equivalence assertions.
coh.ctx.claim(g,T.scopeMapping,coh.T['PRAC-row-20300'],coh.T['PRAC-signal-20300'],G.signalScope,T.scope,origin='mapping-interpretation',pointer='EMA/PRAC/183502/2026#page=6&footnote=4')
g.add((coh.T['PRAC-row-20300'],RDF.type,C.SourceRecord));g.add((coh.T['PRAC-signal-20300'],RDF.type,C.Assertion))
save('pv-group-data.ttl',g);save('pv-group-delta.ttl',delta);save('pv-group-shapes.ttl',shapes)
checks=[];fixtures=Dataset()
def admission(name,fixture,expected):
 ok,report,_=validate(fixture+coh.hierarchy,shacl_graph=coh.shapes+shapes,advanced=True,inference='none');fixtures.graph(URIRef('urn:cmpe-group-case:'+name)).__iadd__(fixture)
 checks.append({'id':name,'kind':'admission','expected':expected,'actual':bool(ok),'pass':bool(ok)==expected})
admission('complete-documentary-scope',g,True)
for name,mutation in [
 ('missing-source',lambda z:z.remove((T.scope,G.scopeSource,None))),
 ('scope-is-source-carrier',lambda z:z.add((T.scope,RDF.type,C.SourceRecord))),
 ('entry-is-source-carrier',lambda z:z.add((T['entry-1'],RDF.type,C.SourceRecord))),
 ('missing-label',lambda z:z.remove((T['entry-1'],G.sourceLabel,None))),
 ('missing-pointer',lambda z:z.remove((T['entry-1'],G.evidencePointer,None))),
 ('wrong-version',lambda z:(z.remove((T['entry-1'],G.scopeVersion,None)),z.add((T['entry-1'],G.scopeVersion,Literal('other-version'))))),
 ('duplicate-ordinal',lambda z:(z.remove((T['entry-2'],G.entryOrdinal,None)),z.add((T['entry-2'],G.entryOrdinal,Literal(1))))),
 ('entry-as-untyped-resource',lambda z:z.remove((T['entry-1'],RDF.type,C.Assertion))),
 ('wrong-source',lambda z:(z.add((T.other,RDF.type,C.SourceRecord)),z.remove((T['entry-1'],G.entrySource,None)),z.add((T['entry-1'],G.entrySource,T.other)))),
 ('nested-entry-without-label-or-profile',lambda z:(z.remove((T['entry-1'],G.sourceLabel,None)),z.remove((T['entry-1'],G.profile,None))))]:
 z=g+Graph();mutation(z);admission(name,z,False)
fixtures.serialize(H/'pv-group-fixtures.trig',format='trig')
version=data['scope_version'];cases=[
 ('exact-unqualified-label',{'label':'dienogest'},'SOURCE_LABEL_LISTED'),
 ('combination-as-listed',{'label':'dienogest/estradiol'},'SOURCE_LABEL_LISTED'),
 ('no-component-propagation',{'label':'ethinylestradiol'},'NOT_LISTED_IN_EXTRACTED_SCOPE_UNKNOWN_CHEMICAL_MEMBERSHIP'),
 ('no-reordered-combination-equivalence',{'label':'ethinylestradiol/chlormadinone'},'NOT_LISTED_IN_EXTRACTED_SCOPE_UNKNOWN_CHEMICAL_MEMBERSHIP'),
 ('no-dose-assumption',{'label':'medroxyprogesterone'},'UNKNOWN_QUALIFIERS'),
 ('source-version-mismatch',{'label':'dienogest','version':'later'},'UNKNOWN_SOURCE_VERSION'),
 ('case-only-normalization',{'label':' DIENOGEST '},'SOURCE_LABEL_LISTED')]
for value,expected in [(99,'QUALIFIER_MATCH_UNDER_PROPOSED_MAPPING'),(100,'OUTSIDE_THIS_ENTRY_UNDER_PROPOSED_MAPPING'),(101,'OUTSIDE_THIS_ENTRY_UNDER_PROPOSED_MAPPING'),(-1,'INVALID_INPUT'),('NaN','INVALID_INPUT')]:
 cases.append(('amount-'+str(value),dict(label='medroxyprogesterone',amount=value,unit='mg',route='oral',basis='source-formulation-amount'),expected))
for change,expected in [({'unit':'g'},'UNKNOWN_UNSUPPORTED_UNIT'),({'route':'injection'},'OUTSIDE_THIS_ENTRY_UNDER_PROPOSED_MAPPING'),({'basis':'daily-dose'},'UNKNOWN_AMOUNT_BASIS')]:
 args=dict(label='medroxyprogesterone',amount=50,unit='mg',route='oral',basis='source-formulation-amount');args.update(change);cases.append(('qualifier-'+str(change),args,expected))
for name,args,expected in cases:
 args=dict(version=version,**args) if 'version' not in args else args
 actual=lookup(data,**args);checks.append({'id':name,'kind':'lookup','input':args,'expected':expected,'actual':actual,'pass':actual==expected})
for name,actual,expected in [('entry-count',len(entries),28),('unique-source-labels',len(set(LABELS)),28),('group-not-chemical',len(list(g.subjects(RDF.type,C.PharmaceuticalSubstance))),0),('scope-link-mapping-only',coh.ctx.claim_answer(g,coh.T['PRAC-signal-20300'],G.signalScope,T.scope)['status'],'MAPPING_PROPOSED')]:checks.append({'id':name,'kind':'integrity','actual':actual,'expected':expected,'pass':actual==expected})
positive=coh.full+delta+g+Graph().parse(P/'2.1.0-alpha.1-domain-coherence-lab/prac-claims.ttl')
hr=coh.ctx.prev.hermit(positive);checks.append({'id':'group-integrated-consistency','kind':'reasoner',**hr,'pass':hr['consistent'] and not hr['unsatisfiable_named_classes']})
z=positive+Graph();coh.ctx.prev.not_type(z,T.scope,C.PharmaceuticalSubstance);coh.ctx.prev.not_edge(z,coh.T['PRAC-signal-20300'],G.signalScope,T.scope)
hr=coh.ctx.prev.hermit(z);checks.append({'id':'group-not-substance-and-no-materialized-link-countermodel','kind':'reasoner',**hr,'pass':hr['consistent'] and not hr['unsatisfiable_named_classes']})
dump('pv-group-results.json',{'checks':checks,'passed':sum(x['pass'] for x in checks),'total':len(checks),'scope_entries':28,'new_native_classes':0,'new_native_relations':0,'status':'INFORMATION_PROFILE_PROPOSAL_PENDING_SEMANTIC_REVIEW'})
print(json.dumps({'passed':sum(x['pass'] for x in checks),'total':len(checks)}),flush=True)
assert all(x['pass'] for x in checks)
