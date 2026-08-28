# W4 — UFO/OntoUML Conceptualization

Status: **implementation complete; Gate D approved**.

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

Risk Management extension alignment is informed by the UFO-grounded COVER/ROSE lineage, including Oliveira et al., *An Ontology of Security from a Risk Treatment Perspective*, DOI 10.1007/978-3-031-17995-2_26. W4 does not import ROSE/COVER axioms; it defines an alignment boundary for later formalization.

## Outputs
1. `architecture.md` — Core/X-INFRA/Extension architecture.
2. `domain-taxonomy.md` — canonical 17-domain naming taxonomy and old→new migration map.
3. `stereotype-decision-matrix.md` — W3→W4 UFO stereotype decisions.
4. `relator-material-patterns.md` — relator/material-relation patterns.
5. `events-situations-observations.md` — event/situation/observation analysis.
6. `geography-jurisdiction.md` — facility/geography/jurisdiction conceptualization.
7. `risk-resilience-extension.md` — modular risk/resilience design evidence; canonical human-facing domain name is Risk Management.
8. `business-architecture-view.md` — Business Architecture as optional analytical view.
9. `integrated-ontouml-model.md` — integrated conceptual model specification organized by canonical domains.
10. `integrated-ontouml-overview.puml` — reviewable diagram source organized by canonical domains.
11. `anti-pattern-review.md` — semantic/anti-pattern review and refactorings.
12. `w3-w4-transformation-ledger.md` — explicit split/merge/rename decisions.
13. `gate-d-conceptual-freeze.md` — approved Gate D commitments.
14. `W4-CLOSURE.md` — closure summary.
15. manuscript/evidence-ledger alignment notes.

## Canonical domain naming
Domain titles use cohesive semantic noun phrases and do not concatenate concerns with `&` or `/`. The canonical taxonomy contains:
- Core: Ecosystem Organization, Facility Operations, Regulatory Governance, Pharmaceutical Product, Supply Operations, Ecosystem Observation.
- X-INFRA: Spatiotemporal Context, Evidence Traceability, Entity Identity.
- Extensions: Regulatory Policy, Supply Resilience, Market Access, Risk Management, Pharmacovigilance, Business Architecture, Digital Systems, Clinical Care.

This normalization changes human-facing architecture labels only. It does not change Gate-D semantics, formal ontology axioms, or the 87-element inventory.

## W4 conceptual inventory
The integrated specification contains **87 named conceptual types/pattern elements**:
- **32 Core**
- **25 cross-cutting infrastructure (X-INFRA)**
- **30 modular extension**

The increase from W3's 80 candidates is intentional: W4 split several overloaded discovery candidates, including observation/activity versus result, classification scheme versus assignment, supply capacity versus its observation, and risk treatment plan versus activity, and introduced a small number of semantic truth-makers required by UFO patterns. The two W3 deferred candidates remain outside the W4 freeze.

## Gate discipline
Gate D is approved and freezes the conceptual commitments that W5 formalized. Any later material change to identity/dependence structure or domain boundaries requires a recorded design-change review. Domain-label normalization under issue #154 is non-semantic and preserves the frozen conceptual baseline.
