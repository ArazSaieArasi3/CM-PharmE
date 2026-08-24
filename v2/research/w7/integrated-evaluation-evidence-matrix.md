# CM-PharmE 2.0 — Integrated W7 Evaluation Evidence Matrix

## Purpose
This document is the reviewer- and manuscript-facing synthesis of the prospective W7 evaluation program. It keeps evaluation families analytically distinct, connects them to claim boundaries, and prevents stronger wording than the retained evidence supports.

Machine-readable claim traceability: `v2/evaluation/results/w7-claim-evidence-traceability.csv`.

## Evaluation-family matrix

| Family | Focus | Primary evidence | Result | Manuscript contribution | Required boundary |
|---|---|---|---|---|---|
| E1 | Structural/ontology quality | 87/87 conceptual registry; 36/36 mapping IRIs; 8/8 protected distinctions | PASS WITH WARNING | Structural integrity and traceability baseline | Annotation/domain/range completeness is descriptive, not ontology completeness |
| E2 | OWL 2 DL and multi-reasoner logic | HermiT/JFact exit 0; 0 unsatisfiable named classes; 91/91 subclass-pair agreement | Mandatory gate PASS; family WARN | Logical processability of current axiom set | Six project-native datatype compatibility warnings; no full datatype-level equivalence claim |
| E3 | UFO/OntoUML commitments | 17 executable checks; 87/87 stereotype agreement; 8/8 protected distinctions | PASS WITH WARNING | Conceptual-model discipline and preservation of Gate-D decisions | Project-native review, not official OntoUML-tool conformance; extension warnings retained |
| E4 | Competency questions | 18 frozen CQs; 8/8 positive and 10/10 negative outcomes | PASS | Requirements-oriented executable validation | Negative ASK results are regression/consistency checks under open-world semantics |
| E5 | SHACL/data conformance | pristine profiles 0 findings; 8/8 controlled mutations detected | PASS WITH WARNING | Constraint executability and defect sensitivity | Fixture-bounded; only 3/11 W5 shapes had direct focus nodes in the reference fixture |
| E6 | Dataset→ontology mapping | 39/39 decisions explicit; 36/38 in-scope direct/derived/bounded; 2 ambiguous; 0 unmapped; 12/12 audit | PASS WITH WARNING | Data-grounding and field-level traceability | Quantitative mapping strongest for frozen P1/P2 contracts; bounded/ambiguous mappings remain explicit |
| E7 | Concept/relation coverage | 97 requirements; 74/97 exact; 88/97 exact-or-partial; relations 33/34 bounded | PASS WITH WARNING | Source-semantic coverage and retained gaps | Not global domain completeness and not a like-for-like V1 percentage comparison |
| E8 | Held-out generalizability | 51 frozen requirements; 38/51 exact-or-partial; 0 first-pass Core identity conflicts | PASS WITH WARNING | Cross-source/cross-jurisdiction first-pass evidence | H2/H3 stronger than H1; bounded generalizability, not global completeness |
| E9 | Prospective expert review | protocol/instrument frozen; 27/27 readiness checks | READINESS ONLY | Prospective human-evaluation method | **0 real responses; no expert-result claim is admissible yet** |
| E10 | Ontology↔RDB↔KG consistency | 36 mappings; 14/14 class, 10/10 relation, 44/44 identity checks; 4/4 SQL↔SPARQL | PASS WITH WARNING | Cross-representation semantic traceability | Registered/reference scope only; not universal lossless bidirectional equivalence |
| E11 | Analytics/AI eligibility | 17 candidates audited; only AN-08 benchmark-supported; 4/4 benchmark | PASS WITH DEFERRED AI | Evidence-based claim discipline for analytics/AI | 0 AI performance/novelty claims; unsupported tasks deferred rather than fabricated |
| E12 | Resilience scenarios | 5 frozen scenarios; 5/5 query outcomes and provenance; sensitivity mechanism | PASS WITH WARNING | Scenario-level representational adequacy for resilience use | No predictive, causal, intervention-effectiveness or operational-resilience claim |
| E13 | Reproducibility | clean rebuild; 54/54 checks; ontology and KG fingerprints reproduced byte-identically | PASS WITH WARNING | Repository-level computational reproducibility | Not third-party independent replication; human E9 evidence excluded |

## Cross-family synthesis

