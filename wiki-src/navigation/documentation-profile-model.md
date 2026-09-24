# Documentation profile composition model

**Pilot:** CM-PharmE  
**Issue:** #242  
**Cross-repo target:** ArazSaieArasi3/OGCM-RF#49  
**Status:** Pilot profile model; generic ownership transfers to OGCM-RF only after #243.

## Principle

A repository selects the documentation profiles it actually needs. No profile is universal, and selecting one profile does not imply the others.

Profiles organize **documentation responsibility**, not ontology modules, software packages or organizational departments.

## Profile 1 — Research / Ontology

### Purpose
Explain and reference a research contribution whose core artifact includes a conceptual model, ontology or ontology-grounded method.

### Mandatory when selected
- project/research overview;
- research problem, questions/objectives and method;
- evidence/literature/data basis;
- conceptual model and/or ontology architecture;
- concept/relation/property reference appropriate to the artifact;
- evaluation/validation/assurance;
- limitations/threats/non-claims;
- reproducibility;
- version/evolution history;
- publications/citation/reuse.

### Optional
- datasets and source registry;
- database/KG implementation;
- tutorials;
- research demonstrators;
- generated ontology reference.

## Profile 2 — Data / Engineering

### Purpose
Document data structures, transformations and engineering realizations used to store, map, query or expose information.

### Mandatory when selected
- data architecture and scope;
- database/schema or equivalent data model;
- data lifecycle and provenance;
- mappings and identity-resolution rules where applicable;
- build/bootstrap/reproduction instructions;
- query interfaces and contracts actually implemented;
- implementation limitations.

### Optional
- KG/RDF;
- API;
- ETL/ELT orchestration;
- operational/deployment material;
- performance/observability evidence.

## Profile 3 — Software / Product

### Purpose
Document a software/product system as something users/operators build, use, integrate, deploy and evolve.

### Mandatory when selected
- product/system scope;
- users/personas and use cases;
- features/capabilities;
- workflows;
- software architecture;
- services/components;
- APIs/integrations;
- non-functional requirements;
- deployment/operations;
- release/change guidance.

### Optional
- UX/UI design;
- security model;
- support/runbooks;
- analytics/telemetry;
- product roadmap.

## Profile 4 — Business

### Purpose
Document the business system, operating model and economic/value logic around a solution or organization.

### Mandatory when selected
- actors/stakeholders;
- value propositions;
- business/operating model;
- value/process flows;
- economics/revenue/cost/funding where applicable;
- market/ecosystem context;
- governance/business risks;
- business metrics.

### Optional
- commercial strategy;
- partnership model;
- business canvases;
- service portfolio;
- market sizing/competitive analysis.

## Ownership boundary matrix

| Subject | Canonical documentation owner | Cross-profile rule |
|---|---|---|
| Research question/method/contribution | Research/Ontology | Other profiles link; do not restate as product/business claims |
| Ontology concept definition | Research/Ontology | Data/Product may reference the definition, not redefine it |
| Ontology relation/property semantics | Research/Ontology | Engineering mappings point back to semantic authority |
| Research evaluation/claim boundaries | Research/Ontology | Product performance evidence is separate |
| Relational schema/table/field semantics | Data/Engineering | Link ontology mapping; do not make the DB a competing ontology |
| Data provenance/transformation | Data/Engineering | Research profile may cite as evidence |
| KG generation/query implementation | Data/Engineering | Semantic meaning remains owned by Research/Ontology |
| Product feature/workflow | Software/Product | Research demonstrator is not automatically a product feature |
| Runtime/service architecture | Software/Product | Research implementation may link if it becomes productized |
| Deployment/operations | Software/Product | Data profile owns only data-engineering operational specifics |
| Value proposition/business model | Business | Product may link; Research/Ontology does not infer business viability |
| Market/economics/commercial model | Business | Must not be inferred from ontology coverage |
| Business Architecture ontology extension | Research/Ontology when it is ontology semantics | Does **not** automatically activate Business Profile |
| Research demonstrator | Research/Ontology unless explicitly productized | Does **not** automatically activate Software/Product Profile |

## Cross-profile linking rules

1. One canonical owner per definition or claim family.
2. A secondary profile links to the owner instead of copying a competing definition.
3. Cross-profile pages must state which profile owns the authoritative meaning.
4. Implementation mappings may narrow or encode semantics but may not silently redefine ontology concepts.
5. Product success/performance claims require product evidence; ontology evaluation is not a substitute.
6. Business viability/value claims require business evidence; research novelty is not a substitute.
7. Shared indexes may aggregate links, but canonical definitions remain with their owning profile.

## Multi-profile Home pattern

Home should:
1. state which profiles are active;
2. identify primary vs supporting profiles;
3. provide one entry path per active profile;
4. state important profiles that are **not** declared when confusion is likely;
5. avoid duplicating the full table of contents for each profile.

## CM-PharmE classification

| Profile | State | Role | Entry path | Rationale |
|---|---|---|---|---|
| Research/Ontology | **Active** | Primary | Research Guide; Ontology and Conceptual Model Guide; Evaluation and Reproducibility Guide | Principal research/ontology contribution |
| Data/Engineering | **Active** | Supporting | Data and Database Guide; Knowledge Graph and Queries Guide | V2 has PostgreSQL/PostGIS, mappings, RDF/KG and query evidence |
| Software/Product | **Not declared** | — | Applications Guide remains research-facing | Observatory surfaces are research demonstrators, not a product documentation commitment |
| Business | **Not declared** | — | — | Business Architecture is an ontology extension/view, not a business-model documentation program |

## Repository self-classification checklist

Before selecting a profile:
- Does the repository contain authoritative artifacts of that profile type?
- Is the repository expected to answer reader questions in that profile's mandatory areas?
- Is there evidence/implementation sufficient to document the profile truthfully?
- Would selecting the profile create duplicate ownership with another profile?
- Is the content a real repository responsibility or merely an example/demonstrator?

Select only profiles with affirmative, evidence-backed answers.

## Anti-patterns

### Universal mega-template
Every repository receives Research, Product, Business and Data sections whether relevant or not.

**Why it fails:** creates empty/fictional documentation and weakens ownership.

### Ontology-as-product documentation
Concepts, relations and CQs are presented as a complete product manual.

**Why it fails:** semantic research artifacts do not describe users, operations, deployment or product behavior.

### Database-as-ontology
Table/column names become canonical domain definitions.

**Why it fails:** implementation representation can narrow or restructure semantics.

### Demonstrator-as-product
A research application is documented as production/product capability without product evidence.

**Why it fails:** representability/task evidence is not product readiness.

### Business Architecture extension = Business Profile
An ontology module about capability/organization/value concepts is treated as proof that a business model has been documented.

**Why it fails:** modeled business concepts and actual business documentation have different evidence and purpose.

### Duplicated definitions
Research, data and product pages each define the same domain term differently.

**Why it fails:** creates semantic drift; use one canonical owner and cross-links.

## Portability

This is the CM-PharmE pilot model. #243 and OGCM-RF#45–#50 will generalize it, remove pharmaceutical-specific assumptions and validate it against another ontology/research repository before it becomes a reusable canonical profile.
