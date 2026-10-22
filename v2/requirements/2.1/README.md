# CM-PharmE 2.1 research candidate

This directory keeps the 2.1 requirements and their execution plan together without conflating document versions, model candidates, database mappings, manuscript drafts and released ontology versions.

| Layer | Current record | Next gate |
|---|---|---|
| Requirements specification | [ORSD 0.2.0, Word/PDF and source registries](orsd/README.md) | One author content review, then a separately versioned ORSD 1.0.0 freeze |
| Requirement execution | [Ledger 0.1.0 with 83 stable IDs](execution/0.1.0/README.md) | Independent evidence for unexecuted Must contracts, then remaining bounded acceptance |
| Ontology | [Draft PR #305](https://github.com/ArazSaieArasi3/CM-PharmE/pull/305) | Scientific semantics and four-domain decisions; native/OWL/SHACL plus applicable anti-pattern validation |
| Relational representation | W6 2.0 reference, [source integration #307](https://github.com/ArazSaieArasi3/CM-PharmE/issues/307), [2.1 delta #317](https://github.com/ArazSaieArasi3/CM-PharmE/issues/317) | Accepted 2.1 migration and SQL↔SPARQL/provenance regression |
| Paper and release surfaces | [Draft manuscript #171](https://github.com/ArazSaieArasi3/CM-PharmE/issues/171); [program #24](https://github.com/ArazSaieArasi3/CM-PharmE/issues/24) | Evidence-to-claim review, reproducible package, versioned diagrams/docs and actual release |

The ORSD's version `0.2.0` is its **document version**. The ledger's `0.1.0` is the **execution-ledger version**. The ontology target is **CM-PharmE 2.1**; it is currently a research candidate and has no corresponding published GitHub Release. Source snapshots, checks, author decisions and remaining limits are recorded in the linked ledgers.

Historical 1.x reviewer materials stay on `main`; the 2.0 integration line is `v2/research-program`; 2.1 candidate work belongs to its draft PR until its scientific and validation gates pass.
