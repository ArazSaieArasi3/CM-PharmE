# W3 Source-Schema Concept Extraction

## Purpose
Translate Gate C discovery evidence into normalized **candidate semantics** without treating database columns as ontology classes by default. A field becomes a concept/relation candidate only when it represents a persistent domain distinction, contextual role, event/situation, observation, classification, identifier, or relationship needed by the approved research questions/demonstrators.

## P1 — NHIF Outpatient DOI 10.5281/zenodo.19160825
Empirical unit: aggregated region–product–diagnosis–period/part reimbursement observation.

Source structures → candidate semantics:
- `region_num`, `region_name` → Administrative Region / Regional Identifier / geographic scope.
- `atc_code`, `atc_name` → Product/Substance Classification + Classification Identifier; ATC is not a medicinal-product identity.
- `nhif_code` → source-scoped Medicinal Product/Reimbursable Item Identifier.
- `market_name` → marketed/product name lexicalization; not identity by itself.
- `packaging`, `num_in_pack` → Package Configuration / quantity attributes.
- `concentration` → Strength/Concentration Specification.
- `icd_code`, `icd_name` → Diagnosis Classification reference; market-access extension, not Core product identity.
- `patients_num` → Aggregate Patient Count measure; **not Individual Patient**.
- `pack_num` → Dispensed/Reimbursed Package Count measure.
- `costs`, `currency`, `costs_bgn`, `costs_eur` → Reimbursement/Expenditure Measure + Currency.
- `period`, `part` → Reporting Period / source partition context.

Candidate observation structure:
`Reimbursement/Utilisation Observation → about Product → in Region → for Diagnosis Classification → during Reporting Period → has Aggregate Measures`.

## P2 — NHIF Inpatient DOI 10.5281/zenodo.19160637
Empirical unit: aggregated facility–product–diagnosis–month reimbursement observation.

Source structures → candidate semantics:
- `hospital_code`, `hospital_name` → Healthcare Facility/Site + source-scoped Facility Identifier.
- product/ATC/packaging/concentration fields → same normalized product semantics as P1.
- diagnosis fields → Diagnosis Classification reference.
- patient/package/expenditure fields → aggregate measures.
- `period` → Reporting Period.

Key discovery consequence:
**Organization and Facility/Site must not be conflated.** A hospital-coded unit is evidence for a facility/site identity layer; the organization that operates it may require a separate record/mapping.

## P3a — FDA DECRS
Source purpose: currently registered drug establishments involved in manufacturing/preparing/propagating/compounding/processing drugs distributed in or imported to the U.S.

Candidate semantics:
- Organization / Establishment operator.
- Drug Establishment / Physical Site.
- Establishment Registration.
- Registration Status and Validity/Reporting Time.
- Business/Operational Role performed at an Establishment.
- Address / Geographic Location.
- Regulatory Jurisdiction.
- Source-scoped Establishment/Registration Identifier.

Boundary:
Registration is evidence of a registration status, not a universal assertion of product approval or regulatory compliance.

## P3b — FDA Wholesale Drug Distributor / Third-Party Logistics Provider reporting
Source purpose: facility-level wholesale-distributor and 3PL annual/license reporting.

Candidate semantics:
- Wholesale Distributor Role.
- Third-Party Logistics Provider Role.
- Facility/Site.
- License / Regulatory Registration.
- Licensing/Reporting Jurisdiction.
- License Validity/Status.

Key discovery consequence:
Because one facility may have multiple licenses, **Facility ≠ License** and **Organization/Site ≠ Role**. Regulatory permission/registration should be represented as a distinct relationship/status-bearing entity or record candidate, subject to W4 analysis.

## P4a — openFDA NDC
Source purpose: marketed/listed drug product and package information with harmonized identifiers.

Candidate semantics:
- Medicinal Product / Marketed Product Presentation.
- Product Name / lexical designation.
- Pharmaceutical Substance / Active Ingredient.
- Dosage Form.
- Route of Administration (candidate product-use/formulation extension).
- Strength/Concentration Specification.
- Package Configuration / Package Identifier.
- Product Listing / Marketing Status.
- Labeler/Responsible Organization Role.
- Marketing Category / Application reference.
- Product Classification.
- Identifier Scheme and Identifier values: Product NDC, Package NDC, SPL ID/Set ID, Application Number, UNII, RxCUI and other source/harmonized identifiers.

Boundary:
An NDC listing is a source-specific marketed/listed-product assertion and must not be treated as universal product identity or proof of approval.

## P4b — FDA / openFDA SPL
Source purpose: Structured Product Labeling submissions with product, label and facility/organization information.

Candidate semantics:
- Product Label / Labeling Artifact.
- Label/Submission Version.
- Submitting/Authoring Organization Role.
- Product↔Label relation.
- Product/Organization/Site identifiers.
- Source Record / Submission Record.

Boundary:
SPL can support product/facility linkage where explicit, but it is not evidence of a complete global supply relationship.

