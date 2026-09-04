# CM-PharmE 2.0 — Integrated Manuscript Draft 0

**Working title**  
CM-PharmE 2.0: A Data-Grounded UFO/OntoUML Ontology and Knowledge Infrastructure for the Global Pharmaceutical Ecosystem

**Draft status:** D0 — integrated evidence-backed skeleton  
**Repository line:** CM-PharmE 2.0 only  
**Main-branch boundary:** CM-PharmE 1.x reviewer-facing `main` is out of scope.

---

## Draft-control rules

1. Every substantive result claim must resolve to the V2 evidence ledger, W7 claim-evidence traceability matrix, W8 evidence, or an explicitly marked pending/deferred item.
2. E9 expert evaluation is method/readiness only until real eligible expert responses are collected and analyzed under the frozen protocol.
3. W8 application claims are bounded to implemented and evaluated demonstrator tasks; no production-readiness, universal usability, predictive, causal, market-completeness or AI-performance claims are admitted without dedicated evidence.
4. V1 remains prior work and baseline lineage. V2 novelty must be stated as a qualitative and architectural/evidential delta unless a like-for-like quantitative V1 denominator exists.
5. Project-native OntoUML checks are not presented as official OntoUML-tool certification.
6. Repository-level reproducibility is not described as independent third-party replication.

---

## Abstract — D0 placeholder

CM-PharmE 2.0 extends the earlier CM-PharmE conceptual ecosystem model into a data-grounded, UFO/OntoUML-based pharmaceutical domain ontology and knowledge infrastructure. The research combines multi-source evidence acquisition, evidence-driven concept discovery, ontological analysis, modular conceptualization, OWL 2 DL formalization, SHACL constraints, ontology-aligned relational and knowledge-graph realizations, and a prospective multi-family evaluation program. The current Gate-D baseline contains 87 conceptual elements organized as Core, cross-cutting infrastructure, and extension elements. The formal alpha baseline represents these commitments using 81 OWL classes, six datatypes, 52 object properties and five datatype properties, while the data-infrastructure layer provides PostgreSQL/PostGIS, a deterministic RDF ABox, registered ontology-to-relational mappings, provenance structures and paired SQL/SPARQL benchmark queries. Evaluation covers structural, logical, OntoUML, competency-question, SHACL, mapping, coverage, held-out generalizability, cross-representation consistency, analytics, resilience and reproducibility evidence; expert evaluation remains prospectively frozen and pending real participant evidence. Application demonstrators expose actor/facility, entity/relationship, knowledge-graph, analytics and resilience views, with provenance-aware semantic search and representative-task evaluation still in progress. The contribution is therefore bounded to an evidence-traceable ontology and knowledge-infrastructure architecture with demonstrated formal consistency, reproducible reference realizations and selected ecosystem analyses, rather than claims of universal pharmaceutical completeness, production readiness or predictive effectiveness.

**D0 TODO:** tighten to target-journal word limit after journal selection; insert final W8 and E9 outcomes only when evidence exists.

---

## 1. Introduction

### 1.1 Problem
The pharmaceutical ecosystem spans medicinal products and substances, organizations and facilities, manufacturing and supply relationships, logistics, regulatory authorization, clinical evidence, pharmacovigilance, market access, reimbursement, digital/data infrastructure, geography/jurisdiction and resilience concerns. These concerns are represented across heterogeneous scientific, regulatory and operational data sources and are commonly separated by domain-specific schemas and information systems.

### 1.2 Research gap
Existing domain resources are valuable but do not, by themselves, provide one traceable conceptual-to-formal-to-data architecture for representing cross-domain pharmaceutical ecosystem semantics while preserving explicit ontological commitments, provenance, jurisdictional context and application-facing realizations.

### 1.3 Evolution from CM-PharmE 1.x
CM-PharmE 1.x established a five-domain business-architecture-informed and ontology-grounded conceptual baseline. CM-PharmE 2.0 changes the center of gravity from a business-architecture-informed conceptual reference model toward a data-grounded pharmaceutical domain ontology and knowledge infrastructure. Business-architecture semantics remain a compatible analytical view rather than the dominant organizing principle.

**Claim boundary:** no quantitative V1→V2 coverage-superiority claim is made because no like-for-like V1 denominator has been established.

### 1.4 Research questions
**RQ1.** How can heterogeneous pharmaceutical-ecosystem concepts and data be systematically conceptualized using UFO/OntoUML while preserving identity, relational semantics, modularity, provenance and contextual roles?

**RQ2.** To what extent can CM-PharmE 2.0 consistently integrate and represent heterogeneous real-world pharmaceutical datasets across formal ontology, relational-database and knowledge-graph representations?

