#!/usr/bin/env python3
"""Validate CM-PharmE generated artifacts against pinned B3 fingerprints."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from rdflib import Graph, Literal, Namespace
from rdflib.compare import to_canonical_graph, to_isomorphic
from rdflib.namespace import DCTERMS, OWL, RDF, SH, SKOS, XSD

ROOT = Path(__file__).resolve().parents[2]
C = Namespace("https://w3id.org/cm-pharme/concept/")
R = Namespace("https://w3id.org/cm-pharme/relation/")
D = Namespace("https://w3id.org/cm-pharme/domain/")
META = Namespace("https://w3id.org/cm-pharme/meta/")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def graph_fingerprint(graph: Graph) -> str:
    cg = to_canonical_graph(graph)
    lines = sorted(f"{s.n3()} {p.n3()} {o.n3()} .\n" for s, p, o in cg)
    return hashlib.sha256("".join(lines).encode("utf-8")).hexdigest()


def parse(path: Path, fmt: str) -> Graph:
    graph = Graph()
    graph.parse(path, format=fmt)
    return graph


def load_module_union() -> Graph:
    graph = Graph()
    modules = sorted((ROOT / "ontology/source/modules").rglob("*.ttl"))
    if not modules:
        raise SystemExit("No authoring modules found")
    for module in modules:
        graph.parse(module, format="turtle")
    return graph


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", default="ontology")
    parser.add_argument("--report", default="ontology/validation/quality-report.json")
    args = parser.parse_args()

    artifact_root = Path(args.artifact_root)
    if not artifact_root.is_absolute():
        artifact_root = ROOT / artifact_root
    report_path = Path(args.report)
    if not report_path.is_absolute():
        report_path = ROOT / report_path

    fingerprints = json.loads((ROOT / "ontology/validation/b3-reference-fingerprints.json").read_text(encoding="utf-8"))
    module_graph = load_module_union()
    canonical = parse(artifact_root / "source/cm-pharme.ttl", "turtle")
    shapes = parse(artifact_root / "shapes/cm-pharme.shacl.ttl", "turtle")
    distributions = {
        "distributions/cm-pharme.ttl": "turtle",
        "distributions/cm-pharme.owl": "xml",
        "distributions/cm-pharme.rdf": "xml",
        "distributions/cm-pharme.jsonld": "json-ld",
        "distributions/cm-pharme.nt": "nt",
    }
    distribution_graphs = {rel: parse(artifact_root / rel, fmt) for rel, fmt in distributions.items()}

    manifest = json.loads((artifact_root / "validation/build-manifest.json").read_text(encoding="utf-8"))
    manifest_hashes = {item["path"]: item["sha256"] for item in manifest["artifacts"]}
    artifact_hash_match = {
        rel: sha256_file(artifact_root / rel) == expected
        for rel, expected in manifest_hashes.items()
    }

    counts = {
        "concept_class_count": sum(1 for s in canonical.subjects(RDF.type, OWL.Class) if str(s).startswith(str(C))),
        "relation_object_property_count": sum(1 for s in canonical.subjects(RDF.type, OWL.ObjectProperty) if str(s).startswith(str(R))),
        "generalization_record_count": sum(1 for s in canonical.subjects(RDF.type, META.GeneralizationRecord) if str(s).startswith(str(R))),
        "domain_count": sum(1 for s in canonical.subjects(RDF.type, SKOS.Concept) if str(s).startswith(str(D))),
        "owl_restriction_count": sum(1 for _ in canonical.subjects(RDF.type, OWL.Restriction)),
        "shacl_node_shape_count": sum(1 for _ in shapes.subjects(RDF.type, SH.NodeShape)),
        "shacl_property_shape_count": sum(1 for _ in shapes.subjects(RDF.type, SH.PropertyShape)),
    }
    expected_counts = {
        "concept_class_count": 39,
        "relation_object_property_count": 39,
        "generalization_record_count": 1,
        "domain_count": 5,
        "owl_restriction_count": 42,
        "shacl_node_shape_count": 76,
        "shacl_property_shape_count": 76,
    }

    checks = {
        "module_union_matches_generated_source": to_isomorphic(module_graph) == to_isomorphic(canonical),
        "module_union_triples_match_reference": len(module_graph) == fingerprints["ontology"]["triples"],
        "module_union_graph_fingerprint_matches_reference": graph_fingerprint(module_graph) == fingerprints["ontology"]["canonical_nt_sha256"],
        "generated_source_graph_fingerprint_matches_reference": graph_fingerprint(canonical) == fingerprints["ontology"]["canonical_nt_sha256"],
        "generated_shapes_match_reference": graph_fingerprint(shapes) == fingerprints["shacl"]["canonical_nt_sha256"],
        "generated_shapes_triples_match_reference": len(shapes) == fingerprints["shacl"]["triples"],
        "all_distributions_isomorphic_to_source": all(to_isomorphic(g) == to_isomorphic(canonical) for g in distribution_graphs.values()),
        "all_manifest_artifact_hashes_match": all(artifact_hash_match.values()),
        "counts_match_expected": counts == expected_counts,
        "r0011_deprecated": (R["CMPE-R0011"], OWL.deprecated, Literal(True, datatype=XSD.boolean)) in canonical,
        "r0011_replaced_by_r0027": (R["CMPE-R0011"], DCTERMS.isReplacedBy, R["CMPE-R0027"]) in canonical,
        "r0031_normalized_label": (R["CMPE-R0031"], SKOS.prefLabel, Literal("constrains")) in canonical,
        "c0025_canonical_relator": (C["CMPE-C0025"], META.stereotype, META.Relator) in canonical,
        "historical_example_org_namespace_absent": not any("example.org" in str(term) for triple in canonical for term in triple),
        "historical_converter_cardinality_classes_absent": all(
            str(s).split("/")[-1] not in {"0..*", "1", "1..*", "2..*"}
            for s in canonical.subjects(RDF.type, OWL.Class)
        ),
    }

    status = "PASS" if all(checks.values()) else "FAIL"
    report = {
        "schema_version": 1,
        "validation_profile": "CM-PharmE-B5-quality-gates-v1",
        "status": status,
        "ontology_triples": len(canonical),
        "ontology_graph_sha256_canonical_nt": graph_fingerprint(canonical),
        "shacl_triples": len(shapes),
        "shacl_graph_sha256_canonical_nt": graph_fingerprint(shapes),
        "counts": counts,
        "expected_counts": expected_counts,
        "artifact_hash_match": artifact_hash_match,
        "checks": checks,
        "evidential_boundary": "Build/logic/structure reproducibility does not establish domain completeness, empirical effectiveness, or resolve B4 semantic refinement candidates.",
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
