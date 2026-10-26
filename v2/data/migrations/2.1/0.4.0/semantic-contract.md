# RDB-M3 scoped manufacturer contract — 0.4.0

Issue #320; requirement FR-02; wider scientific gate #306. This is the delegated
candidate decision for one manufacturer context, subject to later author review.
Importer, wholesaler, manufacturing-site use and product authorization are outside
this slice. Frozen 2.0 and ORSD 0.2.0 inputs remain unchanged.

## Adopted candidate choices

| ID | Choice | Justification and boundary |
|---|---|---|
| M3-D01 | Each admitted ManufacturingResponsibility has one ManufacturerRole holder and one ManufacturingResponsibilitySubjectRole product. | Reuses the existing native/OWL/SHACL ends and cardinalities; does not introduce a new global axiom. Separate contextual records can share either participant. |
| M3-D02 | The role uses the Organization identity; it does not create another legal entity. | One organization may participate in multiple product contexts. Relator identity is an explicit public ID plus a source/assertion identity, not the company name or the global organization/product pair. Repeated contexts remain separate. |
| M3-D03 | An explicit manufacturer attribution in a pinned source supports a documentary context in an experimental graph. | The FDA-hosted label in source-witness.json differentiates its manufacturer from its commissioned-for party. The relator interpretation remains subject to #306; a label attribution does not establish a legal duty, factory, production event, batch or current operation. |
| M3-D04 | SourceRecord, Assertion and EvidenceSupport identities must be present and aligned for every admitted M3 row. | Admission is stricter than open-world OWL. A missing source, counterpart or mismatched assertion is rejected; absence of a record means unknown. Do not use the manufactured-for statement as a manufacturer statement. |
| M3-D05 | Source revision and retrieval dates are provenance, not responsibility validity dates. | The real witness has unknown valid_from/valid_to. Only explicitly synthetic contexts exercise intervals and repeated assignments. |
| M3-D06 | Use a new versioned table and validation trigger in a copied database; export separately into the 2.1 namespace. | Preserve existing Organization/product rows and 2.0 schema/views/exporter. Transaction rollback restores all persistent state, including sequences. No production migration is authorized by this research slice. |

## Source and identity limits

The source URL, PDF SHA-256, revision, page locations, two short excerpts and
document-scoped product/organization IDs are recorded in source-witness.json.
These IDs refer to the documentary participants. No global entity-resolution claim
is made. The full PDF is a local research intermediate, not a repository artifact.
The replay uses the reviewed extraction offline and does not pretend to redownload
the label. `verify_source.py --pdf PATH` can independently recheck its bytes and
page attribution with Poppler.

The manufactured-for party remains an Organization without ManufacturerRole in
this witness. This is a non-entailment boundary, not a claim that the organization
cannot manufacture elsewhere. A company named Manufacturer Limited without a
qualifying relation also receives no role. An OWL countermodel must allow both.

## Finite stages and closure

1. Freeze this contract, source extraction, pinned model and independent oracles
   before writing the exporter, SQL fixtures and test implementation.
2. Execute the additive copied-PostgreSQL projection, paired SQL/SPARQL query,
   source/provenance checks, native anchor checks, SHACL/OWL witnesses and legacy
   before/during/after regression. Record exact software and commit evidence.
3. Close #320 only when this scoped contract passes. Keep #306 open for broader
   semantic/author review, empirical generalization, remaining mappings and release.

No source witness may be synthesized. The three additional synthetic records must
remain identified as test fixtures in SQL, RDF, query outputs and the final report.
