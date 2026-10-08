# G3-3-B2 — Mode natures, BinOver and DecInt checks, RepRel witness packet

The [review overlay](ontouml-b2-review-overlay.json) is a separate OntoUML candidate based on G3-3-B. It sets `restrictedTo: ["intrinsic-mode"]` for `EnterpriseCapability` and `SupplyCapacity`, consistent with the author's bounded acceptance that each Mode inheres in one bearer. It **does not** solve the missing typed Organization/Facility exactly-one-of-two bearer route for `SupplyCapacity`, or make every Organization/Facility instantiate a Mode.

It removes one redundant direct `ListingResponsibleOrganizationRole → Organization` generalization. The role still specializes `ProductResponsibleLabelerRole → Organization`; the direct edge was not used in a generalization set. The transitive ancestry of **every class is unchanged**. The native element count is 524 → 523, with 144 classes unchanged. The DecInt multiple-concrete-parent trigger disappears, and the archived validator no longer double-counts the same ultimate sortal.

| Executed check | Result | Scope |
| --- | --- | --- |
| OntoUML Schema 1.0.2 and JS parser 1.0.0 | Valid, zero schema errors; 144 classes parsed | Direct review overlay |
| Legacy JS 0.4.1 syntax verifier | 0 diagnostics (prior candidate 244, G3-3-B overlay 2) | Compatibility projection; not full catalogue |
| Archived graph validator | 0 warnings/errors in 13 implemented class rules | RDF projection with source class metadata restored; not full catalogue |
| pySHACL 0.30.1 geography cases | 6/6 expected pass/fail | Existing G3-2e-F `GeographyShape`, selected shape only |
| pySHACL 0.30.1 RepRel cases | 19/19 same-party-tuple duplicate relator pairs accepted; 19/19 missing-party negatives rejected | Each focal relator shape only, synthetic instances; no time or provenance policy in those fixtures |

The two BinOver links `withinCountry` and `withinRegion` already have author-approved no-self-containment decisions, `owl:IrreflexiveProperty` declarations, and an existing SHACL cycle rule. [Executed fixtures](shacl-fixture-results.json) confirm that the selected rule accepts ordinary containment and rejects country/region self links and a two-step cycle. This is a bounded resolution of the self-loop risk; broader overlapping-type behavior and actual versioned geographic source admission still need review. The source geography shape contains a duplicated equivalent SPARQL constraint; the fixtures test the actual existing shape. Deduplication is a later cleanup, not required for the behavior tested here.

The [19-row RepRel dossier](reprel-19-decision-docket.json) identifies the mediated end types, other existing references, a **candidate** discriminator to check, and positive/rejecting witness criteria for each relator. The duplicated participant tuple is permitted by each focal SHACL shape, so whether concurrent duplicates are legitimate remains a scientific decision. Imposing `max 1` on the relator ends would also forbid some potentially valid historical or scoped instances; no such axiom was added. Official [RepRel](https://ontouml.readthedocs.io/en/latest/anti-patterns/RepRel/index.html) and [BinOver](https://ontouml.readthedocs.io/en/latest/anti-patterns/BinOver/index.html) definitions guide these tests.

Reproduction: run [make_b2_overlay.py](make_b2_overlay.py) as `python make_b2_overlay.py <G3-3-B/ontouml-nature-overlay.json> <output.json>`; run G3-3-A `run_checks.cjs` on the output with pinned JS packages. Run [pySHACL fixtures](run_b2_shacl_fixtures.py) as `python run_b2_shacl_fixtures.py <G3-2e-F/constraints.ttl> <G3-2e-E/ontouml.json> <G3-3-B/pattern-prefilter.json> <results.json>` with pySHACL 0.30.1. The [summary](test-and-gate-summary.json) records the exact boundary.

## Gate and exact next action

G3-P5 remains **in progress**. Zero errors in these scoped checks are not a certificate for the 20 anti-patterns, and the formal `SupplyCapacity` bearer route is open. The next bounded step **G3-3-B3** is to examine the 10 ImpAbs endpoints, implement bounded RelComp/RelOver structural checks, and convert the 19 RepRel questions into a concise scientific decision packet with source/temporal evidence; maintain any full-detector gap explicitly. Then G3-3-C–F cover OWL/SHACL integrated validation, real data, connectivity and reviewer handoff.

G1/G2 closed = **2/5 major stages, 40% closed**. G3 still has **2/7 packages, 28.6% closed**; P3/P4/P5 are in progress. B3 and C–F are five bounded work turns, plus author decisions and any additional detector work. PR #305 remains draft and issue #306 open.
