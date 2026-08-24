# W7-E8 — Held-out and Cross-Jurisdiction Generalizability

## Status
**COMPLETE — Mandatory Gate PASS; family PASS WITH WARNING.**

GitHub Actions run: `32371213714` — SUCCESS.
Evidence artifact: `cm-pharme-v2-w7-e8-heldout-evidence`, artifact ID `9407208016`, digest `sha256:47cac3a8d7a7218b010322cee046637bd92916b43b41b0733498fa44c9763fe6`.

## Prospective unblinding control
H1–H3 remained protected through W7-E7. E8 is the first authorized evaluation family to inspect and normalize their semantics.

The source manifest, 51 held-out semantic requirements and 12 held-out CQs were frozen before first-pass mapping results were written. The last freeze commit before first-pass mapping is:

`c666fd588487b984df37f150b6bcd32a14f73f02`

No ontology change was made between the held-out freeze and first-pass scoring. The ontology build gate reconfirmed the frozen formal fingerprint:

`59ef47eeed732290736e60bfa1c6bf43a12d15df2f50cff931badb5938cc954a`

## Held-out sources

### H1 — ClinicalTrials.gov / AACT
Evidence basis:
- ClinicalTrials.gov API documentation: `https://clinicaltrials.gov/data-api/api`
- API version endpoint: `https://clinicaltrials.gov/api/v2/version`
- AACT schema: `https://aact.ctti-clinicaltrials.org/schema`

Frozen metadata: ClinicalTrials.gov API `2.0.5`; data timestamp `2026-08-10T09:00:05`; AACT live schema accessed 2026-08-20.

Purpose in E8: test whether an ontology designed around pharmaceutical ecosystem infrastructure can absorb previously unseen clinical-trial semantics without retrofitting the Core.

### H2 — openFDA Drug Shortages
Evidence basis:
- `https://open.fda.gov/apis/drug/drugshortages/`
- `https://open.fda.gov/apis/drug/drugshortages/searchable-fields/`
- `https://open.fda.gov/apis/drug/drugshortages/download/`

Frozen metadata: official download documentation reported one Drug Shortages file last updated `2026-07-23`; documentation accessed 2026-08-20.

Purpose in E8: test a U.S. held-out shortage representation against shortage/product/presentation/jurisdiction semantics learned without using this endpoint during discovery.

### H3 — India National List of Essential Medicines 2022
Evidence basis:
- `https://cdsco.gov.in/opencms/opencms/en/consumer/Essential-Medicines/`
- official NLEM 2022 PDF: `https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2018/UploadPublic_NoticesFiles/reportnlem2022.pdf`

Frozen metadata: NLEM 2022; release date `2022-09-13`; official PDF 157 pages; accessed 2026-08-20.

Purpose in E8: test national, non-EU/non-U.S. essential-medicine contextualization, formulation semantics and healthcare-level recommendations.

## First-pass results

| Measure | Result |
|---|---:|
| Frozen held-out requirements | 51 |
| Exact mapping | **23/51 = 45.10%** |
| Exact or partial mapping | **38/51 = 74.51%** |
| Unseen requirements | **13/51 = 25.49%** |
| Unseen concepts | **5/30 = 16.67%** |
| Unseen relations | **8/21 = 38.10%** |
| Held-out CQs exact | **5/12 = 41.67%** |
| Held-out CQs exact or partial | **9/12 = 75.00%** |
| First-pass ontology changes applied | **0** |
| Gate-D/Core identity conflicts | **0** |

### Per-source mapping

| Source | Exact | Exact + Partial | Unseen |
|---|---:|---:|---:|
| H1 ClinicalTrials.gov/AACT | 4/19 = 21.05% | 7/19 = 36.84% | 12 |
| H2 openFDA Drug Shortages | 12/18 = 66.67% | 18/18 = 100.00% | 0 |
| H3 India NLEM 2022 | 7/14 = 50.00% | 13/14 = 92.86% | 1 |

## Interpretation
The result is intentionally heterogeneous.

H2 is the strongest held-out result: every normalized shortage requirement is at least partially representable and two-thirds are exact. This supports the claim that the product–presentation–shortage–jurisdiction backbone generalizes to a previously unused U.S. shortage source.

H3 is also strong for the principal essential-medicine semantics: contextual essential classification, jurisdiction, dosage form, strength, list/version and therapeutic classification are representable. The main mismatch concerns healthcare-level applicability and medicine-versus-active-moiety granularity.

H1 creates substantial extension pressure. The frozen Core can represent organizations, facilities, geography and pharmaceutical identity distinctions, but it intentionally lacks explicit Clinical Study, Study Arm/Group, Trial Outcome, Study Phase/Status and study-specific relations. These are not treated as evidence that Organization, Facility, Product, Substance, Presentation, Jurisdiction or provenance identities were modeled incorrectly. They indicate that a **Clinical Trials Extension** would be required to make trial semantics first-class.

## Mismatch categories
The first-pass result preserves the following categories rather than normalizing them away:
- domain-scope extension pressure;
- missing domain relations;
- source-report versus domain-semantic mismatch;
- product/substance/presentation identity granularity;
- jurisdiction/context applicability;
- version/list context.

No finding requires reversing the protected Gate-D distinctions.

## Post-test adaptation pressure
Three bounded adaptation packages are recommended for later consideration; **none is applied in E8 first-pass scoring**:

1. **Clinical Trials Extension** — ClinicalStudy, Intervention context, Arm/Group, Outcome, Phase, Status, Sponsorship and Study↔Facility/Condition/Outcome/Intervention relations.
2. **Shortage Reporting Refinement** — explicit ShortageStatus/Reason semantics, company/reporting association and typed posting/update/change/discontinuation lifecycle metadata.
3. **Essential-Medicines Refinement** — healthcare-level applicability and a broader contextual-classification target pattern that can safely handle medicine/product versus active-moiety/substance granularity.

Any implementation of these packages must be recorded as post-test adaptation and cannot retroactively increase the initial E8 score.

## Claim boundary
E8 supports bounded representational generalizability. It does **not** establish global pharmaceutical-domain completeness. ClinicalTrials.gov/AACT, a U.S. shortage endpoint and one Indian national essential-medicines list are deliberately heterogeneous held-out probes, not a statistically representative sample of all jurisdictions or pharmaceutical data systems.
