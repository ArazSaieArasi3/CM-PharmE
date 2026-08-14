# Why CM-PharmE Exists

## Repository narrative

CM-PharmE is maintained as an evolving conceptual model and research knowledge base, not as a copy of its associated publications. The publications explain a research study; this repository explains the artifact, its evidence, its design decisions, its evaluation state, and how it can be inspected, reused, challenged, and evolved.

The repository narrative follows a compact chain:

**Problem → Research gap → CM-PharmE response → Design method → Evidence → Evaluation → Applications → Limitations → Evolution**

## Problem

Pharmaceutical ecosystems are regulated socio-technical systems involving pharmaceutical enterprises, regulatory authorities, healthcare providers, patients, collaborative arrangements, operational and clinical processes, and digital infrastructures. These concerns are interdependent: governance constrains operations, organizational roles participate in collaborative and clinical contexts, and digital systems enable information exchange and regulated workflows.

When these concerns are modeled through disconnected architectural, process, data, or technology viewpoints, semantic traceability across the ecosystem becomes difficult. The resulting fragmentation can weaken shared understanding, governance reasoning, interoperability analysis, and downstream requirements or architecture work.

## Research gap

The research associated with CM-PharmE identified a recurring separation among several useful but only partially overlapping streams:

- pharmaceutical and healthcare ontologies often focus on clinical or data-level semantics;
- enterprise/reference-architecture studies structure organizational and digital concerns but usually do not make foundational-ontology commitments explicit;
- ecosystem, supply-chain, and process models cover multi-actor contexts but often lack a shared ontological treatment of identity, dependence, roles, relators, modes, and temporally unfolding activities;
- governance, collaboration, operations, and digital enablement are frequently represented in separate views rather than through explicit cross-domain dependencies.

CM-PharmE addresses this design space by combining business-architecture-informed concern identification with UFO/OntoUML-based ontological clarification.

## CM-PharmE response

CM-PharmE organizes the ecosystem into five interrelated modeling domains:

1. Organizational / Structural
2. Ecosystem / Collaborative
3. Operational / Process
4. Governance / Regulatory
5. Digital Transformation

The domains are not intended to be isolated silos or implementation boundaries. They separate modeling responsibilities while allowing explicit cross-domain relations and constraints.

The current stable semantic baseline contains 39 canonical concepts, 40 stable relation records, and five domains. The repository also contains an integrated modular formal ontology, stable identifiers and IRIs, executable competency questions, ROBOT/HermiT logical validation, SHACL constraints, and a reproducible build/CI pipeline while preserving the historical `v1.0.0` artifacts unchanged.

## Design logic

The core design logic is deliberately two-stage:

1. **Business-architecture concerns identify what should be represented.** Organization design, capabilities, stakeholder participation, value delivery, strategy, process, governance, and digital enablement are used as analytical lenses.
2. **UFO/OntoUML clarifies what the selected constructs mean ontologically.** Candidate concepts are classified by identity, dependence, relational, and temporal characteristics; relations and cardinalities are then selected conservatively according to the intended semantics and available evidence.

This is an analytical alignment, not a claim that CM-PharmE implements the complete BACM metamodel or that business-architecture concepts are formally equivalent to OntoUML stereotypes. See the [Official OntoUML Ecosystem References](../references/ontouml-ecosystem.md).

## Why the model matters

CM-PharmE is intended to provide a shared semantic scaffold for work such as:

- ecosystem and governance reasoning;
- cross-domain conceptual traceability;
- interoperability-oriented analysis;
- requirements elicitation and refinement;
- reference-architecture interpretation;
- standards-specific semantic mapping;
- ontology-to-knowledge-graph development;
- later DDD and architectural analysis.

These are application pathways, not claims of deployed effectiveness.

## Evidence and limitations

The model was developed from a PRISMA-guided evidence review, thematic synthesis, business-architecture-informed decomposition, and UFO/OntoUML modeling procedure. The journal-oriented research extends the published initial study with stronger evidence-to-domain traceability and a bounded multi-method assessment including expert review, focused anti-pattern inspection, competency questions, comparative scenario analysis, and illustrative vaccine-distribution instantiation.

Repository work subsequently made part of that assessment executable and reproducible: structural checks, eight competency queries, scenario validation, SHACL generation, deterministic serializations, and ROBOT/HermiT reasoning are recorded as repository evidence.

The repository preserves the evidential boundary of those studies. CM-PharmE is not currently claimed to be:

- a complete or uniquely correct ontology of the pharmaceutical ecosystem;
- empirically validated across operational pharmaceutical organizations;
- proven interoperable with implementation standards;
- a complete reference architecture implementation;
- a set of predefined DDD bounded contexts or microservices;
- free of every open ontological modeling question merely because the current logical axiom set passes HermiT.

## Relationship to the publications

The published conference paper records the initial research contribution and its early evaluation claims. The later journal manuscript, currently under review, preserves the five-domain conceptual architecture while strengthening the methodological explanation, traceability, comparative positioning, and evidential boundaries.

Repository evidence therefore distinguishes what was **reported by a publication** from what has subsequently been **reproduced or verified in the repository**. See [Publication-to-Repository Traceability](publication-to-repository-traceability.md) and the [Final Evaluation Report](../evaluations/b4-final-evaluation.md).