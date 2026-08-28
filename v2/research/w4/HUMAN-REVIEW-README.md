# CM-PharmE 2.0 Human Review Entry Point

This is the V2-only entry point for human conceptual review before public Pages deployment or manuscript freeze.

## Primary review artifact
- [87-concept provenance and V1→V2 evidence matrix](human-review-concept-provenance-matrix.md)
- [17-domain visual ontology package](visual-ontology-package.md)
- [Final integrated OntoUML conceptual specification](integrated-ontouml-model.md)
- [Concept naming audit](concept-naming-audit.md)

## Predecessor and evidence sources
- [V1 concept registry](../../../catalog/concepts.yaml)
- [V1 human-readable concept pages](../../../docs/concepts/)
- [V1→V2 migration matrix](../w3/v1-v2-migration-matrix.md)
- [W3 candidate definitions and evidence](../w3/candidate-concept-inventory.md)
- [W3 evidence traceability](../w3/evidence-traceability.md)
- [W2 dataset/source portfolio](../w2/gate-c-dataset-portfolio.md)
- [W1 literature and official-source registry](../w1/evidence-sources.md)
- [W7 held-out first-pass mapping](../../evaluation/results/e8-heldout-first-pass-mapping.csv)

## Review sequence
Review one canonical domain at a time. For each concept inspect: definition → OntoUML stereotype → V1 lineage → dataset/official-source evidence → literature/ontology support → held-out evidence → formal IRI. Record one of: APPROVE, APPROVE WITH WORDING CHANGE, REVISE SEMANTICS, SPLIT/MERGE, MOVE DOMAIN/MODULE, or DEFER.

Any semantic change after Gate D should become a V2 design-decision issue before OWL/SHACL is changed.

## Boundary
This review package is V2-only. It does not modify CM-PharmE 1.x or the reviewer-facing `main` branch. The human-review method itself will be generalized into OGCM-RF only after this review cycle teaches us which steps and views are actually useful.