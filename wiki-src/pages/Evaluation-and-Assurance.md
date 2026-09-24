# Evaluation and Assurance

> **Page scope:** Cross-version  
> **Documentation maturity:** Stable-to-date / Evolving  
> **Authoritative sources:** V1 evaluation artifacts on `main`; V2 W7/Gate evidence on `v2/research-program`  
> **Last synchronized:** 2026-09-23  
> **Related issues/PRs:** V1 evaluation lineage; #21, #98, #103, #104, #207  
> **Evidence status:** Version-specific evidence preserved; V2 E9 remains pending  
> **Future refresh:** #212, #213, #214  
> **Wiki baseline:** WB-2026.09.1

## Assurance principle

CM-PharmE does not use one aggregate quality score as a substitute for evidence. Different procedures answer different questions: syntax, logical consistency, structural integrity, semantic adequacy, mapping quality, competency questions, data conformance, generalizability, application/task behavior, human review and reproducibility must remain analytically distinct.

## V1 evaluation

V1 repository documentation organizes evidence into nine layers:
- Syntax Validation;
- Logical Consistency;
- Structural Integrity;
- Ontological Soundness;
- Semantic & Expert Validation;
- Data & Mapping Validation;
- Competency Questions;
- Application Validation;
- Research Reproducibility.

Current V1 results include PASS, PARTIAL and CONDITIONAL states. See [[V1 Evaluation Index]] and [[V1 Evaluation and Evidence]].

## V2 evaluation

V2 prospectively organizes evaluation as E1–E13:
- E1 Structural
- E2 Logical/multi-reasoner
- E3 UFO/OntoUML
- E4 Competency Questions
- E5 SHACL/data conformance
- E6 Dataset→ontology mapping
- E7 Source-semantic coverage
- E8 Held-out generalizability
- E9 Prospective expert evaluation
- E10 Ontology↔RDB↔KG consistency
- E11 Analytics/AI eligibility
- E12 Resilience scenarios
- E13 Reproducibility

At the current stable-to-date baseline, E1–E8 and E10–E13 have executed evidence; E9 is **readiness only** with **0 real expert responses**.

See [[V2 Evaluation E1-E13]].

## Assurance layers

A useful reading order is:

1. **Conceptual assurance** — OntoUML/UFO commitments and human review.
2. **Formal assurance** — syntax, profile, reasoning and structural checks.
3. **Constraint assurance** — SHACL and controlled mutation detection.
4. **Requirements assurance** — competency questions.
5. **Evidence/data assurance** — mappings, source coverage, held-out evidence.
6. **Representation assurance** — ontology↔RDB↔KG consistency.
7. **Application assurance** — representative tasks and scenario-level evidence.
8. **Human assurance** — structured expert review and author semantic review.
9. **Reproducibility assurance** — deterministic rebuilds, fingerprints and evidence regeneration.

No layer subsumes all others.

## Negative and partial evidence

Warnings, unresolved semantic findings, ambiguous mappings, held-out gaps and NOT_EXECUTED tasks are retained as evidence. They must not be silently removed to produce a cleaner narrative.

## Claim discipline

Evaluation evidence is translated into manuscript claims through explicit gate decisions. A PASS result supports only the claim scope defined by its protocol and evidence.

See [[Gate and Claim Dispositions]].

## Reproducibility

Computational reproducibility is documented separately from human/semantic validation. Rebuilding the same artifacts does not prove domain completeness or third-party scientific replication.

See [[Reproducibility Guide]].

## Authoritative navigation

- [V1 evaluation index](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/evaluations/index.md)
- [V1 machine-readable evaluation assets](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/evaluation/README.md)
- [V2 integrated W7 matrix](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w7/integrated-evaluation-evidence-matrix.md)
- [V2 claim-evidence traceability](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/evaluation/results/w7-claim-evidence-traceability.csv)
