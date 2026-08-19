# W3 Normalized Candidate Concept Inventory

Status: **pre-UFO inventory**. Names and candidate interpretations are intentionally provisional until W4. Admission status means “worth conceptualizing,” not “final OWL class.”

Legend:
- **CORE** — candidate for stable pharmaceutical-ecosystem Core.
- **X-INFRA** — cross-cutting semantic/data infrastructure candidate.
- **EXT** — modular extension candidate.
- **DEFER** — retained as future/application concept, not principal V2 ontology commitment.

## A. Organizations, roles, facilities and regulation
| ID | Normalized candidate | Working meaning | Evidence | W4 hypothesis | Status | V1 lineage |
|---|---|---|---|---|---|---|
| V2C-001 | Organization | Institutional/legal/social entity participating in ecosystem activities. | P3, C2, P2, V1 | Kind/Category family | CORE | Refines C0001/C0013/C0020/C0023 into a common organizational bearer. |
| V2C-002 | Ecosystem Participant Role | Contextual role borne by an entity participating in a pharmaceutical ecosystem relation/activity. | P3–P6, V1 | Role | CORE | Refines C0008 and part of C0003. |
| V2C-003 | Regulatory Authority Role | Role borne by an organization when exercising pharmaceutical regulatory authority in a jurisdiction. | P3, P5, C2, V1 | Role | CORE | Retains/refines C0024; replaces entity-specific treatment of C0023. |
| V2C-004 | Manufacturer Role | Role borne by an organization/site when authorized/acting to manufacture/process pharmaceutical products/substances. | P3, C2 | Role | CORE | New explicit specialization; partly implicit in V1 actor/supply semantics. |
| V2C-005 | Importer Role | Contextual pharmaceutical import role under a jurisdiction/authorization. | P3, C2 | Role | CORE | New. |
| V2C-006 | Product-Responsible / Labeler Role | Organization role responsible for listing/labeling/market responsibility in a source/jurisdiction. | P4, C2 | Role | CORE | New; jurisdiction-specific specializations such as labeler/MAH deferred to W4 modules. |
| V2C-007 | Wholesale Distributor Role | Facility/organization role for wholesale distribution. | P3, C2 | Role | CORE | New explicit ecosystem role. |
| V2C-008 | Third-Party Logistics Provider Role | Contextual role for 3PL pharmaceutical logistics. | P3 | Role | CORE | New. |
| V2C-009 | Payer / Funding Organization Role | Role borne by an organization that reimburses/funds medicines or access. | P1, P2, S2 | Role | EXT — Market Access | Refines broader stakeholder ideas; new explicit role. |
| V2C-010 | Site / Facility | Physical operational site distinct from the organization that owns/operates it. | P2, P3, C2 | Kind | CORE | New explicit distinction; major V2 improvement. |
| V2C-011 | Manufacturing Site Role | Role borne by a facility when used/authorized for manufacturing/processing activities. | P3, C2 | Role | CORE | New. |
| V2C-012 | Distribution Site Role | Role borne by a facility in wholesale/distribution/3PL activity. | P3, C2 | Role | CORE | New. |
| V2C-013 | Establishment Registration | Regulatory relationship/record establishing source-specific registration of an establishment. | P3 | Relator / normative record split candidate | CORE | New; W4 must distinguish real normative relation from registration record. |
| V2C-014 | Regulatory Authorization / License | Permission/authorization relating authority, organization/site, activity/role and jurisdiction. | P3, C2 | Relator | CORE | Refines C0004 and governance relations into explicit authorization semantics. |
| V2C-015 | Regulatory Requirement | Normative requirement applicable to an entity/activity/context. | P3, P5, C2, V1 | Normative mode / social object candidate | EXT — Regulatory | Refines C0027 and C0036 family. |
| V2C-016 | Regulatory Oversight Relationship | Relationship through which an authority supervises/constrains a regulated actor/activity. | P3, C2, V1 | Relator/material relation | EXT — Regulatory | Refines C0004. |

