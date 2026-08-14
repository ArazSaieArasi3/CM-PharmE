# Reference Scenario — Vaccine Distribution

This constructed scenario is adapted from the journal manuscript and retained as reusable evaluation evidence. It supports representational traceability and executable testing; it is not an empirical deployment or a claim of complete vaccine-lifecycle coverage.

## Scenario mapping

| Scenario element | CM-PharmE construct | Interpretation |
|---|---|---|
| Vaccine manufacturer | `CMPE-C0001` Pharmaceutical Enterprise | Organizational bearer for pharmaceutical activities |
| National health authority | `CMPE-C0023` Regulatory Authority Entity | Regulatory actor; entity/role distinction remains explicit |
| Distribution partnership | `CMPE-C0014` Strategic Partnership Agreement | Collaborative relator among ecosystem actors |
| Regulatory supervision | `CMPE-C0004` Regulatory Oversight | Oversight relator distinct from the regulator entity |
| Governance obligation | `CMPE-C0026` Governance Policy Framework | Normative governance condition |
| Compliance obligation | `CMPE-C0027` Compliance Requirement | Compliance-related mode |
| Cold-chain distribution | `CMPE-C0015` Pharmaceutical Business Process | Temporally unfolding regulated process |
| Vaccinated person | `CMPE-C0017` Individual Patient | Context-dependent patient role |
| Vaccination activity | `CMPE-C0016` Clinical Activity Sequence | Clinical activity sequence |
| Clinical coordination | `CMPE-C0018` Clinical Pathway | Relator coordinating clinical participation |
| Adverse-event obligation | `CMPE-C0036` Pharmacovigilance Requirement | Normative requirement |
| Adverse-event reporting | `CMPE-C0022` Adverse Event Reporting Procedure | Reporting procedure/activity |
| Post-market analysis | `CMPE-C0037` Post-Market Surveillance Activity | Operational post-market activity |
| Evidence platform | `CMPE-C0038` Real-World Evidence Platform | Digital evidence platform |
| Risk analysis | `CMPE-C0028` Risk Management Activity | Governance response activity |
| Clinical information system | `CMPE-C0033` Electronic Health Record System | Digital clinical-information enabler |
| Supply-chain ledger | `CMPE-C0031` Blockchain-Based Supply Chain Ledger | Digital traceability enabler |

## B4 machine-readable realization

The constructed RDF sample is available at [`../samples/vaccine-distribution.ttl`](../samples/vaccine-distribution.ttl). It uses only existing CM-PharmE classes and canonical relations.

Executed schema validation found **33 individuals**, **32 distinct core classes**, **all five domains**, and **34 CM-PharmE relation assertions**, with no unknown class/property assertion, no explicit domain/range violation, and no scenario-defined `owl:Class`.

The eight B4 competency queries execute over the canonical ontology plus this sample.

## Manuscript-to-formal boundary

The manuscript scenario is an interpretive research narrative, while the RDF sample is constrained to the current canonical formal graph. B4 therefore records rather than hides several differences:

- Governance Policy / Compliance Requirement are discussed in the manuscript as constraining operational constructs, but no direct policy/compliance-to-business-process constrain property is currently encoded.
- The manuscript states that Pharmacovigilance Requirement constrains Adverse Event Reporting Procedure; the canonical model instead encodes requirement → Post-Market Surveillance Activity and surveillance → reporting procedure.
- The manuscript describes RWE Platform → surveillance → risk-management reasoning more directly than the canonical graph, which explicitly has RWE Platform → Pharmacovigilance Requirement and RWE Platform → Risk Management Activity.
- EHR information exchange and blockchain traceability remain application interpretations broader than their narrow formal relations.

See [`../evidence/b4-scenario-traceability.yaml`](../evidence/b4-scenario-traceability.yaml) for the complete disposition.

## Evidential boundary

The sample demonstrates bounded representational plausibility and executable traceability. It does not establish empirical correctness, operational interoperability, legal conformance, organizational adoption, or general completeness.
