import json
from pathlib import Path

model=json.loads(Path('candidate-ontouml.json').read_text())
proposal=json.loads(Path('nature-proposals.json').read_text())
byid={r['class_id']:r for r in proposal['rows']}
changed=[]
for e in model['elements']:
    if e['type']!='Class':continue
    row=byid[e['id']]
    if row['status']=='proposed_for_author_review':
        assert e['restrictedTo']==[]
        e['restrictedTo']=row['candidate_restrictedTo']
        changed.append(e['id'])
assert len(changed)==142
Path('nature-overlay.json').write_text(json.dumps(model,indent=2,ensure_ascii=False)+'\n')
print('nature overlay:',len(changed),'classes updated; unresolved:',[r['class_id'] for r in proposal['rows'] if r['status']=='requires_semantic_decision'])
