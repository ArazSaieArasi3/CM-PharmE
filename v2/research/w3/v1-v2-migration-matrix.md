# W3 CM-PharmE 1.x → 2.0 Migration Matrix

## Purpose
Make continuity and novelty explicit before formal modeling. V1 remains a valid predecessor; V2 does not present retained V1 foundations as new contributions.

Migration statuses:
- **Retain/Refine** — concept remains relevant but is renamed, generalized, or restructured.
- **Split** — one V1 concept is replaced by multiple evidence-backed distinctions.
- **Move to Extension** — useful, but no longer part of the ecosystem Core.
- **Defer** — retained only for future/application scope.
- **Deprecate Generic/Technology-specific form** — semantics replaced by more durable typed concepts.

## A. V1 concept-by-concept migration
| V1 ID | V1 concept | V2 decision | V2 target / rationale |
|---|---|---|---|
| C0001 | Pharmaceutical Enterprise | **Refine** | Replace enterprise-centric identity with `Organization` plus contextual pharmaceutical roles. This removes Business Architecture from Core identity while preserving organizations as ecosystem participants. |
| C0002 | Organizational Unit Structure | **Move to Extension** | Organizational-design/BA view; not required by admitted data for principal ecosystem Core. |
| C0003 | Organizational Stakeholder | **Refine/Split** | `Ecosystem Participant Role` plus more specific regulatory/manufacturer/distributor/payer/etc. roles. |
| C0004 | Regulatory Oversight | **Refine** | `Regulatory Oversight Relationship`, `Regulatory Authorization/License`, Authority Role and Jurisdiction are modeled explicitly rather than one broad relator. |
| C0005 | Enterprise Capability | **Move to BA Extension** | Retained as `Enterprise Capability` in optional Business Architecture View, not Core decomposition. |
| C0006 | Strategic Resource Allocation | **Move/Defer** | BA/strategy extension; no W3 primary data need. |
| C0007 | Clinical Workforce | **Move to Clinical Extension** | Consolidated under `Clinical Care Participant Role`; principal V2 does not focus on care-delivery workforce. |
| C0008 | Ecosystem Actor | **Refine** | Becomes `Ecosystem Participant Role` borne by Organization/Site/other eligible bearers; actor is treated contextually rather than as a universal kind. |
| C0009 | Ecosystem Relationship | **Split / deprecate generic form** | Replaced by typed authorization, participation, supply-dependency, location, classification, provenance, mapping and partnership relations. |
| C0010 | Ecosystem Demand Signal | **Refine** | `Demand Observation`; evidence sources represent time/context-bounded observations rather than a generic Mode. |
| C0011 | Ecosystem Supply Capacity | **Refine** | `Supply Capacity Observation` and possibly a capacity/disposition distinction to be resolved in W4. |
| C0012 | Public-Private Partnership Structure | **Move/Defer** | `Public–Private Partnership Arrangement` in Partnerships/BA extension; not Core data-grounded need. |
| C0013 | Ecosystem Governance Entity | **Refine** | `Organization` + Governance/Regulatory Authority Role. Avoid governance-specific kind when the same organization can bear different roles. |
| C0014 | Strategic Partnership Agreement | **Retain in Extension** | Commitment-bearing partnership relator remains useful but outside principal Core. |
| C0015 | Pharmaceutical Business Process | **Refine/Split** | Data-grounded activities become typed `Manufacturing Activity`, `Distribution/Logistics Activity`, `Procurement Activity` etc.; BA process view remains optional. |
| C0016 | Clinical Activity Sequence | **Move to Clinical Extension** | Deferred from principal Core. |
| C0017 | Individual Patient | **Move to Clinical/Access Extension** | P1/P2 provide aggregate patient counts, not patient instances; do not infer individual patients from aggregate data. |
| C0018 | Clinical Pathway | **Move/Defer** | Clinical extension only; not needed by primary V2 demonstrators. |
| C0019 | Prescribing Physician | **Move to Clinical Extension** | Specialization of Clinical Care Participant Role; not principal Core. |
| C0020 | Healthcare Provider Organization | **Refine/Extension** | Generalize to `Organization`; provider status becomes contextual role when healthcare extension is activated. |
| C0021 | Healthcare Provider | **Move to Clinical/Access Extension** | Contextual healthcare-provider role; not Core. |
| C0022 | Adverse Event Reporting Procedure | **Move to Safety Extension** | `Adverse Event Reporting Activity`; optional S3/V1 lineage, not Core driver. |
| C0023 | Regulatory Authority Entity | **Refine** | `Organization` + `Regulatory Authority Role`; avoids hard-coding authority as a separate organizational kind where role/context is central. |
| C0024 | Regulatory Authority Role | **Retain/Refine** | Core role with explicit Jurisdiction and authorization/oversight relations. |
| C0025 | Enterprise Governance Relator | **Move/Re-evaluate** | BA/Governance extension; previous stereotype conflict remains historical evidence. W4 only revisits if extension is activated. |
| C0026 | Governance Policy Framework | **Move to Regulatory/BA Extension** | Policy/normative framework is not principal Core object. |
| C0027 | Compliance Requirement | **Refine** | `Regulatory Requirement`; extension/cross-cutting regulatory semantics with explicit applicability/jurisdiction. |
| C0028 | Risk Management Activity | **Move and Refine** | `Risk Assessment` / `Risk Treatment` in Risk & Resilience Extension; generic risk semantics aligned to COVER/ROSE patterns later. |
| C0029 | Digital Health Platform Component | **Generalize / Move** | General `Digital / Information System Component` in application extension; no technology/platform-specific Core. |
| C0030 | AI-Enabled Clinical Decision Support System | **Defer** | Technology/application-specific; AI becomes evaluable use case, not Core class. |
| C0031 | Blockchain-Based Supply Chain Ledger | **Deprecate technology-specific Core form** | Ledger technology is an implementation option, not durable ecosystem semantics. Provenance/KG/RDB infrastructure replaces blockchain-specific modeling need. |
| C0032 | Supply Chain Relationship | **Split / deprecate generic form** | Typed `Supply Dependency`, procurement/distribution participation and relationship evidence; no claim of complete transaction network. |
| C0033 | Electronic Health Record System | **Move to Digital/Clinical Extension** | Not principal ecosystem Core. |
| C0034 | Patient Record Quality | **Generalize** | `Data Quality Finding` cross-cutting infrastructure; patient-record-specific quality remains extension specialization. |
| C0035 | Telemedicine Service Channel | **Move to Digital/Clinical Extension** | Not principal V2 need. |
| C0036 | Pharmacovigilance Requirement | **Retain in Safety Extension** | Normative safety requirement; not Core unless safety extension activated. |
| C0037 | Post-Market Surveillance Activity | **Retain in Safety Extension** | Durable safety activity but not principal Core. |
| C0038 | Real-World Evidence Platform | **Generalize / Move** | Replace platform-specific Core semantics with `Data Source`, `Dataset`, `Evidence Item`, `Observation`, provenance activities; RWE platform may remain an application specialization. |
| C0039 | Service Offering Specification | **Move to BA/Service Extension** | Useful for business/application view, not ecosystem domain Core. |

