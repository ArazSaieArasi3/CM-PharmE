# V2 Ontology Reference

> **Version scope:** V2  
> **Status:** Stable-to-date / Evolving; semantic review pending  
> **Updated:** 2026-09-24

This is the exhaustive reader-facing reference projection for the current CM-PharmE 2.0 conceptual/formal baseline. It combines curated navigation with deterministic entity references generated from the V2 authority at `v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999`.

## Purpose and scope
Use this reference to discover modules, conceptual elements and formal properties, then follow the authoritative source links for semantic/evidence decisions. The reference does not replace the ontology source or semantic-review process.

## Architecture
- **Conceptual elements:** 87
- **OWL classes:** 81
- **Declared conceptual/formal datatypes:** 6
- **Object properties:** 52
- **Datatype properties:** 5
- **Review taxonomy:** 17 domains/modules
- **Conceptual layers:** Core / X-INFRA / Extensions

The 87 conceptual elements are **not** 87 OWL classes: 81 formalize as OWL classes and 6 as declared datatypes.

## Namespace and version
- target namespace: `https://w3id.org/cm-pharme/2.0/`
- formal development version: `2.0.0-alpha.1`
- conceptual registry: `Gate-D-2026-08-19`
- external w3id redirect deployment/registration remains outside the documentation claim.

## Formalization strategy
The conceptual registry preserves the UFO/OntoUML decisions. OWL/SHACL formalization may add implementation structure but may not silently reverse approved identity/dependence commitments. Generated reference pages report explicit formal constraints and do not infer absent endpoints.

## Relationship to V1
See [[V1 to V2 Research Evolution]], [[V1 to V2 Concept Migration]] and [[V1 to V2 Relation Migration]]. V2 is a controlled research evolution; predecessor semantics and V2-new distinctions are not conflated.

## How to use this reference
1. Start with a module below.
2. Open a concept page for definition, stereotype, formal entity, provenance and review state.
3. Follow principal object-property references for explicit formal relations.
4. Use datatype-property pages for literal-valued implementation properties.
5. Follow authority links when a semantic decision or review disposition matters.

## Module reference
| # | Module | Layer | Concepts | Review |
|---:|---|---|---:|---|
| 1 | [[V2 Module 01 Ecosystem Organization|Ecosystem Organization]] | Core | 8 | Pending |
| 2 | [[V2 Module 02 Facility Operations|Facility Operations]] | Core | 4 | Pending |
| 3 | [[V2 Module 03 Regulatory Governance|Regulatory Governance]] | Core | 3 | Pending |
| 4 | [[V2 Module 04 Pharmaceutical Product|Pharmaceutical Product]] | Core | 10 | Pending |
| 5 | [[V2 Module 05 Supply Operations|Supply Operations]] | Core | 4 | Pending |
| 6 | [[V2 Module 06 Ecosystem Observation|Ecosystem Observation]] | Core | 3 | Pending |
| 7 | [[V2 Module 07 Spatiotemporal Context|Spatiotemporal Context]] | X-INFRA | 7 | Pending |
| 8 | [[V2 Module 08 Evidence Traceability|Evidence Traceability]] | X-INFRA | 13 | Pending |
| 9 | [[V2 Module 09 Entity Identity|Entity Identity]] | X-INFRA | 5 | Pending |
| 10 | [[V2 Module 10 Regulatory Policy|Regulatory Policy]] | Extension | 2 | Pending |
| 11 | [[V2 Module 11 Supply Resilience|Supply Resilience]] | Extension | 11 | Pending |
| 12 | [[V2 Module 12 Market Access|Market Access]] | Extension | 3 | Pending |
| 13 | [[V2 Module 13 Risk Management|Risk Management]] | Extension | 5 | Pending |
| 14 | [[V2 Module 14 Pharmacovigilance|Pharmacovigilance]] | Extension | 3 | Pending |
| 15 | [[V2 Module 15 Business Architecture|Business Architecture]] | Extension | 4 | Pending |
| 16 | [[V2 Module 16 Digital Systems|Digital Systems]] | Extension | 1 | Pending |
| 17 | [[V2 Module 17 Clinical Care|Clinical Care]] | Extension | 1 | Pending |