### Conceptual and formal adequacy
E1–E3 jointly support the claim that the frozen Gate-D/W5 baseline is structurally traceable, logically processable on the evaluated axiom set, and consistent with the project's explicit UFO/OntoUML commitments. The evidence is strongest for the protected Core distinctions. Extension-level warnings remain visible for selected Relators, Role dependence and Mode bearer semantics.

### Requirements and constraint adequacy
E4–E5 show that frozen competency questions execute with their expected outcomes and that SHACL profiles are executable and sensitive to predefined controlled defects. These results do not establish universal domain truth or conformance of every external dataset.

### Empirical grounding and coverage
E6–E8 provide the principal data-grounding evidence. Source-field mapping decisions are explicit, semantic coverage is measurable with retained gaps, and held-out first-pass evaluation was performed without pre-test ontology adaptation. The evidence supports bounded multi-source and cross-jurisdiction reuse; it does not support global completeness.

### Representation and application mechanics
E10 supports traceable semantics across the registered ontology, relational and KG reference representations. E11 prevents unsupported AI claims, while E12 supports only controlled resilience-scenario representation. Strong usability, operational effectiveness, production-scale analytics and AI claims remain W8 or future-study questions.

### Reproducibility
E13 independently regenerates the computable W5–W7 evidence in a fresh GitHub-hosted environment and reproduces the frozen ontology/KG fingerprints. This is computational reproducibility of the repository pipeline, not external-team replication.

### Human expert evidence
E9 is methodologically prepared but empirically incomplete. Its protocol, participant package and readiness checks can be described as prospective method evidence only. No manuscript Results statement may imply expert validation before real eligible responses are collected and analyzed.

## Gate-F claim disposition pre-analysis
The detailed 32-claim matrix is stored in `w7-claim-evidence-traceability.csv`. Before the formal Gate-F decision, the evidence suggests:

- **15 claims** are candidates for approval with normal scope wording;
- **12 claims** require explicit bounded/qualified wording;
- **1 claim** is supportable only for selected evaluated tasks;
- **1 claim** is retained as an explicit limitation;
- **1 claim** (C-01) should be narrowed because a like-for-like quantitative V1 denominator is unavailable;
- **2 downstream performance claims** should remain deferred: W8 geospatial demonstrator effectiveness and real-world entity-resolution accuracy.

These are recommendations for Gate F, not the Gate-F decision itself.

## Reviewer-facing limitations that must remain visible
1. No complete global product→supplier→buyer→shipment reconstruction is claimed.
2. The W6 reference realization uses deterministic schema-faithful fixtures; full-source ingestion is not implied by fixture conformance.
3. Held-out generalizability is bounded to the selected H1–H3 source families and shows material clinical-trial extension pressure.
4. No AI novelty/performance, shortage prediction, GraphRAG utility, graph-learning performance or production application effectiveness is currently supported.
5. Controlled resilience scenarios do not establish predictive or causal validity.
6. Project-native OntoUML checks are not official OntoUML-tool certification.
7. The clean rebuild is repository-level computational reproducibility, not third-party replication.
8. Expert evaluation results remain pending real recruitment and collection.
9. Extension formalization gaps remain documented for selected mediation, bearer, recovery and treatment-link semantics.
10. Exact conformance to external standards or a separate risk ontology is not claimed without dedicated alignment evaluation.

## Manuscript integration map
- **Introduction/Contribution:** C-01 must be qualitative/bounded; C-02, C-03, C-04, C-05 can be stated with explicit evaluated scope.
- **Research design/data protocol:** E6–E8, C-10–C-14.
- **UFO/OntoUML conceptualization:** E3, C-15–C-24.
- **Formal ontology/constraints:** E1, E2, E5, C-25–C-28.
- **RDB/KG realization:** E10, C-29–C-32.
- **Evaluation:** all E1–E13, with E9 placed under prospective/pending expert evidence rather than Results.
- **Application demonstrators:** C-08/C-09; operational effectiveness stays outside current evidence until W8.
- **Discussion/limitations:** E7/E8/E11/E12/E13 boundaries and all retained negative findings.

## Closure condition for W7 synthesis
The computational and documentary W7 evidence package is sufficiently consolidated for Gate-F claim adjudication. E9 remains open as a separate human-evidence dependency and can be integrated later without rewriting or reconstructing prior evidence.