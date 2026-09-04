# CM-PharmE 2.0 Human Review — Concept Provenance and V1→V2 Evidence Matrix

Issue: #159  
Scope: CM-PharmE 2.0 only  
Review status: **Pending domain-by-domain author review**  
V1/main impact: **none**

## Purpose
This is the primary human-review matrix for the final 87-element V2 conceptual baseline. For each concept it records a concise working definition, OntoUML stereotype, V1 lineage, admitted evidence, held-out evidence where applicable, non-dataset support, and stable formal IRI.

Source presence is not treated as proof of ontological correctness. Dataset/official-source evidence shows that a distinction is present or operationally needed; UFO/OntoUML evidence supports the modeling treatment; held-out evidence records later representational fit.

## Review addresses
- V1 registry: [`../../../catalog/concepts.yaml`](../../../catalog/concepts.yaml)
- V1 concept pages: [`../../../docs/concepts/`](../../../docs/concepts/)
- V1→V2 migration: [`../w3/v1-v2-migration-matrix.md`](../w3/v1-v2-migration-matrix.md)
- V2 candidate definitions/evidence: [`../w3/candidate-concept-inventory.md`](../w3/candidate-concept-inventory.md)
- Evidence traceability: [`../w3/evidence-traceability.md`](../w3/evidence-traceability.md)
- W3→W4 transformation ledger: [`w3-w4-transformation-ledger.md`](w3-w4-transformation-ledger.md)
- Final conceptual specification: [`integrated-ontouml-model.md`](integrated-ontouml-model.md)
- Naming audit: [`concept-naming-audit.md`](concept-naming-audit.md)
- Visual review package: [`visual-ontology-package.md`](visual-ontology-package.md)
- Core OWL: [`../../ontology/source/modules/10-core.ttl`](../../ontology/source/modules/10-core.ttl)
- X-INFRA OWL: [`../../ontology/source/modules/20-xinfra.ttl`](../../ontology/source/modules/20-xinfra.ttl)
- Extensions OWL: [`../../ontology/source/modules/30-extensions.ttl`](../../ontology/source/modules/30-extensions.ttl)
- W2 source portfolio: [`../w2/gate-c-dataset-portfolio.md`](../w2/gate-c-dataset-portfolio.md)
- W1 literature/official sources: [`../w1/evidence-sources.md`](../w1/evidence-sources.md)
- Held-out E8 mapping: [`../../evaluation/results/e8-heldout-first-pass-mapping.csv`](../../evaluation/results/e8-heldout-first-pass-mapping.csv)

## Evidence codes
**P1** NHIF outpatient DOI 10.5281/zenodo.19160825; **P2** NHIF inpatient DOI 10.5281/zenodo.19160637; **P3** FDA DECRS + WDD/3PL; **P4** openFDA NDC + SPL; **P5** EMA Critical Medicines + shortage/ESMP; **P6** WHO Model List/eEML; **P7** GeoNames; **C1** pharma supply operations DOI 10.5281/zenodo.18851842 (conditional); **C2** EudraGMDP semantic/schema evidence (ingestion conditional); **S1** ChEMBL; **S2** NHIF Individually Approved Medicines; **S3** FAERS optional PV extension; **H1** ClinicalTrials/AACT held-out; **H2** openFDA Drug Shortages held-out; **H3** national EML held-out.

Non-dataset codes: **PR1** CM-PharmE 1.x; **M1** UFO foundational literature; **M2** OntoUML methodology/specification; **R1** UFO-grounded COVER/ROSE risk literature; **O1** FDA registration/listing; **O2** EudraGMDP; **O3** EMA ESMP/shortage; **O4** EMA Critical Medicines; **O5** WHO Essential Medicines; **O7** EudraVigilance/FAERS.

## Summary
- V1 concepts: **39**.
- Final V2 concepts: **87** = 32 Core + 25 X-INFRA + 30 Extensions.
- W3 migration accounted for all 39 V1 concepts: 15 materially contribute to Core/infrastructure patterns, 18 move to extensions, 6 are deferred/deprecated in generic or technology-specific form.
- W3 had 80 normalized candidates; W4 reached 87 through explicit foundational splits/truth-makers, not uncontrolled source expansion.

