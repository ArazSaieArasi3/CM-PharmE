#!/usr/bin/env python3
"""Build and validate the CM-PharmE 2.0 formal ontology.

The modular Turtle files are authoritative. This script creates deterministic
canonical N-Triples, interoperable RDF serializations, a manifest, and a
quality report. It also checks the Gate-D conceptual registry and executes a
small SHACL smoke test when pySHACL is available.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Iterable

from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef
from rdflib.compare import isomorphic, to_canonical_graph

CMPE = Namespace("https://w3id.org/cm-pharme/2.0/")
SH = Namespace("http://www.w3.org/ns/shacl#")


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--source-dir", default="v2/ontology/source/modules")
    p.add_argument("--conceptual-model", default="v2/ontouml/cm-pharme-v2.conceptual-model.json")
    p.add_argument("--baseline", default="v2/ontology/baseline/formal-baseline.json")
    p.add_argument("--shapes", default="v2/ontology/shapes/cm-pharme-v2.shacl.ttl")
    p.add_argument("--smoke-data", default="v2/ontology/tests/formal-smoke.ttl")
    p.add_argument("--output-root", default="build/v2-ontology")
    p.add_argument("--require-shacl", action="store_true")
    return p.parse_args()


def load_union(source_dir: Path) -> tuple[Graph, list[str]]:
    graph = Graph()
    files = sorted(source_dir.glob("*.ttl"))
    if not files:
        raise SystemExit(f"No Turtle modules found in {source_dir}")
    for path in files:
        graph.parse(path, format="turtle")
    return graph, [str(p) for p in files]


def canonical_lines(graph: Graph) -> list[str]:
    cg = to_canonical_graph(graph)
    lines = []
    for s, p, o in cg:
        lines.append(f"{s.n3()} {p.n3()} {o.n3()} .\n")
    return sorted(lines)


def canonical_bytes(graph: Graph) -> bytes:
    return "".join(canonical_lines(graph)).encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_serializations(graph: Graph, out: Path):
    dist = out / "distributions"
    dist.mkdir(parents=True, exist_ok=True)
    canonical = canonical_bytes(graph)
    (dist / "cm-pharme-v2.nt").write_bytes(canonical)
    graph.serialize(dist / "cm-pharme-v2.ttl", format="turtle")
    graph.serialize(dist / "cm-pharme-v2.owl", format="xml")
    graph.serialize(dist / "cm-pharme-v2.rdf", format="xml")
    graph.serialize(dist / "cm-pharme-v2.jsonld", format="json-ld", indent=2)
    return canonical


def reparse_and_compare(reference: Graph, paths: Iterable[tuple[Path, str]]) -> dict[str, bool]:
    result = {}
    for path, fmt in paths:
        g = Graph().parse(path, format=fmt)
        result[path.name] = isomorphic(reference, g)
    return result


def conceptual_types(model: dict):
    for module, pairs in model["modules"].items():
        for name, stereotype in pairs:
            yield module, name, stereotype


def explicit_disjoint(graph: Graph, a: URIRef, b: URIRef) -> bool:
    if (a, OWL.disjointWith, b) in graph or (b, OWL.disjointWith, a) in graph:
        return True
    for node in graph.subjects(RDF.type, OWL.AllDisjointClasses):
        members = graph.value(node, OWL.members)
        if members is None:
            continue
        try:
            from rdflib.collection import Collection
            vals = set(Collection(graph, members))
            if a in vals and b in vals:
                return True
        except Exception:
            pass
    return False


def run_shacl(data_graph: Graph, shapes_graph: Graph, ontology_graph: Graph, require: bool):
    try:
        from pyshacl import validate
    except ImportError:
        if require:
            raise SystemExit("pySHACL is required but not installed")
        return {"executed": False, "conforms": None, "note": "pySHACL not installed"}

    meta_conforms, _, meta_text = validate(shapes_graph, shacl_graph=None, meta_shacl=True, advanced=True)
    if not meta_conforms:
        raise SystemExit("SHACL Meta-SHACL validation failed:\n" + str(meta_text))
    conforms, report_graph, report_text = validate(
        data_graph,
        shacl_graph=shapes_graph,
        ont_graph=ontology_graph,
        inference="rdfs",
        abort_on_first=False,
        allow_infos=True,
        allow_warnings=True,
        meta_shacl=True,
        advanced=True,
    )
    if not conforms:
        raise SystemExit("Formal smoke data failed SHACL validation:\n" + str(report_text))
    return {
        "executed": True,
        "conforms": bool(conforms),
        "report_triples": len(report_graph),
        "meta_shacl_conforms": bool(meta_conforms),
    }


def main():
    args = parse_args()
    source_dir = Path(args.source_dir)
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)

    graph, source_files = load_union(source_dir)
    model = json.loads(Path(args.conceptual_model).read_text(encoding="utf-8"))
    baseline = json.loads(Path(args.baseline).read_text(encoding="utf-8"))

    if model.get("official_ontouml_json") is not False:
        raise SystemExit("Conceptual registry must explicitly state official_ontouml_json=false")
    type_rows = list(conceptual_types(model))
    if len(type_rows) != model["counts"]["total"]:
        raise SystemExit("Conceptual model count mismatch")

    missing = []
    for module, name, stereotype in type_rows:
        iri = URIRef(model["namespace"] + name)
        is_class = (iri, RDF.type, OWL.Class) in graph
        is_datatype = (iri, RDF.type, RDFS.Datatype) in graph
        if not (is_class or is_datatype):
            missing.append(name)
    if missing:
        raise SystemExit("Conceptual types missing from formal graph: " + ", ".join(sorted(missing)))

    owl_classes = set(graph.subjects(RDF.type, OWL.Class))
    datatypes = set(graph.subjects(RDF.type, RDFS.Datatype))
    object_props = set(graph.subjects(RDF.type, OWL.ObjectProperty))
    datatype_props = set(graph.subjects(RDF.type, OWL.DatatypeProperty))

    counts = {
        "triples": len(graph),
        "owl_classes": len(owl_classes),
        "rdfs_datatypes": len(datatypes),
        "object_properties": len(object_props),
        "datatype_properties": len(datatype_props),
        "conceptual_types": len(type_rows),
    }
    expected = {
        "owl_classes": baseline["expected_owl_classes"],
        "rdfs_datatypes": baseline["expected_rdfs_datatypes"],
        "object_properties": baseline["expected_object_properties"],
        "datatype_properties": baseline["expected_datatype_properties"],
        "conceptual_types": baseline["conceptual_type_count"],
    }
    for key, value in expected.items():
        if counts[key] != value:
            raise SystemExit(f"Formal inventory mismatch for {key}: {counts[key]} != {value}")

    canonical = write_serializations(graph, out)
    fingerprint = sha256(canonical)
    expected_fingerprint = baseline.get("canonical_graph_sha256")
    if expected_fingerprint and fingerprint != expected_fingerprint:
        raise SystemExit(f"Canonical graph fingerprint changed: {fingerprint} != {expected_fingerprint}")

    dist = out / "distributions"
    equivalence = reparse_and_compare(graph, [
        (dist / "cm-pharme-v2.nt", "nt"),
        (dist / "cm-pharme-v2.ttl", "turtle"),
        (dist / "cm-pharme-v2.owl", "xml"),
        (dist / "cm-pharme-v2.rdf", "xml"),
        (dist / "cm-pharme-v2.jsonld", "json-ld"),
    ])
    if not all(equivalence.values()):
        raise SystemExit("One or more generated RDF serializations are not graph-isomorphic")

    protected = {}
    for left, right in model["protected_distinctions"]:
        a = URIRef(model["namespace"] + left)
        b = URIRef(model["namespace"] + right)
        protected[f"{left}!={right}"] = explicit_disjoint(graph, a, b)
    if not all(protected.values()):
        failed = [k for k, v in protected.items() if not v]
        raise SystemExit("Gate-D disjointness not formalized for: " + ", ".join(failed))

    shapes = Graph().parse(args.shapes, format="turtle")
    smoke = Graph().parse(args.smoke_data, format="turtle")
    shape_count = len(set(shapes.subjects(RDF.type, SH.NodeShape)))
    if shape_count < 10:
        raise SystemExit(f"Expected at least 10 SHACL node shapes; found {shape_count}")
    shacl_result = run_shacl(smoke, shapes, graph, args.require_shacl)

    manifest = {
        "schema_version": 1,
        "ontology_iri": "https://w3id.org/cm-pharme/2.0/ontology",
        "formal_version": "2.0.0-alpha.1",
        "source_files": source_files,
        "canonical_graph_sha256": fingerprint,
        "counts": counts,
        "serialization_equivalence": equivalence,
        "gate_d_disjointness": protected,
        "shacl": {"node_shapes": shape_count, **shacl_result},
        "w3id_redirect_status": "pending",
        "official_ontouml_json": False,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    quality = {
        "passed": True,
        "baseline_fingerprint_frozen": bool(expected_fingerprint),
        "manifest": manifest,
        "boundaries": [
            "Formal checks do not establish domain completeness, empirical correctness or organizational adoption.",
            "External mapping hints do not establish standards conformance.",
            "Held-out H1-H3 remain protected for W7 evaluation."
        ],
    }
    validation = out / "validation"
    validation.mkdir(parents=True, exist_ok=True)
    (validation / "quality-report.json").write_text(json.dumps(quality, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(quality, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
