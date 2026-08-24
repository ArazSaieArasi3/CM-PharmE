#!/usr/bin/env python3
"""W7-E5 SHACL and data-conformance evaluation.

Evaluates the frozen Gate-E schema-faithful fixture graph against:
1) the frozen W5 SHACL profile; and
2) the frozen W7-E5 evaluation-only research-integrity profile.

It also executes predefined controlled graph mutations to test sensitivity of
selected constraints. Controlled mutations are not real-data findings and do
not estimate population-level false-positive/false-negative rates.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from pyshacl import validate
from rdflib import Graph, Namespace, RDF, URIRef
from rdflib.namespace import DCTERMS, SH

CMPE = Namespace("https://w3id.org/cm-pharme/2.0/")
PROV = Namespace("http://www.w3.org/ns/prov#")
PREFIXES = {
    "cmpe": str(CMPE),
    "prov": str(PROV),
    "dct": str(DCTERMS),
}
SEVERITY_RANK = {
    str(SH.Info): 1,
    str(SH.Warning): 2,
    str(SH.Violation): 3,
}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--kg", required=True)
    p.add_argument("--ontology", required=True)
    p.add_argument("--w5-shapes", required=True)
    p.add_argument("--e5-shapes", required=True)
    p.add_argument("--mutations", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--summary", required=True)
    return p.parse_args()


def expand(term: str) -> URIRef:
    if term.startswith("http://") or term.startswith("https://"):
        return URIRef(term)
    prefix, local = term.split(":", 1)
    return URIRef(PREFIXES[prefix] + local)


def load_graph(path: str) -> Graph:
    g = Graph()
    g.parse(path)
    return g


def merge_shapes(*paths: str) -> Graph:
    g = Graph()
    for p in paths:
        g.parse(p, format="turtle")
    return g


def result_rows(report: Graph) -> list[dict]:
    rows = []
    for r in report.subjects(RDF.type, SH.ValidationResult):
        severity = report.value(r, SH.resultSeverity)
        source_shape = report.value(r, SH.sourceShape)
        focus = report.value(r, SH.focusNode)
        path = report.value(r, SH.resultPath)
        component = report.value(r, SH.sourceConstraintComponent)
        message = report.value(r, SH.resultMessage)
        rows.append({
            "severity": str(severity) if severity else None,
            "source_shape": str(source_shape) if source_shape else None,
            "focus_node": str(focus) if focus else None,
            "path": str(path) if path else None,
            "constraint_component": str(component) if component else None,
            "message": str(message) if message else None,
        })
    rows.sort(key=lambda x: (x["severity"] or "", x["source_shape"] or "", x["focus_node"] or "", x["path"] or ""))
    return rows


def validate_graph(data: Graph, ontology: Graph, shapes: Graph):
    conforms, report_graph, report_text = validate(
        data_graph=data,
        shacl_graph=shapes,
        ont_graph=ontology,
        inference="rdfs",
        abort_on_first=False,
        allow_infos=True,
        allow_warnings=True,
        meta_shacl=True,
        advanced=True,
        debug=False,
    )
    rows = result_rows(report_graph)
    counts = Counter((r["severity"] or "unknown").rsplit("#", 1)[-1] for r in rows)
    by_shape = Counter(r["source_shape"] or "unknown" for r in rows)
    return bool(conforms), rows, dict(sorted(counts.items())), dict(sorted(by_shape.items())), report_text


def target_counts(data: Graph, shapes: Graph) -> dict:
    out = {}
    for shape in sorted(set(shapes.subjects(RDF.type, SH.NodeShape)), key=str):
        target_classes = list(shapes.objects(shape, SH.targetClass))
        count = 0
        for cls in target_classes:
            count += len(set(data.subjects(RDF.type, cls)))
        out[str(shape)] = {
            "target_classes": [str(x) for x in target_classes],
            "direct_focus_node_count": count,
        }
    return out


def first_target(data: Graph, cls: URIRef) -> URIRef:
    nodes = sorted(set(data.subjects(RDF.type, cls)), key=str)
    if not nodes:
        raise RuntimeError(f"No target node of class {cls}")
    return nodes[0]


def apply_mutation(base: Graph, case: dict) -> Graph:
    g = Graph()
    for t in base:
        g.add(t)
    op = case["operation"]
    if op == "remove_property_from_first_target":
        target = first_target(g, expand(case["target_class"]))
        prop = expand(case["property"])
        triples = list(g.triples((target, prop, None)))
        if not triples:
            raise RuntimeError(f"Mutation {case['id']} found no {prop} on {target}")
        for t in triples:
            g.remove(t)
    elif op == "add_minimal_shortage_without_jurisdiction":
        node = URIRef("https://w3id.org/cm-pharme/2.0/instance/e5-controlled/shortage-without-jurisdiction")
        g.add((node, RDF.type, CMPE.MedicineShortageSituation))
    else:
        raise RuntimeError(f"Unsupported mutation operation: {op}")
    return g


def mutation_detected(rows: list[dict], case: dict) -> tuple[bool, list[dict]]:
    min_severity = case["expected_min_severity"]
    min_rank = {"Info": 1, "Warning": 2, "Violation": 3}[min_severity]
    if case["operation"] == "remove_property_from_first_target":
        expected_path = str(expand(case["property"]))
    elif case["operation"] == "add_minimal_shortage_without_jurisdiction":
        expected_path = str(CMPE.shortageJurisdiction)
    else:
        expected_path = None

    hits = []
    for r in rows:
        sev_rank = SEVERITY_RANK.get(r["severity"] or "", 0)
        path_ok = expected_path is None or r["path"] == expected_path
        if sev_rank >= min_rank and path_ok:
            hits.append(r)
    return bool(hits), hits


def main():
    a = parse_args()
    data = load_graph(a.kg)
    ontology = load_graph(a.ontology)
    w5_shapes = load_graph(a.w5_shapes)
    e5_shapes = load_graph(a.e5_shapes)
    all_shapes = merge_shapes(a.w5_shapes, a.e5_shapes)
    mutations = json.loads(Path(a.mutations).read_text(encoding="utf-8"))

    # Validate base profiles separately and combined, preserving provenance of findings.
    w5_conforms, w5_rows, w5_sev, w5_by_shape, _ = validate_graph(data, ontology, w5_shapes)
    e5_conforms, e5_rows, e5_sev, e5_by_shape, _ = validate_graph(data, ontology, e5_shapes)
    combined_conforms, combined_rows, combined_sev, combined_by_shape, _ = validate_graph(data, ontology, all_shapes)

    mutation_results = []
    for case in mutations["cases"]:
        mutated = apply_mutation(data, case)
        conforms, rows, sev, _, _ = validate_graph(mutated, ontology, all_shapes)
        detected, hits = mutation_detected(rows, case)
        mutation_results.append({
            "id": case["id"],
            "operation": case["operation"],
            "expected_shape": str(expand(case["expected_shape"])),
            "expected_path": str(expand(case["property"])) if "property" in case else str(CMPE.shortageJurisdiction),
            "expected_min_severity": case["expected_min_severity"],
            "conforms_after_mutation": conforms,
            "detected": detected,
            "result_count": len(rows),
            "severity_counts": sev,
            "sample_hits": hits[:5],
        })

    counts = {
        "triples": len(data),
        "medicinal_product_presentations": len(set(data.subjects(RDF.type, CMPE.MedicinalProductPresentation))),
        "facilities": len(set(data.subjects(RDF.type, CMPE.Facility))),
        "source_records": len(set(data.subjects(RDF.type, CMPE.SourceRecord))),
        "identifier_assignments": len(set(data.subjects(RDF.type, CMPE.IdentifierAssignment))),
        "evidence_supports": len(set(data.subjects(RDF.type, CMPE.EvidenceSupport))),
        "observations": len(set(data.subjects(RDF.type, CMPE.ReimbursementUtilisationObservationResult))),
        "entity_matches": len(set(data.subjects(RDF.type, CMPE.EntityMatchAssertion))),
    }

    def complete(cls, prop):
        nodes = set(data.subjects(RDF.type, cls))
        satisfied = sum(1 for n in nodes if any(data.triples((n, prop, None))))
        return {"eligible": len(nodes), "complete": satisfied, "rate": (satisfied / len(nodes) if nodes else None)}

    integrity = {
        "source_record_generated_by": complete(CMPE.SourceRecord, PROV.wasGeneratedBy),
        "facility_located_in": complete(CMPE.Facility, CMPE.locatedIn),
        "observation_about": complete(CMPE.ReimbursementUtilisationObservationResult, CMPE.observationResultAbout),
        "observation_spatial": complete(CMPE.ReimbursementUtilisationObservationResult, DCTERMS.spatial),
        "observation_derived_from": complete(CMPE.ReimbursementUtilisationObservationResult, PROV.wasDerivedFrom),
        "observation_generated_by": complete(CMPE.ReimbursementUtilisationObservationResult, PROV.wasGeneratedBy),
        "identifier_entity": complete(CMPE.IdentifierAssignment, CMPE.identifierEntity),
        "identifier_scheme": complete(CMPE.IdentifierAssignment, CMPE.identifierScheme),
        "evidence_record": complete(CMPE.EvidenceSupport, CMPE.evidenceRecord),
        "evidence_assertion": complete(CMPE.EvidenceSupport, CMPE.evidenceAssertion),
    }

    mandatory_pass = (
        w5_conforms and e5_conforms and combined_conforms
        and len(combined_rows) == 0
        and all(x["detected"] for x in mutation_results)
    )

    report = {
        "schema_version": 1,
        "evidence_family": "W7-E5",
        "evidence_class": "fixture-regression",
        "gate_status": "PASS" if mandatory_pass else "FAIL",
        "fixture_graph": counts,
        "w5_profile": {
            "conforms": w5_conforms,
            "result_count": len(w5_rows),
            "severity_counts": w5_sev,
            "results_by_shape": w5_by_shape,
            "target_counts": target_counts(data, w5_shapes),
        },
        "e5_integrity_profile": {
            "conforms": e5_conforms,
            "result_count": len(e5_rows),
            "severity_counts": e5_sev,
            "results_by_shape": e5_by_shape,
            "target_counts": target_counts(data, e5_shapes),
        },
        "combined_profile": {
            "conforms": combined_conforms,
            "result_count": len(combined_rows),
            "severity_counts": combined_sev,
            "results_by_shape": combined_by_shape,
            "results": combined_rows,
        },
        "integrity_completeness": integrity,
        "controlled_mutation_review": {
            "total": len(mutation_results),
            "detected": sum(1 for x in mutation_results if x["detected"]),
            "cases": mutation_results,
            "interpretation": "Controlled sensitivity only; not a statistical false-positive/false-negative estimate."
        },
        "held_out_used": False,
        "admitted_real_data_executed": False,
        "boundary": "PASS is bounded to the Gate-E schema-faithful synthetic fixture. Real and held-out source conformance remains unevaluated in E5 and must be reported separately when executed."
    }

    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# W7-E5 SHACL and Data-Conformance Summary",
        "",
        f"- Mandatory fixture gate: **{report['gate_status']}**",
        f"- Fixture triples: **{counts['triples']}**",
        f"- W5 SHACL profile conforms: **{w5_conforms}**; results: **{len(w5_rows)}**",
        f"- W7-E5 integrity profile conforms: **{e5_conforms}**; results: **{len(e5_rows)}**",
        f"- Combined profile conforms: **{combined_conforms}**; violations/warnings/info: **{len(combined_rows)}** total",
        f"- Controlled mutation sensitivity: **{report['controlled_mutation_review']['detected']}/{report['controlled_mutation_review']['total']} detected**",
        f"- Source-record provenance completeness: **{integrity['source_record_generated_by']['complete']}/{integrity['source_record_generated_by']['eligible']}**",
        f"- Facility geography completeness: **{integrity['facility_located_in']['complete']}/{integrity['facility_located_in']['eligible']}**",
        f"- Observation provenance completeness: **{integrity['observation_derived_from']['complete']}/{integrity['observation_derived_from']['eligible']} derived-from; {integrity['observation_generated_by']['complete']}/{integrity['observation_generated_by']['eligible']} generated-by**",
        f"- Observation geography completeness: **{integrity['observation_spatial']['complete']}/{integrity['observation_spatial']['eligible']}**",
        f"- Identifier assignment completeness: **{integrity['identifier_entity']['complete']}/{integrity['identifier_entity']['eligible']} entity; {integrity['identifier_scheme']['complete']}/{integrity['identifier_scheme']['eligible']} scheme**",
        f"- EvidenceSupport completeness: **{integrity['evidence_record']['complete']}/{integrity['evidence_record']['eligible']} record; {integrity['evidence_assertion']['complete']}/{integrity['evidence_assertion']['eligible']} assertion**",
        "- Held-out H1–H3 used: **false**",
        "- Admitted full real-data graph executed in E5: **false**",
        "",
        "## Boundary",
        report["boundary"],
        "",
        "Controlled mutations establish sensitivity for selected registered constraints only. A conforming synthetic fixture does not establish real-world data quality or domain completeness."
    ]
    Path(a.summary).parent.mkdir(parents=True, exist_ok=True)
    Path(a.summary).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))

    if not mandatory_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