## 1. Ecosystem Organization
| # | V2 concept | Stereo | Working definition | V1 lineage / migration | Evidence | Held-out | Other support | IRI |
|---:|---|---|---|---|---|---|---|---|
|1|Organization|Kind|Institutional, legal, or social entity that can bear contextual pharmaceutical roles.|C0001/C0013/C0020/C0023 → refine/generalize|P2/P3/P4/P5/C2|H1 sponsor exact; H2 company exact|PR1/O1/O2/M1/M2|`cmpe:Organization`|
|2|Ecosystem Participant|RoleMixin|Anti-rigid participation pattern for entities participating in pharmaceutical ecosystem relations or activities.|C0003/C0008 → refine|P3–P6 + V1|—|PR1/M1/M2|`cmpe:EcosystemParticipant`|
|3|Regulatory Authority|Role|Role of an Organization when exercising regulatory authority in a jurisdiction.|C0023/C0024 → retain/refine|P3/P5/C2|—|PR1/O1/O2/M1/M2|`cmpe:RegulatoryAuthorityRole`|
|4|Manufacturer|Role|Role of an Organization responsible for pharmaceutical manufacturing or regulated manufacturing responsibility.|New|P3/C2|—|O1/O2/M1/M2|`cmpe:ManufacturerRole`|
|5|Importer|Role|Regulated role of an Organization importing pharmaceutical goods into a jurisdiction.|New|P3/C2|—|O1/O2/M1/M2|`cmpe:ImporterRole`|
|6|Product Responsible Organization|Role|Organization role responsible for product listing, labeling, or market responsibility in a source/jurisdiction.|New|P4/C2|—|O1/O2/M1/M2|`cmpe:ProductResponsibleLabelerRole`|
|7|Wholesale Distributor|Role|Regulated Organization role engaged in wholesale pharmaceutical distribution.|New|P3/C2|—|O1/O2/M1/M2|`cmpe:WholesaleDistributorRole`|
|8|Third-Party Logistics Provider|Role|Regulated Organization role providing third-party pharmaceutical logistics.|New|P3|—|O1/M1/M2|`cmpe:ThirdPartyLogisticsProviderRole`|

## 2. Facility Operations
|#|V2 concept|Stereo|Working definition|V1 lineage / migration|Evidence|Held-out|Other support|IRI|
|---:|---|---|---|---|---|---|---|---|
|9|Facility|Kind|Physical operational site distinct from the organization operating or owning it.|New|P2/P3/C2|H1 trial site exact|O1/O2/M1/M2|`cmpe:Facility`|
|10|Manufacturing Site|Role|Facility role when used or authorized for pharmaceutical manufacturing/processing.|New|P3/C2|—|O1/O2/M1/M2|`cmpe:ManufacturingSiteRole`|
|11|Distribution Site|Role|Facility role when used for distribution, storage, handling, or 3PL operations.|New|P3/C2|—|O1/O2/M1/M2|`cmpe:DistributionSiteRole`|
|12|Facility Operation|Relator|Relational entity grounding operational responsibility between Organization and Facility.|New W4 truth-maker|P2/P3/C2 inherited|—|M1/M2|`cmpe:FacilityOperation`|

## 3. Regulatory Governance
|#|V2 concept|Stereo|Working definition|V1 lineage / migration|Evidence|Held-out|Other support|IRI|
|---:|---|---|---|---|---|---|---|---|
|13|Establishment Registration|Relator|Regulatory relation connecting registered organization/facility with authority and jurisdiction.|C0004 broad → refine/split|P3|—|O1/M1/M2|`cmpe:EstablishmentRegistration`|
|14|Regulatory Authorization|Relator|Permission relation connecting authority, regulated party/activity, jurisdiction, and validity.|C0004 → refine/split|P3/C2|—|O1/O2/M1/M2|`cmpe:RegulatoryAuthorization`|
|15|Regulatory Jurisdiction|Kind|Legal/regulatory scope in which authorizations, requirements, roles, and classifications apply.|New|P3/P5/P6/C2|H3 exact with Country distinction|O1/O2/O4/O5/M1/M2|`cmpe:RegulatoryJurisdiction`|

