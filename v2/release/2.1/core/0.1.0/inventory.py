#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Inventory the proposed 2.1 support cut; no DB writes or ontology correction."""
import ast
import csv
import hashlib
import io
import json
import subprocess
from pathlib import Path

from rdflib import BNode, Graph, Namespace, OWL, RDF, RDFS, URIRef
from rdflib.compare import to_canonical_graph

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
SOURCE = 'c9792b25f7a837b3a34d2a868243e5f5e4dc1198'
OLD = Namespace('https://w3id.org/cm-pharme/2.0/')
NEW = Namespace('https://w3id.org/cm-pharme/2.1/')
SH = Namespace('http://www.w3.org/ns/shacl#')
M1 = 'v2/data/migrations/2.1/0.2.0/'
P3 = 'v2/ontology/candidates/2.1.0-alpha.1-p3-facility-operation/'
NAMES = ['Dataset', 'DatasetRelease', 'SourceRecord', 'ProvenanceActivity',
         'hasDatasetRelease', 'containsSourceRecord']


def save(name, data):
    (HERE / name).write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


def table(name, rows):
    out = io.StringIO(newline='')
    writer = csv.DictWriter(out, fieldnames=list(rows[0]), lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    (HERE / name).write_text(out.getvalue())


def canonical(graph):
    return ''.join(sorted(f'{s.n3()} {p.n3()} {o.n3()} .\n'
                          for s, p, o in to_canonical_graph(graph))).encode()


def main():
    baseline = Graph()
    paths = sorted((ROOT / 'v2/ontology/baseline/w5-source/modules').glob('*.ttl'))
    for p in paths:
        baseline.parse(p, format='turtle')
    expected = json.loads((ROOT / 'v2/ontology/baseline/formal-baseline.json').read_text())
    fingerprint = hashlib.sha256(canonical(baseline)).hexdigest()
    assert len(paths) == 6 and len(baseline) == 642
    assert fingerprint == expected['canonical_graph_sha256']
    candidate = Graph().parse(ROOT / (P3 + 'active.ttl'))
    shapes = Graph().parse(ROOT / (P3 + 'constraints.ttl'))
    seeds = {NEW[n] for n in NAMES}

    def logical(graph, term, namespace):
        def normalize(node):
            return str(node).replace(str(namespace), '{cmpe}/')
        predicates = {RDF.type, RDFS.domain, RDFS.range, RDFS.subClassOf,
                      RDFS.subPropertyOf, OWL.equivalentClass, OWL.equivalentProperty,
                      OWL.disjointWith, OWL.inverseOf}
        return sorted((normalize(p), normalize(o)) for p, o in graph.predicate_objects(term)
                      if p in predicates)

    terms = []
    for kind in [OWL.Class, RDFS.Datatype, OWL.ObjectProperty, OWL.DatatypeProperty]:
        for term in sorted(set(baseline.subjects(RDF.type, kind)), key=str):
            terms.append(dict(iri=str(term),kind=str(kind),layer='UNCHANGED_20_COMPATIBILITY_REFERENCE',
                              source='v2/ontology/baseline/w5-source/modules/',
                              acceptance='Historical research baseline; no new whole-model semantic approval'))
    seed_details = []
    for name in NAMES:
        old, new = OLD[name], NEW[name]
        before, after = logical(baseline, old, OLD), logical(candidate, new, NEW)
        assert before == after
        direct_shapes = sorted(str(s) for s in shapes.subjects(SH.targetClass, new))
        assert not direct_shapes
        seed_details.append(dict(name=name,iri=str(new),historical_iri=str(old),
                                 namespace_normalized_outgoing_logical_signature_equal=True,
                                 signature=after,target_class_shapes=direct_shapes))
        terms.append(dict(iri=str(new),kind=str(candidate.value(new, RDF.type)),
                          layer='PROPOSED_21_M1_PROFILE_NOT_YET_ISOLATED',source=P3+'active.ttl',
                          acceptance='No equivalence bridge or whole-candidate promotion inferred'))
    table('terms.csv', terms)

    m1_predicates = {RDF.type, URIRef('http://purl.org/dc/terms/identifier'),
                     NEW.hasDatasetRelease, NEW.containsSourceRecord, RDF.value,
                     URIRef('http://www.w3.org/ns/prov#value'),
                     URIRef('http://www.w3.org/ns/prov#wasGeneratedBy')}
    target_subject_intersection = sorted(str(p) for p in shapes.objects(None, SH.targetSubjectsOf)
                                         if p in m1_predicates)
    incoming = sorted({(str(s), str(p), str(o)) for s,p,o in candidate
                       if o in seeds and s not in seeds})
    inventory_paths = [(p.relative_to(ROOT).as_posix(), 'UNCHANGED_20_REFERENCE') for p in paths]
    inventory_paths += [(p,role) for role,ps in {
        'HISTORICAL_M1_RUNTIME_DEPENDENCY_NOT_APPROVED_AS_NEW_PROFILE': [
            M1+'verify_m1.py',M1+'scope.json',M1+'mapping-dispositions.csv',
            P3+'active.ttl',P3+'constraints.ttl',
            'tools/v2_data/bootstrap_ingest.py','tools/v2_data/source_contract.py',
            'tools/v2_data/export_kg.py','tools/v2_data/compare_sql_sparql.py',
            'v2/data/db/schema.sql','v2/data/db/views.sql',
            'v2/data/fixtures/nhif_outpatient_fixture.csv',
            'v2/data/fixtures/nhif_inpatient_fixture.csv',
            'v2/data/fixtures/geography_alias_fixture.csv',
            'v2/data/sources/source-manifest.json',
            'v2/data/queries/sql-sparql-benchmarks.json',
            'v2/data/migrations/2.1/0.1.0/w6-mapping-crosswalk.csv',
            '.github/workflows/v2-21-rdb-m1.yml'],
        'REFERENCE_OR_VERIFICATION_INPUT': [
            'v2/ontology/baseline/formal-baseline.json',
            'v2/requirements/2.1/orsd/0.2.0/requirements.json',
            'v2/requirements/2.1/execution/0.2.0/traceability-ledger.csv',
            'v2/release/2.1/ga/0.1.0/relcomp-review.json',
            'v2/release/2.1/rc.1/publication/publication-contract.json'],
    }.items() for p in ps]
    file_rows = []
    for path, role in inventory_paths:
        content = (ROOT/path).read_bytes()
        frozen = subprocess.check_output(['git','show',SOURCE+':'+path],cwd=ROOT)
        assert content == frozen, path
        file_rows.append(dict(path=path,role=role,bytes=len(content),
                              sha256=hashlib.sha256(content).hexdigest(),source_commit=SOURCE))
    table('files.csv',file_rows)

    import_rows = []
    for p in [M1+'verify_m1.py','tools/v2_data/bootstrap_ingest.py',
              'tools/v2_data/source_contract.py','tools/v2_data/export_kg.py',
              'tools/v2_data/compare_sql_sparql.py']:
        tree = ast.parse((ROOT/p).read_text())
        names = sorted({n.module or '' for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)} |
                       {a.name for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names})
        import_rows.append(dict(path=p,imports=names))

    report = dict(
        schema_version='CMPE-CoreInventory/0.1.0',source_commit=SOURCE,
        status='PASS_INVENTORY_NOT_IMPLEMENTATION_OR_GA',audit_issue=330,
        baseline=dict(files=6,triples=len(baseline),canonical_sha256=fingerprint,
                      owl_classes=len(set(baseline.subjects(RDF.type,OWL.Class))),
                      datatypes=len(set(baseline.subjects(RDF.type,RDFS.Datatype))),
                      object_properties=len(set(baseline.subjects(RDF.type,OWL.ObjectProperty))),
                      datatype_properties=len(set(baseline.subjects(RDF.type,OWL.DatatypeProperty))),
                      owl_imports=[str(x) for x in baseline.objects(None,OWL.imports)],
                      historical_semantic_approval_not_extended=True),
        m1=dict(selected_mapping_ids=['M001','M002','M003','M004'],
                selected_cmpe_classes=NAMES[:4],selected_cmpe_properties=NAMES[4:],
                historical_tbox_triples=len(candidate),historical_shape_triples=len(shapes),
                seed_defining_triples=sum(len(list(candidate.triples((t,None,None)))) for t in seeds),
                direct_target_class_shapes=0,
                target_subjects_of_intersection=target_subject_intersection,
                target_node_count=len(list(shapes.objects(None,SH.targetNode))),
                target_objects_of_count=len(list(shapes.objects(None,SH.targetObjectsOf))),
                advanced_target_count=len(list(shapes.objects(None,SH.target))),
                seeds=seed_details,incoming_references_to_review=incoming,
                isolated_semantic_module_claimed=False,
                historical_conformance_is_not_targeted_completeness_evidence=True),
        dependencies=dict(files_pinned=len(file_rows),python_static_imports=import_rows,
                          python='3.12',direct_python_dependencies=['psycopg[binary]==3.2.9','rdflib==7.5.0','pyshacl==0.31.0'],
                          database_image='postgis/postgis:16-3.4',external_runtime_bundled=False,
                          lockfile_for_new_cut_not_yet_built=True),
        compatibility=dict(historical_reference_bytes_unchanged=True,
                           six_terms_outgoing_logical_signatures_match_after_namespace_normalization=True,
                           full_namespace_equivalence_claimed=False,default_database_migration=False,
                           full_native_or_v1_equivalence_claimed=False,
                           v1='Historical 1.0.0 remains separate; 2.x is a new major generation',
                           new_profile_actual_regression_pending=True),
        findings=[
            dict(id='CORE-F01',severity='BLOCKS_SCOPED_GA',finding='Historical M1 validation imports the whole experimental P3 TBox/shapes rather than a separate supported entrypoint',resolution_issue=331),
            dict(id='CORE-F02',severity='BLOCKS_SCOPED_GA',finding='No direct targetClass shape for the four selected M1 classes; targeted admission/focus coverage is not established by old conformance',resolution_issue=331),
            dict(id='CORE-F03',severity='CLAIM_SCOPE',finding='FR-28 issuer/system identifier requirement is broader than the existing composite source-record key; do not declare the entire requirement satisfied',resolution='Keep scoped identity contract; defer broader FR-28 implementation'),
        ],
        ga_ready=False,new_database_run=False,new_reasoner_run=False,
        new_shacl_execution=False,model_or_oracle_changed=False,
    )
    assert not target_subject_intersection
    assert report['baseline']['owl_classes'] == 81
    assert report['baseline']['datatypes'] == 6
    assert report['baseline']['object_properties'] == 52
    assert report['baseline']['datatype_properties'] == 5
    save('inventory.json',report)
    print(json.dumps(dict(status=report['status'],source_files=len(file_rows),
                         public_term_rows=len(terms),baseline_triples=len(baseline),
                         m1_seed_terms=len(seeds),m1_target_class_shapes=0,
                         historical_tbox_triples=len(candidate),historical_shape_triples=len(shapes),
                         ga_blocking_findings=2,ga_ready=False),indent=2))


if __name__ == '__main__':
    main()
