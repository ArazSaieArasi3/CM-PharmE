# W2 Manuscript Notes — Dataset Landscape and Admission Protocol

Status: working manuscript evidence for later drafting; not a completed-results section.

## Research-design contribution
CM-PharmE 2.0 uses a **role-separated, multi-source data design** rather than treating one dataset as the ontology specification. W2 distinguishes:
1. DOI-backed research datasets for reproducible empirical anchoring;
2. authoritative operational/regulatory sources for current domain structures and identifiers;
3. conditional sources with useful semantics but unresolved reuse/ingestion constraints;
4. secondary enrichment sources;
5. protected held-out source families reserved before concept discovery.

## Admission protocol
Candidate sources are scored on stable identity/authority, legal reuse, reproducible access, schema documentation, provenance, geography, temporal coverage, identifier quality, relationship richness, Gate B demonstrator fit and reproducibility packaging. Hard exclusions prevent inaccessible, legally unusable, non-reproducible or ethically unsuitable data from becoming primary empirical anchors.

## DOI-backed empirical anchors identified
Two NHIF Bulgaria datasets are proposed as primary DOI-backed anchors:
- outpatient pharmacy reimbursement — DOI 10.5281/zenodo.19160825;
- inpatient antineoplastic/coagulopathy medicine reimbursement — DOI 10.5281/zenodo.19160637.

They provide large, structured, documented product/geography/time and facility/product data suitable for later RDB/KG mapping. Their common Bulgarian/NHIF origin is an explicit limitation; they are not used as evidence of cross-jurisdiction generalizability by themselves.

## Operational-source strategy
FDA, EMA and WHO sources are proposed for product/site/logistics/shortage/criticality/essential-medicine semantics and identifiers. GeoNames is used only for geographic normalization. ChEMBL is secondary substance/identifier enrichment rather than evidence of ecosystem supply relationships.

## Held-out design
Before W3 concept discovery, the following source families are proposed as protected held-out evidence:
- ClinicalTrials.gov/AACT for organization/site/location/intervention relational generalizability;
- openFDA Drug Shortages as a U.S. cross-jurisdiction test after EU shortage/criticality semantics are discovered primarily from EMA evidence;
- a small, separately audited set of WHO national essential-medicine lists for jurisdiction-sensitive essentiality/criticality testing.

This is not a fully blind external evaluation: W2 records high-level feasibility and source existence. The protection rule is narrower and auditable — **W3 must not use held-out schemas to justify Core concept/relation admission**.

## Important negative finding
W2 did not identify a single openly reusable global source that exposes a complete product-level supplier→buyer→shipment pharmaceutical network. Regulatory sources are strong for establishments, authorizations, shortages and trading-partner roles, while the richest operational supply dataset found has conditional reuse wording. Therefore the manuscript must avoid claims of complete global supply-chain reconstruction.

## Conditional supply dataset
DOI 10.5281/zenodo.18851842 is highly relevant to procurement, inventory, lead time, stockout and resilience semantics, but the available record uses “scientific and academic use” wording rather than a standard open-data license. It may support analysis/concept discovery within those terms, but raw-data redistribution in the CM-PharmE research package remains prohibited unless terms are clarified.

## Expected manuscript use
W2 can support the Research Design / Dataset Admission subsection and motivate why V2 combines DOI-backed data, operational sources and held-out evidence. It must not yet claim successful ontology coverage, mapping accuracy, cross-jurisdiction generalizability or application performance; those results belong to W3–W7.