## 4. Pharmaceutical Product
|#|V2 concept|Stereo|Working definition|V1 lineage / migration|Evidence|Held-out|Other support|IRI|
|---:|---|---|---|---|---|---|---|---|
|16|Medicinal Product|Kind|Pharmaceutical product identity represented across regulatory, access, shortage, and product-reference sources.|New|P1/P2/P4/P5/P6|H1 partial; H2 exact; H3 partial|O3/O4/O5/M1/M2|`cmpe:MedicinalProduct`|
|17|Pharmaceutical Substance|Kind|Medicinal/active substance identity distinct from product identity and presentation.|New|P1/P2/P4/P5/P6/S1|H1 partial; H2 exact; H3 partial|O4/O5/M1/M2|`cmpe:PharmaceuticalSubstance`|
|18|Medicinal Product Presentation|Kind|Independently identifiable marketed/presented configuration of a medicinal product.|New|P1/P2/P4/P5|H1 partial; H2 exact|O1/O3/O4/M1/M2|`cmpe:MedicinalProductPresentation`|
|19|Dosage Form Specification|Kind|Specification of pharmaceutical dosage form associated with a product presentation.|New|P4/P5/P6|H2 exact; H3 exact|O4/O5/M1/M2|`cmpe:DosageFormSpecification`|
|20|Strength|Quality|Quantitative strength/concentration characteristic borne by a product presentation.|New/W4 refine|P1/P2/P4/P5/P6|H2 exact; H3 exact|O4/O5/M1/M2|`cmpe:Strength`|
|21|Package Configuration|Kind|Packaging or pack-quantity configuration associated with a product presentation.|New|P1/P2/P4|H2 partial|O1/M1/M2|`cmpe:PackageConfiguration`|
|22|Product Classification Scheme|Kind|Identified vocabulary/scheme used to classify products or substances.|New W4 split|P1/P2/P4/P5|H2 exact; H3 exact|O4/O5/M1/M2|`cmpe:ProductClassificationScheme`|
|23|Classification Entry|Kind|Identified category/entry within a classification scheme.|New W4 split|P1/P2/P4/P5|H2 exact; H3 exact|O4/O5/M1/M2|`cmpe:ClassificationEntry`|
|24|Product Classification Assignment|Relator|Contextual assignment connecting a product/substance to a classification entry.|New W4 split|P1/P2/P4/P5|H2 exact; H3 partial|O4/O5/M1/M2|`cmpe:ProductClassificationAssignment`|
|25|Market Listing|Relator|Contextual relation that a product presentation is listed/marketed under source, jurisdiction, responsibility, and time conditions.|New W4 refine|P4|H2 partial|O1/M1/M2|`cmpe:MarketListing`|

## 5. Supply Operations
|#|V2 concept|Stereo|Working definition|V1 lineage / migration|Evidence|Held-out|Other support|IRI|
|---:|---|---|---|---|---|---|---|---|
|26|Manufacturing Activity|Event|Occurrence of pharmaceutical manufacturing/processing involving relevant actors, sites, products, or substances.|C0015 → refine/split|P3/C2|—|PR1/O1/O2/M1/M2|`cmpe:ManufacturingActivity`|
|27|Pharmaceutical Logistics Activity|Event|Occurrence of pharmaceutical distribution, storage, handling, or logistics activity.|C0015/C0032 → refine/split|P3/C2|—|PR1/O1/O2/M1/M2|`cmpe:DistributionLogisticsActivity`|
|28|Medicine Shortage Situation|Situation|Time-, source-, and jurisdiction-bounded state of insufficient/unavailable medicine supply.|New|P5|H2 exact|O3/O4/M1/M2|`cmpe:MedicineShortageSituation`|
|29|Supply Capacity|Mode|Disposition/capacity inhering in an organization or facility to provide, manufacture, or supply medicines.|C0011 → refine/split|P5/C1|—|PR1/O3/O4/M1/M2|`cmpe:SupplyCapacity`|

