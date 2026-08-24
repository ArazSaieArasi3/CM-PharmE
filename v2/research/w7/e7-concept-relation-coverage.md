# W7-E7 — Concept and Relation Coverage Across Source Families

## Status
**PASS WITH WARNING** under the frozen W7 protocol. Mandatory registry/traceability conditions passed; partial and not-represented semantics are retained as findings.

## Evaluation basis
W7-E7 evaluates the normalized semantics already extracted during W3 from admitted discovery, conditional and secondary source families. It does **not** inspect H1 ClinicalTrials.gov/AACT, H2 openFDA Drug Shortages, or H3 reserved national essential-medicines schemas.

The machine-readable first-pass registry was frozen before execution in:

- `v2/evaluation/protocol/e7-source-semantic-coverage.csv`
- `v2/evaluation/protocol/e7-coverage-rules.json`

The evaluator resolves every represented/partial CM-PharmE target against the frozen W5 ontology and keeps `represented`, `partial`, and `not_represented` outcomes separate.

## Overall source-semantic coverage

| Measure | Result |
|---|---:|
| Normalized source-semantic requirements | **97** |
| Exact represented | **74/97 = 76.29%** |
| Represented or partial | **88/97 = 90.72%** |
| Partial | **14** |
| Not represented | **9** |
| Concept requirements | **63** |
| Concept exact represented | **48/63 = 76.19%** |
| Concept represented or partial | **55/63 = 87.30%** |
| Relation requirements | **34** |
| Relation exact represented | **26/34 = 76.47%** |
| Relation represented or partial | **33/34 = 97.06%** |
| Critical non-exact requirements | **1** |
| Held-out H1–H3 used | **No** |

The one critical non-exact requirement is the P1 outpatient relation **Observation in administrative region**. The semantic association is preserved in the W6 reference KG using `dct:spatial`, but CM-PharmE does not currently define a dedicated internal observation→geography property. It is therefore scored `partial`, not upgraded to `represented` merely to improve the percentage.

## Per-source denominators

| Source | Concept n | Relation n | Exact | Represented/partial | Gaps |
|---|---:|---:|---:|---:|---:|
| P1 NHIF outpatient | 8 | 4 | **9/12 (75.00%)** | **12/12 (100%)** | 0 |
| P2 NHIF inpatient | 5 | 3 | **7/8 (87.50%)** | **8/8 (100%)** | 0 |
| P3 FDA actors/facilities | 5 | 5 | **9/10 (90.00%)** | **10/10 (100%)** | 0 |
| P4 FDA/openFDA product + SPL | 10 | 5 | **12/15 (80.00%)** | **13/15 (86.67%)** | 2 |
| P5 EMA critical/shortage | 6 | 5 | **8/11 (72.73%)** | **11/11 (100%)** | 0 |
| P6 WHO Model List | 4 | 3 | **4/7 (57.14%)** | **7/7 (100%)** | 0 |
| P7 GeoNames | 5 | 2 | **6/7 (85.71%)** | **6/7 (85.71%)** | 1 |
| C1 supply operations | 5 | 3 | **6/8 (75.00%)** | **7/8 (87.50%)** | 1 |
| C2 EudraGMDP | 5 | 2 | **6/7 (85.71%)** | **6/7 (85.71%)** | 1 |
| S1 ChEMBL 37 | 3 | 1 | **3/4 (75.00%)** | **3/4 (75.00%)** | 1 |
| S2 NHIF individual access | 4 | 1 | **2/5 (40.00%)** | **3/5 (60.00%)** | 2 |
| S3 FAERS safety extension | 3 | 0 | **2/3 (66.67%)** | **2/3 (66.67%)** | 1 |

These source-specific denominators are normalized semantic requirements, not raw column counts. W7-E6 remains the field-level mapping evaluation for the frozen NHIF source contracts.

## Explicit not-represented findings
Nine normalized source semantics are not represented in the Gate-D/W5 baseline:

1. P4 — Route of administration.
2. P4 — Product label / labeling artifact.
3. P7 — Alternative geographic name.
4. C1 — Reorder policy / stock parameter.
5. C2 — GMP/GDP certificate or status.
6. S1 — Substance synonym.
7. S2 — Exceptional funding decision or record.
8. S2 — Funding organization associated with access decision.
9. S3 — Adverse-event case/event entity.

These are retained as evidence gaps. They are not automatically promoted into the ontology during first-pass evaluation.

## Partial findings
Fourteen requirements are represented only at bounded/coarser granularity. Important examples include:

- P1 outpatient marketed-name lexicalization;
- observation→region through external `dct:spatial` rather than a dedicated internal property;
- observation→diagnosis association without a dedicated CM-PharmE property;
- P2 observation→facility association represented in the relational layer but not by a dedicated object property;
- FDA registration validity through generic `validFrom`/`validTo`;
- FDA application/marketing-category semantics through broader authorization/listing patterns;
- EMA shortage status and therapeutic-area semantics through broader situation/classification constructs;
- WHO list-version and indication semantics through generic provenance/time/diagnosis structures;
- supply-operations procurement/aboutness semantics at a coarser granularity;
- S2 decision-time/jurisdiction without a dedicated funding-decision relator.

## Gate-D conceptual-element evidence coverage
A second denominator asks a different question: **which of the 87 Gate-D conceptual elements are evidenced by at least one evaluated source-semantic requirement?**

| Module | Evidenced | Denominator | Evidence coverage |
|---|---:|---:|---:|
| Core | **24** | 32 | **75.00%** |
| Cross-cutting infrastructure | **14** | 25 | **56.00%** |
| Extensions | **16** | 30 | **53.33%** |
| **Total** | **54** | **87** | **62.07%** |

This is **not** an ontology-quality or ontology-completeness score. An ontology element can be valid because of literature, methodological, V1-lineage, application or architectural evidence even when none of these evaluated source schemas directly instantiate it.

### Gate-D elements not directly evidenced by the E7 source registry

**Core:** DistributionLogisticsActivity; DistributionSiteRole; EcosystemParticipant; ManufacturingActivity; ManufacturingSiteRole; ProductClassificationAssignment; RegulatoryAuthorityRole; SupplyCapacity.

**Cross-cutting infrastructure:** Address; Assertion; DataQualityFinding; DataSourceResource; Dataset; EntityMatchAssertion; EvidenceItem; IdentifierValue; MappingAssertion; MatchConfidence; ObservationActivity.

**Extensions:** AssetAtRisk; BusinessArchitectureView; ClinicalCareParticipant; DigitalInformationSystemComponent; EnterpriseCapability; PostMarketSurveillanceActivity; RegulatoryOversight; RegulatoryRequirement; RiskAssessmentActivity; RiskTreatmentActivity; RiskTreatmentPlan; ServiceOfferingSpecification; StrategicPartnershipAgreement; Vulnerability.

`Unsupported` in this context means **not directly evidenced by the evaluated source-semantic registry**. It does not mean invalid, unnecessary, or absent from the pharmaceutical domain.

## Incremental source-family contribution
The frozen source order is used only for descriptive accounting and is order-dependent.

| Source | New CM-PharmE targets introduced at that point |
|---|---:|
| P1 NHIF outpatient | **17** |
| P2 NHIF inpatient | **3** |
| P3 FDA actors/facilities | **16** |
| P4 FDA/openFDA product + SPL | **13** |
| P5 EMA critical/shortage | **18** |
| P6 WHO Model List | **2** |
| P7 GeoNames | **5** |
| C1 supply operations | **9** |
| C2 EudraGMDP | **3** |
| S1 ChEMBL | **2** |
| S2 NHIF individual access | **2** |
| S3 FAERS | **2** |

The large contributions from P3–P5 reinforce the W3 finding that actor/facility/regulatory, product/presentation/substance, and shortage/context semantics materially expand the model beyond a single-source or enterprise-centric structure.

## V1→V2 comparison boundary
The existing W3 migration matrix remains the authoritative V1 continuity/novelty record. It identifies 15 V1 concepts materially contributing to Core/infrastructure patterns, 18 moved to modular extensions, 6 deferred/deprecated generic or technology-specific forms, and ten material V2 advances.

W7-E7 does **not** invent a V1 source-level coverage percentage, because no equivalent frozen V1 source-semantic requirement registry exists. The defensible claim is qualitative: V2 introduces explicit evidence-grounded distinctions that the W3 migration matrix documents as new/refined/split semantics. Quantitative source coverage reported here applies only to the frozen V2 registry.

## Research-integrity interpretation
- Coverage percentages are source-specific descriptive evidence.
- Absence of evidence in a source is not evidence of absence in the pharmaceutical ecosystem.
- Discovery-source coverage is not held-out generalizability; that is W7-E8.
- `partial` and `not_represented` findings remain visible and are not normalized away.
- No post-result ontology adaptation is counted as first-pass E7 performance.

## Reproducibility
Final GitHub Actions run: `32366637722` — **SUCCESS**.  
Evidence artifact: `cm-pharme-v2-w7-e7-coverage-evidence`, ID `9405520553`, digest `sha256:e0080b5a074bcf36a39c5ac353d86beba89dd49e84c48a357ab43731871fc70e`.
