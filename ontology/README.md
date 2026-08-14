# CM-PharmE Ontology

This directory contains the formal-ontology engineering layer for CM-PharmE. The current stable semantic baseline remains `v1.0.0`; B3–B5 formalization, evaluation and repository engineering do not themselves declare a new semantic model release.

## Authoritative source

The manual ontology authoring source is [`source/modules/`](source/modules/). It contains ontology metadata, metamodel terms, domains, concepts, relation/property formalization and the B5 annotation/provenance parity supplement.

Related authoritative evidence includes:

- [`../mappings/cardinality/`](../mappings/cardinality/) — endpoint multiplicity and cardinality provenance
- [`IRI_POLICY.md`](IRI_POLICY.md) — stable IRI policy
- [`mappings/ufo-stereotypes.ttl`](mappings/ufo-stereotypes.ttl) — cautious UFO/OntoUML correspondence notes
- [`../evaluation/`](../evaluation/) — competency questions, scenarios, evidence and semantic findings
- [`validation/`](validation/) — reproducible build and validation evidence

## Formal inventory

The current formal graph contains:

- **39** canonical concept classes
- **40** stable relation records: 39 OWL object properties + one explicit generalization record
- **5** architectural domains
- **42** OWL qualified cardinality restrictions
- full cardinality-registry coverage for all 40 stable relation IDs
- lifecycle/provenance handling for deprecated and superseded relations

## B5 source parity

B4.10 showed that the earlier GitHub modular source had 888 triples while the B3 packaged reference had 1,086 triples, with zero logical-axiom differences. B5 closes the remaining annotation/provenance gap.

The modular source now reconstructs the complete B3 reference graph at **1,086 triples** with canonical graph SHA-256:

`cc823a8aff4d7e7818f8470f2dbad6ca8045ff92e5637fbf3503bc105170a83f`

This parity restoration does not alter the logical axiom set and does not resolve the open B4.10 semantic-refinement candidates.

## Generated distributions and SHACL

B5 deterministically generates the following consumer views in CI:

- consolidated Turtle
- RDF/XML / OWL
- RDF/XML
- expanded JSON-LD
- canonical N-Triples
- SHACL shapes

See [`distributions/`](distributions/) for the generation contract. The generated files and SHACL are published as CI/release artifacts rather than hand-maintained repository sources.

## Validation

The repository now combines:

- B3 structural/reference-package validation;
- B4 structural, scenario and competency-question evidence;
- B4.10 ROBOT/HermiT logical validation;
- B5 graph-fingerprint, serialization, byte-reproducibility, SHACL and CI quality gates.

See [`validation/`](validation/) and [`../docs/engineering/b5-reproducible-build.md`](../docs/engineering/b5-reproducible-build.md).

## Persistent IRI boundary

The planned namespace is `https://w3id.org/cm-pharme/`. The IRI policy is established, but the external `w3id.org` redirect registration is still an administrative follow-up; the repository must not imply that redirects are deployed until that registration is completed.

## Historical ontology

The original v1.0.0 auto-converted OWL file remains immutable under [`../releases/v1.0.0/ontology/`](../releases/v1.0.0/ontology/). It is preserved for reproducibility but is not the canonical cleaned ontology source.
