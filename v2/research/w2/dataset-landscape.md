# W2 Comprehensive Pharmaceutical Dataset and Source Landscape

Snapshot date: 2026-08-18.

## Scope rule
This inventory is intentionally broader than the final admitted portfolio. It covers sources that may inform W3 discovery, W6 implementation, W7 evaluation or future extensions. A source appearing here is **not automatically admitted**.

| ID | Source | Type | Main coverage | Access / structure | W2 role signal |
|---|---|---|---|---|---|
| D01 | NHIF Bulgaria Outpatient Pharmacy Reimbursement, DOI 10.5281/zenodo.19160825 | DOI-backed research dataset derived from official NHIF reporting | Product, ATC/INN, region, diagnosis, patients, packages, reimbursement, time | Downloadable CSV + metadata dictionary; 7,266,074 rows, 19 columns, Jul-2020–Dec-2025, 28 regions | Strong primary discovery/implementation candidate for product/access/geography/time/RDB |
| D02 | NHIF Bulgaria Inpatient Antineoplastic/Coagulopathy Medicines, DOI 10.5281/zenodo.19160637 | DOI-backed research dataset derived from official NHIF reporting | Hospital/facility, product, diagnosis, region, patients, expenditure, time | Downloadable CSV + variable metadata; facility–product–diagnosis–month observations | Strong primary candidate for facility/product/geography/RDB |
| D03 | NHIF Bulgaria Individually Approved Medicines, DOI 10.5281/zenodo.15680002 | DOI-backed research dataset | Individually funded therapies outside standard list/process | Downloadable dataset | Supplemental/held-out access/reimbursement candidate; institutionally related to D01/D02 |
| D04 | Risk-Informed Data Analytics for Sustainable Pharmaceutical Supply, DOI 10.5281/zenodo.18851842 | DOI-backed operational research dataset | Inventory, consumption, procurement lead times, arrivals, price, stock parameters, stockouts/operational events | Downloadable multi-file Excel + code; real public oncology hospital data; use wording is scientific/academic rather than a standard open license | High semantic richness for supply/resilience; **conditional** until redistribution/reuse terms are clarified |
| D05 | Hospital Pharmacy Medication Supply under Demand Uncertainty, DOI 10.5281/zenodo.21456323 | DOI-backed research dataset | 13 anonymized medicines, 48-month demand/cost, inventory decision simulation | Downloadable data + reproducible code/simulation | Exploratory resilience/forecasting candidate; license requires explicit verification before admission |
| O01 | FDA DECRS | Authoritative operational source | Current drug establishments that manufacture/prepare/compound/process drugs distributed in/imported to U.S. | FDA search + downloadable ZIP; current registration status | Strong organization/site/facility source for geospatial demonstrator |
| O02 | FDA Wholesale Drug Distributor / 3PL annual reporting database | Authoritative operational source | Facility-level wholesale-distributor and 3PL licenses/annual reports | Search + downloadable database; updated every business day | Strong distributor/logistics-role/site source |
| O03 | openFDA NDC | Authoritative operational source | Marketed drug products, product/package identifiers, brand/generic, ingredients, form/route and harmonized identifiers | API/download; daily updates; public-domain/CC0 openFDA data family | Strong product/identifier enrichment and cross-source linking |
| O04 | FDA/openFDA Structured Product Labeling (SPL) | Authoritative operational source / standard-format submissions | Product labeling plus product/facility information in HL7 SPL | API/original downloads; weekly openFDA label feed; public-domain/CC0 for openFDA data | High-value product/facility/identifier semantics; parsing pipeline candidate |
| O05 | openFDA Drug Shortages | Authoritative operational source | Shortage records plus harmonized drug identifiers | API/download | Strong **held-out** U.S. shortage source if EU shortage semantics drive discovery |
| O06 | EMA Union List of Critical Medicines | Authoritative operational/reference source | EU critical medicines, criticality selection and annual review | Official XLSX; current V2.1 revision 1 | Strong criticality/alternative semantics for resilience discovery |
| O07 | EMA Medicine Supply Shortages JSON | Authoritative operational source | Ongoing/resolved shortage, INN/common name, therapeutic area, forms, strengths, alternatives, start/resolution/update dates | Public JSON website-data export | Strong EU shortage discovery/implementation source |
| O08 | EMA EudraGMDP | Authoritative regulatory database | Manufacturing/import authorisations, GMP/GDP, wholesale distribution, active-substance actors/sites | Public web search/database; organization/location master data use EMA OMS | Important semantic/source evidence for EU actor/site roles; automated bulk ingestion remains conditional until compliant bulk/API access is verified |
| O09 | EMA ESMP reporting model/guidance | Authoritative regulatory platform/schema evidence | Supply, demand, availability and shortage reporting during normal/preparedness/crisis operations | Platform/guidance/templates; machine-to-machine support for reporters | Schema/methodological evidence; not treated as a public empirical bulk dataset at W2 |
| O10 | WHO Model List / Electronic Essential Medicines List | Authoritative international source | Essential medicines, indications, formulations, alternatives/classifications | Public WHO resources; machine-readable/export options vary by interface/release | Strong product/essentiality semantics; redistribution terms for exact machine export must be checked before packaging |
| O11 | WHO National Essential Medicines Lists repository | Authoritative cross-jurisdiction source | National essential medicine lists across many countries | Country-specific downloadable documents/resources | Potential held-out cross-jurisdiction criticality/essentiality source; per-list format/reuse checks required |
| O12 | ClinicalTrials.gov API/download | Authoritative global research registry | Study, sponsor/collaborator, intervention, facility, city/state/postcode/country, status/time | API v2 + JSON/CSV/full study download | Excellent globally distributed source; proposed **held-out** for organization/site/location/trial generalizability |
| O13 | AACT | Authoritative derived relational research infrastructure | Relational representation of ClinicalTrials.gov with 51 tables; sponsor, facility, intervention, geography and results relations | PostgreSQL dump + pipe-delimited tables; 2026-08-10 snapshot 2.33 GB | Excellent held-out relational benchmark and later RDB comparison source; avoid Core concept discovery if reserved |
| O14 | openFDA FAERS | Authoritative safety source | Adverse-event reports with harmonized drug identifiers | API/download; openFDA public-domain/CC0 data family | Optional pharmacovigilance extension/held-out source; known spontaneous-reporting bias and no causal interpretation |
| O15 | ChEMBL 37 | Authoritative curated scientific database | Compounds, drug-like molecules, bioactivities, targets and identifiers | Bulk/API; CC BY-SA 3.0; release 37 (2026-05-01) | Secondary substance/compound identifier enrichment; not an ecosystem supply dataset |
| G01 | GeoNames | Authoritative/open geospatial reference dataset | Global place names, coordinates, administrative codes, alternate names | Daily worldwide/country text dumps; CC BY 4.0 | Geospatial normalization/enrichment only; not pharmaceutical-domain evidence |

## Coverage observations
The landscape deliberately spans:
- **product/substance semantics**: D01/D02, O03/O04, O10, O15;
- **organization/site/facility roles**: O01/O02/O08/O12/O13;
- **shortage/criticality/resilience**: D04/D05, O05/O06/O07/O09;
- **access/reimbursement**: D01/D02/D03, O10/O11;
- **clinical research**: O12/O13;
- **safety**: O14;
- **geospatial normalization**: G01 plus native location fields in D01/D02/O01/O02/O08/O12/O13.

## Main methodological conclusion
No single dataset is sufficiently comprehensive to define a global pharmaceutical ecosystem ontology. V2 therefore requires a **multi-source discovery design** and an explicitly reserved held-out set. DOI-backed datasets provide reproducible empirical anchors, while authoritative operational sources provide domain structures and current regulatory semantics that are not expected to carry dataset DOIs.
