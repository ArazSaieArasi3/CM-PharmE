# G3-P3 FacilityOperation decision overlay — bounded 2.1 candidate

This folder is a new review snapshot built from the hash-pinned [G3-P4a package](../2.1.0-alpha.1-g3-p4a-supply-capacity/README.md). It implements [DEC-21-01/02](../../../release/2.1/0.1.0/decision-register.csv) for ORSD FR-01/FR-03 and #306/#319. It is not a final 2.1 ontology or an expert-reviewed global policy. Previous candidate snapshots and the stable W6 2.0 model remain unchanged.

## Decision and rationale

One `FacilityOperation` represents one accountable Organization operating one Facility within a scoped assignment. A jointly operated site has separate relators (one per organization); a successive operator gets a separate relator. Each retains its own identifier and potentially distinct time/source evidence. This fits the current W6 single `organization_id` per operation without imposing a global one-operator-per-facility rule. The latter would falsely rule out joint or successive operations.

The native `end-operationOrganization-target` cardinality changes from `1..*` to `1`; the OWL `FacilityOperation` gets qualified max-one on `operationOrganization` in addition to the inherited min-one; the SHACL `FacilityOperationShape` gets maxCount one. The facility end was already exactly one. The native derived `operates` material relation now has an OWL property chain `inverse(operationOrganization) o operationFacility`. An asserted direct `operates` edge must have an explicit `FacilityOperation` mediator under the new SHACL admission shape. Missing participant triples remain unknown in open-world OWL, while incomplete relator records fail this named admission profile.

## Reproduce and results

From the repository root, with Python 3.12, RDFLib 7.6.0, pySHACL 0.30.1, owlrl 7.6.2, Owlready2 0.49 and Java:

```bash
python v2/ontology/candidates/2.1.0-alpha.1-p3-facility-operation/build_candidate.py
python v2/ontology/candidates/2.1.0-alpha.1-p3-facility-operation/validate_candidate.py
node v2/ontology/candidates/2.1.0-alpha.1-g3-p4a-supply-capacity/check_native.cjs v2/ontology/candidates/2.1.0-alpha.1-p3-facility-operation/ontouml.json /path/to/node_modules v2/ontology/candidates/2.1.0-alpha.1-p3-facility-operation/official-native-results.json
```

The Node dependencies are `ontouml-js@1.0.0`, `ontouml-schema@1.0.2`, `ajv@8`, `ajv-formats`. [Build manifest](build-manifest.json) pins the G3-P4a input SHA-256 values. [Validation results](validation-results.json) record **10/10** positive, negative and missing-information SHACL expectations, OWL RL derived relation results (two sites and joint operation via separate relators each produce two correct pairs; co-location produces none), three HermiT consistency checks including an explicitly distinct two-operator countermodel, and the unchanged **39,272-triple/768-row** mapped P1 ABox passing the candidate SHACL profile with zero violations. That ABox contains **zero** `FacilityOperation` instances, so it checks nonregression, not real operation coverage. [Official native parser and schema](official-native-results.json) pass with zero schema errors and 144 parsed classes.

## Limits and next gate

The one-operator-per-relator decision is the best bounded rule for this release candidate because it preserves independent identity/time/source evidence and makes the W6 mapping representable. It remains reviewable: evidence of a genuinely indivisible multi-organization operation would require a new decision and likely a different SQL projection. This package does not establish operation source provenance, complete OntoUML anti-pattern conformance, author/expert acceptance, full ORSD coverage, or database SQL↔SPARQL parity. #306 and #319 remain open for those wider gates.
