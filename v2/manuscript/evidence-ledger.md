# CM-PharmE 2.0 Manuscript and Evidence Ledger

## Purpose
Keep the manuscript, repository, datasets, ontology artifacts, evaluation results, and application evidence synchronized throughout development.

## Claim lifecycle
Each manuscript claim is tracked as Proposed, Evidence pending, Supported, Bounded/qualified, Rejected, or Deferred to future work.

## Candidate claims and current evidence state
| Claim ID | Candidate claim | Required evidence | Current status |
|---|---|---|---|
| C-01 | V2 provides broader pharmaceutical-ecosystem concept coverage than V1. | V1→V2 migration matrix + concept coverage evaluation | W3/W4 design expansion supported; comparative coverage result pending W7. |
| C-02 | V2 is data-grounded rather than scenario-grounded. | Approved DOI/authoritative discovery sources + concept provenance | **Supported as W2–W4 research design; formal ontology grounding pending W5.** |
| C-03 | UFO/OntoUML commitments are explicit/systematic. | W4 decision matrix + integrated conceptual model + semantic review | **Supported at conceptual-design level; formal/tool validation pending W5/W7.** |
| C-04 | Ontology, relational database and KG preserve traceable semantics. | Mapping rules + cross-representation tests | Evidence pending — W6/W7. |
| C-05 | V2 supports cross-jurisdiction/generalizable representation. | Protected held-out evaluation | Held-out design protected through W4; results pending W7. |
| C-06 | Selected analytics/resilience use cases can be reproducibly executed. | Demonstrator + metrics + reproducible datasets/code | Evidence pending — W6/W7. |
| C-07 | Cross-source identity, organization/site distinction, geography/jurisdiction, time and provenance are material integration needs. | W1 official evidence + W2/W3 source convergence + W4 conceptualization | **Supported as bounded design need.** |
| C-08 | Geospatial actor/facility integration is a defensible research demonstrator. | W1 rationale + W2 data + W3/W4 semantic backbone + W6/W7 implementation/results | **Rationale/data/conceptual model supported; results pending.** |
| C-09 | Critical-medicine supply vulnerability/resilience is a defensible demonstrator. | W1 need evidence + W2 data + W3/W4 resilience semantics + W6/W7 results | **Rationale/data/conceptual model supported; results pending.** |
| C-10 | AI opportunities are plausible but must not be claimed without benchmarks. | Task-specific data, baselines and metrics | Bounded / future-dependent. |
| C-11 | V2 uses a deliberately multi-source discovery design rather than one schema as the ontology specification. | W2 role separation + W3 extraction/traceability + W4 evidence-grounded decisions | **Supported as research design.** |
| C-12 | V2 reserves external sources before Core concept discovery for later generalizability evaluation. | Gate C portfolio + W3/W4 contamination discipline + W7 tests | **Design and W3/W4 compliance supported; outcome pending W7.** |
| C-13 | Public pharmaceutical data do not currently justify a claim of complete global product-level supplier→buyer→shipment reconstruction. | W2/W3 source audit | **Supported as limitation / negative finding.** |
| C-14 | DOI-backed empirical anchors and operational sources can play complementary research roles. | P1/P2 + operational registry + later ETL/mappings | **Source-role design supported; implementation pending.** |
| C-15 | V2 explicitly distinguishes Organization, contextual Role and physical Facility. | P2/P3/C2 evidence + W3 inventory + W4 identity/role analysis | **Supported as W4 conceptual commitment.** |
| C-16 | V2 introduces an explicit Medicinal Product–Substance–Presentation–Form–Strength–Package semantic layer. | P1/P2/P4/P5/P6 convergence + W3 inventory + W4 identity/quality analysis | **Supported as W4 conceptual commitment.** |
| C-17 | Essential/Critical medicine semantics are context/list/jurisdiction/version dependent rather than intrinsic product kinds. | P5/P6 + W3 admission + W4 Relator pattern | **Supported as W4 conceptual commitment.** |
| C-18 | Shortage, availability, demand and supply evidence require explicit temporal/source/context semantics. | P1/P2/P5/C1 + W3 observation design + W4 event/situation/result analysis | **Supported as W4 conceptual commitment.** |
| C-19 | Provenance, identifier schemes and mapping assertions are first-class infrastructure for the V2 research architecture. | W1 need + W2 heterogeneous sources + W3 traceability + W4 X-INFRA design | **Supported as conceptual/research-design requirement; implementation pending W5/W6.** |
| C-20 | Business Architecture is retained as an optional analytical extension rather than the V2 Core decomposition principle. | V1→V2 migration + W3 admission + W4 architecture | **Supported as W4 design decision.** |
| C-21 | Regulatory registration/authorization relations should be separated from their source records/documents/identifiers. | Regulatory-source evidence + W4 Relator analysis | **Supported as W4 conceptual commitment.** |
| C-22 | Observation activities and persistent observation results should be modeled separately. | Aggregate/regulatory source structure + W4 UFO analysis | **Supported as W4 conceptual commitment.** |
| C-23 | Supply Capacity should be separated from evidence about Supply Capacity. | W3 supply semantics + W4 Mode/Observation Result analysis | **Supported as W4 conceptual commitment.** |
| C-24 | Risk/Resilience should remain a modular extension aligned toward UFO-grounded reference ontology work rather than duplicated in Core. | W1 risk strategy + W4 extension analysis + ROSE/COVER lineage | **Supported as design decision; formal alignment pending W5/future risk work.** |

