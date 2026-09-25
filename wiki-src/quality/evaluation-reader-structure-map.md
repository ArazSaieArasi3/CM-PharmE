# WIKI-27 — Frozen Evaluation Reader-Structure Map

Issue: #238  
Status: **FROZEN BEFORE PROSE REFACTOR**  
Date: 2026-09-25  
Branch: `wiki/238-evaluation-reader-refactor`

## Purpose

Freeze the reader-facing evaluation information architecture before editing prose. This prevents a cleaner narrative from silently changing scientific meaning, current evidence states, or provenance.

## Governing interpretation rules

1. Reader-facing labels come first; E1–E13 and Gate identifiers remain retrievable technical/provenance references.
2. Protocol, execution, observed result, claim disposition, and limitation are distinct layers.
3. PASS does not mean universal validity, domain completeness, production readiness, human validation, or independent replication unless the underlying evidence explicitly supports that scope.
4. Negative, partial, warning, bounded, deferred, NOT_EXECUTED, and pending states remain visible.
5. E9 remains **readiness only with 0 real expert responses**.
6. Current representative-task evidence remains **6 PASS / 3 NOT_EXECUTED** until #170 is advanced with auditable post-freeze evidence.
7. Demonstrator evaluation and research-release readiness remain pending where current evidence says they are pending.
8. Repository-level reproducibility must not be described as third-party independent scientific replication.

## Current → target reader structure

| Current Wiki surface | Current role/problem | Frozen target reader-facing role | Technical/provenance retained |
|---|---|---|---|
| `Evaluation-and-Reproducibility-Guide.md` | Navigation hub already mostly reader-centered | **Evaluation & Reproducibility Guide** — primary entry path answering what was evaluated, what evidence exists, what is supported, and what is reproducible | Cross-links to V1/V2 technical evidence |
| `Evaluation-and-Assurance.md` | Cross-version assurance overview; some internal decision language remains | **Evaluation & Assurance** — explain assurance families first, then result/boundary, with a compact evaluation architecture diagram | E1–E13 and historical/internal decision refs in reference sections |
| `V2-Evaluation-E1-E13.md` | Technical matrix organized primarily by E IDs | **CM-PharmE 2.0 Evaluation Framework** — descriptive labels first; E1–E13 as stable technical IDs | Exact E IDs, quantitative evidence, authoritative artifacts |
| `Gate-and-Claim-Dispositions.md` | Visible title already reader-friendly but slug is historical | **Evidence Scope and Supported Claims** — supported, bounded, selected-only, deferred, and explicit limitations | Gate A–H only in collapsible/internal-provenance mapping |
| `V2-Manuscript-and-Claim-Traceability.md` | Manuscript-oriented claim mapping with Gate-F-centric prose | **Claim & Manuscript Traceability** — Claim → Evidence → Result → Boundary → Manuscript use | Claim IDs C-01..C-32; internal Gate-F decision record |
| `Evaluation-Artifact-Index.md` | Artifact index | **Evaluation Evidence Index** — artifact-oriented lookup, not narrative explanation | Exact repository paths, workflow runs, artifacts |
| `Reproducibility-Guide.md` | Cross-version reproducibility navigation | **Reproducibility Guide** — distinguish deterministic rebuild, evidence regeneration, and independent replication | Fingerprints, runs, archived evidence |
| `V2-Reproducibility-and-Release-Plan.md` | V2 lifecycle/release detail | **V2 Reproducibility & Release Readiness** — current reproducibility evidence plus unresolved release dependencies | Gate-H/release-control refs |
| `V2-Research-Program-and-Gates.md` | Research process with historical Gate vocabulary in slug | **CM-PharmE 2.0 Research Method and Development** — descriptive stage names first | Gate IDs preserved as provenance/history |
| `V2-Limitations-and-Deferred-Work.md` | Limitations/deferred work | **Limitations & Deferred Evidence** — explicit negative-space companion to supported claims | IDs/issues/research dependencies |

## Frozen reader journey

**Evaluation & Reproducibility Guide**  
→ **Evaluation & Assurance**  
→ **CM-PharmE 2.0 Evaluation Framework**  
→ **Evidence Scope and Supported Claims**  
→ **Claim & Manuscript Traceability**  
→ **Reproducibility Guide / Limitations & Deferred Evidence**  
→ **Evaluation Evidence Index** for audit-level detail.

## Required semantic separation inside each substantive evaluation page

Each evaluation family/claim should, where applicable, expose these fields in this order:

1. **What was evaluated**
2. **Why it matters**
3. **Protocol / method**
4. **Observed result**
5. **Warning / limitation**
6. **Supported claim**
7. **Unsupported or deferred claim**
8. **Reproducibility path**
9. **Technical/provenance reference**

## Negative-evidence invariants

The following statements are frozen and must survive the refactor without semantic weakening:

- E9: **0 real expert responses**; no admissible expert-result claim.
- E11: no AI novelty/performance claim; only AN-08 is benchmark-supported and 16 candidates remain deferred.
- E12: scenario-level representational adequacy only; no predictive/causal/intervention-effectiveness or operational-resilience claim.
- E13: repository-level clean GitHub-hosted CI reproducibility, **not** third-party independent replication.
- C-13: current public evidence is insufficient for complete global product→supplier→buyer→shipment reconstruction.
- C-32: entity-match mechanics are supported; real-world precision/recall is not evaluated.
- Representative tasks: current result remains **6 PASS / 0 PARTIAL / 0 FAIL / 3 NOT_EXECUTED**.
- Demonstrator evaluation and research-release readiness remain pending until their governed dependencies are dispositioned.

## Change control

This map is the pre-edit baseline for #238. Any later page merge, split, rename, redirect, or navigation change must preserve:
- claim IDs;
- E-family IDs;
- exact negative/partial/pending states;
- authoritative evidence links;
- future synchronization hooks to #212/#214.
