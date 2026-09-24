# Dataset and Source Index

> **Version scope:** Primarily V2, with cross-version research context  
> **Status:** Stable-to-date / Evolving  
> **Updated:** 2026-09-23

## Research source families

| Code | Source | Research role | Current boundary |
|---|---|---|---|
| P1 | NHIF Outpatient Pharmacy — DOI 10.5281/zenodo.19160825 | Primary | W6 uses schema-faithful fixture; aggregate patient counts are not patient identities |
| P2 | NHIF Inpatient — DOI 10.5281/zenodo.19160637 | Primary/secondary research source | W6 fixture preserves facility vs organization identity |
| P3 | FDA DECRS + wholesale/3PL registration sources | Authoritative | organization/facility/registration evidence; W6 full execution not implied |
| P4 | openFDA NDC + SPL context | Authoritative product/reference | identifiers are not universal entity identity |
| P5 | EMA Critical Medicines + shortage/ESMP context | Authoritative | criticality/shortage remain source/version/jurisdiction contextual |
| P6 | WHO Model List / eEML | Authoritative | supports essential-medicine/classification evidence |
| P7 | GeoNames | Normalization/reference | geography normalization, not pharmaceutical-domain evidence |
| C1 | Pharmaceutical supply operations — DOI 10.5281/zenodo.18851842 | Conditional | used only within admitted bounded role |
| C2 | EudraGMDP semantic/schema evidence | Conditional / authoritative | ingestion/coverage claims remain bounded |
| S1 | ChEMBL | Secondary/extension | substance/product reference support |
| S2 | NHIF Individually Approved Medicines | Secondary/extension | market-access/product evidence |
| S3 | FAERS | Optional Pharmacovigilance extension | not principal Core driver |
| H1 | ClinicalTrials.gov / AACT | Held-out | protected from Core discovery; later E8 evidence |
| H2 | openFDA Drug Shortages | Held-out | protected from Core discovery; later E8 evidence |
| H3 | Reserved national Essential Medicines List sample | Held-out | protected from Core discovery; later E8 evidence |

## W6 executable source manifest

The W6 source manifest explicitly records P1, P2, P3, P4, P5 and P7 contracts.

Only P1/P2 are executed through deterministic schema-faithful fixture adapters in the W6 reference pipeline. Contract existence must not be misread as full-source ingestion.

## Held-out discipline

H1–H3 were reserved from Core discovery and used later for bounded generalizability evaluation. This separation is important to the V2 research design.

## Evidence navigation

- [W6 source manifest](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/data/sources/source-manifest.json)
- [W2 dataset portfolio](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w2/gate-c-dataset-portfolio.md)
- [Source-field mapping](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/data/mappings/source-field-ontology-mapping.csv)
- [Held-out manifest](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/evaluation/heldout/e8-heldout-source-manifest.json)
- [Concept provenance matrix](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w4/human-review-concept-provenance-matrix.md)

## Related pages

[[V2 Dataset Landscape and Provenance]] · [[V1 to V2 Evidence and Provenance]]

---

<details>
<summary>Documentation record</summary>

- **Page scope:** Primarily V2, with cross-version research context
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative sources:** V2 source portfolio, source manifest and concept-provenance matrix
- **Last synchronized:** 2026-09-23
- **Related issues:** W2/W3, #208
- **Evidence status:** Research-source registry; execution/ingestion status varies by source
- **Future refresh:** #214
- **Wiki baseline:** WB-2026.09.1
- **Authoritative source:** V1: main; V2: v2/research-program
- **Last synchronized ref:** V1: main; V2: v2/research-program

</details>