## 6. Ecosystem Observation
|#|V2 concept|Stereo|Working definition|V1 lineage / migration|Evidence|Held-out|Other support|IRI|
|---:|---|---|---|---|---|---|---|---|
|30|Availability Observation Result|Subkind|Persistent information object recording observed/reported medicine availability in context.|New|P5/ESMP + P1/P2 context|H2 partial|O3/M1/M2|`cmpe:AvailabilityObservationResult`|
|31|Demand Observation Result|Subkind|Information object recording measured/reported demand, consumption, or demand-related evidence.|C0010 → refine|P5/ESMP/C1/P1/P2|—|PR1/O3/M1/M2|`cmpe:DemandObservationResult`|
|32|Supply Capacity Observation Result|Subkind|Information object recording evidence or assessment about supply capacity.|C0011 → refine/split|P5/ESMP/C1|—|PR1/O3/M1/M2|`cmpe:SupplyCapacityObservationResult`|

## 7. Spatiotemporal Context
|#|V2 concept|Stereo|Working definition|V1 lineage / migration|Evidence|Held-out|Other support|IRI|
|---:|---|---|---|---|---|---|---|---|
|33|Geographic Feature|Kind|Identified geographic place/feature used to contextualize facilities, organizations, observations, and events.|New|P7 + native locations|H1 exact|O1/O2/M1/M2|`cmpe:GeographicFeature`|
|34|Administrative Region|Subkind|Administrative/reporting area specialized from Geographic Feature.|New|P1/P2/P7|—|M1/M2|`cmpe:AdministrativeRegion`|
|35|Country|Subkind|Country-level geographic/political reference specialized from Geographic Feature.|New|P3/P5/P7|H1 exact; H3 exact|O1/O4/M1/M2|`cmpe:Country`|
|36|Geospatial Position|Datatype|Coordinate/geometry value used to locate a feature or facility.|New infrastructure|P7|—|M2|`cmpe:GeospatialPosition`|
|37|Address|Datatype|Structured/textual location description used for organization/facility location and entity resolution.|New|P3/C2|—|O1/O2|`cmpe:Address`|
|38|Time Interval|Datatype|Temporal extent qualifying validity, shortage, observation, activity, or context.|New infrastructure|P1/P2/P3/P5|H2 partial|M1/M2|`cmpe:TimeInterval`|
|39|Reporting Period|Datatype|Source-defined period over which aggregate values, observations, or reports apply.|New|P1/P2/P5|—|M2|`cmpe:ReportingPeriod`|

## 8. Evidence Traceability
|#|V2 concept|Stereo|Working definition|V1 lineage / migration|Evidence|Held-out|Other support|IRI|
|---:|---|---|---|---|---|---|---|---|
|40|Data Source|Kind|Information resource/source artifact from which datasets, records, or evidence are obtained.|C0038 broad → generalize|All source families|—|PR1/M2|`cmpe:DataSourceResource`|
|41|Dataset|Kind|Organized data collection admitted or referenced by the research program.|C0038 broad → generalize/new|P1/P2/C1/S1/S2|—|M2|`cmpe:Dataset`|
|42|Dataset Release|Kind|Identified dataset version/snapshot used for reproducible analysis.|C0038 broad → new infrastructure|P1–P7|H3 exact list/version support|M2|`cmpe:DatasetRelease`|
|43|Source Record|Kind|Identifiable row, entry, document, or source record from which assertions/mappings derive.|New|P1–P5|H2 partial|M2|`cmpe:SourceRecord`|
|44|Assertion|Kind|Information object representing a proposition in research, mapping, provenance, or KG layers.|New|Demonstrator C/all mappings|H2 partial|M1/M2|`cmpe:Assertion`|
|45|Observation Activity|Event|Occurrence in which observation, measurement, reporting, or evidence-production takes place.|New W4 split|P1/P2/P5/C1 inherited|—|M1/M2|`cmpe:ObservationActivity`|
|46|Observation Result|Kind|Persistent information object produced by/representing an observation and carrying values/context.|New W4 split|P1/P2/P5/C1|H1 partial|M1/M2|`cmpe:ObservationResult`|
|47|Measure Value|Datatype|Numeric, coded, monetary, count, or quantity value associated with an observation result.|New|P1/P2/C1/P4|H1 partial|M2|`cmpe:MeasureValue`|
|48|Evidence Item|RoleMixin|Role borne by an information object when serving as evidence for an assertion, mapping, or decision.|C0038 broad → generalize/W4 refine|Research traceability/all sources|—|M1/M2|`cmpe:EvidenceItem`|
|49|Evidence Support|Relator|Relation grounding that an evidence item supports an assertion or model claim.|New W4 truth-maker|Research traceability/all sources|—|M1/M2|`cmpe:EvidenceSupport`|
|50|Mapping Assertion|Subkind|Assertion stating an explicit source-to-canonical semantic mapping.|New|Demonstrator C|—|M2|`cmpe:MappingAssertion`|
|51|Provenance Activity|Event|Ingestion, transformation, normalization, or mapping activity generating derived artifacts/assertions.|New|Demonstrator C|H2 partial temporal/provenance support|M2|`cmpe:ProvenanceActivity`|
|52|Data Quality Finding|Subkind|Assertion recording validation, quality, anomaly, or conformance findings about data/mappings.|C0034 → generalize|W1/W2/W3 methodology|—|PR1/M2|`cmpe:DataQualityFinding`|

