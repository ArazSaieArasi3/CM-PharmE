"""Conservative structural prefilter. Candidate != semantic anti-pattern verdict."""
import collections
import itertools
import json
import sys
import hashlib
from pathlib import Path

input_path=Path(sys.argv[1])
output_path=Path(sys.argv[2])
m=json.loads(input_path.read_text())
e={x['id']:x for x in m['elements']}
cl={x['id']:x for x in m['elements'] if x['type']=='Class'}
parents=collections.defaultdict(set)
children=collections.defaultdict(set)
for g in m['elements']:
    if g['type']=='Generalization' and g['specific'] in cl and g['general'] in cl:
        parents[g['specific']].add(g['general']);children[g['general']].add(g['specific'])
def ancestors(x):
    seen=set();stack=list(parents[x])
    while stack:
        p=stack.pop()
        if p not in seen:seen.add(p);stack.extend(parents[p])
    return seen
def descendants(x):
    seen=set();stack=list(children[x])
    while stack:
        p=stack.pop()
        if p not in seen:seen.add(p);stack.extend(children[p])
    return seen
def upper(card):
    if card is None:return 0  # Unknown cardinality: do not infer an upper bound.
    s=card.split('..')[-1]
    return float('inf') if s=='*' else int(s)
rels=[]
for x in m['elements']:
    if x['type']=='BinaryRelation':
        a,b=(e[i] for i in x['properties'])
        rels.append({'id':x['id'],'name':x['name']['en'],'stereotype':x['stereotype'],
                     'source':a['propertyType'],'target':b['propertyType'],
                     'source_card':a['cardinality'],'target_card':b['cardinality'],
                     'source_readonly':a['isReadOnly'],'target_readonly':b['isReadOnly'],
                     'source_id':a['id'],'target_id':b['id']})
med=[r for r in rels if r['stereotype']=='mediation']
triggers={}
triggers['BinOver_definite']=[r for r in rels if r['source']==r['target'] or r['source'] in ancestors(r['target']) or r['target'] in ancestors(r['source'])]
triggers['DecInt_multiple_concrete_parents']=[{'class':c,'parents':sorted(p)} for c,p in parents.items() if sum(not cl[x].get('isAbstract') for x in p)>=2]
triggers['DepPhase']=[r for r in med if cl[r['target']]['stereotype']=='phase']
triggers['FreeRole_direct_path']=[]
for c in cl:
    if cl[c]['stereotype']!='role' or any(r['target']==c for r in med):continue
    pp=[p for p in parents[c] if cl[p]['stereotype']=='role' and any(r['target']==p for r in med)]
    if pp:triggers['FreeRole_direct_path'].append({'role':c,'mediated_parent_roles':pp})
rigid={'kind','subkind','relator','quality','mode','event','situation','datatype','category'}
anti={'role','roleMixin','phase','phaseMixin'}
triggers['GSRig']=[]
for gs in (x for x in m['elements'] if x['type']=='GeneralizationSet'):
    ids=[e[g]['specific'] for g in gs['generalizations']]
    sts={cl[i]['stereotype'] for i in ids if i in cl}
    if sts & rigid and sts & anti:
        triggers['GSRig'].append({'set':gs['id'],'members':ids,'stereotypes':sorted(sts)})
triggers['MixRig']=[x for x in cl if cl[x]['stereotype']=='mixin' and len(children[x])>=2]
triggers['MultDep_direct']=[]
bytarget=collections.defaultdict(list)
for r in med:bytarget[r['target']].append(r)
for c,rows in bytarget.items():
    pairs=[(a,b) for a,b in itertools.combinations(rows,2) if a['source']!=b['source'] and a['source'] not in ancestors(b['source']) and b['source'] not in ancestors(a['source'])]
    if pairs:triggers['MultDep_direct'].append({'class':c,'mediations':sorted({r['name'] for pair in pairs for r in pair})})
triggers['RelRig_rigid_endpoint']=[r for r in med if cl[r['target']]['stereotype'] in rigid]
triggers['RepRel_direct']=[]
for c in cl:
    if cl[c]['stereotype']=='relator':
        rows=[r for r in med if r['source']==c and upper(r['source_card'])>1]
        if len(rows)>=2:triggers['RepRel_direct'].append({'relator':c,'mediations':[r['name'] for r in rows]})
triggers['ImpAbs']=[{'relation':r['name'],'end':end,'class':r[end],'subtype_count':len(descendants(r[end]))}
    for r in rels for end in ['source','target'] if upper(r[end+'_card'])>1 and len(descendants(r[end]))>=2]
triggers['UndefFormal']=[r for r in rels if r['stereotype']=='formal']
triggers['UndefPhase']=[x for x in cl if cl[x]['stereotype']=='phase']
meronymics={'componentOf','memberOf','subCollectionOf','subQuantityOf'}
triggers['meronymic_relations']=[r for r in rels if r['stereotype'] in meronymics]
triggers['MixIden_precondition']=[{'non_sortal':c,'children':sorted(children[c])} for c in cl if cl[c]['stereotype']=='roleMixin' and len(children[c])>=2]
triggers['RelSpec_simple']=[]
for a,b in itertools.combinations(rels,2):
    if None in (a['source'],a['target'],b['source'],b['target']):continue
    if (a['source']==b['source'] or a['source'] in ancestors(b['source']) or b['source'] in ancestors(a['source'])) and (a['target']==b['target'] or a['target'] in ancestors(b['target']) or b['target'] in ancestors(a['target'])):
        triggers['RelSpec_simple'].append([a['name'],b['name']])
output_path.write_text(json.dumps({'scope':'Conservative source-graph prefilter, not official detector or full catalogue adjudication',
    'native_sha256': hashlib.sha256(input_path.read_bytes()).hexdigest(),
    'native_elements':len(m['elements']),
    'counts':{k:len(v) for k,v in triggers.items()},'triggers':triggers},indent=2)+'\n')
print({k:len(v) for k,v in triggers.items()})
