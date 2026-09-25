# V2 Data / KG Architecture Documentation QA — Issue #237

**Date:** 2026-09-25  
**Issue:** #237  
**Authority ref:** `v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999`  
**Status:** PRE-PUBLICATION PASS

## Deliverable coverage

- end-to-end architecture overview: **PASS**
- provenance/evidence flow: **PASS**
- ontology↔RDB↔RDF/KG mapping explanation: **PASS**
- deterministic KG generation/query explanation: **PASS**
- SQL↔SPARQL benchmark explanation: **PASS**
- API/query boundary: **PASS**
- reproducible source→RDB→KG trace: **PASS**
- database/ontology cross-links: **PASS**
- mandatory diagrams: **5/5**

## Governed diagram package

New governed diagrams:
- DGM-ARC-004 — source→transformation→RDB→KG;
- DGM-ARC-005 — provenance/evidence flow;
- DGM-ARC-006 — ontology↔RDB↔RDF/KG mapping;
- DGM-ARC-007 — SQL↔SPARQL benchmark path;
- DGM-ARC-008 — API/query boundary.

All five have editable Mermaid source, committed SVG output, title/description, internal white canvas, explicit foreground/background and `data-theme-safe="true"`. Cache-busted embeds use content-derived SHA-256 keys.

Governed-diagram manifest after #237 candidate changes: **34 diagrams**.

## Evidence reconciliation

Documentation is reconciled to W6/E10:
- SourceRecords: **7**
- Assertions: **7**
- EvidenceSupport records: **7**
- relational aggregate observations: **7**
- accepted exact fixture match assertions: **2**
- RDF ABox triples: **398**
- mapping-registry entries: **36**
- unresolved registered ontology IRIs: **0**
- class/cardinality checks: **14/14 PASS**
- relation/cardinality checks: **10/10 PASS**
- deterministic identity round trips: **44/44 PASS**
- aggregate→metric RDF projection: **7 rows → 28 expected / 28 observed metric nodes**
- frozen SQL↔SPARQL pairs: **4/4 PASS**
- KG canonical SHA-256: `6f93a00c2fa9a853e44db80b547d69f8033719948a03cf09b2b175dff5b40825`

## End-to-end trace verification

The first committed outpatient fixture row was independently recomputed using the exact `bootstrap_ingest.py` algorithms.

Verified values:
- `source_hash`: `fc4f28d217129c90048aa48ae817d46ec9700198bd225de85897488d523817f4`
- transformation run: `run:w6-fixture:3cef83edd2c025392ef3`
- substance public ID: `substance:source-label:5b7c9e04321068d35ae0`
- product public ID: `product:source-normalized:c8a9859abe6ffd900982`
- presentation public ID: `presentation:nhif:b1730e50e764943e8891`

The trace preserves SourceRecord → Assertion/EvidenceSupport → relational ObservationResult → metric-level RDF projection and exposes the same SourceRecord hash at the bounded provenance API contract.

## Mapping-boundary verification

E10 mapping status distribution is preserved:
- direct: **26**
- bounded: **4**
- polymorphic: **2**
- relational projection: **1**
- one-to-many RDF projection: **1**
- deferred: **2**

The documentation does not convert the ten non-direct mappings into lossless-equivalence claims.

## Claim-boundary verification

PASS:
- EntityMatchAssertion is described as an auditable matching assertion, not proof of identity.
- IdentifierAssignment is not described as entity identity.
- 4/4 SQL↔SPARQL is bounded to the registered benchmark suite.
- OpenAPI is described as a read-only research/interface contract, not production deployment.
- fixtures are described as deterministic schema-faithful test data, not full external-dataset ingestion or empirical outcome evidence.

## Publication state

Seven new source-complete Wiki pages are registered as **pending** until the controlled publication workflow completes. Publication/rendered-Wiki verification must be recorded before #237 closure.
