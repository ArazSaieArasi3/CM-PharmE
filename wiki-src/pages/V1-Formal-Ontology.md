# V1 Formal Ontology

> **Page scope:** V1  
> **Documentation maturity:** Stable  
> **Authoritative source:** `main/ontology/` plus preserved V1 release artifacts  
> **Last synchronized:** 2026-09-23  
> **Last synchronized ref:** `5099888668d35f798e4759e3534e707ed906db24`  
> **Related issues/PRs:** V1 semantic-engineering closure  
> **Evidence status:** Repository-executed formal/validation evidence with explicit profile boundary  
> **Future refresh:** No semantic change unless a governed later release is declared  
> **Wiki baseline:** WB-2026.09.1 Candidate

## Historical versus canonical formal source

The historical OWL/RDF/XML export bundled with `v1.0.0` is preserved unchanged for provenance. It is not treated as the cleaned canonical ontology source.

The maintained canonical formal source is the modular Turtle under `ontology/source/modules/`.

## Current formal-engineering capabilities

The repository supports:
- deterministic reconstruction of the canonical graph;
- multiple RDF/OWL serializations;
- SHACL generation and execution;
- competency-query regressions;
- ontology metrics/profile assessment;
- ROBOT/HermiT reasoning;
- graph fingerprints and equivalence checks;
- deterministic release packaging.

The repository README records a canonical graph of **1,086 triples** and a generated SHACL graph of **574 triples**, with **76 NodeShapes and 76 PropertyShapes**.

## Validation boundary

Logical reasoning PASS for the current axiom set does not establish:
- universal domain completeness;
- correctness of every modeling commitment;
- external-standard conformance;
- application effectiveness.

The repository explicitly distinguishes logical consistency from OWL-profile hygiene and semantic adequacy.

## Evidence

- [Ontology guide](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/ontology/README.md)
- [Validation architecture](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/engineering/VALIDATION.md)
- [Formats](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/engineering/FORMATS.md)
- [Semantic engineering completion](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/engineering/SEMANTIC_ENGINEERING_COMPLETION.md)
- [Historical OWL export](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/releases/v1.0.0/ontology/CM-PharmE-1.0.owl)

## Related pages

[[V1 Conceptual Model]] · [[V1 Evaluation and Evidence]] · [[V1 Reproducibility]]
