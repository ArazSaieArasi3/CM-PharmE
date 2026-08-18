# W1 Data-Analytics and Ontology-Enabled AI Opportunity Catalog

## Design rule
AI is not a novelty claim by itself. A candidate is promoted into the principal research contribution only when the ontology/KG materially improves the task, the data are admitted, a non-ontology baseline exists, and reproducible metrics can be reported.

## A. High-value analytical use cases

| ID | Analytical task | Ontology/KG contribution | Candidate baseline | Candidate metrics | Priority |
|---|---|---|---|---|---|
| AN-01 | Supply-network dependency and concentration | Typed actor/site/product/supply relations support graph construction without ad-hoc joins | SQL network built from source-specific tables | degree/betweenness, HHI/concentration, component/alternative-path metrics | **Very high** |
| AN-02 | Critical-medicine vulnerability | Integrates medicine criticality, sites, suppliers, alternatives, geography and regulatory context | Rule-based single-source analysis | vulnerability-query coverage, expert/official-case agreement, concentration exposure | **Very high** |
| AN-03 | Geographic ecosystem concentration | Distinguishes organization, facility, location and jurisdiction; enables cross-source geospatial joins | Source-specific map | geocoding/entity-resolution accuracy, coverage, regional concentration | **Very high** |
| AN-04 | Shortage event characterization | Connects shortage events to products, MAHs, sites, alternative products/sites and temporal evidence | descriptive shortage database | coverage, query correctness, causal-factor retrieval | High |
| AN-05 | Clinical-trial network analysis | Normalizes sponsor/collaborator/facility/intervention geography across records | direct ClinicalTrials.gov tables | network coverage, cross-country/site metrics | Medium–High |
| AN-06 | Market-access/reimbursement comparison | Separates reimbursement, price/amount, availability and geography/time | tabular comparison | coverage, temporal/geographic comparability | Medium |
| AN-07 | Pharmacovigilance evidence retrieval | Connects product/substance/safety reports/signals with provenance | keyword/product-code search | precision@k, recall@k, provenance coverage | Medium–High |
| AN-08 | Cross-representation benchmark analytics | Tests equivalent semantic questions over PostgreSQL/PostGIS and RDF/SPARQL | manual cross-checks | SQL↔SPARQL result agreement | **Very high as evaluation** |

## B. AI use cases

| ID | AI task | Why ontology/KG may matter | Baseline / comparison | Evaluation | Proposed phase |
|---|---|---|---|---|---|
| AI-01 | Cross-source entity resolution | Ontology constrains entity types, roles, identifiers and permissible mappings; provenance retains match evidence | deterministic identifier/name matching; conventional fuzzy/embedding matchers | precision, recall, F1 on curated gold subset; ambiguity rate | **Potential V2 cross-cutting evaluation** |
| AI-02 | Provenance-aware semantic QA / GraphRAG | KG supplies typed relations and source-level evidence so answers can be traced rather than generated from unstructured retrieval alone | keyword/RAG baseline without KG constraints | answer correctness, evidence precision/recall, unsupported-claim rate | Application candidate |
| AI-03 | Pharmaceutical demand forecasting with KG context | Product/substitution/clinical/supply relations can augment time-series models; literature provides a direct precedent | ARIMA/Prophet/LSTM or equivalent non-KG model | MAE, RMSE, MAPE | Future research unless admitted data strongly support it |
| AI-04 | Shortage occurrence/duration/cause prediction | Integrated product/MAH/site/alternative/history semantics may provide features and interpretable context | standard tabular ML | AUROC/F1 or duration error; calibration; feature stability | Future research / possible follow-on paper |
| AI-05 | Supplier/facility criticality prediction | Graph structure and typed dependencies support graph-learning or supervised criticality models | centrality/rule-based scoring | ranking agreement, predictive performance on observed disruptions | Future research |
| AI-06 | Graph anomaly detection | Formal relation/domain constraints improve anomaly candidates and explanations | unsupervised tabular/graph anomaly baseline | precision/recall on known/injected anomalies | Application/research candidate |
| AI-07 | Graph completion / missing-relation prediction | Ontology provides relation types/domain/range constraints that can bound link prediction | unconstrained KG embedding | MRR/Hits@k plus constraint-violation rate | Future research |
| AI-08 | Pharmacovigilance ADR/signal prioritization | Integrates product, safety and other biomedical evidence; prior KG studies show feasibility | conventional disproportionality or non-KG ML depending dataset | AUROC/AUPRC, calibration, external validation | Future extension; avoid diluting ecosystem paper |
| AI-09 | Explainable resilience/risk analytics | Risk ontology patterns + pharmaceutical dependencies can provide explanations for risk ranking | opaque score/model | predictive/task metrics + explanation fidelity/coverage | Future research |

## Evidence observations from W1
- Knowledge-graph-enhanced deep learning has been reported for pharmaceutical demand forecasting (W1-S09), supporting AI-03 as a credible future research direction rather than a speculative label.
- Machine-learning models have been used on regulatory-reported shortage cases to predict shortage duration/cause classes (W1-S10), supporting AI-04.
- Knowledge graphs have supported pharmacovigilance data integration and adverse-event prediction (W1-S11, W1-S12), supporting AI-08.
- These examples do **not** establish that CM-PharmE 2.0 will outperform baselines; they establish evaluable opportunity families.

## W1 recommendation
For the principal ontology paper, keep AI subordinate to ontology/data evaluation. The safest V2 AI candidate is **entity resolution (AI-01)** because it is directly required for heterogeneous-source integration and can be measured on a curated gold subset. Provenance-aware semantic QA (AI-02) is a strong application demonstrator, while forecasting, shortage prediction and pharmacovigilance prediction are better treated as follow-on research unless W2 exposes unusually strong datasets.
