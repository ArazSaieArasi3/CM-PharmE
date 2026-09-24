# CM-PharmE Wiki information architecture — reader-centered revision

**Issue:** #230  
**Date:** 2026-09-24  
**Principle:** domain-oriented reader navigation with version-aware content underneath.

## Previous top-level structure

```text
Home
├── Project Overview
├── Version Selector
│   ├── CM-PharmE 1.x pages
│   └── CM-PharmE 2.0 pages
├── V1 → V2 Evolution and Traceability
├── Evaluation / Validation / Assurance / Reproducibility
├── Applications and Demonstrators
├── Publications / Citation / Releases
├── Reference Indexes
├── Documentation Governance
└── Current Synchronization Checkpoints
```

The previous structure was complete and version-aware, but the Home page carried a large page list and exposed repository/program structure before reader intent.

## Target structure

```text
Home / Start Here
├── Research Guide
├── Ontology and Conceptual Model Guide
├── Data and Database Guide
├── Knowledge Graph and Queries Guide
├── Evaluation and Reproducibility Guide
├── Applications Guide
├── Publications and Citation Guide
├── Reference Guide
└── Documentation History and Governance
```

Each landing page owns a coherent reader question and links to version-specific or reference pages below it. V1/V2 remain explicit inside the relevant guide.

## Design decisions

### Home
Home is a portal, not the complete table of contents. It provides:
- reader-intent paths;
- version shortcuts;
- one-paragraph documentation-area summaries;
- current high-level status.

### Landing pages
Landing pages provide the detailed second navigation layer. Existing substantive pages remain authoritative explanatory/reference pages.

### Version separation
V1 and V2 are not merged into one undifferentiated topic tree. Where both versions are relevant, the landing page groups them separately or labels cross-version material explicitly.

### Governance
Documentation lifecycle, QA and branch/repository rules remain fully available, but they no longer dominate the primary research reading path.

## Compatibility-slug and redirect plan

The visible titles introduced under #229 use descriptive terminology while the following compatibility slugs remain stable:
- `V2-Research-Program-and-Gates`
- `V2-Evaluation-E1-E13`
- `V2-Human-Ontology-Review`
- `Gate-and-Claim-Dispositions`

Decision for #230: **retain the existing slugs** because the visible navigation already presents the new canonical titles and retaining URLs avoids unnecessary link churn. If a future baseline migrates the slugs, the old slug must be retained as a deprecation/redirect page and all inbound links must be audited.

## Navigation-depth contract

For the current Wiki:
- Home = depth 0.
- Section landing page or deliberate version shortcut = depth 1.
- Substantive/reference page = depth <=2.
- A deeper path requires an explicit documented exception.

The automated navigation checker enforces this contract for every source-complete inventory page.

## Relationship to future work

- #231 refactors metadata presentation.
- #232 establishes the formal diagram standard.
- #239 adds tutorials/how-to journeys.
- #242 formalizes multi-profile Home composition for reuse beyond CM-PharmE.