**RQ3.** To what extent does the resulting ontology support reproducible cross-domain and resilience-oriented pharmaceutical ecosystem analyses?

### 1.5 Contributions — D0
C1. A data-grounded CM-PharmE 2.0 conceptual architecture with 87 Gate-D elements across Core, cross-cutting infrastructure and extensions.

C2. UFO/OntoUML analysis that makes identity, roles, relators, events, modes, information objects and protected distinctions explicit.

C3. An OWL 2 DL formal alpha implementation with SHACL constraints, deterministic builds and multi-reasoner evidence.

C4. An ontology-aligned PostgreSQL/PostGIS and RDF/KG realization with registered mappings, provenance mechanics and paired SQL↔SPARQL benchmarks.

C5. A prospective multi-family evaluation architecture with held-out evidence, cross-representation consistency checks, resilience scenarios and clean computational reproducibility.

C6. A bounded observatory/demonstrator layer exposing ontology-backed ecosystem tasks while maintaining explicit non-claims.

**Pending contribution evidence:** real E9 expert results; final V2-082 semantic/search evidence; V2-083 representative-task evaluation.

---

## 2. Background and Research Lineage

### 2.1 Pharmaceutical ecosystem modeling
D0 TODO: synthesize only sources already registered in the V2 evidence registry plus verified literature used for final manuscript positioning.

### 2.2 Ontology engineering, UFO and OntoUML
D0 TODO: explain identity, rigidity, relational dependence, relators, roles, modes and events at the level required to understand design decisions; cite primary methodological sources.

### 2.3 CM-PharmE 1.x lineage
D0 TODO: explicitly cite the published IEEE CM-PharmE ver.1 work and the journal-version lineage when bibliographic status is appropriate; separate inherited foundations from V2 novelty.

### 2.4 Related ontologies, standards and knowledge infrastructures
D0 TODO: build final comparison table after journal target is clearer. External mappings must not be converted into standards-conformance claims without dedicated evaluation.

---

## 3. Research Design and Evidence Protocol

### 3.1 Overall design
The V2 program follows a prospective design-science and ontology-engineering workflow: requirements and competency questions → evidence acquisition → concept/relation discovery → normalization → UFO analysis → OntoUML conceptualization → formal OWL/SHACL realization → relational/KG realization → multi-family evaluation → bounded application demonstrators → reproducible research release.

### 3.2 Evidence acquisition and source roles
Evidence is separated into research benchmark datasets and authoritative operational sources. Dataset/source admission records provenance, source role, access/licensing constraints and intended use. Discovery leads are not treated as validated evidence until admitted under the project protocol.

### 3.3 Dataset landscape
Primary/authoritative evidence used across the program includes admitted pharmaceutical reimbursement/utilization, regulatory/product, critical-medicine/shortage and essential-medicine sources. Conditional and held-out sources are analytically separated from discovery/admission sources.

D0 TODO: insert final source table from W2 with DOI, authority, access path, license/terms status and role in discovery vs held-out evaluation.

### 3.4 Held-out discipline
Held-out sources are used after the conceptual baseline is frozen to test cross-source/cross-jurisdiction pressure without changing the first-pass ontology merely to improve the held-out result.

### 3.5 Concept admission lifecycle
Candidate → Normalized → Evidence-backed → UFO-analyzed → Accepted Core / Cross-cutting Infrastructure / Extension / Rejected / Deferred.

Each accepted concept should be traceable through evidence, domain rationale, UFO category, OntoUML stereotype, formal representation and evaluation evidence.

---

## 4. Evidence-Driven Concept Discovery and V1→V2 Evolution

### 4.1 Candidate discovery
W3 produced a normalized pre-UFO candidate inventory from source evidence, schema mining and V1 migration analysis.

### 4.2 Gate-D conceptual baseline
The approved conceptual baseline comprises 87 elements: 32 Core, 25 cross-cutting infrastructure and 30 Extensions.

### 4.3 Migration treatments
V1 concepts are explicitly treated as retained, refined, renamed, split, merged, deprecated, moved to extension or complemented by new V2 concepts rather than being silently overwritten.

### 4.4 Human-review control surface
The V2 human-review package contains an 87-concept provenance matrix, visual domain diagrams, provenance-gap taxonomy, risk-first review queue, bounded evidence packets and an empty-by-default disposition log. Real author/reviewer dispositions are recorded only after actual review activity.

**Boundary:** this author/human review infrastructure is distinct from E9 prospective expert evaluation and is not expert-validation evidence by itself.

---

## 5. UFO/OntoUML Conceptualization

### 5.1 Conceptual architecture
D0 TODO: insert final 17-domain presentation architecture and explain that domains are review/organization views rather than automatically equivalent to software bounded contexts.

