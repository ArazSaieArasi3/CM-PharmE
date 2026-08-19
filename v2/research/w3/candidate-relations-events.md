# W3 Candidate Relations, Roles, Relators and Events

Status: pre-UFO/pre-OWL relationship inventory. The table records **semantic needs**, not final object-property names or cardinalities. W4 determines whether a relation is material, formal, mediation-based, part-whole, participation, characterization, derivation, or should be reified through a relator/event.

## A. Actor, organization, site and regulatory relations
| ID | Candidate relation / relationship entity | Source evidence | Domain → Range / participants | Preliminary treatment |
|---|---|---|---|---|
| V2R-001 | bears ecosystem role | P3/P4/P5/C2/V1 | Organization/Site/Person → Ecosystem Participant Role | role-bearing relation |
| V2R-002 | operates / is responsible for site | P2/P3/C2 | Organization → Site/Facility | material/ownership-operation relation; exact semantics may split |
| V2R-003 | site bears manufacturing role | P3/C2 | Site → Manufacturing Site Role | role-bearing |
| V2R-004 | site bears distribution/3PL role | P3/C2 | Site → Distribution Site Role / WDD/3PL role | role-bearing |
| V2R-005 | organization bears regulatory-authority role | P3/P5/C2/V1 | Organization → Regulatory Authority Role | role-bearing |
| V2R-006 | organization bears manufacturer/importer/labeler role | P3/P4/C2 | Organization → contextual pharmaceutical role | role-bearing; specializations retained |
| V2R-007 | authorization/license mediates authority and regulated party | P3/C2 | Regulatory Authorization ↔ Authority Role ↔ Organization/Site | relator candidate |
| V2R-008 | authorization permits activity/role | P3/C2 | Authorization → Manufacturing/Import/Distribution role/activity | normative relation |
| V2R-009 | authorization/license applies in jurisdiction | P3/C2 | Authorization → Regulatory Jurisdiction | contextual scope |
| V2R-010 | establishment registration identifies/registers site | P3 | Establishment Registration ↔ Site/Organization | relator/record distinction to resolve |
| V2R-011 | oversight relation connects authority and regulated entity/activity | P3/C2/V1 | Regulatory Oversight ↔ Authority Role ↔ Entity/Activity | relator/material relation candidate |
| V2R-012 | requirement applies to entity/activity/role | P3/P5/C2/V1 | Regulatory Requirement → Entity/Activity/Role | normative applicability |

## B. Product, substance, presentation and classification relations
| ID | Candidate relation | Source evidence | Domain → Range | Preliminary treatment |
|---|---|---|---|---|
| V2R-013 | product has active ingredient/substance | P4/P6/S1 | Medicinal Product/Presentation → Pharmaceutical Substance | material/composition/specification relation |
| V2R-014 | product/presentation has dosage form | P4/P5/P6 | Product/Presentation → Dosage Form | descriptive relation |
| V2R-015 | product/presentation has strength specification | P1/P2/P4/P5/P6 | Product/Presentation → Strength Specification | characterization |
| V2R-016 | product has package configuration | P1/P2/P4 | Product/Presentation → Package Configuration | composition/specification |
| V2R-017 | product classified under classification | P1/P2/P4/P5 | Product/Substance → Product Classification | classification-assignment candidate |
| V2R-018 | product has listed/marketed status | P4 | Product/Presentation → Product Listing/Marketing Status | contextual status |
| V2R-019 | product-responsible role is responsible for listing/label | P4 | Organization Role → Product/Label | material relation through responsibility context |
| V2R-020 | label describes product/presentation | P4 | Product Label → Product/Presentation | aboutness/specification |
| V2R-021 | essential classification applies to medicine in list/version/context | P6 | Essential Classification ↔ Product/Substance ↔ List/Jurisdiction/Version | relator/classification assignment |
| V2R-022 | critical classification applies to medicine in list/version/jurisdiction | P5 | Critical Classification ↔ Product/Substance ↔ List/Jurisdiction/Version | relator/classification assignment |
| V2R-023 | medicine serves as alternative to medicine in context | P5/P6 | Product/Presentation ↔ Alternative Product Role ↔ Product/Presentation | contextual material relation |

