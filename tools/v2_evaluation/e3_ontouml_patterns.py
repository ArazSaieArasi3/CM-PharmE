#!/usr/bin/env python3
"""Execute the CM-PharmE 2.0 W7-E3 project-native OntoUML pattern checks.

This evaluator checks the frozen Gate-D conceptual registry against the W5 OWL
projection. It is deliberately NOT an official OntoUML parser or official
OntoUML anti-pattern tool. Its purpose is to make the already-frozen W4/W7
semantic commitments executable and auditable.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from collections import defaultdict

from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef, Literal
from rdflib.collection import Collection

CMPE = Namespace("https://w3id.org/cm-pharme/2.0/")
CMMETA = Namespace("https://w3id.org/cm-pharme/2.0/meta/")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--source-dir", default="v2/ontology/source/modules")
    p.add_argument("--conceptual-model", default="v2/ontouml/cm-pharme-v2.conceptual-model.json")
    p.add_argument("--checks", default="v2/evaluation/protocol/e3-pattern-checks.json")
    p.add_argument("--output", required=True)
    return p.parse_args()


def load_union(source_dir: Path) -> Graph:
    g = Graph()
    files = sorted(source_dir.glob("*.ttl"))
    if not files:
        raise SystemExit(f"No Turtle modules found in {source_dir}")
    for path in files:
        g.parse(path, format="turtle")
    return g


def concept_rows(model: dict):
    for module, pairs in model["modules"].items():
        for name, stereotype in pairs:
            yield module, name, stereotype


def explicit_disjoint(g: Graph, a: URIRef, b: URIRef) -> bool:
    if (a, OWL.disjointWith, b) in g or (b, OWL.disjointWith, a) in g:
        return True
    for node in g.subjects(RDF.type, OWL.AllDisjointClasses):
        members = g.value(node, OWL.members)
        if members is None:
            continue
        try:
            vals = set(Collection(g, members))
        except Exception:
            continue
        if a in vals and b in vals:
            return True
    return False


def local(term: URIRef | str) -> str:
    return str(term).rsplit("/", 1)[-1]


def add(checks_out, check_id, category, status, message, evidence=None, blocking=False):
    checks_out.append({
        "id": check_id,
        "category": category,
        "status": status,
        "blocking": bool(blocking),
        "message": message,
        "evidence": evidence or {},
    })


def main():
    args = parse_args()
    graph = load_union(Path(args.source_dir))
    model = json.loads(Path(args.conceptual_model).read_text(encoding="utf-8"))
    registry = json.loads(Path(args.checks).read_text(encoding="utf-8"))
    out = []

    # Boundary / registry integrity.
    add(out, "E3-01", "boundary", "PASS" if model.get("official_ontouml_json") is False else "FAIL",
        "Project-native conceptual registry is explicitly not claimed as official OntoUML JSON.",
        {"official_ontouml_json": model.get("official_ontouml_json")}, blocking=True)

    rows = list(concept_rows(model))
    allowed = set(registry["allowed_stereotypes"])
    invalid_st = [(n, s) for _, n, s in rows if s not in allowed]
    add(out, "E3-02", "stereotype-discipline", "PASS" if not invalid_st else "FAIL",
        "All conceptual stereotypes belong to the frozen project vocabulary." if not invalid_st else "Unexpected stereotypes found.",
        {"invalid": invalid_st, "count": len(rows)}, blocking=True)

    mismatches = []
    missing = []
    for module, name, stereotype in rows:
        iri = URIRef(model["namespace"] + name)
        formal = [str(x) for x in graph.objects(iri, CMMETA.ontoumlStereotype)]
        if not formal:
            missing.append(name)
        elif stereotype not in formal:
            mismatches.append({"name": name, "registry": stereotype, "formal": formal})
    add(out, "E3-03", "stereotype-discipline", "PASS" if not missing and not mismatches else "FAIL",
        "Gate-D stereotype registry and OWL projection agree for all conceptual elements." if not missing and not mismatches else "Registry/formal stereotype mismatch.",
        {"resolved": len(rows) - len(missing), "total": len(rows), "missing": missing, "mismatches": mismatches}, blocking=True)

    # Role grounding / identity providers.
    role_failures = []
    role_count = 0
    for identity_name, role_names in registry["role_grounding"].items():
        identity = CMPE[identity_name]
        for role_name in role_names:
            role_count += 1
            role = CMPE[role_name]
            ok_identity = (role, RDFS.subClassOf, identity) in graph
            ok_participant = (role, RDFS.subClassOf, CMPE.EcosystemParticipant) in graph
            if not (ok_identity and ok_participant):
                role_failures.append({"role": role_name, "identity": identity_name, "identity_grounded": ok_identity, "ecosystem_participant": ok_participant})
    add(out, "E3-04", "role-kind-discipline", "PASS" if not role_failures else "FAIL",
        "Concrete Roles are grounded in the expected identity-providing Kind and EcosystemParticipant RoleMixin." if not role_failures else "One or more Roles lack expected grounding.",
        {"roles_checked": role_count, "failures": role_failures}, blocking=True)

    # Relator mediation proxies: outgoing properties whose domain is the Relator.
    by_domain = defaultdict(list)
    for p in graph.subjects(RDF.type, OWL.ObjectProperty):
        for d in graph.objects(p, RDFS.domain):
            if isinstance(d, URIRef):
                by_domain[d].append(p)
    relator_failures = []
    relator_counts = {}
    for rel_name, minimum in registry["principal_relator_mediation_minimum"].items():
        rel = CMPE[rel_name]
        props = sorted(local(p) for p in by_domain.get(rel, []))
        relator_counts[rel_name] = props
        if len(props) < minimum:
            relator_failures.append({"relator": rel_name, "minimum": minimum, "properties": props})
    add(out, "E3-05", "relator-mediation", "PASS" if not relator_failures else "FAIL",
        "Principal Relator patterns have at least the frozen minimum number of explicit participant-facing properties." if not relator_failures else "Principal Relator mediation proxy is incomplete.",
        {"relators": relator_counts, "failures": relator_failures}, blocking=True)

    extension_gaps = []
    for rel_name in registry["extension_relators_review_only"]:
        props = sorted(local(p) for p in by_domain.get(CMPE[rel_name], []))
        if len(props) < 2:
            extension_gaps.append({"relator": rel_name, "participant_properties": props})
    add(out, "E3-06", "relator-mediation", "WARN" if extension_gaps else "PASS",
        "Extension-only Relators with incomplete OWL mediation remain bounded implementation gaps." if extension_gaps else "Reviewed extension Relators expose mediation properties.",
        {"gaps": extension_gaps}, blocking=False)

    # Material relation truth-maker marker.
    operates_ok = (
        (CMPE.operates, RDF.type, OWL.ObjectProperty) in graph
        and any(str(v).lower() == "true" for v in graph.objects(CMPE.operates, CMMETA.materialRelation))
        and any(str(v) == "FacilityOperation" for v in graph.objects(CMPE.operates, CMMETA.derivedFromRelator))
    )
    add(out, "E3-07", "material-relation", "PASS" if operates_ok else "FAIL",
        "The operates material relation is explicitly tied to FacilityOperation as its Relator pattern." if operates_ok else "The operates material relation lacks its frozen truth-maker metadata.",
        {}, blocking=True)

    # Protected distinctions.
    distinction_results = {}
    missing_dist = []
    for left, right in registry["mandatory_protected_distinctions"]:
        ok = explicit_disjoint(graph, CMPE[left], CMPE[right])
        distinction_results[f"{left}!={right}"] = ok
        if not ok:
            missing_dist.append([left, right])
    add(out, "E3-08", "identity-separation", "PASS" if not missing_dist else "FAIL",
        "All eight Gate-D protected distinctions remain explicit in the OWL projection." if not missing_dist else "One or more protected distinctions are missing.",
        {"results": distinction_results}, blocking=True)

    # Contextual classification: no rigid Product subtype shortcut.
    cc_failures = []
    for name in registry["contextual_classification_subclasses"]:
        iri = CMPE[name]
        if (iri, RDFS.subClassOf, CMPE.ContextualMedicineClassificationAssignment) not in graph:
            cc_failures.append({"name": name, "missing_assignment_subclass": True})
        if (iri, RDFS.subClassOf, CMPE.MedicinalProduct) in graph:
            cc_failures.append({"name": name, "incorrect_product_subclass": True})
    add(out, "E3-09", "contextual-classification", "PASS" if not cc_failures else "FAIL",
        "Essential/Critical medicine concepts remain contextual assignment specializations, not rigid MedicinalProduct subtypes." if not cc_failures else "Contextual classification pattern violation.",
        {"failures": cc_failures}, blocking=True)

    # Event/situation discipline.
    es_failures = []
    model_map = {name: stereotype for _, name, stereotype in rows}
    for name, expected in registry["expected_event_situation_stereotypes"].items():
        if model_map.get(name) != expected:
            es_failures.append({"name": name, "expected": expected, "actual": model_map.get(name)})
    add(out, "E3-10", "event-situation", "PASS" if not es_failures else "FAIL",
        "Frozen Event/Situation distinctions are preserved." if not es_failures else "Event/Situation stereotype mismatch.",
        {"failures": es_failures}, blocking=True)

    # Mode/Quality discipline.
    mq_failures = []
    for name, expected in registry["expected_mode_quality_stereotypes"].items():
        if model_map.get(name) != expected:
            mq_failures.append({"name": name, "expected": expected, "actual": model_map.get(name)})
    add(out, "E3-11", "mode-quality", "PASS" if not mq_failures else "FAIL",
        "Frozen Mode/Quality stereotypes are preserved." if not mq_failures else "Mode/Quality stereotype mismatch.",
        {"failures": mq_failures}, blocking=True)

    # Characterization signals for principal quality/mode patterns.
    characterization = {
        "Strength": (CMPE.MedicinalProductPresentation, CMPE.hasStrength, CMPE.Strength),
        "MatchConfidence": (CMPE.EntityMatchAssertion, CMPE.hasMatchConfidence, CMPE.MatchConfidence),
        "SupplyCapacity": (CMPE.SupplyCapacity, CMPE.capacityBearer, None),
    }
    char_failures = []
    for name, (domain, prop, range_) in characterization.items():
        ok = (prop, RDF.type, OWL.ObjectProperty) in graph
        if name == "SupplyCapacity":
            ok = ok and (prop, RDFS.domain, domain) in graph
        else:
            ok = ok and (prop, RDFS.domain, domain) in graph and (prop, RDFS.range, range_) in graph
        if not ok:
            char_failures.append(name)
    add(out, "E3-12", "mode-quality", "PASS" if not char_failures else "FAIL",
        "Principal Quality/Mode characterization signals remain explicit." if not char_failures else "A principal characterization pattern is missing.",
        {"checked": list(characterization), "failures": char_failures}, blocking=True)

    # Identifier as assignment, not intrinsic identity datatype/class conflation.
    identifier_ok = (
        model_map.get("IdentifierValue") == "Datatype"
        and model_map.get("IdentifierAssignment") == "Relator"
        and (CMPE.identifierEntity, RDFS.domain, CMPE.IdentifierAssignment) in graph
        and (CMPE.identifierScheme, RDFS.domain, CMPE.IdentifierAssignment) in graph
    )
    add(out, "E3-13", "identifier-pattern", "PASS" if identifier_ok else "FAIL",
        "Identifier Value/Scheme/Assignment remain separated and assignment is relational." if identifier_ok else "Identifier assignment pattern is incomplete.",
        {}, blocking=True)

    # Observation activity/result separation and explicit production relation.
    observation_ok = (
        model_map.get("ObservationActivity") == "Event"
        and model_map.get("ObservationResult") == "Kind"
        and (CMPE.producesObservationResult, RDFS.domain, CMPE.ObservationActivity) in graph
        and (CMPE.producesObservationResult, RDFS.range, CMPE.ObservationResult) in graph
    )
    add(out, "E3-14", "observation-pattern", "PASS" if observation_ok else "FAIL",
        "Observation Activity and Observation Result remain distinct and explicitly connected." if observation_ok else "Observation Activity/Result pattern is incomplete.",
        {}, blocking=True)

    # Generic catch-all/part-whole anti-pattern local names must remain absent.
    internal_props = {
        local(p) for p in graph.subjects(RDF.type, OWL.ObjectProperty)
        if str(p).startswith(str(CMPE))
    }
    forbidden_present = sorted(set(registry["forbidden_internal_property_local_names"]) & internal_props)
    add(out, "E3-15", "generic-relation-partwhole", "PASS" if not forbidden_present else "FAIL",
        "Rejected generic catch-all/componentOf relations remain absent from the V2 formal vocabulary." if not forbidden_present else "Forbidden legacy/generic relation reintroduced.",
        {"present": forbidden_present}, blocking=True)

    # Formalization caveat: OWL annotations encode stereotypes, but no official tool validation.
    role_names = [name for _, name, stereotype in rows if stereotype == "Role"]
    roles_with_existential_restriction = []
    for name in role_names:
        role = CMPE[name]
        for obj in graph.objects(role, RDFS.subClassOf):
            if (obj, RDF.type, OWL.Restriction) in graph and graph.value(obj, OWL.someValuesFrom) is not None:
                roles_with_existential_restriction.append(name)
                break
    add(out, "E3-16", "formalization-boundary", "WARN" if len(roles_with_existential_restriction) < len(role_names) else "PASS",
        "Role relational dependence is primarily preserved by the conceptual registry/pattern relations rather than fully axiomatized as OWL existential restrictions; this bounds OWL-level OntoUML semantic enforcement.",
        {"roles": len(role_names), "roles_with_existential_restriction": sorted(roles_with_existential_restriction)}, blocking=False)

    # Extension-only mode characterization completeness: descriptive warning, not principal gate.
    extension_mode_props = {}
    for name in ["Vulnerability", "EnterpriseCapability"]:
        props = sorted(local(p) for p in by_domain.get(CMPE[name], []))
        extension_mode_props[name] = props
    extension_mode_gaps = [name for name, props in extension_mode_props.items() if not props]
    add(out, "E3-17", "extension-boundary", "WARN" if extension_mode_gaps else "PASS",
        "Some extension-only Modes remain conceptually typed but do not yet expose explicit bearer/characterization properties in the W5 OWL projection." if extension_mode_gaps else "Reviewed extension Modes expose characterization properties.",
        {"gaps": extension_mode_gaps, "properties": extension_mode_props}, blocking=False)

    blocking_failures = [x for x in out if x["blocking"] and x["status"] == "FAIL"]
    warnings = [x for x in out if x["status"] == "WARN"]
    family_status = "FAIL" if blocking_failures else ("PASS_WITH_WARNING" if warnings else "PASS")

    report = {
        "family": "W7-E3",
        "status": family_status,
        "official_ontouml_tool_executed": False,
        "conceptual_elements": len(rows),
        "checks_total": len(out),
        "blocking_failures": len(blocking_failures),
        "warnings": len(warnings),
        "checks": out,
        "interpretation": (
            "This project-native executable review tests the frozen Gate-D/W5 semantic commitments. "
            "It does not establish official OntoUML tool conformance. A PASS means no blocking "
            "anti-pattern defined by the frozen W7-E3 checklist was found in the evaluated artifacts."
        ),
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    if blocking_failures:
        raise SystemExit("W7-E3 blocking anti-pattern check failure")


if __name__ == "__main__":
    main()
