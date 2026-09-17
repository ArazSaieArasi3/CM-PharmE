#!/usr/bin/env python3
from semantic_search import search


def validate():
    cases = [
        ('product', 'supported'),
        ('substance', 'supported'),
        ('definitely-not-in-fixture', 'insufficient-evidence'),
        ('', 'insufficient-evidence'),
    ]
    for query, expected in cases:
        result = search(query)
        assert result['status'] == expected, (query, result)
        assert result['evidence_boundary']
        if expected == 'supported':
            assert result['results'], query
            for item in result['results']:
                assert item['provenance_state'] in {'source-backed', 'provenance-unavailable'}
                for evidence in item['evidence']:
                    assert evidence['provenance_state'] in {'source-backed', 'provenance-unavailable'}
    print('semantic-search validation: PASS (4 representative cases)')


if __name__ == '__main__':
    validate()
