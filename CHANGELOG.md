# CM-PharmE Semantic Changelog

This changelog records research-model and repository-level changes that are meaningful for reproducibility. Git commits remain the technical history; this file records semantic and release-level change.

## Unreleased / vNext

### Repository Architecture
- Began migration from a publication-centric repository to a versioned research knowledge repository.
- Added explicit separation of model, ontology, mappings, evaluation, methodology, publications, applications, and release documentation.
- Added preservation and migration traceability for the original repository state.

### Documentation
- Reframed the root README as a model-centric academic landing page while retaining authors, affiliations, ORCID links, and publication visibility.

### Versioning
- Materialized the original repository state as historical release `v1.0.0`.
- Introduced lifecycle and versioning policies for future semantic entities.

## v1.0.0 — Historical Initial Release

### Added
- Initial CM-PharmE conceptual model in Draw.io/XML form.
- Initial PNG export of the conceptual model.
- Initial domain-view PNG.
- Initial OWL/RDF/XML export derived from the diagram.
- Academic README describing the initial model and authorship.

### Preservation Note
The historical artifacts are preserved unchanged in `releases/v1.0.0/`. Later ontology cleanup or model evolution must create new artifacts rather than rewrite the released v1.0.0 files.
