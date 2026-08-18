# W1 Manuscript Notes — Problem, Need and Application Framing

Status: working notes for later manuscript drafting. These are not final claims.

## Problem framing supported at W1
Pharmaceutical ecosystem information is distributed across regulatory shortage platforms, establishment and manufacturing-site records, clinical-trial registries, pharmacovigilance systems, medicines-access indicators, and other operational sources. The challenge for CM-PharmE 2.0 is not merely to aggregate more records, but to provide an explicit conceptual basis for reconciling **entities, contextual roles, physical sites, jurisdictions, temporal status, cross-domain dependencies, and evidence provenance** across heterogeneous sources.

Official regulatory evidence supports concrete needs for:
- monitoring medicine supply, demand, availability and shortages;
- identifying critical medicines and supply-chain vulnerabilities;
- representing organizations and physical manufacturing/distribution sites separately;
- supporting crisis/preparedness and alternative-supply reasoning;
- integrating sponsor/facility/geographic structures for clinical research;
- connecting safety evidence and signals with traceable product/source information;
- measuring medicine availability/access in a geographic context.

## Working application framing
The principal V2 article should not attempt to implement every possible ecosystem application. W1 identifies a broad portfolio and recommends two primary domain demonstrators plus one cross-representation research demonstrator:

1. **Global Actor/Facility Geospatial Integration** — cross-source/cross-jurisdiction representation of organizations, roles, sites, location and regulatory evidence.
2. **Critical Medicine Supply Vulnerability & Resilience** — ontology-driven analysis of product/site/supplier/geographic dependencies and alternatives.
3. **Ontology↔RDB↔KG Consistency & Provenance** — test whether equivalent benchmark questions remain semantically consistent across representations and remain traceable to evidence.

These are candidate commitments only until Gate B and W2 data-admission evidence confirm feasibility.

## AI framing
AI is treated as an evaluable capability, not a rhetorical novelty label. Entity resolution is the most directly relevant cross-cutting candidate for the principal V2 research because heterogeneous data integration requires measured identity reconciliation. Provenance-aware semantic QA/GraphRAG is a useful demonstrator candidate. Demand forecasting, predictive shortage modeling, graph completion, anomaly detection and pharmacovigilance prediction remain follow-on opportunities unless W2/W7 provide strong benchmark data and objective evaluation.

## Risk/resilience framing
CM-PharmE Core should represent pharmaceutical ecosystem facts and dependencies. Generic risk concepts should be reused/aligned through a modular Risk & Resilience Extension, potentially drawing on UFO-grounded reference work such as COVER/ROSE. W1 does not claim an existing user-owned risk ontology has already been integrated.

## Contribution discipline inherited from V1 experience
- state V1→V2 differences explicitly;
- do not repackage shared foundations as novelty;
- explain how domains/modules are derived from evidence;
- predefine expert protocol and evaluation criteria prospectively;
- distinguish illustrative/application evidence from empirical validation;
- avoid interoperability, completeness, superiority or adoption claims without direct evidence;
- maintain exact manuscript↔repository↔data traceability.
