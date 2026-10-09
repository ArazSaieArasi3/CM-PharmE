"""Reproduce the native specialization and serialization audit without model edits."""
import copy
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from native_specialization import audit, index, PASS, FAIL, UNKNOWN

H = Path(__file__).resolve().parent
SOURCE = H.parent / '2.1.0-alpha.1-four-domain-refinement/ontouml-experimental.json'
CAL = H.parent / '2.1.0-alpha.1-detector-calibration'
sys.path.insert(0, str(CAL))
from adapter_specialization import convert


def write(name, data):
    (H/name).write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n')


def toy():
    # Hand-declared rule witness; this minimal structure is not OntoUML JSON interchange.
    els = [{'id': n, 'type':'Class'} for n in ['Parent','Child','Context','Subcontext','Other']]
    els += [{'id':'g1','type':'Generalization','specific':'Child','general':'Parent'},
            {'id':'g2','type':'Generalization','specific':'Subcontext','general':'Context'}]
    for rel, a, b in [('wide','Context','Parent'),('narrow','Subcontext','Child')]:
        els.append({'id':rel,'type':'BinaryRelation','properties':[rel+'-a',rel+'-b']})
        for end, typ in [('a',a),('b',b)]:
            els.append({'id':rel+'-'+end,'type':'Property','name':{'en':rel+'-'+end},'propertyType':typ,
                        'cardinality':'0..2','subsettedProperties': ['wide-b'] if (rel,end)==('narrow','b') else []})
    return {'elements':els}


def sensitivity():
    rows=[]
    def test(name, edit, field, expected):
        m=toy();d={e['id']:e for e in m['elements']};edit(m,d)
        try:
            r=audit(m)['rows'][0];actual=r.get(field)
        except ValueError as e:
            actual='REFUSED';r={'error':str(e)}
        rows.append({'name':name,'checked':field,'expected':expected,'actual':actual,'pass':actual==expected,'observation':r})
    test('valid-type-and-context',lambda m,d:None,'overall',PASS)
    test('same-type-allowed',lambda m,d:d['narrow-b'].update(propertyType='Parent'),'type_conformance',PASS)
    test('reverse-type-rejected',lambda m,d:(d['narrow-b'].update(propertyType='Parent'),d['wide-b'].update(propertyType='Child')),'type_conformance',FAIL)
    test('unrelated-type-rejected',lambda m,d:d['narrow-b'].update(propertyType='Other'),'type_conformance',FAIL)
    test('unknown-parent-type-not-pass',lambda m,d:d['wide-b'].update(propertyType=None),'type_conformance',UNKNOWN)
    test('opposite-end-context-rejected',lambda m,d:d['narrow-a'].update(propertyType='Other'),'context_conformance',FAIL)
    test('same-type-at-both-ends-still-has-context',lambda m,d:(d['narrow-a'].update(propertyType='Child'),d['wide-a'].update(propertyType='Parent')),'context_conformance',PASS)
    test('unknown-context-not-pass',lambda m,d:d['wide-a'].update(propertyType=None),'context_conformance',UNKNOWN)
    test('finite-upper-widening-rejected',lambda m,d:d['narrow-b'].update(cardinality='0..3'),'upper_bound',FAIL)
    test('unbounded-child-finite-parent-rejected',lambda m,d:d['narrow-b'].update(cardinality='0..*'),'upper_bound',FAIL)
    test('finite-child-unbounded-parent-allowed',lambda m,d:d['wide-b'].update(cardinality='0..*'),'upper_bound',PASS)
    test('both-unbounded-allowed',lambda m,d:(d['wide-b'].update(cardinality='0..*'),d['narrow-b'].update(cardinality='0..*')),'upper_bound',PASS)
    test('unknown-upper-not-defaulted',lambda m,d:d['wide-b'].update(cardinality=None),'upper_bound',UNKNOWN)
    test('lower-may-be-less',lambda m,d:d['wide-b'].update(cardinality='1..2'),'overall',PASS)
    test('same-property-name-rejected',lambda m,d:d['narrow-b'].update(name={'en':'wide-b'}),'different_names',FAIL)
    test('dangling-reference-rejected',lambda m,d:d['narrow-b'].update(subsettedProperties=['missing']),'reference',FAIL)
    test('redefinition-not-certified-as-subsetting',lambda m,d:d['narrow-b'].update(subsettedProperties=[],redefinedProperties=['wide-b']),'overall',UNKNOWN)
    test('inverted-bounds-refused',lambda m,d:d['narrow-b'].update(cardinality='3..2'),'overall','REFUSED')
    test('cyclic-generalization-refused',lambda m,d:m['elements'].append({'id':'g3','type':'Generalization','specific':'Parent','general':'Child'}),'overall','REFUSED')
    test('duplicate-id-refused',lambda m,d:m['elements'].append(copy.deepcopy(d['Parent'])),'overall','REFUSED')
    test('multiple-end-owners-refused',lambda m,d:m['elements'].append({'id':'other-rel','type':'BinaryRelation','properties':['wide-a','wide-b']}),'overall','REFUSED')
    return {'scope':'Hand-specified rule sensitivity witnesses; not real candidate acceptance or native parser cases.',
            'cases':rows,'pass':sum(r['pass'] for r in rows),'total':len(rows)}


