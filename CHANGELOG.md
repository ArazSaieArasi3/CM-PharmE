# CM-PharmE Semantic Changelog

This changelog records research-model and repository-level changes that are meaningful for reproducibility. Git commits remain the technical history; this file records semantic and release-level change.

## Unreleased / Repository Restructuring

### Repository Architecture
- Migrated from a publication-centric repository to a versioned research knowledge repository.
- Separated model, ontology, mappings, evaluation, methodology, publications, applications, engineering and release documentation.
- Added preservation and migration traceability for the original repository state.

### Documentation
- Reframed the root README as a model-centric academic landing page while retaining authors, affiliations, ORCID links and publication visibility.
- Added one documentation page for each canonical v1.0 concept, relation and domain.
- Added structural extraction audit and descriptive model statistics.

### Semantic Registry
- Assigned stable IDs to 39 canonical concepts from 40 graphical concept occurrences.
- Extracted 40 canonical relations from 41 labeled semantic relation occurrences.
- Formalized the five-domain registry and primary/cross-domain mappings.
- Added Concept↔Domain and Concept↔Relation traceability mappings.
- Frozen concept, relation and domain registries inside the v1.0.0 release snapshot.

### Source-model review flags
- Recorded the `Enterprise Governance Relator` duplicate/stereotype conflict rather than silently removing it.
- Collapsed one duplicated mediation occurrence while preserving source provenance.
- Preserved conflicting mediation-direction evidence between `Ecosystem Actor` and `Strategic Partnership Agreement` for formal review.
- Excluded an unlabeled graphical self-loop from the semantic relation registry.
- Preserved generic/awkward source relation labels for later terminology review.

### Versioning
- Materialized the original repository state as historical release `v1.0.0`.
- Introduced lifecycle and versioning policies for future semantic entities.
- Kept `v1.0.0` as the stable semantic baseline; manuscript revisions do not automatically create model versions.

### B3 Formal Ontology Engineering
- Added modular formal-ontology authoring source derived from the canonical v1.0.0 semantic inventory.
- Added stable identifier-based IRI policy under the planned `https://w3id.org/cm-pharme/` namespace without claiming deployed redirects.
- Formalized 39 concept classes and 40 stable relation records as 39 OWL object properties plus one explicit generalization record.
- Added formal concept definitions, domain/stereotype metadata and OWL cardinality restrictions.
- Added complete cardinality-registry coverage for all 40 stable relation IDs.
- Deprecated `CMPE-R0011` while preserving provenance and supersession by active `CMPE-R0027`.
- Normalized `CMPE-R0031` from raw label `constraints` to `constrains` while retaining provenance.
- Added cautious UFO/OntoUML stereotype-correspondence notes without unsupported equivalence claims.
- Recorded structural/reference-package validation and a dedicated B3 formal-ontology audit.

### B4 Paper-Grounded Research and Evaluation
- Added repository-native problem/gap/solution narrative and application boundaries derived from the two CM-PharmE papers without duplicating manuscript structure.
- Added reusable model-development and evaluation methods, including PRISMA/thematic-synthesis provenance, Business Architecture and UFO/OntoUML procedures.
- Added eight competency questions and eight OntoUML-informed anti-pattern categories as machine-readable evaluation registries.
- Added the vaccine-distribution reference scenario, evidence-status policy and publication-evidence matrix.
- Added curated method/evaluation references and explicit publication-to-repository traceability.
- Added the journal manuscript under review to the publication registry without inventing unverified bibliographic metadata.
- Executed 28/28 structural/traceability checks and 8/8 bounded competency-query tests.
- Added a machine-readable vaccine scenario spanning all five domains without scenario-specific core classes.
- Re-evaluated anti-pattern categories and recorded targeted semantic findings without changing core ontology semantics.

### B4.10 Reasoner and Semantic Finding Disposition
- Added GitHub Actions ROBOT/HermiT logical validation.
- Pinned ROBOT `v1.9.10` by SHA-256 and RDFLib `7.5.0` for controlled execution.
- Completed GitHub Actions run `31796520297` successfully with HermiT exit code `0`.
- Recorded source parity finding: 888 GitHub modular triples versus 1,086 B3 reference triples with zero logical-predicate differences.
- Dispositioned five semantic findings without core semantic changes: three model-refinement candidates, one domain-evidence deferral and one documentation clarification.

### B5 Reproducible Build and Release Engineering
- Closed the B4.10 annotation/provenance parity gap so the modular authoring source reconstructs the full **1,086-triple** B3 reference graph.
- Pinned the canonical ontology graph fingerprint `cc823a8aff4d7e7818f8470f2dbad6ca8045ff92e5637fbf3503bc105170a83f` and SHACL fingerprint `2a79cc94a2118a0f6f6edb6eb3b72ed9ad20f278ebda60e9e258b0e3d0a9e893`.
- Added deterministic generation of consolidated Turtle, RDF/XML/OWL, RDF/XML, expanded JSON-LD, canonical N-Triples and SHACL.
- Configured generated ontology distributions as CI/release artifacts while retaining `ontology/source/modules/` as the manual source of truth.
- Added deterministic build manifest and SHA-256 checksums.
- Added automated graph, entity-count, SHACL, serialization, lifecycle and byte-reproducibility quality gates.
- Added machine-readable competency-query regression expectations and CI execution of all eight CQs.
- Expanded ontology CI to relevant Pull Requests and pushes to `main`, with ROBOT/HermiT enforced as a logical-validation gate.
- Added deterministic release-bundle construction verified by a double-build byte comparison.
- Added release-readiness documentation while deliberately leaving semantic version/tag creation, license selection and `w3id.org` registration as separate governance decisions.
- No new stable semantic model release is declared by B5 and no B4.10 model-refinement candidate is silently applied.

## v1.0.0 — Historical Initial Release

### Added
- Initial CM-PharmE conceptual model in Draw.io/XML form.
- Initial PNG export of the conceptual model.
- Initial domain-view PNG.
- Initial OWL/RDF/XML export derived from the diagram.
- Academic README describing the initial model and authorship.

### Preservation Note
The historical artifacts are preserved unchanged in `releases/v1.0.0/`. Normalized registries, formal ontology artifacts, evaluations and later engineering work describe or evolve the model without rewriting the immutable historical release source files.
