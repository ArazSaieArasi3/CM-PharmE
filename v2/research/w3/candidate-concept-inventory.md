# W3 Normalized Candidate Concept Inventory

Status: **pre-UFO inventory**. These candidates state what semantic distinctions require analysis; W4 may merge, split, reclassify or reject them after UFO/OntoUML analysis. Candidate interpretations below are hypotheses, not final stereotypes.

Evidence codes follow the W2/W3 registry: P1–P7 primary, C1–C2 conditional, S1–S3 secondary/extension, V1 lineage. Protected H1–H3 held-out sources are not admission evidence.

## A. CORE candidates — 29
| ID | Candidate | Working semantic role | Main evidence / lineage |
|---|---|---|---|
| V2C-001 | Organization | Institutional/legal/social participant and bearer of roles. | P2/P3/P4/P5/C2/V1 |
| V2C-002 | Ecosystem Participant Role | Contextual role for participation in pharmaceutical ecosystem relations/activities. | P3–P6/V1 C0008/C0003 |
| V2C-003 | Regulatory Authority Role | Role borne when exercising regulatory authority in a jurisdiction. | P3/P5/C2/V1 C0024 |
| V2C-004 | Manufacturer Role | Contextual manufacturing role of organization/site. | P3/C2 |
| V2C-005 | Importer Role | Contextual regulated import role. | P3/C2 |
| V2C-006 | Product-Responsible / Labeler Role | Source/jurisdiction-specific responsibility for product listing/labeling/market responsibility. | P4/C2 |
| V2C-007 | Wholesale Distributor Role | Regulated wholesale-distribution role. | P3/C2 |
| V2C-008 | Third-Party Logistics Provider Role | Regulated 3PL role. | P3 |
| V2C-010 | Site / Facility | Physical operational site distinct from the organization operating/owning it. | P2/P3/C2 |
| V2C-011 | Manufacturing Site Role | Role borne by a site used/authorized for manufacturing/processing. | P3/C2 |
| V2C-012 | Distribution Site Role | Role borne by a site in wholesale/distribution/3PL activity. | P3/C2 |
| V2C-013 | Establishment Registration | Source/regulatory registration context connecting establishment/site and authority. | P3 |
| V2C-014 | Regulatory Authorization / License | Permission/authorization connecting authority, regulated party/activity, jurisdiction and validity. | P3/C2/V1 C0004 |
| V2C-017 | Regulatory Jurisdiction | Legal/regulatory scope in which roles, requirements, authorizations or classifications apply. | P3/P5/P6/C2 |
| V2C-025 | Medicinal Product | Pharmaceutical product entity/specification represented across product/regulatory/access sources. | P1/P2/P4/P5/P6 |
| V2C-026 | Pharmaceutical Substance / Active Ingredient | Active/medicinal substance identity layer. | P1/P2/P4/P5/P6/S1 |
| V2C-027 | Medicinal Product Presentation | Marketed/identified product presentation combining form/strength/package context. | P1/P2/P4/P5 |
| V2C-028 | Dosage Form | Pharmaceutical form associated with a product/presentation. | P4/P5/P6 |
| V2C-029 | Strength / Concentration Specification | Quantitative strength/concentration specification. | P1/P2/P4/P5/P6 |
| V2C-030 | Package Configuration | Pack/package structure and quantity configuration. | P1/P2/P4 |
| V2C-031 | Product Classification | Classification assignment/scheme such as ATC/therapeutic classification. | P1/P2/P4/P5 |
| V2C-032 | Product Listing / Marketing Status | Contextual source/jurisdiction/time status that a product is listed/marketed. | P4 |
| V2C-036 | Manufacturing Activity | Manufacturing/processing activity involving actor/site and product/substance. | P3/C2/V1 C0015 |
| V2C-037 | Distribution / Logistics Activity | Distribution/handling/storage/logistics activity in the pharmaceutical ecosystem. | P3/C2/V1 C0015/C0032 |
| V2C-039 | Medicine Shortage Case | Time/source/jurisdiction-bounded shortage case/situation. | P5 |
| V2C-040 | Shortage Status | Source-defined current/resolved/etc. status of a shortage case. | P5 |
| V2C-041 | Availability Observation | Evidence-bearing observation of product availability in context/time/place. | P5/ESMP + P1/P2 context |
| V2C-042 | Demand Observation | Evidence-bearing observation of product demand/consumption. | P5/ESMP/C1/P1/P2; refines V1 C0010 |
| V2C-043 | Supply Capacity Observation | Evidence-bearing observation/assessment of supply or capacity. | P5/ESMP/C1; refines V1 C0011 |

