# W2 DOI-Backed Research Dataset Registry

## Admission principle
A DOI is valuable for reproducibility and citation, but it is not sufficient for admission. W2 also checks downloadability, reuse terms, schema/data dictionary, provenance, coverage, relation richness and fit to the approved demonstrators.

| ID | DOI | Dataset | Verified characteristics | Reuse/access status | Proposed role |
|---|---|---|---|---|---|
| D01 | 10.5281/zenodo.19160825 | NHIF Bulgaria Outpatient Pharmacy Reimbursement | 7,266,074 rows; 19 columns; Jul-2020–Dec-2025; all 28 NHIF regions; 3,367 medication codes; 526 ATC codes; regional/product/diagnosis/patient/package/cost/time dimensions; CSV + metadata dictionary | Zenodo description states CC BY 4.0 unless otherwise restricted by NHIF; downloadable ~1.7 GB dataset. Preserve original attribution/caveat. | **Primary discovery + implementation** for product/access/geography/time and RDB/KG ingestion |
| D02 | 10.5281/zenodo.19160637 | NHIF Bulgaria Inpatient Antineoplastic/Coagulopathy Medicines | Facility/hospital–product–diagnosis–month administrative reimbursement records; national/regional hospital context; CSV + variable metadata | Zenodo description states CC BY 4.0 unless otherwise specified; downloadable | **Primary discovery + implementation** for facility/product/geography/time/RDB |
| D03 | 10.5281/zenodo.15680002 | NHIF Bulgaria Individually Approved Medicines | Exception-based individually funded pharmaceutical treatments outside the standard Positive Drug List process | Downloadable; source/reuse metadata documented by Zenodo | **Supplemental held-out/access extension**; not institutionally independent of D01/D02 |
| D04 | 10.5281/zenodo.18851842 | Risk-Informed Data Analytics for Sustainable Pharmaceutical Supply | Real public oncology-hospital operational layers: consumption 2023–24, procurement lead times/arrivals, inventory/overstock, item master/price/formulation, stock parameters, stockout/operational-event and finance-related purchasing files; code included; no patient data | Files are downloadable. Record states files are released for “scientific and academic use,” but no standard open-data license was verified in W2. | **Conditional high-value resilience discovery/analysis source**. Raw redistribution in CM-PharmE release is prohibited until reuse terms are clarified. |
| D05 | 10.5281/zenodo.21456323 | Hospital Pharmacy Medication Supply under Demand Uncertainty | Empirical demand/cost data for 13 anonymized medicines across 48 months plus reproducible simulation/code | Downloadable; explicit standard license not verified in W2 source review | Exploratory/conditional forecasting and inventory-resilience source; not required if D04 is usable |

## DOI portfolio assessment
### Strongly admitted for W3/W6
- **D01** and **D02**: reproducible DOI anchors with rich relational/tabular structure and explicit metadata. They cover complementary outpatient regional and inpatient facility-level perspectives.

### Held-out / supplemental
- **D03**: useful for testing access/exception-treatment semantics but shares the NHIF institutional context with D01/D02; therefore it is not sufficient as the main independent external-generalizability dataset.

### Conditional
- **D04**: exceptionally useful for supply/resilience concept and relation discovery, but public redistribution rights are not sufficiently explicit for inclusion of raw files in a future open research package. It may be used for scholarly analysis under the stated scientific/academic-use condition while the license is clarified.
- **D05**: relevant to demand/inventory analytics but narrow and not currently needed for the principal article; retain as backup/future research.

## Licensing discipline
No raw dataset is copied into the public repository merely because it is downloadable. W6 ingestion uses download/ETL instructions, checksums and source citations; redistribution occurs only where the license explicitly permits it. For conditional datasets, derived schemas/ontology mappings may be documented without republishing restricted raw content, subject to the source terms.
