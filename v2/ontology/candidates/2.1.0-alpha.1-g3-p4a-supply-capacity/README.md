# G3-P4a — typed SupplyCapacity bearer routes (review candidate)

This package implements the previously accepted bounded scientific choice tracked by [issue #309](https://github.com/ArazSaieArasi3/CM-PharmE/issues/309). It is a **candidate** for ontology 2.1, not a release or a blanket OntoUML anti-pattern certificate. The G3-F human review packet remains the baseline; draft PR #305 remains draft.

## Model and traceability

| Decision | Native OntoUML | OWL DL | SHACL / executable witness |
|---|---|---|---|
| SupplyCapacity remains an intrinsic Mode | `SupplyCapacity.restrictedTo = intrinsic-mode` | Existing `SupplyCapacity` class and Mode disjointness | Observation and Mode collision rejected |
| Organization bearer | `organizationHasSupplyCapacity`, bearer→Mode `characterization`, 0..* capacities per bearer and 0..1 bearer per capacity | Inverse of `capacityOrganizationBearer`; inverse subproperty of `capacityBearer` | Inverse path on SupplyCapacity; positive Organization fixture |
| Facility bearer | `facilityHasSupplyCapacity`, same direction and multiplicities | Inverse of `capacityFacilityBearer`; inverse subproperty of `capacityBearer` | Positive Facility fixture |
| Exactly one bearer across routes | Native note `p4a-capacity-xor-note` documents combined constraint, because isolated per-route bounds cannot express XOR | Unqualified cardinality 1 on broad `capacityBearer` plus union of typed existentials; Organization/Facility are disjoint | Combined inverse-path min/max 1, per-route XOR, typed bearer; no-bearer, two-route, two-bearer and wrong-type negatives |
| Common query surface | Existing `capacityBearer` now documented as derived; typed inverse relations also derived | Inverse and subproperty entailment | Explicit query assertions must match a primary bearer assertion; broad-only and inverse-only rejected |
| Capacity observation separate | Existing `SupplyCapacityObservationResult` unchanged | Existing disjoint classes | Observation as Mode is rejected; no Organization or Facility is globally required to have any capacity |

The native relation-end cardinalities express the count of bearer instances associated with each Mode (source end `0..1`) and the count of Mode instances per bearer (target end `0..*`). The OWL existence axiom does **not** demand that a bearer be explicitly asserted in an open-world ABox. Two IRIs may denote one bearer absent `owl:differentFrom`; this is why closed-world SHACL and OWL DL report different results for those two cases. The native XOR note is explanatory, while OWL and SHACL supply executable combined policies.

## Files and reproduced outcome

- `build_p4a.py` deterministically builds `ontouml.json`, `active.ttl`, `constraints.ttl` and `integration-manifest.json` from the frozen B2/G3-C inputs. The outputs add 13 native elements (four relations, eight ends, one note); native elements 523→536, 138 named classes plus six datatypes unchanged, relation and OWL object-property names both 86.
- `check_native.cjs` checks the official `ontouml-schema@1.0.2` and parses with `ontouml-js@1.0.0`; `official-native-results.json` records **pass, zero schema errors, 144 parsed classes**.
- `validate_p4a.py` generates `validation-results.json`: **16/16** scoped SHACL fixtures; **11/11** G3-C SHACL regressions (the prior bearer-free gap intentionally changes from accept to reject); **9/9** HermiT fixture/coherence expectations; OWL RL inverse/subproperty entailment; and all 39,272 triples of the 768-row mapped real-source ABox pass full candidate SHACL with zero results.
- `validate_real_abox.py` generates `abox-reasoner-results.json`: full mapped ABox plus the new TBox is consistent with no unsatisfiable named classes, and a deliberately contradictory type assertion is detected.
- Structural native named-class graph: 138 nodes; typed relation edges 71→75, unique class-pair edges 168→170; components 15→14, largest component 124→125; isolates 14→13. `SupplyCapacity` is the one isolate connected by this change. This graph metric does not measure full ontological adequacy.

To reproduce with compatible dependencies installed, run `python build_p4a.py` from the package directory, `node check_native.cjs ontouml.json <node_modules> official-native-results.json`, `python validate_p4a.py`, and `python validate_real_abox.py active.ttl ../g3-3-d-real-source-migration/real-source-abox.nt abox-reasoner-results.json`. The Python commands need RDFLib 7.6.0, pySHACL 0.30.1, Owlready2 0.49 and owlrl. The full ABox is recoverable from the G3-D `real-source-abox.nt.gz.b64` artifact; it is omitted here to avoid duplication.

## Gate and next work

The bounded 768-record nonrandom P1 source ABox contains **zero** `SupplyCapacity` individuals; it establishes nonregression, not empirical truth of these bearer routes. The other 13 isolates still need concept-by-concept evidence before a proposed edge is accepted. G3-P3 scientific relation decisions, G3-P5 official full 20-antipattern execution, G3-P6 source contract #307 and wider source evidence, and G3-P7 human review remain open. Do not merge PR #305 or promote a final 2.1 release on this checkpoint.
