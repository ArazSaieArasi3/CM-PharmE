#!/usr/bin/env python3
"""Account for every fidelity blocker before anyone converts the full model."""
import hashlib
import json
from pathlib import Path

from to_refontouml import STEREOTYPES, convert

HERE=Path(__file__).resolve().parent
native_path=HERE.parent/'g3-p4a-supply-capacity/ontouml.json'
model=json.loads(native_path.read_text())
elements={e['id']:e for e in model['elements']}
classes=[e for e in elements.values() if e['type']=='Class']
relations=[e for e in elements.values() if e['type']=='BinaryRelation']
unknown_end_type=[]
unknown_cardinality=[]
subsetting=[]
for r in relations:
    for end_id in r['properties']:
        end=elements[end_id]
        if end['propertyType'] is None:
            unknown_end_type.append({'relation':r['id'],'end':end_id})
        if end['cardinality'] is None:
            unknown_cardinality.append({'relation':r['id'],'end':end_id})
        if end.get('subsettedProperties') or end.get('redefinedProperties'):
            subsetting.append({'relation':r['id'],'end':end_id,
                               'subsetted':end.get('subsettedProperties',[]),
                               'redefined':end.get('redefinedProperties',[])})
unsupported_classes=[{'id':c['id'],'stereotype':c['stereotype']}
                     for c in classes if c['stereotype'] not in STEREOTYPES]
notes=[e['id'] for e in elements.values() if e['type']=='Note']
natures=[{'id':c['id'],'restrictedTo':c.get('restrictedTo')}
         for c in classes if c.get('restrictedTo')]
try:
    convert(model)
    result='UNEXPECTEDLY_SUCCEEDED'
except ValueError as e:
    result='REFUSED: '+str(e)

report={
    'scope':'Full-model fidelity audit for archived RefOntoUML adapter; no full candidate detector run',
    'model_sha256':hashlib.sha256(native_path.read_bytes()).hexdigest(),
    'model_counts':{'elements':len(elements),'classes':len(classes),
                    'relations':len(relations),'generalizations':sum(e['type']=='Generalization' for e in elements.values()),
                    'generalization_sets':sum(e['type']=='GeneralizationSet' for e in elements.values())},
    'unsupported_class_stereotypes':{'count':len(unsupported_classes),'rows':unsupported_classes,
                                     'meaning':'Legacy Ecore has no direct Event or Situation classifier; coercion to generic Class would change semantic pattern detection.'},
    'untyped_relation_ends':{'count':len(unknown_end_type),'rows':unknown_end_type,
                             'meaning':'A missing native endpoint type must not be fabricated during XMI export.'},
    'unspecified_cardinality_ends':{'count':len(unknown_cardinality),'rows':unknown_cardinality,
                                    'distinct_relations':len({e['relation'] for e in unknown_cardinality}),
                                    'meaning':'Absent native cardinalities cannot silently become an EMF default such as 1..1.'},
    'subsetted_or_redefined_ends':{'count':len(subsetting),'rows':subsetting,
                                   'meaning':'The strict toy adapter does not yet preserve property specialization semantics.'},
    'modern_nature_restrictions':{'count':len(natures),
                                  'examples':[x for x in natures if x['id'] in ('Organization','SupplyCapacity')],
                                  'meaning':'Legacy model has no exact equivalent of restrictedTo; even a class stereotype conversion loses an explicit nature axiom.'},
    'notes':{'count':len(notes),'includes_capacity_xor_note':'p4a-capacity-xor-note' in notes,
             'meaning':'The explanatory native XOR note must not be mistaken for an executable legacy constraint.'},
    'full_adapter_result':result,
    'safe_next_action':'Design a loss-aware policy per blocker; then verify full model structural roundtrip and detector sensitivity on all 20 patterns before official findings.'
}
assert len(classes)==144 and len(relations)==86
assert len(unsupported_classes)==12
assert result.startswith('REFUSED:')
(HERE/'full-feasibility.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'refused':True,'unsupported_class_stereotypes':len(unsupported_classes),
                  'untyped_ends':len(unknown_end_type),
                  'missing_cardinality_ends':len(unknown_cardinality),
                  'subsetted_ends':len(subsetting),'modern_natures':len(natures)}))
