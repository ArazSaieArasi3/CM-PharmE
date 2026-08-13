# CM-PharmE Concepts

CM-PharmE v1.0.0 contains **39 canonical concepts** derived from **40 graphical concept occurrences** in the source model. `Enterprise Governance Relator` appears twice with conflicting stereotypes (`relator` and `mode`); it is represented once in the canonical registry as `relator` and explicitly flagged for review.

## Descriptive summary

| Stereotype | Count | Share |
|---|---:|---:|
| Kind | 13 | 33.3% |
| Mode | 8 | 20.5% |
| Role | 7 | 17.9% |
| Relator | 6 | 15.4% |
| Perdurant | 5 | 12.8% |
| **Total** | **39** | **100%** |

## Concept registry

| ID | Concept | Stereotype | Primary domain |
|---|---|---|---|
| `CMPE-C0001` | [Pharmaceutical Enterprise](pharmaceutical-enterprise.md) | kind | Organizational / Structural |
| `CMPE-C0002` | [Organizational Unit Structure](organizational-unit-structure.md) | kind | Organizational / Structural |
| `CMPE-C0003` | [Organizational Stakeholder](organizational-stakeholder.md) | role | Organizational / Structural |
| `CMPE-C0004` | [Regulatory Oversight](regulatory-oversight.md) | relator | Governance / Regulatory |
| `CMPE-C0005` | [Enterprise Capability](enterprise-capability.md) | mode | Organizational / Structural |
| `CMPE-C0006` | [Strategic Resource Allocation](strategic-resource-allocation.md) | mode | Organizational / Structural |
| `CMPE-C0007` | [Clinical Workforce](clinical-workforce.md) | role | Organizational / Structural |
| `CMPE-C0008` | [Ecosystem Actor](ecosystem-actor.md) | role | Ecosystem / Collaborative |
| `CMPE-C0009` | [Ecosystem Relationship](ecosystem-relationship.md) | relator | Ecosystem / Collaborative |
| `CMPE-C0010` | [Ecosystem Demand Signal](ecosystem-demand-signal.md) | mode | Ecosystem / Collaborative |
| `CMPE-C0011` | [Ecosystem Supply Capacity](ecosystem-supply-capacity.md) | mode | Ecosystem / Collaborative |
| `CMPE-C0012` | [Public-Private Partnership Structure](public-private-partnership-structure.md) | kind | Ecosystem / Collaborative |
| `CMPE-C0013` | [Ecosystem Governance Entity](ecosystem-governance-entity.md) | kind | Ecosystem / Collaborative |
| `CMPE-C0014` | [Strategic Partnership Agreement](strategic-partnership-agreement.md) | relator | Ecosystem / Collaborative |
| `CMPE-C0015` | [Pharmaceutical Business Process](pharmaceutical-business-process.md) | perdurant | Operational / Process |
| `CMPE-C0016` | [Clinical Activity Sequence](clinical-activity-sequence.md) | perdurant | Operational / Process |
| `CMPE-C0017` | [Individual Patient](individual-patient.md) | role | Operational / Process |
| `CMPE-C0018` | [Clinical Pathway](clinical-pathway.md) | relator | Operational / Process |
| `CMPE-C0019` | [Prescribing Physician](prescribing-physician.md) | role | Operational / Process |
| `CMPE-C0020` | [Healthcare Provider Organization](healthcare-provider-organization.md) | kind | Organizational / Structural |
| `CMPE-C0021` | [Healthcare Provider](healthcare-provider.md) | role | Operational / Process |
| `CMPE-C0022` | [Adverse Event Reporting Procedure](adverse-event-reporting-procedure.md) | perdurant | Operational / Process |
| `CMPE-C0023` | [Regulatory Authority Entity](regulatory-authority-entity.md) | kind | Governance / Regulatory |
| `CMPE-C0024` | [Regulatory Authority Role](regulatory-authority-role.md) | role | Governance / Regulatory |
| `CMPE-C0025` | [Enterprise Governance Relator](enterprise-governance-relator.md) | relator | Organizational / Structural |
| `CMPE-C0026` | [Governance Policy Framework](governance-policy-framework.md) | mode | Governance / Regulatory |
| `CMPE-C0027` | [Compliance Requirement](compliance-requirement.md) | mode | Governance / Regulatory |
| `CMPE-C0028` | [Risk Management Activity](risk-management-activity.md) | perdurant | Governance / Regulatory |
| `CMPE-C0029` | [Digital Health Platform Component](digital-health-platform-component.md) | kind | Digital Transformation |
| `CMPE-C0030` | [AI-Enabled Clinical Decision Support System](ai-enabled-clinical-decision-support-system.md) | kind | Digital Transformation |
| `CMPE-C0031` | [Blockchain-Based Supply Chain Ledger](blockchain-based-supply-chain-ledger.md) | kind | Digital Transformation |
| `CMPE-C0032` | [Supply Chain Relationship](supply-chain-relationship.md) | relator | Ecosystem / Collaborative |
| `CMPE-C0033` | [Electronic Health Record System](electronic-health-record-system.md) | kind | Digital Transformation |
| `CMPE-C0034` | [Patient Record Quality](patient-record-quality.md) | mode | Digital Transformation |
| `CMPE-C0035` | [Telemedicine Service Channel](telemedicine-service-channel.md) | kind | Digital Transformation |
| `CMPE-C0036` | [Pharmacovigilance Requirement](pharmacovigilance-requirement.md) | mode | Governance / Regulatory |
| `CMPE-C0037` | [Post-Market Surveillance Activity](post-market-surveillance-activity.md) | perdurant | Operational / Process |
| `CMPE-C0038` | [Real-World Evidence Platform](real-world-evidence-platform.md) | kind | Digital Transformation |
| `CMPE-C0039` | [Service Offering Specification](service-offering-specification.md) | kind | Ecosystem / Collaborative |

The registry deliberately excludes cardinality labels (`0..*`, `1`, `1..*`, `2..*`) and relation-label artifacts that the historical Draw.io-to-OWL converter incorrectly emitted as `owl:Class` declarations.
