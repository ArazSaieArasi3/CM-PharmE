# G3-2d — domain semantics and derived operation audit

Date: 2026-10-08 (Asia/Tehran). Source PR head: `accb79534f43c940b2214ef74557b4e9de7e0ada`.

## Outcome

- Detailed design review of the 20 prior domain-semantics relations, plus the existing derived `operates`; 39/42 relations now have a detailed first design review across G3-2b/c/d. The three G3-2a mediation changes are implemented but still need full semantic disposition. This is **review coverage**, not final semantic approval.
- One evidence-backed native change: `hasStrength` became bearer→Quality `characterization`; bearer end `1`, Quality end `1..*`. W4 names Strength as the Quality of Product Presentation. The G3-2a three mediation changes remain. No other relation was forcibly stereotyped, especially no mereology for source or geographic containment and no reversed Mode→bearer Characterization.
- `operates`: six existing FacilityOperation relational fixtures were evaluated by a deterministic rule: 1 positive and 5 negative cases matched the expected validity/rule. Derivation pairs are produced only after the complete, typed, same-relator operation exists. The current OWL `derivedFromRelator` is an annotation, not an executable derivation rule.
- Native overlay has 520 elements/81 binary relations. The checks are structural and synthetic, **not** an official OntoUML antipattern run, ontology reasoner test, or SHACL run on this overlay. Frozen 2.0 and G3d OWL/SHACL remain unchanged.

## Files

- `domain-decisions.json`: 20 bounded reviews with ends, truthmaker, multiplicity, temporal scope, negative example, recommendation and pending author disposition.
- `operates-derivation-audit.json`: rule, role identity caveat, six fixture evaluations.
- `ontouml.json`: native-only overlay with the one new Characterization.
- `static-checks.json`: observed native differences, endpoint resolution and fixture checks.
- `consolidated-relation-register.json`: cumulative 39/42 detailed reviews; three mediation-only records remain, still pending full scientific disposition and formal integration.

## Next exact step: G3-2e

Complete the three mediation-only records, then resolve the 42 decisions as a coherent semantic package, with author adjudication for uncertain truthmakers and cardinalities; implement approved native/OWL/SHACL changes in a separate candidate; rerun official OntoUML schema/anti-pattern, OWL reasoners, SHACL and negative/positive cases. Specifically align the `hasStrength` existential/bearer uniqueness claim and `operates` temporal derivation before any promotion. Then G3-3 official global validation, G4 source/wiki/pages/manuscript reconciliation, G5 human review and comprehensive diagram.

Sources: [W4 integrated model](https://github.com/ArazSaieArasi3/CM-PharmE/blob/accb79534f43c940b2214ef74557b4e9de7e0ada/v2/research/w4/integrated-ontouml-model.md), [W4 relator pattern](https://github.com/ArazSaieArasi3/CM-PharmE/blob/accb79534f43c940b2214ef74557b4e9de7e0ada/v2/research/w4/relator-material-patterns.md), [OntoUML Characterization](https://ontouml.readthedocs.io/en/latest/relationships/characterization/), [Derivation](https://ontouml.readthedocs.io/en/latest/relationships/derivation/), [Mediation](https://ontouml.readthedocs.io/en/latest/relationships/mediation/).
