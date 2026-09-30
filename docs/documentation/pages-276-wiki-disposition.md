# Post-Pages Wiki disposition — #276

Assessment source: `67b1630bc3686195b781cfa02d1d4c07094e110b`, after #301.

Pages now supplies WIDOCO formal lookup and WebVOWL. The Wiki reference generator
also consumes concept passports, UFO/OntoUML stereotypes, module ownership,
review state, protected distinctions and V1 lineage. These are not interchangeable
with WIDOCO's OWL projection. Retaining those pages is justified by their evidence
and interpretation value, rather than by a second manually authored OWL catalogue.

The per-page matrix is `pages-276-wiki-disposition.json`. Each candidate has a
decision, rationale, content hash and inbound-link count. Concept, module and
property projections remain deterministic products of
`tools/wiki/generate_ontology_reference.py`; semantic edits belong in the source,
not in two documentation surfaces. Synchronization remains governed by #213/#214.

| Family | Decision | Retained value |
|---|---|---|
| 87 concept pages | RETAIN_CURATED | Concept passport, stereotype, protected distinctions, lineage, evidence and pending review |
| 17 module pages | RETAIN_CURATED | Layer ownership, modeling rationale, contextual constraints and evaluation |
| 52 object-property pages | RETAIN_CURATED | Explicit endpoints, relator derivation, relation review and semantic boundaries |
| 5 datatype-property pages | RETAIN_BRIDGE | Formal lookup linked to conceptual/data/review context |
| V2 reference index | RETAIN_BRIDGE | Conceptual/formal distinction and module/entity navigation; Pages links added by #274 |
| V1/V2 formal guides | RETAIN_CURATED | Engineering status, logical limits and executable validation interpretation |
| Diagram suite | RETAIN_CURATED | Authored multi-level views and explicit modeling notes |
| Ontology/reference guides | RETAIN_BRIDGE | Reader choice between explanation, generated reference and source |
| Migration and conceptual pages | NO_CHANGE | Evolution and conceptual commitments beyond OWL |

Before/after information architecture: the same pages, slugs, headings and Wiki
links remain; #274 adds direct generated-reference/explorer/source journeys.
No page is removed, moved or redirected, so inbound compatibility is preserved.
Page count reduction is zero. Existing unique content remains byte-for-byte intact
at assessment; the audit compares every candidate against its recorded hash.

The Wiki index retains 87 conceptual elements versus 81 OWL classes and 6 datatypes.
Pending semantic review remains pending; keeping explanatory pages does not approve
the ontology. WIDOCO adoption does not replace curated explanation or the diagram suite.

Validation: `python tools/pages/audit_wiki_disposition.py`, Wiki source/navigation
checks, #274 published link/reader-journey report and successful Wiki publication.
