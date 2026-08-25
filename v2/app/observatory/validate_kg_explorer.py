#!/usr/bin/env python3
import csv
from pathlib import Path
import kg_explorer

ROOT = Path(__file__).resolve().parents[3]
FREEZE = ROOT / 'research' / 'w8' / 'kg-explorer-mapping-freeze.csv'
FIXTURE = Path(__file__).parent / 'fixtures' / 'kg-explorer-fixture.csv'
EXPECTED_MAPPINGS = {'M009','M010','M011','M012','M013','M014','M015','M016','M021','M031'}
EXPECTED_VISIBLE_EDGES = {
    'E-PRES-PROD': 'https://w3id.org/cm-pharme/2.0/presentationOf',
    'E-PROD-SUB': 'https://w3id.org/cm-pharme/2.0/hasActiveSubstance',
}

with FREEZE.open(encoding='utf-8') as f:
    freeze = list(csv.DictReader(f))
assert {r['mapping_id'] for r in freeze} == EXPECTED_MAPPINGS
assert all(r['status'] in {'direct','bounded'} for r in freeze)

nodes, edges = kg_explorer.load_fixture(FIXTURE)
assert {'N-PROD-001','N-PRES-001','N-SUB-001','N-ORG-001','N-FAC-001','N-OP-001'} <= set(nodes)
assert all(r['provenance_state'] in kg_explorer.ALLOWED_PROVENANCE for r in [*nodes.values(), *edges])
visible = {e['record_id']: e['semantic_type_or_edge'] for e in edges if e['expected_visible'].lower() == 'true'}
assert visible == EXPECTED_VISIBLE_EDGES

product = kg_explorer.neighborhood('N-PROD-001')
assert {e['edge_id'] for e in product['edges']} == {'E-PRES-PROD','E-PROD-SUB'}
organization = kg_explorer.neighborhood('N-ORG-001')
assert organization['edges'] == [], 'unregistered helper adjacency must not become a traversable ontology edge'
assert product['semantic_type'].endswith('/MedicinalProduct')
assert nodes['N-PRES-001']['semantic_type_or_edge'].endswith('/MedicinalProductPresentation')
assert nodes['N-ORG-001']['semantic_type_or_edge'].endswith('/Organization')
assert nodes['N-FAC-001']['semantic_type_or_edge'].endswith('/Facility')
print('PASS: V2-079 deterministic KG explorer contract')
print('PASS: semantic IDs distinct from presentation/source metadata')
print('PASS: registered-edge-only traversal enforced')
print('PASS: explicit provenance state enforced')
