#!/usr/bin/env python3
"""Derive controlled mini-models from the exact G3-P4a OntoUML JSON."""
import copy
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
source=json.loads((HERE.parent/'g3-p4a-supply-capacity/ontouml.json').read_text())
lookup={x['id']:x for x in source['elements']}


def build(title, class_ids, relation, source_type, target_type):
    project=copy.deepcopy(source)
    ids=set(class_ids)
    route=copy.deepcopy(lookup[relation])
    ends=[copy.deepcopy(lookup[x]) for x in route['properties']]
    route['id']='rel-toy'
    route['name']={'en':'toyRelation'}
    route['properties']=['end-toy-source','end-toy-target']
    route['stereotype']=None if title in ('positive','negative') else route['stereotype']
    for end, name, typ in zip(ends,route['properties'],(source_type,target_type)):
        end['id']=name
        end['propertyType']=typ
        end['name']={'en':name}
        assert end['cardinality'] is not None
    root=copy.deepcopy(lookup[source['root']])
    root['contents']=list(class_ids)+[route['id']]+route['properties']
    root['name']={'en':'CMPharmEtoy'+title}
    project['elements']=[root]+[copy.deepcopy(lookup[x]) for x in class_ids]+[route]+ends
    project['name']={'en':'CMPharmEtoy'+title}
    path=HERE/f'toy-{title}.json'
    path.write_text(json.dumps(project,indent=2,ensure_ascii=False)+'\n')
    return path


positive=build('positive',['Organization'],'rel-organizationHasSupplyCapacity','Organization','Organization')
negative=build('negative',['Organization','Facility'],'rel-organizationHasSupplyCapacity','Organization','Facility')
route=build('route',['Organization','SupplyCapacity'],'rel-organizationHasSupplyCapacity','Organization','SupplyCapacity')
print(json.dumps({'positive':str(positive),'negative':str(negative),'typed_route':str(route)}))
