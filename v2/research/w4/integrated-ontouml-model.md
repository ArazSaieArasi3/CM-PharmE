# W4 Integrated OntoUML Conceptual Model Specification

## Status
Gate-D candidate conceptual model. This is the authoritative W4 specification for W5 formalization; it is not yet the OWL release.

## 1. Core package — 32 named types

### Organization and contextual roles
| Type | Stereotype | Identity / dependence commitment |
|---|---|---|
| Organization | `<<Kind>>` | Social/institutional identity provider. |
| Ecosystem Participant | `<<RoleMixin>>` | Anti-rigid participation pattern spanning multiple bearer identities. |
| Regulatory Authority Role | `<<Role>>` | Role of Organization. |
| Manufacturer Role | `<<Role>>` | Role of Organization. |
| Importer Role | `<<Role>>` | Role of Organization. |
| Product-Responsible / Labeler Role | `<<Role>>` | Role of Organization. |
| Wholesale Distributor Role | `<<Role>>` | Role of Organization. |
| Third-Party Logistics Provider Role | `<<Role>>` | Role of Organization. |

### Facility and regulatory context
| Type | Stereotype | Commitment |
|---|---|---|
| Facility | `<<Kind>>` | Physical operational identity provider. |
| Manufacturing Site Role | `<<Role>>` | Role of Facility. |
| Distribution Site Role | `<<Role>>` | Role of Facility. |
| Facility Operation | `<<Relator>>` | Grounds Organization↔Facility operation/responsibility. |
| Establishment Registration | `<<Relator>>` | Grounds registered-entity/authority/jurisdiction context. |
| Regulatory Authorization | `<<Relator>>` | Grounds authorization/license relation. |
| Regulatory Jurisdiction | `<<Kind>>` | Social/legal scope entity. |

### Product layer
| Type | Stereotype | Commitment |
|---|---|---|
| Medicinal Product | `<<Kind>>` | Product identity layer represented across regulatory/access sources. |
| Pharmaceutical Substance | `<<Kind>>` | Substance identity layer. |
| Medicinal Product Presentation | `<<Kind>>` | Independently identifiable marketed/presented configuration. |
| Dosage Form Specification | `<<Kind>>` | Pharmaceutical-form specification/reference. |
| Strength | `<<Quality>>` | Quantitative characteristic of Product Presentation. |
| Package Configuration | `<<Kind>>` | Packaging/configuration specification. |
| Product Classification Scheme | `<<Kind>>` | Classification scheme identity. |
| Classification Entry | `<<Kind>>` | Entry/category identity within a scheme. |
| Product Classification Assignment | `<<Relator>>` | Product/Substance↔classification contextual assignment. |
| Market Listing | `<<Relator>>` | Product Presentation↔responsibility/source/jurisdiction/time listing context. |

### Activities, shortage and supply evidence
| Type | Stereotype | Commitment |
|---|---|---|
| Manufacturing Activity | `<<Event>>` | Manufacturing/processing occurrence. |
| Distribution / Logistics Activity | `<<Event>>` | Distribution/handling/storage/logistics occurrence. |
| Medicine Shortage Situation | `<<Situation>>` | Temporally/contextually bounded shortage state/configuration. |
| Supply Capacity | `<<Mode>>` | Disposition/capacity inhering in an Organization or Facility. |
| Availability Observation Result | `<<Subkind>>` of Observation Result | Persistent evidence result about availability. |
| Demand Observation Result | `<<Subkind>>` of Observation Result | Persistent evidence result about demand/consumption. |
| Supply Capacity Observation Result | `<<Subkind>>` of Observation Result | Evidence result about Supply Capacity. |

## 2. Cross-cutting infrastructure package — 25 named types

### Geography and time
| Type | Stereotype |
|---|---|
| Geographic Feature | `<<Kind>>` |
| Administrative Region | `<<Subkind>>` of Geographic Feature |
| Country | `<<Subkind>>` of Geographic Feature |
| Geospatial Position | `<<Datatype>>` |
| Address | `<<Datatype>>` |
| Time Interval | `<<Datatype>>` |
| Reporting Period | `<<Datatype>>` |

