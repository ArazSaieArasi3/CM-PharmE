#!/usr/bin/env python3
"""Static W4 PlantUML pattern screen; NOT an official OntoUML validator.

The checks intentionally return triggers/unknowns, never a blanket PASS for
anti-patterns requiring multiplicity, meta-properties, or human semantics.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from rdflib import Graph, Namespace, RDFS

ROOT = Path(__file__).resolve().parents[2]
PUML = ROOT / "v2/research/w4/integrated-ontouml-overview.puml"
PROJECTION = ROOT / "v2/research/w4/integrated-ontouml-review-projection.puml"
MODULES = ROOT / "v2/ontology/source/modules"
CMPE = Namespace("https://w3id.org/cm-pharme/2.0/")

CLASS = re.compile(r'^\s*(abstract )?class\s+(?:"[^"]+"|(\w+))(?:\s+as\s+(\w+))?\s+<<([^>]+)>>')
EDGE = re.compile(r'^\s*(\w+)\s+(<\|--|-->|--)\s+(\w+)(?:\s*:\s*(.*))?$')
PACKAGE = re.compile(r'^package "([^"]+)"')


def parse(path: Path) -> dict:
    domain = None
    classes, edges = {}, []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = PACKAGE.match(line)
        if match:
            domain = match.group(1)
            continue
        match = CLASS.match(line)
        if match:
            alias = match.group(3) or match.group(2)
            if alias in classes:
                raise ValueError(f"Duplicate class alias {alias}")
            classes[alias] = {"domain": domain, "stereotype": match.group(4), "abstract": bool(match.group(1))}
        if line.strip() == "}":
            domain = None
        match = EDGE.match(line)
        if match:
            a, arrow, b, label = match.groups()
            edges.append({"source": a, "target": b, "arrow": arrow, "label": label or ""})
    if len(classes) != 87 or len({v["domain"] for v in classes.values()}) != 17:
        raise ValueError("Expected frozen 87 concepts in 17 domains")
    if any(e["source"] not in classes or e["target"] not in classes for e in edges):
        raise ValueError("Diagram edge has undeclared endpoint")
    return {"classes": classes, "edges": edges}


def analyze(model: dict) -> dict:
    classes, edges = model["classes"], model["edges"]
    by_domain = defaultdict(lambda: {"concepts": 0, "relators": 0, "rolemixins": 0, "events": 0, "situations": 0, "datatypes": 0})
    for _, obj in classes.items():
        row = by_domain[obj["domain"]]
        row["concepts"] += 1
        key = {"Relator": "relators", "RoleMixin": "rolemixins", "Event": "events", "Situation": "situations", "Datatype": "datatypes"}.get(obj["stereotype"])
        if key:
            row[key] += 1
    relators = sorted(a for a, v in classes.items() if v["stereotype"] == "Relator")
    mediation = defaultdict(list)
    invalid_datatype_mediation = []
    rigid_mediation = []
    for e in edges:
        if "<<mediation>>" not in e["label"]:
            continue
        a, b = e["source"], e["target"]
        if a not in relators and b not in relators:
            raise ValueError(f"Mediation without a relator: {a}-{b}")
        relator, endpoint = (a, b) if a in relators else (b, a)
        mediation[relator].append(endpoint)
        if classes[endpoint]["stereotype"] == "Datatype":
            invalid_datatype_mediation.append([relator, endpoint])
        if classes[endpoint]["stereotype"] in {"Kind", "Subkind"}:
            rigid_mediation.append([relator, endpoint])
    rolemixins = sorted(a for a, v in classes.items() if v["stereotype"] == "RoleMixin")
    nonabstract_rm = [a for a in rolemixins if not classes[a]["abstract"]]
    subclasses = defaultdict(list)
    for e in edges:
        if e["arrow"] == "<|--":
            subclasses[e["source"]].append(e["target"])
    rm_no_subtypes = [a for a in rolemixins if not subclasses[a]]
    modes_qualities = sorted(a for a, v in classes.items() if v["stereotype"] in {"Mode", "Quality"})
    uncharacterized = [a for a in modes_qualities if not any("<<characterization>>" in e["label"] and a in {e["source"], e["target"]} for e in edges)]
    return {
        "domains": dict(sorted(by_domain.items())),
        "relator_mediation_endpoints": {a: mediation[a] for a in relators},
        "relators_with_fewer_than_two_drawn_mediations": [a for a in relators if len(mediation[a]) < 2],
        "datatype_mediation_triggers": invalid_datatype_mediation,
        "rigid_type_mediation_triggers": rigid_mediation,
        "rolemixins_without_abstract_keyword": nonabstract_rm,
        "rolemixins_without_drawn_subtypes": rm_no_subtypes,
        "modes_or_qualities_without_drawn_characterization": uncharacterized,
        "product_role_also_ecosystem_participant": "AlternativeRole" in subclasses["EcosystemParticipant"],
        "generalization_count": sum(e["arrow"] == "<|--" for e in edges),
    }


def main() -> None:
    baseline = analyze(parse(PUML))
    projection = analyze(parse(PROJECTION))
    formal = Graph()
    for module in sorted(MODULES.glob("*.ttl")):
        formal.parse(module, format="turtle")
    formal_only = {
        "alternative_role_subclass_of_ecosystem_participant":
            (CMPE.AlternativeMedicinalProductRole, RDFS.subClassOf, CMPE.EcosystemParticipant) in formal,
        "alternative_role_subclass_of_medicinal_product":
            (CMPE.AlternativeMedicinalProductRole, RDFS.subClassOf, CMPE.MedicinalProduct) in formal,
    }
    print(json.dumps({
        "status": "static trigger screen, not official OntoUML conformance",
        "baseline": baseline,
        "corrected_projection": projection,
        "formal_cross_projection_checks": formal_only,
        "limitations": [
            "Multiplicity, generalization-set, read-only and existential-dependence meta-properties are unavailable in W4 PlantUML.",
            "An anti-pattern trigger requires human interpretation and may be justified; an untriggered check is not certification.",
            "The OWL graph does not preserve all OntoUML stereotypes of relations or modal constraints.",
        ],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
