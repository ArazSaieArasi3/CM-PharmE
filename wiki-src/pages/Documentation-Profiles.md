# Documentation Profiles

> **Version scope:** Version-neutral  
> **Status:** Stable pilot for CM-PharmE  
> **Updated:** 2026-09-24

CM-PharmE separates documentation by **reader responsibility**, so research/ontology material is not mistaken for product, engineering or business documentation.

## Profiles used by CM-PharmE

| Profile | State | What it covers here | Start here |
|---|---|---|---|
| **Research / Ontology** | Active — primary | research method, conceptual model, ontology, evolution, evaluation, reproducibility, publications | [[Research Guide]] · [[Ontology and Conceptual Model Guide]] · [[Evaluation and Reproducibility Guide]] |
| **Data / Engineering** | Active — supporting | datasets, provenance, PostgreSQL/PostGIS, mappings, RDF/KG and query architecture | [[Data and Database Guide]] · [[Knowledge Graph and Queries Guide]] |
| **Software / Product** | Not declared | the Observatory is currently documented as a research demonstrator, not as a product documentation program | [[Applications Guide]] |
| **Business** | Not declared | Business Architecture concepts may occur in the ontology, but a business model/operating/economic documentation program is not claimed | — |

## Why the separation matters

A concept definition belongs to the ontology documentation even when a database table implements it. The database page should link to that semantic definition rather than create a competing one.

Likewise, a research demonstrator can show that selected tasks are representable or executable without establishing the feature, operations, usability and release obligations of a software product.

A Business Architecture ontology extension models business-oriented concepts; it does not by itself document CM-PharmE as a business venture.

## Profile responsibilities

### Research / Ontology
Owns research questions, methods, evidence, ontology semantics, evaluation, limitations, evolution and scholarly citation.

### Data / Engineering
Owns schemas, data lifecycle/provenance, mappings, KG/query realization and engineering reproduction.

### Software / Product
Would own product scope, user workflows, software/service architecture, integrations, deployment and operations **if explicitly activated in a repository**.

### Business
Would own actors/value propositions, business and operating models, economics/market context and business risks **if explicitly activated**.

## Linking rule

When two profiles touch the same subject, one profile owns the canonical definition and the other links to it. Implementation or commercial documentation must not silently redefine research/ontology semantics.

## Reusable profile work

The detailed pilot model is maintained in `wiki-src/navigation/documentation-profile-model.md`. After the CM-PharmE pilot stabilizes, #243 transfers the reusable Research/Ontology profile and multi-profile rules to OGCM-RF.

---

<details>
<summary>Documentation record</summary>

- **Page scope:** Version-neutral
- **Documentation maturity:** Stable pilot
- **Authoritative source:** main / wiki-src documentation controls
- **Last synchronized:** 2026-09-24
- **Last synchronized ref:** main (documentation source)
- **Related issues/PRs:** #228, #242, #243
- **Evidence status:** Documentation architecture/pilot profile; no research semantic change
- **Future refresh:** #243 and OGCM-RF#45–#50
- **Wiki baseline:** WB-2026.09.1

</details>
