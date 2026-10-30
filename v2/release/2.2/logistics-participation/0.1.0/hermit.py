#!/usr/bin/env python3
"""Run HermiT on the bounded candidate TBox and four synthetic ABox cases."""
import json
import tempfile
from pathlib import Path

from owlready2 import OwlReadyInconsistentOntologyError, World, sync_reasoner
from rdflib import Graph, Namespace, OWL, RDF, URIRef

HERE = Path(__file__).resolve().parent
C = Namespace("https://w3id.org/cm-pharme/2.1/")
D = Namespace("https://w3id.org/cm-pharme/experimental/coherence/")
P = Namespace("https://w3id.org/cm-pharme/experimental/logistics-site/0.1.0/")
W = Namespace("urn:cmpe:logistics-integration:")


def main():
    base = Graph().parse(HERE / "model.ttl", format="turtle")
    cases = {
        "no-site-recorded": [],
        "one-origin": [("origin", W.siteA)],
        "multiple-functions-and-sites": [("origin", W.siteA), ("storage", W.siteB), ("destination", W.siteB)],
        "generic-unspecified": [("generic", W.siteA)],
    }
    outcomes = []
    for label, links in cases.items():
        graph = base + Graph()
        graph.add((W.event, RDF.type, C.DistributionLogisticsActivity))
        for function, site in links:
            pred = D.logisticsFacility if function == "generic" else P["logistics" + function.title() + "Facility"]
            graph.add((W.event, pred, site))
            graph.add((site, RDF.type, C.Facility))
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "case.rdf"
            graph.serialize(destination=source, format="xml")
            world = World()
            world.get_ontology(source.as_uri()).load()
            try:
                sync_reasoner(world, debug=0)
                inconsistent = [x.iri for x in world.inconsistent_classes() if x.iri != str(OWL.Nothing)]
                if inconsistent:
                    raise AssertionError((label, inconsistent))
            except OwlReadyInconsistentOntologyError as exc:
                raise AssertionError(label) from exc
            finally:
                world.close()
        outcomes.append({"id": label, "consistent": True, "unsatisfiable_named_classes": []})
    print(json.dumps({"hermit_cases": outcomes, "status": "BOUNDED_TBOX_ONLY",
                      "full_model_reasoned": False, "scientific_acceptance": False}))


if __name__ == "__main__":
    main()
