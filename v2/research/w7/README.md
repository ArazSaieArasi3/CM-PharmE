# CM-PharmE 2.0 — W7 Prospective Multi-Family Evaluation

## Status
W7 starts from the Gate-E-approved W6 merge baseline `59417e352c68585effc3056440fd1a815f6b92bc`.

The evaluation protocol was frozen before W7 result interpretation. W7 evidence families remain separate; there is no single composite quality score.

## Progress
- V2-062 / #89 — protocol and metric registry — COMPLETE
- V2-063 / #90 — structural/ontology quality — COMPLETE
- V2-064 / #91 — OWL profile and multi-reasoner logic — COMPLETE
- V2-065 / #92 — UFO/OntoUML pattern/anti-pattern review — COMPLETE
- V2-066 / #93 — positive and negative competency questions — NEXT
- V2-067 / #94 — SHACL/data conformance
- V2-068 / #95 — dataset-to-ontology mapping quality
- V2-069 / #96 — concept/relation coverage
- V2-070 / #97 — held-out and cross-jurisdiction evaluation
- V2-071 / #98 — prospective structured expert evaluation
- V2-072 / #99 — ontology↔RDB↔KG semantic consistency
- V2-073 / #100 — selected analytics/AI demonstrators
- V2-074 / #101 — pharmaceutical resilience scenarios
- V2-075 / #102 — independent rebuild/reproducibility audit
- W7 evidence register / #103
- Gate F / #104 — evidence sufficiency for principal manuscript claims

## Evidence to date
### W7-E1 — structural quality
Mandatory structural gate PASS with non-blocking quality warnings. Conceptual registry 87/87; ontology↔RDB mapping IRIs 36/36; protected distinctions 8/8.

### W7-E2 — logical/multi-reasoner
Mandatory logical gate PASS with a bounded JFact datatype compatibility warning. OWL 2 DL PASS; HermiT/JFact exit 0; 0 unsatisfiable named classes; exact agreement on 91 named-class subclass pairs.

### W7-E3 — UFO/OntoUML patterns
Project-native executable review PASS WITH WARNING. 17 checks; 0 blocking failures; 87/87 conceptual/formal stereotype agreement; 10 concrete Roles grounded in expected identity providers; principal Relator mediation checks PASS; protected distinctions 8/8. Warnings are bounded to extension-only Relator/Mode formalization and the degree to which Role relational dependence is executable in OWL. This is not official OntoUML-tool conformance.

## Protected held-out boundary
H1 ClinicalTrials.gov/AACT: NOT USED  
H2 openFDA Drug Shortages: NOT USED  
H3 reserved national essential-medicines sample: NOT USED

Any ontology change triggered by held-out evidence is recorded as post-test adaptation and is not counted as initial held-out success.

## Main-branch boundary
All W7 work remains on the V2 research line. `main` is not a target.
