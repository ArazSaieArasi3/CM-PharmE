# Reference Scenario — Vaccine Distribution

This constructed scenario is adapted from the journal manuscript and is retained as reusable evaluation evidence. It supports representational traceability and later executable testing; it is not an empirical deployment or a claim of complete vaccine-lifecycle coverage.

## Scenario mapping

| Scenario element | CM-PharmE construct | Interpretation |
|---|---|---|
| Vaccine manufacturer | `CMPE-C0001` Pharmaceutical Enterprise | Organizational bearer for pharmaceutical activities |
| National health authority | `CMPE-C0023` Regulatory Authority Entity | Regulatory actor rather than a new scenario-specific class |
| Distribution partnership | `CMPE-C0014` Strategic Partnership Agreement | Collaborative relator among relevant ecosystem actors |
| Regulatory supervision | `CMPE-C0004` Regulatory Oversight | Oversight relation distinct from the regulator entity |
| Governance obligation | `CMPE-C0026` Governance Policy Framework | Normative governance condition |
| Compliance obligation | `CMPE-C0027` Compliance Requirement | Compliance constraint affecting relevant work |
| Cold-chain distribution | `CMPE-C0015` Pharmaceutical Business Process | Temporally unfolding regulated process |
| Vaccinated person | `CMPE-C0017` Individual Patient | Context-dependent patient role |
| Vaccination activity | `CMPE-C0016` Clinical Activity Sequence | Clinical activity coordinated through the clinical context |
| Clinical coordination | `CMPE-C0018` Clinical Pathway | Relator coordinating relevant participation |
| Adverse-event obligation | `CMPE-C0036` Pharmacovigilance Requirement | Normative requirement distinct from reporting activity |
| Adverse-event reporting | `CMPE-C0022` Adverse Event Reporting Procedure | Reporting activity/procedure |
| Post-market analysis | `CMPE-C0037` Post-Market Surveillance Activity | Operational post-market activity |
| Evidence platform | `CMPE-C0038` Real-World Evidence Platform | Digital enabler supporting evidence use |
| Risk analysis | `CMPE-C0028` Risk Management Activity | Governance response activity |
| Clinical information system | `CMPE-C0033` Electronic Health Record System | Digital enabler for clinical information exchange |
| Supply-chain ledger | `CMPE-C0031` Blockchain-Based Supply Chain Ledger | Digital enabler for traceability |

## Evaluation expectations

The scenario should preserve the distinctions between organization and role, participant and relator, requirement and activity, process and rigid entity, and digital enabler and operational work. It is relevant to competency questions `CMPE-CQ002` through `CMPE-CQ005` and to the application/extension questions `CMPE-CQ007` and `CMPE-CQ008`.

## B4 target

A later B4 sub-batch should create a machine-readable constructed sample for selected scenario instances and use it with executable SPARQL and constraint checks. Any such sample remains evaluation data unless a separately documented real-world source is introduced.