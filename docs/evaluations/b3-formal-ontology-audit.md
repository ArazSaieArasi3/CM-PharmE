# CM-PharmE B3 — Formal Ontology Audit

## Scope

This audit evaluates the unreleased B3 formal-ontology engineering work on `ontology/b3-formal-ontology-v1`. It evaluates repository structure, semantic coverage, cardinality transcription, lifecycle/provenance decisions, IRI design, and the available validation evidence. It does **not** claim that B3 is a released CM-PharmE semantic version.

The current stable semantic baseline remains `v1.0.0`.

## Branch integration status

B3 has been synchronized with the merged B0–B2 `main` history through a non-destructive merge commit. The branch therefore preserves both the B3 engineering history and the merged research-repository foundation.

## Formal ontology coverage

| Item | B3 status |
|---|---:|
| Canonical concept classes | 39 |
| Stable relation records | 40 |
| OWL object properties | 39 |
| Explicit generalization record | 1 (`CMPE-R0006`) |
| Architectural domains | 5 |
| Relation IDs with cardinality-registry coverage | 40 / 40 |
| Stable IRI policy | Present |
| UFO/OntoUML stereotype correspondence notes | Present, cautious/non-equivalence |

The concept modules contain stable identifier-based IRIs, preferred labels, formal definitions, lifecycle/stereotype metadata, primary-domain assignments, and OWL restrictions where cardinality semantics have been formalized.

## Cardinality and relation audit

The seven CSV partitions under `mappings/cardinality/` cover `CMPE-R0001` through `CMPE-R0040`. `CMPE-R0006` is intentionally represented as a generalization rather than as an association with endpoint multiplicities.

Important curated resolutions remain explicit and traceable:

1. `CMPE-R0002` uses the occurrence connected to the canonical `Enterprise Governance Relator` relator node.
2. `CMPE-R0011` is retained for provenance but deprecated and superseded by active `CMPE-R0027`.
3. `CMPE-R0031` normalizes the source label `constraints` to `constrains` while preserving the raw label.
4. Generic source labels such as `material relation` remain provisional rather than being silently replaced with invented domain-specific predicates.
5. Provisional cardinalities remain marked as provisional where the source diagram is ambiguous.

## IRI and ontology-grounding audit

The B3 IRI policy uses identifier-bearing paths under the planned namespace `https://w3id.org/cm-pharme/`, separating ontology, concept, relation, domain, metamodel, and SHACL identifiers.

The `w3id.org` redirect is **not yet registered**, so B3 does not claim that these identifiers are currently dereferenceable public URLs.

UFO/OntoUML correspondence is represented conservatively through internal metamodel terms and scope notes. B3 does not assert unsupported `owl:equivalentClass` links to an external UFO ontology. More specific foundational-ontology alignment belongs to a later validation/alignment cycle.

## Validation evidence

The locally generated B3 reference package recorded the following successful structural checks:

- canonical Turtle parse: PASS
- canonical graph size: 1,086 triples
- OWL cardinality restrictions: 42
- SHACL graph size: 574 triples
- SHACL NodeShapes: 76
- SHACL PropertyShapes: 76
- RDF/XML / OWL, JSON-LD and N-Triples graph equivalence to the canonical Turtle: PASS
- historical converter cardinality-classes absent from the cleaned reference ontology: PASS

The reference artifact hashes are recorded under `ontology/validation/`.

### Important validation boundary

A full OWL DL reasoner such as HermiT/ELK/ROBOT has **not yet been executed as repository evidence**, and the complete generated distributions are not yet automatically rebuilt on GitHub. Accordingly, B3 makes no final OWL DL consistency claim and is not yet release-ready.

## Audit findings

### Passed

- semantic inventory preservation and stable-ID usage
- 39-concept formalization coverage
- 40-relation traceability coverage
- 40/40 cardinality-registry coverage
- separation of generalization from object-property semantics
- lifecycle preservation for deprecated/superseded relations
- explicit source-label provenance
- persistent-IRI design
- historical v1.0.0 ontology preservation
- explicit separation of source-of-truth modules from generated distributions

### Remaining gaps

1. Run and record full OWL DL reasoner validation.
2. Install deterministic GitHub build/CI to regenerate all distributions from the authoritative source.
3. Materialize release-quality SHACL and serialization outputs through that pipeline.
4. Register the `w3id.org` redirect before describing project IRIs as dereferenceable public identifiers.
5. Expand competency questions and run them as versioned evaluation evidence.
6. Perform broader expert semantic validation.
7. Complete authoritative external upper-ontology mappings only where justified.
8. Resolve remaining provisional cardinalities/generic predicate labels when evidence permits.

## Quality assessment

| Dimension | Score / 10 |
|---|---:|
| Formal ontology source architecture | 9.6 |
| Concept coverage | 9.8 |
| Relation/cardinality traceability | 9.6 |
| Lifecycle and provenance | 9.8 |
| IRI architecture | 9.6 |
| Ontological grounding discipline | 9.1 |
| Validation evidence | 8.5 |
| Repository reproducibility before CI | 8.8 |

**Overall B3 engineering quality: 9.4 / 10.**

**Draft-PR readiness: PASS.**  
**Release readiness: CONDITIONAL / NOT YET.**

B3 is sufficiently coherent and traceable for review as a dedicated pull request, while full reasoning, CI-driven reproducibility, and broader evaluation should remain explicit follow-up work rather than being overstated in this batch.
