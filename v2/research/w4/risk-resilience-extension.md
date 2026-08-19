# W4 Pharmaceutical Ecosystem Risk & Resilience Extension

## Design goal
Provide a pharmaceutical-specific adapter for risk/resilience reasoning without duplicating a generic risk ontology in the CM-PharmE Core.

## Reference-ontology strategy
The extension is designed for later alignment/reuse with UFO-grounded risk ontologies such as COVER and ROSE. W4 records conceptual compatibility; it does not yet import or copy their formal axioms.

Reference:
- Oliveira, I.; Sales, T. P.; Baratella, R.; Fumagalli, M.; Guizzardi, G. *An Ontology of Security from a Risk Treatment Perspective*. ER 2022. DOI: 10.1007/978-3-031-17995-2_26.

## Extension pattern

### Asset-at-Risk — `<<RoleMixin>>`
A Core entity may play an Asset-at-Risk role in a risk context. The role may be borne by entities with different identity principles, e.g. Organization, Facility, Product, Supply Dependency, Activity or information asset. Therefore a RoleMixin is more adequate than a single Role tied to one Kind.

This adapter should not make every Core entity a risk asset by definition.

### Vulnerability — `<<Mode>>`
A Vulnerability is modeled as a dependent mode/disposition of an asset/bearer, representing susceptibility under a relevant threat/disruption context.

W4 boundary: the exact COVER/ROSE specialization/alignment and whether threat-specific vulnerability requires a relational pattern will be finalized during formal ontology alignment. The CM-PharmE extension must not independently redefine generic risk theory.

### Disruption Event — `<<Event>>`
A temporally bounded occurrence that can affect an Asset-at-Risk, Facility, Activity, Supply Dependency, Organization or Product-availability context.

### Supply Dependency — `<<Relator>>`
A domain-specific Core-adjacent resilience relation connecting a dependent entity with a supply source/provider. This is one of the main pharmaceutical specializations contributed by CM-PharmE rather than a generic risk construct.

### Risk Assessment Activity — `<<Event>>`
An assessment process that evaluates evidence about vulnerabilities, disruptions, dependencies, consequences or other risk-relevant conditions.

Its outputs should be represented as Assertions/Assessment Results in X-INFRA, rather than confusing the activity with the result.

### Risk Treatment Plan — information object
A plan/description specifying intended mitigation/treatment actions.

### Risk Treatment Activity — `<<Event>>`
The execution of a treatment/mitigation action. A plan may exist without being executed; therefore plan and activity are separate.

## Pharmaceutical resilience specializations
The following extension elements connect generic risk/resilience semantics to actual pharmaceutical evidence:
- Critical Medicine Classification
- Alternative Medicine Assignment
- Supply Dependency
- Inventory Observation Result
- Lead-Time Observation Result
- Stockout Situation
- Procurement Activity
- Disruption Event
- Medicine Shortage Situation (Core)
- Availability / Demand / Supply-Capacity Observation Results (Core)

## Example reasoning pattern
A Product Presentation can be assigned a `Critical Medicine Classification` in a Jurisdiction. A Facility or Organization participates in a Supply Dependency relevant to that Product. A Disruption Event affects a Facility or Dependency. Observation Results provide evidence about availability, inventory or lead time. A Risk Assessment Activity uses these evidence items to assert a vulnerability/risk finding. A Treatment Plan may propose alternative supply or mitigation actions.

The ontology must distinguish these statements from a quantitative risk score. Risk scores/probabilities require explicit analytical models and empirical evidence; W4 does not claim them.

## Separation from shortage semantics
`Medicine Shortage Situation` is not itself a generic Risk. A shortage may be:
- an observed adverse situation;
- a consequence of a disruption;
- a trigger/input for risk assessment;
- evidence of a vulnerability;
- an outcome to be mitigated.

Conflating shortage and risk would prevent reuse across regulatory monitoring and resilience analysis.

## Data/evidence boundary
Detailed supply dependency/procurement/lead-time semantics rely substantially on conditional C1 evidence and regulatory vulnerability/shortage sources. Therefore:
- the conceptual pattern is admitted;
- empirical instance claims must remain source-bounded;
- CM-PharmE must not claim global network completeness.

## W5/W7 handoff
W5 should keep Risk/Resilience as a separate ontology module/import. W7 should evaluate this extension separately from Core coverage so that limited supply-dependency data do not weaken claims about the independently supported Core.
