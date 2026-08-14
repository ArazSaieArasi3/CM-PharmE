# CM-PharmE Ontology

This directory contains the **unreleased B3 formal-ontology engineering source** for CM-PharmE. The current stable semantic baseline remains `v1.0.0`; B3 is an engineering/formalization cycle under review and is not yet a released semantic model version.

## Authoritative B3 source

The GitHub-authoritative B3 authoring basis is:

- [`source/modules/`](source/modules/) — modular ontology source for ontology metadata, metamodel terms, domains, concepts, and relation/property formalization
- [`../mappings/cardinality/`](../mappings/cardinality/) — endpoint multiplicity, lifecycle, supersession, and cardinality provenance for all 40 stable relation IDs
- [`IRI_POLICY.md`](IRI_POLICY.md) — stable identifier and namespace policy
- [`mappings/ufo-stereotypes.ttl`](mappings/ufo-stereotypes.ttl) — cautious UFO/OntoUML stereotype-correspondence notes
- [`validation/`](validation/) — B3 reference validation evidence and artifact hashes
- [`../docs/evaluations/b3-formal-ontology-audit.md`](../docs/evaluations/b3-formal-ontology-audit.md) — final B3 engineering audit

## Historical ontology

The original v1.0.0 OWL/RDF/XML export is preserved unchanged under [`../releases/v1.0.0/ontology/`](../releases/v1.0.0/ontology/) for reproducibility. It was auto-converted from the Draw.io/XML model and contains converter artifacts, so it is **not** treated as the canonical cleaned ontology source.

## Formalization status

B3 formalizes:

- 39 canonical concept classes
- 40 stable relation records, represented as 39 OWL object properties plus one explicit generalization record
- 5 architectural domains
- complete cardinality-registry coverage for all 40 relation IDs
- stable identifier-based IRIs under the planned `https://w3id.org/cm-pharme/` namespace
- lifecycle/provenance handling for deprecated and superseded semantic relations
- formal definitions and OWL restrictions in the concept modules

The `w3id.org` redirect has not yet been registered, so the planned project IRIs should not yet be described as dereferenceable public URLs.

## Generated distributions

A local B3 reference build produced canonical Turtle, OWL/RDF/XML, RDF/XML, JSON-LD, N-Triples and SHACL representations and verified structural graph equivalence. These are **generated views**, not independent sources of truth. Their deterministic GitHub rebuild/materialization is intentionally deferred to the B5 CI/build workflow; see [`distributions/README.md`](distributions/README.md).

## Validation boundary

Structural/reference-package validation has passed, but full OWL DL reasoner evidence with HermiT/ELK/ROBOT has not yet been recorded. B3 therefore does not make a final logical-consistency or release-readiness claim. Those checks belong to B4/B5.
