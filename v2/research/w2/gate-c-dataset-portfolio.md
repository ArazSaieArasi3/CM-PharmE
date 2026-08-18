# W2 Gate C — Proposed Dataset / Source Portfolio

## Status
**W2 selection complete — awaiting Gate C approval.**

The portfolio is designed to support the approved Gate B demonstrators while preventing CM-PharmE 2.0 from becoming a mirror of one dataset or jurisdiction.

## A. Proposed Primary Discovery / Implementation Portfolio

| Portfolio ID | Source | Role in W3/W6 | Gate B support |
|---|---|---|---|
| P1 | NHIF Outpatient, DOI **10.5281/zenodo.19160825** | DOI-backed empirical anchor for product/ATC/INN, region, diagnosis, utilisation/reimbursement and time; large tabular RDB benchmark | A, C; supplementary access analytics |
| P2 | NHIF Inpatient, DOI **10.5281/zenodo.19160637** | DOI-backed empirical anchor for hospital/facility–product–diagnosis–region–time relations | A, C |
| P3 | FDA DECRS + WDD/3PL operational source family | U.S. organization/site/facility-role discovery and implementation for manufacturer/establishment/distributor/3PL distinctions | **A**, B, C |
| P4 | openFDA NDC + SPL operational source family | Product/package/substance identifiers, product attributes, labeler/product/facility semantics and cross-source identifiers | A, B, C |
| P5 | EMA Union List of Critical Medicines + EMA shortage JSON | EU criticality, shortage, alternatives, forms/strengths and temporal shortage semantics | **B**, C |
| P6 | WHO Model List / eEML | Essential-medicine/product/formulation/alternative semantics and international reference layer | B; product enrichment |
| P7 | GeoNames | Place/geographic normalization for PostGIS and cross-source location resolution | **A**, B, C |

### Primary portfolio boundary
P1/P2 are the main DOI-backed reproducible empirical anchors. P3–P7 are authoritative operational/reference sources. Exact source snapshots, terms, hashes and ETL instructions must be frozen in W6 before empirical results are produced.

## B. Conditional Discovery / Resilience Evidence

### C1 — Pharmaceutical supply operations dataset
**DOI: 10.5281/zenodo.18851842**

Reason to include conditionally:
- directly exposes consumption, procurement lead times/arrivals, inventory, prices, stock parameters and stockout/operational events;
- provides relation richness not available in public regulatory registries;
- materially strengthens Gate B demonstrator B.

Restriction:
- W2 verified the dataset statement “released for scientific and academic use,” but did not verify a standard open-data license permitting unrestricted redistribution.
- It may inform scholarly analysis/concept discovery under the stated terms, but raw files must not be republished in the CM-PharmE public research release unless reuse/redistribution rights are clarified.

### C2 — EMA EudraGMDP
Use as authoritative semantic/schema evidence for manufacturing/import/GMP/GDP/wholesale/active-substance actor and site roles. Automated ingestion remains conditional until a compliant public bulk/API access method is verified.

## C. Secondary / Enrichment Sources

| ID | Source | Role |
|---|---|---|
| S1 | ChEMBL 37 | Substance/compound identifier and terminology enrichment; do not import broad bioactivity semantics into Core without use-case evidence |
| S2 | NHIF Individually Approved Medicines, DOI 10.5281/zenodo.15680002 | Supplemental access/funding/exception-treatment evaluation; not an independent jurisdiction from P1/P2 |
| S3 | openFDA FAERS | Optional Safety/Pharmacovigilance extension; not used to expand Core unless extension work is activated |

## D. Protected Held-out Evaluation Sources

### H1 — ClinicalTrials.gov / AACT family
- Reserve the **ClinicalTrials.gov / AACT source family** for W7 generalizability and W6/W7 relational comparison.
- AACT provides a PostgreSQL snapshot and 51-table schema; the 2026-08-10 snapshot is available as a 2.33 GB PostgreSQL dump.
- W3 must not mine this schema to admit Core concepts/relations.
- Later evaluation may test coverage of sponsor/collaborator/facility/location/intervention structures and cross-jurisdiction records against the independently designed Core.

### H2 — openFDA Drug Shortages
- Reserve U.S. Drug Shortages as a cross-jurisdiction shortage test.
- W3 shortage/criticality semantics are primarily discovered from EMA sources plus pharmaceutical supply evidence.
- W7 then tests how well those semantics represent the independent U.S. shortage source.

### H3 — Selected WHO National Essential Medicines Lists, conditional
- Select a small jurisdiction-diverse sample only after per-list format/reuse audit.
- Do not use selected held-out lists for Core concept admission.
- Intended to test context/jurisdiction handling of essential/critical medicine semantics.

## E. Explicitly Not Required for the Principal V2 Paper
- DOI 10.5281/zenodo.21456323 demand-uncertainty dataset: retain for future forecasting/inventory research.
- Full FAERS pharmacovigilance ingestion: future extension unless the principal ontology evaluation needs it.
- Broad ChEMBL bioactivity integration: outside the pharmaceutical ecosystem Core scope.
- Financing/counterparty datasets: no sufficiently strong public evidence found in W2 to justify a dedicated Core finance domain.
- Global transaction-level supplier→buyer→shipment reconstruction: current public data landscape is insufficient for a defensible completeness claim.

## F. Dataset-to-Demonstrator mapping
| Demonstrator | Primary support | Conditional/secondary support | Held-out test |
|---|---|---|---|
| **A. Global Actor/Facility Geospatial Integration** | FDA DECRS/WDD3PL, NHIF inpatient, GeoNames, openFDA product identity | EudraGMDP semantic evidence | ClinicalTrials.gov/AACT global facilities/sponsors/locations |
| **B. Critical Medicine Supply Vulnerability & Resilience** | EMA Critical Medicines, EMA shortages JSON, FDA site/product identity | D04 supply operations, WHO eEML | openFDA Drug Shortages; later selected national EMLs |
| **C. Ontology↔RDB↔KG Consistency & Provenance** | NHIF D01/D02, FDA/openFDA snapshots, GeoNames | D04 if terms permit analysis | AACT relational source family for additional representation/generalizability tests |

## G. Entity-resolution AI decision
**Conditional promotion approved in principle, not yet activated.**

W6/W7 may activate measured entity resolution only if P3/P4/P7 and/or held-out sources yield a curated overlapping sample where same-entity judgments can be established independently. Required evaluation: precision, recall, F1 and ambiguity/error analysis. No AI performance claim is made at Gate C.

## Gate C decision requested
Approve, modify or reject this role-separated portfolio. Approval freezes the **source roles**, not the ontology concepts. W3 will then discover concepts/relations from P1–P7 plus approved conditional/schema evidence while respecting H1–H3 held-out boundaries.