## Evidence artifacts by wave
### W1
- `v2/research/w1/evidence-sources.md`
- `v2/research/w1/stakeholder-needs.md`
- `v2/research/w1/use-case-catalog.md`
- `v2/research/w1/analytics-ai-opportunities.md`
- `v2/research/w1/geospatial-resilience-risk.md`
- `v2/research/w1/application-opportunities.md`
- `v2/research/w1/research-funding-opportunities.md`
- `v2/research/w1/demonstrator-prioritization.md`

### W2
- `v2/research/w2/dataset-landscape.md`
- `v2/research/w2/doi-dataset-registry.md`
- `v2/research/w2/operational-source-registry.md`
- `v2/research/w2/domain-source-profiles.md`
- `v2/research/w2/dataset-admission-rubric.md`
- `v2/research/w2/dataset-scorecard.md`
- `v2/research/w2/gate-c-dataset-portfolio.md`
- `v2/manuscript/w2-dataset-method-notes.md`

### W3
- `v2/research/w3/source-schema-concept-extraction.md`
- `v2/research/w3/candidate-concept-inventory.md`
- `v2/research/w3/candidate-relations-events.md`
- `v2/research/w3/geospatial-temporal-jurisdiction.md`
- `v2/research/w3/provenance-evidence-observation.md`
- `v2/research/w3/identifiers-entity-resolution.md`
- `v2/research/w3/v1-v2-migration-matrix.md`
- `v2/research/w3/evidence-traceability.md`
- `v2/research/w3/concept-admission-protocol.md`
- `v2/research/w3/gate-concept-inventory.md`
- `v2/manuscript/w3-concept-discovery-notes.md`

### W4
- `v2/research/w4/architecture.md`
- `v2/research/w4/stereotype-decision-matrix.md`
- `v2/research/w4/relator-material-patterns.md`
- `v2/research/w4/events-situations-observations.md`
- `v2/research/w4/geography-jurisdiction.md`
- `v2/research/w4/risk-resilience-extension.md`
- `v2/research/w4/business-architecture-view.md`
- `v2/research/w4/integrated-ontouml-model.md`
- `v2/research/w4/integrated-ontouml-overview.puml`
- `v2/research/w4/anti-pattern-review.md`
- `v2/research/w4/w3-w4-transformation-ledger.md`
- `v2/research/w4/gate-d-conceptual-freeze.md`
- `v2/manuscript/w4-ufo-ontouml-notes.md`

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

## Writing guidance after W4
After Gate D approval, the manuscript may describe the W4 identity/rigidity/dependence analysis, Role/RoleMixin decisions, Relator patterns, Product/Substance/Presentation distinctions, shortage Situation pattern, observation Activity/Result split, provenance/identifier infrastructure, and modular Risk/BA architecture.

The W4 model contains **87 named conceptual types/pattern elements** (32 Core, 25 X-INFRA, 30 Extensions). This must be reported as a conceptual-model count, not an OWL class count. The increase from W3's 80 candidates reflects semantic splits/truth-makers rather than uncontrolled concept discovery.

The W4 anti-pattern review was manual/static against OntoUML semantic rules; do not label it an automated validation run.

Do not yet claim OWL DL consistency, HermiT/ROBOT success for V2, SHACL data conformance, mapping accuracy, held-out generalizability, AI performance or demonstrator effectiveness. Those are W5–W7 results.

## Persistent limitations
- No current evidence supports completeness of a global transaction-level pharmaceutical supply graph.
- Detailed supply/procurement semantics rely substantially on conditional C1.
- Finance/counterparty remains outside Core.
- Held-out H1/H2/H3 must remain uncontaminated until the planned W7 evaluation.
- Exact native OntoUML JSON serialization/tool validation and formal OWL encoding are implementation tasks after Gate D.

## Writing rule
No result is written as completed until its corresponding repository/data evidence exists and passes the applicable gate.
