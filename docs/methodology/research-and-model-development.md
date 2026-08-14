# Research and Model Development Method

## Purpose

This page records the reusable method used to move from research evidence to the CM-PharmE conceptual model. It is derived from the associated research but is written as repository methodology rather than manuscript prose.

## Method overview

The method is a traceable sequence:

**Problem framing → PRISMA-guided evidence review → thematic synthesis → evidence-to-domain mapping → business-architecture concern identification → UFO/OntoUML concept classification → relation selection → cardinality assignment → integrated model → demonstration and evaluation → versioned repository evidence**

## 1. Problem framing

The modeling problem is defined at ecosystem level. The target is not a single workflow or information system, but the interaction among enterprises, regulators, healthcare actors, collaborative structures, processes, normative constraints, and digital enablers.

The model objective is to provide an integrated conceptual scaffold with explicit ontological commitments and cross-domain traceability.

## 2. PRISMA-guided evidence review

The journal-oriented study reports a PRISMA 2020-guided review covering peer-reviewed work published from 2018 to 2025. The combined identification process yielded 380 records. After removing 49 duplicates, 331 records were screened; 89 full-text reports were assessed; and 17 studies were retained for qualitative synthesis.

The review focused on ontology engineering, business/enterprise architecture, conceptual modeling, and organizational or ecosystem-level concerns in pharmaceutical and healthcare contexts.

These counts are research provenance for the current model-development lineage. They are not recalculated by the repository unless a new evidence-review cycle is explicitly performed.

## 3. Thematic synthesis

The later study describes a three-stage thematic-synthesis logic consistent with Thomas and Harden:

1. line-by-line coding of extracted statements;
2. consolidation into descriptive categories;
3. abstraction into higher-order analytical themes.

Representative codes included organizational structure, enterprise capability, strategic alignment, stakeholder collaboration, partnership, governance, compliance, clinical/business process, data integration, digital platform, traceability, and semantic interoperability.

The synthesis is interpretive rather than frequency-based. A concern may be retained because it recurs across studies or because it is conceptually important to ecosystem-level representation.

## 4. Evidence-to-domain decomposition

The literature themes and the CM-PharmE domains are not one-to-one classifications. Themes organize research evidence; domains separate modeling responsibilities.

The five domains are:

- Organizational / Structural
- Ecosystem / Collaborative
- Operational / Process
- Governance / Regulatory
- Digital Transformation

The decomposition is design-oriented. For example, internal enterprise composition is separated from external ecosystem participation because they involve different identity, dependence, and mediation concerns. Governance and digital transformation remain distinct cross-cutting domains because they constrain and enable constructs across the other domains.

## 5. Business-architecture-informed concern identification

Business architecture is used as an analytical lens for deciding what kinds of ecosystem concerns require representation. The research operationalizes high-level concerns such as:

- organization design and stakeholder participation;
- capability and strategy;
- stakeholder value delivery and offerings;
- process and operating activity;
- governance, policy, and compliance;
- digital enablement and information exchange.

This does not assert full BACM conformance. Business architecture identifies relevant concerns; it does not directly determine their OntoUML stereotype.

## 6. UFO/OntoUML concept classification

Each candidate concept is reviewed according to its mode of existence and dependence.

### Kind
Used for a rigid entity type that supplies an identity principle for its instances.

### Role
Used for a context-dependent classification that an entity can contingently assume through participation in a relation or context.

### Relator
Used when a social, contractual, governance, or coordination relationship is reified and existentially depends on its participants.

### Mode
Used for an existentially dependent capability, property, signal, policy, objective, or requirement that characterizes a bearer or context.

### Perdurant
Used for a process, activity, procedure, or sequence that unfolds in time.

Classification decisions are explicit modeling commitments rather than claims of universal pharmaceutical-domain truth. CM-PharmE keeps these internal modeling commitments separate from unsupported external equivalence assertions. For maintained language/tooling context, see [Official OntoUML Ecosystem References](../references/ontouml-ecosystem.md).

## 7. Relation selection

Relation semantics follow the ontological status of the connected concepts.

- **Mediation** connects a relator to the roles or entity types participating in the corresponding relationship.
- **Characterization** connects a mode to its bearer.
- **Part-whole** relations are used only when structural composition or membership is intended.
- **Domain-specific associations** such as enables, assists, constrains, informs, records, follows, or governs are retained when available evidence supports the dependency but not a stronger ontological commitment.

The design principle is conservative commitment: do not introduce semantics stronger than the evidence and model purpose justify.

## 8. Cardinality assignment

Cardinalities are conceptual participation constraints rather than measured frequencies. Mandatory multiplicities are used only where the intended role, relator, or relation presupposes participation. Optional or multiple participation is retained when stronger restrictions are not justified.

Where the historical diagram is ambiguous or duplicated, provenance and curation status are recorded explicitly rather than silently normalized. The formal ontology engineering layer materializes this policy in the relation-cardinality registry.

## 9. Integration and cross-domain review

The integrated model is examined for whether relations connect organizational, collaborative, operational, governance, and digital concerns coherently. Cross-domain links are important because the model is intended to support ecosystem-level reasoning rather than five isolated domain diagrams.

## 10. Design-science orientation

The research aligns completed activities with the DSRM logic of problem identification, objectives, design/development, demonstration, evaluation, and communication. The alignment is a methodological and reporting structure; it is not a claim that the work completed repeated operational build-evaluate deployment cycles.

The illustrative vaccine-distribution instantiation serves as demonstration. Evaluation methods are documented separately in [Evaluation Method](evaluation-method.md).

## 11. Versioning and repository translation

Research evidence, modeling decisions, formal ontology artifacts, and evaluations are versioned separately from publication revisions. A new paper or manuscript revision does not itself create a new model release.

Stable IDs, provenance records, lifecycle states, release manifests, and frozen registries preserve traceability as the model evolves.