## B. Geography, jurisdiction and time
| ID | Normalized candidate | Working meaning | Evidence | W4 hypothesis | Status | V1 lineage |
|---|---|---|---|---|---|---|
| V2C-017 | Regulatory Jurisdiction | Legal/regulatory scope within which rules, roles, authorizations or classifications apply. | P3, P5, P6, C2 | Social object / context candidate | CORE | New explicit cross-cutting concept. |
| V2C-018 | Geographic Feature | Identifiable geographic place/feature used for spatial reference. | P7 + native source locations | Kind | X-INFRA | New. |
| V2C-019 | Administrative Region | Geographic/administrative area used for aggregation/reporting. | P1, P2, P7 | Subkind/RoleMixin candidate | X-INFRA | New. |
| V2C-020 | Country | Country-level geographic/political reference used in source/jurisdiction mapping. | P3, P5, P7 | Subkind/category candidate | X-INFRA | New. |
| V2C-021 | Geospatial Position | Coordinate/geometry representation associated with a place/site. | P7 | Quality/measurement candidate | X-INFRA | New. |
| V2C-022 | Address | Structured location description for organization/site matching. | P3, C2 | Information object / complex quality candidate | X-INFRA | New. |
| V2C-023 | Time Interval | Bounded temporal extent for validity, shortage, observation, registration or reporting. | P1, P2, P3, P5 | Temporal region | X-INFRA | New explicit semantics. |
| V2C-024 | Reporting Period | Source-defined period over which an aggregate observation/report applies. | P1, P2, P5 | Temporal role/context | X-INFRA | New. |

## C. Medicinal products, substances, presentations and classifications
| ID | Normalized candidate | Working meaning | Evidence | W4 hypothesis | Status | V1 lineage |
|---|---|---|---|---|---|---|
| V2C-025 | Medicinal Product | Pharmaceutical product entity/specification represented across product/regulatory/access sources. | P1, P2, P4, P5, P6 | Kind/category; artifact-vs-specification analysis required | CORE | Major new domain-centric concept absent explicitly in V1. |
| V2C-026 | Pharmaceutical Substance / Active Ingredient | Substance identified as active/medicinal ingredient. | P1/P2 ATC/INN, P4, P5, P6, S1 | Kind | CORE | New explicit substance layer. |
| V2C-027 | Medicinal Product Presentation | Marketed/identified presentation combining product/form/strength/package context. | P1, P2, P4, P5 | Kind / description-artifact split candidate | CORE | New. |
| V2C-028 | Dosage Form | Pharmaceutical form in which a product/presentation is supplied/administered. | P4, P5, P6 | Kind/Quality structure candidate | CORE | New. |
| V2C-029 | Strength / Concentration Specification | Quantitative strength/concentration associated with ingredient/product presentation. | P1, P2, P4, P5, P6 | Quality + quantity/value pattern | CORE | New. |
| V2C-030 | Package Configuration | Pack/package structure, size and contained quantity for a product presentation. | P1, P2, P4 | Complex artifact/description candidate | CORE | New. |
| V2C-031 | Product Classification | Classification assignment/scheme such as ATC/therapeutic categorization. | P1, P2, P4, P5 | Classification relator/assignment candidate | CORE | New. |
| V2C-032 | Product Listing / Marketing Status | Contextual status that a product/presentation is listed/marketed under a source/jurisdiction/time. | P4 | Role/phase/status candidate | CORE | New; prevents NDC listing from becoming universal identity. |
| V2C-033 | Essential Medicine Classification | Contextual assignment of a medicine to an essential-medicine list/version/context. | P6 | Relator/classification status | EXT — Policy/Access | New; deliberately not intrinsic Kind. |
| V2C-034 | Critical Medicine Classification | Contextual assignment of medicine to a critical-medicine list/version/jurisdiction. | P5 | Relator/classification status | EXT — Resilience/Policy | New; deliberately jurisdiction/version sensitive. |
| V2C-035 | Alternative Medicinal Product Role | Contextual role of a medicine/presentation as an alternative to another in shortage/policy context. | P5, P6 | Role + material relation | EXT — Resilience/Policy | New. |

