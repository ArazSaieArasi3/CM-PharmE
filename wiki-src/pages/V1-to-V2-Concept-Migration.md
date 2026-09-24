# V1 to V2 Concept Migration

> **Page scope:** Cross-version  
> **Documentation maturity:** Stable-to-date / Evolving  
> **V1 authority:** `main/catalog/concepts.yaml`  
> **V2 authority:** V2 W3/W4 migration and provenance artifacts  
> **Last synchronized:** 2026-09-23  
> **Related issues/PRs:** #159, #173, #206  
> **Evidence status:** All 39 V1 concepts have W3 migration dispositions; final V2 human review is still active  
> **Future refresh:** #213  
> **Wiki baseline:** WB-2026.09.1

## Migration vocabulary

V2 uses explicit migration outcomes rather than treating every old/new name as novelty:
- Retain / Refine
- Split
- Move to Extension
- Defer
- Deprecate generic/technology-specific form
- New V2 concept

## Complete V1 concept accounting

All **39 V1 canonical concepts** have a recorded W3 migration decision.

| V1 ID | V1 concept | Current V2 migration decision |
|---|---|---|
| C0001 | Pharmaceutical Enterprise | Refine to Organization + contextual pharmaceutical roles |
| C0002 | Organizational Unit Structure | Move to Business Architecture extension |
| C0003 | Organizational Stakeholder | Refine/Split into Ecosystem Participant and typed roles |
| C0004 | Regulatory Oversight | Refine/Split into oversight, authorization, authority role and jurisdiction patterns |
| C0005 | Enterprise Capability | Move to Business Architecture extension |
| C0006 | Strategic Resource Allocation | Move/Defer to BA/strategy extension |
| C0007 | Clinical Workforce | Move to Clinical extension |
| C0008 | Ecosystem Actor | Refine to contextual Ecosystem Participant role pattern |
| C0009 | Ecosystem Relationship | Split / deprecate generic form in favor of typed relations/relators |
| C0010 | Ecosystem Demand Signal | Refine to Demand Observation Result pattern |
| C0011 | Ecosystem Supply Capacity | Refine/Split into Supply Capacity and observation result |
| C0012 | Public-Private Partnership Structure | Move/Defer to partnership/BA extension |
| C0013 | Ecosystem Governance Entity | Refine to Organization + governance/regulatory role |
| C0014 | Strategic Partnership Agreement | Retain in extension |
| C0015 | Pharmaceutical Business Process | Refine/Split into typed manufacturing/logistics/procurement activities |
| C0016 | Clinical Activity Sequence | Move/Defer to Clinical extension |
| C0017 | Individual Patient | Move to Clinical/Access extension; not inferred from aggregate patient data |
| C0018 | Clinical Pathway | Move/Defer |
| C0019 | Prescribing Physician | Move to Clinical extension |
| C0020 | Healthcare Provider Organization | Refine/generalize to Organization; provider status contextual |
| C0021 | Healthcare Provider | Move to Clinical/Access extension |
| C0022 | Adverse Event Reporting Procedure | Move/refine to Pharmacovigilance extension activity |
| C0023 | Regulatory Authority Entity | Refine to Organization + Regulatory Authority role |
| C0024 | Regulatory Authority Role | Retain/Refine |
| C0025 | Enterprise Governance Relator | Move/Re-evaluate in extension |
| C0026 | Governance Policy Framework | Move to Regulatory/BA extension |
| C0027 | Compliance Requirement | Refine to Regulatory Requirement |
| C0028 | Risk Management Activity | Move and refine into Risk Management extension |
| C0029 | Digital Health Platform Component | Generalize/Move to Digital Systems extension |
| C0030 | AI-Enabled Clinical Decision Support System | Defer; application/technology-specific |
| C0031 | Blockchain-Based Supply Chain Ledger | Deprecate technology-specific Core form |
| C0032 | Supply Chain Relationship | Split / deprecate generic form into typed supply/procurement/distribution patterns |
| C0033 | Electronic Health Record System | Move to Digital/Clinical extension |
| C0034 | Patient Record Quality | Generalize to Data Quality Finding |
| C0035 | Telemedicine Service Channel | Move to Digital/Clinical extension |
| C0036 | Pharmacovigilance Requirement | Retain in Pharmacovigilance extension |
| C0037 | Post-Market Surveillance Activity | Retain in Pharmacovigilance extension |
| C0038 | Real-World Evidence Platform | Generalize into Data Source/Dataset/Evidence/Observation/Provenance patterns |
| C0039 | Service Offering Specification | Move to Business Architecture extension |

## W3 migration summary

The W3 migration artifact summarizes the 39 concepts as:
- **15** materially contributing to V2 Core or cross-cutting infrastructure patterns;
- **18** moved to modular extensions;
- **6** deferred or deprecated in generic/technology-specific form.

These counts describe W3 migration decisions, not the final number of V2 classes.

## New V2 semantic areas

Large parts of the V2 87-element baseline are genuinely new distinctions relative to V1, especially:
- facility/site identity and contextual site roles;
- medicinal product/substance/presentation/form/strength/package;
- classification scheme/entry/assignment;
- geography, jurisdiction and time;
- shortage/observation semantics;
- dataset/source/record/assertion/provenance;
- identifier scheme/assignment;
- entity match assertion/confidence.

## W3 to W4 transformation

W3 contained 80 normalized candidates; W4 reached 87 named conceptual elements through explicit foundational transformations such as:
- splitting Observation into Activity + Result;
- splitting Product Classification into Scheme + Entry + Assignment;
- separating Supply Capacity from evidence about capacity;
- adding truth-makers such as Facility Operation and Evidence Support.

This increase is not treated as uncontrolled scope expansion.

## Human-review status

The concept-provenance matrix records, for each V2 concept:
- definition;
- stereotype;
- V1 lineage;
- admitted evidence;
- held-out evidence;
- non-dataset support;
- formal IRI.

The 87-concept baseline is under domain-by-domain human review. Any approved semantic change must be reflected through #213.

## Evidence

- [Complete W3 migration matrix](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w3/v1-v2-migration-matrix.md)
- [W3→W4 transformation ledger](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w4/w3-w4-transformation-ledger.md)
- [V2 concept provenance matrix](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w4/human-review-concept-provenance-matrix.md)
- [V2 concept review catalog](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/review/concepts/index.md)
