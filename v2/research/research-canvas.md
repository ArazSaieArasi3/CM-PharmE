# CM-PharmE 2.0 Research Canvas

## Research problem
Pharmaceutical ecosystem knowledge is fragmented across product, organization, facility, regulation, supply, logistics, clinical, safety, reimbursement, digital, geographic, and resilience data. Existing resources are often schema-specific, jurisdiction-specific, operationally siloed, or weakly connected to foundational ontology.

## Research objective
Develop and evaluate a data-grounded pharmaceutical ecosystem ontology and knowledge infrastructure that:
1. is conceptually grounded in UFO and modeled in OntoUML;
2. integrates heterogeneous real-world evidence and datasets;
3. supports formal OWL/SHACL implementation;
4. maintains traceability across ontology, relational database, and RDF knowledge graph representations;
5. enables reproducible ecosystem analytics and selected resilience-oriented applications.

## Proposed research questions
**RQ1.** How can heterogeneous pharmaceutical-ecosystem concepts and data be systematically conceptualized using UFO/OntoUML while preserving identity, relational semantics, modularity, provenance, and contextual roles?

**RQ2.** To what extent can CM-PharmE 2.0 consistently integrate and represent heterogeneous real-world pharmaceutical datasets across formal ontology, relational-database, and knowledge-graph representations?

**RQ3.** To what extent does the resulting ontology support reproducible cross-domain, geospatial, and resilience-oriented pharmaceutical ecosystem analyses?

## Novelty hypotheses
1. **Data-grounded ontology evolution** — concept and relation admission is supported by traceable literature, schema, dataset, and domain evidence.
2. **UFO/OntoUML-first conceptualization** — identity, rigidity, dependence, relators, events, modes, roles, and temporal participation are treated explicitly before OWL implementation.
3. **Ontology–RDB–KG traceability** — semantics are mapped and tested across OntoUML, OWL/SHACL, PostgreSQL/PostGIS, and RDF/KG representations.
4. **Cross-source and cross-jurisdiction evaluation** — discovery and evaluation use multiple DOI-backed and authoritative datasets, including a held-out evaluation set.
5. **Pharmaceutical ecosystem intelligence** — the ontology supports concrete analytical use cases such as actor/facility mapping, supply dependencies, shortage/resilience analysis, market-access analysis, semantic search, and provenance-aware AI.

## Scope model
### Core ontology
Stable domain semantics for pharmaceutical ecosystem entities, roles, relators, activities/events, products/substances, facilities/sites, locations/jurisdictions, regulatory objects, evidence/provenance, and cross-domain dependencies.

### Extensions / views
- Business Architecture View
- Risk & Resilience Extension
- Clinical/Trial Extension
- Pharmacovigilance Extension
- Supply & Logistics Extension
- Pricing/Reimbursement/Finance Extension
- Digital/Data Extension
- Standards Mapping Modules

## Data strategy
- Primary research datasets: DOI-backed, downloadable, legally reusable, documented schema/data dictionary, suitable provenance.
- Secondary datasets: complementary DOI-backed sources.
- Authoritative operational sources: official public sources such as regulatory, trial, product, facility, and market data where DOI is not expected.
- Held-out datasets: not used for core concept discovery; reserved for generalizability evaluation.

## Application strategy
Three levels are maintained:
1. **Research Demonstrators** — must be evaluated in the V2 paper.
2. **Application Candidates** — may be prototyped in the repository.
3. **Future Research Opportunities** — documented but outside the main article scope.

Candidate applications include:
- global actor and manufacturing/facility map;
- pharmaceutical ecosystem browser;
- supply dependency and concentration analytics;
- shortage/resilience analysis;
- regulatory/jurisdiction comparison;
- clinical-trial and sponsor/site linkage;
- pricing/reimbursement/market-access analysis;
- provenance-aware semantic search and GraphRAG;
- entity resolution and data integration support;
- AI-supported anomaly, risk, and shortage analysis.

## Evaluation families
A. Conceptual/UFO evaluation
B. Formal/logical evaluation
C. Constraint/data-conformance evaluation
D. Competency-question evaluation
E. Dataset/mapping evaluation
F. Provenance evaluation
G. Cross-representation evaluation
H. Generalizability / held-out evaluation
I. Prospective structured expert evaluation
J. Application/task evaluation
K. Resilience scenario evaluation
L. Reproducibility evaluation

## Publication strategy
The principal V2 article should focus on ontology design, data grounding, cross-representation realization, and rigorous evaluation. The observatory and resilience components may support separate follow-on publications if their evaluation becomes substantial enough to dilute the main ontology contribution.

## Working title
**CM-PharmE 2.0: A Data-Grounded UFO/OntoUML Ontology and Knowledge Infrastructure for the Global Pharmaceutical Ecosystem**
