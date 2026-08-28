# CM-PharmE 2.0 Visual Ontology Package

Status: V2 human-review artifact.  
Scope: 17 canonical domains.  
Source: Gate-D 87-element conceptual model plus the approved V2 concept-label normalization.  
Boundary: visual review aid only; stable V2 IRIs and formal semantics remain unchanged.

## 1. Ecosystem Organization
```mermaid
classDiagram
direction TB
class Organization { <<Kind>> }
class EcosystemParticipant { <<RoleMixin>> }
class RegulatoryAuthority { <<Role>> }
class Manufacturer { <<Role>> }
class Importer { <<Role>> }
class ProductResponsibleOrganization { <<Role>> }
class WholesaleDistributor { <<Role>> }
class ThirdPartyLogisticsProvider { <<Role>> }
Organization <|-- RegulatoryAuthority
Organization <|-- Manufacturer
Organization <|-- Importer
Organization <|-- ProductResponsibleOrganization
Organization <|-- WholesaleDistributor
Organization <|-- ThirdPartyLogisticsProvider
EcosystemParticipant <|-- RegulatoryAuthority
EcosystemParticipant <|-- Manufacturer
EcosystemParticipant <|-- Importer
EcosystemParticipant <|-- ProductResponsibleOrganization
EcosystemParticipant <|-- WholesaleDistributor
EcosystemParticipant <|-- ThirdPartyLogisticsProvider
```

## 2. Facility Operations
```mermaid
classDiagram
direction TB
class Facility { <<Kind>> }
class ManufacturingSite { <<Role>> }
class DistributionSite { <<Role>> }
class FacilityOperation { <<Relator>> }
class Organization { <<Kind>> }
Facility <|-- ManufacturingSite
Facility <|-- DistributionSite
FacilityOperation --> Organization : mediation
FacilityOperation --> Facility : mediation
```

## 3. Regulatory Governance
```mermaid
classDiagram
direction TB
class EstablishmentRegistration { <<Relator>> }
class RegulatoryAuthorization { <<Relator>> }
class RegulatoryJurisdiction { <<Kind>> }
class RegulatoryAuthority { <<Role>> }
class Facility { <<Kind>> }
class EcosystemParticipant { <<RoleMixin>> }
EstablishmentRegistration --> RegulatoryAuthority : mediation
EstablishmentRegistration --> Facility : mediation
EstablishmentRegistration --> RegulatoryJurisdiction : applies in
RegulatoryAuthorization --> RegulatoryAuthority : mediation
RegulatoryAuthorization --> EcosystemParticipant : mediation
RegulatoryAuthorization --> RegulatoryJurisdiction : applies in
```

## 4. Pharmaceutical Product
```mermaid
classDiagram
direction TB
class MedicinalProduct { <<Kind>> }
class PharmaceuticalSubstance { <<Kind>> }
class MedicinalProductPresentation { <<Kind>> }
class DosageFormSpecification { <<Kind>> }
class Strength { <<Quality>> }
class PackageConfiguration { <<Kind>> }
class ProductClassificationScheme { <<Kind>> }
class ClassificationEntry { <<Kind>> }
class ProductClassificationAssignment { <<Relator>> }
class MarketListing { <<Relator>> }
MedicinalProductPresentation --> MedicinalProduct : presentation of
MedicinalProductPresentation --> PharmaceuticalSubstance : active substance
MedicinalProductPresentation --> DosageFormSpecification : dosage form
MedicinalProductPresentation --> Strength : characterization
MedicinalProductPresentation --> PackageConfiguration : package
ProductClassificationAssignment --> MedicinalProduct : mediation
ProductClassificationAssignment --> ClassificationEntry : mediation
ClassificationEntry --> ProductClassificationScheme : in scheme
MarketListing --> MedicinalProductPresentation : mediation
```