## B. V1 relation migration policy
V1 includes 39 object properties plus one explicit generalization record. W3 does not preserve relation identity merely because a V1 property exists. Relation migration is governed by semantic families:

| V1 relation family | V2 disposition | Rationale |
|---|---|---|
| Enterprise structure/capability/resource relations | Move to BA extension | BA remains optional analytical view. |
| Generic stakeholder/actor relations | Refine into role-bearing and typed participation | Actor semantics become context-dependent and source-grounded. |
| Generic ecosystem relationship | Split into typed relators/material relations | Avoid one catch-all relationship class/property. |
| Clinical pathway/provider/patient relations | Move to Clinical extension | Not principal Core; held-out ClinicalTrials schema remains protected. |
| Governance/oversight relations | Refine into Authority Role, Jurisdiction, Requirement, Authorization/License and Oversight patterns | Strong current regulatory evidence supports explicit distinctions. |
| Generic business-process relations | Split into typed activities and participation | Manufacturing/distribution/procurement evidence supports domain-specific events. |
| Supply-chain relations | Split into distribution participation, conditional procurement/supply dependency, shortage/availability and alternatives | Public data do not justify full transaction network. |
| Digital-platform relations | Move to Digital/Application extension | Technology implementation is not Core ontology identity. |
| Safety/PV relations | Move to Safety extension | Preserved for modular extension. |
| Risk-management relations | Move/alignment to Risk & Resilience extension | Reuse generic risk semantics rather than duplicate. |

### Relation-level continuity rule for W4
When formal V2 relations are created, each should record `replaces/refines` metadata against relevant V1 relation IDs where a direct semantic predecessor exists. If a V1 relation has no evidence-backed V2 purpose, it remains in the frozen V1 lineage and is not automatically carried forward.

## C. Novelty accounting after migration
### Clearly retained foundations — not V2 novelty by themselves
- ecosystem actors/relationships as a research concern;
- regulatory governance/oversight concern;
- supply and demand concern;
- process/activity concern;
- UFO/OntoUML methodological lineage;
- competency-question/repository engineering experience.

### Material V2 advances emerging from W3
1. **Organization vs contextual role vs physical Site/Facility** distinction.
2. Explicit **Medicinal Product–Substance–Presentation–Form–Strength–Package** layer.
3. Explicit **Jurisdiction–Geography–Time** semantics.
4. Contextual **Critical/Essential Medicine classification** rather than intrinsic drug kinds.
5. Time/source-bounded **Shortage, Availability, Demand and Supply observations**.
6. First-class **Dataset–Record–Assertion–Mapping–Provenance** layer.
7. Explicit **Identifier Scheme/Assignment/Entity Match** semantics.
8. Business Architecture demoted from Core identity to an optional view.
9. Typed supply/resilience relations instead of generic “Supply Chain Relationship.”
10. Prospective held-out evaluation design before W3 concept discovery.

## D. Migration summary
| Migration outcome | Count / scope |
|---|---|
| Retain/refine into Core or cross-cutting V2 semantics | 15 V1 concepts materially contribute to new Core/infrastructure patterns |
| Move to modular extensions | 18 V1 concepts |
| Defer/deprecate technology/generic form | 6 V1 concepts |
| New normalized V2 candidates | Substantial — especially product, site, geography/jurisdiction, shortage/observation, evidence/provenance and identifier layers |

Counts describe W3 migration decisions, not final W4 ontology-class counts. W4 may merge/split candidates after foundational analysis.
