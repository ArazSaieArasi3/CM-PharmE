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

The modular source reconstructs the complete reference graph at **1,086 triples** with canonical graph SHA-256:

`cc823a8aff4d7e7818f8470f2dbad6ca8045ff92e5637fbf3503bc105170a83f`

This parity restoration did not alter the logical axiom set and did not silently resolve the open semantic-refinement candidates.

## Generated distributions and SHACL

The CI pipeline generates a complete reproducible distribution family from the same authoritative source:

- consolidated Turtle
- OWL / RDF-XML
- RDF/XML
- expanded and compacted JSON-LD plus JSON-LD context
- canonical N-Triples
- TriG and N-Quads dataset-capable views
- Manchester Syntax
- OWL Functional Syntax
- SHACL shapes

RDF-compatible views are graph-equivalence checked. Manchester and Functional Syntax are produced through ROBOT/OWLAPI and compared with the source at the OWL axiom level. See [`distributions/`](distributions/) and [`../docs/engineering/FORMATS.md`](../docs/engineering/FORMATS.md).

## Validation

The repository combines:

- structural/reference-package validation;
- executed SHACL validation over the vaccine sample with an explicitly registered bounded finding profile;
- eight positive and four negative executable competency-query regressions;
- ROBOT ontology metrics and OWL profile assessment;
- ROBOT/HermiT logical validation;
- graph-fingerprint, serialization-equivalence, byte-reproducibility and deterministic-package gates.

The executable SHACL step currently reproduces **three registered findings** in the illustrative vaccine sample: two Violations and one Warning. These findings are intentionally preserved rather than editing the sample or ontology only to force conformance.

The canonical CM-PharmE 1.0 RDF source is also explicitly assessed against the OWL 2 DL profile. The current source is **not reported as OWL 2 DL-profile conformant** because OWLAPI identifies formal-profile hygiene issues such as explicit declaration requirements around annotation/external vocabulary resources. This is recorded as a formalization finding rather than hidden. HermiT logical reasoning nevertheless completes successfully for the current axiom set. Neither result is interpreted as domain completeness or universal ontological correctness.

See [`validation/`](validation/), the [Evaluation overview](../docs/evaluations/index.md), [Validation architecture](../docs/engineering/VALIDATION.md), and [Semantic engineering completion](../docs/engineering/SEMANTIC_ENGINEERING_COMPLETION.md).

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