### 5.2 Key ontological commitments
Representative decisions include Organization and Facility as identity-bearing kinds; contextual participant, manufacturer, importer, regulatory and logistics roles; explicit relators for authorization/registration/market-listing patterns; distinction of product/substance/presentation; geography vs regulatory jurisdiction; observation activity vs observation result; and separate risk/resilience extension semantics.

### 5.3 Protected distinctions
The evaluation protects high-consequence distinctions including Organization/Facility, Geography/RegulatoryJurisdiction, MedicinalProduct/Substance/Presentation, ObservationActivity/ObservationResult and SupplyCapacity/ObservationResult.

### 5.4 OntoUML evaluation boundary
Project-native checks support internal stereotype agreement and protected-distinction preservation. They are not reported as official OntoUML-tool conformance certification.

---

## 6. Formal Ontology and Constraint Layer

### 6.1 OWL 2 DL implementation
Formal version `2.0.0-alpha.1` contains 642 asserted triples representing the Gate-D baseline through 81 OWL classes, six datatypes, 52 object properties and five datatype properties.

### 6.2 Constraints and SHACL
The alpha formal layer includes 11 SHACL NodeShapes and a controlled mutation-based validation procedure.

### 6.3 Logical evaluation
The formal baseline passes the project OWL 2 DL profile gate, with HermiT/JFact reporting zero named unsatisfiable classes and 91/91 named subclass-pair agreement for the evaluated scope.

### 6.4 Reproducible formal build
E13 reproduces the canonical formal fingerprint in two clean builds and regenerates structural/logical evidence under a captured environment.

---

## 7. Ontology-Aligned Relational and Knowledge-Graph Realization

### 7.1 Relational backbone
The reference realization uses PostgreSQL/PostGIS with entity, entity type, identifier, relation assertion, source dataset, evidence/provenance, temporal validity, jurisdiction and geography structures plus domain projections.

### 7.2 Ontology↔RDB mapping
The W6 baseline contains 36 registered ontology↔RDB mappings.

### 7.3 RDF/KG realization
The reference ABox contains 398 triples with canonical KG fingerprinting and deterministic regeneration.

### 7.4 SQL↔SPARQL equivalence suite
Four frozen SQL↔SPARQL benchmark pairs support consistency for the registered reference representation.

**Boundary:** this does not establish universal lossless RDB↔RDF equivalence, production-scale ingestion or real-world entity-resolution accuracy.

---

## 8. Multi-Family Evaluation

### 8.1 Evaluation design
Evaluation separates structural, logical, conceptual/OntoUML, competency-question, SHACL/data, mapping, source coverage, held-out generalizability, expert, representation-consistency, analytics, resilience and reproducibility evidence. No composite quality score is used.

### 8.2 E1–E8 and E10–E13 summary
- E1 Structural: PASS WITH WARNING.
- E2 Logical/multi-reasoner: mandatory PASS with bounded datatype warnings.
- E3 UFO/OntoUML: PASS WITH WARNING.
- E4 Competency questions: PASS, 18/18 frozen outcomes.
- E5 SHACL/data: PASS WITH WARNING; pristine conformance plus 8/8 controlled mutations detected.
- E6 Mapping: PASS WITH WARNING; 39/39 decisions explicit, 36/38 in-scope direct/derived/bounded, 0 unmapped.
- E7 Coverage: PASS WITH WARNING; 74/97 exact and 88/97 exact-or-partial.
- E8 Held-out: PASS WITH WARNING; 38/51 exact-or-partial, 0 first-pass Core identity conflicts.
- E10 RDB/KG consistency: PASS WITH WARNING; 36 mappings resolve and 4/4 paired SQL↔SPARQL queries pass for the reference suite.
- E11 Analytics/AI: PASS WITH DEFERRED AI; no AI novelty/performance claim.
- E12 Resilience: PASS WITH WARNING; 5/5 frozen scenario outcomes with provenance.
- E13 Reproducibility: PASS WITH WARNING; 54/54 clean rebuild checks pass.

### 8.3 Gate F claim adjudication
Gate F approved progression with bounded claim dispositions. Fifteen claims are admitted with normal scoped wording, twelve require explicit bounds, selected-task claims remain task-bounded, one evidence limitation is retained, and unsupported demonstrator/entity-resolution performance claims remain deferred.

### 8.4 E9 expert evaluation — pending empirical evidence
The E9 protocol, 23-item instrument, analysis plan, ethics/data-governance boundary and participant package are frozen/recruitment-ready. Final readiness validation passed 27/27 checks. Real eligible participant responses have not yet been collected.

**Manuscript-safe wording:** the expert-evaluation protocol is prospectively specified and operationally ready.  
**Prohibited wording until evidence exists:** experts validated/confirmed/approved/rated CM-PharmE 2.0.

