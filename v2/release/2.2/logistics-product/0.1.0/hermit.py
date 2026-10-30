#!/usr/bin/env python3
"""Four bounded HermiT consistency probes, never a whole-model claim."""
import json
import tempfile
from pathlib import Path

from owlready2 import OwlReadyInconsistentOntologyError, World, sync_reasoner
from rdflib import Graph, Namespace, RDF, OWL

HERE = Path(__file__).resolve().parent
C = Namespace("https://w3id.org/cm-pharme/2.1/")
D = Namespace("https://w3id.org/cm-pharme/experimental/coherence/")
W = Namespace("urn:cmpe:logistics-product-integration:")


def main():
    base = Graph().parse(HERE / "model.ttl", format="turtle")
    cases = {
        "no-product-recorded": [],
        "one-type": [(W.event, D.logisticsProduct, W.typeA)],
        "two-types-one-event": [(W.event, D.logisticsProduct, W.typeA),
                                (W.event, D.logisticsProduct, W.typeB)],
        "same-type-two-events": [(W.event, D.logisticsProduct, W.typeA),
                                 (W.otherEvent, D.logisticsProduct, W.typeA)],
    }
    outcomes = []
    for label, links in cases.items():
        graph = base + Graph()
        graph.add((W.event, RDF.type, C.DistributionLogisticsActivity))
        for triple in links:
            graph.add(triple)
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "case.rdf"
            graph.serialize(destination=source, format="xml")
            world = World()
            world.get_ontology(source.as_uri()).load()
            try:
                sync_reasoner(world, debug=0)
                bad = [x.iri for x in world.inconsistent_classes() if x.iri != str(OWL.Nothing)]
                if bad:
                    raise AssertionError((label, bad))
            except OwlReadyInconsistentOntologyError as exc:
                raise AssertionError(label) from exc
            finally:
                world.close()
        outcomes.append({"id": label, "consistent": True, "unsatisfiable_named_classes": []})
    print(json.dumps({"hermit_cases": outcomes, "status": "BOUNDED_TBOX_ONLY",
                      "full_model_reasoned": False, "scientific_acceptance": False}))


if __name__ == "__main__":
    main()
