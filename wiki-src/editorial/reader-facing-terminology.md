# Reader-facing terminology policy

**Status:** Active editorial policy for CM-PharmE Wiki  
**Program:** #228  
**Implementation issue:** #229  
**Baseline preserved:** WB-2026.09.1 evidence and research semantics

## Purpose

CM-PharmE uses internal identifiers such as workstream codes, decision checkpoints, issues and review-control names to manage research execution. These identifiers are valuable for provenance, but they should not be the vocabulary a reader must learn in order to understand the research.

This policy separates **reader-facing terminology** from **internal provenance terminology**.

## Core rule

Use a descriptive scientific/technical term first. Preserve the exact internal identifier only where it helps provenance, audit or repository navigation.

Good:

> The conceptual baseline contains 87 modeled elements. The corresponding internal decision record is Gate D.

Avoid:

> Gate D froze 87 elements.

The first form explains the research fact before exposing the project-control label.

## Classification

| Internal term/pattern | Reader-facing treatment | Provenance treatment |
|---|---|---|
| W0–W8 / Wave | Use descriptive stage name | Internal stage ID may appear secondarily |
| Gate A–H | Use descriptive decision/checkpoint name | Exact Gate ID retained in evidence/history |
| Gate D | Conceptual Baseline | Internal checkpoint: Gate D |
| Gate F | Evidence Sufficiency Review | Internal checkpoint: Gate F |
| Gate G | Demonstrator Evaluation | Internal checkpoint: Gate G |
| Gate H | Research Release Readiness | Internal checkpoint: Gate H |
| Formal Gate | Formal Ontology Readiness | Internal identifier retained where needed |
| Human Ontology Review | Semantic Review | Existing repository artifact names remain unchanged |
| Human Review Control Center | Semantic Review Control Center in Wiki prose | Repository path/title may remain exact when linked |
| W5 Closure | Formal Ontology implementation/closure record | Exact artifact filename retained in link target |
| W6 Closure | Data Infrastructure implementation/closure record | Exact artifact filename retained in link target |
| E1–E13 | Descriptive evaluation-family name first | E-number retained as technical reference ID |
| Issue/PR number | Avoid as narrative vocabulary | Retain in Documentation Record/evidence links |

## Canonical reader-facing page titles

| Compatibility slug/source file | Canonical visible title |
|---|---|
| V2-Research-Program-and-Gates | CM-PharmE 2.0 Research Method and Development |
| V2-Evaluation-E1-E13 | CM-PharmE 2.0 Evaluation Framework |
| V2-Human-Ontology-Review | CM-PharmE 2.0 Semantic Review |
| Gate-and-Claim-Dispositions | Evidence Scope and Supported Claims |

Compatibility slugs remain temporarily stable. #230 may later perform a coordinated slug migration with redirects/deprecation pages if the information-architecture redesign justifies it.

## Where internal terminology may remain

Internal labels are appropriate in:
- Documentation Record / provenance sections;
- exact repository artifact names and paths;
- issue/PR references;
- historical decision logs;
- technical evaluation reference tables where IDs are useful;
- changelog and synchronization records.

They should not dominate:
- Home;
- Sidebar;
- introductory paragraphs;
- H1/H2 navigation titles;
- research narrative;
- explanatory summaries.

## Review terminology

The public-facing term is **Semantic Review** or **Ontology Review**, depending on context.

Do not use “Human” as branding merely to contrast human work with automation/AI. Where the fact of expert or researcher review is methodologically important, say so directly in the explanatory text.

## Evidence-preservation rule

Editorial relabeling must not:
- change a status;
- alter a count;
- change a supported/deferred claim;
- hide a warning or limitation;
- convert an internal checkpoint into a scientific result;
- rename authoritative repository artifacts silently.

## Quality test

A new reader should be able to understand the main research and technical documentation without knowing what W6, Gate F, HORP, an issue number or a branch name means.

A maintainer should still be able to recover every relevant internal identifier from provenance/evidence links.