## 9. Entity Identity
|#|V2 concept|Stereo|Working definition|V1 lineage / migration|Evidence|Held-out|Other support|IRI|
|---:|---|---|---|---|---|---|---|---|
|53|Identifier Value|Datatype|Symbolic identifier value under a defined scheme; not itself entity identity.|New W4 refine|P1–P7/C2/S1|H2 exact with presentation identity|M1/M2|`cmpe:IdentifierValue`|
|54|Identifier Scheme|Kind|Information object defining identifier scope, issuer, semantics, or syntax.|New|P1–P7/S1|—|M2|`cmpe:IdentifierScheme`|
|55|Identifier Assignment|Relator|Relation connecting entity, identifier value, scheme, and optional source/validity context.|New|Cross-source identity requirement|H2 exact|M1/M2|`cmpe:IdentifierAssignment`|
|56|Entity Match Assertion|Subkind|Assertion that source representations correspond to the same or related real-world entity.|New|P3/P4/P7 overlap + W1 need|—|M2|`cmpe:EntityMatchAssertion`|
|57|Match Confidence|Quality|Quality expressing confidence or ambiguity attached to an entity-match assertion.|New W4 refine|Entity-resolution design|—|M1/M2|`cmpe:MatchConfidence`|

## 10. Regulatory Policy
|#|V2 concept|Stereo|Working definition|V1 lineage / migration|Evidence|Held-out|Other support|IRI|
|---:|---|---|---|---|---|---|---|---|
|58|Regulatory Requirement|Kind|Normative information object expressing a regulatory obligation/rule applicable in context.|C0027; broader C0036 lineage → refine|P3/P5/C2|—|PR1/O1/O2/O4/M1/M2|`cmpe:RegulatoryRequirement`|
|59|Regulatory Oversight|Relator|Relationship connecting authority with supervised organization/party under requirements/jurisdiction.|C0004 → retain/refine|P3/C2|—|PR1/O1/O2/M1/M2|`cmpe:RegulatoryOversight`|

## 11. Supply Resilience
|#|V2 concept|Stereo|Working definition|V1 lineage / migration|Evidence|Held-out|Other support|IRI|
|---:|---|---|---|---|---|---|---|---|
|60|Contextual Medicine Classification Assignment|Relator|Contextual assignment of a medicine to a policy/resilience classification in list/jurisdiction/version context.|New W4 parent|P5/P6|H3 exact/partial|O4/O5/M1/M2|`cmpe:ContextualMedicineClassificationAssignment`|
|61|Essential Medicine Classification Assignment|Subkind|Assignment stating that a medicine is essential under a defined list, jurisdiction, and version.|New|P6|H3 exact|O5/M1/M2|`cmpe:EssentialMedicineClassification`|
|62|Critical Medicine Classification Assignment|Subkind|Assignment stating that a medicine is critical under a defined regulatory/policy context.|New|P5|—|O4/M1/M2|`cmpe:CriticalMedicineClassification`|
|63|Alternative Medicinal Product|Role|Anti-rigid role of a product/presentation designated as an alternative in context.|New|P5/P6|—|O4/O5/M1/M2|`cmpe:AlternativeMedicinalProductRole`|
|64|Alternative Medicinal Product Assignment|Relator|Relation grounding designation of one medicinal product as an alternative to another.|New W4 truth-maker|P5/P6|—|O4/O5/M1/M2|`cmpe:AlternativeMedicineAssignment`|
|65|Supply Dependency|Relator|Contextual dependency among actors, facilities, products, or supply arrangements.|C0032 generic predecessor → refine/split|P5/C1/W1|—|O4/R1/M1/M2|`cmpe:SupplyDependency`|
|66|Disruption Event|Event|Occurrence disrupting or threatening normal pharmaceutical supply/availability.|C0028 indirect lineage|W1/P5/C1|—|O1/O4/R1/M1/M2|`cmpe:DisruptionEvent`|
|67|Inventory Observation Result|Subkind|Observation result recording inventory/stock information in operational context.|New conditional|C1|—|M2|`cmpe:InventoryObservationResult`|
|68|Procurement Activity|Event|Occurrence of pharmaceutical procurement/acquisition in a supply context.|C0015 broad → split|C1|—|M1/M2|`cmpe:ProcurementActivity`|
|69|Lead Time Observation Result|Subkind|Observation result recording procurement/replenishment/delivery lead-time information.|New conditional|C1|—|M2|`cmpe:LeadTimeObservationResult`|
|70|Stockout Situation|Situation|State in which required pharmaceutical stock is unavailable in operational context.|New conditional|C1 + P5 framing|—|O3/O4/M1/M2|`cmpe:StockoutSituation`|