## B. Cross-cutting infrastructure (X-INFRA) — 23
| ID | Candidate | Working semantic role | Main evidence / rationale |
|---|---|---|---|
| V2C-018 | Geographic Feature | Identified geographic place/feature. | P7 + native locations |
| V2C-019 | Administrative Region | Administrative/reporting geographic area. | P1/P2/P7 |
| V2C-020 | Country | Country-level geographic/political reference. | P3/P5/P7 |
| V2C-021 | Geospatial Position | Coordinate/geometry representation. | P7 |
| V2C-022 | Address | Structured location description for organization/site resolution. | P3/C2 |
| V2C-023 | Time Interval | Temporal extent for validity, shortage, observation or activity. | P1/P2/P3/P5 |
| V2C-024 | Reporting Period | Source-defined period for aggregate observations/reports. | P1/P2/P5 |
| V2C-049 | Data Source | Maintaining/publishing authority/system/resource. | All source families |
| V2C-050 | Dataset | Organized data collection used by the research program. | P1/P2/C1/S1/S2 |
| V2C-051 | Dataset Release / Version | Identified snapshot/version for reproducibility. | P1–P7 |
| V2C-052 | Source Record | Identifiable row/entry/document record in a source. | P1–P5 |
| V2C-053 | Assertion | Proposition represented in canonical research/KG artifacts. | Demonstrator C |
| V2C-054 | Observation | Generic evidence-producing/evidence-representing observation pattern. | P1/P2/P5/C1 |
| V2C-055 | Measure / Quantity Value | Numeric/coded observation result with unit/currency/count semantics. | P1/P2/C1/P4 |
| V2C-056 | Evidence Item | Evidence supporting an assertion, mapping or model decision. | Research traceability requirement |
| V2C-057 | Mapping Assertion | Explicit source→canonical mapping claim. | Demonstrator C |
| V2C-058 | Provenance Activity | Ingestion/transformation/normalization/mapping activity. | Demonstrator C |
| V2C-059 | Data Quality Finding | Recorded validation/quality result. | W1/W2/W3 methodology; generalizes V1 C0034 |
| V2C-060 | Identifier | Symbolic identifier under a defined scheme/source. | P1–P7/C2/S1 |
| V2C-061 | Identifier Scheme | Scheme defining identifier scope/issuer/syntax. | P1–P7/S1 |
| V2C-062 | Identifier Assignment | Context connecting identifier, entity, scheme/source and validity. | Cross-source identity requirement |
| V2C-063 | Entity Match Assertion | Evidence-bearing same/corresponding-entity claim across sources. | W1 entity-resolution candidate + P3/P4/P7 overlap |
| V2C-064 | Match Evidence / Confidence | Evidence/result supporting match status, confidence or ambiguity. | Entity-resolution design |

