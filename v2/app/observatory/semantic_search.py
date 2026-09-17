#!/usr/bin/env python3
"""Bounded deterministic semantic-search assistance for CM-PharmE V2.

This prototype intentionally operates only over the admitted KG explorer fixture.
It returns provenance states and explicit answer boundaries; it makes no claim of
open-world completeness, AI novelty, predictive performance, or production readiness.
"""
import json
import sys

from kg_explorer import load_fixture, ALLOWED_EDGES, ALLOWED_PROVENANCE


def _label(row):
    return (row.get('label') or row.get('name') or row.get('record_id') or '').strip()


def search(term):
    term = (term or '').strip().lower()
    if not term:
        return {
            'status': 'insufficient-evidence',
            'intent': 'semantic entity lookup',
            'query': term,
            'results': [],
            'evidence_boundary': 'a non-empty query is required',
        }

    nodes, edges = load_fixture()
    matches = []
    for node_id, row in sorted(nodes.items()):
        haystack = ' '.join(str(v) for v in row.values()).lower()
        if term not in haystack:
            continue
        evidence = []
        for edge in edges:
            if edge['semantic_type_or_edge'] not in ALLOWED_EDGES:
                continue
            if edge['expected_visible'].lower() != 'true':
                continue
            if edge['source_id'] == node_id or edge['target_id'] == node_id:
                evidence.append({
                    'edge_id': edge['record_id'],
                    'relation': edge['semantic_type_or_edge'],
                    'source': edge['source_id'],
                    'target': edge['target_id'],
                    'provenance_state': edge['provenance_state'],
                })
        matches.append({
            'record_id': node_id,
            'label': _label(row),
            'semantic_type': row['semantic_type_or_edge'],
            'provenance_state': row['provenance_state'],
            'evidence': sorted(evidence, key=lambda x: x['edge_id']),
        })

    invalid = [m['record_id'] for m in matches if m['provenance_state'] not in ALLOWED_PROVENANCE]
    if invalid:
        raise ValueError(f'invalid provenance state for: {invalid}')

    return {
        'status': 'supported' if matches else 'insufficient-evidence',
        'intent': 'semantic entity lookup',
        'query': term,
        'results': matches,
        'retrieval_path': 'admitted KG explorer fixture -> node lexical match -> registered visible edges',
        'evidence_boundary': (
            'registered fixture nodes and visible admitted edges only; absence is not evidence of ecosystem absence'
        ),
    }


def main():
    query = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else ''
    print(json.dumps(search(query), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