## Concept reference — 87 conceptual elements
| # | Concept | Domain | Stereotype | Formal type | Review |
|---:|---|---|---|---|---|
| 1 | [[V2 Concept C001 Organization|Organization]] | Ecosystem Organization | Kind | OWL Class | pending |
| 2 | [[V2 Concept C002 Ecosystem Participant|Ecosystem Participant]] | Ecosystem Organization | RoleMixin | OWL Class | pending |
| 3 | [[V2 Concept C003 Regulatory Authority|Regulatory Authority]] | Ecosystem Organization | Role | OWL Class | pending |
| 4 | [[V2 Concept C004 Manufacturer|Manufacturer]] | Ecosystem Organization | Role | OWL Class | pending |
| 5 | [[V2 Concept C005 Importer|Importer]] | Ecosystem Organization | Role | OWL Class | pending |
| 6 | [[V2 Concept C006 Product Responsible Organization|Product Responsible Organization]] | Ecosystem Organization | Role | OWL Class | pending |
| 7 | [[V2 Concept C007 Wholesale Distributor|Wholesale Distributor]] | Ecosystem Organization | Role | OWL Class | pending |
| 8 | [[V2 Concept C008 Third-Party Logistics Provider|Third-Party Logistics Provider]] | Ecosystem Organization | Role | OWL Class | pending |
| 9 | [[V2 Concept C009 Facility|Facility]] | Facility Operations | Kind | OWL Class | pending |
| 10 | [[V2 Concept C010 Manufacturing Site|Manufacturing Site]] | Facility Operations | Role | OWL Class | pending |
| 11 | [[V2 Concept C011 Distribution Site|Distribution Site]] | Facility Operations | Role | OWL Class | pending |
| 12 | [[V2 Concept C012 Facility Operation|Facility Operation]] | Facility Operations | Relator | OWL Class | pending |
| 13 | [[V2 Concept C013 Establishment Registration|Establishment Registration]] | Regulatory Governance | Relator | OWL Class | pending |
| 14 | [[V2 Concept C014 Regulatory Authorization|Regulatory Authorization]] | Regulatory Governance | Relator | OWL Class | pending |
| 15 | [[V2 Concept C015 Regulatory Jurisdiction|Regulatory Jurisdiction]] | Regulatory Governance | Kind | OWL Class | pending |
| 16 | [[V2 Concept C016 Medicinal Product|Medicinal Product]] | Pharmaceutical Product | Kind | OWL Class | pending |
| 17 | [[V2 Concept C017 Pharmaceutical Substance|Pharmaceutical Substance]] | Pharmaceutical Product | Kind | OWL Class | pending |
| 18 | [[V2 Concept C018 Medicinal Product Presentation|Medicinal Product Presentation]] | Pharmaceutical Product | Kind | OWL Class | pending |
| 19 | [[V2 Concept C019 Dosage Form Specification|Dosage Form Specification]] | Pharmaceutical Product | Kind | OWL Class | pending |
| 20 | [[V2 Concept C020 Strength|Strength]] | Pharmaceutical Product | Quality | OWL Class | pending |
| 21 | [[V2 Concept C021 Package Configuration|Package Configuration]] | Pharmaceutical Product | Kind | OWL Class | pending |
| 22 | [[V2 Concept C022 Product Classification Scheme|Product Classification Scheme]] | Pharmaceutical Product | Kind | OWL Class | pending |
| 23 | [[V2 Concept C023 Classification Entry|Classification Entry]] | Pharmaceutical Product | Kind | OWL Class | pending |
| 24 | [[V2 Concept C024 Product Classification Assignment|Product Classification Assignment]] | Pharmaceutical Product | Relator | OWL Class | pending |
| 25 | [[V2 Concept C025 Market Listing|Market Listing]] | Pharmaceutical Product | Relator | OWL Class | pending |
| 26 | [[V2 Concept C026 Manufacturing Activity|Manufacturing Activity]] | Supply Operations | Event | OWL Class | pending |
| 27 | [[V2 Concept C027 Pharmaceutical Logistics Activity|Pharmaceutical Logistics Activity]] | Supply Operations | Event | OWL Class | pending |
| 28 | [[V2 Concept C028 Medicine Shortage Situation|Medicine Shortage Situation]] | Supply Operations | Situation | OWL Class | pending |
| 29 | [[V2 Concept C029 Supply Capacity|Supply Capacity]] | Supply Operations | Mode | OWL Class | pending |
| 30 | [[V2 Concept C030 Availability Observation Result|Availability Observation Result]] | Ecosystem Observation | Subkind | OWL Class | pending |
| 31 | [[V2 Concept C031 Demand Observation Result|Demand Observation Result]] | Ecosystem Observation | Subkind | OWL Class | pending |
| 32 | [[V2 Concept C032 Supply Capacity Observation Result|Supply Capacity Observation Result]] | Ecosystem Observation | Subkind | OWL Class | pending |
| 33 | [[V2 Concept C033 Geographic Feature|Geographic Feature]] | Spatiotemporal Context | Kind | OWL Class | pending |
| 34 | [[V2 Concept C034 Administrative Region|Administrative Region]] | Spatiotemporal Context | Subkind | OWL Class | pending |
| 35 | [[V2 Concept C035 Country|Country]] | Spatiotemporal Context | Subkind | OWL Class | pending |
| 36 | [[V2 Concept C036 Geospatial Position|Geospatial Position]] | Spatiotemporal Context | Datatype | RDFS Datatype | pending |
| 37 | [[V2 Concept C037 Address|Address]] | Spatiotemporal Context | Datatype | RDFS Datatype | pending |
| 38 | [[V2 Concept C038 Time Interval|Time Interval]] | Spatiotemporal Context | Datatype | RDFS Datatype | pending |
| 39 | [[V2 Concept C039 Reporting Period|Reporting Period]] | Spatiotemporal Context | Datatype | RDFS Datatype | pending |
| 40 | [[V2 Concept C040 Data Source|Data Source]] | Evidence Traceability | Kind | OWL Class | pending |
| 41 | [[V2 Concept C041 Dataset|Dataset]] | Evidence Traceability | Kind | OWL Class | pending |
| 42 | [[V2 Concept C042 Dataset Release|Dataset Release]] | Evidence Traceability | Kind | OWL Class | pending |
| 43 | [[V2 Concept C043 Source Record|Source Record]] | Evidence Traceability | Kind | OWL Class | pending |
| 44 | [[V2 Concept C044 Assertion|Assertion]] | Evidence Traceability | Kind | OWL Class | pending |
| 45 | [[V2 Concept C045 Observation Activity|Observation Activity]] | Evidence Traceability | Event | OWL Class | pending |
| 46 | [[V2 Concept C046 Observation Result|Observation Result]] | Evidence Traceability | Kind | OWL Class | pending |
| 47 | [[V2 Concept C047 Measure Value|Measure Value]] | Evidence Traceability | Datatype | RDFS Datatype | pending |
| 48 | [[V2 Concept C048 Evidence Item|Evidence Item]] | Evidence Traceability | RoleMixin | OWL Class | pending |
| 49 | [[V2 Concept C049 Evidence Support|Evidence Support]] | Evidence Traceability | Relator | OWL Class | pending |
| 50 | [[V2 Concept C050 Mapping Assertion|Mapping Assertion]] | Evidence Traceability | Subkind | OWL Class | pending |
| 51 | [[V2 Concept C051 Provenance Activity|Provenance Activity]] | Evidence Traceability | Event | OWL Class | pending |
| 52 | [[V2 Concept C052 Data Quality Finding|Data Quality Finding]] | Evidence Traceability | Subkind | OWL Class | pending |
| 53 | [[V2 Concept C053 Identifier Value|Identifier Value]] | Entity Identity | Datatype | RDFS Datatype | pending |
| 54 | [[V2 Concept C054 Identifier Scheme|Identifier Scheme]] | Entity Identity | Kind | OWL Class | pending |
| 55 | [[V2 Concept C055 Identifier Assignment|Identifier Assignment]] | Entity Identity | Relator | OWL Class | pending |
| 56 | [[V2 Concept C056 Entity Match Assertion|Entity Match Assertion]] | Entity Identity | Subkind | OWL Class | pending |
| 57 | [[V2 Concept C057 Match Confidence|Match Confidence]] | Entity Identity | Quality | OWL Class | pending |
| 58 | [[V2 Concept C058 Regulatory Requirement|Regulatory Requirement]] | Regulatory Policy | Kind | OWL Class | pending |
| 59 | [[V2 Concept C059 Regulatory Oversight|Regulatory Oversight]] | Regulatory Policy | Relator | OWL Class | pending |
| 60 | [[V2 Concept C060 Contextual Medicine Classification Assignment|Contextual Medicine Classification Assignment]] | Supply Resilience | Relator | OWL Class | pending |
| 61 | [[V2 Concept C061 Essential Medicine Classification Assignment|Essential Medicine Classification Assignment]] | Supply Resilience | Subkind | OWL Class | pending |
| 62 | [[V2 Concept C062 Critical Medicine Classification Assignment|Critical Medicine Classification Assignment]] | Supply Resilience | Subkind | OWL Class | pending |
| 63 | [[V2 Concept C063 Alternative Medicinal Product|Alternative Medicinal Product]] | Supply Resilience | Role | OWL Class | pending |
| 64 | [[V2 Concept C064 Alternative Medicinal Product Assignment|Alternative Medicinal Product Assignment]] | Supply Resilience | Relator | OWL Class | pending |
| 65 | [[V2 Concept C065 Supply Dependency|Supply Dependency]] | Supply Resilience | Relator | OWL Class | pending |
| 66 | [[V2 Concept C066 Disruption Event|Disruption Event]] | Supply Resilience | Event | OWL Class | pending |
| 67 | [[V2 Concept C067 Inventory Observation Result|Inventory Observation Result]] | Supply Resilience | Subkind | OWL Class | pending |
| 68 | [[V2 Concept C068 Procurement Activity|Procurement Activity]] | Supply Resilience | Event | OWL Class | pending |
| 69 | [[V2 Concept C069 Lead Time Observation Result|Lead Time Observation Result]] | Supply Resilience | Subkind | OWL Class | pending |
| 70 | [[V2 Concept C070 Stockout Situation|Stockout Situation]] | Supply Resilience | Situation | OWL Class | pending |
| 71 | [[V2 Concept C071 Healthcare Financing Organization|Healthcare Financing Organization]] | Market Access | Role | OWL Class | pending |
| 72 | [[V2 Concept C072 Reimbursement and Utilization Observation Result|Reimbursement and Utilization Observation Result]] | Market Access | Subkind | OWL Class | pending |
| 73 | [[V2 Concept C073 Diagnosis Classification Reference|Diagnosis Classification Reference]] | Market Access | Kind | OWL Class | pending |
| 74 | [[V2 Concept C074 Asset at Risk|Asset at Risk]] | Risk Management | RoleMixin | OWL Class | pending |
| 75 | [[V2 Concept C075 Risk Assessment Activity|Risk Assessment Activity]] | Risk Management | Event | OWL Class | pending |
| 76 | [[V2 Concept C076 Vulnerability|Vulnerability]] | Risk Management | Mode | OWL Class | pending |
| 77 | [[V2 Concept C077 Risk Treatment Plan|Risk Treatment Plan]] | Risk Management | Kind | OWL Class | pending |
| 78 | [[V2 Concept C078 Risk Treatment Activity|Risk Treatment Activity]] | Risk Management | Event | OWL Class | pending |
| 79 | [[V2 Concept C079 Pharmacovigilance Requirement|Pharmacovigilance Requirement]] | Pharmacovigilance | Kind | OWL Class | pending |
| 80 | [[V2 Concept C080 Adverse Event Reporting Activity|Adverse Event Reporting Activity]] | Pharmacovigilance | Event | OWL Class | pending |
| 81 | [[V2 Concept C081 Post-Market Surveillance Activity|Post-Market Surveillance Activity]] | Pharmacovigilance | Event | OWL Class | pending |
| 82 | [[V2 Concept C082 Business Architecture View|Business Architecture View]] | Business Architecture | Kind | OWL Class | pending |
| 83 | [[V2 Concept C083 Enterprise Capability|Enterprise Capability]] | Business Architecture | Mode | OWL Class | pending |
| 84 | [[V2 Concept C084 Strategic Partnership Agreement|Strategic Partnership Agreement]] | Business Architecture | Relator | OWL Class | pending |
| 85 | [[V2 Concept C085 Service Offering Specification|Service Offering Specification]] | Business Architecture | Kind | OWL Class | pending |
| 86 | [[V2 Concept C086 Digital System Component|Digital System Component]] | Digital Systems | Kind | OWL Class | pending |
| 87 | [[V2 Concept C087 Clinical Care Participant|Clinical Care Participant]] | Clinical Care | RoleMixin | OWL Class | pending |

