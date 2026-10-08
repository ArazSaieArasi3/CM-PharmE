"""Dry-run only: derives candidate restrictedTo values, never edits ontology."""
import collections
import json
from pathlib import Path

m=json.loads(Path('candidate-ontouml.json').read_text())
cl={x['id']:x for x in m['elements'] if x['type']=='Class'}
parents=collections.defaultdict(set); children=collections.defaultdict(set)
for g in m['elements']:
    if g['type']=='Generalization' and g['specific'] in cl:
        parents[g['specific']].add(g['general']);children[g['general']].add(g['specific'])
seed={'kind':'functional-complex','relator':'relator','event':'event',
      'situation':'situation','quality':'quality','datatype':'abstract'}
def ancestors(c):
    out=set();stack=list(parents[c])
    while stack:
        x=stack.pop()
        if x not in out:out.add(x);stack.extend(parents[x])
    return out
def descendants(c):
    out=set();stack=list(children[c])
    while stack:
        x=stack.pop()
        if x not in out:out.add(x);stack.extend(children[x])
    return out
rows=[]
for c,record in sorted(cl.items()):
    st=record['stereotype']
    natures=set()
    if st in seed: natures={seed[st]}
    elif st in {'role','subkind'}:
        natures={seed[cl[a]['stereotype']] for a in ancestors(c) if cl[a]['stereotype'] in seed}
    elif st=='roleMixin':
        natures={seed[cl[a]['stereotype']] for d in descendants(c) for a in ancestors(d) if cl[a]['stereotype'] in seed}
    status='proposed_for_author_review' if len(natures)==1 else 'requires_semantic_decision'
    reason='direct stereotype nature' if st in seed else ('inherited from typed ancestors/descendants' if natures else 'mode requires intrinsic versus extrinsic nature and bearer decision')
    rows.append({'class_id':c,'stereotype':st,'current_restrictedTo':record.get('restrictedTo'),
                 'candidate_restrictedTo':sorted(natures) if len(natures)==1 else None,
                 'status':status,'basis':reason})
Path('nature-proposals.json').write_text(json.dumps({
    'scope':'Dry-run nature proposals only; no native candidate changed; 13-class-rule archived validator still warns on current candidate',
    'counts':dict(collections.Counter(r['status'] for r in rows)),
    'rows':rows},indent=2)+'\n')
print(collections.Counter(r['status'] for r in rows))
print([r['class_id'] for r in rows if r['status']!='proposed_for_author_review'])
