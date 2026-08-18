# W2 Dataset / Source Scorecard

Scores are W2 selection aids, not claims of intrinsic dataset quality. Official operational sources are scored on stable authority rather than DOI presence. Held-out status is independent of score.

| ID | Source | Score /100 | Admission | Intended role | Main limitation |
|---|---|---:|---|---|---|
| D01 | NHIF Outpatient, DOI 10.5281/zenodo.19160825 | **93** | Strong | Discovery + Implementation + Evaluation | Bulgaria/NHIF-specific; regional not facility-level |
| D02 | NHIF Inpatient, DOI 10.5281/zenodo.19160637 | **92** | Strong | Discovery + Implementation + Evaluation | Hospital reimbursement context, not manufacturing/supply network |
| D03 | NHIF Individually Approved Medicines, DOI 10.5281/zenodo.15680002 | **79** | Bounded | Supplemental evaluation / access extension | Same institutional/jurisdiction family as D01/D02 |
| D04 | Risk-Informed Pharmaceutical Supply, DOI 10.5281/zenodo.18851842 | **78** | Conditional | Discovery/analysis for supply & resilience | Standard open-data license not verified; do not redistribute raw files without clarification |
| D05 | Hospital Pharmacy Demand Uncertainty, DOI 10.5281/zenodo.21456323 | **69** | Exploratory | Future forecasting/inventory research | Narrow 13-medicine scope; explicit standard license not verified |
| O01 | FDA DECRS | **88** | Strong operational | Discovery + Implementation | Establishment registration is not product approval/compliance; U.S.-specific |
| O02 | FDA WDD/3PL reporting | **86** | Strong operational | Discovery + Implementation | Facility license/reporting records, not complete product-level transaction network |
| O03 | openFDA NDC | **92** | Strong operational | Product/identifier enrichment + Implementation | Labeler-submitted listing; NDC does not itself establish FDA approval |
| O04 | FDA/openFDA SPL | **91** | Strong operational | Schema discovery + product/facility identity + Implementation | Parsing complexity; labeling does not encode complete supply dependencies |
| O05 | openFDA Drug Shortages | **90** | Strong, reserved | **Held-out** shortage/generalizability evaluation | U.S. reporting scope; must remain outside W3 shortage concept admission |
| O06 | EMA Union List of Critical Medicines | **84** | Bounded/strong reference | Discovery + resilience reference | EU-contextual criticality; exact redistribution terms for source file should be respected |
| O07 | EMA Medicine Supply Shortages JSON | **86** | Strong operational | Discovery + Implementation | EMA website shortage scope, not all national EU shortages |
| O08 | EMA EudraGMDP | **73** | Conditional operational | Schema/semantic discovery; later implementation if compliant access is verified | Public bulk/API ingestion not verified in W2 |
| O09 | EMA ESMP model/guidance | **72** | Schema evidence | Methodological/schema evidence | Not a public bulk empirical dataset |
| O10 | WHO Model List / eEML | **81** | Bounded/strong reference | Discovery + product/essentiality enrichment | Exact machine-export reuse terms require verification before redistribution |
| O11 | WHO National EML repository | **74** | Conditional family | Candidate held-out cross-jurisdiction evaluation | Per-country formats, versions and reuse terms vary |
| O12 | ClinicalTrials.gov API/download | **91** | Strong, reserved | **Held-out** generalizability | Terms/attribution must be respected; schema excluded from W3 Core discovery |
| O13 | AACT 2026-08-10 snapshot | **94** | Strong, reserved | **Held-out relational benchmark** + W6/W7 comparison | Same underlying source family as ClinicalTrials.gov; not independent from O12 |
| O14 | openFDA FAERS | **86** | Strong optional | Safety extension / held-out | Reporting bias; no causal interpretation |
| O15 | ChEMBL 37 | **89** | Strong secondary | Substance/identifier enrichment | Not ecosystem supply/manufacturing evidence; share-alike license implications |
| G01 | GeoNames | **90** | Strong enrichment | Geospatial normalization | Not pharmaceutical-domain evidence; geocoding/matching errors must be measured |

## Portfolio interpretation
### Primary discovery/implementation anchors
D01, D02, O01, O02, O03/O04, O06/O07, O10 and G01 provide complementary empirical, regulatory, product and geospatial structures.

### Conditional but strategically important
D04 is the richest current candidate for actual inventory/procurement/lead-time/stockout semantics. It is admitted only as **conditional scholarly-use evidence** until redistribution/reuse terms are clarified. O08 is semantically important but automated public ingestion is conditional on verified access.

### Protected held-out evidence
O05 and the O12/O13 source family are deliberately protected from W3 Core concept discovery. O11 may provide a second cross-jurisdiction held-out family after a small country subset passes per-file reuse/format audit.

### Optional/future
D05, O14 and deeper ChEMBL bioactivity structures remain available without forcing the principal ontology paper into forecasting, safety prediction or molecular drug discovery.
