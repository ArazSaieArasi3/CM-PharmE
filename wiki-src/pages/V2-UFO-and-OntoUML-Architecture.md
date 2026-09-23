# V2 UFO and OntoUML Architecture

> **Page scope:** V2  
> **Documentation maturity:** Stable-to-date / Evolving  
> **Authoritative source:** Gate-D W4 conceptual artifacts and V2 review package  
> **Last synchronized:** 2026-09-23  
> **Last synchronized ref:** `1226b0a5484f8f5d3a8d214e0d0f52f066b88999`  
> **Related issues/PRs:** W4, #159, #173  
> **Evidence status:** Gate-D architecture frozen for current baseline; selected extension/human-review findings remain active  
> **Future refresh:** #213  
> **Wiki baseline:** WB-2026.09.1 Candidate

## Foundational stance

V2 makes UFO/OntoUML a first-class conceptualization method before OWL implementation. Identity, rigidity, dependence, relational entities, events/activities, modes and contextual roles are resolved conceptually rather than delegated to serialization.

## Protected Gate-D commitments

The current baseline preserves distinctions including:
- Organization vs Facility/Site vs Geographic Feature vs Regulatory Jurisdiction;
- Ecosystem Participant as a RoleMixin with context-dependent concrete actor/site roles;
- Establishment Registration and Regulatory Authorization as explicit Relator patterns;
- Medicinal Product vs Pharmaceutical Substance vs Product Presentation;
- Product classification using Scheme + Entry + Assignment;
- Essential/Critical medicine classification as contextual;
- Medicine Shortage as a Situation distinct from shortage evidence records;
- Observation Activity distinct from Observation Result;
- Supply Capacity as a Mode distinct from evidence about capacity;
- Identifier Value distinct from identity principle, with contextual Identifier Assignment;
- first-class evidence/provenance/mapping/entity-match semantics.

## Modularity

Risk/Resilience and Business Architecture are modular extensions rather than Core decomposition principles.

This is a deliberate evolution from V1, where business-architecture framing was more central to the model identity.

## Project-native artifact boundary

The project-native conceptual JSON and executable OntoUML checks are useful repository artifacts, but they are not claimed to be official OntoUML-tool export/certification.

## Human review layer

The Human Ontology Review Procedure adds:
- whole-ontology overview;
- 17-domain navigation;
- concept review catalog;
- concept evidence passports;
- relation review/evolution packages as they mature.

Review projections do not themselves change semantics.

## Evidence

- [Integrated OntoUML model notes](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w4/integrated-ontouml-model.md)
- [Gate D](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w4/gate-d-conceptual-freeze.md)
- [Human review overview](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/review/ontology-overview.md)
- [Review control center](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/review/README.md)
