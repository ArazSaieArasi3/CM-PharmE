#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef

CMPE = Namespace("https://w3id.org/cm-pharme/2.0/")
EX = Namespace("https://w3id.org/cm-pharme/2.0/evaluation/e12/")

MODULES = [
    "v2/ontology/source/modules/00-metadata.ttl",
    "v2/ontology/source/modules/10-core.ttl",
    "v2/ontology/source/modules/20-xinfra.ttl",
    "v2/ontology/source/modules/25-gate-d-disjointness.ttl",
    "v2/ontology/source/modules/30-extensions.ttl",
    "v2/ontology/source/modules/40-mappings.ttl",
]

QUERIES = {
    "RES-01": """
PREFIX cmpe: <https://w3id.org/cm-pharme/2.0/>
PREFIX ex: <https://w3id.org/cm-pharme/2.0/evaluation/e12/>
ASK {
  ex:res01_critical a cmpe:CriticalMedicineClassification ;
    cmpe:contextClassificationProduct ex:res01_product ;
    cmpe:contextClassificationJurisdiction ex:res01_jurisdiction .
  ex:res01_dependency a cmpe:SupplyDependency ;
    cmpe:dependencyDependent ex:res01_product ;
    cmpe:dependencyProvider ex:res01_provider .
  ex:res01_disruption a cmpe:DisruptionEvent ; cmpe:disruptionAffects ex:res01_provider .
  ex:res01_shortage a cmpe:MedicineShortageSituation ;
    cmpe:shortageProduct ex:res01_product ;
    cmpe:shortageJurisdiction ex:res01_jurisdiction .
}
""",
    "RES-02": """
PREFIX cmpe: <https://w3id.org/cm-pharme/2.0/>
PREFIX ex: <https://w3id.org/cm-pharme/2.0/evaluation/e12/>
ASK {
  ex:res02_dependency a cmpe:SupplyDependency ;
    cmpe:dependencyDependent ex:res02_product ;
    cmpe:dependencyProvider ex:res02_provider .
  ex:res02_disruption a cmpe:DisruptionEvent ; cmpe:disruptionAffects ex:res02_provider .
  ex:res02_alternative_assignment a cmpe:AlternativeMedicineAssignment ;
    cmpe:alternativeForProduct ex:res02_product ;
    cmpe:alternativeProduct ex:res02_alternative .
}
""",
    "RES-03": """
PREFIX cmpe: <https://w3id.org/cm-pharme/2.0/>
PREFIX ex: <https://w3id.org/cm-pharme/2.0/evaluation/e12/>
ASK {
  ex:res03_shortage a cmpe:MedicineShortageSituation ; cmpe:shortageJurisdiction ?jurisdiction .
  ex:res03_facility a cmpe:Facility ; cmpe:locatedIn ?region .
  FILTER (?jurisdiction != ?region)
}
""",
    "RES-04": """
PREFIX cmpe: <https://w3id.org/cm-pharme/2.0/>
PREFIX ex: <https://w3id.org/cm-pharme/2.0/evaluation/e12/>
ASK {
  ex:res04_vulnerability a cmpe:Vulnerability .
  ex:res04_plan a cmpe:RiskTreatmentPlan .
  ex:res04_activity a cmpe:RiskTreatmentActivity ; cmpe:riskTreatmentAddresses ex:res04_vulnerability .
}
""",
    "RES-05": """
PREFIX cmpe: <https://w3id.org/cm-pharme/2.0/>
PREFIX ex: <https://w3id.org/cm-pharme/2.0/evaluation/e12/>
ASK {
  ex:res05_dependency a cmpe:SupplyDependency ;
    cmpe:dependencyDependent ex:res05_product ;
    cmpe:dependencyProvider ?provider .
  ex:res05_disruption a cmpe:DisruptionEvent ; cmpe:disruptionAffects ?provider .
}
""",
}


def load_graph(paths):
    g = Graph()
    for path in paths:
        g.parse(path, format="turtle")
    return g


