# Generated vs curated ontology documentation

**Issue:** #234  
**Decision:** generated reference is an aid and projection; curated interpretation remains the human-facing explanatory layer.

## Decision

CM-PharmE will not use an auto-generated OWL documentation site as the primary Wiki narrative or as a competing semantic source.

Generated documentation is appropriate for:
- exhaustive entity discoverability;
- IRI/entity-type lookup;
- domain/range/subclass lookup;
- deterministic cross-linking;
- coverage auditing;
- change/regression detection.

Curated documentation is required for:
- why a concept/module exists;
- conceptual identity/dependence interpretation;
- V1→V2 evolution;
- evidence strength and limitations;
- review-state interpretation;
- examples/non-examples requiring domain judgment;
- relationship between conceptual, formal, data and evaluation layers.

## WIDOCO / LODE-style tooling feasibility

Tools in the WIDOCO/LODE family can be useful downstream as **formal-ontology reference-generation aids**. They are not selected here as the canonical Wiki generator because the CM-PharmE reference must combine:
- project-native conceptual registry information;
- UFO/OntoUML stereotypes;
- Concept Evidence Passports;
- V1 lineage/migration evidence;
- pending semantic-review status;
- formal OWL entity information;
- Wiki lifecycle and provenance conventions.

A generic OWL documentation generator normally sees only part of that project-specific evidence model.

## Current implementation choice

Use a repository-native deterministic generator for the Wiki reference projection. Keep WIDOCO/LODE-style generation as an optional formal-reference/export experiment, especially useful for:
- cross-checking formal entity coverage;
- producing an alternate OWL-centric artifact;
- future static reference hosting.

Any such output must:
- link back to the authoritative TTL;
- be version/ref stamped;
- not override curated definitions;
- be labeled generated;
- be QA-checked against the frozen formal baseline.

## Tool adoption gate

A generated-reference tool may be added later only if:
1. it reproduces the 81-class / 52-object-property / 5-datatype-property baseline accurately;
2. it does not erase the 87 conceptual-element distinction;
3. it supports stable versioned output;
4. it can coexist with project-specific provenance/review information;
5. maintenance cost is lower than the benefit.
