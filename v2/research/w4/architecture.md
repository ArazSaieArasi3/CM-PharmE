# W4 Core / Infrastructure / Extension Architecture

## Architectural principle
CM-PharmE 2.0 is centered on **pharmaceutical-ecosystem entities, roles, sites, products, regulatory context, shortage/supply observations and traceable evidence**, not on Business Architecture as the primary decomposition mechanism.

## Package architecture

### 1. Core
The Core contains only semantics needed to identify and relate pharmaceutical ecosystem entities across the Gate C source portfolio and Gate B demonstrators.

Core clusters:
1. **Organization & Role** — Organization; ecosystem participant role pattern; authority/manufacturer/importer/labeler/distributor/3PL roles.
2. **Facility & Operation** — Facility; manufacturing/distribution site roles; facility-operation relation.
3. **Regulation** — Regulatory Jurisdiction; Establishment Registration; Regulatory Authorization.
4. **Product** — Medicinal Product; Pharmaceutical Substance; Product Presentation; Dosage Form Specification; Strength; Package Configuration; Classification Scheme/Entry/Assignment; Market Listing.
5. **Activities & Supply State** — Manufacturing Activity; Distribution/Logistics Activity; Supply Capacity; Medicine Shortage Situation.
6. **Core observation specializations** — Availability, Demand and Supply-Capacity Observation Results.

### 2. X-INFRA — cross-cutting semantic infrastructure
X-INFRA is reusable across Core and extensions but is not pharmaceutical-domain identity in itself.

Clusters:
- **Geography/time** — Geographic Feature, Administrative Region, Country, position/address/time/reporting values.
- **Evidence/provenance** — Data Source Resource, Dataset, Dataset Release, Source Record, Assertion, Observation Activity, Observation Result, Evidence support, provenance activity and data-quality findings.
- **Identity/integration** — Identifier Scheme/Value/Assignment, Mapping Assertion, Entity Match Assertion and Match Confidence.

### 3. Extensions
Extensions depend on Core/X-INFRA but do not alter Core identity principles.

| Extension | Main W4 elements | Boundary |
|---|---|---|
| Regulatory | Regulatory Requirement, Regulatory Oversight | Normative detail beyond minimum Core authorization/jurisdiction semantics. |
| Policy / Resilience | Essential/Critical classification, alternative-product pattern, Supply Dependency, Disruption, inventory/procurement/lead-time/stockout | Supports Demonstrator B; detailed operational semantics remain evidence-bounded. |
| Market Access | Payer/Funder Role, reimbursement/utilisation result, diagnosis classification reference | Based mainly on NHIF/access evidence; not a universal Core finance model. |
| Risk & Resilience | Asset-at-Risk role, Vulnerability, Risk Assessment, Risk Treatment | Adapter/alignment layer toward COVER/ROSE; no duplication of a generic risk ontology in Core. |
| Safety | Pharmacovigilance Requirement, AE Reporting, Post-Market Surveillance | Optional safety module. |
| Business Architecture | BA View, Enterprise Capability, Strategic Partnership Agreement, Service Offering Specification | Optional analytical view over ecosystem semantics. |
| Digital/Application | Digital/Information System Component | Technology/application specialization only. |
| Clinical | Clinical Care Participant RoleMixin | Minimal compatibility extension; detailed care pathway remains deferred. |

## Allowed dependency direction

```text
Business Architecture ─┐
Risk/Resilience ───────┤
Safety ────────────────┤
Market Access ─────────┤
Digital/Application ───┤──> Core ───> X-INFRA
Clinical ──────────────┤
Policy/Resilience ─────┤
Regulatory Extension ──┘
```

X-INFRA can be referenced by all modules. Core must not depend on BA, Risk, Clinical, Digital, Market Access or Safety extensions. Policy/Resilience may extend Core shortage/supply semantics but cannot redefine Product, Organization, Facility or Jurisdiction identity.

## Key architectural decisions
- `Pharmaceutical Enterprise` is not retained as the Core identity provider; `Organization` is.
- `Ecosystem Participant` is modeled as a contextual **RoleMixin**, not a Kind.
- physical `Facility` is distinct from social/legal `Organization` and from `Geographic Feature`.
- `Regulatory Jurisdiction` is a social/legal context linked to geography, not equivalent to country/region geometry.
- product identity is separated into Product, Substance and Presentation layers.
- evidence/provenance and identifier semantics are mandatory infrastructure because V2 claims traceable cross-representation consistency.
- Business Architecture and technology-specific concepts remain optional extensions.

## Gate D architectural condition
Gate D should approve this module dependency structure before W5 formalization. Changes to module boundaries after W5 should require a recorded architecture decision because they affect OWL imports, IRI policy and validation scope.
