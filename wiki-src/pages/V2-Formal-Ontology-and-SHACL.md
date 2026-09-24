# V2 Formal Ontology and SHACL

> **Page scope:** V2  
> **Documentation maturity:** Stable-to-date / Evolving  
> **Authoritative source:** V2 W5 ontology and validation artifacts  
> **Last synchronized:** 2026-09-23  
> **Last synchronized ref:** `1226b0a5484f8f5d3a8d214e0d0f52f066b88999`  
> **Related issues/PRs:** W5, E1/E2/E5/E13 evidence families  
> **Evidence status:** Formal baseline complete for current V2 alpha baseline  
> **Future refresh:** #213/#214 if semantic/final-release changes occur  
> **Wiki baseline:** WB-2026.09.1

## Formal baseline

Current formal development version: **2.0.0-alpha.1**

Key metrics:
- 642 asserted triples;
- canonical SHA-256 `59ef47eeed732290736e60bfa1c6bf43a12d15df2f50cff931badb5938cc954a`;
- 87 Gate-D conceptual elements;
- 81 OWL classes;
- 6 declared datatypes;
- 52 object properties;
- 5 datatype properties.

## Gate results

The W5 closure records:
- Turtle parse PASS;
- 87-element registry coverage PASS;
- protected distinction checks PASS;
- multi-serialization graph equivalence PASS;
- deterministic build PASS;
- Meta-SHACL PASS;
- SHACL smoke validation PASS;
- OWL 2 DL profile PASS;
- ROBOT/HermiT logical validation PASS;
- Manchester/Functional Syntax generation PASS;
- frozen fingerprint regression PASS.

## SHACL role

SHACL provides executable research-integrity/data-conformance constraints. It is not evidence that every external pharmaceutical source will conform or that all possible constraints are modeled.

## Reasoning boundary

HermiT reasoning over the formal baseline supports logical processability of the evaluated axiom set. It does not establish domain completeness or empirical correctness.

## Namespace/mapping boundaries

The `w3id.org/cm-pharme/2.0/` namespace is a target namespace; external redirect registration remains a separate governance action.

Mapping hints do not automatically establish external-standard conformance.

## Evidence

- [V2 ontology README](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/ontology/README.md)
- [W5 closure](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w5/W5-CLOSURE.md)
- [Formal baseline](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/ontology/baseline/formal-baseline.json)
- [SHACL shapes](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/ontology/shapes/cm-pharme-v2.shacl.ttl)
