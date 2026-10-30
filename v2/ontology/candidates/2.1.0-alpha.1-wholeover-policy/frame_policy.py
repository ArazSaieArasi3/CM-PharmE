"""Independent threshold predicate for one explicitly restricted sibling-part frame."""
import xml.etree.ElementTree as ET
PROFILE = "CMPE-WholeOver-UpperSumTwo/1.0.0"
XMI = "{http://www.omg.org/XMI}"
XSI = "{http://www.w3.org/2001/XMLSchema-instance}"


def evaluate_frame(path):
    root = ET.parse(path).getroot()
    ids = {}
    for node in root.iter():
        key = node.get(XMI+'id')
        if key:
            if key in ids: raise ValueError('duplicate_id')
            ids[key] = node
        if node.get('subsettedProperty') or node.get('redefinedProperty'):
            raise ValueError('unsupported_subsetting')
    classes, relations, sets = {}, [], []
    for node in root.findall('packagedElement'):
        kind = node.get(XSI+'type','').removeprefix('RefOntoUML:')
        if kind in {'Kind','SubKind'}: classes[node.get(XMI+'id')] = node
        elif kind == 'componentOf': relations.append(node)
        elif kind == 'GeneralizationSet': sets.append(node)
        else: raise ValueError('unsupported_legacy_element')
    if len(classes)!=4 or len(relations)!=2 or len(sets)!=1:
        raise ValueError('outside_two_sibling_scope')
    selected=[]
    for relation in relations:
        ends=relation.findall('ownedEnd'); order=relation.get('memberEnd','').split()
        if len(ends)!=2 or len(order)!=2 or set(order)!={e.get(XMI+'id') for e in ends}:
            raise ValueError('unbound_binary_ends')
        parsed=[]
        for end in ends:
            lower,upper=end.find('lowerValue'),end.find('upperValue')
            if lower is None or lower.get('value') is None: raise ValueError('missing_lower')
            if upper is None or upper.get('value') is None: raise ValueError('missing_upper')
            lo,hi=int(lower.get('value')),int(upper.get('value'))
            if lo<0: raise ValueError('negative_lower')
            if hi < -1 or (hi!=-1 and hi<lo): raise ValueError('invalid_interval')
            if end.get('type') not in classes: raise ValueError('untyped_end')
            if end.get('association')!=relation.get(XMI+'id'): raise ValueError('unbound_binary_ends')
            parsed.append(dict(id=end.get(XMI+'id'),type=end.get('type'),lower=lo,upper=hi,aggregation=end.get('aggregation')))
        wholes=[e for e in parsed if e['aggregation']=='shared'];parts=[e for e in parsed if e['aggregation']=='none']
        if len(wholes)!=1 or len(parts)!=1: raise ValueError('ambiguous_aggregation')
        selected.append(dict(relation=relation.get(XMI+'id'),whole=wholes[0],part=parts[0]))
    selected.sort(key=lambda s:s['relation'])
    whole_types={s['whole']['type'] for s in selected};part_types={s['part']['type'] for s in selected}
    if len(whole_types)!=1 or len(part_types)!=2: raise ValueError('unsupported_ancestry')
    whole=next(iter(whole_types))
    if classes[whole].get(XSI+'type')!='RefOntoUML:Kind' or classes[whole].findall('generalization'):
        raise ValueError('unsupported_ancestry')
    generals=[];gens=[]
    for part in sorted(part_types):
        node=classes[part];gg=node.findall('generalization')
        if node.get(XSI+'type')!='RefOntoUML:SubKind' or len(gg)!=1: raise ValueError('unsupported_ancestry')
        generals.append(gg[0].get('general'));gens.append(gg[0])
    parent=generals[0]
    if len(set(generals))!=1 or parent in part_types|whole_types or parent not in classes:
        raise ValueError('unsupported_ancestry')
    if classes[parent].get(XSI+'type')!='RefOntoUML:Kind' or classes[parent].findall('generalization'):
        raise ValueError('unsupported_ancestry')
    gs=sets[0];gsid=gs.get(XMI+'id')
    if gs.get('isDisjoint') not in {'true','false'}: raise ValueError('missing_disjoint')
    if gs.get('isCovering') not in {'true','false'}: raise ValueError('missing_covering')
    if set(gs.get('generalization','').split())!={g.get(XMI+'id') for g in gens} or any(g.get('generalizationSet')!=gsid for g in gens):
        raise ValueError('unbound_generalization_set')
    upper=[s['part']['upper'] for s in selected];unlimited=-1 in upper
    finite_sum=None if unlimited else sum(upper)
    overlap=gs.get('isDisjoint')=='false'
    return dict(profile=PROFILE,whole=whole,part_roles=selected,part_upper_bounds=upper,
                finite_part_upper_sum=finite_sum,unlimited_part_upper=unlimited,
                possibly_overlapping_siblings=overlap,
                frame_match=int(overlap and (unlimited or finite_sum>=2)),
                full_candidate_executed=False)
