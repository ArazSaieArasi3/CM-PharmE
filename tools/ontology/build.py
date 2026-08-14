#!/usr/bin/env python3
"""Deterministic CM-PharmE ontology build from modular Turtle authoring source."""
from __future__ import annotations

import argparse
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import rdflib
from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.compare import to_canonical_graph
from rdflib.namespace import DCTERMS, OWL, RDF, RDFS, SH, SKOS, XSD

ROOT = Path(__file__).resolve().parents[2]
MODULE_ROOT = ROOT / "ontology" / "source" / "modules"

C = Namespace("https://w3id.org/cm-pharme/concept/")
R = Namespace("https://w3id.org/cm-pharme/relation/")
D = Namespace("https://w3id.org/cm-pharme/domain/")
META = Namespace("https://w3id.org/cm-pharme/meta/")

PREFIXES = [
    ("c", C), ("r", R), ("d", D), ("meta", META),
    ("owl", OWL), ("rdf", RDF), ("rdfs", RDFS), ("xsd", XSD),
    ("skos", SKOS), ("dcterms", DCTERMS), ("sh", SH),
]
WARNING_RELATIONS = {"CMPE-R0001", "CMPE-R0018", "CMPE-R0024", "CMPE-R0039"}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def bind_prefixes(graph: Graph) -> None:
    for prefix, ns in PREFIXES:
        graph.bind(prefix, ns, replace=True)


def canonical_graph(graph: Graph) -> Graph:
    out = Graph()
    bind_prefixes(out)
    for triple in to_canonical_graph(graph):
        out.add(triple)
    return out


def canonical_nt_bytes(graph: Graph) -> bytes:
    cg = to_canonical_graph(graph)
    lines = sorted(f"{s.n3()} {p.n3()} {o.n3()} .\n" for s, p, o in cg)
    return "".join(lines).encode("utf-8")


def graph_fingerprint(graph: Graph) -> str:
    return sha256_bytes(canonical_nt_bytes(graph))


def load_modules(module_root: Path = MODULE_ROOT) -> tuple[Graph, list[dict]]:
    modules = sorted(module_root.rglob("*.ttl"))
    if not modules:
        raise SystemExit(f"No Turtle modules found under {module_root}")
    graph = Graph()
    bind_prefixes(graph)
    records = []
    for module in modules:
        before = len(graph)
        graph.parse(module, format="turtle")
        records.append({
            "path": module.relative_to(ROOT).as_posix() if module.is_relative_to(ROOT) else module.as_posix(),
            "sha256": sha256_file(module),
            "new_triples_after_union": len(graph) - before,
            "graph_size_after_parse": len(graph),
        })
    return graph, records


def add_count(shape_graph: Graph, property_shape: URIRef, multiplicity: str | None) -> None:
    if multiplicity == "1":
        shape_graph.add((property_shape, SH.minCount, Literal(1)))
        shape_graph.add((property_shape, SH.maxCount, Literal(1)))
    elif multiplicity == "1..*":
        shape_graph.add((property_shape, SH.minCount, Literal(1)))
    elif multiplicity == "2..*":
        shape_graph.add((property_shape, SH.minCount, Literal(2)))
    elif multiplicity in (None, "0..*"):
        return
    else:
        raise ValueError(f"Unsupported multiplicity: {multiplicity}")