## D. Activities, supply and resilience situations
| ID | Normalized candidate | Working meaning | Evidence | W4 hypothesis | Status | V1 lineage |
|---|---|---|---|---|---|---|
| V2C-036 | Manufacturing Activity | Activity/event in which pharmaceutical product/substance is manufactured/processed at a site by an actor. | P3, C2 | Perdurant/Event | CORE | Refines broad C0015 business process. |
| V2C-037 | Distribution / Logistics Activity | Activity of distributing/handling/storing/moving pharmaceutical goods in a regulated logistics role. | P3, C2 | Perdurant/Event | CORE | Refines part of C0015/C0032. |
| V2C-038 | Supply Dependency | Context-dependent dependency between a pharmaceutical need/product/activity and an actor/site/source/alternative. | P5, C1, W1 demonstrator B | Relator/material relation candidate | EXT — Resilience | Refines/splits C0032 generic Supply Chain Relationship. |
| V2C-039 | Medicine Shortage Case | Time/source/jurisdiction-bounded case/situation in which supply does not meet relevant availability need/status. | P5 | Situation/Event candidate | CORE | New explicit shortage semantics. |
| V2C-040 | Shortage Status | Status of a shortage case (e.g., current/resolved/source-defined). | P5 | Phase/quality/status | CORE | New. |
| V2C-041 | Availability Observation | Evidence-bearing observation about product availability for a scope/time/place. | P5/ESMP, P1/P2 access context | Observation/event + result split candidate | CORE | Refines V1 signal ideas. |
| V2C-042 | Demand Observation | Evidence-bearing observation of demand/consumption for product/context/time. | P5/ESMP, C1, P1/P2 aggregate use | Observation | CORE | Refines C0010 Ecosystem Demand Signal from Mode to evidence-bearing observation. |
| V2C-043 | Supply Capacity Observation | Observation/assessment of supply/capacity for actor/site/product/context/time. | P5/ESMP, C1 | Observation/quality-assessment split | CORE | Refines C0011 Ecosystem Supply Capacity. |
| V2C-044 | Disruption Event | Event that impairs manufacturing, supply, logistics or availability. | W1 resilience evidence, P5, C1 | Event | EXT — Resilience | New. |
| V2C-045 | Inventory Observation | Observation/state of product inventory at site/time. | C1 | Observation/state | EXT — Supply/Resilience | New. |
| V2C-046 | Procurement Activity | Activity of acquiring pharmaceutical items under a procurement channel/relationship. | C1 | Perdurant/Event | EXT — Supply | New. |
| V2C-047 | Lead-Time Observation | Observation of elapsed procurement/supply lead time. | C1 | Observation + duration value | EXT — Supply/Resilience | New. |
| V2C-048 | Stockout Event / Situation | Time-bounded occurrence/state of unavailable stock for an item/site. | C1 | Event/Situation | EXT — Supply/Resilience | New. |

## E. Evidence, provenance, observations and identifiers
| ID | Normalized candidate | Working meaning | Evidence | W4 hypothesis | Status | V1 lineage |
|---|---|---|---|---|---|---|
| V2C-049 | Data Source | Authority/system/publication from which research data/evidence originate. | All P/C/S sources | Social/information artifact | X-INFRA | New formal provenance layer; improves C0038 limitations. |
| V2C-050 | Dataset | Organized data collection used for discovery/implementation/evaluation. | P1/P2/C1/S1/S2 | Information object | X-INFRA | New. |
| V2C-051 | Dataset Release / Version | Identified release/snapshot of a dataset or operational export. | P1/P2/P3/P4/P5/P7 | Information object/version relation | X-INFRA | New. |
| V2C-052 | Source Record | Identifiable row/record/document entry in a dataset/source. | P1–P5 | Information object | X-INFRA | New. |
| V2C-053 | Assertion | Proposition represented in the KG/research layer about domain entities/relations. | Demonstrator C, all sources | Proposition/information object | X-INFRA | New. |
| V2C-054 | Observation | Evidence-producing or evidence-representing observation about a domain subject with context/time. | P1/P2/P5/C1 | Event/result split candidate | X-INFRA | New generic parent for observation families. |
| V2C-055 | Measure / Quantity Value | Numeric/coded value attached to an observation, with unit/currency where applicable. | P1/P2/C1/P4 | Quality/value pattern | X-INFRA | New. |
| V2C-056 | Evidence Item | Source-backed evidence used to support an assertion, mapping or model decision. | Research design | Information object | X-INFRA | New; key traceability improvement. |
| V2C-057 | Mapping Assertion | Explicit claim that source concept/entity/field maps to a canonical concept/entity/relation. | Demonstrator C | Relator/proposition candidate | X-INFRA | New. |
| V2C-058 | Provenance Activity | Ingestion/transformation/normalization/mapping activity that uses and generates artifacts. | Demonstrator C | Perdurant | X-INFRA | New. |
| V2C-059 | Data Quality Finding | Recorded validation/quality result about a source record, mapping or artifact. | W1/W2 methodology, future SHACL/ETL | Information object/result | X-INFRA | Refines V1 C0034 beyond patient-record-specific quality. |
| V2C-060 | Identifier | Symbolic identifier assigned to a domain entity/record under a scheme/source. | P1–P7, C2, S1 | Information object / quality relation | X-INFRA | New explicit identity layer. |
| V2C-061 | Identifier Scheme | Scheme defining identifier syntax/issuer/scope (NDC, SPL, UNII, NHIF, ATC, GeoNames etc.). | P1–P7/S1 | Description/social object | X-INFRA | New. |
| V2C-062 | Identifier Assignment | Context connecting identifier, identified entity, scheme/source and validity. | Cross-source identity need | Relator | X-INFRA | New. |
| V2C-063 | Entity Match Assertion | Evidence-bearing assertion that two records/identifiers refer to the same or corresponding entity. | W1 AI candidate, P3/P4/P7 overlaps | Proposition/relator candidate | X-INFRA | New. |
| V2C-064 | Match Evidence / Confidence | Evidence/result supporting match status, confidence or ambiguity. | Entity-resolution design | Quality/result/information object | X-INFRA | New. |

