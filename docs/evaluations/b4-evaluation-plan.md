# B4 Evaluation Plan — Paper-Grounded Validation

## Objective

B4 translates the evaluation logic reported in the two CM-PharmE publications into a versioned, repository-native evidence program. The goal is not to repeat the manuscripts, but to make their evaluation claims inspectable, traceable, progressively reproducible, and capable of being strengthened by computational or empirical evidence.

The stable semantic baseline remains `v1.0.0`. B4 is an evaluation cycle and does not by itself declare a new semantic release.

## Evaluation inputs

B4 uses the following inputs:

- the canonical concept/relation/domain registries;
- the B3 modular formal ontology source and cardinality registry;
- the published conference paper as historical research evidence;
- the journal manuscript under review as the primary source for the strengthened evaluation method and evidential boundaries;
- the eight manuscript competency questions;
- the eight manually inspected OntoUML-informed anti-pattern categories;
- the illustrative vaccine-distribution scenario;
- the publication references that define the methodological basis of the review, modeling, and evaluation procedures.

## Principle: publication evidence versus repository verification

B4 distinguishes four things that must not be conflated:

1. a result reported by the published paper;
2. a result reported by the journal manuscript;
3. a result whose provenance has been recorded in the repository;
4. a result independently reproduced or computationally verified from repository artifacts.

This distinction is especially important where the earlier paper used stronger evaluation language than the later manuscript.

## Work packages

### B4.1 — Evaluation evidence normalization

Create machine-readable registries for competency questions, anti-pattern observations, scenarios, and publication-derived claims. Each record receives an identifier, source, status, result boundary, and target verification method.

**Acceptance condition:** publication-derived evidence is traceable without converting historical claims into current verification claims.

### B4.2 — Structural and traceability validation

Cross-check concepts, relations, domains, cardinalities, lifecycle states, and mappings across source model, registries, B3 formal source, and evaluation records.

**Acceptance condition:** no unexplained dangling entity, missing stable ID, or untraceable B4 evidence reference.

### B4.3 — Logical/reasoner validation

Run a documented OWL reasoner workflow and record consistency, unsatisfiable classes, and tool/version evidence.

**Acceptance condition:** exact toolchain and results are captured. If the ontology fails, the failure is preserved as evidence and becomes an explicit issue; no consistency claim is made until resolved.

### B4.4 — OntoUML-informed anti-pattern re-evaluation

Revisit the eight historical inspection categories and, where feasible, broaden the inspection or connect it to tool-supported checks. Particular attention is given to the two minor issues reported in the journal manuscript:

- mediation specificity for Supply Chain Relationship;
- possible misuse/ambiguity of the Public–Private Partnership Structure part-whole relation.

**Acceptance condition:** each historical observation has a current repository status and rationale.

### B4.5 — Competency-question execution

Preserve the eight manuscript CQs as the initial CQ baseline, connect each to concepts/relations/domains, and implement executable SPARQL tests where representative data permits.

**Acceptance condition:** every CQ has an explicit conceptual status; executable CQs record query, dataset/sample, expected result, and observed result.

### B4.6 — Scenario and instance validation

Use the vaccine-distribution scenario as the first reference instantiation and add machine-readable sample assertions in a later B4 sub-batch where appropriate.

**Acceptance condition:** scenario elements map to stable CM-PharmE identifiers and cross-domain dependencies without inventing unsupported new core classes.

### B4.7 — Expert and semantic evidence

Normalize the four-expert qualitative evidence from the journal manuscript into a traceable evidence format. Do not invent unpublished quotations, scores, demographic details, or consensus statistics.

**Acceptance condition:** documented feedback categories and author actions are represented with their original evidential boundary.

### B4.8 — Application and pragmatic validation

Trace model constructs to selected downstream uses: governance analysis, requirements derivation, architecture interpretation, standards mapping, and computational/knowledge-graph use.

**Acceptance condition:** each pathway clearly distinguishes conceptual support from deployed or measured effectiveness.

### B4.9 — Reproducibility assessment

Produce an evaluation matrix that connects each claim to input artifacts, evidence, tools, results, publications, and remaining gaps.

**Acceptance condition:** an independent reader can determine what was tested, what was only reported historically, what passed, what remains untested, and which commit/release each result applies to.

## Initial E1–E9 matrix

| Layer | B4 target | Starting evidence |
|---|---|---|
| E1 Syntax | Re-run and record parse/format checks | B3 structural reference-package PASS |
| E2 Logic | Execute reasoner and record results | Not yet repository-evidenced |
| E3 Structure | Cross-registry and mapping validation | B2/B3 audits |
| E4 Ontology | Reassess ontology commitments and anti-pattern findings | Manual eight-category inspection in journal manuscript |
| E5 Semantic | Normalize expert feedback and terminology findings | Four-expert qualitative review |
| E6 Data/Mapping | Add representative mapping/instance checks | Illustrative scenario only |
| E7 CQ | Version and execute CQs where feasible | Eight traceability-based CQs |
| E8 Application | Test bounded analytical pathways | Vaccine scenario and practical guidelines |
| E9 Reproducibility | Link evidence to commits, sources, and methods | Release manifests + publication lineage |

## Explicit non-claims during B4

Until corresponding evidence exists, B4 must not claim:

- complete ontology validation;
- universal pharmaceutical-domain completeness;
- empirical effectiveness;
- technical interoperability or standards conformance;
- reference-architecture adoption;
- statistically representative expert validation;
- exhaustive anti-pattern clearance;
- computational consistency before reasoner evidence is recorded.

## Expected B4 outputs

B4 is expected to produce a structured evaluation package rather than a manuscript chapter. Primary outputs include:

- evaluation method documentation;
- competency-question registry and queries;
- anti-pattern registry;
- scenario evidence;
- publication evidence matrix;
- logical/structural/semantic result records;
- evaluation traceability matrix;
- final B4 assessment with explicit remaining gaps.

A later pull request will be opened only after the B4 evidence package is audited for internal consistency.