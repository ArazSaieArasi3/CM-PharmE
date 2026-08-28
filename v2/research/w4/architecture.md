# W4 Core / Infrastructure / Extension Architecture

## Architectural principle
CM-PharmE 2.0 is centered on pharmaceutical-ecosystem entities, roles, sites, products, regulatory context, shortage and supply observations, and traceable evidence. Business Architecture remains an optional analytical extension rather than the primary ontology decomposition mechanism.

The canonical domain names are maintained in `domain-taxonomy.md`. Domain titles use cohesive semantic noun phrases and do not use `&` or `/` to concatenate concerns.

## Package architecture

### 1. Core
The Core contains only semantics needed to identify and relate pharmaceutical ecosystem entities across the Gate C source portfolio and Gate B demonstrators.

Core domains:
1. **Ecosystem Organization** — Organization; Ecosystem Participant; Regulatory Authority, Manufacturer, Importer, Product-Responsible/Labeler, Wholesale Distributor, and Third-Party Logistics Provider roles.
2. **Facility Operations** — Facility; Manufacturing Site Role; Distribution Site Role; Facility Operation.
3. **Regulatory Governance** — Regulatory Jurisdiction; Establishment Registration; Regulatory Authorization.
4. **Pharmaceutical Product** — Medicinal Product; Pharmaceutical Substance; Medicinal Product Presentation; Dosage Form Specification; Strength; Package Configuration; Product Classification Scheme; Classification Entry; Product Classification Assignment; Market Listing.
5. **Supply Operations** — Manufacturing Activity; Distribution/Logistics Activity; Supply Capacity; Medicine Shortage Situation.
6. **Ecosystem Observation** — Availability Observation Result; Demand Observation Result; Supply Capacity Observation Result.

### 2. X-INFRA — cross-cutting semantic infrastructure
X-INFRA is reusable across Core and extensions but is not pharmaceutical-domain identity in itself.

Cross-cutting domains:
- **Spatiotemporal Context** — Geographic Feature, Administrative Region, Country, Geospatial Position, Address, Time Interval, Reporting Period.
- **Evidence Traceability** — Data Source Resource, Dataset, Dataset Release, Source Record, Assertion, Observation Activity, Observation Result, Measure Value, Evidence Item, Evidence Support, Mapping Assertion, Provenance Activity, Data Quality Finding.
- **Entity Identity** — Identifier Value, Identifier Scheme, Identifier Assignment, Entity Match Assertion, Match Confidence.

### 3. Extensions
Extensions depend on Core/X-INFRA but do not alter Core identity principles.

| Extension domain | Main W4 elements | Boundary |
|---|---|---|
| Regulatory Policy | Regulatory Requirement, Regulatory Oversight | Normative detail beyond minimum Core authorization and jurisdiction semantics. |
| Supply Resilience | Essential/Critical classification, alternative-product pattern, Supply Dependency, Disruption, inventory, procurement, lead time, stockout | Supports resilience demonstrators; detailed operational semantics remain evidence-bounded. |
| Market Access | Payer/Funder Role, reimbursement/utilisation result, diagnosis classification reference | Based mainly on NHIF/access evidence; not a universal Core finance model. |
| Risk Management | Asset-at-Risk role, Vulnerability, Risk Assessment, Risk Treatment | Adapter/alignment layer toward COVER/ROSE; no duplication of a generic risk ontology in Core. |
| Pharmacovigilance | Pharmacovigilance Requirement, Adverse Event Reporting Activity, Post-Market Surveillance Activity | Optional safety and surveillance module. |
| Business Architecture | Business Architecture View, Enterprise Capability, Strategic Partnership Agreement, Service Offering Specification | Optional analytical view over ecosystem semantics. |
| Digital Systems | Digital/Information System Component | Technology/application specialization only. |
| Clinical Care | Clinical Care Participant RoleMixin | Minimal compatibility extension; detailed care pathway remains deferred. |

## Allowed dependency direction

```text
Business Architecture ─┐
Risk Management ───────┤
Pharmacovigilance ─────┤
Market Access ─────────┤
Digital Systems ───────┤──> Core ───> X-INFRA
Clinical Care ─────────┤
Supply Resilience ─────┤
Regulatory Policy ─────┘
```

X-INFRA can be referenced by all modules. Core must not depend on Business Architecture, Risk Management, Clinical Care, Digital Systems, Market Access, Pharmacovigilance, Supply Resilience, or Regulatory Policy extensions. Supply Resilience may extend Core shortage and supply semantics but cannot redefine Product, Organization, Facility, or Regulatory Jurisdiction identity.

## Key architectural decisions
- `Pharmaceutical Enterprise` is not retained as the Core identity provider; `Organization` is.
- `Ecosystem Participant` is modeled as a contextual **RoleMixin**, not a Kind.
- physical `Facility` is distinct from social/legal `Organization` and from `Geographic Feature`.
- `Regulatory Jurisdiction` is a social/legal context linked to geography, not equivalent to country/region geometry.
- product identity is separated into Product, Substance, and Presentation layers.
- Evidence Traceability and Entity Identity are mandatory cross-cutting infrastructure because V2 claims traceable cross-representation consistency.
- Business Architecture and technology-specific concepts remain optional extensions.

## Domain-name normalization record
The approved naming refinement is documented in `domain-taxonomy.md`. It changes human-facing architecture labels only; the Gate-D inventory remains **32 Core + 25 X-INFRA + 30 Extension = 87** conceptual elements.

## Gate D architectural condition
Gate D is approved. The module dependency structure is frozen as the W5 formalization baseline. Later changes to domain boundaries or identity/dependence commitments require a recorded design-change review because they can affect OWL imports, IRI policy, validation scope, manuscript claims, and visual ontology artifacts.
