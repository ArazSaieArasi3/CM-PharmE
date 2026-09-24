# V2 UFO and OntoUML Architecture

> **Version scope:** V2  
> **Status:** Stable-to-date / Evolving  
> **Updated:** 2026-09-24

## Visual architecture

![V2 ontology architecture](https://raw.githubusercontent.com/ArazSaieArasi3/CM-PharmE/main/wiki-src/diagrams/rendered/ontology/DGM-ONT-002--v2-ontology-architecture-core-x-infra-and-extensions.svg?sha=57f52a9a4974)

**DGM-ONT-002** is an authoritative projection of the current 17-domain architecture across Core, X-INFRA and Extensions. See [[V2 Ontology Diagram Suite]] for the complete multi-level visual set.

## Foundational stance

V2 makes UFO/OntoUML a first-class conceptualization method before OWL implementation. Identity, rigidity, dependence, relational entities, events/activities, modes and contextual roles are resolved conceptually rather than delegated to serialization.

## Protected conceptual commitments

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

## Semantic review layer

The governed semantic-review layer adds:
- whole-ontology overview;
- 17-domain navigation;
- concept review catalog;
- concept evidence passports;
- relation review/evolution packages as they mature.

Review projections do not themselves change semantics.

## Evidence

- [Integrated OntoUML model notes](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w4/integrated-ontouml-model.md)
- [Conceptual freeze evidence](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w4/gate-d-conceptual-freeze.md)
- [Review overview](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/review/ontology-overview.md)
- [Review control center](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/review/README.md)

---

<details>
<summary>Documentation record</summary>

- **Page scope:** V2
- **Documentation maturity:** Stable-to-date / Evolving
- **Authoritative source:** Gate-D W4 conceptual artifacts and V2 review package
- **Last synchronized:** 2026-09-23
- **Last synchronized ref:** `1226b0a5484f8f5d3a8d214e0d0f52f066b88999`
- **Related issues/PRs:** #159, #173, #235
- **Evidence status:** Gate-D architecture frozen for current baseline; selected extension/human-review findings remain active
- **Future refresh:** #213
- **Wiki baseline:** WB-2026.09.1

</details>
