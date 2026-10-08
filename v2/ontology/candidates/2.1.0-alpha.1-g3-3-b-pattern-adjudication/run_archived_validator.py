import json
import sys
from collections import Counter
from pathlib import Path
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from loguru import logger

logger.remove()
from validator.validations.rules_general import execute_rule_switch  # noqa: E402

native_path, projection_ttl, out_path = map(Path, sys.argv[1:4])
source = json.loads(native_path.read_text())
g = Graph().parse(projection_ttl, format='turtle')
ONT = Namespace('https://w3id.org/ontouml#')
nature_uri = {'functional-complex':'functionalComplexNature', 'collective':'collectiveNature',
              'quantity':'quantityNature','relator':'relatorNature',
              'intrinsic-mode':'intrinsicModeNature','extrinsic-mode':'extrinsicModeNature',
              'quality':'qualityNature','event':'eventNature','situation':'situationNature',
              'abstract':'abstractNature','type':'typeNature'}
base = str(next(g.subjects(RDF.type, ONT.Project))).rsplit('#', 1)[0] + '#'
classes = [e for e in source['elements'] if e['type'] == 'Class']
for c in classes:
    subject = URIRef(base + c['id'])
    assert (subject, RDF.type, ONT.Class) in g, c['id']
    name = c.get('name')
    if isinstance(name, dict): name = name.get('en') or next(iter(name.values()), None)
    if name: g.add((subject, ONT.name, Literal(name, lang='en')))
    if c.get('stereotype'): g.add((subject, ONT.stereotype, ONT[c['stereotype']]))
    for nature in c.get('restrictedTo', []):g.add((subject, ONT.restrictedTo, ONT[nature_uri[nature]]))
    # Empty restrictedTo remains absent; do not infer nature to make the validation pass.

codes = ['R_CL_XJZ','R_CL_JOJ','R_CL_UMC','R_CL_AIB','R_CL_EDA',
         'R_CL_ZGT','R_CL_GJU','R_CL_BWZ','R_CL_YOK','R_CL_QJC',
         'R_CL_EGT','R_CL_EMV','R_CL_ALX']
out = {'tool': 'OntoUML/ontouml-validator archived commit 46f54c1a5225fc9ea74ac2256fd4a673e9101a40',
       'input': 'json2graph legacy projection augmented with source class name/stereotype/restrictedTo',
       'coverage': '13 implemented class-only rules, not full validator or 20 anti-pattern catalogue',
       'class_count': len(classes), 'graph_triples': len(g), 'rules': []}
for code in codes:
    try:
        warnings, errors = execute_rule_switch(g, code)
        out['rules'].append({'code': code,
            'warnings': [{'source': x.related_id, 'message': x.issue_description} for x in warnings],
            'errors': [{'source': x.related_id, 'message': x.issue_description} for x in errors]})
    except Exception as ex:
        out['rules'].append({'code': code, 'exception': type(ex).__name__ + ': ' + str(ex)})
out['summary'] = {'warnings': sum(len(x.get('warnings', [])) for x in out['rules']),
                  'errors': sum(len(x.get('errors', [])) for x in out['rules']),
                  'exceptions': sum('exception' in x for x in out['rules']),
                  'by_rule': {x['code']: [len(x.get('warnings', [])), len(x.get('errors', []))]
                              for x in out['rules']}}
out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
print(out['summary'])