def structural_fragment(m, seed):
    """Preserve selected elements verbatim; close references and ancestors/sets.

    All notes remain in the authoritative original, separately listed in the
    manifest. Projection is only a conversion feasibility probe.
    """
    d, owners, _=index(m);chosen={seed};changed=True
    while changed:
        previous=set(chosen)
        for key in list(chosen):
            e=d[key]
            if e['type']=='BinaryRelation':chosen.update(e['properties'])
            if e['type']=='Property':
                if e.get('propertyType'):chosen.add(e['propertyType'])
                for field in ['subsettedProperties','redefinedProperties']:
                    for target in e.get(field,[]):chosen.update([target,owners[target]])
            if e['type']=='Class':chosen.update(e.get('properties',[]))
            if e['type']=='Generalization':chosen.update([e['specific'],e['general']])
            if e['type']=='GeneralizationSet':chosen.update(e['generalizations'])
        for e in d.values():
            if e['type']=='Generalization' and e['specific'] in chosen:chosen.update([e['id'],e['general']])
            if e['type']=='GeneralizationSet' and chosen.intersection(e['generalizations']):chosen.add(e['id'])
        changed=chosen!=previous
    chosen.add(m['root']);f=copy.deepcopy(m);f['elements']=[copy.deepcopy(e) for e in m['elements'] if e['id'] in chosen]
    root=next(e for e in f['elements'] if e['id']==m['root']);root['contents']=[e for e in root['contents'] if e in chosen]
    return f,sorted(chosen)


def main():
    raw=SOURCE.read_bytes();m=json.loads(raw);d,owners,_=index(m)
    candidate=audit(m);tests=sensitivity();write('rule-sensitivity.json',tests)
    fragments=[]
    relations=sorted({r['relation'] for r in candidate['rows']})
    for relation in relations:
        f,ids=structural_fragment(m,relation)
        try:convert(f);result='UNEXPECTED_ACCEPTANCE'
        except (ValueError,AssertionError) as e:result='REFUSED: '+str(e)
        selected={e['id']:e for e in f['elements']}
        blockers={
            'unknown_cardinality_ends':[e['id'] for e in f['elements'] if e['type']=='Property' and e.get('cardinality') is None],
            'untyped_ends':[e['id'] for e in f['elements'] if e['type']=='Property' and e.get('propertyType') is None],
            'event_situation_classes':[e['id'] for e in f['elements'] if e.get('stereotype') in ['event','situation']],
            'unknown_readonly_ends':[e['id'] for e in f['elements'] if e['type']=='Property' and e.get('isReadOnly') is None],
            'nature_not_encoded_by_legacy':[e['id'] for e in f['elements'] if e.get('restrictedTo')],
        }
        # No source element may be rewritten to make conversion possible.
        assert all(selected[k]==d[k] for k in ids if k!=m['root'])
        fragments.append({'seed_relation':relation,'included_ids':ids,'source_fields_unchanged':True,
            'source_element_count':len(m['elements']),'projection_element_count':len(f['elements']),
            'excluded_note_ids':[e['id'] for e in m['elements'] if e['type']=='Note'],
            'excluded_relation_ids':[e['id'] for e in m['elements'] if e['type']=='BinaryRelation' and e['id'] not in ids],
            'root_contents_filtered':True,'scope':'Dependency-closed structural projection only; original retains all annotations and external relations.',
            'blockers':blockers,'legacy_attempt':result,'full_validation':False})
    candidate.update(source=str(SOURCE.relative_to(H.parent)),source_sha256=hashlib.sha256(raw).hexdigest(),
        actual_specialized_ends=len(candidate['rows']),relations=len(relations),
        redefinition_references=sum(bool(e.get('redefinedProperties')) for e in m['elements']),
        fragments=fragments,fully_resolved_specializations=sum(r['overall']==PASS for r in candidate['rows']))
    write('actual-specialization-results.json',candidate)
    subprocess.run(['node',str(H/'check_native_fidelity.cjs'),str(SOURCE),sys.argv[1],str(H/'native-roundtrip-results.json')],check=True,timeout=40)
    assert SOURCE.read_bytes()==raw and all(r['legacy_attempt'].startswith('REFUSED:') for r in fragments)
    assert tests['pass']==tests['total']
    print(json.dumps({'specialized_ends':len(candidate['rows']),'counts':candidate['counts'],'fragments':len(fragments),'rule_tests':str(tests['pass'])+'/'+str(tests['total']),'source_unchanged':True}))


if __name__=='__main__':main()
