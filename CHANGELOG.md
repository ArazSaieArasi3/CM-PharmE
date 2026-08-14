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

### B3 Formal Ontology Engineering
- Added a modular formal-ontology authoring source derived from the canonical v1.0.0 semantic inventory.
- Added stable identifier-based IRI policy under the planned `https://w3id.org/cm-pharme/` namespace without claiming deployed redirects.
- Formalized 39 concept classes and 40 stable relation records as 39 OWL object properties plus one explicit generalization record.
- Added formal concept definitions, domain/stereotype metadata, and OWL cardinality restrictions.
- Added complete cardinality-registry coverage for all 40 stable relation IDs.
- Deprecated `CMPE-R0011` while preserving provenance and supersession by active `CMPE-R0027`.
- Normalized `CMPE-R0031` from the raw source label `constraints` to `constrains` while retaining provenance.
- Added cautious UFO/OntoUML stereotype-correspondence notes without asserting unsupported external equivalence.
- Recorded structural/reference-package validation evidence and a dedicated B3 formal-ontology audit.
- Kept generated serializations and SHACL outputs as derived artifacts pending deterministic GitHub CI/build materialization.
- Deferred full OWL DL reasoner evidence, persistent-IRI deployment, broader competency-question execution, and expert semantic validation.

### B4 Paper-Grounded Research and Evaluation
- Added a repository-native problem/gap/solution narrative and application boundaries derived from the two CM-PharmE papers without duplicating manuscript structure.
- Added reusable model-development and evaluation methods, including PRISMA/thematic-synthesis provenance, business-architecture-informed concern identification, UFO/OntoUML classification, and E1–E9 evaluation mapping.
- Added the eight journal-manuscript competency questions and eight OntoUML-informed anti-pattern categories as machine-readable evaluation registries.
- Added the vaccine-distribution reference scenario, evidence-status policy, and publication-evidence matrix.
- Added curated method/evaluation references and explicit publication-to-repository traceability.
- Added the journal manuscript under review to the publication registry and strengthened the published conference-paper record without inventing unverified bibliographic metadata.
- Executed 28/28 structural/traceability checks and 8/8 bounded competency-query tests.
- Added a machine-readable vaccine-distribution sample spanning all five domains without scenario-specific core classes.
- Re-evaluated the eight anti-pattern categories and recorded targeted semantic findings without changing the core ontology.
- No new semantic model release is declared by this B4 documentation/evaluation work.

### B4.10 Reasoner and Semantic Finding Disposition
- Added `.github/workflows/ontology-reasoner.yml` for reproducible ROBOT/HermiT logical validation.
- Pinned ROBOT `v1.9.10` by SHA-256 before execution and added deterministic recursive Turtle-module assembly with RDFLib `7.5.0`.
- Completed GitHub Actions run `31796520297` successfully with HermiT exit code `0`, closing the initial E2 logical-validation gap for the current logical axiom set.
- Uploaded versioned reasoner evidence including assembled input, manifest, reasoned OWL, tool/version record, exit code, and machine-readable summary.
- Compared the 888-triple GitHub modular-source assembly with the 1,086-triple B3 packaged canonical source and recorded zero logical-predicate differences; annotation/provenance parity remains an engineering follow-up.
- Dispositioned five semantic findings without changing core semantics: three model-refinement candidates, one domain-evidence deferral, and one manuscript/formal discrepancy handled as documentation clarification.
- No five-domain architecture redesign was required and no new semantic release was declared.

## v1.0.0 — Historical Initial Release

### Added
- Initial CM-PharmE conceptual model in Draw.io/XML form.
- Initial PNG export of the conceptual model.
- Initial domain-view PNG.
- Initial OWL/RDF/XML export derived from the diagram.
- Academic README describing the initial model and authorship.

### Preservation Note
The historical artifacts are preserved unchanged in `releases/v1.0.0/`. The normalized registries and documentation created during repository restructuring describe the historical model without rewriting its immutable source artifacts. Later ontology cleanup or model evolution must create new artifacts rather than rewrite the released v1.0.0 files.
