# Repository Artifact Index

> **Version scope:** Cross-version  
> **Status:** Stable-to-date / Evolving  
> **Updated:** 2026-09-23

## V1 / shared repository areas

| Path | Purpose |
|---|---|
| `README.md` | Project entry point and stable V1 baseline summary |
| `docs/` | Reader-oriented concepts, relations, domains, methods, evaluations, engineering, policies, research and versions |
| `catalog/` | Canonical V1 concept/relation/domain registries |
| `mappings/` | V1 concept/domain/relation/publication/data traceability |
| `ontology/` | Canonical maintained formal ontology source and distributions |
| `evaluation/` | Machine-readable evaluation inputs/results/scenarios |
| `releases/` | Preserved semantic/model release snapshots |
| `publications/` | Publication lineage and repository associations |
| `tools/` | Reproducible build/validation utilities |
| `.github/workflows/` | CI/validation workflows |
| `wiki-src/` | Source-controlled Wiki content, inventory and governance |

## V2 areas

| Path | Purpose |
|---|---|
| `v2/research/` | W0–W8 research program, gates, evidence and design records |
| `v2/ontology/` | V2 OWL/SHACL formal baseline |
| `v2/ontouml/` | V2 conceptual-model serialization/artifacts |
| `v2/data/` | relational schema, mappings, source contracts, fixtures, queries and API contract |
| `v2/evaluation/` | E1–E13 protocols/results/templates/held-out evidence |
| `v2/review/` | Human Ontology Review control layer |
| `v2/app/` | Observatory/demonstrator implementation and task evidence |
| `v2/manuscript/` | evidence-led manuscript notes/ledger/integration artifacts |
| `tools/v2_ontology/` | V2 formal build/validation |
| `tools/v2_data/` | V2 data bootstrap/KG/mapping validation |
| `tools/v2_evaluation/` | executable V2 evaluation tooling |
| `tools/v2_w8/` and `tools/v2_observatory/` | demonstrator validation/rendering tooling |

## Authority rule

Wiki pages synthesize and navigate these artifacts. They do not replace the semantic/evidential authority of the version-specific repository source.

## Branch rule

- V1 stable evidence: `main`.
- V2 evolving research evidence: `v2/research-program`.

Use exact commit refs in reproducibility/claim audits where practical.

---

<details>
<summary>Documentation record</summary>

- **Page scope:** Cross-version
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative source:** CM-PharmE repository structure on `main` and `v2/research-program`
- **Last synchronized:** 2026-09-23
- **Related issues:** #208
- **Evidence status:** Navigation index; repository artifacts remain authoritative
- **Future refresh:** #214
- **Wiki baseline:** WB-2026.09.1
- **Last synchronized ref:** V1: main; V2: v2/research-program

</details>
