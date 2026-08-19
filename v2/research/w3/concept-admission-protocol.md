# W3 Concept and Relation Admission Protocol

## Purpose
Apply explicit, auditable rules before UFO/OntoUML modeling so the V2 inventory is neither a copy of source schemas nor an unconstrained brainstorming list.

## 1. Admission unit
An admission decision applies to a **normalized semantic candidate**, not directly to a CSV column, database table, API field, UI label, V1 class, or technology name.

## 2. Required evidence fields
Each admitted candidate must have:
1. normalized preferred term;
2. working definition/scope;
3. evidence source(s) or V1 lineage;
4. source role (primary/conditional/secondary/lineage);
5. reason the distinction matters to RQ/demonstrator or reusable ontology infrastructure;
6. preliminary Core/Extension/X-INFRA disposition;
7. V1 migration status where applicable;
8. candidate UFO interpretation to investigate in W4;
9. known boundary/ambiguity;
10. held-out contamination check.

## 3. Admission statuses
### CORE candidate
Admit when the semantic distinction is broadly necessary for the pharmaceutical ecosystem and is supported by convergent primary/authoritative evidence or a strong authoritative source plus independent use-case/V1 evidence.

### X-INFRA candidate
Admit when the distinction is cross-cutting infrastructure required for geography/time, identifiers, evidence/provenance, mapping or reproducibility across multiple domain modules. It does not become a pharmaceutical domain concept merely because it is necessary infrastructure.

### EXT candidate
Admit to a named modular extension when the concept is valid and evidence-backed but would over-specialize the principal Core or belongs primarily to market access, supply/resilience, safety, risk, BA, digital/application or clinical care.

### DEFER
Retain in backlog when useful for a future use case but not necessary/evidenced enough for the principal V2 ontology/article.

### REJECT
Reject when the item is:
- only a source-format artifact;
- merely a label/string/value rather than a semantic distinction;
- redundant with a normalized candidate;
- technology-specific with no durable domain semantics;
- supported only by held-out data intended for later evaluation;
- legally/ethically unusable as the sole basis for a research claim;
- outside the approved research scope.

## 4. Hard methodological exclusions
1. **Held-out schema leakage:** H1/H2/H3 cannot justify W3 Core admission.
2. **Column-to-class fallacy:** fields such as `patients_num`, `costs`, coordinates, or status strings are not automatically classes.
3. **Identifier-to-entity fallacy:** NDC/ATC/NHIF/GeoNames/license values do not themselves define the real-world entity type.
4. **Technology lock-in:** Blockchain, AI-CDSS, EHR, GraphRAG or specific database technologies are not Core ontology concepts merely because an application uses them.
5. **Unlicensed evidence dependency:** a concept based only on a conditional/restricted source cannot become a strong Core novelty claim without independent support.
6. **Overgeneralized supply network:** no complete global supplier→buyer→shipment relation is admitted from currently available public evidence.

## 5. Core-strength rubric
For prioritization only; not a statistical validation score.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Source convergence | no admitted source | one admitted source | ≥2 independent/admitted source families |
| Ecosystem centrality | peripheral/future | one module/use case | cross-module / principal demonstrator |
| V1/use-case continuity | none | one supporting lineage/use-case | multiple independent rationale signals |
| Representation necessity | can remain attribute/value | useful explicit concept | flattening would lose identity/context/event/relational semantics |
| Reuse/generalization value | source-specific only | jurisdiction/module-specific | reusable across jurisdictions/modules |

Guidance:
- 8–10: strong CORE/X-INFRA candidate.
- 5–7: Extension or conditional Core review.
- 0–4: Extension/Defer/Reject unless a strong qualitative rationale overrides.

This rubric supports consistency but does not replace expert UFO/OntoUML analysis.

## 6. Applied admission summary
| Disposition | Count | Main families |
|---|---:|---|
| CORE | **29** | organizations/roles/sites; jurisdiction; product/substance/presentation; manufacturing/distribution; shortage; demand/availability/supply observations |
| X-INFRA | **23** | geography/time; data source/dataset/record/assertion; provenance; identifiers; entity-match semantics |
| EXT | **26** | market access; detailed supply/resilience; safety; risk; BA/partnerships; digital/application; clinical roles |
| DEFER | **2** | detailed clinical pathway/activity pattern; public–private partnership arrangement in principal V2 scope |
| REJECT as normalized inventory item | Source-specific fields/technology duplicates are recorded as mappings, values or deprecated V1 forms rather than counted as candidate concepts | e.g., patient count as Patient, generic blockchain ledger as Core, generic V1 Ecosystem Relationship |

Total normalized candidate concepts: **80**.

## 7. Relation admission rules
A relation is retained when it captures a semantically meaningful dependency/participation/authorization/location/classification/provenance/mapping pattern. Generic relations are split when evidence consistently distinguishes relation types.

Special rules:
- site–organization relation must not imply legal identity;
- jurisdiction–geography relation must not imply identity;
- product–classification relation must preserve scheme/context;
- shortage–product relation must preserve case/time/source context;
- supply-dependency relations remain extension/bounded until stronger product-level network evidence exists;
- entity-match relations retain evidence/confidence and avoid uncontrolled `owl:sameAs`.

## 8. W4 handoff
The Concept Inventory Gate freezes **scope and evidence**, not final foundational semantics. W4 may:
- merge candidates that are ontologically the same;
- split candidates that conflate object/role/relator/event/result;
- change Core↔Extension placement with explicit rationale;
- reject candidates after identity/rigidity/dependence analysis;
- introduce upper-level abstractions necessary to make the OntoUML model coherent.

Any W4 addition not traceable to W3 evidence must be recorded as a **foundational modeling addition**, not silently presented as data-discovered.