## C. Manufacturing, distribution, supply and resilience relations
| ID | Candidate relation / event participation | Evidence | Participants | Preliminary treatment |
|---|---|---|---|---|
| V2R-024 | organization/site participates in manufacturing activity | P3/C2 | Organization/Site ↔ Manufacturing Activity | participation |
| V2R-025 | manufacturing activity concerns/produces product/substance | P3/C2/P4 where explicit | Manufacturing Activity → Product/Substance | participation/result relation; evidence boundary required |
| V2R-026 | organization/site participates in distribution/logistics activity | P3/C2 | Organization/Site ↔ Distribution/Logistics Activity | participation |
| V2R-027 | distribution/logistics activity concerns product | P3/C1 where explicit | Activity → Product/Presentation | participation/topic relation |
| V2R-028 | supply dependency connects dependent and provider/source entity | P5/C1/W1 | Product/Actor/Site/Activity ↔ Supply Dependency ↔ Actor/Site/Product | relator/material relation candidate |
| V2R-029 | supply dependency has geographic exposure | P3/P5/P7/C1 | Supply Dependency → Geographic Feature/Region | derived contextual relation |
| V2R-030 | disruption event affects site/actor/activity/dependency | P5/C1/W1 | Disruption Event → Site/Organization/Activity/Dependency | event participation/impact relation |
| V2R-031 | disruption/shortage has downstream affected entity | P5/C1 | Event/Situation → Product/Site/Region/Actor | impact relation |
| V2R-032 | procurement activity involves buyer/provider/product | C1 | Procurement Activity ↔ Organization/Site/Product | multi-party event; extension only |
| V2R-033 | arrival/purchase event realizes procurement activity | C1 | Event → Procurement Activity/Product/Site | event relation |
| V2R-034 | inventory observation about product at site | C1 | Inventory Observation → Product + Site | observation aboutness |
| V2R-035 | stockout event affects product at site | C1 | Stockout Event → Product + Site | event participation/context |
| V2R-036 | lead-time observation concerns procurement/supply relation | C1 | Lead-Time Observation → Procurement/Supply relation | observation aboutness |

## D. Shortage, availability, demand and criticality relations
| ID | Candidate relation | Evidence | Domain → Range / participants | Preliminary treatment |
|---|---|---|---|---|
| V2R-037 | shortage case affects medicine/product/presentation | P5 | Shortage Case → Product/Substance/Presentation | material/context relation |
| V2R-038 | shortage case affects form | P5 | Shortage Case → Dosage Form | contextual relation |
| V2R-039 | shortage case affects strength | P5 | Shortage Case → Strength Specification | contextual relation |
| V2R-040 | shortage case has status | P5 | Shortage Case → Shortage Status | characterization/phase |
| V2R-041 | shortage case valid during interval | P5 | Shortage Case → Time Interval | temporal extent |
| V2R-042 | shortage case has alternative medicine | P5 | Shortage Case → Product/Alternative Role | contextual material relation |
| V2R-043 | shortage case reported/published by source | P5 | Shortage Case → Data Source/Record | provenance relation |
| V2R-044 | availability observation about medicine/context | P5/ESMP | Availability Observation → Product + scope | observation aboutness |
| V2R-045 | demand observation about medicine/context | P5/ESMP/C1/P1/P2 | Demand Observation → Product + scope | observation aboutness |
| V2R-046 | supply-capacity observation about actor/site/product | P5/ESMP/C1 | Supply Capacity Observation → Actor/Site/Product | observation aboutness |
| V2R-047 | observation has spatial/jurisdiction scope | P1/P2/P5 | Observation → Region/Jurisdiction | context relation |
| V2R-048 | observation valid for reporting period/time | P1/P2/P5/C1 | Observation → Reporting Period/Interval | temporal context |

## E. Geography and jurisdiction relations
| ID | Candidate relation | Evidence | Domain → Range | Preliminary treatment |
|---|---|---|---|---|
| V2R-049 | site located in geographic feature | P2/P3/C2/P7 | Site → Geographic Feature | spatial relation |
| V2R-050 | geographic feature located within administrative region | P7 | Geographic Feature → Administrative Region | part-whole/spatial containment candidate |
| V2R-051 | administrative region within country | P1/P2/P7 | Administrative Region → Country | part-whole/administrative containment |
| V2R-052 | geographic feature has geospatial position | P7 | Geographic Feature/Site → Geospatial Position | characterization |
| V2R-053 | entity has address | P3/C2 | Site/Organization → Address | characterization/information relation |
| V2R-054 | jurisdiction covers/applies to geographic/political scope | P3/P5/P6 | Regulatory Jurisdiction → Region/Country | social scope relation; not identity |
| V2R-055 | authority role exercises authority in jurisdiction | P3/P5/C2 | Regulatory Authority Role → Jurisdiction | role-context relation |

