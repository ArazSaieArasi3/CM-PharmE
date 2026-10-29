CM-PharmE **2.1.0 — M1 Provenance Core** is the first stable distribution of the explicitly bounded 2.1 provenance core.

## Supported scope
- Four classes and two object properties in the isolated M1 profile 0.1.0.
- Explicit opt-in SHACL/nonempty/public-composite-key admission and unchanged Q21-01.
- M001–M004 tested on seven synthetic copied-W6 records; four legacy query pairs, 24 base tables and 22 default IRIs preserved.
- 24 frozen admission expectations, five HermiT cases and bounded strict OWL views; extracted-file replay and byte-identical deterministic rebuild.

## Download and reproduce
Use `cm-pharme-2.1.0.tar`, its `.sha256` checksum and `provenance.json`.
The archive includes release-specific citation, notices, documentation, exact source support manifest and rebuild/verification tools. External runtime dependencies are obtained separately under upstream terms.
SHA-256: `4c9d3a1e52379c8c63b3619aedd7d0243cf702bcc078c9989a23619d50cc4350`.

## Scope and compatibility limits
This curated release tree is separate from `main` and broad Draft PR #305. It does not promote the whole experimental 2.1.0-rc.1 research checkpoint. Original RC/tag/assets and frozen source/oracle/history bytes are preserved.
Raw RDF keeps row-number rdf:value assertions; the strict OWL view explicitly omits only those assertions and reports the loss. The profile adds no global cardinality, disjointness or namespace equivalence and performs no production database migration.
Source-policy acceptance remains 1/4, historical ORSD acceptance 0/83 and no new external expert responses. Full native/model/domain/real-source/all-36-mapping, expert and product-effectiveness claims remain outside this release. Source fixtures remain explicitly synthetic and retain their upstream notices.