## 12. Market Access
|#|V2 concept|Stereo|Working definition|V1 lineage / migration|Evidence|Held-out|Other support|IRI|
|---:|---|---|---|---|---|---|---|---|
|71|Healthcare Financing Organization|Role|Organization role acting as payer, funder, or healthcare-financing actor in access/reimbursement.|New extension|P1/P2/S2|—|M1/M2|`cmpe:PayerFundingOrganizationRole`|
|72|Reimbursement and Utilization Observation Result|Subkind|Observation result recording reimbursement and/or utilization evidence in defined population/period/access context.|New extension|P1/P2/S2|—|M2|`cmpe:ReimbursementUtilisationObservationResult`|
|73|Diagnosis Classification Reference|Kind|Information object representing diagnosis code/category used to contextualize utilization/access evidence.|New extension|P1/P2|H1 partial|M2|`cmpe:DiagnosisClassificationReference`|

## 13. Risk Management
|#|V2 concept|Stereo|Working definition|V1 lineage / migration|Evidence|Held-out|Other support|IRI|
|---:|---|---|---|---|---|---|---|---|
|74|Asset at Risk|RoleMixin|Role borne by an entity when treated as an asset exposed to risk in an assessment context.|C0028 indirect → W4 adapter|V1/W1 risk evidence|—|R1/M1/M2|`cmpe:AssetAtRisk`|
|75|Risk Assessment Activity|Event|Occurrence in which risk, vulnerability, exposure, or consequence is assessed.|C0028 → refine/split|V1/W1|—|R1/PR1/M1/M2|`cmpe:RiskAssessmentActivity`|
|76|Vulnerability|Mode|Susceptibility/disposition of an asset/bearer making adverse outcomes possible under conditions.|C0028 broad → explicit|W1 risk alignment|—|R1/M1/M2|`cmpe:Vulnerability`|
|77|Risk Treatment Plan|Kind|Normative information object specifying intended actions/controls for addressing risk/vulnerability.|C0028 broad → W4 split|W1/V1|—|R1/M1/M2|`cmpe:RiskTreatmentPlan`|
|78|Risk Treatment Activity|Event|Occurrence executing a planned risk treatment, mitigation, prevention, or control.|C0028 → refine/split|W1/V1|—|R1/M1/M2|`cmpe:RiskTreatmentActivity`|

## 14. Pharmacovigilance
|#|V2 concept|Stereo|Working definition|V1 lineage / migration|Evidence|Held-out|Other support|IRI|
|---:|---|---|---|---|---|---|---|---|
|79|Pharmacovigilance Requirement|Kind|Normative information object expressing a pharmacovigilance obligation/requirement.|C0036 → retain/refine|V1 + optional S3|—|PR1/O7/M1/M2|`cmpe:PharmacovigilanceRequirement`|
|80|Adverse Event Reporting Activity|Event|Occurrence of reporting an adverse event through a pharmacovigilance process/system.|C0022 → refine|V1 + optional S3|—|PR1/O7/W1-S11/W1-S12/M1/M2|`cmpe:AdverseEventReportingActivity`|
|81|Post-Market Surveillance Activity|Event|Occurrence of monitoring/surveillance performed after a medicinal product is marketed.|C0037 → retain/refine|V1 + optional S3|—|PR1/O7/W1-S11/M1/M2|`cmpe:PostMarketSurveillanceActivity`|