## 5. Supply Operations
```mermaid
classDiagram
direction TB
class ManufacturingActivity { <<Event>> }
class PharmaceuticalLogisticsActivity { <<Event>> }
class MedicineShortageSituation { <<Situation>> }
class SupplyCapacity { <<Mode>> }
class Organization { <<Kind>> }
class Facility { <<Kind>> }
class MedicinalProductPresentation { <<Kind>> }
class RegulatoryJurisdiction { <<Kind>> }
Organization --> ManufacturingActivity : participates
Facility --> ManufacturingActivity : participates
MedicinalProductPresentation --> ManufacturingActivity : concerns
Organization --> PharmaceuticalLogisticsActivity : participates
Facility --> PharmaceuticalLogisticsActivity : participates
MedicineShortageSituation --> MedicinalProductPresentation : involves
MedicineShortageSituation --> RegulatoryJurisdiction : context
Organization --> SupplyCapacity : characterization
Facility --> SupplyCapacity : characterization
```

## 6. Ecosystem Observation
```mermaid
classDiagram
direction TB
class ObservationResult { <<Kind>> }
class AvailabilityObservationResult { <<Subkind>> }
class DemandObservationResult { <<Subkind>> }
class SupplyCapacityObservationResult { <<Subkind>> }
ObservationResult <|-- AvailabilityObservationResult
ObservationResult <|-- DemandObservationResult
ObservationResult <|-- SupplyCapacityObservationResult
```

## 7. Spatiotemporal Context
```mermaid
classDiagram
direction TB
class GeographicFeature { <<Kind>> }
class AdministrativeRegion { <<Subkind>> }
class Country { <<Subkind>> }
class GeospatialPosition { <<Datatype>> }
class Address { <<Datatype>> }
class TimeInterval { <<Datatype>> }
class ReportingPeriod { <<Datatype>> }
GeographicFeature <|-- AdministrativeRegion
GeographicFeature <|-- Country
GeographicFeature --> GeospatialPosition : position
GeographicFeature --> Address : address
```

## 8. Evidence Traceability
```mermaid
classDiagram
direction TB
class DataSource { <<Kind>> }
class Dataset { <<Kind>> }
class DatasetRelease { <<Kind>> }
class SourceRecord { <<Kind>> }
class Assertion { <<Kind>> }
class ObservationActivity { <<Event>> }
class ObservationResult { <<Kind>> }
class MeasureValue { <<Datatype>> }
class EvidenceItem { <<RoleMixin>> }
class EvidenceSupport { <<Relator>> }
class MappingAssertion { <<Subkind>> }
class ProvenanceActivity { <<Event>> }
class DataQualityFinding { <<Subkind>> }
Assertion <|-- MappingAssertion
Assertion <|-- DataQualityFinding
DataSource --> Dataset : maintains
Dataset --> DatasetRelease : release
DatasetRelease --> SourceRecord : contains
ObservationActivity --> ObservationResult : produces
ObservationResult --> MeasureValue : value
EvidenceSupport --> EvidenceItem : mediation
EvidenceSupport --> Assertion : mediation
ProvenanceActivity --> SourceRecord : uses
ProvenanceActivity --> Assertion : generates
```

## 9. Entity Identity
```mermaid
classDiagram
direction TB
class IdentifierValue { <<Datatype>> }
class IdentifierScheme { <<Kind>> }
class IdentifierAssignment { <<Relator>> }
class Assertion { <<Kind>> }
class EntityMatchAssertion { <<Subkind>> }
class MatchConfidence { <<Quality>> }
Assertion <|-- EntityMatchAssertion
IdentifierAssignment --> IdentifierValue : mediation
IdentifierAssignment --> IdentifierScheme : mediation
EntityMatchAssertion --> MatchConfidence : characterization
```

## 10. Regulatory Policy
```mermaid
classDiagram
direction TB
class RegulatoryRequirement { <<Kind>> }
class RegulatoryOversight { <<Relator>> }
class RegulatoryAuthority { <<Role>> }
class Organization { <<Kind>> }
RegulatoryOversight --> RegulatoryAuthority : mediation
RegulatoryOversight --> Organization : supervised party
RegulatoryOversight --> RegulatoryRequirement : governed by
```

