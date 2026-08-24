#!/usr/bin/env python3
"""Compare CM-PharmE 2.0 reasoned OWL views for W7-E2.

This evaluator intentionally limits agreement checks to named CM-PharmE classes
and explicit/inferred named-class subclass relations. Anonymous-expression
normalization differences are not treated as semantic disagreements.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef

CMPE = Namespace("https://w3id.org/cm-pharme/2.0/")


def args():
    p = argparse.ArgumentParser()
    p.add_argument("--asserted", required=True)
    p.add_argument("--hermit", required=True)
    p.add_argument("--jfact", required=True)
    p.add_argument("--hermit-unsat", required=True)
    p.add_argument("--jfact-unsat", required=True)
    p.add_argument("--hermit-log", required=False)
    p.add_argument("--jfact-log", required=False)
    p.add_argument("--output", required=True)
    return p.parse_args()


def load(path: str) -> Graph:
    return Graph().parse(path)


def load_optional(path: str) -> Graph:
    p = Path(path)
    if not p.exists() or p.stat().st_size == 0:
        return Graph()
    return Graph().parse(p)


def internal_named_classes(g: Graph) -> set[URIRef]:
    return {
        c for c in g.subjects(RDF.type, OWL.Class)
        if isinstance(c, URIRef) and str(c).startswith(str(CMPE))
    }


def internal_datatypes(g: Graph) -> set[URIRef]:
    return {
        d for d in g.subjects(RDF.type, RDFS.Datatype)
        if isinstance(d, URIRef) and str(d).startswith(str(CMPE))
    }


def semantically_used_datatypes(g: Graph, datatypes: set[URIRef]) -> dict[str, list[str]]:
    """Report semantic uses beyond declaration/annotation of project-native datatypes."""
    benign_predicates = {RDF.type, RDFS.label}
    out: dict[str, list[str]] = {}
    for dt in datatypes:
        uses = []
        for s, p, o in g.triples((None, None, dt)):
            uses.append(f"object:{s.n3()} {p.n3()}")
        for s, p, o in g.triples((dt, None, None)):
            if p not in benign_predicates and not str(p).startswith("https://w3id.org/cm-pharme/2.0/meta/"):
                uses.append(f"subject:{p.n3()} {o.n3()}")
        if uses:
            out[str(dt)] = sorted(uses)
    return out


def unsat_named(g: Graph, universe: set[URIRef]) -> set[URIRef]:
    out = set()
    for c in universe:
        if (c, RDFS.subClassOf, OWL.Nothing) in g or (c, OWL.equivalentClass, OWL.Nothing) in g:
            out.add(c)
        if (OWL.Nothing, OWL.equivalentClass, c) in g:
            out.add(c)
    return out


def named_subclass_pairs(g: Graph, universe: set[URIRef]) -> set[tuple[str, str]]:
    pairs = set()
    for s, o in g.subject_objects(RDFS.subClassOf):
        if s in universe and isinstance(o, URIRef) and (o in universe or o == OWL.Thing or o == OWL.Nothing):
            pairs.add((str(s), str(o)))
    return pairs


def labels(items):
    return sorted(str(x).rsplit("/", 1)[-1] for x in items)


def log_findings(path: str | None) -> list[str]:
    if not path:
        return []
    p = Path(path)
    if not p.exists():
        return []
    findings = []
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        if " ERROR " in line or " WARN " in line or line.startswith("ERROR") or line.startswith("WARN"):
            findings.append(line.strip())
    return findings


def main():
    a = args()
    asserted = load(a.asserted)
    hermit = load(a.hermit)
    jfact = load(a.jfact)
    hu = load_optional(a.hermit_unsat)
    ju = load_optional(a.jfact_unsat)

    universe = internal_named_classes(asserted)
    h_unsat = unsat_named(hermit, universe) | unsat_named(hu, universe)
    j_unsat = unsat_named(jfact, universe) | unsat_named(ju, universe)

    h_pairs = named_subclass_pairs(hermit, universe)
    j_pairs = named_subclass_pairs(jfact, universe)
    only_h = sorted(h_pairs - j_pairs)
    only_j = sorted(j_pairs - h_pairs)

    datatypes = internal_datatypes(asserted)
    datatype_uses = semantically_used_datatypes(asserted, datatypes)
    hermit_findings = log_findings(a.hermit_log)
    jfact_findings = log_findings(a.jfact_log)

    mandatory_pass = not h_unsat and not j_unsat and not only_h and not only_j
    compatibility_warn = bool(hermit_findings or jfact_findings)
    status = "WARN" if mandatory_pass and compatibility_warn else ("PASS" if mandatory_pass else "FAIL")

    report = {
        "family": "W7-E2",
        "status": status,
        "mandatory_logical_gate": "PASS" if mandatory_pass else "FAIL",
        "named_internal_classes": len(universe),
        "project_native_datatypes": len(datatypes),
        "project_native_datatype_semantic_uses": datatype_uses,
        "hermit": {
            "unsatisfiable_named_classes": labels(h_unsat),
            "named_subclass_pairs": len(h_pairs),
            "log_findings": hermit_findings,
        },
        "jfact": {
            "unsatisfiable_named_classes": labels(j_unsat),
            "named_subclass_pairs": len(j_pairs),
            "log_findings": jfact_findings,
        },
        "agreement": {
            "named_unsatisfiable_sets_equal": h_unsat == j_unsat,
            "named_subclass_pairs_equal": h_pairs == j_pairs,
            "only_hermit": only_h,
            "only_jfact": only_j,
        },
        "interpretation": (
            "The mandatory logical gate passes only when both reasoners report no unsatisfiable "
            "named CM-PharmE class and agree on named-class subclass relations materialized in "
            "their ROBOT outputs. Tool-specific warnings are retained separately. This does not "
            "establish semantic truth, completeness, or equivalence for every anonymous OWL expression."
        ),
    }
    Path(a.output).parent.mkdir(parents=True, exist_ok=True)
    Path(a.output).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))

    if not mandatory_pass:
        raise SystemExit("Reasoner disagreement or unsatisfiable named class requires investigation")


if __name__ == "__main__":
    main()
