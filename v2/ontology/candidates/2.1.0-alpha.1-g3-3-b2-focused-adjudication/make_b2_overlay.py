import json
import sys
from pathlib import Path

input_path,output_path=map(Path,sys.argv[1:3])
source=json.loads(input_path.read_text())
changed=[]
for item in source['elements']:
    if item['type']=='Class' and item['id'] in {'EnterpriseCapability','SupplyCapacity'}:
        assert item['stereotype']=='mode' and item['restrictedTo']==[]
        item['restrictedTo']=['intrinsic-mode']
        changed.append(item['id'])
assert sorted(changed)==['EnterpriseCapability','SupplyCapacity']
redundant='gen-ListingResponsibleOrganizationRole-Organization'
assert sum(e['id']==redundant for e in source['elements'])==1
assert not any(redundant in e.get('generalizations',[]) for e in source['elements'] if e['type']=='GeneralizationSet')
source['elements']=[e for e in source['elements'] if e['id']!=redundant]
root=next(e for e in source['elements'] if e['id']==source['root'])
assert redundant in root['contents']
root['contents'].remove(redundant)
output_path.write_text(json.dumps(source,indent=2,ensure_ascii=False)+'\n')
print(changed,'removed redundant generalization',redundant)
