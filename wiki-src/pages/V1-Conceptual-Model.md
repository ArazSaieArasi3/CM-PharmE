# V1 Conceptual Model

> **Page scope:** V1  
> **Documentation maturity:** Stable  
> **Authoritative source:** V1 model artifacts and normalized catalogs on `main`  
> **Last synchronized:** 2026-09-23  
> **Last synchronized ref:** `5099888668d35f798e4759e3534e707ed906db24`  
> **Related issues/PRs:** V1 model normalization and semantic-engineering closure  
> **Evidence status:** Stable conceptual baseline with explicit review flags  
> **Future refresh:** No silent semantic changes; any future evolution belongs to governed later versions  
> **Wiki baseline:** WB-2026.09.1 Candidate

## Baseline

CM-PharmE v1.0.0 contains:
- 39 canonical concepts;
- 40 canonical semantic relations;
- 5 modeling domains;
- 5 stereotype families;
- 6 relation categories.

Concept stereotypes:
- 13 kind;
- 8 mode;
- 7 role;
- 6 relator;
- 5 perdurant.

Relation categories:
- 19 material;
- 8 mediation;
- 6 characterization;
- 4 componentOf;
- 2 association;
- 1 generalization.

## Modeling principles

V1 combines business-architecture-informed concern identification with UFO/OntoUML ontological classification.

Key principles include:
- distinguish rigid identity-bearing entities from contingent roles;
- reify socially/materially meaningful relational structures when a Relator is justified;
- model dependent qualities/capabilities/policies as Modes where appropriate;
- treat activities/processes as temporally unfolding Perdurants;
- prefer conservative relation semantics when evidence does not justify stronger commitments.

## Cross-domain integration

The model is intended as an ecosystem-level scaffold, so cross-domain relations are as important as domain-internal groupings. Organization, collaboration, operation, governance and digital concerns are therefore connected rather than modeled as five isolated diagrams.

## Historical and normalized artifacts

The original Draw.io/XML model is preserved as provenance. The repository later adds normalized concept/relation/domain catalogs and a formal semantic-engineering layer without silently rewriting the frozen historical release.

## Known semantic review flags

The V1 version record preserves several issues rather than hiding them, including:
- Enterprise Governance Relator stereotype conflict;
- duplicated mediation occurrence;
- inconsistent mediation direction for Strategic Partnership Agreement;
- generic/awkward relation wording retained from source;
- converter pollution in historical OWL export.

These flags are inputs to later semantic evolution, not grounds for retroactively changing V1.

## Evidence

- [V1 version record](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/versions/v1.0.0.md)
- [Concept catalog](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/catalog/concepts.yaml)
- [Relation catalog](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/catalog/relations.yaml)
- [Model image](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/releases/v1.0.0/model/CM-PharmE-1.0.png)
- [Draw.io source](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/releases/v1.0.0/model/CM-PharmE-1.0.drawio)

## Related pages

[[V1 Concepts]] · [[V1 Relations]] · [[V1 Domain Architecture]] · [[V1 Formal Ontology]]
