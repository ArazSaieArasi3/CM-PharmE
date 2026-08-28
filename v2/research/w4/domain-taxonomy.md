# CM-PharmE 2.0 Canonical Domain Taxonomy

Issue: #154
Status: **approved naming normalization**
Semantic baseline: Gate D approved; 87 conceptual elements unchanged.

## Naming rule
Domain and bounded-context titles use a single cohesive semantic noun phrase. Domain titles do not use `&` or `/` to concatenate semantic concerns. If concerns need to remain distinct, they are represented as separate domains or modules.

This naming refinement is architectural/documentary only. It does not change ontology identity, OntoUML stereotypes, OWL axioms, SHACL constraints, RDB/KG mappings, evaluation evidence, or manuscript claims.

## Canonical domains

| Layer | Canonical domain | Named concepts | Purpose |
|---|---|---:|---|
| Core | Ecosystem Organization | 8 | Organization identity and contextual pharmaceutical actor roles. |
| Core | Facility Operations | 4 | Facility identity, site roles, and organization-to-facility operational grounding. |
| Core | Regulatory Governance | 3 | Regulatory jurisdiction, registration, and authorization semantics. |
| Core | Pharmaceutical Product | 10 | Product, substance, presentation, formulation, packaging, classification, and listing semantics. |
| Core | Supply Operations | 4 | Manufacturing, logistics, shortage, and supply-capacity semantics. |
| Core | Ecosystem Observation | 3 | Core observation-result specializations for availability, demand, and supply capacity. |
| X-INFRA | Spatiotemporal Context | 7 | Geography, position, address, time interval, and reporting-period semantics. |
| X-INFRA | Evidence Traceability | 13 | Sources, datasets, releases, records, assertions, observation evidence, provenance, and quality findings. |
| X-INFRA | Entity Identity | 5 | Identifier assignment, identifier schemes, entity matching, and match confidence. |
| Extension | Regulatory Policy | 2 | Normative regulatory requirements and oversight. |
| Extension | Supply Resilience | 11 | Criticality, alternatives, dependencies, disruption, inventory, procurement, lead time, and stockout. |
| Extension | Market Access | 3 | Payer roles, reimbursement/utilisation observations, and diagnosis classification references. |
| Extension | Risk Management | 5 | Assets at risk, vulnerability, risk assessment, treatment plans, and treatment activities. |
| Extension | Pharmacovigilance | 3 | Pharmacovigilance requirements, adverse-event reporting, and post-market surveillance. |
| Extension | Business Architecture | 4 | Optional business-architecture analytical view and partnership/capability/service constructs. |
| Extension | Digital Systems | 1 | Digital and information-system component specialization. |
| Extension | Clinical Care | 1 | Minimal clinical-care participant compatibility extension. |

### Inventory check
- Core: **32**
- X-INFRA: **25**
- Extensions: **30**
- Total: **87**

## Approved migration map

| Previous label | Canonical label |
|---|---|
| Organization & Role | Ecosystem Organization |
| Facility & Operation | Facility Operations |
| Regulation | Regulatory Governance |
| Product | Pharmaceutical Product |
| Activities & Supply | Supply Operations |
| Core Observation | Ecosystem Observation |
| Geography & Time | Spatiotemporal Context |
| Evidence & Provenance | Evidence Traceability |
| Identity & Matching | Entity Identity |
| Regulatory Extension | Regulatory Policy |
| Policy & Resilience | Supply Resilience |
| Market Access | Market Access |
| Risk & Resilience | Risk Management |
| Safety | Pharmacovigilance |
| Business Architecture | Business Architecture |
| Digital / Application | Digital Systems |
| Clinical | Clinical Care |

## Architectural interpretation
These names provide a stable human-review taxonomy for manuscript writing, visualization, module documentation, and future DDD alignment. They do not by themselves assert that every domain is an independently deployable bounded context. A later DDD review may classify domains as Core, Supporting, Generic, Cross-Cutting Infrastructure, or Extension without changing this ontology taxonomy.

## Preservation boundary
The normalization preserves all Gate-D commitments, including:
- Organization distinct from Facility;
- Facility distinct from Geographic Feature;
- Regulatory Jurisdiction distinct from geographic identity;
- Medicinal Product distinct from Pharmaceutical Substance and Product Presentation;
- Observation Activity distinct from Observation Result;
- Supply Capacity distinct from its observation result;
- Risk Management and Business Architecture remaining extensions rather than Core decomposition principles.
