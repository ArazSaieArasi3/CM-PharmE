# G3-2e-E — bounded native OntoUML integration candidate

Date: 2026-10-08 Asia/Tehran. Source: G3-2d native overlay (520 elements), G3-2e-C scientific approval (13 bounded decisions), W4 specification and bounded M016 mapping. Candidate branch only; draft PR #305 and issue #306 remain open.

## Native delta

The candidate has **524 elements**: one typed `MedicinalProduct → PharmaceuticalSubstance` `productHasActiveSubstance` relation, its two ends, and one scope note. It changes two existing end-pairs' multiplicities:

- `capabilityBearer` is still Mode→Organization. Mode end `0..*`, Organization end `1`: each modeled EnterpriseCapability has exactly one Organization; an Organization need not bear any. This is **not** a Characterization and does not claim complete Mode conformance.
- `hasMatchConfidence` is Assertion→Quality. Assertion end `1`, Quality end `0..*`: each linked MatchConfidence belongs to exactly one EntityMatchAssertion; an Assertion may have no confidence. This is **not** a Characterization and does not claim complete Quality conformance.
- `productHasActiveSubstance` is Product→Substance with `0..*` at both ends. The bounded M016 primary-substance hook supports the Product scope, without claiming universal existence, maximum one, Presentation scope, or part-whole composition. It is **intended** as a child of the existing broad `hasActiveSubstance`; native JSON does not itself encode that subproperty inference. OWL/SHACL alignment is due in G3-2e-F.

All 13 accepted decisions are preserved in the relevant relation descriptions. The `decision-implementation.json` ledger identifies three partial native changes, nine typed/guarded retentions, and one formal-design blocker.

## Formal design blocker

The accepted `capacityBearer` decision requires a SupplyCapacity Mode to have **exactly one** Organization or Facility bearer. Its generic native target remains null. Two optional typed routes alone permit zero or two bearers; a Characterization from Organization or Facility to the Mode would falsely require every such bearer to exemplify capacity. The same Characterization issue prevents a blanket inverse for EnterpriseCapability, while the unscored EntityMatchAssertion case blocks a universal hasMatchConfidence minimum. The official specification describes Characterization as bearer→Mode/Quality, with bearer end exactly one and feature end at least one for that bearer type. See [Characterization](https://ontouml.readthedocs.io/en/latest/relationships/characterization/index.html), [Mode](https://ontouml.readthedocs.io/en/latest/classes/aspects/mode/index.html), and [Quality](https://ontouml.readthedocs.io/en/latest/classes/aspects/quality/index.html). We retain these as explicit conformance blockers rather than inventing global existence axioms.

## Verification scope

`static-checks.json` verifies 524 unique identifiers, root references, typed endpoint references, retention of all 520 baseline elements, exactly 13 annotated decisions, cardinalities and the native named-class graph. The graph remains **138 classes, 15 components and 14 isolates**. No official parser, anti-pattern tooling, integrated OWL reasoner, SHACL or real-data migration was run on this new overlay. Isolate connector proposals remain unapproved.

## Next

G3-2e-F aligns OWL/SHACL for the supported subset, exercises positive and negative cases, and resolves the `operates` derivation or documents a precise exclusion. Formal bearer modeling and official OntoUML conformance remain separate gates. See `g3-closure-plan.json`.
