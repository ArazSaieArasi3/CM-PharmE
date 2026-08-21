# W7-E11 — Selected Analytics and AI Demonstrator Evaluation

## Status
**Mandatory gate: PASS**  
**Family status: PASS WITH DEFERRED AI**

Issue: #100  
Eligibility freeze anchor: `e66411966bc76a26d01223429320650a9ead50e5`  
Final GitHub Actions run: `32497401994` — SUCCESS  
Evidence artifact: `9452149859`  
Artifact digest: `sha256:6447825f45bd74c741358208cfe55b40acf43c6bcf4ea472180024aeddb564c8`

## Evaluation rule
A candidate was eligible only if all four elements were available before benchmarking:
1. a defined dataset or executable reference realization;
2. a comparison baseline;
3. a predefined metric;
4. an ontology-dependent hypothesis.

The registry was frozen before the evaluator/workflow was introduced. A missing prerequisite produces a transparent deferral, not a synthetic benchmark or a retrospective AI claim.

## Candidate audit
The W1 catalog contributed **17 candidates**: **8 analytics** and **9 AI** tasks.

- Benchmark-supported candidates: **1**
- Deferred candidates: **16**
- AI candidates promoted to a performance/novelty claim: **0**

### Benchmark-supported analytics
`AN-08 — Cross-representation benchmark analytics` is the only candidate that currently satisfies all mandatory prerequisites. W7-E11 rebuilt the reference PostgreSQL/PostGIS realization and deterministic RDF/KG, then independently re-ran the frozen paired query suite. Result: **4/4 SQL↔SPARQL benchmark pairs PASS**.

The supported claim is bounded: selected ontology-aligned benchmark questions preserve canonicalized answers across the reference relational and RDF representations. This is not a claim of universal lossless SQL↔SPARQL equivalence.

## AI deferral findings
The AI opportunity catalog remains scientifically relevant, but current W7 evidence is insufficient for measured AI novelty claims:

- `AI-01 Cross-source entity resolution`: **DEFERRED**. The repository contains two schema-faithful exact fixture matches, but no defensible real-world audited/gold subset. Therefore precision/recall/F1 are not reported.
- `AI-02 Provenance-aware semantic QA / GraphRAG`: **DEFERRED**. No frozen QA corpus, answer key and non-KG baseline.
- `AI-03 Demand forecasting`: **DEFERRED**. No admitted longitudinal forecasting benchmark with predefined train/test design.
- `AI-04 Shortage prediction`: **DEFERRED**. No frozen labeled training/evaluation dataset and split.
- `AI-05 Supplier/facility criticality prediction`: **DEFERRED**. No complete dependency graph with disruption ground truth.
- `AI-06 Graph anomaly detection`: **DEFERRED**. No real anomaly gold set; synthetic anomalies alone would not justify an empirical AI novelty claim.
- `AI-07 Graph completion`: **DEFERRED**. No frozen link-prediction train/validation/test benchmark.
- `AI-08 Pharmacovigilance prediction`: **DEFERRED**. PV benchmark data and ground truth are not part of the current implementation evidence.
- `AI-09 Explainable resilience/risk analytics`: **DEFERRED TO FOLLOW-ON**. Risk/resilience semantics and outcome benchmark are not mature enough for an AI claim in the principal ontology article.

## Non-AI analytics deferrals
Other analytics candidates were also kept bounded where the data are not yet sufficient. In particular, full supplier→buyer→shipment reconstruction, empirical geocoding accuracy, full shortage analytics, clinical-trial network analytics, pharmacovigilance retrieval and real-data reimbursement-effectiveness analytics are not claimed from the current repository state. `AN-02` is handed to E12 as a scenario/resilience evaluation rather than being mislabeled as an empirical predictive benchmark.

## Reproducibility
Workflow: `.github/workflows/v2-w7-e11-analytics-ai.yml`  
Evaluator: `tools/v2_evaluation/e11_analytics_ai_gate.py`  
Frozen registry: `v2/evaluation/protocol/e11-analytics-ai-eligibility.json`

The final workflow also regenerated the 398-triple reference fixture KG and re-ran the four frozen cross-representation benchmarks before evaluating the E11 claim gate.

## Interpretation boundary
E11 supports **one benchmarked analytics claim (AN-08)** and, equally importantly, establishes a repository-enforced rule against unsupported AI claims. It does **not** show that the deferred AI methods are ineffective. It shows only that the current principal-paper evidence is insufficient to report their accuracy, predictive gain, utility or novelty.

This is a deliberate evidence-sufficiency decision: the principal CM-PharmE 2.0 article remains ontology/data-infrastructure centered rather than being diluted by unbenchmarked AI claims.