## Object-property reference — 52 properties
| Property | Layer | Domain | Range | Review |
|---|---|---|---|---|
| [[V2 Object Property alternativeForProduct|`alternativeForProduct`]] | Extension | AlternativeMedicineAssignment | cmpe:MedicinalProduct | Pending |
| [[V2 Object Property alternativeProduct|`alternativeProduct`]] | Extension | AlternativeMedicineAssignment | cmpe:MedicinalProduct | Pending |
| [[V2 Object Property authorizationAuthority|`authorizationAuthority`]] | Core | RegulatoryAuthorization | cmpe:Organization | Pending |
| [[V2 Object Property authorizationJurisdiction|`authorizationJurisdiction`]] | Core | RegulatoryAuthorization | cmpe:RegulatoryJurisdiction | Pending |
| [[V2 Object Property authorizationParty|`authorizationParty`]] | Core | RegulatoryAuthorization | unspecified | Pending |
| [[V2 Object Property baViewRepresents|`baViewRepresents`]] | Extension | BusinessArchitectureView | unspecified | Pending |
| [[V2 Object Property capacityBearer|`capacityBearer`]] | Core | SupplyCapacity | unspecified | Pending |
| [[V2 Object Property classificationEntity|`classificationEntity`]] | Core | ProductClassificationAssignment | unspecified | Pending |
| [[V2 Object Property classificationEntry|`classificationEntry`]] | Core | ProductClassificationAssignment | cmpe:ClassificationEntry | Pending |
| [[V2 Object Property containsSourceRecord|`containsSourceRecord`]] | X-INFRA | DatasetRelease | cmpe:SourceRecord | Pending |
| [[V2 Object Property contextClassificationEntry|`contextClassificationEntry`]] | Extension | ContextualMedicineClassificationAssignment | cmpe:ClassificationEntry | Pending |
| [[V2 Object Property contextClassificationJurisdiction|`contextClassificationJurisdiction`]] | Extension | ContextualMedicineClassificationAssignment | cmpe:RegulatoryJurisdiction | Pending |
| [[V2 Object Property contextClassificationProduct|`contextClassificationProduct`]] | Extension | ContextualMedicineClassificationAssignment | cmpe:MedicinalProduct | Pending |
| [[V2 Object Property dependencyDependent|`dependencyDependent`]] | Extension | SupplyDependency | unspecified | Pending |
| [[V2 Object Property dependencyProvider|`dependencyProvider`]] | Extension | SupplyDependency | unspecified | Pending |
| [[V2 Object Property disruptionAffects|`disruptionAffects`]] | Extension | DisruptionEvent | unspecified | Pending |
| [[V2 Object Property entryInScheme|`entryInScheme`]] | Core | ClassificationEntry | cmpe:ProductClassificationScheme | Pending |
| [[V2 Object Property evidenceAssertion|`evidenceAssertion`]] | X-INFRA | EvidenceSupport | cmpe:Assertion | Pending |
| [[V2 Object Property evidenceRecord|`evidenceRecord`]] | X-INFRA | EvidenceSupport | cmpe:SourceRecord | Pending |
| [[V2 Object Property generatedAssertion|`generatedAssertion`]] | X-INFRA | ProvenanceActivity | cmpe:Assertion | Pending |
| [[V2 Object Property hasActiveSubstance|`hasActiveSubstance`]] | Core | unspecified | cmpe:PharmaceuticalSubstance | Pending |
| [[V2 Object Property hasDatasetRelease|`hasDatasetRelease`]] | X-INFRA | Dataset | cmpe:DatasetRelease | Pending |
| [[V2 Object Property hasDosageForm|`hasDosageForm`]] | Core | MedicinalProductPresentation | cmpe:DosageFormSpecification | Pending |
| [[V2 Object Property hasMatchConfidence|`hasMatchConfidence`]] | X-INFRA | EntityMatchAssertion | cmpe:MatchConfidence | Pending |
| [[V2 Object Property hasPackageConfiguration|`hasPackageConfiguration`]] | Core | MedicinalProductPresentation | cmpe:PackageConfiguration | Pending |
| [[V2 Object Property hasStrength|`hasStrength`]] | Core | MedicinalProductPresentation | cmpe:Strength | Pending |
| [[V2 Object Property identifierEntity|`identifierEntity`]] | X-INFRA | IdentifierAssignment | unspecified | Pending |
| [[V2 Object Property identifierScheme|`identifierScheme`]] | X-INFRA | IdentifierAssignment | cmpe:IdentifierScheme | Pending |
| [[V2 Object Property listingJurisdiction|`listingJurisdiction`]] | Core | MarketListing | cmpe:RegulatoryJurisdiction | Pending |
| [[V2 Object Property listingPresentation|`listingPresentation`]] | Core | MarketListing | cmpe:MedicinalProductPresentation | Pending |
| [[V2 Object Property listingResponsibleOrganization|`listingResponsibleOrganization`]] | Core | MarketListing | cmpe:Organization | Pending |
| [[V2 Object Property locatedIn|`locatedIn`]] | X-INFRA | unspecified | cmpe:GeographicFeature | Pending |
| [[V2 Object Property maintainsDataset|`maintainsDataset`]] | X-INFRA | DataSourceResource | cmpe:Dataset | Pending |
| [[V2 Object Property matchObject|`matchObject`]] | X-INFRA | EntityMatchAssertion | unspecified | Pending |
| [[V2 Object Property matchSubject|`matchSubject`]] | X-INFRA | EntityMatchAssertion | unspecified | Pending |
| [[V2 Object Property observationResultAbout|`observationResultAbout`]] | Core | ObservationResult | unspecified | Pending |
| [[V2 Object Property operates|`operates`]] | Core | Organization | cmpe:Facility | Pending |
| [[V2 Object Property operationFacility|`operationFacility`]] | Core | FacilityOperation | cmpe:Facility | Pending |
| [[V2 Object Property operationOrganization|`operationOrganization`]] | Core | FacilityOperation | cmpe:Organization | Pending |
| [[V2 Object Property presentationOf|`presentationOf`]] | Core | MedicinalProductPresentation | cmpe:MedicinalProduct | Pending |
| [[V2 Object Property producesObservationResult|`producesObservationResult`]] | Core | ObservationActivity | cmpe:ObservationResult | Pending |
| [[V2 Object Property registrationAuthority|`registrationAuthority`]] | Core | EstablishmentRegistration | cmpe:Organization | Pending |
| [[V2 Object Property registrationEntity|`registrationEntity`]] | Core | EstablishmentRegistration | unspecified | Pending |
| [[V2 Object Property registrationJurisdiction|`registrationJurisdiction`]] | Core | EstablishmentRegistration | cmpe:RegulatoryJurisdiction | Pending |
| [[V2 Object Property riskAssessmentConcerns|`riskAssessmentConcerns`]] | Extension | RiskAssessmentActivity | unspecified | Pending |
| [[V2 Object Property riskTreatmentAddresses|`riskTreatmentAddresses`]] | Extension | RiskTreatmentActivity | unspecified | Pending |
| [[V2 Object Property shortageJurisdiction|`shortageJurisdiction`]] | Core | MedicineShortageSituation | cmpe:RegulatoryJurisdiction | Pending |
| [[V2 Object Property shortagePresentation|`shortagePresentation`]] | Core | MedicineShortageSituation | cmpe:MedicinalProductPresentation | Pending |
| [[V2 Object Property shortageProduct|`shortageProduct`]] | Core | MedicineShortageSituation | cmpe:MedicinalProduct | Pending |
| [[V2 Object Property usedSourceArtifact|`usedSourceArtifact`]] | X-INFRA | ProvenanceActivity | unspecified | Pending |
| [[V2 Object Property withinCountry|`withinCountry`]] | X-INFRA | GeographicFeature | cmpe:Country | Pending |
| [[V2 Object Property withinRegion|`withinRegion`]] | X-INFRA | GeographicFeature | cmpe:AdministrativeRegion | Pending |

