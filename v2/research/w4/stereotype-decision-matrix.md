# W4 UFO/OntoUML Stereotype Decision Matrix

This matrix records the W4 interpretation of every W3 candidate. Stereotypes are conceptual commitments for Gate D; W5 will encode them formally.

Legend: **K** Kind, **SK** Subkind, **R** Role, **RM** RoleMixin, **REL** Relator, **M** Mode, **Q** Quality, **E** Event, **SIT** Situation, **DT** Datatype/value type, **INF** information-object Kind, **DEFER** outside Gate D freeze.

## A. W3 Core candidates
| W3 ID | W4 target | Stereotype | W4 decision |
|---|---|---|---|
| V2C-001 | Organization | K | Identity provider for institutional/social organizations. |
| V2C-002 | Ecosystem Participant | RM | Contextual participation can be borne by Organizations and Facilities with different identities. |
| V2C-003 | Regulatory Authority Role | R | Organization-dependent, anti-rigid regulatory role. |
| V2C-004 | Manufacturer Role | R | Organization role; relationally dependent on regulated/manufacturing context. |
| V2C-005 | Importer Role | R | Organization role. |
| V2C-006 | Product-Responsible / Labeler Role | R | Organization role bound to product-listing/label responsibility. |
| V2C-007 | Wholesale Distributor Role | R | Organization role. |
| V2C-008 | Third-Party Logistics Provider Role | R | Organization role. |
| V2C-010 | Facility | K | Physical operational functional complex with identity distinct from Organization and Location. |
| V2C-011 | Manufacturing Site Role | R | Facility role. |
| V2C-012 | Distribution Site Role | R | Facility role. |
| V2C-013 | Establishment Registration | REL | Relational truth-maker connecting authority, registered organization/facility and jurisdiction/validity. |
| V2C-014 | Regulatory Authorization | REL | Authorization relation; license/source document remains evidence/record, not the relator itself. |
| V2C-017 | Regulatory Jurisdiction | K | Social/legal scope entity, not geographic geometry. |
| V2C-025 | Medicinal Product | K | Regulatory/product identity layer. |
| V2C-026 | Pharmaceutical Substance | K | Substance identity layer, independent from product/presentation identity. |
| V2C-027 | Medicinal Product Presentation | K | Independently identifiable marketed/presented product configuration. |
| V2C-028 | Dosage Form Specification | K | Stable pharmaceutical-form specification/reference entity. |
| V2C-029 | Strength | Q | Quantitative property characterized by a presentation; value/unit represented separately. |
| V2C-030 | Package Configuration | K | Identifiable packaging/configuration specification. |
| V2C-031 | Product Classification Scheme + Classification Entry + Product Classification Assignment | K + K + REL | Split overloaded discovery candidate into scheme, entry and contextual assignment. |
| V2C-032 | Market Listing + Listing Status Value | REL + DT | Listing/marketing is jurisdiction/source/time relational context; status is not an intrinsic Product phase. |
| V2C-036 | Manufacturing Activity | E | Perdurant/event with Organization/Facility/Product participation. |
| V2C-037 | Distribution / Logistics Activity | E | Perdurant/event. |
| V2C-039 | Medicine Shortage Situation | SIT | Shortage is modeled primarily as a temporally bounded situation; source cases are records/assertions about it. |
| V2C-040 | Shortage Status Value | DT | Source-defined status value; not forced into a Phase partition. |
| V2C-041 | Availability Observation Result | SK of Observation Result | Information result about availability; not the observing event itself. |
| V2C-042 | Demand Observation Result | SK of Observation Result | Evidence result about demand/consumption. |
| V2C-043 | Supply Capacity + Supply Capacity Observation Result | M + SK | Split actual capacity/disposition from evidence about that capacity. |

## B. W3 X-INFRA candidates
| W3 ID | W4 target | Stereotype | W4 decision |
|---|---|---|---|
| V2C-018 | Geographic Feature | K | Identifiable geographic/place reference entity. |
| V2C-019 | Administrative Region | SK | Rigid specialization of geographic reference entity. |
| V2C-020 | Country | SK | Rigid specialization; not identical to Regulatory Jurisdiction. |
| V2C-021 | Geospatial Position | DT | Structured coordinate/geometry value. |
| V2C-022 | Address | DT | Structured address value used for site/entity resolution. |
| V2C-023 | Time Interval | DT | Temporal extent value. |
| V2C-024 | Reporting Period | DT | Specialized time value with source/reporting semantics. |
| V2C-049 | Data Source Resource | INF | Identifiable information resource/system/publication endpoint; maintainer may be linked separately. |
| V2C-050 | Dataset | INF | Information object/collection. |
| V2C-051 | Dataset Release | INF | Immutable/reproducible release/snapshot identity distinct from Dataset. |
| V2C-052 | Source Record | INF | Information object/record contained in a release. |
| V2C-053 | Assertion | INF | Proposition/information-content entity. |
| V2C-054 | Observation Activity + Observation Result | E + INF | Split observing/measurement event from its information result. |
| V2C-055 | Measure Value | DT | Numeric/coded/unit-bearing value. |
| V2C-056 | Evidence Item | RM | Contextual role borne by records/datasets/publications when supporting an assertion/decision. |
| V2C-057 | Mapping Assertion | SK of Assertion | Proposition about mapping/correspondence. |
| V2C-058 | Provenance Activity | E | Ingestion/transformation/normalization/mapping event. |
| V2C-059 | Data Quality Finding | SK of Assertion | Evidence-bearing information finding, not an intrinsic Mode of a dataset by default. |
| V2C-060 | Identifier Value | DT | Symbol/string value; never a global identity principle by itself. |
| V2C-061 | Identifier Scheme | INF | Scheme/description defining scope, issuer and syntax. |
| V2C-062 | Identifier Assignment | REL | Contextual assignment connecting entity, value, scheme, issuer/source and validity. |
| V2C-063 | Entity Match Assertion | SK of Assertion | Proposition that source/canonical entities correspond. |
| V2C-064 | Match Confidence + supporting Evidence Item | Q + RM | Split confidence quality from evidence support. |

