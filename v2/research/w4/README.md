# W4 — UFO/OntoUML Conceptualization

Status: **implementation complete; Gate D decision pending**.

W4 transforms the Gate-approved W3 evidence inventory into a first-class UFO/OntoUML conceptualization. W3 candidates were semantic needs, not predetermined classes; W4 therefore permits explicit split/merge/rename/reclassification where identity, rigidity, dependence, event/situation or relator analysis requires it.

## Methodological basis
The conceptualization follows UFO/OntoUML distinctions for identity, rigidity, relational dependence, roles, relators, modes/qualities, events/situations, material relations, mediation and part-whole relations. Primary specification references used for the W4 design review include:
- OntoUML specification: https://ontouml.readthedocs.io/en/latest/
- Kind: https://ontouml.readthedocs.io/en/latest/classes/sortals/kind/
- Role: https://ontouml.readthedocs.io/en/latest/classes/sortals/role/
- RoleMixin: https://ontouml.readthedocs.io/en/latest/classes/nonsortals/rolemixin/
- Relator: https://ontouml.readthedocs.io/en/latest/classes/sortals/relator/
- Mode and Quality: https://ontouml.readthedocs.io/en/latest/classes/aspects/
- Relationships/mediation/material/characterization: https://ontouml.readthedocs.io/en/latest/relationships/
- UFO overview: https://dev.nemo.inf.ufes.br/seon/UFO.html

Risk/resilience extension alignment is informed by the UFO-grounded COVER/ROSE lineage, including Oliveira et al., *An Ontology of Security from a Risk Treatment Perspective*, DOI 10.1007/978-3-031-17995-2_26. W4 does not import ROSE/COVER axioms; it defines an alignment boundary for later formalization.

## Outputs
1. `architecture.md` — Core/X-INFRA/Extension architecture.
2. `stereotype-decision-matrix.md` — W3→W4 UFO stereotype decisions.
3. `relator-material-patterns.md` — relator/material-relation patterns.
4. `events-situations-observations.md` — event/situation/observation analysis.
5. `geography-jurisdiction.md` — facility/geography/jurisdiction conceptualization.
6. `risk-resilience-extension.md` — modular risk/resilience design.
7. `business-architecture-view.md` — BA as optional analytical view.
8. `integrated-ontouml-model.md` — integrated conceptual model specification.
9. `integrated-ontouml-overview.puml` — reviewable diagram source.
10. `anti-pattern-review.md` — semantic/anti-pattern review and refactorings.
11. `w3-w4-transformation-ledger.md` — explicit split/merge/rename decisions.
12. `gate-d-conceptual-freeze.md` — Gate D proposal.
13. `W4-CLOSURE.md` — closure summary.
14. manuscript/evidence-ledger alignment notes.

## W4 conceptual inventory
The integrated specification contains **87 named conceptual types/pattern elements**:
- **32 Core**
- **25 cross-cutting infrastructure (X-INFRA)**
- **30 modular extension**

The increase from W3's 80 candidates is intentional: W4 split several overloaded discovery candidates (e.g., observation/activity vs result, classification scheme vs assignment, supply capacity vs its observation, risk treatment plan vs activity) and introduced a small number of semantic truth-makers required by UFO patterns. The two W3 deferred candidates remain outside the W4 freeze.

## Gate discipline
W4 does **not** create the final OWL ontology. Gate D freezes the conceptual commitments that W5 will formalize. OWL restrictions, SHACL, serialization, reasoning and formal validation remain W5/W7 work.
