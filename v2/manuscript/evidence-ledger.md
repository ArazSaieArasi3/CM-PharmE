# CM-PharmE 2.0 Manuscript and Evidence Ledger

## Purpose
Keep the manuscript, repository, datasets, ontology artifacts, evaluation results, and application evidence synchronized throughout development.

## Claim lifecycle
Each manuscript claim is tracked as Proposed, Evidence pending, Supported, Bounded/qualified, Rejected, or Deferred to future work.

## Candidate claims and current evidence state
| Claim ID | Candidate claim | Required evidence | Current status |
|---|---|---|---|
| C-01 | V2 provides broader pharmaceutical-ecosystem concept coverage than V1. | V1→V2 migration matrix + dataset/literature coverage evidence | Evidence pending — W3/W7 |
| C-02 | V2 is data-grounded rather than scenario-grounded. | Admitted DOI-backed/authoritative datasets + concept provenance | **Dataset strategy supported at W2; ontology grounding pending W3** |
| C-03 | UFO/OntoUML commitments are more explicit/systematic. | Decision records + OntoUML evaluation | Evidence pending — W4/W7 |
| C-04 | Ontology, relational database and KG preserve traceable semantics. | Mapping rules + cross-representation tests | Evidence pending — W6/W7 |
| C-05 | V2 supports cross-jurisdiction/generalizable representation. | Protected held-out evaluation | Held-out design established at W2; results pending W7 |
| C-06 | Selected analytics/resilience use cases can be reproducibly executed. | Demonstrator + metrics + reproducible datasets/code | Evidence pending — W6/W7 |
| C-07 | Cross-source identity, organization/site distinction, geography/jurisdiction, time and provenance are material integration needs. | W1 official/application evidence | **Bounded support** |
| C-08 | Geospatial actor/facility integration is a defensible research demonstrator. | W1 rationale + W2 data + W6 implementation + W7 metrics | **W1 rationale + W2 feasible source portfolio supported; results pending** |
| C-09 | Critical-medicine supply vulnerability/resilience is a defensible demonstrator. | W1 need evidence + W2 data + reproducible analysis | **W1 rationale + W2 criticality/shortage/supply-source portfolio supported; results pending** |
| C-10 | AI opportunities are plausible but must not be claimed without benchmarks. | Task-specific data, baselines and metrics | Bounded / future-dependent |
| C-11 | V2 uses a deliberately multi-source discovery design rather than one schema as the ontology specification. | W2 landscape + admission protocol + role separation | **Supported as research design** |
| C-12 | V2 reserves external sources before Core concept discovery for later generalizability evaluation. | Gate C portfolio + W3 compliance + W7 tests | **Design supported; Gate C pending** |
| C-13 | Public pharmaceutical data do not currently justify a claim of complete global product-level supplier→buyer→shipment reconstruction. | W2 source audit | **Supported as a limitation / negative finding** |
| C-14 | DOI-backed empirical anchors can support relational/KG realization while operational sources provide complementary domain structures. | D01/D02 + operational registry + later ETL/mappings | W2 source availability supported; implementation pending |

## W1 evidence artifacts
- `v2/research/w1/evidence-sources.md`
- `v2/research/w1/stakeholder-needs.md`
- `v2/research/w1/use-case-catalog.md`
- `v2/research/w1/analytics-ai-opportunities.md`
- `v2/research/w1/geospatial-resilience-risk.md`
- `v2/research/w1/application-opportunities.md`
- `v2/research/w1/research-funding-opportunities.md`
- `v2/research/w1/demonstrator-prioritization.md`

## W2 evidence artifacts
- `v2/research/w2/dataset-landscape.md`
- `v2/research/w2/doi-dataset-registry.md`
- `v2/research/w2/operational-source-registry.md`
- `v2/research/w2/domain-source-profiles.md`
- `v2/research/w2/dataset-admission-rubric.md`
- `v2/research/w2/dataset-scorecard.md`
- `v2/research/w2/gate-c-dataset-portfolio.md`
- `v2/manuscript/w2-dataset-method-notes.md`

## Manuscript skeleton
1. Introduction
2. Background and prior CM-PharmE lineage
3. Research design and dataset admission protocol
4. Concept discovery and evidence traceability
5. UFO/OntoUML conceptualization
6. Formal ontology and constraints
7. Relational/KG realization and data integration
8. Evaluation
9. Application demonstrator(s)
10. Discussion
11. Limitations
12. Conclusion

## Writing guidance after W2
The Research Design section may describe the dataset-admission rubric, DOI-backed vs operational-source distinction, source-role separation and pre-reserved held-out design. It may identify candidate/admitted sources only after Gate C approval.

The manuscript must state the negative W2 finding transparently: the current public-source landscape does not support a completeness claim for a global transaction-level pharmaceutical supply network. Regulatory actor/site, product, shortage and criticality sources remain valuable but are not equivalent to a complete supplier–buyer–shipment graph.

No W2 evidence permits claims of ontology coverage, mapping accuracy, generalizability, AI performance or resilience-analytics effectiveness. Those remain W3–W7 results.

## Writing rule
The manuscript is updated after each wave, but no result is written as completed until its corresponding repository/data evidence exists and passes the applicable gate.