## C. W3 Extension candidates
| W3 ID | W4 target | Stereotype | Module / decision |
|---|---|---|---|
| V2C-009 | Payer / Funding Organization Role | R | Market Access. |
| V2C-015 | Regulatory Requirement | INF | Regulatory normative-description/social-object pattern. |
| V2C-016 | Regulatory Oversight | REL | Regulatory relation between authority and governed entity/activity. |
| V2C-033 | Essential Medicine Classification | SK of Contextual Medicine Classification Assignment (REL) | Policy/Access; context/list/jurisdiction dependent. |
| V2C-034 | Critical Medicine Classification | SK of Contextual Medicine Classification Assignment (REL) | Resilience/Policy. |
| V2C-035 | Alternative Medicinal Product Role + Alternative Medicine Assignment | R + REL | Resilience/Policy; alternative status is contextual and anti-rigid. |
| V2C-038 | Supply Dependency | REL | Resilience; truth-maker connecting dependent and supply-source participants. |
| V2C-044 | Disruption Event | E | Resilience. |
| V2C-045 | Inventory Observation Result | SK of Observation Result | Supply/Resilience. |
| V2C-046 | Procurement Activity | E | Supply. |
| V2C-047 | Lead-Time Observation Result | SK of Observation Result | Supply/Resilience. |
| V2C-048 | Stockout Situation | SIT | Primary representation is state/situation; transition events may be derived/added later. |
| V2C-065 | Reimbursement / Utilisation Observation Result | SK of Observation Result | Market Access. |
| V2C-066 | Diagnosis Classification Reference | INF | Market Access terminology/reference. |
| V2C-067 | Risk Assessment Activity | E | Risk/Resilience. |
| V2C-068 | Vulnerability | M | Risk/Resilience mode/disposition characterized by an asset/bearer; detailed COVER/ROSE alignment deferred to formal adapter. |
| V2C-069 | Risk Treatment Plan + Risk Treatment Activity | INF + E | Split planned normative/intended treatment from its execution. |
| V2C-070 | Pharmacovigilance Requirement | INF | Safety normative description. |
| V2C-071 | Adverse Event Reporting Activity | E | Safety. |
| V2C-072 | Post-Market Surveillance Activity | E | Safety. |
| V2C-073 | Business Architecture View | INF | BA analytical description/view. |
| V2C-074 | Enterprise Capability | M | BA extension; intrinsic organizational capability characterized by Organization. |
| V2C-075 | Strategic Partnership Agreement | REL | Partnerships/BA commitment-bearing relation. |
| V2C-076 | Digital / Information System Component | K | Digital/Application artifact identity. |
| V2C-077 | Clinical Care Participant | RM | Clinical extension; multiple possible bearer identity principles. |
| V2C-079 | Service Offering Specification | INF | BA/Service description. |

## D. Deferred W3 candidates
| W3 ID | Decision |
|---|---|
| V2C-078 Clinical Care Pathway / Activity Pattern | **DEFER** from Gate D; revisit only when Clinical extension is activated with non-held-out evidence. |
| V2C-080 Public–Private Partnership Arrangement | **DEFER**; partnership semantics can initially use Strategic Partnership Agreement without a dedicated PPP structure. |

## New semantic helpers introduced by W4
These are not arbitrary scope expansion; they are required to resolve overloaded W3 candidates and satisfy UFO patterns:
- Facility Operation — REL
- Product Classification Scheme — K/INF pattern
- Classification Entry — K/INF pattern
- Contextual Medicine Classification Assignment — REL
- Alternative Medicine Assignment — REL
- Evidence Support — REL
- Observation Result — INF
- Asset-at-Risk — RM (Risk extension adapter)

## Review conclusion
No W3 Role candidate is retained as a rigid Kind. No operational identifier is used as an identity provider. No source-defined status is forced into a Phase unless a disjoint/complete intrinsic partition can later be demonstrated. These decisions are deliberate controls against common OntoUML rigidity/dependence errors.