### Evidence and provenance
| Type | Stereotype |
|---|---|
| Data Source Resource | information-object `<<Kind>>` |
| Dataset | information-object `<<Kind>>` |
| Dataset Release | information-object `<<Kind>>` |
| Source Record | information-object `<<Kind>>` |
| Assertion | information-object `<<Kind>>` |
| Observation Activity | `<<Event>>` |
| Observation Result | information-object `<<Kind>>` |
| Measure Value | `<<Datatype>>` |
| Evidence Item | `<<RoleMixin>>` |
| Evidence Support | `<<Relator>>` |
| Mapping Assertion | `<<Subkind>>` of Assertion |
| Provenance Activity | `<<Event>>` |
| Data Quality Finding | `<<Subkind>>` of Assertion |

### Identity and matching
| Type | Stereotype |
|---|---|
| Identifier Value | `<<Datatype>>` |
| Identifier Scheme | information-object `<<Kind>>` |
| Identifier Assignment | `<<Relator>>` |
| Entity Match Assertion | `<<Subkind>>` of Assertion |
| Match Confidence | `<<Quality>>` of Entity Match Assertion |

## 3. Modular extension package — 30 named types

### Regulatory extension
- Regulatory Requirement — information/normative-object `<<Kind>>`
- Regulatory Oversight — `<<Relator>>`

### Policy / resilience / supply extension
- Contextual Medicine Classification Assignment — `<<Relator>>`
- Essential Medicine Classification — `<<Subkind>>` of Contextual Medicine Classification Assignment
- Critical Medicine Classification — `<<Subkind>>` of Contextual Medicine Classification Assignment
- Alternative Medicinal Product Role — `<<Role>>` of Medicinal Product/Presentation
- Alternative Medicine Assignment — `<<Relator>>`
- Supply Dependency — `<<Relator>>`
- Disruption Event — `<<Event>>`
- Inventory Observation Result — `<<Subkind>>` of Observation Result
- Procurement Activity — `<<Event>>`
- Lead-Time Observation Result — `<<Subkind>>` of Observation Result
- Stockout Situation — `<<Situation>>`

### Market Access extension
- Payer / Funding Organization Role — `<<Role>>` of Organization
- Reimbursement / Utilisation Observation Result — `<<Subkind>>` of Observation Result
- Diagnosis Classification Reference — information-object `<<Kind>>`

### Risk & Resilience adapter extension
- Asset-at-Risk — `<<RoleMixin>>`
- Risk Assessment Activity — `<<Event>>`
- Vulnerability — `<<Mode>>`
- Risk Treatment Plan — information/normative-object `<<Kind>>`
- Risk Treatment Activity — `<<Event>>`

### Safety extension
- Pharmacovigilance Requirement — information/normative-object `<<Kind>>`
- Adverse Event Reporting Activity — `<<Event>>`
- Post-Market Surveillance Activity — `<<Event>>`

### Business Architecture / partnership extension
- Business Architecture View — information-object `<<Kind>>`
- Enterprise Capability — `<<Mode>>`
- Strategic Partnership Agreement — `<<Relator>>`
- Service Offering Specification — information-object `<<Kind>>`

### Digital / Clinical extensions
- Digital / Information System Component — `<<Kind>>`
- Clinical Care Participant — `<<RoleMixin>>`

## 4. Generalization structure

### Organization role family
`Ecosystem Participant <<RoleMixin>>` generalizes role semantics across distinct bearer identities. Organization-specific specializations inherit identity from Organization:
- Regulatory Authority Role
- Manufacturer Role
- Importer Role
- Product-Responsible / Labeler Role
- Wholesale Distributor Role
- Third-Party Logistics Provider Role
- Payer / Funding Organization Role (extension)

Facility-specific specializations inherit identity from Facility:
- Manufacturing Site Role
- Distribution Site Role

The RoleMixin itself is abstract and cannot be instantiated without a concrete bearer identity.

### Geographic family
`Geographic Feature <<Kind>>`
- `Administrative Region <<Subkind>>`
- `Country <<Subkind>>`

No disjointness between the two subkinds is asserted at W4 because source/reference practices differ; W5 may add a more precise geographic pattern if necessary.

### Assertion family
`Assertion <<Kind>>`
- Mapping Assertion `<<Subkind>>`
- Entity Match Assertion `<<Subkind>>`
- Data Quality Finding `<<Subkind>>`