## P5a — EMA Union List of Critical Medicines
Source purpose: EU context-specific list of medicines whose continued supply is prioritized; list is revised over time.

Candidate semantics:
- Critical Medicine Classification/Status.
- Classification Scheme/List and List Version.
- Jurisdiction/Policy Context.
- Product/Substance/Medicine group to which classification applies.
- Alternative/Therapeutic alternative evidence where present.
- Classification Validity/Publication Time.

Key discovery consequence:
**Critical Medicine is not assumed to be a rigid medicinal-product kind.** It is a contextual classification/status tied to list, jurisdiction and version; final UFO treatment is W4 work.

## P5b — EMA Medicine Supply Shortages JSON
Source structures include medicine affected, shortage status, INN/common name, therapeutic area, affected forms/strengths, alternatives, shortage start/resolution, first-publication and last-update dates.

Candidate semantics:
- Medicine Shortage Situation/Event/Case.
- Shortage Status.
- Affected Medicinal Product/Substance/Presentation.
- Affected Dosage Form.
- Affected Strength.
- Alternative Medicinal Product / Alternative Supply Option relation.
- Shortage Time Interval.
- Publication/Update Time.
- Reporting/Regulatory Source.
- Therapeutic Classification/Area reference.

Key discovery consequence:
Shortage is time-bounded and source/jurisdiction-contextual. It should not be modeled as a permanent quality of a product.

## P5c — EMA ESMP reporting semantics
Schema/methodological evidence only; not bulk empirical data.

Candidate semantics:
- Supply Observation.
- Demand Observation.
- Availability Observation.
- Shortage Report.
- Reporting Organization Role (e.g., MAH/NCA context).
- Reporting Period and Jurisdiction.

## P6 — WHO Model List / eEML
Candidate semantics:
- Essential Medicine Classification/Status.
- Essential Medicines List / List Version.
- Indication reference.
- Formulation / Dosage Form / Strength where available.
- Alternative medicine/formulation relationship where supported.
- Global/reference policy context.

Key discovery consequence:
Essentiality is context-sensitive and list/version-dependent. It is not treated as an intrinsic permanent kind of drug/substance.

## P7 — GeoNames
Normalization-only structures:
- Geographic Feature.
- Administrative Region.
- Country.
- Geospatial Position (latitude/longitude).
- Geographic Identifier (GeoNames ID).
- Alternative Geographic Name.
- Geographic Hierarchy / containment.

Boundary:
GeoNames supports identity/normalization and geospatial representation. It is **not** evidence for admitting pharmaceutical-domain actors, products, processes or relationships.

## C1 — Supply-operations DOI 10.5281/zenodo.18851842 (conditional)
Use only within verified scientific/academic terms; raw files are not redistributed.

Metadata/schema signals → candidate semantics:
- Pharmaceutical Item/Product.
- Inventory Observation / Inventory State.
- Consumption/Demand Observation.
- Procurement Activity / Procurement Channel.
- Purchase/Arrival Event.
- Lead-Time Observation.
- Stock Parameter / Reorder Policy observation.
- Stockout Event.
- Cost/Price Observation.
- Supplier/Procurement Relationship where explicitly present.
- Operational Exception/Event.

Boundary:
This single-institution operational dataset supports richer resilience semantics but cannot justify a complete global supplier→buyer→shipment ontology by itself.

## C2 — EudraGMDP (conditional automated ingestion; public semantic evidence allowed)
Candidate semantics:
- Manufacturer / Importer / Active-Substance Manufacturer/Importer/Distributor roles.
- Wholesale Distribution Role.
- Manufacturing/Import Authorisation.
- GMP/GDP Certificate/Status evidence.
- Organization.
- Site/Location.
- Regulatory Authority / Jurisdiction.

## S1 — ChEMBL 37 (secondary enrichment)
Candidate enrichment semantics:
- Chemical/Pharmaceutical Substance identity.
- Molecule/Compound Identifier / Synonym.
- Cross-reference.

Boundary:
Bioactivity/target assay structures do not enter the Core unless a later use case explicitly activates a drug-discovery extension.

## S2 — NHIF Individually Approved Medicines
Candidate extension semantics:
- Exceptional/Individual Funding or Access Decision/Record.
- Product.
- Payer/Funding Organization Role.
- Decision/Validity Time.
- Jurisdiction.

## S3 — openFDA FAERS
Optional pharmacovigilance extension only; not Core driver.

## Protected held-out sources
H1 ClinicalTrials.gov/AACT, H2 openFDA Drug Shortages and H3 selected national EML schemas are intentionally absent from the extraction tables above. No candidate is admitted because one of those schemas contains a field or table.

## Extraction conclusion
The admitted discovery sources consistently require a V2 conceptual layer centered on **products/substances, organizations and contextual roles, physical sites/facilities, regulatory permissions/status, geography and jurisdiction, temporal events/situations, observations/measures, identifiers, and evidence/provenance**. Market-access, detailed supply operations, safety, risk/resilience, business architecture and digital-health semantics are better handled as modular extensions unless W3/W4 evidence establishes otherwise.
