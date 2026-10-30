# G3-2e-C — author approval and isolate review

Date: 2026-10-08 Asia/Tehran. Branch: `v2/connectivity-audit-2-1-candidate`. Source candidate: `2.1.0-alpha.1-g3d-candidate`; native overlay: `2.1.0-alpha.1-g3-2d-domain-review`.

## Scientific decision boundary

The author approved the 13 **bounded recommendations** in the bilingual scientific decision PDF. `author-approved-13.json` records the wording and conditions; `consolidated-decision-register.json` carries those exact dispositions into the 42-row register. The remaining 29 rows stay pending. Approval does not authorize blanket global axioms, unknown sources, release promotion, or a claim of complete OntoUML conformance.

## Fourteen isolated named classes

`isolate-review.json` reviews all 14 classes listed by the G3d named-class graph metric, with current stereotype, scope, candidate connector, prospective target, required truthmaker, positive witness design, negative acceptance condition and source anchors. Six proposals have an explicit W4 conceptual pattern but still require instance/source evidence; six are source-conditional, one optional source-conditional, and one optional BA proposal is deferred. **All 14 connector proposals remain unapproved and unasserted**. Three already have broad native relations with untyped targets: `baViewRepresents`, `capacityBearer`, `riskTreatmentAddresses`. The graph metric excludes these untyped ends, so an isolate does not mean the concept lacks every conceptual association.

The baseline remains 138 named classes, 15 components, largest component 124, and 14 isolates. This packet changes decisions and review records only. `static-checks.json` verifies one-to-one coverage and target existence. Official parser/anti-pattern tooling, integrated OWL/SHACL, real-data migration and scientific acceptance remain open.

## Next bounded turn

`G3-2e-E`: integrate only source-supported portions of the 13 accepted recommendations into native OntoUML, check end typing, cardinality, direction and negative witnesses. Defer any change requiring an unapproved isolate proposal or unsupported global axiom. Then `G3-2e-F` aligns OWL/SHACL and checks operation derivation or documents its exclusion. See `g3-closure-plan.json` for the full G3 gate sequence.