def generate_shapes(ontology: Graph) -> Graph:
    shapes = Graph()
    bind_prefixes(shapes)
    properties = sorted(set(ontology.subjects(RDF.type, OWL.ObjectProperty)), key=str)
    for prop in properties:
        if not str(prop).startswith(str(R)):
            continue
        status = next(ontology.objects(prop, META.status), None)
        if str(status) != "active":
            continue
        source = next(ontology.objects(prop, RDFS.domain), None)
        target = next(ontology.objects(prop, RDFS.range), None)
        if source is None or target is None:
            raise ValueError(f"Active relation lacks domain/range: {prop}")
        source_end = next(ontology.objects(prop, META.sourceEndMultiplicity), None)
        target_end = next(ontology.objects(prop, META.targetEndMultiplicity), None)
        rid = str(prop).rsplit("/", 1)[-1]
        directions = [
            ("forward", source, target, str(target_end) if target_end is not None else None),
            ("inverse", target, source, str(source_end) if source_end is not None else None),
        ]
        for direction, focus, other, multiplicity in directions:
            shape = URIRef(f"https://w3id.org/cm-pharme/shape/{rid}-{direction}")
            pshape = URIRef(f"{shape}-property")
            shapes.add((shape, RDF.type, SH.NodeShape))
            shapes.add((shape, SH.targetClass, focus))
            shapes.add((shape, SH.property, pshape))
            shapes.add((pshape, RDF.type, SH.PropertyShape))
            shapes.add((pshape, SH["class"], other))
            if direction == "forward":
                shapes.add((pshape, SH.path, prop))
            else:
                inverse_path = BNode()
                shapes.add((pshape, SH.path, inverse_path))
                shapes.add((inverse_path, SH.inversePath, prop))
            add_count(shapes, pshape, multiplicity)
            if rid in WARNING_RELATIONS:
                shapes.add((pshape, SH.severity, SH.Warning))
    return shapes


def term_sort_key(term) -> str:
    return term.n3()


def deterministic_rdfxml(graph: Graph) -> bytes:
    """Serialize RDF graph as deterministic RDF/XML using rdf:Description nodes."""
    ns_map = {
        "rdf": str(RDF),
        "rdfs": str(RDFS),
        "owl": str(OWL),
        "xsd": str(XSD),
        "skos": str(SKOS),
        "dcterms": str(DCTERMS),
        "meta": str(META),
    }
    for prefix, uri in ns_map.items():
        ET.register_namespace(prefix, uri)

    def qname(uri: str) -> str:
        for _, ns in ns_map.items():
            if uri.startswith(ns):
                return f"{{{ns}}}{uri[len(ns):]}"
        raise ValueError(f"No deterministic RDF/XML namespace mapping for predicate {uri}")

    cg = to_canonical_graph(graph)
    root = ET.Element(f"{{{RDF}}}RDF")
    subjects = sorted(set(cg.subjects()), key=term_sort_key)
    for subject in subjects:
        desc = ET.SubElement(root, f"{{{RDF}}}Description")
        if isinstance(subject, BNode):
            desc.set(f"{{{RDF}}}nodeID", str(subject))
        else:
            desc.set(f"{{{RDF}}}about", str(subject))
        pairs = sorted(cg.predicate_objects(subject), key=lambda po: (po[0].n3(), po[1].n3()))
        for predicate, obj in pairs:
            el = ET.SubElement(desc, qname(str(predicate)))
            if isinstance(obj, URIRef):
                el.set(f"{{{RDF}}}resource", str(obj))
            elif isinstance(obj, BNode):
                el.set(f"{{{RDF}}}nodeID", str(obj))
            else:
                if obj.language:
                    el.set("{http://www.w3.org/XML/1998/namespace}lang", obj.language)
                if obj.datatype:
                    el.set(f"{{{RDF}}}datatype", str(obj.datatype))
                el.text = str(obj)
    ET.indent(root, space="  ")
    body = ET.tostring(root, encoding="utf-8", xml_declaration=True, short_empty_elements=True)
    return body + (b"\n" if not body.endswith(b"\n") else b"")