### Observation-result family
`Observation Result <<Kind>>`
- Availability Observation Result
- Demand Observation Result
- Supply Capacity Observation Result
- Inventory Observation Result (extension)
- Lead-Time Observation Result (extension)
- Reimbursement / Utilisation Observation Result (extension)

### Contextual classification family
`Contextual Medicine Classification Assignment <<Relator>>`
- Essential Medicine Classification `<<Subkind>>`
- Critical Medicine Classification `<<Subkind>>`

## 5. Core relation patterns

| Relation / pattern | OntoUML treatment | Main participants |
|---|---|---|
| operates | `<<Material>>` derived from Facility Operation | Organization ↔ Facility |
| role mediation | `<<Mediation>>` | contextual Relator ↔ Role bearer/role context |
| registered with | `<<Material>>` derived from Establishment Registration | Organization/Facility ↔ Authority |
| authorized for | `<<Material>>` derived from Regulatory Authorization | regulated party ↔ permitted role/activity |
| authorization applies in | formal/context relation | Regulatory Authorization → Jurisdiction |
| presentation of product | formal relation | Product Presentation → Medicinal Product |
| has active substance | formal/compositional specification relation | Product/Presentation → Substance |
| has dosage form | formal specification relation | Presentation → Dosage Form Specification |
| characterized by strength | `<<Characterization>>` | Product Presentation ↔ Strength |
| has package configuration | formal specification relation | Presentation → Package Configuration |
| classified as | `<<Material>>` derived from Product Classification Assignment | Product/Substance ↔ Classification Entry |
| listed/marketed in context | `<<Material>>` derived from Market Listing | Presentation ↔ jurisdiction/source/responsible role |
| participates in activity | participation relation | Organization/Facility/Product ↔ Event |
| shortage involves | situation involvement relation | Shortage Situation ↔ Product/Presentation/Jurisdiction |
| supply capacity characterizes | `<<Characterization>>` | Organization/Facility ↔ Supply Capacity |
| observation result about | formal/aboutness relation | Observation Result → domain entity/context |
| observation produces result | event→information relation | Observation Activity → Observation Result |
| result has value | value relation | Observation Result → Measure Value |

## 6. X-INFRA relation patterns
- Data Source Resource maintains/publishes Dataset.
- Dataset has Dataset Release.
- Dataset Release contains Source Record.
- Source Record supports Assertion through Evidence Support.
- Provenance Activity uses Dataset/Record and generates Assertion/Mapping/Artifact.
- Identifier Assignment connects identified entity, Identifier Value and Identifier Scheme.
- Identifier Scheme is maintained/issued by an authority/source where known.
- Entity Match Assertion links representations/entities propositionally and has Match Confidence/evidence.
- Geographic/temporal values qualify assertions, observations, relators and events without becoming identity providers.

## 7. Explicit non-equivalences / disjoint conceptual commitments
The model explicitly distinguishes:
- Organization ≠ Facility.
- Facility ≠ Geographic Feature/Position.
- Country/Region ≠ Regulatory Jurisdiction.
- Medicinal Product ≠ Pharmaceutical Substance.
- Medicinal Product ≠ Product Presentation.
- Product identity ≠ Identifier Value.
- Product Classification Entry ≠ Product identity.
- Observation Activity ≠ Observation Result.
- Observation Result ≠ domain phenomenon observed.
- Medicine Shortage Situation ≠ regulatory Source Record about the shortage.
- Supply Capacity ≠ Supply Capacity Observation Result.
- Risk ≠ Medicine Shortage Situation.
- BA View ≠ Core ontology identity.

These distinctions are primary W4 quality controls and should be preserved in W5 unless a recorded design decision revises them.

## 8. Deferred from Gate D
- Clinical Care Pathway / Activity Pattern.
- Public–Private Partnership Arrangement.
- complete global shipment/transaction ontology.
- finance/counterparty Core.
- technology-specific blockchain/EHR/telemedicine/AI system classes as Core.

## 9. W5 formalization contract
W5 must preserve the W4 identity and dependency structure while translating it into OWL/SHACL artifacts. Formalization may optimize OWL expressivity, but any semantic loss (e.g., RoleMixin/Relator distinctions not directly expressible in OWL DL) must be documented through annotations, SHACL or companion model metadata rather than silently discarded.
