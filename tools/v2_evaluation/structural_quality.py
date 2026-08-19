#!/usr/bin/env python3
"""W7-E1 syntactic, structural and ontology-quality evaluation.

This evaluator is intentionally narrower than semantic completeness assessment.
It checks the frozen formal baseline, conceptual-registry coverage, protected
Gate-D distinctions, registered ontology↔RDB IRI resolution and descriptive
annotation/structure indicators.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef, Literal
from rdflib.collection import Collection
from rdflib.compare import to_canonical_graph

CMPE_NS = "https://w3id.org/cm-pharme/2.0/"
CMPE = Namespace(CMPE_NS)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--source-dir", default="v2/ontology/source/modules")
    p.add_argument("--conceptual-model", default="v2/ontouml/cm-pharme-v2.conceptual-model.json")
    p.add_argument("--baseline", default="v2/ontology/baseline/formal-baseline.json")
    p.add_argument("--mapping-registry", default="v2/data/mappings/ontology-rdb-mapping.csv")
    p.add_argument("--output", default="build/w7-e1/structural-quality.json")
    return p.parse_args()


def canonical_sha256(graph: Graph) -> str:
    cg = to_canonical_graph(graph)
    lines = sorted(f"{s.n3()} {p.n3()} {o.n3()} .\n" for s, p, o in cg)
    return hashlib.sha256("".join(lines).encode("utf-8")).hexdigest()


def explicit_disjoint(graph: Graph, a: URIRef, b: URIRef) -> bool:
    if (a, OWL.disjointWith, b) in graph or (b, OWL.disjointWith, a) in graph:
        return True
    for node in graph.subjects(RDF.type, OWL.AllDisjointClasses):
        members = graph.value(node, OWL.members)
        if members is None:
            continue
        try:
            vals = set(Collection(graph, members))
        except Exception:
            continue
        if a in vals and b in vals:
            return True
    return False


def in_graph(graph: Graph, iri: URIRef) -> bool:
    return any(graph.triples((iri, None, None))) or any(graph.triples((None, None, iri)))


def label_stats(graph: Graph, terms: set[URIRef]) -> dict:
    labelled = {t for t in terms if any(graph.objects(t, RDFS.label))}
    labels = []
    for term in terms:
        for label in graph.objects(term, RDFS.label):
            labels.append((str(label).strip().lower(), str(term)))
    counts = Counter(l for l, _ in labels if l)
    duplicate_labels = sorted([l for l, n in counts.items() if n > 1])
    return {
        "term_count": len(terms),
        "labelled_terms": len(labelled),
        "label_coverage": round(len(labelled) / len(terms), 6) if terms else 1.0,
        "duplicate_label_count": len(duplicate_labels),
        "duplicate_labels": duplicate_labels,
    }


def main():
    a = parse_args()
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    source_files = sorted(Path(a.source_dir).glob("*.ttl"))
    if not source_files:
        raise SystemExit("No authoritative Turtle modules found")

    graph = Graph()
    parse_results = {}
    for path in source_files:
        try:
            module = Graph().parse(path, format="turtle")
            parse_results[str(path)] = {"parsed": True, "triples": len(module)}
            graph += module
        except Exception as exc:
            parse_results[str(path)] = {"parsed": False, "error": str(exc)}

    parse_pass = all(v.get("parsed") for v in parse_results.values())
    if not parse_pass:
        result = {"schema_version": 1, "family": "W7-E1", "passed": False, "parse_results": parse_results}
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        raise SystemExit("One or more authoritative modules failed to parse")

    model = json.loads(Path(a.conceptual_model).read_text(encoding="utf-8"))
    baseline = json.loads(Path(a.baseline).read_text(encoding="utf-8"))

    owl_classes = {x for x in graph.subjects(RDF.type, OWL.Class) if isinstance(x, URIRef)}
    datatypes = {x for x in graph.subjects(RDF.type, RDFS.Datatype) if isinstance(x, URIRef)}
    object_props = {x for x in graph.subjects(RDF.type, OWL.ObjectProperty) if isinstance(x, URIRef)}
    datatype_props = {x for x in graph.subjects(RDF.type, OWL.DatatypeProperty) if isinstance(x, URIRef)}
    declared_terms = owl_classes | datatypes | object_props | datatype_props
    internal_declared = {x for x in declared_terms if str(x).startswith(CMPE_NS)}

    counts = {
        "triples": len(graph),
        "owl_classes": len(owl_classes),
        "rdfs_datatypes": len(datatypes),
        "object_properties": len(object_props),
        "datatype_properties": len(datatype_props),
    }
    expected_counts = {
        "owl_classes": baseline["expected_owl_classes"],
        "rdfs_datatypes": baseline["expected_rdfs_datatypes"],
        "object_properties": baseline["expected_object_properties"],
        "datatype_properties": baseline["expected_datatype_properties"],
    }
    count_checks = {k: counts[k] == v for k, v in expected_counts.items()}

    fingerprint = canonical_sha256(graph)
    expected_fingerprint = baseline.get("canonical_graph_sha256")
    fingerprint_match = expected_fingerprint is None or fingerprint == expected_fingerprint

    conceptual_rows = []
    for module_name, pairs in model["modules"].items():
        for name, stereotype in pairs:
            conceptual_rows.append((module_name, name, stereotype))
    conceptual_missing = []
    for module_name, name, stereotype in conceptual_rows:
        iri = URIRef(model["namespace"] + name)
        if iri not in owl_classes and iri not in datatypes:
            conceptual_missing.append({"module": module_name, "name": name, "stereotype": stereotype})
    conceptual_coverage = {
        "expected": len(conceptual_rows),
        "resolved": len(conceptual_rows) - len(conceptual_missing),
        "missing": conceptual_missing,
    }

    protected = {}
    for left, right in model["protected_distinctions"]:
        protected[f"{left}!={right}"] = explicit_disjoint(
            graph, URIRef(model["namespace"] + left), URIRef(model["namespace"] + right)
        )

    mapping_rows = []
    with open(a.mapping_registry, encoding="utf-8-sig", newline="") as f:
        mapping_rows = list(csv.DictReader(f))
    mapping_unresolved = []
    for row in mapping_rows:
        iri_text = (row.get("ontology_iri") or "").strip()
        if not iri_text:
            mapping_unresolved.append({"mapping_id": row.get("mapping_id"), "reason": "missing ontology_iri"})
            continue
        iri = URIRef(iri_text)
        if not in_graph(graph, iri):
            mapping_unresolved.append({"mapping_id": row.get("mapping_id"), "ontology_iri": iri_text})
    mapping_resolution = {
        "registered_rows": len(mapping_rows),
        "resolved_rows": len(mapping_rows) - len(mapping_unresolved),
        "unresolved": mapping_unresolved,
    }

    # Descriptive quality indicators. These are reported but are not universal
    # pass/fail completeness thresholds.
    label_quality = label_stats(graph, internal_declared)
    prop_terms = object_props | datatype_props
    domain_count = sum(1 for p in prop_terms if any(graph.objects(p, RDFS.domain)))
    range_count = sum(1 for p in prop_terms if any(graph.objects(p, RDFS.range)))
    deprecated_terms = sorted(
        str(s) for s, _, o in graph.triples((None, OWL.deprecated, None))
        if isinstance(s, URIRef) and str(s).startswith(CMPE_NS) and isinstance(o, Literal) and str(o).lower() in {"true", "1"}
    )

    mandatory_checks = {
        "all_authoritative_modules_parse": parse_pass,
        "frozen_inventory_counts_match": all(count_checks.values()),
        "frozen_canonical_fingerprint_matches": fingerprint_match,
        "conceptual_registry_fully_resolves": not conceptual_missing,
        "protected_gate_d_distinctions_intact": all(protected.values()),
        "ontology_rdb_registry_fully_resolves": not mapping_unresolved,
    }
    passed = all(mandatory_checks.values())

    result = {
        "schema_version": 1,
        "family": "W7-E1",
        "issue": 90,
        "evaluation_target_baseline": baseline.get("formal_version", "2.0.0-alpha.1"),
        "passed": passed,
        "mandatory_checks": mandatory_checks,
        "parse_results": parse_results,
        "counts": counts,
        "expected_counts": expected_counts,
        "count_checks": count_checks,
        "canonical_graph_sha256": fingerprint,
        "expected_canonical_graph_sha256": expected_fingerprint,
        "conceptual_registry": conceptual_coverage,
        "protected_distinctions": protected,
        "ontology_rdb_mapping_resolution": mapping_resolution,
        "descriptive_quality": {
            "internal_declared_term_labels": label_quality,
            "property_domain_declarations": domain_count,
            "property_range_declarations": range_count,
            "property_count": len(prop_terms),
            "deprecated_internal_terms": deprecated_terms,
        },
        "interpretation_boundary": [
            "Structural and annotation indicators do not establish domain completeness.",
            "Mapping IRI resolution establishes registry referential integrity, not mapping correctness.",
            "Formal inventory stability is evaluated against the frozen W5 baseline."
        ],
    }
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not passed:
        raise SystemExit("W7-E1 mandatory structural checks failed")


if __name__ == "__main__":
    main()
