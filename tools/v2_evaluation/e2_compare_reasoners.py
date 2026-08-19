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
    p.add_argument("--output", required=True)
    return p.parse_args()


def load(path: str) -> Graph:
    return Graph().parse(path)


def internal_named_classes(g: Graph) -> set[URIRef]:
    return {
        c for c in g.subjects(RDF.type, OWL.Class)
        if isinstance(c, URIRef) and str(c).startswith(str(CMPE))
    }


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


def main():
    a = args()
    asserted = load(a.asserted)
    hermit = load(a.hermit)
    jfact = load(a.jfact)
    hu = load(a.hermit_unsat)
    ju = load(a.jfact_unsat)

    universe = internal_named_classes(asserted)
    h_unsat = unsat_named(hermit, universe) | unsat_named(hu, universe)
    j_unsat = unsat_named(jfact, universe) | unsat_named(ju, universe)

    h_pairs = named_subclass_pairs(hermit, universe)
    j_pairs = named_subclass_pairs(jfact, universe)
    only_h = sorted(h_pairs - j_pairs)
    only_j = sorted(j_pairs - h_pairs)

    agreement = not h_unsat and not j_unsat and not only_h and not only_j
    status = "PASS" if agreement else "WARN"

    report = {
        "family": "W7-E2",
        "status": status,
        "named_internal_classes": len(universe),
        "hermit": {
            "unsatisfiable_named_classes": labels(h_unsat),
            "named_subclass_pairs": len(h_pairs),
        },
        "jfact": {
            "unsatisfiable_named_classes": labels(j_unsat),
            "named_subclass_pairs": len(j_pairs),
        },
        "agreement": {
            "named_unsatisfiable_sets_equal": h_unsat == j_unsat,
            "named_subclass_pairs_equal": h_pairs == j_pairs,
            "only_hermit": only_h,
            "only_jfact": only_j,
        },
        "interpretation": (
            "PASS means both reasoners report no unsatisfiable named CM-PharmE class "
            "and agree on named-class subclass relations materialized in their ROBOT outputs. "
            "This does not establish semantic truth, completeness, or equivalence for every "
            "anonymous OWL expression."
        ),
    }
    Path(a.output).parent.mkdir(parents=True, exist_ok=True)
    Path(a.output).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))

    # Per the frozen protocol, disagreement requires investigation. Keep the workflow
    # green only for full agreement; a disagreement must be inspected explicitly.
    if status != "PASS":
        raise SystemExit("Reasoner disagreement or unsatisfiable named class requires investigation")


if __name__ == "__main__":
    main()
