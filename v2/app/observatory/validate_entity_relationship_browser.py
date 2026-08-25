from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SQL = ROOT / 'v2/app/observatory/sql/entity-relationship-browser.sql'
FIXTURE = ROOT / 'v2/app/observatory/fixtures/entity-relationship-browser-fixture.csv'
FREEZE = ROOT / 'v2/research/w8/entity-relationship-browser-mapping-freeze.csv'

required_sql_tokens = {
    'M009', 'M010', 'M011', 'M013', 'M015', 'M016', 'M021',
    'cmpe.medicinal_product', 'cmpe.product_presentation',
    'cmpe.organization', 'cmpe.facility', 'cmpe.facility_operation',
    'cmpe.identifier_assignment', 'cmpe.source_record',
    'provenance-unavailable', 'source-backed',
    'presentationOf', 'hasActiveSubstance'
}
forbidden_sql_tokens = {
    'owl:equivalentClass', 'CREATE TABLE', 'INSERT INTO', 'UPDATE ', 'DELETE FROM', 'DROP TABLE'
}
allowed_provenance = {'source-backed', 'provenance-unavailable'}
allowed_semantic_types = {
    'MedicinalProduct', 'Presentation', 'PharmaceuticalSubstance',
    'Organization', 'Facility'
}


def fail(msg: str) -> None:
    raise SystemExit(f'FAIL: {msg}')


sql = SQL.read_text(encoding='utf-8')
freeze = FREEZE.read_text(encoding='utf-8')
for token in sorted(required_sql_tokens):
    if token not in sql and token not in freeze:
        fail(f'missing governed token: {token}')
for token in sorted(forbidden_sql_tokens):
    if token in sql:
        fail(f'forbidden mutation/equivalence token in read-only browser SQL: {token}')

with FIXTURE.open(newline='', encoding='utf-8') as fh:
    rows = list(csv.DictReader(fh))

if len(rows) < 6:
    fail('fixture must contain at least six representative cases')
case_ids = [r['case_id'] for r in rows]
if len(case_ids) != len(set(case_ids)):
    fail('fixture case_id values must be unique')

for row in rows:
    if row['provenance_status'] not in allowed_provenance:
        fail(f"invalid provenance status for {row['case_id']}")
    if row['semantic_type'] not in allowed_semantic_types:
        fail(f"unregistered semantic type for {row['case_id']}: {row['semantic_type']}")
    if row['semantic_type'] == 'Organization' and row['semantic_id'].startswith('FAC-'):
        fail('Organization/Facility identity leakage detected')
    if row['semantic_type'] == 'Facility' and row['semantic_id'].startswith('ORG-'):
        fail('Facility/Organization identity leakage detected')
    if row['semantic_type'] == 'MedicinalProduct' and row['semantic_id'].startswith('PRES-'):
        fail('MedicinalProduct/Presentation identity leakage detected')
    if row['semantic_type'] == 'Presentation' and row['semantic_id'].startswith('MED-'):
        fail('Presentation/MedicinalProduct identity leakage detected')
    predicate = row['predicate_iri']
    if predicate and predicate not in {
        'https://w3id.org/cm-pharme/2.0/presentationOf',
        'https://w3id.org/cm-pharme/2.0/hasActiveSubstance',
        'https://w3id.org/cm-pharme/2.0/operatesFacility',
    }:
        fail(f"unregistered traversal predicate for {row['case_id']}: {predicate}")

# Guard against source labels/codes becoming semantic identity in the SQL contract.
if 'AS semantic_id' not in sql:
    fail('semantic_id projection missing')
if 'lexical_value AS semantic_id' in sql or 'source_hash AS semantic_id' in sql:
    fail('source field promoted to semantic identity')

print(f'PASS: {len(rows)} deterministic browser cases validated')
print('PASS: Organization != Facility')
print('PASS: MedicinalProduct != Presentation')
print('PASS: source label/code != semantic identity')
print('PASS: traversal predicates bounded to registered relations')
print('PASS: provenance status is explicit on representative fixture cases')
