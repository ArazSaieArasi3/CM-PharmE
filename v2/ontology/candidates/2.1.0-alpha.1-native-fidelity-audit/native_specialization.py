"""Bounded native checks, not a complete UML/OntoUML validator.

UML 2.5.1 9.9.17.8: subsetting_rules, subsetting_context_conforms,
subsetted_property_names. Null model values remain UNKNOWN, never defaults.
The binary-end context is the opposite end's type. Redefinition needs a
different rule set and is deliberately not certified by these checks.
"""
import re
from collections import Counter, defaultdict

PASS, FAIL, UNKNOWN = 'PASS', 'FAIL', 'UNKNOWN'


def index(model):
    d = {e['id']: e for e in model['elements']}
    if len(d) != len(model['elements']):
        raise ValueError('Duplicate element IDs')
    owners, parents = {}, defaultdict(set)
    for e in d.values():
        if e['type'] == 'BinaryRelation':
            if len(e['properties']) != 2 or len(set(e['properties'])) != 2:
                raise ValueError('Expected two distinct binary ends')
            for end in e['properties']:
                if end in owners or end not in d or d[end]['type'] != 'Property':
                    raise ValueError('Invalid or multiply owned binary end')
                owners[end] = e['id']
        if e['type'] == 'Generalization':
            if any(x not in d or d[x]['type'] != 'Class' for x in [e['specific'], e['general']]):
                raise ValueError('Invalid generalization reference')
            parents[e['specific']].add(e['general'])
    def visit(node, active, done):
        if node in active:
            raise ValueError('Cyclic generalization')
        if node in done:
            return
        for parent in parents[node]:
            visit(parent, active | {node}, done)
        done.add(node)
    done = set()
    for node in list(parents):
        visit(node, set(), done)
    return d, owners, parents


def cardinality(value):
    if value is None:
        return None
    match = re.fullmatch(r'(\d+)(?:\.\.(\d+|\*))?', value)
    if not match:
        raise ValueError('Malformed cardinality')
    lo, hi = int(match[1]), match[2] or match[1]
    hi = float('inf') if hi == '*' else int(hi)
    if hi < lo:
        raise ValueError('Inverted cardinality')
    return lo, hi


def audit(model):
    d, owners, parents = index(model)
    def conforms(specific, general):
        if specific is None or general is None:
            return UNKNOWN
        if specific not in d or general not in d or d[specific]['type'] != 'Class' or d[general]['type'] != 'Class':
            return FAIL
        todo, seen = [specific], set()
        while todo:
            current = todo.pop()
            if current == general:
                return PASS
            if current not in seen:
                seen.add(current)
                todo.extend(parents[current])
        return FAIL
    def context(end):
        return d[next(x for x in d[owners[end]]['properties'] if x != end)].get('propertyType')
    rows = []
    for e in d.values():
        for field in ['subsettedProperties', 'redefinedProperties']:
            for target in e.get(field, []):
                row = {'end': e['id'], 'target': target, 'kind': field,
                       'relation': owners.get(e['id'])}
                valid = e['id'] in owners and target in owners and d[target]['type'] == 'Property'
                row['reference'] = PASS if valid else FAIL
                if not valid:
                    row['overall'] = FAIL
                    rows.append(row)
                    continue
                q = d[target]
                row.update(source_type=e.get('propertyType'), target_type=q.get('propertyType'),
                           source_cardinality=e.get('cardinality'), target_cardinality=q.get('cardinality'))
                if field == 'redefinedProperties':
                    row.update(overall=UNKNOWN, reason='Redefinition semantic rules are outside this bounded checker')
                    rows.append(row)
                    continue
                row['type_conformance'] = conforms(e.get('propertyType'), q.get('propertyType'))
                row['context_conformance'] = conforms(context(e['id']), context(target))
                a, b = cardinality(e.get('cardinality')), cardinality(q.get('cardinality'))
                row['upper_bound'] = UNKNOWN if a is None or b is None else PASS if a[1] <= b[1] else FAIL
                en, qn = (e.get('name') or {}).get('en'), (q.get('name') or {}).get('en')
                row['different_names'] = UNKNOWN if en is None or qn is None else PASS if en != qn else FAIL
                values = [row[k] for k in ['reference', 'type_conformance', 'context_conformance', 'upper_bound', 'different_names']]
                row['overall'] = FAIL if FAIL in values else UNKNOWN if UNKNOWN in values else PASS
                rows.append(row)
    return {'scope': 'Binary subsetting reference/type/context/upper-bound/English-name checks only. No lower-bound strengthening rule. No scientific acceptance.',
            'rows': rows, 'counts': {key: dict(Counter(r[key] for r in rows if key in r)) for key in
                ['reference', 'type_conformance', 'context_conformance', 'upper_bound', 'different_names', 'overall']}}