## F. Market-access, safety, risk, BA and application extensions
| ID | Normalized candidate | Working meaning | Evidence | W4 hypothesis | Status | V1 lineage |
|---|---|---|---|---|---|---|
| V2C-065 | Reimbursement / Utilisation Observation | Aggregate observation of reimbursed/utilized products with payer/region/facility/diagnosis/time measures. | P1, P2, S2 | Observation | EXT — Market Access | New; replaces temptation to model aggregate `patients_num` as patients. |
| V2C-066 | Diagnosis Classification Reference | Diagnosis code/category used as context for reimbursement/clinical aggregate observations. | P1, P2 | Classification reference | EXT — Market Access | New. |
| V2C-067 | Risk Assessment | Assessment activity/result about risk in pharmaceutical ecosystem context. | W1 risk alignment + V1 | Perdurant + result split candidate | EXT — Risk/Resilience | Refines C0028. |
| V2C-068 | Vulnerability | Context-dependent vulnerability of an asset/value/system to a threat/disruption. | W1 risk alignment | Mode/relational quality | EXT — Risk/Resilience | New; align to COVER/ROSE in W4. |
| V2C-069 | Risk Treatment / Mitigation | Action/plan intended to modify risk/vulnerability/consequence. | W1 risk alignment | Perdurant/plan split | EXT — Risk/Resilience | Refines C0028 family. |
| V2C-070 | Pharmacovigilance Requirement | Normative safety-monitoring/reporting requirement. | V1 + optional S3 | Normative mode/social object | EXT — Safety | Retains/refines C0036. |
| V2C-071 | Adverse Event Reporting Activity | Activity of documenting/communicating suspected adverse-event information. | V1 + optional S3 | Perdurant | EXT — Safety | Refines C0022. |
| V2C-072 | Post-Market Surveillance Activity | Monitoring/evidence-gathering after market entry. | V1 + optional S3 | Perdurant | EXT — Safety | Retains C0037. |
| V2C-073 | Business Architecture View | Analytical representation mapping domain entities/activities to capabilities/processes/governance concerns. | V1 lineage | Description/View | EXT — BA | New explicit separation; replaces BA as Core decomposition principle. |
| V2C-074 | Enterprise Capability | Organizational capability used only in BA analytical view. | V1 | Mode/Disposition | EXT — BA | Moves C0005 out of Core identity. |
| V2C-075 | Strategic Partnership Agreement | Commitment-bearing partnership relation among actors. | V1/W1 application | Relator | EXT — Partnerships/BA | Retains C0014 only as extension. |
| V2C-076 | Digital / Information System Component | Application/information-system component supporting ecosystem activities. | V1 application lineage | Kind/artifact | EXT — Digital/Application | Generalizes C0029/C0030/C0031/C0033/C0035/C0038; technology-specific classes no longer Core. |
| V2C-077 | Clinical Care Participant Role | Generic clinical-care participant role for future clinical extension. | V1 only in W3; held-out H1 not mined | Role | EXT — Clinical | Consolidates C0007/C0017/C0019/C0021; detailed trial roles intentionally not admitted from H1. |
| V2C-078 | Clinical Care Pathway / Activity Pattern | Coordinated clinical-care activity/pathway semantics. | V1 | Relator/Perdurant pattern | DEFER — Clinical | Consolidates C0016/C0018; not needed for principal ecosystem article. |
| V2C-079 | Service Offering Specification | Specification of an ecosystem/business service offering. | V1 | Description | EXT — BA/Service | Retains C0039 outside Core. |
| V2C-080 | Public–Private Partnership Arrangement | Arrangement among public/private organizations. | V1/W1 partnership opportunity | Relator/Collective structure | DEFER — Partnerships | Refines C0012; not Core evidence-driven in W3. |

## Inventory counts
- Total normalized candidates: **80**.
- CORE candidates: **39**.
- Cross-cutting infrastructure (X-INFRA): **16**.
- Extension candidates: **23**.
- Deferred candidates: **2**.

These counts are a **pre-UFO discovery inventory**, not the final ontology size. W4 may split, merge, reclassify or reject candidates after identity/rigidity/dependence/relator analysis.

## Main discovery result
The data-grounded V2 center of gravity is materially different from V1. The strongest new semantic backbone is:

**Organization/Role → Site/Facility → Regulatory Context → Product/Substance/Presentation → Geography/Jurisdiction/Time → Shortage/Availability/Demand/Supply observations → Evidence/Provenance/Identifier infrastructure.**

This backbone directly supports Gate B demonstrators A–C while leaving Business Architecture, detailed clinical care, digital-health systems, pharmacovigilance, market access and generic risk as modular extensions rather than forcing them into the Core.
