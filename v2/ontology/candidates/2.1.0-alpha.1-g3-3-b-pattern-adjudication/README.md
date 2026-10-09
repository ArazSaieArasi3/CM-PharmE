# G3-3-B — bounded anti-pattern triage and nature repair candidate

This checkpoint starts from the [G3-2e-E native candidate](../2.1.0-alpha.1-g3-2e-e-native-integration/ontouml.json). It adds a **separate review overlay**, not a release or an edit to the prior model. The overlay changes only `restrictedTo` on 142 of 144 class records; the two unresolved Modes (`EnterpriseCapability`, `SupplyCapacity`) remain empty. All other element JSON is identical. [Per-class proposal and basis](nature-proposals.json) · [native review overlay](ontouml-nature-overlay.json) · [comparison and results](test-and-delta-summary.json).

| Check | Original | Review overlay | Interpretation |
| --- | ---: | ---: | --- |
| OntoUML Schema 1.0.2 / current parser 1.0.0 | Pass / 144 classes | Pass / 144 classes | Exchange validity preserved |
| Legacy JS 0.4.1 compatibility diagnostics | 244: 144 missing natures, 100 generalization natures | 2 missing natures | Proposed metadata removes the cascading generalization warnings; no claim that all semantic issues are solved |
| Archived RDF validator 13 implemented class rules | 144 missing-nature warnings; one apparent provider error | 2 missing-nature warnings; same apparent provider error | Source class metadata had to be restored to the decoded RDF graph; not a 20-pattern detector |

The archived validator package at commit `46f54c1a5225fc9ea74ac2256fd4a673e9101a40` could not be installed as a wheel because its Poetry package path is missing. Its published `execute_all_validation_rules` calls unimplemented cases and throws an end-of-switch error. We invoked only its 13 implemented class rules on the decoded RDF graph **after adding source class name, stereotype, and restrictedTo triples** lost by the compatibility conversion. This scope is fully recorded in [results](archived-validator-overlay-results.json) and [adapter script](run_archived_validator.py). The single `R_CL_ZGT` error on `ListingResponsibleOrganizationRole` counts `Organization` twice: one direct path and one through `ProductResponsibleLabelerRole`; the source has **one distinct ultimate sortal**. This is an archived rule's path-count artifact, not evidence for inventing a second identity provider.

## Catalogue triage

All [20 catalogue entries](catalogue-triage.json) have a documented structural precondition and scoped outcome. The [prefilter](pattern-prefilter.json) is reproducible with [scan_pattern_triggers.py](scan_pattern_triggers.py). It is **not the official full anti-pattern engine** and does not certify a clean model. Key candidates:

| Pattern | Bounded candidates | Disposition |
| --- | ---: | --- |
| BinOver | 2 (`withinCountry`, `withinRegion`) | Broad `GeographicFeature` endpoint overlaps its target subtype. Determine and test irreflexivity or narrow the endpoint without inventing a global exclusion. Cardinalities remain unspecified. |
| DecInt | 1 (`ListingResponsibleOrganizationRole`) | Multiple concrete parents; both paths carry `Organization` identity. Explicitly justify the intersection and nonempty witness before sign-off. |
| ImpAbs | 10 relation-end triggers | Check subtype-specific cardinalities with positive/negative witnesses; a broad association is not automatically wrong. |
| RelSpec | 3 typed association pairs | Both corresponding ends already subset their parent ends; retain with documented implication. Untyped relations need later review. |
| RepRel | 19 Relators | Ask whether the same participant tuple can support repeated/concurrent instances; represent effective time and a justified current uniqueness rule where required. Do not globally set upper 1. |
| RelComp / RelOver | Not fully scanned | Full tool or bounded explicit detector and human adjudication still required. |

Eight structures have no relevant class/relation stereotype in this native model (phase, mixin, meronymic, or formal as applicable). Other zeroes in the ledger are limited to the implemented direct structural scan. The 9 roleMixins considered for MixIden have children with distinct identity-provider **classes**, so its same-provider-only precondition was not found in that bounded review. For example `RegisteredParty` has `Facility` and `Organization` provider paths. This is a structural finding, not a full possible-world proof.

Official catalogue definitions: [anti-pattern index](https://ontouml.readthedocs.io/en/latest/anti-patterns/index.html), [RepRel](https://ontouml.readthedocs.io/en/latest/anti-patterns/RepRel/index.html), [BinOver](https://ontouml.readthedocs.io/en/latest/anti-patterns/BinOver/index.html), [RelSpec](https://ontouml.readthedocs.io/en/latest/anti-patterns/RelSpec/index.html), [RelRig](https://ontouml.readthedocs.io/en/latest/anti-patterns/RelRig/index.html). OLED's archived tool advertises automatic anti-pattern detection but does not supply an established direct current flat-JSON run; the archived Python validator executes class rules, not these 20 detectors. **The full-catalogue gate stays open.**

## Next gate and progress

G3-3-B is **partially executed**: metadata repair tested and catalogue preconditions triaged; no global conformance claim. Next bounded turn **G3-3-B2** should resolve the two Mode natures from bearer/lifecycle evidence and adjudicate the high-priority BinOver, DecInt and RepRel cases with positive and rejecting instances. Then complete the remaining ImpAbs, RelComp, RelOver and full-engine gap before P5 closure. Formal OWL/SHACL, real data, connectivity, and release gates remain G3-3-C–F.

G1/G2 closed = 2/5 major stages (40% closed). G3 remains 2/7 packages closed (28.6%), P3/P4/P5 in progress. Five bounded agent turns remain when B2 plus C–F are counted; additional work may be needed for unresolved anti-pattern coverage and human scientific gates. These percentages measure closure only.
