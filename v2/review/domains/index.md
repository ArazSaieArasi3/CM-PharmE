---
artifact_type: domain_review_catalog
ontology_id: CM-PharmE
ontology_version: 2.0.0-alpha.1
review_status: active
---

# CM-PharmE 2.0 — Domain Review Catalog

The 17 canonical domains below are the approved V2 review taxonomy. Domain names avoid compound `and` / `&` constructions and each domain is intended to have one dominant semantic center.

| # | Domain | Layer | Working definition | Concepts | Review status | Diagram |
|---:|---|---|---|---:|---|---|
| 1 | Ecosystem Organization | Core | Organizations participating in the pharmaceutical ecosystem and the contextual roles through which they act. | 8 | Pending | [View](../../research/w4/visual-ontology-package.md#1-ecosystem-organization) |
| 2 | Facility Operations | Core | Physical or organizational facilities and the operational roles/relators through which sites participate in pharmaceutical activities. | 4 | Pending | [View](../../research/w4/visual-ontology-package.md#2-facility-operations) |
| 3 | Regulatory Governance | Core | Jurisdictions, registrations and authorizations that establish regulatory standing for organizations, facilities and products. | 3 | Pending | [View](../../research/w4/visual-ontology-package.md#3-regulatory-governance) |
| 4 | Pharmaceutical Product | Core | Medicinal products, substances, presentations, dosage/strength/package specifications and product classification/listing semantics. | 10 | Pending | [View](../../research/w4/visual-ontology-package.md#4-pharmaceutical-product) |
| 5 | Supply Operations | Core | Manufacturing, logistics, shortage situations and capacity semantics required to represent operational pharmaceutical supply. | 4 | Pending | [View](../../research/w4/visual-ontology-package.md#5-supply-operations) |
| 6 | Ecosystem Observation | Core | Core observation-result types used to represent availability, demand and supply-capacity measurements. | 3 | Pending | [View](../../research/w4/visual-ontology-package.md#6-ecosystem-observation) |
| 7 | Spatiotemporal Context | X-INFRA | Cross-cutting geographic and temporal context used to locate, scope and time ecosystem entities, observations and events. | 7 | Pending | [View](../../research/w4/visual-ontology-package.md#7-spatiotemporal-context) |
| 8 | Evidence Traceability | X-INFRA | Sources, datasets, records, assertions, observations and provenance structures used to make semantic claims traceable to evidence. | 13 | Pending | [View](../../research/w4/visual-ontology-package.md#8-evidence-traceability) |
| 9 | Entity Identity | X-INFRA | Identifier, assignment and entity-matching semantics used to connect heterogeneous records to the same or related real-world entities. | 5 | Pending | [View](../../research/w4/visual-ontology-package.md#9-entity-identity) |
| 10 | Regulatory Policy | Extension | Regulatory requirements and oversight structures that extend the core governance model with normative policy semantics. | 2 | Pending | [View](../../research/w4/visual-ontology-package.md#10-regulatory-policy) |
| 11 | Supply Resilience | Extension | Contextual criticality, alternatives, dependencies, disruption, procurement, inventory, lead-time and stockout semantics for resilience analysis. | 11 | Pending | [View](../../research/w4/visual-ontology-package.md#11-supply-resilience) |
| 12 | Market Access | Extension | Financing, reimbursement/utilization and diagnosis-reference semantics needed to represent access and funding context. | 3 | Pending | [View](../../research/w4/visual-ontology-package.md#12-market-access) |
| 13 | Risk Management | Extension | Assets at risk, assessment, vulnerability and treatment semantics for bounded pharmaceutical ecosystem risk analysis. | 5 | Pending | [View](../../research/w4/visual-ontology-package.md#13-risk-management) |
| 14 | Pharmacovigilance | Extension | Requirements and post-market reporting/surveillance activities used to represent medicine-safety monitoring context. | 3 | Pending | [View](../../research/w4/visual-ontology-package.md#14-pharmacovigilance) |
| 15 | Business Architecture | Extension | Optional business-architecture view semantics including capabilities, partnerships and service-offering specifications. | 4 | Pending | [View](../../research/w4/visual-ontology-package.md#15-business-architecture) |
| 16 | Digital Systems | Extension | Digital and information-system components that support organizations, facilities and ecosystem operations. | 1 | Pending | [View](../../research/w4/visual-ontology-package.md#16-digital-systems) |
| 17 | Clinical Care | Extension | Clinical-care participation as a bounded extension without expanding into a full clinical pathway ontology. | 1 | Pending | [View](../../research/w4/visual-ontology-package.md#17-clinical-care) |

## Layer summary
- **Core:** 32 concepts across 6 domains.
- **X-INFRA:** 25 concepts across 3 cross-cutting infrastructure domains.
- **Extensions:** 30 concepts across 8 extension domains.
- **Total:** 87 concepts across 17 domains.

## Human review questions
For each domain, confirm:
1. Is the domain name semantically cohesive and understandable?
2. Is the definition accurate and appropriately bounded?
3. Are the included concepts correctly owned by this domain?
4. Are important cross-domain dependencies visible?
5. Should any concept move, split, merge or be deferred?
6. Is the Core/X-INFRA/Extension placement justified?

## Authoritative sources
- [Integrated OntoUML model](../../research/w4/integrated-ontouml-model.md)
- [Visual ontology package](../../research/w4/visual-ontology-package.md)
- [Human-review concept provenance matrix](../../research/w4/human-review-concept-provenance-matrix.md)
