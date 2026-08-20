# W7-E8 Post-Test Adaptation Register

## Rule
This register is downstream of the frozen first-pass E8 result. No item below is counted as initial held-out success. Any implementation requires a separate issue/commit and must preserve the first-pass evidence artifact.

| Adaptation ID | Package | Triggered by | Proposed scope | Core identity change? | First-pass applied? | Disposition |
|---|---|---|---|---|---|---|
| E8-A01 | Clinical Trials Extension | H1 | Add ClinicalStudy, trial intervention context, study arm/group, trial outcome, phase/status and study-specific sponsorship/site/condition/outcome/intervention relations | **No** | **No** | Candidate extension for later scope decision |
| E8-A02 | Shortage Reporting Refinement | H2 | Add explicit shortage status/reason semantics, company/reporting association and typed publication/update/change/discontinuation lifecycle metadata | **No** | **No** | High-value refinement candidate |
| E8-A03 | Essential-Medicines Refinement | H3 | Add healthcare-level applicability and broaden contextual classification targeting so medicine/product and active-moiety/substance granularity can be handled explicitly | **No** | **No** | High-value refinement candidate |

## Non-adaptation findings
The following are intentionally **not** treated as reasons to change the model:
- Organization remains distinct from Facility.
- Geography remains distinct from Regulatory Jurisdiction.
- Medicinal Product remains distinct from Pharmaceutical Substance and Product Presentation.
- Observation Result is not silently redefined as Clinical Trial Outcome.
- Source-record status/reason strings are not automatically promoted to domain entities.

## Decision principle
Implement an E8 adaptation only if it advances the principal CM-PharmE 2.0 research questions or an approved extension/demonstrator. Do not expand the Core merely to maximize held-out coverage.
