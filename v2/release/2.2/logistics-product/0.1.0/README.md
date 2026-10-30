# #349 — bounded logisticsProduct integration

This package implements the precommitted LS-PRODUCT-01 decision on the exact
695-element #347 review candidate. It preserves all element IDs and all prior
fields except the English description of `coherence-rel-logisticsProduct`.
The optional `0..*` ends and null stereotype remain unchanged; this candidate
does not settle the full OntoUML Event participation semantics.

The native link goes from `DistributionLogisticsActivity` to the
`MedicinalProduct` **type**. `model.ttl` declares the same domain/range without
global occurrence, cardinality, identity or delivery axioms. The opted-in
source claim in the frozen #348 SHACL profile requires one performed event,
product type and source record. A valid claim projects only to a candidate
named graph keyed by the record IRI. No projection enters the default graph.
The source record is provenance, neither the event nor the product identity.

Run `build.py --output <dir> --check-committed`, the frozen #348 `verify.py`
with its own `--check-committed`, then `hermit.py`. The integration checks 12
frozen independent cases and requires the prior three combined results;
the CI job replays all 15 independently. Four RDFS probes establish the
limited entailments/non-entailments; HermiT runs four bounded cases. Source
claims are not independently verified world facts. Scientific full-model
validation, 47 other relation proposals, 83 historical ORSD dispositions,
source-policy acceptance and public Pages are outside this packet.
