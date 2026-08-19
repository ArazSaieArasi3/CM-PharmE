# W2 — Dataset Landscape, Admission and Held-out Evaluation Design Closure

## Status
**W2 implementation: COMPLETE**

**Gate C: READY FOR USER DECISION**

## Issues covered
- V2-018 Comprehensive pharmaceutical dataset landscape
- V2-019 DOI-backed research dataset registry
- V2-020 Authoritative operational-source registry
- V2-021 Geospatial actor/facility source profile
- V2-022 Medicinal-product/substance source profile
- V2-023 Manufacturing/supplier/logistics source profile
- V2-024 Clinical-trial/pharmacovigilance/shortage source profile
- V2-025 Market-access/reimbursement/finance source profile
- V2-026 Dataset admission/scoring criteria
- V2-027 Primary/secondary/held-out portfolio selection

## Main outputs
1. `dataset-landscape.md`
2. `doi-dataset-registry.md`
3. `operational-source-registry.md`
4. `domain-source-profiles.md`
5. `dataset-admission-rubric.md`
6. `dataset-scorecard.md`
7. `gate-c-dataset-portfolio.md`
8. `../../manuscript/w2-dataset-method-notes.md`
9. updated `../evidence-registry.md`
10. updated `../../manuscript/evidence-ledger.md`

## Key W2 conclusions
1. A single dataset cannot credibly define the global pharmaceutical ecosystem; V2 needs a role-separated, multi-source design.
2. Two NHIF Bulgaria DOI datasets provide strong, reproducible relational empirical anchors for product/access/geography/time and facility/product relationships.
3. FDA, EMA and WHO operational/reference sources provide complementary product, establishment, logistics-role, shortage, criticality and essential-medicine semantics.
4. GeoNames is suitable as geospatial normalization/enrichment, not as pharmaceutical-domain evidence.
5. ClinicalTrials.gov/AACT and openFDA Drug Shortages are valuable enough to reserve before W3 concept discovery as held-out evaluation source families.
6. The richest operational supply dataset found (DOI 10.5281/zenodo.18851842) is scientifically useful but has nonstandard reuse wording; its raw redistribution remains conditional.
7. Public-source evidence is currently insufficient for a claim of complete global product-level supplier→buyer→shipment reconstruction.
8. Financing/counterparty data remain too weak for promotion into the V2 Core; finance remains an extension/future research candidate.

## Gate C recommended portfolio
### Primary Discovery / Implementation
- P1 NHIF Outpatient — DOI 10.5281/zenodo.19160825
- P2 NHIF Inpatient — DOI 10.5281/zenodo.19160637
- P3 FDA DECRS + WDD/3PL
- P4 openFDA NDC + FDA/openFDA SPL
- P5 EMA Union Critical Medicines + EMA shortages JSON
- P6 WHO Model List / eEML
- P7 GeoNames for geographic normalization

### Conditional
- C1 Pharmaceutical supply operations — DOI 10.5281/zenodo.18851842
- C2 EMA EudraGMDP automated ingestion; semantic/schema use is acceptable but bulk/API access must be verified before pipeline ingestion

### Secondary / Enrichment
- ChEMBL 37
- NHIF Individually Approved Medicines — DOI 10.5281/zenodo.15680002
- optional openFDA FAERS safety extension

### Protected Held-out
- H1 ClinicalTrials.gov / AACT source family
- H2 openFDA Drug Shortages
- H3 small jurisdiction-diverse WHO national EML sample after per-list audit

## Gate C decision
Approval freezes these **source roles and held-out boundaries**, not the ontology. W3 will then begin evidence-driven concept/relation discovery using the approved discovery sources while preventing held-out schemas from silently shaping the Core.

## Main-branch safety
All W2 work is isolated on `v2/w2-data-landscape`. No V2 change targets `main`.
