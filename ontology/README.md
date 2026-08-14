# CM-PharmE Ontology

This directory contains the formal-ontology engineering layer for CM-PharmE. The current stable semantic baseline remains `v1.0.0`; formalization, evaluation and repository engineering do not themselves declare a new semantic model release.

## Authoritative source

The manual ontology authoring source is [`source/modules/`](source/modules/). It contains ontology metadata, metamodel terms, domains, concepts, relation/property formalization and the annotation/provenance parity supplement.

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

## Source parity and provenance

During evaluation, the earlier modular source was found to contain the same logical axiom set as the packaged formal reference but less annotation/provenance metadata. The reproducible-build phase closed that gap.

The modular source now reconstructs the complete reference graph at **1,086 triples** with canonical graph SHA-256:

`cc823a8aff4d7e7818f8470f2dbad6ca8045ff92e5637fbf3503bc105170a83f`

This parity restoration did not alter the logical axiom set and did not silently resolve the open semantic-refinement candidates.

## Generated distributions and SHACL

The CI pipeline deterministically generates the following consumer views:

- consolidated Turtle
- RDF/XML / OWL
- RDF/XML
- expanded JSON-LD
- canonical N-Triples
- SHACL shapes

See [`distributions/`](distributions/) for the generation contract. The generated files and SHACL are published as CI/release artifacts rather than hand-maintained repository sources.

## Validation

The repository combines:

- structural/reference-package validation;
- structural, scenario and competency-question evidence;
- ROBOT/HermiT logical validation;
- graph-fingerprint, serialization, byte-reproducibility, SHACL and CI quality gates.

See [`validation/`](validation/), the [Evaluation overview](../docs/evaluations/index.md), and the [Reproducible-build architecture](../docs/engineering/b5-reproducible-build.md).

## UFO/OntoUML relationship

CM-PharmE uses UFO/OntoUML concepts as a modeling foundation, while keeping its internal metamodel terms and formal ontology separate from unsupported external equivalence claims. The repository does not currently claim native OntoUML Vocabulary or OntoUML Schema conformance.

See:

- [Official OntoUML Ecosystem References](../docs/references/ontouml-ecosystem.md)
- [`mappings/ufo-stereotypes.ttl`](mappings/ufo-stereotypes.ttl)
- [Research and Model Development Method](../docs/methodology/research-and-model-development.md)

## Persistent IRI boundary

The planned namespace is `https://w3id.org/cm-pharme/`. The IRI policy is established, but the external `w3id.org` redirect registration is still an administrative follow-up; the repository must not imply that redirects are deployed until that registration is completed.

## Historical ontology

The original v1.0.0 auto-converted OWL file remains immutable under [`../releases/v1.0.0/ontology/`](../releases/v1.0.0/ontology/). It is preserved for reproducibility but is not the canonical cleaned ontology source.