---

## 9. Application Demonstrators / Global Pharmaceutical Ecosystem Observatory

### 9.1 Scope
The observatory is an application of the ontology/data infrastructure rather than the design authority for the ontology.

### 9.2 Completed W8 surfaces
D0 current implemented surfaces include the observatory baseline, actor/facility map, entity/relationship browser, knowledge-graph explorer, analytics dashboard and bounded resilience/risk view.

### 9.3 V2-082 — pending
Provenance-aware semantic/search assistance is tracked in #169. The design must prioritize auditable semantic retrieval and provenance surfacing and must separate retrieval evidence from any generative layer.

### 9.4 V2-083 — pending
Representative-task evaluation is tracked in #170 and will freeze task statements, expected outcomes, evidence paths and success/failure criteria before final interpretation.

---

## 10. Discussion

### 10.1 What V2 establishes
The current evidence supports a traceable progression from heterogeneous pharmaceutical source evidence through conceptual commitments and formal ontology into reproducible reference relational/KG realizations and selected ecosystem analyses.

### 10.2 What V2 does not establish
V2 does not claim universal pharmaceutical-domain completeness, full global product-supplier-buyer-shipment reconstruction, production-scale ingestion, production readiness, exact external-standard conformance, predictive shortage/resilience validity, causal effectiveness, AI novelty/performance or real-world entity-resolution accuracy without dedicated evidence.

### 10.3 Generalizability and extension pressure
Held-out evaluation shows meaningful exact/partial coverage while also exposing extension pressure, particularly in areas such as clinical trials and selected resilience/recovery semantics. These negative/partial findings are retained as evidence rather than normalized away.

### 10.4 Research and infrastructure contribution
D0 TODO: sharpen depending on journal selection: semantic-resource emphasis vs biomedical-informatics methodology vs conceptual-modeling emphasis.

---

## 11. Threats to Validity and Limitations

1. Source coverage is broad but does not prove global domain completeness.
2. Held-out generalizability is bounded to the selected held-out sources/jurisdictions.
3. Reference RDB/KG execution uses controlled schema-faithful fixtures for reproducible integration evidence and does not imply full operational-source ingestion.
4. Current project-native OntoUML checks are not official-tool certification.
5. Selected datatype and extension-modeling warnings remain bounded limitations.
6. Controlled resilience scenarios establish representational/query behavior, not predictive or causal validity.
7. Computational reproducibility is repository-level and not independent third-party replication.
8. Real E9 expert-result evidence is pending.
9. W8 semantic/search and representative-task evaluation are pending.
10. External standards/risk-ontology mappings are not conformance certifications unless separately tested.

---

## 12. Reproducibility and Research Release

The repository provides deterministic ontology/KG builds, fingerprints, validation artifacts, executable query suites and evidence ledgers. The final paper track will package the frozen ontology, mappings, benchmark data permitted for redistribution, provenance records, RDB dump/schema, RDF snapshot, executable CQs/benchmarks and manuscript-evidence traceability into a DOI-backed research release.

**Pending:** final DOI/release work item V2-090.

---

## 13. Conclusion — D0 placeholder

CM-PharmE 2.0 develops the CM-PharmE research line from a conceptual ecosystem model into a data-grounded ontology and knowledge infrastructure whose conceptual, formal, relational, graph and application layers are explicitly traceable to evidence and evaluation. The current results support formal consistency, bounded cross-source coverage, reproducible reference realizations and selected ecosystem analyses while preserving explicit limitations and deferred claims. The remaining pre-submission work is concentrated in V2 branch consolidation, real human expert evidence, provenance-aware semantic/search assistance, representative-task demonstrator evaluation, the reproducible DOI release, journal-fit selection and final manuscript↔repository↔data traceability.

---

## D0 evidence/TODO register

| Manuscript area | Current evidence state | Remaining action |
|---|---|---|
| Introduction/novelty | Evidence-backed qualitative V1→V2 delta | final literature positioning and target-journal framing |
| Research design/data | Strong W0–W3 records | final source table and methods prose |
| UFO/OntoUML | Gate-D + E3 | finalize figures/citations and human-review dispositions |
| Formal ontology | W5 + E1/E2/E5/E13 | final release version/fingerprint |
| RDB/KG | W6 + E10/E13 | final release bundle |
| Evaluation | E1–E8, E10–E13 complete | E9 real expert collection/analysis |
| Observatory | 6/8 W8 items complete | #169, #170, Gate G |
| Reproducibility | repository-level evidence strong | DOI package and third-party-use instructions |
| Journal selection | not frozen | execute after D0/1 contribution profile stabilizes |
| Final submission | not authorized | Gate H only after release/traceability/journal freeze |
