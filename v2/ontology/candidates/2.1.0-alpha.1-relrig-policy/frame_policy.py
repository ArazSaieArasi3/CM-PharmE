"""Explicit RelRig endpoint review; no dependency truth or clean-model inference."""
import xml.etree.ElementTree as ET
PROFILE = "CMPE-RelRig-ExplicitEndpointReview/1.0.0"
XMI = "{http://www.omg.org/XMI}"
XSI = "{http://www.w3.org/2001/XMLSchema-instance}"


def evaluate_frame(path):
    root=ET.parse(path).getroot();ids={}
    for e in root.iter():
        key=e.get(XMI+'id')
        if key:
            if key in ids: raise ValueError('duplicate_id')
            ids[key]=e
        if e.get('subsettedProperty') or e.get('redefinedProperty'):
            raise ValueError('unsupported_subsetting')
    classes={};relations=[]
    for e in root.findall('packagedElement'):
        kind=e.get(XSI+'type','').removeprefix('RefOntoUML:')
        if kind in {'Kind','SubKind','Role','Relator'}:
            classes[e.get(XMI+'id')]=(kind,e)
        elif kind=='Mediation':relations.append(e)
        else:raise ValueError('unsupported_stereotype')
    if len(relations)!=1 or len(classes) not in {2,3}:raise ValueError('outside_single_mediation_scope')
    rel=relations[0];ends=rel.findall('ownedEnd');order=rel.get('memberEnd','').split()
    if len(ends)!=2 or len(order)!=2 or set(order)!={e.get(XMI+'id') for e in ends}:
        raise ValueError('unbound_binary_ends')
    if any(e.get('type') not in classes for e in ends):raise ValueError('untyped_end')
    relator_ends=[e for e in ends if classes[e.get('type')][0]=='Relator']
    if len(relator_ends)!=1:raise ValueError('ambiguous_relator')
    relator_end=relator_ends[0];mediated_end=next(e for e in ends if e is not relator_end)
    values=[]
    for e in [relator_end,mediated_end]:
        if e.get('isReadOnly') is None:
            raise ValueError('missing_relator_readonly' if e is relator_end else 'missing_mediated_readonly')
        if e.get('isReadOnly') not in {'true','false'}:raise ValueError('invalid_readonly')
        lo,hi=e.find('lowerValue'),e.find('upperValue')
        if lo is None or lo.get('value') is None:raise ValueError('missing_lower')
        if hi is None or hi.get('value') is None:raise ValueError('missing_upper')
        low,up=int(lo.get('value')),int(hi.get('value'))
        if low<0 or up < -1 or (up!=-1 and up<low):raise ValueError('invalid_interval')
        if e.get('aggregation')!='none':raise ValueError('unsupported_aggregation')
        if e.get('association')!=rel.get(XMI+'id'):raise ValueError('unbound_binary_ends')
        values.append(dict(id=e.get(XMI+'id'),type=e.get('type'),read_only=e.get('isReadOnly')=='true',lower=low,upper=up,serialized_end_index=order.index(e.get(XMI+'id'))))
    for key,(kind,node) in classes.items():
        if node.get('isAbstract')!='false':raise ValueError('unsupported_abstractness')
        gens=node.findall('generalization')
        if kind in {'Kind','Relator'} and gens:raise ValueError('unsupported_ancestry')
        if kind in {'SubKind','Role'} and (len(gens)!=1 or gens[0].get('general') not in classes or classes[gens[0].get('general')][0]!='Kind'):
            raise ValueError('unsupported_ancestry')
    rr,mr=values;kind=classes[mediated_end.get('type')][0];rigid=kind in {'Kind','SubKind'}
    baseline_missing=not mr['read_only']
    return dict(profile=PROFILE,relator_end=rr,mediated_end=mr,mediated_stereotype=kind,
                published_frame_match=int(rigid and mr['read_only']),
                rigid_dependency_review_required=rigid,mediation_baseline_review_required=baseline_missing,
                review_required=rigid or baseline_missing,
                disposition='RIGID_DEPENDENCY_SEMANTICS_REVIEW_REQUIRED' if rigid else
                'MEDIATION_BASELINE_REVIEW_REQUIRED' if baseline_missing else
                'NO_RELRIG_SIGNATURE_IN_FRAME_NOT_CLEAN_CERTIFICATE',
                dependency_direction_inferred=False,domain_error_established=False,full_candidate_executed=False)