def local(uri):
    text = str(uri)
    return text.rsplit("/", 1)[-1].rsplit("#", 1)[-1]


def ontology_term_exists(graph, name, kind):
    uri = CMPE[name]
    if kind == "class":
        return (uri, RDF.type, OWL.Class) in graph or (uri, RDF.type, RDFS.Datatype) in graph
    return (uri, RDF.type, OWL.ObjectProperty) in graph or (uri, RDF.type, OWL.DatatypeProperty) in graph


def ask(graph, query):
    result = graph.query(query)
    return bool(result.askAnswer)


def provenance_ok(graph, sid):
    suffix = sid.lower().replace("-", "")
    record = EX[f"{suffix}_record"]
    assertion = EX[f"{suffix}_assertion"]
    support = EX[f"{suffix}_support"]
    return all([
        (record, RDF.type, CMPE.SourceRecord) in graph,
        (assertion, RDF.type, CMPE.Assertion) in graph,
        (support, RDF.type, CMPE.EvidenceSupport) in graph,
        (support, CMPE.evidenceRecord, record) in graph,
        (support, CMPE.evidenceAssertion, assertion) in graph,
        (EX.scenarioRelease, CMPE.containsSourceRecord, record) in graph,
    ])


def detect_extension_gaps(ontology):
    recovery_terms = sorted({local(s) for s in ontology.subjects() if isinstance(s, URIRef) and str(s).startswith(str(CMPE)) and "recover" in local(s).lower()})
    plan_activity_links = []
    vulnerability_domain_properties = []
    for prop in ontology.subjects(RDF.type, OWL.ObjectProperty):
        if (prop, RDFS.domain, CMPE.RiskTreatmentPlan) in ontology and (prop, RDFS.range, CMPE.RiskTreatmentActivity) in ontology:
            plan_activity_links.append(local(prop))
        if (prop, RDFS.domain, CMPE.Vulnerability) in ontology:
            vulnerability_domain_properties.append(local(prop))
    return {
        "explicit_recovery_terms": recovery_terms,
        "risk_treatment_plan_to_activity_properties": sorted(plan_activity_links),
        "vulnerability_domain_properties": sorted(vulnerability_domain_properties),
        "expected_gaps_detected": {
            "explicit_recovery_semantics_missing": len(recovery_terms) == 0,
            "risk_treatment_plan_activity_link_missing": len(plan_activity_links) == 0,
            "vulnerability_bearer_property_missing": len(vulnerability_domain_properties) == 0,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default="v2/evaluation/protocol/e12-resilience-scenario-registry.json")
    parser.add_argument("--scenarios", default="v2/evaluation/protocol/e12-resilience-scenarios.ttl")
    parser.add_argument("--output", required=True)
    parser.add_argument("--summary", required=True)
    args = parser.parse_args()

    registry = json.loads(Path(args.registry).read_text())
    ontology = load_graph(MODULES)
    scenarios = load_graph([args.scenarios])
    combined = ontology + scenarios

    scenario_results = []
    all_terms_ok = True
    all_queries_ok = True
    all_provenance_ok = True

    for scenario in registry["scenarios"]:
        sid = scenario["id"]
        class_checks = {name: ontology_term_exists(ontology, name, "class") for name in scenario.get("required_classes", [])}
        property_checks = {name: ontology_term_exists(ontology, name, "property") for name in scenario.get("required_properties", [])}
        term_ok = all(class_checks.values()) and all(property_checks.values())
        baseline = ask(combined, QUERIES[sid])
        expected = scenario.get("expected_query_outcome", scenario.get("expected_query_outcome_before_removal"))
        query_ok = baseline == expected
        prov = provenance_ok(scenarios, sid)
        all_terms_ok = all_terms_ok and term_ok
        all_queries_ok = all_queries_ok and query_ok
        all_provenance_ok = all_provenance_ok and prov
        scenario_results.append({
            "id": sid,
            "expected_representability": scenario["expected_representability"],
            "class_term_checks": class_checks,
            "property_term_checks": property_checks,
            "all_required_terms_resolve": term_ok,
            "baseline_query_result": baseline,
            "expected_query_result": expected,
            "query_matches_frozen_expectation": query_ok,
            "provenance_complete": prov,
            "expected_gap": scenario.get("expected_gap"),
        })

    # Controlled missing-evidence sensitivity mutation for RES-05.
    mutated = Graph()
    for triple in combined:
        mutated.add(triple)
    mutated.remove((EX.res05_dependency, CMPE.dependencyProvider, EX.res05_provider))
    before = ask(combined, QUERIES["RES-05"])
    after = ask(mutated, QUERIES["RES-05"])
    sensitivity_ok = before is True and after is False

    gaps = detect_extension_gaps(ontology)
    expected_gap_flags = gaps["expected_gaps_detected"]
    expected_gaps_ok = all(expected_gap_flags.values())

    representability_counts = {
        "EXACT": sum(1 for s in registry["scenarios"] if s["expected_representability"] == "EXACT"),
        "PARTIAL": sum(1 for s in registry["scenarios"] if s["expected_representability"] == "PARTIAL"),
        "EXACT_TEST_MECHANISM": sum(1 for s in registry["scenarios"] if s["expected_representability"] == "EXACT_TEST_MECHANISM"),
    }

    passed = all([all_terms_ok, all_queries_ok, all_provenance_ok, sensitivity_ok, expected_gaps_ok])
    report = {
        "schema_version": 1,
        "family": "W7-E12",
        "mandatory_gate_passed": passed,
        "family_status": "PASS_WITH_WARNING" if passed else "FAIL",
        "scenario_count": len(registry["scenarios"]),
        "representability_counts": representability_counts,
        "scenario_queries_matching_frozen_expectations": sum(1 for r in scenario_results if r["query_matches_frozen_expectation"]),
        "scenario_provenance_complete": sum(1 for r in scenario_results if r["provenance_complete"]),
        "scenario_results": scenario_results,
        "missing_evidence_sensitivity": {
            "baseline_exposure_query": before,
            "after_dependency_provider_removed": after,
            "passed": sensitivity_ok,
            "interpretation": "INSUFFICIENT_EVIDENCE_NOT_RESILIENCE" if sensitivity_ok else "UNEXPECTED",
        },
        "extension_gap_taxonomy": gaps,
        "first_pass_ontology_changes": 0,
        "claim_boundary": registry["claim_boundary"],
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")

    md = [
        "# W7-E12 Pharmaceutical Resilience Scenario Evaluation",
        "",
        f"- Mandatory gate: **{'PASS' if passed else 'FAIL'}**",
        f"- Family status: **{report['family_status']}**",
        f"- Frozen scenarios: **{report['scenario_count']}**",
        f"- Expected representability: **{representability_counts['EXACT']} exact + {representability_counts['PARTIAL']} partial + {representability_counts['EXACT_TEST_MECHANISM']} sensitivity mechanism**",
        f"- Scenario queries matching frozen expectations: **{report['scenario_queries_matching_frozen_expectations']}/{report['scenario_count']}**",
        f"- Scenario provenance complete: **{report['scenario_provenance_complete']}/{report['scenario_count']}**",
        f"- Missing-evidence sensitivity: **{'PASS' if sensitivity_ok else 'FAIL'}** (true → false after provider-edge removal; interpreted as evidence insufficiency, not resilience)",
        f"- First-pass ontology changes: **{report['first_pass_ontology_changes']}**",
        "",
        "## Retained extension gaps",
        f"- Explicit recovery semantics missing: **{expected_gap_flags['explicit_recovery_semantics_missing']}**",
        f"- RiskTreatmentPlan→RiskTreatmentActivity property missing: **{expected_gap_flags['risk_treatment_plan_activity_link_missing']}**",
        f"- Vulnerability bearer/domain property missing: **{expected_gap_flags['vulnerability_bearer_property_missing']}**",
        "",
        "## Boundary",
        registry["claim_boundary"],
    ]
    Path(args.summary).write_text("\n".join(md) + "\n")
    print("\n".join(md))
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
