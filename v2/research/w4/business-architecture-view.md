# W4 Business Architecture as an Optional Analytical View

## Decision
Business Architecture remains part of the CM-PharmE research lineage but no longer determines the identity or decomposition of the pharmaceutical ecosystem Core.

This preserves useful V1 work while preventing enterprise-centric constructs from constraining a broader ecosystem ontology.

## BA extension elements

### Business Architecture View — information object
An analytical description/view that maps ecosystem entities, activities and relationships to business-architecture concerns.

A BA View may organize:
- Organizations and ecosystem roles;
- Activities and processes;
- capabilities;
- governance/responsibility;
- partnerships;
- service offerings.

It does not create alternative identities for Core entities.

### Enterprise Capability — `<<Mode>>`
An organizational capability/disposition characterized by an Organization. This preserves the durable semantic part of V1 `Enterprise Capability` while keeping it in an optional BA extension.

A capability is not an Organization component and should not be confused with an Activity that realizes/exercises it.

### Strategic Partnership Agreement — `<<Relator>>`
A commitment-bearing relationship among Organizations. It may ground material partnership relations, but is not required for all ecosystem interactions.

### Service Offering Specification — information object
A specification/description of a service offering. It may refer to actors, activities, products or capabilities but remains an analytical/business description rather than Core pharmaceutical identity.

## V1 concepts repositioned
| V1 concept | W4 treatment |
|---|---|
| Pharmaceutical Enterprise | Replaced in Core by Organization + contextual roles. |
| Organizational Unit Structure | BA/organizational-design extension only. |
| Enterprise Capability | Retained as Mode in BA extension. |
| Strategic Resource Allocation | Not promoted to principal W4 model; future strategy/BA specialization. |
| Ecosystem Governance Entity | Replaced by Organization + governance/regulatory roles. |
| Strategic Partnership Agreement | Retained as extension Relator. |
| Pharmaceutical Business Process | Core evidence-grounded activities are modeled directly; BA process views can group them analytically. |
| Public–Private Partnership Structure | Deferred. |
| Enterprise Governance Relator | Not carried into Core; governance/oversight modeled with typed regulatory patterns. |
| Governance Policy Framework | Regulatory/BA extension only. |
| Service Offering Specification | Retained in BA/Service extension. |

## Mapping pattern
The BA View may state analytical mappings such as:
- `Organization` **hasCapability** `Enterprise Capability`;
- `Manufacturing Activity` **isMappedToProcessView** a BA process representation;
- `Regulatory Authorization` **isMappedToGovernanceConcern**;
- `Strategic Partnership Agreement` **supports** a collaboration/capability view;
- `Service Offering Specification` **references** Product/Activity/Role.

These are view semantics. The inverse dependency is prohibited: Core Product, Facility, Authorization or Activity must remain meaningful when the BA module is absent.

## Novelty accounting
V2 should not claim that Business Architecture itself is new. The V2 methodological advance is the **repositioning** of BA from a Core organizing principle to a modular analytical view over a data-grounded pharmaceutical ecosystem model.

This allows the article to cite V1/CM4DI lineage while making the scientific identity of V2 clearly distinct.

## W5 handoff
BA should be a separate importable module with no mandatory import from Core. The principal V2 OWL release may publish it as an optional extension; evaluation of the Core should not depend on BA extension coverage.
