# G3-3-B3 — bounded pattern closure and scientific decision packet

Input: G3-3-B2 native review overlay (523 elements), B2 synthetic fixtures and the G3-3-B catalogue inventory. This is a **review packet**, not a full anti-pattern clearance.

## Reproduced counts

| Check | Result | Meaning |
| --- | ---: | --- |
| ImpAbs | 10 endpoints / 6 relations | All require domain review of subtype-specific bounds; none is an automatic violation. |
| RelComp | 0 known-cardinality pairs; 2 conditional pairs | The conditional A associations are `withinCountry` and `withinRegion`, whose target bounds are null; no assertion of absence follows. |
| RelOver | 5 relators with potentially overlapping mediated types; 0 prove upper sum >2; 1 has an unknown bound | Four have known sum 2; `EvidenceSupport` has unknown `evidenceRecord` upper and remains conditional. |
| RepRel | 19 decision rows | 4 with typed extra context, 1 with indirect reference, 14 with no extra typed reference; none has an approved tuple/time key. |

There are 82 native binary relations; 71 have both typed endpoints, and 33 have at least one unknown cardinality. Counts use a conservative local scanner, not the official detector. `structural-results.json` contains the exact pairs and subtype lists.

## ImpAbs: 10 endpoint decisions

The official criterion is an association end with upper ≥2 and a connected class with ≥2 subtypes. It asks whether subtype-specific multiplicities or meta-properties are needed. The current broad admission shapes check class membership, not subtype-specific limits. `classificationEntity` and `classificationEntry` each have a contextual specializing relation, but those native relation ends have no cardinality, so they do not close the two questions. Do not infer that every subtype requires a link or add a blanket bound.

| Relation | Triggered ends | Current recommendation |
| --- | --- | --- |
| `assertionAboutProduct` | source, target | Retain broad typing; collect subtype-specific positive and negative instances before adding bounds. |
| `classificationEntity` | source | Review contextual subset and fill only source-supported bounds. |
| `classificationEntry` | source | Review contextual subset and fill only source-supported bounds. |
| `observationAboutPresentation` | source, target | Retain broad typing; collect subtype-specific positive and negative instances before adding bounds. |
| `observationAboutProduct` | source, target | Retain broad typing; collect subtype-specific positive and negative instances before adding bounds. |
| `productHasActiveSubstance` | source, target | Retain broad typing; collect subtype-specific positive and negative instances before adding bounds. |

## RepRel: ranked questions

The typed context in rank A is evidence of a possible discriminator, not a unique key. Rank B contains reverse references that do not establish identity. Rank C requires source data or author input. For all 19, ask whether the same participant tuple can recur concurrently, under different jurisdiction/scope, or in a later interval. The prior selected SHACL fixture accepted duplicates and rejected missing mediation ends; it did not test time. Preserve repeatability until the rule is approved.

| Rank | Relators | Evidence and action |
| --- | --- | --- |
| A (4) | EstablishmentRegistration, MarketListing, RegulatoryAuthorization, EvidenceSupport | Inspect typed jurisdiction or evidence-record reference; establish cardinality, scope and temporal identity. |
| B (1) | SupplyDependency | Check whether disruption and risk-assessment references are merely downstream context. |
| C (14) | All remaining rows in `reprel-evidence-ranked-decisions.json` | Find a source-backed discriminator; a proposed lexical value or period does not yet exist in the native model. |

## Semantic disposition and gate

1. Request concrete positive/rejecting source examples for each ImpAbs subtype family, then constrain only the approved cases in OntoUML and SHACL/OCL.
2. Fill the geography relation bounds from domain evidence; re-run RelComp. Resolve the `EvidenceSupport/evidenceRecord` mediated-end bound and potential dual role; re-run RelOver.
3. Author-adjudicate the 19 RepRel policies; encode any accepted current uniqueness rule with explicit scope and temporal fields and both acceptance/rejection fixtures.
4. Run a compatible official full 20-pattern detector with reproducible model import and inspect every finding. The archived 13 class rules, schema/parser, and these structural scans cannot certify catalogue-wide absence of anti-patterns.

No new ontology axiom was committed in B3: the necessary cardinalities and domain keys are scientifically unconfirmed. G3-P5 remains in progress. The 29 relation dispositions, 14 isolate proposals and the `SupplyCapacity` typed bearer route also remain open.

## Reproduction and next turn

From this directory using Python 3, run `python scan_b3.py ../2.1.0-alpha.1-g3-3-b2-focused-adjudication/ontouml-b2-review-overlay.json .` and `python build_b3_decisions.py . ../2.1.0-alpha.1-g3-3-b2-focused-adjudication/reprel-19-decision-docket.json ../2.1.0-alpha.1-g3-3-b2-focused-adjudication/g3-closure-plan.json`; compare the produced JSON and assertions. The next bounded turn is **G3-3-C: integrated OWL DL and pySHACL validation** of the currently approved candidate, with positive/negative fixtures and reasoner limits explicit. Keep B3's scientific and full-detector gates in the G3 closure list.

G1/G2 are closed (2/5 = 40% by closed-stage count). G3 has P1/P2 closed (2/7 = 28.6% by package count); P3/P4/P5 are in progress, P6/P7 pending. After B3, bounded turns C, D, E, F remain, plus human decisions and conditional detector work.

Definitions: [ImpAbs](https://ontouml.readthedocs.io/en/latest/anti-patterns/ImpAbs/index.html), [RelComp](https://ontouml.readthedocs.io/en/latest/anti-patterns/RelComp/index.html), [RelOver](https://ontouml.readthedocs.io/en/latest/anti-patterns/RelOver/index.html), [RepRel](https://ontouml.readthedocs.io/en/latest/anti-patterns/RepRel/index.html).
