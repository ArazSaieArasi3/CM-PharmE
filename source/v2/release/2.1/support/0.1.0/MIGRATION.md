# Compatibility and support limits

This is an opt-in profile, not an automatic database migration. Existing W6 2.0
default IRIs, tables and legacy queries stay unchanged. M1 projects selected
records into the 2.1 namespace using its existing public/composite-key rules.
No owl:sameAs, namespace equivalence, global cardinality or global disjointness
is introduced. Applications choose the explicit profile; old callers remain on
their historical entrypoints until they intentionally opt in.

Keep raw RDF for queries and admission. The strict OWL view omits only rdf:value
serialization triples and cannot replace the raw export without losing row-number assertions.
The frozen profile's 0.1.0 and alpha source-lineage annotations are retained even
when the eventual distribution is 2.1.0. Cite this release-specific CITATION.cff
for the selected distribution and the historical research citation as appropriate.

Support is limited to the listed profile and tested synthetic mapping. The full
P3 ontology and source shapes are derivation/hash references, not supported public
modules. New source mappings, full native validation, four broader domain modules,
external expert evaluation, full ORSD acceptance and product effectiveness are
separate future work. Compatible fixes use 2.1.x; the next accepted compatible
capability may use 2.2.0. Major bumps require a justified incompatible contract.
