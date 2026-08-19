# CM-PharmE 2.0 Manuscript and Evidence Ledger

## Purpose
Keep the manuscript, repository, datasets, ontology artifacts, evaluation results, and application evidence synchronized throughout development.

## Claim lifecycle
Each manuscript claim is tracked as Proposed, Evidence pending, Supported, Bounded/qualified, Rejected, or Deferred to future work.

## Candidate claims and current evidence state
| Claim ID | Candidate claim | Required evidence | Current status |
|---|---|---|---|
| C-01 | V2 provides broader pharmaceutical-ecosystem concept coverage than V1. | V1→V2 migration matrix + concept coverage evaluation | **W3 design expansion supported; comparative coverage result pending W7** |
| C-02 | V2 is data-grounded rather than scenario-grounded. | Approved DOI/authoritative discovery sources + concept provenance | **Supported as W2/W3 research design; final ontology grounding pending W4** |
| C-03 | UFO/OntoUML commitments are more explicit/systematic. | Decision records + OntoUML evaluation | Evidence pending — W4/W7 |
| C-04 | Ontology, relational database and KG preserve traceable semantics. | Mapping rules + cross-representation tests | Evidence pending — W6/W7 |
| C-05 | V2 supports cross-jurisdiction/generalizable representation. | Protected held-out evaluation | Held-out design protected through W3; results pending W7 |
| C-06 | Selected analytics/resilience use cases can be reproducibly executed. | Demonstrator + metrics + reproducible datasets/code | Evidence pending — W6/W7 |
| C-07 | Cross-source identity, organization/site distinction, geography/jurisdiction, time and provenance are material integration needs. | W1 official evidence + W2/W3 source convergence | **Supported as bounded design need** |
| C-08 | Geospatial actor/facility integration is a defensible research demonstrator. | W1 rationale + W2 data + W3 semantic backbone + W6/W7 implementation/results | **Rationale/data/concept scope supported; results pending** |
| C-09 | Critical-medicine supply vulnerability/resilience is a defensible demonstrator. | W1 need evidence + W2 data + W3 resilience semantics + W6/W7 results | **Rationale/data/concept scope supported; results pending** |
| C-10 | AI opportunities are plausible but must not be claimed without benchmarks. | Task-specific data, baselines and metrics | Bounded / future-dependent |
| C-11 | V2 uses a deliberately multi-source discovery design rather than one schema as the ontology specification. | W2 role separation + W3 extraction/traceability | **Supported as research design** |
| C-12 | V2 reserves external sources before Core concept discovery for later generalizability evaluation. | Gate C portfolio + W3 contamination audit + W7 tests | **Design and W3 compliance supported; outcome pending W7** |
| C-13 | Public pharmaceutical data do not currently justify a claim of complete global product-level supplier→buyer→shipment reconstruction. | W2/W3 source audit | **Supported as limitation / negative finding** |
| C-14 | DOI-backed empirical anchors and operational sources can play complementary research roles. | P1/P2 + operational registry + later ETL/mappings | **Source-role design supported; implementation pending** |
| C-15 | V2 explicitly distinguishes Organization, contextual Role and physical Site/Facility. | P2/P3/C2 evidence + W3 concept/relationship inventory | **Supported as W3 conceptual requirement; foundational treatment pending W4** |
| C-16 | V2 introduces an explicit Medicinal Product–Substance–Presentation–Form–Strength–Package semantic layer. | P1/P2/P4/P5/P6 convergence + W3 inventory | **Supported as W3 conceptual requirement; foundational treatment pending W4** |
| C-17 | Essential/Critical medicine semantics are context/list/jurisdiction/version dependent rather than assumed intrinsic product kinds. | P5/P6 + W3 admission analysis | **Supported as W3 modeling requirement; final OntoUML pattern pending W4** |
| C-18 | Shortage, availability, demand and supply evidence require explicit temporal/source/context semantics. | P1/P2/P5/C1 + W3 observation design | **Supported as W3 modeling requirement; event/situation pattern pending W4** |
| C-19 | Provenance, identifier schemes and mapping assertions are first-class infrastructure for the V2 research architecture. | W1 need + W2 heterogeneous sources + W3 traceability design | **Supported as research-design requirement; formal implementation pending W5/W6** |
| C-20 | Business Architecture is retained as an optional analytical extension rather than the V2 Core decomposition principle. | V1→V2 migration + W3 admission protocol | **Supported as design decision** |

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

## Writing guidance after W3
The manuscript can now draft the Research Design and Concept Discovery procedures, including source-role separation, held-out protection, source-schema interpretation, normalization, V1 migration and concept admission. It may report the **pre-UFO discovery inventory** (80 concepts / 80 relationship semantics, with current Core/X-INFRA/Extension/Deferred distribution) only if clearly distinguished from the final ontology size.

Do not yet claim finalized UFO stereotypes, OWL consistency, mapping accuracy, cross-jurisdiction generalizability, AI performance, expert validation or demonstrator effectiveness. Those are W4–W7 results.

## Persistent limitations
- No current evidence supports completeness of a global transaction-level pharmaceutical supply graph.
- Detailed supply/procurement semantics rely substantially on conditional C1.
- Finance/counterparty remains outside Core.
- Held-out H1/H2/H3 must remain uncontaminated until the planned W7 evaluation.

## Writing rule
No result is written as completed until its corresponding repository/data evidence exists and passes the applicable gate.
