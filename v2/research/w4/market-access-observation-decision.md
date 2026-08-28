# V2 Market Access Observation Decision

Issue: #157

## Decision
For CM-PharmE 2.0, `ReimbursementUtilisationObservationResult` remains one umbrella observation-result subkind with the human-facing label **Reimbursement and Utilization Observation Result**.

## Rationale
- The currently admitted Market Access evidence and mappings do not require a split for the present V2 research scope.
- The umbrella concept remains sufficient for the existing competency-query and cross-representation commitments.
- Splitting now would propagate into OWL/SHACL, mappings, evaluation baselines, W8 views, and manuscript traceability without a demonstrated requirement.
- This is an evidence-bounded modeling choice, not an assertion that reimbursement and utilization are universally the same phenomenon.

## Boundary
- V2 only.
- No change to `main` or CM-PharmE 1.x.
- No IRI change.
- No stereotype change.
- No inventory change: 87 concepts remain 87.
- A future split requires a new evidence-backed design decision in a later ontology version.
