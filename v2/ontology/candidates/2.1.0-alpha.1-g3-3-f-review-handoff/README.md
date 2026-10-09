# G3-3-F — traceability and human-review handoff

Date: 2026-10-09 Asia/Tehran. Candidate branch: `v2/connectivity-audit-2-1-candidate`. This closes the **bounded B3–F preparation sequence**, not G3, the ontology release, or the scientific acceptance gate.

## Two immediate review views

- [Domain → all current concept titles](DOMAIN-TABLE.md): 17 canonical W4 domains, 144 active candidate elements, 14 highlighted named-class isolates at the beginning of their domains.
- [Fourteen isolated concepts and short Persian definitions](ISOLATES-FA.md): one-line definitions paraphrase each Gate-D wiki concept page. [Provenance and English originals](isolate-definitions.json).

The active model has **138 named classes + six datatypes**. Of the 87 earlier Gate-D concepts, 84 remain in the current candidate and three are deliberately deferred (`AssetAtRisk` and `Vulnerability`: S-04; `ClinicalCareParticipant`: S-05). The candidate introduces 60 other roles/relators; their primary-domain allocations are **editorial recommendations pending author review**, not an inherited 87-row authoritative assignment. [Exact domain crosswalk](domain-inventory.json) and [reproducer](build_domain_inventory.py) assert one-to-one coverage.

## Scientific and evidence traceability

[Machine-readable matrix](traceability-matrix.json) and [reproducer](build_handoff.py) trace the pending work to actual native elements, OWL declarations, direct SHACL property paths when present, prior fixtures, source anchors and direct assertions in the bounded real-source ABox. A direct SHACL path alone does not prove the targeted scientific policy, and a zero count in five NHIF slices does not prove absence in other sources. The families below **overlap**; their counts must not be summed as distinct decisions.

| Review family | Rows | Prior evidence | Remaining decision |
|---|---:|---|---|
| Relation dispositions | 29 pending of 42; 13 bounded recommendations already accepted | Native and OWL crosswalk; five pending properties asserted by the bounded P1 mapping | Author decides truthmaker, end typing and scope; focused positive/negative tests follow. |
| Isolate connector proposals | 14 | G3-E: 15 components/14 isolates; no direct source-class or proposed-relation witness in the 768-row sample | Decide each conditional connector only with its truthmaker; optional isolates may legitimately remain. |
| ImpAbs endpoint questions | 10 ends across six relations | B3 structural prefilter, not complete official detection | Decide subtype-specific bounds or properties with counterexamples. |
| RepRel tuple policies | 19 relators | B2 duplicate/missing-end fixtures; B3 evidence ranking | Decide whether repeated same-party relators are valid by context/time or tuple identity; no blanket max-one. |
| Full anti-pattern catalogue | 20 entries triaged | Scoped prefilters only | Run the complete official engine and scientifically triage actual findings. |

The five **pending** relations with at least one direct assertion in the *mapped P1 sample* are `containsSourceRecord` (768), `hasDatasetRelease` (1), `observationAboutPresentation` (3,072), `observationAboutProduct` (3,072), and `reimbursementDiagnosisContext` (3,072). The mapping is a bounded projection, not final author approval of global relation semantics. Two of the 19 reviewed relator classes have direct P1 instances: `IdentifierAssignment` and `ProductClassificationAssignment` (264 each).

## Review order and actionable gates

1. **[P4a, executable next — issue #309](https://github.com/ArazSaieArasi3/CM-PharmE/issues/309):** implement the already accepted **scoped** SupplyCapacity bearer design in a separate candidate. Use typed Organization and Facility routes with exactly one eligible bearer for each Mode; add native, OWL and SHACL positive and negative witnesses. Do not force every Organization/Facility to bear a SupplyCapacity or equate a measurement with the Mode.
2. **P3 scientific review:** start with the five P1-witnessed pending relations, then adjudicate the remaining 24 relation rows, 14 isolate connectors, 10 ImpAbs ends and 19 RepRel policies. Each row in the matrix has a question, negative acceptance or fixture reference; overlap is explicit.
3. **P5 official detection:** run all 20 anti-patterns on the authoritative OntoUML model, recording tool version, raw finding, truthmaker, disposition, and regression witness. The existing prefilter does not certify clean status.
4. **P6 empirical/contract:** repair [issue #307](https://github.com/ArazSaieArasi3/CM-PharmE/issues/307) for the Zenodo filename contract; extend declared-source evaluation beyond five nonrandom byte-range slices where feasible, with provenance and checksum verification.
5. **P7 review/release gate:** the author checks the 60 provisional primary-domain allocations and three deliberate deferrals, then accepts the trace and formal evidence. Keep [PR #305](https://github.com/ArazSaieArasi3/CM-PharmE/pull/305) draft and [issue #306](https://github.com/ArazSaieArasi3/CM-PharmE/issues/306) open until those gates are actually met.

For each gate, the [matrix summary](traceability-matrix.json) records an acceptance and a negative condition. In particular, the isolated classes should never be connected merely to improve a topology score. [G3-C](../2.1.0-alpha.1-g3-3-c-integrated-validation/README.md) has 11/11 scoped SHACL and 8/8 HermiT expectations; [G3-D](../2.1.0-alpha.1-g3-3-d-real-source-migration/README.md) has 768/768 admitted P1 rows and 5/5 deliberately corrupted negatives. These bounded passes do not close P3–P7.

## Reproduce

```bash
python build_domain_inventory.py
python build_review_tables.py
PYTHONPATH=/tmp/cmpe-g3c python build_handoff.py
```

For a fresh environment, install `rdflib==7.6.0`, use the repository's sibling candidate folders, and run the last script with that package on the Python path. It decodes the G3-D compressed ABox in memory; exact input hashes appear in the matrix. The frozen source files `registry.json`, `concept-index.md`, `relation-register.json`, and `approved-13.json` are included to make the historical crosswalk and author decision provenance inspectable.

## Progress accounting

G1/G2 are closed: **2/5 major stages = 40%**. G3 remains active with **2/7 named packages closed = 28.6%**. B3, C, D, E, and F are now **5/5 bounded preparation turns = 100%**. The last measure is a preparation-sequence count, not G3 completion or an ontology quality score.
