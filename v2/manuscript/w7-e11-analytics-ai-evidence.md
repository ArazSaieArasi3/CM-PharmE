# Manuscript Evidence Note — W7-E11 Analytics and AI

## Evidence-supported statement
CM-PharmE 2.0 currently supports a bounded cross-representation analytics claim: four frozen SQL↔SPARQL benchmark pairs returned canonically equivalent answers over the ontology-aligned reference PostgreSQL/PostGIS and RDF/KG realizations. W7-E11 independently re-executed this benchmark and obtained 4/4 PASS.

## AI claim boundary
No AI performance or novelty claim is currently supported for the principal ontology article. The W7-E11 candidate registry froze 17 opportunities (8 analytics, 9 AI) before evaluation. Only AN-08 satisfied dataset→baseline→metric→ontology-dependent-hypothesis eligibility. All nine AI candidates remain deferred because at least one required empirical prerequisite is absent.

In particular, cross-source entity resolution must not be reported with precision/recall/F1 from the current fixture: only two exact schema-faithful match assertions exist and they demonstrate execution mechanics rather than real-world accuracy. GraphRAG/semantic QA lacks a frozen QA gold set and non-KG baseline; predictive forecasting, shortage, graph-learning and pharmacovigilance tasks lack frozen labeled evaluation datasets/splits and appropriate baselines.

## Reporting recommendation
The principal article should describe AI/advanced analytics as a future/application opportunity portfolio, not as a validated contribution. The empirical analytics contribution currently admissible from E11 is the bounded cross-representation consistency benchmark, with explicit reference to E10/E11 evidence.

## Evidence anchors
- eligibility freeze: `e66411966bc76a26d01223429320650a9ead50e5`
- Actions run: `32497401994` — SUCCESS
- artifact: `9452149859`
- digest: `sha256:6447825f45bd74c741358208cfe55b40acf43c6bcf4ea472180024aeddb564c8`
- report: `v2/research/w7/e11-analytics-ai-evaluation.md`

## Interpretation boundary
Deferral is not evidence of poor method performance. It means current W7 evidence does not permit a defensible measured claim. Application effectiveness, real-world entity-resolution accuracy and AI predictive gain remain unestablished.
