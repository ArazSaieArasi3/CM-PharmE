# Gate D — Conceptual Model Freeze

## Status
**APPROVED on 2026-08-19.**

The W4 UFO/OntoUML conceptual baseline is approved as the semantic baseline for W5 formal ontology engineering.

## Frozen commitments
1. **Core identity providers**: Organization, Facility, Regulatory Jurisdiction, Medicinal Product, Pharmaceutical Substance, Product Presentation and selected information/geographic entities remain semantically distinct.
2. **Role pattern**: ecosystem roles are anti-rigid; Organization and Facility roles inherit their bearer identities; `Ecosystem Participant` is a RoleMixin.
3. **Regulatory relations**: Registration and Authorization are Relators; source records/documents/identifiers are evidence about those relations, not identical to them.
4. **Product structure**: Product, Substance and Presentation are distinct; Strength is a Quality; classification is Scheme/Entry/Assignment; listing is contextual.
5. **Shortage semantics**: Medicine Shortage is primarily a Situation; source shortage records/assertions remain provenance-layer information objects.
6. **Observation semantics**: Observation Activity is an Event; Observation Result is an information object. Domain phenomenon and evidence result are not conflated.
7. **Capacity semantics**: Supply Capacity is a Mode/disposition; its measurements are Observation Results.
8. **Geography/jurisdiction**: physical Facility, geographic reference entities/values and Regulatory Jurisdiction remain separate.
9. **Identifier semantics**: Identifier Value is not identity; Identifier Assignment is a contextual Relator governed by a Scheme/source.
10. **Evidence/provenance**: Dataset→Release→Record→Assertion/Mapping/Provenance structure is first-class X-INFRA.
11. **Risk**: Risk & Resilience remains a modular extension aligned toward COVER/ROSE; generic risk theory is not duplicated in Core.
12. **Business Architecture**: BA is an optional analytical extension/view, not Core decomposition.
13. **Held-out integrity**: H1–H3 remain unavailable for Core redesign before W7 generalizability evaluation.
14. **Empirical boundary**: no complete global supplier→buyer→shipment claim; finance/counterparty remains outside Core.

## W4 inventory at freeze
- **32 Core named conceptual types/pattern elements**
- **25 X-INFRA named conceptual types/pattern elements**
- **30 Extension named conceptual types/pattern elements**
- **87 total W4 named conceptual types/pattern elements**
- **2 W3 deferred concepts remain outside the freeze**

Counts are conceptual-model counts, not final OWL class counts. W5 may use OWL annotations, datatypes, properties, reification patterns and SHACL in ways that alter raw OWL entity counts while preserving these semantic commitments.

## Anti-pattern result
Manual/static semantic review: **PASS**.

No critical/high unresolved identity, rigidity, role/relator, event/situation, observation/result, geography/jurisdiction or extension-leakage defect was identified. Residual issues are bounded formalization/source-mapping/alignment questions recorded in `anti-pattern-review.md`.

## W5 authorization
W5 is authorized to:
- assign stable V2 IRIs and formal module imports;
- encode classes/properties/axioms in OWL;
- preserve OntoUML stereotypes as explicit annotations/metadata where OWL DL does not encode them natively;
- encode Relator/Mediation/Material patterns;
- add SHACL constraints and formal validation assets;
- produce synchronized Turtle/RDF/XML/JSON-LD and other distributions from one canonical source;
- prepare formal ontology gate tests before W6 data infrastructure.

## Gate protection
Any W5 change that would collapse a frozen identity distinction or move a modular extension into Core requires an explicit design-change record and, if material, a Gate D revisit.

**Decision: Gate D APPROVED; W5 authorized.**
