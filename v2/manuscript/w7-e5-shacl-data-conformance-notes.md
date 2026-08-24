# W7-E5 Manuscript Notes — SHACL and Data Conformance

## Evidence state
W7-E5 mandatory fixture gate: **PASS**. Family interpretation: **PASS WITH WARNING** because the Gate-E synthetic fixture does not instantiate every W5 SHACL target class.

## Results that may be reported
- Gate-E schema-faithful fixture KG: 398 triples.
- Frozen W5 SHACL profile: conforms; zero findings on the pristine fixture.
- W7-E5 evaluation-only integrity profile: conforms; zero findings on the pristine fixture.
- combined W5+E5 profile: conforms; zero findings.
- controlled mutation sensitivity: 8/8 predefined defects produced the expected Warning/Violation finding.
- source-record provenance completeness: 7/7.
- facility geography completeness: 2/2.
- observation geography: 28/28.
- observation source/transformation provenance: 28/28 + 28/28.
- identifier assignment entity/scheme completeness: 4/4 + 4/4.
- EvidenceSupport source/assertion completeness: 7/7 + 7/7.

## Required boundary
Only 3 of the 11 W5 NodeShapes had direct focus nodes in the Gate-E fixture (`MedicinalProductPresentation`, `IdentifierAssignment`, `EvidenceSupport`). The six W7-E5 research-integrity shapes were all activated. Therefore, E5 does not establish that every W5 domain constraint has been exercised on populated data.

Full admitted real datasets and held-out H1–H3 were not executed in E5. Controlled mutation sensitivity is not a statistical false-positive/false-negative estimate.

## Manuscript-safe wording
“The deterministic Gate-E regression graph conformed to both the frozen W5 SHACL profile and a prospectively defined W7-E5 integrity profile for provenance, geography, observations, identifiers and entity-match evidence. No findings were produced on the pristine fixture, while all eight predefined controlled data defects triggered their expected SHACL warning or violation. This result is bounded to the schema-faithful synthetic evaluation graph; only three of the eleven W5 domain NodeShapes had populated focus nodes, and full real/held-out data conformance was not evaluated in this evidence family.”

## Do not claim
- real-world pharmaceutical data are violation-free;
- all W5 shapes have been empirically exercised;
- SHACL conformance proves ontology/domain completeness;
- 8/8 controlled mutations constitutes a global false-negative rate;
- held-out generalizability from E5.
