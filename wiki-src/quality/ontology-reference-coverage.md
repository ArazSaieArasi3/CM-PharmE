# V2 ontology reference coverage report

**Issue:** #234  
**Date:** 2026-09-24  
**Authority ref:** `v2/research-program@1226b0a5484f8f5d3a8d214e0d0f52f066b88999`

## Result

**PASS — exhaustive V2 ontology reference coverage generated with zero blocking gaps.**

## Conceptual/formal coverage

| Coverage area | Expected | Actual | Status |
|---|---:|---:|---|
| Review domains/modules | 17 | 17 | PASS |
| Conceptual elements | 87 | 87 | PASS |
| OWL classes | 81 | 81 | PASS |
| Declared conceptual/formal datatypes | 6 | 6 | PASS |
| Object properties | 52 | 52 | PASS |
| Datatype properties | 5 | 5 | PASS |

The conceptual count and OWL class count are deliberately different: **87 conceptual elements = 81 OWL classes + 6 declared datatypes**.

## Generated Wiki reference coverage

- Module landing pages: **17**
- Concept reference pages: **87**
- Object-property reference pages: **52**
- Datatype-property reference pages: **5**
- Exhaustive reference index: **1**
- Total #234 generated reference pages: **162**
- Unmatched formal conceptual entities: **0**
- Blocking coverage gaps: **0**

## Authority inputs

The generator reads:
- `v2/ontouml/cm-pharme-v2.conceptual-model.json`
- `v2/review/domains/index.md`
- `v2/review/concepts/passports/*.md`
- `v2/review/relations/index.md`
- `v2/ontology/source/modules/*.ttl`
- `v2/ontology/shapes/cm-pharme-v2.shacl.ttl`
- `v2/ontology/baseline/formal-baseline.json`

## Generated vs curated boundary

Generated pages are exhaustive lookup/reference projections. They:
- preserve the registered concept definition, evidence anchors and review status;
- expose formal class/datatype/property constraints;
- report missing domain/range as `unspecified`;
- link to data mappings and E6/E10 evaluation context;
- never promote pending review to approval.

Curated pages remain responsible for research interpretation, V1→V2 narrative, modeling rationale and evidential boundaries.

## Navigation result after generation

Generation-time navigation QA:
- inventory entries: **231**
- source-complete pages: **230**
- planned pages: **1**
- max source-complete depth from Home: **2**
- unreachable source-complete pages: **0**
- orphan source-complete pages: **0**
- pages deeper than two steps: **0**

The direct Home → V2 Ontology Reference path keeps every generated leaf within the two-step navigation contract.

## Missing-item register

`wiki-src/ontology-reference/MISSING-ITEMS.md` reports no blocking documentation coverage gaps.

Pending human/author review is a semantic-review state, not a documentation coverage defect.

## Tooling

- generator: `tools/wiki/generate_ontology_reference.py`
- permanent coverage checker: `tools/wiki/check_ontology_reference.py`
- architecture: `wiki-src/ontology-reference/ARCHITECTURE.md`
- generated-vs-curated decision: `wiki-src/ontology-reference/GENERATED-VS-CURATED.md`
- source-of-truth rules: `wiki-src/ontology-reference/SOURCE-OF-TRUTH.md`
- coverage JSON/CSV: `wiki-src/ontology-reference/coverage.json`, `coverage.csv`

## Semantic boundary

This report certifies **documentation coverage and traceability**, not semantic correctness or human approval of all 87 concepts/52 object properties. Semantic review remains governed by #213 and the V2 review workflow.