## 15. Business Architecture
|#|V2 concept|Stereo|Working definition|V1 lineage / migration|Evidence|Held-out|Other support|IRI|
|---:|---|---|---|---|---|---|---|---|
|82|Business Architecture View|Kind|Information object representing optional Business Architecture analysis over ecosystem entities/capabilities.|V1 BA-informed architecture → moved to view|V1/W1|—|PR1/M2|`cmpe:BusinessArchitectureView`|
|83|Enterprise Capability|Mode|Organizational disposition/capability represented in the optional BA view.|C0005 → retain in extension|V1|—|PR1/M1/M2|`cmpe:EnterpriseCapability`|
|84|Strategic Partnership Agreement|Relator|Commitment-bearing partnership relation connecting organizations in strategic collaboration.|C0014 → retain in extension|V1/W1|—|PR1/M1/M2|`cmpe:StrategicPartnershipAgreement`|
|85|Service Offering Specification|Kind|Information object describing a service offering in the optional business/application view.|C0039 → retain/move|V1|—|PR1/M2|`cmpe:ServiceOfferingSpecification`|

## 16. Digital Systems
|#|V2 concept|Stereo|Working definition|V1 lineage / migration|Evidence|Held-out|Other support|IRI|
|---:|---|---|---|---|---|---|---|---|
|86|Digital System Component|Kind|Generic digital/information-system component used in ecosystem applications without technology-specific Core commitment.|C0029/C0030/C0031/C0033/C0035/C0038 → generalize/deprecate specific forms|V1 lineage|—|PR1/M2|`cmpe:DigitalInformationSystemComponent`|

## 17. Clinical Care
|#|V2 concept|Stereo|Working definition|V1 lineage / migration|Evidence|Held-out|Other support|IRI|
|---:|---|---|---|---|---|---|---|---|
|87|Clinical Care Participant|RoleMixin|Contextual role family for persons/organizations participating in clinical care relevant to pharmaceutical use/access.|C0007/C0017/C0019/C0021 → consolidate/move to extension|V1 only at admission|H1 shows extension pressure|PR1/M1/M2|`cmpe:ClinicalCareParticipant`|

## Explicit gaps for human review
1. Concept-level external ontology/literature comparison is **not yet complete for every one of the 87 concepts**. The repository has strong source/dataset traceability and strong UFO/OntoUML methodology, but row-by-row external ontology comparison remains a literature-review task. Do not silently infer it.
2. C1-dependent supply concepts (Inventory Observation Result, Procurement Activity, Lead Time Observation Result, detailed stockout semantics) remain conditional.
3. H1 shows that the principal ontology intentionally lacks detailed Clinical Study, Outcome, Arm/Group, Phase/Status, and associated study relations; these are extension pressure, not Core defects.
4. Market Access evidence is mainly NHIF-family and institutionally concentrated.
5. Risk Management is modular and aligned to COVER/ROSE patterns; it is not claimed as an independently validated pharmaceutical risk ontology.
6. Entity matching has structural semantics, but real-world matching accuracy is a separate measured task.

## Human review workflow
For each domain, the author should decide one of: **APPROVE**, **APPROVE WITH WORDING CHANGE**, **REVISE SEMANTICS**, **SPLIT/MERGE**, **MOVE DOMAIN/MODULE**, or **DEFER**. Review the definition, stereotype, V1 migration, dataset evidence, non-dataset support, and evidence boundary independently. Any semantic change after Gate D should become a V2 design-decision issue before OWL/SHACL is changed.

## Boundary
This file is V2-only. It does not modify CM-PharmE 1.x, the reviewer-facing manuscript, V1 concept pages, or `main`. Working definitions are synthesized from W3 evidence roles and W4 semantic commitments and are not claimed to be external normative definitions unless an external source is explicitly identified.