## 11. Supply Resilience
```mermaid
classDiagram
direction TB
class ContextualMedicineClassificationAssignment { <<Relator>> }
class EssentialMedicineClassificationAssignment { <<Subkind>> }
class CriticalMedicineClassificationAssignment { <<Subkind>> }
class AlternativeMedicinalProduct { <<Role>> }
class AlternativeMedicinalProductAssignment { <<Relator>> }
class SupplyDependency { <<Relator>> }
class DisruptionEvent { <<Event>> }
class InventoryObservationResult { <<Subkind>> }
class ProcurementActivity { <<Event>> }
class LeadTimeObservationResult { <<Subkind>> }
class StockoutSituation { <<Situation>> }
class MedicinalProduct { <<Kind>> }
class ObservationResult { <<Kind>> }
ContextualMedicineClassificationAssignment <|-- EssentialMedicineClassificationAssignment
ContextualMedicineClassificationAssignment <|-- CriticalMedicineClassificationAssignment
MedicinalProduct <|-- AlternativeMedicinalProduct
AlternativeMedicinalProductAssignment --> MedicinalProduct : subject
AlternativeMedicinalProductAssignment --> AlternativeMedicinalProduct : alternative
ObservationResult <|-- InventoryObservationResult
ObservationResult <|-- LeadTimeObservationResult
SupplyDependency --> DisruptionEvent : exposed to
InventoryObservationResult --> StockoutSituation : evidences
```

## 12. Market Access
```mermaid
classDiagram
direction TB
class Organization { <<Kind>> }
class HealthcareFinancingOrganization { <<Role>> }
class ObservationResult { <<Kind>> }
class ReimbursementAndUtilizationObservationResult { <<Subkind>> }
class DiagnosisClassificationReference { <<Kind>> }
Organization <|-- HealthcareFinancingOrganization
ObservationResult <|-- ReimbursementAndUtilizationObservationResult
ReimbursementAndUtilizationObservationResult --> DiagnosisClassificationReference : contextualized by
```

## 13. Risk Management
```mermaid
classDiagram
direction TB
class AssetAtRisk { <<RoleMixin>> }
class RiskAssessmentActivity { <<Event>> }
class Vulnerability { <<Mode>> }
class RiskTreatmentPlan { <<Kind>> }
class RiskTreatmentActivity { <<Event>> }
AssetAtRisk --> Vulnerability : characterization
RiskAssessmentActivity --> AssetAtRisk : assesses
RiskAssessmentActivity --> Vulnerability : identifies
RiskTreatmentPlan --> Vulnerability : addresses
RiskTreatmentPlan --> RiskTreatmentActivity : realized through
```

## 14. Pharmacovigilance
```mermaid
classDiagram
direction TB
class PharmacovigilanceRequirement { <<Kind>> }
class AdverseEventReportingActivity { <<Event>> }
class PostMarketSurveillanceActivity { <<Event>> }
AdverseEventReportingActivity --> PharmacovigilanceRequirement : governed by
PostMarketSurveillanceActivity --> PharmacovigilanceRequirement : governed by
```

## 15. Business Architecture
```mermaid
classDiagram
direction TB
class BusinessArchitectureView { <<Kind>> }
class EnterpriseCapability { <<Mode>> }
class StrategicPartnershipAgreement { <<Relator>> }
class ServiceOfferingSpecification { <<Kind>> }
class Organization { <<Kind>> }
Organization --> EnterpriseCapability : characterization
StrategicPartnershipAgreement --> Organization : mediation
BusinessArchitectureView --> Organization : represents
BusinessArchitectureView --> EnterpriseCapability : represents
BusinessArchitectureView --> ServiceOfferingSpecification : represents
```

## 16. Digital Systems
```mermaid
classDiagram
direction TB
class DigitalSystemComponent { <<Kind>> }
class Organization { <<Kind>> }
class Facility { <<Kind>> }
DigitalSystemComponent --> Organization : supports
DigitalSystemComponent --> Facility : supports
```

## 17. Clinical Care
```mermaid
classDiagram
direction TB
class EcosystemParticipant { <<RoleMixin>> }
class ClinicalCareParticipant { <<RoleMixin>> }
EcosystemParticipant <|-- ClinicalCareParticipant
```

## Review guidance
These diagrams are optimized for human conceptual review rather than exhaustive OWL inspection. Cross-domain relations are repeated only where they clarify the domain. Formal truth remains in the V2 OntoUML specification and OWL/SHACL artifacts. Any diagram-driven semantic change must be recorded as a separate V2 design decision before formalization is changed.
