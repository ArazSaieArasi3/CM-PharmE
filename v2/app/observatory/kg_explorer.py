#!/usr/bin/env python3
import csv, json, sys
from pathlib import Path

FIXTURE = Path(__file__).parent / 'fixtures' / 'kg-explorer-fixture.csv'
ALLOWED_EDGES = {
    'https://w3id.org/cm-pharme/2.0/presentationOf',
    'https://w3id.org/cm-pharme/2.0/hasActiveSubstance',
    'https://w3id.org/cm-pharme/2.0/locatedIn',
}
ALLOWED_PROVENANCE = {'source-backed', 'provenance-unavailable'}

def load_fixture(path=FIXTURE):
    rows = list(csv.DictReader(path.open(encoding='utf-8')))
    nodes = {r['record_id']: r for r in rows if r['record_kind'] == 'node'}
    edges = [r for r in rows if r['record_kind'] == 'edge']
    return nodes, edges

def neighborhood(node_id):
    nodes, edges = load_fixture()
    if node_id not in nodes:
        raise KeyError(node_id)
    admitted = []
    for e in edges:
        if e['semantic_type_or_edge'] not in ALLOWED_EDGES:
            continue
        if e['expected_visible'].lower() != 'true':
            continue
        if e['source_id'] == node_id or e['target_id'] == node_id:
            admitted.append({
                'edge_id': e['record_id'],
                'edge_type': e['semantic_type_or_edge'],
                'source': e['source_id'],
                'target': e['target_id'],
                'provenance_state': e['provenance_state'],
            })
    return {
        'node_id': node_id,
        'semantic_type': nodes[node_id]['semantic_type_or_edge'],
        'provenance_state': nodes[node_id]['provenance_state'],
        'edges': sorted(admitted, key=lambda x: x['edge_id']),
        'claim_boundary': 'registered fixture edges only; adjacency and layout do not create ontology relations',
    }

def main():
    node_id = sys.argv[1] if len(sys.argv) > 1 else 'N-PROD-001'
    result = neighborhood(node_id)
    if result['provenance_state'] not in ALLOWED_PROVENANCE:
        raise SystemExit('invalid provenance state')
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
