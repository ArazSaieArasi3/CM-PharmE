# ORSD execution ledger 0.2.0 — first independent contract slice

Target: **CM-PharmE ontology 2.1 research candidate**, not a release. Canonical requirements: **ORSD document 0.2.0**; the historical [ledger 0.1.0](../0.1.0/README.md) is preserved. This execution version adds bounded evidence for FR-01–FR-03 ([issue #316](https://github.com/ArazSaieArasi3/CM-PharmE/issues/316)). [Ledger with all 83 stable IDs](traceability-ledger.csv); [oracles fixed before witnesses](fixed-oracles.json); [runner](run_slice.py); [observed results](results.json).

## Reproduction and provenance

The source snapshot is commit `d01f48bd7be76e02490177c1e6ebcb40825d77a3` on `v2/connectivity-audit-2-1-candidate`. Input SHA-256 values for the ORSD and the latest integrated G3-P4a native, OWL and SHACL model are in `fixed-oracles.json` and checked by the runner. The oracle file was committed first as [`6452d379`](https://github.com/ArazSaieArasi3/CM-PharmE/commit/6452d379ab070486fe632a2146eb249c703a30d0), before the fixtures and runner existed. These are **synthetic** named witnesses; no company, facility or source record is claimed to exist in the empirical dataset. The underlying model still describes itself as a provisional G3-2e-F OWL subset and is not silently relabeled as a release.

From the repository root, with Python 3.12, RDFLib 7.6.0, pySHACL 0.30.1 and owlrl 7.6.2:

```bash
python v2/requirements/2.1/execution/0.2.0/run_slice.py
```

The runner checks pinned hashes, executes RDFLib SPARQL queries against named ABoxes, evaluates the candidate SHACL profile with pySHACL and applies OWL RL entailment for the range/inference diagnostic. It compares every expected field of all three contracts with observations and exits nonzero on a mismatch. `results.json` records the command environment, separate expected/observed values, graph sizes, native ID lookup and supplemental diagnostics. The identity countermodel uses the actual OWL `AllDisjointClasses` axiom to detect the contradictory dual typing; this is an explicit axiom check, not a full DL consistency run.

## Crosswalk and dispositions

| Contract | Native IDs in pinned OntoUML | OWL axioms / executable route | SHACL / observed bounded result | Remaining scope |
|---|---|---|---|---|
| FR-01 | `Organization`, `Facility`, `FacilityOperation`, `rel-operates`, `rel-operationOrganization`, `rel-operationFacility` | `Organization` and `Facility` occur in `owl:AllDisjointClasses`; query joins `FacilityOperation` via `operationOrganization` and `operationFacility`. | `FacilityOperationShape` requires both endpoints; 2/2 pairs returned; same-label no-link 0; incomplete relator 0 query results and fails admission; collapsed identity countermodel contradicts disjointness. | `operates` is marked `derivedFromRelator` but OWL RL did **not** entail a direct `operates` triple from the two mediated links. The two endpoints' exact identities are stipulated in the synthetic fixture; no source identities verified. |
| FR-02 | `Organization`, `ManufacturerRole`, `ImporterRole`, `WholesaleDistributorRole`, `ManufacturingResponsibility`, `ManufacturingResponsibilitySubjectRole`, `rel-manufacturingResponsibilityHolder`, `rel-manufacturingResponsibilityCounterpart` | `ManufacturerRole` is a subclass of `Organization` with inverse responsibility restriction; `manufacturingResponsibilityHolder` has range `ManufacturerRole`. Query requires the explicit responsibility and product-side counterpart. | `ManufacturerRoleDependenceShape` plus `ManufacturingResponsibilityShape`; 1 contextual manufacturing answer; name-only 0; incomplete responsibility fails admission; range infers the holder role but cannot fabricate a missing counterpart. | One manufacturing witness only. Importer and wholesale anchors were found in native and OWL, but their own context witnesses and real source coverage were not executed here. |
| FR-03 | `FacilityOperation`, `OperatingOrganizationRole`, `OperatedFacilityRole`, `rel-operationOrganization`, `rel-operationFacility` | `FacilityOperation` is a Relator; OWL has qualified min 1 for both participant roles, max 1 for the facility role and mediation property domains/ranges. Query uses the explicit relator. | `FacilityOperationShape` and inverse role-dependence shapes; 1/1 operation; both parties `locatedIn` one `GeographicFeature` but 0 operation answers; missing facility 0 query answers and fails admission. | OWL's existential restriction permits an unknown participant on incomplete ABoxes. No claim of a real operator/site, temporal policy or materialized direct `operates` link. |

All three **fixed synthetic-contract expectations passed**. The positive witnesses conform to the pinned SHACL profile; the no-relation negative witnesses also conform, correctly expressing absence of an answer without treating absence as OWL falsity. The boundary witnesses fail admission **only under the declared SHACL profile**. This does not give semantic acceptance to all three requirements: every row's `acceptance_status` remains `PENDING_SEMANTIC_REVIEW`, with author review, source-backed regression, direct relation semantics and the other role contexts open. The model's identifier presence, scoped semantic checks and empirical acceptance have distinct meanings.

## Ledger accounting

83 unique rows remain: 71 functional and 12 quality. FR-01–FR-03 moved from `SPECIFIED_NOT_EXECUTED` to `BOUNDED_FRESH_EXECUTION`; therefore 44 functional rows remain in that prior category, 23 are bounded prior replays and one is the earlier fresh scoped query/countermodel. The three new passes share fixture building blocks and count as three requirement dispositions, not three independent source datasets. No quality contract or author-accepted requirement was added.