## Datatype-property reference — 5 properties
| Property | Domain | Range |
|---|---|---|
| [[V2 Datatype Property identifierLexicalValue|`identifierLexicalValue`]] | IdentifierAssignment | xsd:string |
| [[V2 Datatype Property measureNumericValue|`measureNumericValue`]] | ObservationResult | xsd:decimal |
| [[V2 Datatype Property measureUnitLabel|`measureUnitLabel`]] | ObservationResult | xsd:string |
| [[V2 Datatype Property validFrom|`validFrom`]] | unspecified | xsd:dateTime |
| [[V2 Datatype Property validTo|`validTo`]] | unspecified | xsd:dateTime |

## Generated vs curated boundary
The exhaustive tables/pages are generated for discoverability and coverage. Curated interpretation remains in [[V2 UFO and OntoUML Architecture]], [[V2 Formal Ontology and SHACL]], [[V2 Human Ontology Review|CM-PharmE 2.0 Semantic Review]] and cross-version research pages.

## Review boundary
Concept and relation review remains pending where the V2 review artifacts say pending. Generated presence is not approval. Accepted semantic findings later flow through #213 and trigger regeneration.

## Reference-generation evidence
See repository files:
- `wiki-src/ontology-reference/coverage.json`
- `wiki-src/ontology-reference/coverage.csv`
- `wiki-src/ontology-reference/MISSING-ITEMS.md`
- `wiki-src/ontology-reference/GENERATED-VS-CURATED.md`
- `wiki-src/ontology-reference/SOURCE-OF-TRUTH.md`

---

<details>
<summary>Documentation record</summary>

- **Page scope:** V2
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative source:** V2 conceptual registry, review passports/catalogs and formal ontology
- **Last synchronized:** 2026-09-24
- **Last synchronized ref:** v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999
- **Related issues/PRs:** #213, #234
- **Evidence status:** Generated exhaustive reference projection; semantic authority remains in V2 sources
- **Future refresh:** #213 / #214 as applicable
- **Wiki baseline:** WB-2026.09.1

</details>
