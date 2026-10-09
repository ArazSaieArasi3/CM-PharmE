"""Guarded extension of the prior structural adapter for end reference serialization only.
No changes to source models, stereotype decisions, unknown bounds or nature-loss policy.
"""
import copy,sys,xml.etree.ElementTree as ET
from pathlib import Path
B=Path(__file__).resolve().parent.parent/'2.1.0-alpha.1-g3-p5b-adapter-probe'
sys.path.insert(0,str(B));from to_refontouml import convert as prior_convert,XMI,xid
FIELDS={'subsettedProperties':'subsettedProperty','redefinedProperties':'redefinedProperty'}
def convert(model):
 src={e['id']:e for e in model['elements']}
 if len(src)!=len(model['elements']):raise ValueError('Duplicate element ID')
 owners={}
 for r in src.values():
  if r['type']=='BinaryRelation':
   for end in r['properties']:
    if end in owners:raise ValueError('End belongs to multiple relations')
    owners[end]=r['id']
 refs={};edges={}
 for e in src.values():
  if e['type']!='Property':continue
  for key in FIELDS:
   values=e.get(key,[])
   if not isinstance(values,list):raise ValueError('Specialization references must be lists')
   if not values:continue
   if e['id'] not in owners:raise ValueError('Only binary association end specialization supported')
   if len(values)!=len(set(values)):raise ValueError('Duplicate specialization target')
   for target in values:
    if target==e['id']:raise ValueError('Self specialization reference')
    if target not in src or target not in owners or src[target]['type']!='Property':raise ValueError('Unresolved or non-end specialization target')
    if owners[target]==owners[e['id']]:raise ValueError('Same association end specialization outside supported subset')
   refs.setdefault(e['id'],{})[key]=values;edges.setdefault(e['id'],set()).update(values)
 def visit(n,path,done):
  if n in path:raise ValueError('Cyclic specialization references')
  if n in done:return
  for nxt in edges.get(n,[]):visit(nxt,path|{n},done)
  done.add(n)
 done=set()
 for n in edges:visit(n,set(),done)
 stripped=copy.deepcopy(model)
 for e in stripped['elements']:
  if e['type']=='Property':
   for key in FIELDS:e[key]=[]
 raw,report=prior_convert(stripped) # Unknown cards, endpoint types, events and other old guards still apply.
 root=ET.fromstring(raw);by_id={x.attrib['{'+XMI+'}id']:x for x in root.iter() if '{'+XMI+'}id' in x.attrib}
 for source,fields in refs.items():
  for key,targets in fields.items():by_id[xid(source)].set(FIELDS[key],' '.join(xid(t) for t in targets))
 ET.indent(root,space='  ')
 report.update(specialized_ends=len(refs),specialization_references=sum(len(v) for fields in refs.values() for v in fields.values()),reference_serialization_verified_scope='Binary end references only; not proof of UML semantic validity or full candidate fidelity.',scope='Extended strict structural subset, nature losses remain explicit; full candidate not supported.')
 return ET.tostring(root,encoding='utf-8',xml_declaration=True),report
