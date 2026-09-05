---
artifact_type: human_ontology_review_control_center
ontology_id: CM-PharmE
ontology_version: 2.0.0-alpha.1
review_candidate: RC-V2-HORP-01
review_status: active
---

# CM-PharmE 2.0 — Human Ontology Review Control Center

This is the ordered human-review entry point for CM-PharmE 2.0. It is a review projection over the authoritative V2 research, OntoUML, OWL, data and evaluation artifacts; it is not a second semantic source of truth.

## Review candidate
- **Ontology:** CM-PharmE 2.0
- **Candidate:** RC-V2-HORP-01
- **Integration line:** `v2/research-program`
- **Human-review pilot:** [#173](https://github.com/ArazSaieArasi3/CM-PharmE/issues/173)
- **Current semantic baseline:** 87 conceptual elements across 17 canonical domains
- **Main-branch boundary:** CM-PharmE 1.x reviewer-facing `main` remains out of scope
- **Overall disposition:** Pending author review

## Ordered review path

| Step | Review Surface | Scope | Status | Reviewer Action | Link |
|---:|---|---|---|---|---|
| 0 | Project status | V2 program | Ready | Orient | [V2 program issue](https://github.com/ArazSaieArasi3/CM-PharmE/issues/24) |
| 1 | Whole-Ontology Simple View | 87 concepts / 17 domains | Ready | Inspect global conceptual shape | [Open](ontology-overview.md) |
| 2 | Domain Catalog | 17 domains | Ready | Review domain names, definitions and boundaries | [Open](domains/index.md) |
| 3 | Domain Diagrams | 17 diagrams | Ready | Inspect per-domain concept/relationship structure | [Open](../research/w4/visual-ontology-package.md) |
| 4 | Concept Catalog | 87 concepts | Ready | Prioritize concept review | [Open](concepts/index.md) |
| 5 | Concept Provenance Matrix | 87 concepts | Ready | Review V1 lineage, datasets, external support and evidence gaps | [Open](../research/w4/human-review-concept-provenance-matrix.md) |
| 6 | Concept Evidence Passports | Per concept | Planned | Deep review of selected concepts | [#173 Phase 2](https://github.com/ArazSaieArasi3/CM-PharmE/issues/173) |
| 7 | Relation Catalog | All relations | Planned | Review source/target/direction/evidence | [#173 Phase 2](https://github.com/ArazSaieArasi3/CM-PharmE/issues/173) |
| 8 | Version Evolution Package | V1→V2 | Partial | Review justified continuity and justified change | Existing W0/W4 migration artifacts; HORP package pending |
| 9 | Evaluation Diagnostic Report | E1–E13 | Partial | Diagnose warnings, gaps and claim boundaries | W7 evidence; HORP diagnostic projection pending |
| 10 | Human Findings | Author feedback | Active | Record findings and convert accepted findings to issues | [#159](https://github.com/ArazSaieArasi3/CM-PharmE/issues/159) / future HRF records |
| 11 | Release Candidate Re-review | Whole V2 | Pending | Final human sign-off | Later Gate H |

## Current priority
1. Inspect the Whole-Ontology Simple View.
2. Review the 17-domain catalog and per-domain diagrams.
3. Use the Concept Catalog to select a domain/concept for deep review.
4. For each selected concept, cross-check the existing provenance matrix until Concept Evidence Passports are generated.
5. Record semantic feedback before any semantic change is applied.

## Human-review dispositions
`APPROVE / APPROVE_WITH_WORDING_CHANGE / REVISE_SEMANTICS / RE_STEREOTYPE / SPLIT / MERGE / MOVE_DOMAIN_MODULE / DEFER / REJECT`

## Existing evidence anchors
- [Integrated OntoUML model](../research/w4/integrated-ontouml-model.md)
- [W3→W4 transformation ledger](../research/w4/w3-w4-transformation-ledger.md)
- [Concept provenance matrix](../research/w4/human-review-concept-provenance-matrix.md)
- [Visual ontology package](../research/w4/visual-ontology-package.md)
- [Evaluation evidence status](../evaluation/results/w7-evidence-status.csv)
- [Manuscript evidence ledger](../manuscript/evidence-ledger.md)

## HORP source standards
This pilot instantiates the Human Ontology Review Procedure (HORP) defined in OGCM-RF and composes it with the generic review lifecycle in `araz-research-portfolio`.