## C. Modular extension candidates — 26
| ID | Candidate | Extension | Main evidence / lineage |
|---|---|---|---|
| V2C-009 | Payer / Funding Organization Role | Market Access | P1/P2/S2 |
| V2C-015 | Regulatory Requirement | Regulatory | P3/P5/C2/V1 C0027/C0036 |
| V2C-016 | Regulatory Oversight Relationship | Regulatory | P3/C2/V1 C0004 |
| V2C-033 | Essential Medicine Classification | Policy/Access | P6; contextual list/version semantics |
| V2C-034 | Critical Medicine Classification | Resilience/Policy | P5; contextual jurisdiction/version semantics |
| V2C-035 | Alternative Medicinal Product Role | Resilience/Policy | P5/P6 |
| V2C-038 | Supply Dependency | Resilience | P5/C1/W1; bounded because transaction-level global data are incomplete |
| V2C-044 | Disruption Event | Resilience | W1/P5/C1 |
| V2C-045 | Inventory Observation | Supply/Resilience | C1 |
| V2C-046 | Procurement Activity | Supply | C1 |
| V2C-047 | Lead-Time Observation | Supply/Resilience | C1 |
| V2C-048 | Stockout Event / Situation | Supply/Resilience | C1 + shortage framing |
| V2C-065 | Reimbursement / Utilisation Observation | Market Access | P1/P2/S2 |
| V2C-066 | Diagnosis Classification Reference | Market Access | P1/P2 |
| V2C-067 | Risk Assessment | Risk/Resilience | W1 risk alignment + V1 C0028 |
| V2C-068 | Vulnerability | Risk/Resilience | W1 risk alignment; align COVER/ROSE in W4 |
| V2C-069 | Risk Treatment / Mitigation | Risk/Resilience | W1 risk alignment/V1 |
| V2C-070 | Pharmacovigilance Requirement | Safety | V1 C0036 + optional S3 |
| V2C-071 | Adverse Event Reporting Activity | Safety | V1 C0022 + optional S3 |
| V2C-072 | Post-Market Surveillance Activity | Safety | V1 C0037 + optional S3 |
| V2C-073 | Business Architecture View | BA | V1 lineage; explicitly no longer Core decomposition |
| V2C-074 | Enterprise Capability | BA | V1 C0005 |
| V2C-075 | Strategic Partnership Agreement | Partnerships/BA | V1 C0014/W1 |
| V2C-076 | Digital / Information System Component | Digital/Application | Generalizes V1 C0029/C0030/C0031/C0033/C0035/C0038 |
| V2C-077 | Clinical Care Participant Role | Clinical | Consolidates V1 C0007/C0017/C0019/C0021; H1 not mined |
| V2C-079 | Service Offering Specification | BA/Service | V1 C0039 |

## D. Deferred candidates — 2
| ID | Candidate | Reason for deferment | Lineage |
|---|---|---|---|
| V2C-078 | Clinical Care Pathway / Activity Pattern | Valid clinical semantics but not required by principal V2 demonstrators; held-out ClinicalTrials schema remains protected. | V1 C0016/C0018 |
| V2C-080 | Public–Private Partnership Arrangement | Useful partnership/governance concept but weak data-driven Core need in W3. | V1 C0012/W1 |

## E. Explicitly rejected or transformed source/V1 items
These are not counted as separate normalized candidates:
- aggregate `patients_num` → **Measure**, not Individual Patient instances;
- monetary `costs` → **Measure**, not evidence for a Finance Core;
- ATC code → classification identifier, not product identity;
- generic V1 `Ecosystem Relationship` → split into typed relationships;
- generic V1 `Supply Chain Relationship` → split/refined into typed distribution/dependency/procurement relations with bounded evidence;
- Blockchain-Based Supply Chain Ledger → technology-specific implementation option, not Core;
- AI-CDSS/EHR/Telemedicine/RWE platform → application/digital specializations, not Core;
- held-out H1/H2/H3-only fields → cannot be W3 admission evidence.

## Inventory counts
- Total normalized candidates: **80**
- CORE: **29**
- X-INFRA: **23**
- EXT: **26**
- DEFER: **2**

## Main discovery result
The data-grounded V2 center of gravity is:

**Organization/Role → Site/Facility → Regulatory Context → Product/Substance/Presentation → Geography/Jurisdiction/Time → Shortage/Availability/Demand/Supply observations → Evidence/Provenance/Identifier infrastructure.**

This backbone supports Gate B demonstrators A–C while keeping Business Architecture, detailed clinical care, digital-health systems, pharmacovigilance, market access and generic risk modular rather than forcing them into the Core.
