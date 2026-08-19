# W4 Manuscript Notes — UFO/OntoUML Conceptualization

Status: working manuscript evidence; W4 results may be described after Gate D approval, but formal OWL/evaluation results remain W5–W7 work.

## Research-design narrative
After W3 evidence-driven discovery, the admitted semantic inventory was not translated directly into OWL classes. W4 first applied UFO/OntoUML analysis to distinguish identity providers, anti-rigid roles, relational truth-makers, intrinsic modes/qualities, events, situations, information objects and contextual assignments.

This intermediate conceptualization step is important because source schemas frequently collapse ontologically different things into adjacent fields or records. Examples resolved in W4 include:
- Organization vs physical Facility;
- geography vs regulatory jurisdiction;
- Product vs Substance vs Presentation;
- identifier value vs entity identity;
- regulatory record vs underlying authorization/registration relation;
- shortage record vs shortage situation;
- observation activity vs observation result;
- supply capacity vs evidence about supply capacity;
- essential/critical status vs intrinsic Product type.

## W4 method statements supportable after Gate D
The manuscript may state that:
1. W4 applied explicit identity, rigidity and dependence analysis before formalization.
2. Contextual pharmaceutical actor concepts were modeled as Roles/RoleMixins rather than rigid Kinds when role acquisition/loss does not change bearer identity.
3. Relationship concepts with independent validity/evidence/commitment semantics were modeled using Relator/Mediation patterns.
4. Manufacturing/distribution/provenance/assessment processes were separated from shortage/stockout situations and from persistent information results.
5. Business Architecture was retained as an optional analytical extension rather than a Core identity/decomposition mechanism.
6. Risk/Resilience was designed as a modular adapter intended for alignment with UFO-grounded risk reference work rather than duplicating generic risk semantics in the Core.
7. The W4 conceptual model was manually reviewed against OntoUML semantic/anti-pattern principles before formal OWL translation.

## Result framing
W4 produced a Gate-D candidate model containing 87 named conceptual types/pattern elements: 32 Core, 25 cross-cutting infrastructure and 30 extension elements. This count must be described as a **conceptual-model count**, not an OWL-class count.

The W3→W4 increase from 80 candidates should be explained as semantic refinement/splitting, not scope inflation. The main examples are:
- Observation → Activity + Result;
- Product Classification → Scheme + Entry + Assignment;
- Supply Capacity Observation → Capacity Mode + Observation Result;
- Identifier → Value + Scheme + Assignment;
- Risk Treatment → Plan + Activity;
- introduction of explicit truth-makers such as Facility Operation and Evidence Support.

## Novelty discipline
Do not claim UFO/OntoUML itself as V2 novelty. The contribution is the evidence-driven pharmaceutical conceptualization and the systematic use of foundational distinctions to resolve weaknesses/ambiguities identified from V1 and heterogeneous source data.

Do not claim that the W4 manual anti-pattern review is an automated tool validation. Machine-readable OntoUML/OWL validation is a later engineering/evaluation step.

## Suggested paper subsection structure
### 5. UFO/OntoUML Conceptualization
5.1 Identity, rigidity and role analysis
5.2 Organization–Facility–Jurisdiction pattern
5.3 Medicinal Product–Substance–Presentation pattern
5.4 Relators for authorization, registration, listing and classification
5.5 Event–Situation–Observation distinctions
5.6 Provenance and identifier infrastructure
5.7 Core/Extension architecture
5.8 Semantic design review and remaining boundaries

## References to include in final bibliography
- OntoUML/UFO foundational literature and current OntoUML specification.
- Guizzardi foundational work on ontological foundations for structural conceptual models.
- Oliveira et al. (2022), ROSE, DOI 10.1007/978-3-031-17995-2_26, for risk-extension alignment discussion.

## Claims still prohibited at W4
- successful OWL DL consistency;
- HermiT/ROBOT results for V2;
- SHACL conformance of V2 datasets;
- RDB/KG mapping accuracy;
- held-out generalizability;
- complete global supply-network coverage;
- measured AI/entity-resolution performance.

Those remain W5–W7 evidence requirements.
