#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Isolated M1 profile: OWL vocabulary, opt-in SHACL and composite-key admission."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from urllib.parse import quote, unquote

from pyshacl import validate
from rdflib import BNode, Graph, Literal, Namespace, OWL, RDF, RDFS, URIRef, XSD
from rdflib.collection import Collection
from rdflib.compare import to_canonical_graph

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5] if len(HERE.parents)>5 and (HERE.parents[5]/'v2').is_dir() else None
C = Namespace('https://w3id.org/cm-pharme/2.1/')
M = Namespace(str(C) + 'meta/')
S = Namespace(str(C) + 'profiles/m1-provenance/0.1.0/')
SH = Namespace('http://www.w3.org/ns/shacl#')
D = Namespace('http://purl.org/dc/terms/')
P = Namespace('http://www.w3.org/ns/prov#')
SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')
INSTANCE = str(C) + 'instance/'
CLASSES = ('Dataset', 'DatasetRelease', 'SourceRecord', 'ProvenanceActivity')
PROPERTIES = ('hasDatasetRelease', 'containsSourceRecord')
FREEZE_COMMIT = '699bd799c0c0234e9ded1422de83885c9bde24bb'
FREEZE_SHA256 = '017214d94a97a494e39ca95876c75b95f79c615ad30d89e5cb23ea85aa87d843'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical(graph):
    return ''.join(sorted(f'{s.n3()} {p.n3()} {o.n3()} .\n'
                          for s,p,o in to_canonical_graph(graph))).encode()


def frozen():
    require(ROOT is not None, 'Historical build/verification requires the repository; standalone admission does not')
    require(sha(HERE/'freeze.json') == FREEZE_SHA256, 'Freeze manifest drift')
    freeze = json.loads((HERE/'freeze.json').read_text())
    for path, expected in freeze['files_sha256'].items():
        require(sha(HERE/path) == expected, 'Frozen contract/oracle/fixture drift: '+path)
    contract = json.loads((HERE/'contract.json').read_text())
    for path, expected in contract['source_sha256'].items():
        require(sha(ROOT/path) == expected, 'Historical input drift: '+path)
    return contract


def audit_schema(graph):
    named = {s for kind in [OWL.Class,OWL.ObjectProperty,OWL.DatatypeProperty]
             for s in graph.subjects(RDF.type,kind) if str(s).startswith(str(C))}
    require(named == {C[n] for n in CLASSES+PROPERTIES}, 'Supported vocabulary drift')
    require(not list(graph.objects(None,OWL.imports)), 'Implicit ontology import refused')
    forbidden = {OWL.Restriction,OWL.AllDisjointClasses}
    require(not any((None,RDF.type,t) in graph for t in forbidden), 'Universal restriction added')
    require(not list(graph.triples((None,OWL.disjointWith,None))), 'Global disjointness added')
    require(not list(graph.triples((None,OWL.equivalentClass,None))), 'Equivalence bridge added')


def build_schema(contract):
    source_path = 'v2/ontology/candidates/2.1.0-alpha.1-p3-facility-operation/active.ttl'
    source = Graph().parse(ROOT/source_path,format='turtle')
    graph = Graph()
    selected = {C[n] for n in contract['selected_terms']}
    for s,p,o in source:
        if s in selected:
            graph.add((s,p,o))
    require(len(graph) == contract['isolation']['expected_defining_triples'], 'Defining triples changed')
    incoming = {(str(s),str(p),str(o)) for s,p,o in source if o in selected and s not in selected}
    rows = list(csv.DictReader((HERE/'incoming-axioms.csv').open()))
    require(incoming == {(x['subject'],x['predicate'],x['object']) for x in rows}, 'Unreviewed incoming axiom')
    require(all(x['disposition']=='EXCLUDED_OUTSIDE_SELECTED_SIGNATURE' for x in rows), 'Incoming disposition drift')
    for prop in [M.ontoumlStereotype,M.conceptualModule,M.conceptualModelVersion,SKOS.closeMatch,
                 D.title,D.description,D.creator,D.license,D.source]:
        graph.add((prop,RDF.type,OWL.AnnotationProperty))
    for prop in [D.identifier,P.value]:
        graph.add((prop,RDF.type,OWL.DatatypeProperty))
    graph.add((P.wasGeneratedBy,RDF.type,OWL.ObjectProperty))
    ontology = URIRef(str(C)+'profiles/m1-provenance')
    for triple in [(ontology,RDF.type,OWL.Ontology),(ontology,OWL.versionIRI,URIRef(str(S))),
                   (ontology,OWL.versionInfo,Literal('0.1.0')),
                   (ontology,D.title,Literal('CM-PharmE 2.1 M1 provenance support profile',lang='en')),
                   (ontology,D.description,Literal('Six-term support profile; local data admission is separate from universal OWL axioms.',lang='en')),
                   (ontology,D.creator,Literal('Araz Saie Arasi and CM-PharmE contributors')),
                   (ontology,D.license,URIRef('https://creativecommons.org/licenses/by/4.0/')),
                   (ontology,D.source,URIRef('https://github.com/ArazSaieArasi3/CM-PharmE/blob/'+contract['source_commit']+'/'+source_path))]:
        graph.add(triple)
    audit_schema(graph)
    return graph