def deterministic_jsonld(graph: Graph) -> bytes:
    """Serialize as deterministic expanded JSON-LD."""
    cg = to_canonical_graph(graph)
    nodes = []
    for subject in sorted(set(cg.subjects()), key=term_sort_key):
        node = {"@id": f"_:{subject}" if isinstance(subject, BNode) else str(subject)}
        by_predicate = {}
        for predicate, obj in cg.predicate_objects(subject):
            if isinstance(obj, URIRef):
                value = {"@id": str(obj)}
            elif isinstance(obj, BNode):
                value = {"@id": f"_:{obj}"}
            else:
                value = {"@value": str(obj)}
                if obj.language:
                    value["@language"] = obj.language
                if obj.datatype:
                    value["@type"] = str(obj.datatype)
            by_predicate.setdefault(str(predicate), []).append(value)
        for predicate in sorted(by_predicate):
            values = sorted(by_predicate[predicate], key=lambda v: json.dumps(v, sort_keys=True, ensure_ascii=False))
            node[predicate] = values
        nodes.append(node)
    return (json.dumps(nodes, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def serialize_graph(graph: Graph, fmt: str) -> bytes:
    cg = canonical_graph(graph)
    if fmt == "nt":
        return canonical_nt_bytes(cg)
    if fmt == "xml":
        return deterministic_rdfxml(cg)
    if fmt == "json-ld":
        return deterministic_jsonld(cg)
    data = cg.serialize(format=fmt)
    return data.encode("utf-8") if isinstance(data, str) else data


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def build(output_root: Path) -> dict:
    graph, module_records = load_modules()
    graph = canonical_graph(graph)
    shapes = canonical_graph(generate_shapes(graph))

    source_ttl = serialize_graph(graph, "turtle")
    outputs: dict[str, bytes] = {
        "source/cm-pharme.ttl": source_ttl,
        "distributions/cm-pharme.ttl": source_ttl,
        "distributions/cm-pharme.owl": serialize_graph(graph, "xml"),
        "distributions/cm-pharme.rdf": serialize_graph(graph, "xml"),
        "distributions/cm-pharme.jsonld": serialize_graph(graph, "json-ld"),
        "distributions/cm-pharme.nt": serialize_graph(graph, "nt"),
        "shapes/cm-pharme.shacl.ttl": serialize_graph(shapes, "turtle"),
    }

    for rel, data in outputs.items():
        write_bytes(output_root / rel, data)

    artifacts = []
    for rel in sorted(outputs):
        path = output_root / rel
        artifacts.append({
            "path": rel,
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        })

    manifest = {
        "schema_version": 1,
        "build_profile": "CM-PharmE-B5-reproducible-build-v1",
        "authoring_source": "ontology/source/modules/**/*.ttl",
        "source_module_count": len(module_records),
        "source_union_triples": len(graph),
        "source_graph_sha256_canonical_nt": graph_fingerprint(graph),
        "shacl_triples": len(shapes),
        "shacl_graph_sha256_canonical_nt": graph_fingerprint(shapes),
        "toolchain": {
            "python": "3.12",
            "rdflib": "7.5.0",
        },
        "modules": [{"path": item["path"], "sha256": item["sha256"]} for item in module_records],
        "artifacts": artifacts,
    }
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
    write_bytes(output_root / "validation/build-manifest.json", manifest_bytes)

    checksum_targets = [output_root / item["path"] for item in artifacts]
    checksum_targets.append(output_root / "validation/build-manifest.json")
    checksum_lines = [
        f"{sha256_file(path)}  {path.relative_to(output_root).as_posix()}\n"
        for path in sorted(checksum_targets, key=lambda p: p.relative_to(output_root).as_posix())
    ]
    write_bytes(output_root / "validation/SHA256SUMS.txt", "".join(checksum_lines).encode("utf-8"))
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", default="ontology", help="Artifact root; default writes repository ontology artifacts")
    args = parser.parse_args()
    output_root = Path(args.output_root)
    if not output_root.is_absolute():
        output_root = ROOT / output_root
    manifest = build(output_root)
    print(json.dumps({
        "status": "PASS",
        "output_root": str(output_root),
        "source_union_triples": manifest["source_union_triples"],
        "source_graph_sha256_canonical_nt": manifest["source_graph_sha256_canonical_nt"],
        "shacl_triples": manifest["shacl_triples"],
    }, indent=2))


if __name__ == "__main__":
    main()
