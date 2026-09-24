# Glossary

> **Page scope:** Version-neutral / Cross-version  
> **Documentation maturity:** Stable-to-date / Evolving  
> **Authoritative sources:** V1/V2 model, methodology and governance artifacts  
> **Last synchronized:** 2026-09-23  
> **Related issues:** #208  
> **Evidence status:** Controlled reader-facing terminology; semantic definitions remain version-specific where applicable  
> **Future refresh:** #213/#214  
> **Wiki baseline:** WB-2026.09.1

| Term | Reader-facing meaning in CM-PharmE | Version note |
|---|---|---|
| CM-PharmE | Versioned ontology-grounded conceptual/research program for the pharmaceutical ecosystem | Both |
| Conceptual model | Structured representation of relevant concepts, relations and commitments | Both |
| Ontology | Formalized semantic model with explicit classes/properties/axioms and related constraints | Both |
| UFO | Unified Foundational Ontology used for ontological analysis | Both |
| OntoUML | Ontology-driven conceptual modeling language/method grounded in UFO | Both |
| Kind | Rigid identity-supplying type | Both |
| Role | Anti-rigid/context-dependent type whose identity comes from another type | Both |
| RoleMixin | Anti-rigid role pattern that may span different identity providers | Primarily V2 |
| Relator | Relational entity grounding/materializing a relationship among participants | Both |
| Mode | Existentially dependent property/capability/disposition | Both |
| Event / Perdurant | Temporally unfolding occurrence/activity | V1 uses perdurant; V2 commonly uses Event |
| Situation | State/configuration holding in a bounded context/time | V2 |
| Material relation | Domain relation whose truth may be grounded by a relator or domain state | Both |
| Mediation | Relation connecting a relator to its participants | Both |
| Characterization | Relation connecting a mode/quality to its bearer | Both |
| Core | V2 package for stable principal pharmaceutical-domain semantics | V2 |
| X-INFRA | V2 cross-cutting infrastructure semantics such as provenance, identity and spatiotemporal context | V2 |
| Extension | Optional/modular semantic package separated from the principal Core | V2 |
| Evidence Item | Information object serving contextually as evidence for an assertion/decision | V2 |
| Evidence Support | Relator grounding support between evidence and an assertion/decision | V2 |
| Assertion | Information object representing a proposition | V2 |
| Mapping Assertion | Assertion recording an explicit mapping | V2 |
| Provenance Activity | Activity that ingests/transforms/normalizes/maps information and generates artifacts/assertions | V2 |
| Identifier Assignment | Contextual relation between an entity, identifier value and scheme | V2 |
| Entity Match Assertion | Proposition stating a correspondence/sameness relationship across representations | V2 |
| Held-out evidence | Evidence intentionally protected from discovery and used later for evaluation | V2 |
| Competency Question | Question used to define/test expected representational/query capability | Both |
| SHACL | RDF Shapes Constraint Language used for executable constraints/data conformance checks | Both |
| OWL 2 DL | Description-logic-oriented OWL profile targeted by the V2 formal gate | V2 |
| RDB | Relational database representation | V2 |
| KG | Knowledge Graph / RDF graph representation | V2 |
| Gate | Explicit research decision checkpoint controlling progression/claim scope | V2 |
| Wiki Baseline | Documentation-only snapshot identifier such as WB-YYYY.MM.N | Wiki only |
| Stable-to-date / Evolving | Documentation accurately reflects stable evidence at a point while the underlying version remains active | Wiki/V2 |
| Frozen | Documentation synchronized to an explicitly frozen final underlying baseline | Wiki lifecycle |
| Provenance | Traceable origin, transformation and evidential lineage of data/assertions/artifacts | Both, first-class in V2 |

## Terminology rule

This glossary is a reader aid, not a competing ontology source. For formal meaning, follow the relevant version-specific model/ontology artifact.

## Related pages

[[Concept Index]] · [[Relation Index]] · [[Acronyms]] · [[Wiki Authoring Standard]]
