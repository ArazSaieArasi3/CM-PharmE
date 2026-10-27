"""HomoFunc explicit part-minimum predicate; restricted witness frames only."""
import xml.etree.ElementTree as ET
PROFILE = "CMPE-HomoFunc-MinimumTwo/1.0.0"
XMI = "{http://www.omg.org/XMI}"
XSI = "{http://www.w3.org/2001/XMLSchema-instance}"


def evaluate_frame(path):
    root=ET.parse(path).getroot();ids={}
    for e in root.iter():
        key=e.get(XMI+'id')
        if key:
            if key in ids:raise ValueError('duplicate_id')
            ids[key]=e
        if e.get('subsettedProperty') or e.get('redefinedProperty'):
            raise ValueError('unsupported_subsetting')
    classes={};relations=[]
    for e in root.findall('packagedElement'):
        kind=e.get(XSI+'type','').removeprefix('RefOntoUML:')
        if kind=='Kind':
            if e.findall('generalization'):raise ValueError('unsupported_ancestry')
            if e.get('isAbstract')!='false':raise ValueError('unsupported_abstractness')
            classes[e.get(XMI+'id')]=e
        elif kind=='componentOf':relations.append(e)
        else:raise ValueError('unsupported_stereotype')
    if len(relations) not in {1,2} or len(classes)!=3:raise ValueError('outside_direct_kind_scope')
    selected=[]
    for rel in relations:
        ends=rel.findall('ownedEnd');order=rel.get('memberEnd','').split()
        if len(ends)!=2 or len(order)!=2 or set(order)!={e.get(XMI+'id') for e in ends}:
            raise ValueError('unbound_binary_ends')
        parsed=[]
        for e in ends:
            lo,hi=e.find('lowerValue'),e.find('upperValue')
            if lo is None or lo.get('value') is None:raise ValueError('missing_lower')
            if hi is None or hi.get('value') is None:raise ValueError('missing_upper')
            low,up=int(lo.get('value')),int(hi.get('value'))
            if low<0:raise ValueError('negative_lower')
            if up < -1 or (up!=-1 and up<low):raise ValueError('invalid_interval')
            if e.get('type') not in classes:raise ValueError('untyped_end')
            if e.get('association')!=rel.get(XMI+'id'):raise ValueError('unbound_binary_ends')
            parsed.append(dict(id=e.get(XMI+'id'),type=e.get('type'),lower=low,upper=up,aggregation=e.get('aggregation'),serialized_end_index=order.index(e.get(XMI+'id'))))
        wholes=[e for e in parsed if e['aggregation']=='shared'];parts=[e for e in parsed if e['aggregation']=='none']
        if len(wholes)!=1 or len(parts)!=1:raise ValueError('ambiguous_aggregation')
        if wholes[0]['type']==parts[0]['type']:raise ValueError('outside_direct_kind_scope')
        selected.append(dict(relation=rel.get(XMI+'id'),whole=wholes[0],part=parts[0]))
    selected.sort(key=lambda e:e['relation']);whole_types={e['whole']['type'] for e in selected};part_types={e['part']['type'] for e in selected}
    if len(whole_types)!=1 or part_types & whole_types or len(part_types)!=len(relations):
        raise ValueError('outside_direct_kind_scope')
    single=len(selected)==1
    part_minimum=selected[0]['part']['lower'] if single else None
    return dict(profile=PROFILE,whole=next(iter(whole_types)),part_roles=selected,
                direct_part_relation_count=len(selected),distinct_part_type_count=len(part_types),
                no_ancestry_in_admitted_scope=True,part_minimum=part_minimum,
                frame_match=int(single and part_minimum>=2),
                full_candidate_executed=False,domain_error_established=False)