def build_shapes():
    graph = Graph()

    def prop(shape,path,**values):
        b = BNode();graph.add((shape,SH.property,b));graph.add((b,SH.path,path))
        for key,value in values.items():
            graph.add((b,SH[key],value if isinstance(value,URIRef) else Literal(value)))
        return b

    def inverse(predicate):
        b=BNode();graph.add((b,SH.inversePath,predicate));return b

    for name in CLASSES:
        shape=S[name+'Shape']
        graph.add((shape,RDF.type,SH.NodeShape));graph.add((shape,SH.targetClass,C[name]))
        graph.add((shape,SH.nodeKind,SH.IRI))
        prop(shape,RDF.type,hasValue=C[name])
        prop(shape,D.identifier,minCount=1,maxCount=1,datatype=XSD.string,minLength=1)
        # Export-kind separation is local admission, not an OWL disjointness axiom.
        other=BNode();head=BNode();graph.add((shape,SH['not'],other));graph.add((other,SH['or'],head))
        options=[]
        for alternate in CLASSES:
            if alternate!=name:
                option=BNode();graph.add((option,SH['class'],C[alternate]));options.append(option)
        Collection(graph,head,options)
    graph.add((S.DatasetShape,SH.targetSubjectsOf,C.hasDatasetRelease))
    graph.add((S.DatasetReleaseShape,SH.targetObjectsOf,C.hasDatasetRelease))
    graph.add((S.DatasetReleaseShape,SH.targetSubjectsOf,C.containsSourceRecord))
    graph.add((S.SourceRecordShape,SH.targetObjectsOf,C.containsSourceRecord))
    graph.add((S.ProvenanceActivityShape,SH.targetObjectsOf,P.wasGeneratedBy))
    prop(S.DatasetShape,C.hasDatasetRelease,minCount=1,nodeKind=SH.IRI,**{'class':C.DatasetRelease})
    prop(S.DatasetReleaseShape,inverse(C.hasDatasetRelease),minCount=1,maxCount=1,nodeKind=SH.IRI,**{'class':C.Dataset})
    prop(S.DatasetReleaseShape,C.containsSourceRecord,minCount=1,nodeKind=SH.IRI,**{'class':C.SourceRecord})
    prop(S.SourceRecordShape,inverse(C.containsSourceRecord),minCount=1,maxCount=1,nodeKind=SH.IRI,**{'class':C.DatasetRelease})
    prop(S.SourceRecordShape,RDF.value,minCount=1,maxCount=1,datatype=XSD.integer)
    prop(S.SourceRecordShape,P.value,minCount=1,maxCount=1,datatype=XSD.string,minLength=1)
    prop(S.SourceRecordShape,P.wasGeneratedBy,maxCount=1,nodeKind=SH.IRI,**{'class':C.ProvenanceActivity})
    prop(S.ProvenanceActivityShape,inverse(P.wasGeneratedBy),minCount=1,nodeKind=SH.IRI,**{'class':C.SourceRecord})
    audit_shapes(graph)
    return graph


def audit_shapes(shapes):
    require(set(shapes.subjects(RDF.type,SH.NodeShape)) == {S[n+'Shape'] for n in CLASSES}, 'Four target shapes required')
    for name in CLASSES:
        require(set(shapes.objects(S[name+'Shape'],SH.targetClass)) == {C[name]}, 'Direct targetClass missing: '+name)
    require(not list(shapes.triples((None,SH.closed,Literal(True)))), 'Global closed-shape policy refused')


def focus_nodes(data,shapes):
    result={}
    for name in CLASSES:
        shape=S[name+'Shape'];nodes=set(data.subjects(RDF.type,C[name]))
        for p in shapes.objects(shape,SH.targetSubjectsOf):nodes.update(data.subjects(p,None))
        for p in shapes.objects(shape,SH.targetObjectsOf):nodes.update(data.objects(None,p))
        result[name]=nodes
    return result


