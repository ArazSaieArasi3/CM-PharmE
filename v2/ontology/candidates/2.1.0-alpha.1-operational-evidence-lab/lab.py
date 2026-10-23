"""Qualified documentary evidence adapter; never materializes described facts."""
from pathlib import Path
import json,importlib.util,re,calendar
from datetime import date
from rdflib import Graph,Dataset,Namespace,URIRef,Literal,BNode,RDF,RDFS,OWL,XSD
from rdflib.collection import Collection
from pyshacl import validate
H=Path(__file__).resolve().parent;P=H.parent
s=importlib.util.spec_from_file_location('coherence_lab',P/'2.1.0-alpha.1-domain-coherence-lab/lab.py');coh=importlib.util.module_from_spec(s);s.loader.exec_module(coh)
C,L,R,B,SH=coh.C,coh.L,coh.R,coh.ctx.B,coh.SH
E=Namespace('https://w3id.org/cm-pharme/experimental/documentary-evidence/');T=Namespace('urn:cmpe-evidence:')
MODES=['reported-occurrence','planned','required','reported-capability','assessment-content','authorization-report','mapping-proposal']
def dump(name,x):(H/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def graph():
 g=Graph()
 for p,n in [('c',C),('l',L),('r',R),('b',B),('e',E),('t',T),('sh',SH)]:g.bind(p,n)
 return g
def save(name,g):(H/name).write_text(g.serialize(format='trig' if name.endswith('.trig') else 'turtle').rstrip()+'\n')
M=graph()
for p in ['claimMode','timeLexical','timePrecision','timeRole','timeQualifier']:
 M.add((E[p],RDF.type,OWL.DatatypeProperty));M.add((E[p],RDFS.domain,B.StructuredClaim));M.add((E[p],RDFS.range,XSD.string))
for p in ['sourceID','sourceDate','sourceDateKind']:
 M.add((E[p],RDF.type,OWL.DatatypeProperty));M.add((E[p],RDFS.domain,C.SourceRecord));M.add((E[p],RDFS.range,XSD.string))
S=graph();root=E.DocumentaryClaimShape;S.add((root,RDF.type,SH.NodeShape));S.add((root,SH.targetSubjectsOf,E.claimMode));S.add((root,SH['class'],B.StructuredClaim))
S.add((root,SH.targetSubjectsOf,E.profile));forbidden=BNode();S.add((root,SH['not'],forbidden));S.add((forbidden,SH['class'],C.SourceRecord))
def field(prop,choices=None):
 n=BNode();S.add((root,SH.property,n));S.add((n,SH.path,E[prop]));S.add((n,SH.minCount,Literal(1)));S.add((n,SH.maxCount,Literal(1)));S.add((n,SH.datatype,XSD.string))
 if choices:h=BNode();Collection(S,h,[Literal(x) for x in choices]);S.add((n,SH['in'],h))
field('claimMode',MODES);field('timeLexical');field('timePrecision',['day','month','year','unspecified']);field('timeRole',['event-date','event-upper-bound','planned-window','assessment-period','not-established'])
q=BNode();S.add((root,SH.sparql,q));S.add((q,SH.message,Literal('Mapping mode and origin must agree; every witness needs exactly one source ID.')))
S.add((q,SH.select,Literal(f'''PREFIX b: <{B}> PREFIX e: <{E}> PREFIX r: <{R}>
SELECT $this WHERE {{ $this e:claimMode ?m ; b:claimOrigin ?o .
 FILTER ((?m = "mapping-proposal" && ?o != "mapping-interpretation") || (?m != "mapping-proposal" && ?o != "source-extracted") || NOT EXISTS {{ ?src r:carrierClaim $this ; e:sourceID ?id }}) }}''')))
def time_interval(value,precision):
 """Inclusive date bounds retain precision; never invent a midnight instant."""
 if precision=='unspecified':return None if value=='UNKNOWN' else 'INVALID'
 try:
  if precision=='day' and re.fullmatch(r'\d{4}-\d{2}-\d{2}',value):d=date.fromisoformat(value);return (d,d)
  if precision=='month' and re.fullmatch(r'\d{4}-\d{2}',value):y,m=map(int,value.split('-'));return (date(y,m,1),date(y,m,calendar.monthrange(y,m)[1]))
  if precision=='year' and re.fullmatch(r'\d{4}',value):y=int(value);return (date(y,1,1),date(y,12,31))
 except ValueError:return 'INVALID'
 return 'INVALID'
def admission(g):
 ok,report,_=validate(g+coh.hierarchy,shacl_graph=coh.shapes+S,advanced=True,inference='none');bad=[]
 for n in g.subjects(E.claimMode,None):
  lexical=str(g.value(n,E.timeLexical) or '');precision=str(g.value(n,E.timePrecision) or '');role=str(g.value(n,E.timeRole) or '')
  if time_interval(lexical,precision)=='INVALID':bad.append(str(n)+':invalid-calendar-or-precision')
  if (precision=='unspecified')!=(role=='not-established'):bad.append(str(n)+':unknown-time-role-mismatch')
  records=list(g.subjects(R.carrierClaim,n))
  if len(records)!=1 or len(list(g.objects(records[0],E.sourceID)))!=1:bad.append(str(n)+':single-source-required')
  if str(g.value(n,E.claimMode))=='planned' and role not in ['planned-window','not-established']:bad.append(str(n)+':plan-is-not-event-date')
  if role=='planned-window' and str(g.value(n,E.claimMode))!='planned':bad.append(str(n)+':planned-time-requires-planned-mode')
 for record,d in g.subject_objects(E.sourceDate):
  if time_interval(str(d),'day')=='INVALID':bad.append(str(record)+':invalid-source-date')
 return {'conforms':bool(ok) and not bad,'shacl_conforms':bool(ok),'calendar_and_source_errors':bad}
def answer(g,subject,predicate,obj,mode='reported-occurrence',as_of=None):
 if not admission(g)['conforms']:return {'status':'INVALID_INPUT','claims':[],'world_fact_inferred':False}
 if as_of is not None:
  try:cut=date.fromisoformat(as_of)
  except ValueError:return {'status':'INVALID_INPUT','claims':[],'world_fact_inferred':False}
 found=[];unknown_dates=False
 for n in g.subjects(B.claimSubject,subject):
  if g.value(n,B.predicateIRI)!=Literal(str(predicate),datatype=XSD.anyURI) or (n,B.objectValue if isinstance(obj,Literal) else B.objectResource,obj) not in g or str(g.value(n,E.claimMode))!=mode:continue
  record=next(g.subjects(R.carrierClaim,n));d=g.value(record,E.sourceDate)
  if as_of is not None:
   if d is None:unknown_dates=True;continue
   if date.fromisoformat(str(d))>cut:continue
  found.append({'claim':str(n),'source':str(g.value(record,E.sourceID)),'mode':mode,'origin':str(g.value(n,B.claimOrigin)),'polarity':str(g.value(n,B.polarity)),'time':str(g.value(n,E.timeLexical)),'precision':str(g.value(n,E.timePrecision)),'role':str(g.value(n,E.timeRole))})
 pol={x['polarity'] for x in found}
 status='SOURCE_CONFLICT' if len(pol)>1 else 'SOURCE_DENIED_IN_MODE' if pol=={'negative'} else ('MAPPING_PROPOSED' if mode=='mapping-proposal' else 'SOURCE_REPORTED_'+mode.removeprefix('reported-').upper().replace('-','_')) if found else 'UNKNOWN_SOURCE_DATE' if unknown_dates else 'NOT_REPORTED_IN_SELECTED_MODE'
 return {'status':status,'claims':found,'world_fact_inferred':False}
def add(g,id,source,subject,predicate,obj,mode,loc,time='UNKNOWN',precision='unspecified',role='not-established',polarity='positive'):
 n=T[id];record=T[source];coh.ctx.claim(g,n,record,T[subject],predicate,obj if isinstance(obj,URIRef) else Literal(obj),origin='mapping-interpretation' if mode=='mapping-proposal' else 'source-extracted',pointer=source+'#'+loc,polarity=polarity)
 g.add((n,E.profile,Literal('documentary-witness')))
 for p,v in [('claimMode',mode),('timeLexical',time),('timePrecision',precision),('timeRole',role)]:g.add((n,E[p],Literal(v)))
 return n
