# Stable-core inventory — 0.1.0

This completes the read-only #330 inventory, not an ontology implementation or
GA release. Source `c9792b25f7a837b3a34d2a868243e5f5e4dc1198`. Araz approved the
small supported-cut strategy and delegated sequencing; the current approved
[planning record](../../../roadmap/0.2.0/README.md) records that actual decision.

## Exact layers and boundaries

| Layer | Exact retained input | Support meaning |
|---|---|---|
| Compatibility reference | Six frozen W5 modules; 642 triples; 81 OWL classes, 6 datatypes, 52 object properties, 5 datatype properties | Preserve existing 2.0 research contract/namespace and tests; no new whole-model semantic acceptance |
| Selected new 2.1 candidate | Dataset, DatasetRelease, SourceRecord, ProvenanceActivity, hasDatasetRelease, containsSourceRecord; M001–M004 / Q21-01 | A separate M1 provenance profile to isolate and test; not a promotion of the whole modern candidate |
| Historical M1 validation inputs | Full P3 active.ttl: 1,649 triples; constraints.ttl: 764 triples | Historical evidence source, not the new supported import boundary |
| Experimental future work | Full modern native candidate, RM/PV/BA/DS, broader mappings/detectors/expert/product/research results | Preserved, not deleted or silently accepted; incremental later releases |

[files.csv](files.csv) pins **29 directly inventoried source/runtime/reference
files**. [terms.csv](terms.csv) records 144 named historical class/datatype/property
IRIs plus six proposed profile IRIs. Those 150 rows are not native concept counts.
The scripts' static imports, copied-database fixture dependencies and direct
Python/PostGIS versions are in [inventory.json](inventory.json). Transitive runtime
locking and new cold replay remain release work; no offline completeness claim.

## What the audit actually found

1. **CORE-F01:** the historical M1 verifier reads the entire experimental P3
   ontology and shapes, although its export consumes only the six named terms.
   A separate support entrypoint is needed to keep unaccepted research out of
   the new stable import boundary.
2. **CORE-F02:** none of the four selected classes has a direct `sh:targetClass`
   shape. Historical `targetSubjectsOf` predicates also do not match M1's emitted
   predicates; no targetNode/targetObjectsOf/advanced targets supply this coverage.
   Historical conformance is preserved, but it does not establish targeted M1
   data-completeness validation. No fresh SHACL execution is claimed here.
3. **CORE-F03:** FR-28 includes issuer/system/subject identifier semantics beyond
   the current release/row/hash composite key. Keep the useful scoped key without
   declaring that whole requirement complete. FR-25 is the selected provenance
   path; FR-01/02 are compatibility/reference or retained broader work.

The outgoing logical signatures of all six terms match their W5 counterparts
after namespace normalization. This does not assert `owl:equivalentClass`, a
complete semantic-module extraction or equivalence of the whole versions. Incoming
axioms are inventoried for the extraction review; do not retain only subject
triples and claim every original axiom was preserved. Exact W5 source bytes and
the frozen graph fingerprint match. No DB write, namespace rewrite, fresh reasoner,
full native detector or runtime compatibility result is invented.

## Before 2.1.0

[#331](https://github.com/ArazSaieArasi3/CM-PharmE/issues/331) isolates the six-term
profile and adds targeted positive/negative/boundary checks, focus-node counts,
required declarations and appropriate formal/roundtrip evidence. Profile-specific
data completeness stays separate from universal OWL cardinalities. Then replay
the selected copied-W6 SQL/SPARQL integration as its own bounded packet before
new release assembly. Neither historical M1 nor published RC content is edited.

[requirements.csv](requirements.csv) records all sixteen initial audit seeds and
quality obligations without approving their historical ORSD rows. This audit has
finished its exit even though the two concrete implementation blockers are open.
No known critical defect in the retained support closure is waived by D-01.

Run with the existing rdflib 7.5.0 environment:
`python v2/release/2.1/core/0.1.0/inventory.py`.
The new original narrative/code and expressly inventoried owned source assets
follow the approved [license scope](../../../roadmap/0.2.0/license-scope.json).
Third-party terms and historical payloads remain separate.
