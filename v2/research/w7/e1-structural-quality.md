# W7-E1 — Syntactic, Structural and Ontology-Quality Evaluation

## Status
**Mandatory gate: PASS. Descriptive annotation-quality observation: WARN (non-blocking).**

GitHub Actions run: `32231194172` — SUCCESS.  
Evidence artifact: `cm-pharme-v2-w7-e1-structural-evidence`, artifact ID `9357280400`.  
Evaluated branch head: `88e8c50f3608a0db402a312e721bb17e95331e00`.

## Mandatory checks
| Check | Result |
|---|---|
| All authoritative Turtle modules parse | PASS |
| Frozen inventory counts match | PASS |
| Frozen canonical fingerprint matches | PASS |
| Conceptual registry fully resolves | PASS — 87/87 |
| Eight protected Gate-D distinctions remain explicit | PASS — 8/8 |
| Ontology↔RDB mapping IRIs resolve | PASS — 36/36 |

## Frozen formal inventory
- 642 asserted triples
- 81 OWL classes
- 6 RDFS datatypes
- 52 OWL object properties
- 5 OWL datatype properties
- canonical graph SHA-256: `59ef47eeed732290736e60bfa1c6bf43a12d15df2f50cff931badb5938cc954a`

## Protected distinctions
All predefined distinctions were retained:
- Organization ≠ Facility
- Facility ≠ GeographicFeature
- GeographicFeature ≠ RegulatoryJurisdiction
- MedicinalProduct ≠ PharmaceuticalSubstance
- MedicinalProduct ≠ MedicinalProductPresentation
- ObservationActivity ≠ ObservationResult
- SupplyCapacity ≠ SupplyCapacityObservationResult
- MedicineShortageSituation ≠ SourceRecord

## Descriptive ontology-quality indicators
These indicators were not predefined as universal pass/fail completeness thresholds:
- internal declared terms with labels: **87/144 = 60.42%**
- duplicate labels: **0**
- properties with explicit `rdfs:domain`: **53/57**
- properties with explicit `rdfs:range`: **42/57**
- deprecated internal terms: **0**

### Interpretation
The mandatory structural baseline is stable and traceable. However, the 60.42% label coverage and incomplete explicit domain/range declarations are useful quality-improvement signals for human readability/documentation. They are recorded as a non-blocking WARN rather than silently converted into a failure because the frozen protocol did not define them as mandatory completeness thresholds and some properties may intentionally omit global domain/range axioms to avoid unintended OWL inferences.

## Boundary
This PASS establishes syntactic/structural integrity against the frozen baseline and registry referential integrity. It does not establish domain completeness, empirical correctness, mapping semantic accuracy or generalizability.
