# CM-PharmE Semantic Changelog

This changelog records research-model and repository-level changes that are meaningful for reproducibility. Git commits remain the technical history; this file records semantic and release-level change.

## Unreleased / Repository Restructuring

### Repository Architecture
- Began migration from a publication-centric repository to a versioned research knowledge repository.
- Added explicit separation of model, ontology, mappings, evaluation, methodology, publications, applications, and release documentation.
- Added preservation and migration traceability for the original repository state.

### Documentation
- Reframed the root README as a model-centric academic landing page while retaining authors, affiliations, ORCID links, and publication visibility.
- Added one documentation page for each canonical v1.0 concept, relation, and domain.
- Added structural extraction audit and descriptive model statistics.

### Semantic Registry
- Extracted and assigned stable IDs to 39 canonical concepts from 40 graphical concept occurrences.
- Extracted 40 canonical relations from 41 labeled semantic relation occurrences.
- Formalized the five-domain registry and primary/cross-domain mappings.
- Added Concept↔Domain and Concept↔Relation traceability mappings.
- Frozen concept, relation, and domain registries inside the v1.0.0 release snapshot.

### Source-model review flags
- Recorded the `Enterprise Governance Relator` duplicate/stereotype conflict instead of silently removing it.
- Collapsed one exact duplicated mediation relation while preserving source occurrence count.
- Preserved both conflicting mediation-direction wordings between `Ecosystem Actor` and `Strategic Partnership Agreement` pending formal review.
- Excluded one unlabeled graphical self-loop from the semantic relation registry.
- Kept generic/awkward source relation labels (`material relation`, `constraints`) visible for later terminology review.

### Versioning
- Materialized the original repository state as historical release `v1.0.0`.
- Introduced lifecycle and versioning policies for future semantic entities.
- Documented `v1.0.0` as the current stable semantic baseline; manuscript revision numbers do not automatically create model versions.

## v1.0.0 — Historical Initial Release

### Added
- Initial CM-PharmE conceptual model in Draw.io/XML form.
- Initial PNG export of the conceptual model.
- Initial domain-view PNG.
- Initial OWL/RDF/XML export derived from the diagram.
- Academic README describing the initial model and authorship.

### Preservation Note
The historical artifacts are preserved unchanged in `releases/v1.0.0/`. The normalized registries and documentation created during repository restructuring describe the historical model without rewriting its immutable source artifacts. Later ontology cleanup or model evolution must create new artifacts rather than rewrite the released v1.0.0 files.