def node(kind,key):
    return URIRef(INSTANCE+kind+'/'+quote(key,safe=''))


def logical_view(data):
    """OWL 2 DL view; keep rdf:value row payload in the separate RDF/query graph."""
    graph=data+Graph()
    excluded=list(graph.triples((None,RDF.value,None)))
    for triple in excluded:
        graph.remove(triple)
    return graph,excluded


def identity_errors(data,focus):
    errors=[]
    for name,kind in [('Dataset','dataset'),('DatasetRelease','dataset-release'),('ProvenanceActivity','provenance-activity')]:
        for subject in focus[name]:
            identifier=str(data.value(subject,D.identifier))
            if name=='Dataset':
                prefix=INSTANCE+kind+'/';key=unquote(str(subject)[len(prefix):])
                valid=str(subject).startswith(prefix) and bool(key) and node(kind,key)==subject
            else:
                valid=node(kind,identifier)==subject
            if not valid:errors.append(dict(node=str(subject),code='PUBLIC_ID_IRI_MISMATCH'))
    for record in focus['SourceRecord']:
        release=next(data.subjects(C.containsSourceRecord,record))
        expected=[str(data.value(release,D.identifier)),int(data.value(record,RDF.value)),str(data.value(record,P.value))]
        key=json.dumps(expected,ensure_ascii=False,separators=(',',':'))
        if str(data.value(record,D.identifier))!=key:
            errors.append(dict(node=str(record),code='COMPOSITE_KEY_COMPONENT_MISMATCH'))
        if record!=node('source-record',key):
            errors.append(dict(node=str(record),code='RECORD_IRI_KEY_MISMATCH'))
    return errors


def admit(data,profile=None,shapes=None):
    # Runtime needs only the isolated artifacts; historical inputs are build/test inputs.
    profile=profile if profile is not None else Graph().parse(HERE/'profile.ttl')
    shapes=shapes if shapes is not None else Graph().parse(HERE/'shapes.ttl')
    audit_schema(profile);audit_shapes(shapes)
    focus=focus_nodes(data,shapes);counts={k:len(v) for k,v in focus.items()}
    conforms,report,_=validate(data,shacl_graph=shapes,ont_graph=profile,
                              inference='none',advanced=False,meta_shacl=True,inplace=False)
    errors=[]
    if not conforms:stage='SHACL_REJECTED'
    elif not all(counts[n] for n in CLASSES[:3]):stage='EMPTY_SCOPE_REFUSED'
    else:
        errors=identity_errors(data,focus)
        stage='IDENTITY_REJECTED' if errors else 'ADMITTED'
    return dict(stage=stage,admitted=stage=='ADMITTED',shacl_conforms=bool(conforms),
                explicit_target_union_counts=counts,identity_errors=errors,
                shacl_results=len(set(report.subjects(RDF.type,SH.ValidationResult))))


def build():
    contract=frozen();profile=build_schema(contract);shapes=build_shapes()
    for name,graph in [('profile.ttl',profile),('shapes.ttl',shapes)]:
        (HERE/name).write_bytes(b'# SPDX-License-Identifier: CC-BY-4.0\n'+canonical(graph))
    manifest=dict(profile='CMPE-M1ProvenanceProfile/0.1.0',target_ontology='2.1.0',
                  contract_freeze_commit=FREEZE_COMMIT,source_commit=contract['source_commit'],
                  profile_triples=len(profile),shape_triples=len(shapes),supported_class_count=4,
                  supported_cmpe_object_property_count=2,owl_imports=[],
                  global_cardinality_or_disjointness_added=False,
                  full_source_semantic_module_equivalence=False,
                  formal_view=dict(excluded_serialization_predicate=str(RDF.value),
                                   lossless_full_rdf_to_owl_claimed=False,
                                   raw_rdf_retained_for_shacl_identity_and_queries=True),
                  artifacts_sha256={p:sha(HERE/p) for p in ['profile.ttl','shapes.ttl','query.rq']})
    (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True);sub.add_parser('build')
    command=sub.add_parser('admit');command.add_argument('data',type=Path)
    args=parser.parse_args()
    if args.command=='build':result=build()
    else:result=admit(Graph().parse(args.data,format='turtle'))
    print(json.dumps(result,indent=2))
    if args.command=='admit' and not result['admitted']:raise SystemExit(1)


if __name__=='__main__':main()
