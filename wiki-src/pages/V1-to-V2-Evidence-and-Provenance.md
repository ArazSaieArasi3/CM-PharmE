# V1 to V2 Evidence and Provenance

> **Page scope:** Cross-version  
> **Documentation maturity:** Stable-to-date / Evolving  
> **V1 authority:** V1 methodology/evaluation/provenance artifacts  
> **V2 authority:** V2 dataset, mapping, provenance and held-out artifacts  
> **Last synchronized:** 2026-09-23  
> **Related issues/PRs:** #95–#104, #159, #173, #206  
> **Evidence status:** Stable evidence-strategy comparison; final human-review evidence still evolving  
> **Future refresh:** #213 and #214  
> **Wiki baseline:** WB-2026.09.1 Candidate

## V1 evidence strategy

V1 is grounded through:
- PRISMA-guided literature review;
- thematic synthesis;
- business-architecture concern identification;
- model-source preservation and normalized catalogs;
- publication/repository traceability;
- scenario/data mapping;
- competency questions;
- expert/publication evidence;
- structural/logical/formal/reproducibility checks.

V1 already treats provenance and evidence as important research-governance concerns, but evidence/provenance are not as deeply modeled as first-class domain/infrastructure semantics as in V2.

## V2 evidence strategy

V2 retains scholarly/methodological evidence and adds:
- DOI-backed primary/secondary datasets;
- authoritative operational sources;
- admitted source manifests;
- field-level source→ontology mappings;
- protected held-out sources;
- evidence registry;
- explicit assertion/evidence/provenance concepts;
- provenance-preserving RDB/KG realization;
- cross-representation evaluation;
- human concept-evidence review.

## Evidence becomes ontology infrastructure

V2 includes explicit concepts/patterns for:
- Data Source;
- Dataset;
- Dataset Release;
- Source Record;
- Assertion;
- Evidence Item;
- Evidence Support;
- Mapping Assertion;
- Provenance Activity;
- Data Quality Finding;
- Identifier Assignment;
- Entity Match Assertion;
- Match Confidence.

This is a substantive architectural change: provenance is not only metadata about the research process; selected provenance/evidence semantics are represented in the ontology/data infrastructure.

## Admission is not truth

V2 deliberately separates:
- source presence;
- mapping evidence;
- modeling decision;
- formal implementation;
- evaluation result.

A source field can motivate or support a distinction without proving its ontological correctness.

## Held-out discipline

V2 reserves H1–H3 source families for held-out evaluation rather than using them in Core discovery.

E8 records:
- 51 frozen held-out requirements;
- 23 exact;
- 38 exact-or-partial;
- 0 first-pass Core identity conflicts.

These findings support bounded reuse/generalizability conclusions only.

## Mapping and coverage evidence

E6:
- 39/39 mapping decisions explicit;
- 36/38 in-scope direct/derived/bounded;
- 2 ambiguous;
- 0 unmapped.

E7:
- 97 source-semantic requirements;
- 74 exact;
- 88 exact-or-partial.

Gaps remain visible rather than being normalized away.

## Human provenance review

#159 and #173 add a concept-level human review layer linking V2 concepts back to:
- V1 predecessors;
- admitted datasets/official sources;
- held-out evidence;
- UFO/OntoUML support;
- formal IRI/location;
- explicit evidence gaps.

## Cross-version interpretation

V2's stronger provenance infrastructure should not be used to claim that V1 lacked research traceability entirely. The correct distinction is that V2 makes selected evidence/provenance semantics more explicit, granular and computationally integrated.

## Evidence

- [V1 methodology](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/methodology/research-and-model-development.md)
- [V1 evaluation](https://github.com/ArazSaieArasi3/CM-PharmE/blob/main/docs/evaluations/index.md)
- [V2 source manifest](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/data/sources/source-manifest.json)
- [V2 source-field mapping](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/data/mappings/source-field-ontology-mapping.csv)
- [V2 evidence registry](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/evidence-registry.md)
- [V2 concept provenance matrix](https://github.com/ArazSaieArasi3/CM-PharmE/blob/v2/research-program/v2/research/w4/human-review-concept-provenance-matrix.md)