## F. Evidence, provenance and identifier relations
| ID | Candidate relation | Evidence | Domain → Range | Preliminary treatment |
|---|---|---|---|---|
| V2R-056 | data source publishes/maintains dataset | all source registries | Data Source → Dataset | provenance/publication |
| V2R-057 | dataset has release/version | P1/P2/P3/P4/P5/P7 | Dataset → Dataset Release | version relation |
| V2R-058 | release contains source record | P1–P5 | Dataset Release → Source Record | membership/composition |
| V2R-059 | record supports assertion | all ingested sources | Source Record → Assertion | evidence relation |
| V2R-060 | assertion about domain entity/relation | Demonstrator C | Assertion → Entity/Relation | aboutness |
| V2R-061 | observation has measure/value | P1/P2/C1 | Observation → Measure/Quantity Value | characterization |
| V2R-062 | evidence item supports model/mapping/assertion decision | W0–W3 research method | Evidence Item → Assertion/Mapping/Model Decision | evidence relation |
| V2R-063 | mapping assertion maps source representation to canonical representation | Demonstrator C | Mapping Assertion ↔ Source Entity/Field ↔ Canonical Entity/Concept | mapping relator candidate |
| V2R-064 | provenance activity used source artifact | Demonstrator C | Provenance Activity → Dataset/Record/Artifact | PROV-style usage candidate |
| V2R-065 | provenance activity generated artifact/assertion | Demonstrator C | Provenance Activity → Artifact/Assertion/Mapping | generation relation |
| V2R-066 | entity identified by identifier assignment | P1–P7 | Entity ↔ Identifier Assignment ↔ Identifier | relator candidate |
| V2R-067 | identifier governed by scheme | P1–P7/S1 | Identifier → Identifier Scheme | scheme relation |
| V2R-068 | identifier scheme issued/maintained by source/authority | P1–P7 | Identifier Scheme → Data Source/Authority | provenance/governance relation |
| V2R-069 | entity-match assertion links source records/entities | entity-resolution design | Match Assertion ↔ Entity/Record A + Entity/Record B | proposition/relator candidate |
| V2R-070 | match assertion supported by match evidence/confidence | entity-resolution design | Match Assertion → Evidence/Confidence | evidence/quality relation |

## G. Extension-specific relations
| ID | Candidate relation | Evidence | Scope |
|---|---|---|---|
| V2R-071 | reimbursement observation about product/facility/region/diagnosis | P1/P2/S2 | Market Access extension |
| V2R-072 | payer/funder responsible for reimbursement/access decision | P1/P2/S2 | Market Access extension |
| V2R-073 | risk assessment concerns vulnerability/asset/event context | W1 risk alignment/V1 | Risk & Resilience extension |
| V2R-074 | risk treatment addresses assessed risk/vulnerability | W1 risk alignment | Risk & Resilience extension |
| V2R-075 | adverse-event reporting activity concerns safety evidence/product | V1/S3 if activated | Safety extension |
| V2R-076 | post-market surveillance produces/uses safety evidence | V1/S3 if activated | Safety extension |
| V2R-077 | BA view maps domain activity/entity to capability/process/governance view | V1 | Business Architecture extension |
| V2R-078 | partnership agreement mediates participating organizations | V1/W1 | Partnerships/BA extension |
| V2R-079 | digital/information system supports activity/observation/analysis | V1 | Digital/Application extension |
| V2R-080 | clinical participant role participates in care activity/pathway | V1 only | Deferred Clinical extension; held-out trial schema not used |

## Event/activity candidates requiring explicit W4 analysis
- Manufacturing Activity
- Distribution/Logistics Activity
- Procurement Activity
- Medicine Shortage Case: **event vs situation vs socially recognized case** must be resolved.
- Disruption Event
- Stockout Event/Situation
- Observation / provenance activity
- Regulatory registration/authorization lifecycle events
- Adverse Event Reporting and Post-Market Surveillance activities

## Relation inventory conclusion
The principal V2 relation architecture must move away from generic V1 relationships such as “Ecosystem Relationship” or undifferentiated “Supply Chain Relationship.” W3 evidence supports **typed participation, authorization, location, product-composition, classification, shortage, observation, dependency, provenance, identifier and mapping relations**. Generic V1 relators remain lineage evidence but should be split/refined rather than carried forward as the primary semantics.
