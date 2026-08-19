# Gate D — Conceptual Model Freeze

## Status
**APPROVED on 2026-08-19.**

The W4 UFO/OntoUML conceptual baseline is approved as the semantic baseline for W5 formal ontology engineering.

## Frozen commitments
1. Organization, Facility/Site, Geographic Feature and Regulatory Jurisdiction remain distinct identity layers.
2. Ecosystem Participant is a RoleMixin; concrete pharmaceutical actor/site concepts are anti-rigid contextual Roles.
3. Establishment Registration and Regulatory Authorization use explicit Relator patterns; source records and identifiers are evidence, not the authorization itself.
4. Medicinal Product, Pharmaceutical Substance and Product Presentation remain distinct; Strength is modeled separately as a quality/specification pattern.
5. Product classification uses Scheme + Entry + Assignment; Essential/Critical medicine status is contextual rather than a rigid product kind.
6. Medicine Shortage is primarily a Situation; shortage records/assertions remain distinct provenance-layer entities.
7. Observation Activity and Observation Result remain distinct; Supply Capacity is a Mode/disposition separate from evidence about capacity.
8. Identifier Value is not an identity principle; Identifier Assignment is contextual.
9. Evidence, provenance, mapping and entity-match semantics remain first-class cross-cutting infrastructure.
10. Risk/Resilience and Business Architecture remain modular extensions rather than Core decomposition principles.
11. H1–H3 remain protected held-out evidence before W7.
12. No complete global supplier→buyer→shipment claim is permitted from the current evidence base.

## W4 inventory at freeze
- 32 Core named conceptual types/pattern elements
- 25 X-INFRA named conceptual types/pattern elements
- 30 Extension named conceptual types/pattern elements
- 87 total W4 named conceptual types/pattern elements
- 2 W3 deferred concepts remain outside the freeze

## W5 authorization
W5 may assign stable V2 IRIs, formal module imports, OWL classes/properties/axioms, OntoUML annotations, Relator/Mediation patterns, SHACL constraints, synchronized serializations and reproducible validation assets. Any material reversal of the frozen identity/dependence decisions requires a documented design-change review.

**Decision: Gate D APPROVED; W5 authorized.**
