# CM-PharmE 2.0 Human Review Entry Point

This is the V2-only entry point for human conceptual review before public Pages deployment or manuscript freeze.

## Primary review artifact
- [87-concept provenance and V1→V2 evidence matrix](human-review-concept-provenance-matrix.md)
- [Provenance gap register and claim-boundary control surface](human-review-provenance-gap-register.md)
- [Risk-first 19-concept review queue](human-review-high-risk-queue.md)
- [P0 bounded evidence packets — 6 highest-consequence rows](human-review-p0-evidence-packets.md)
- [P1 bounded evidence packets — 10 material evidence/foundational/held-out rows](human-review-p1-evidence-packets.md)
- [P2 bounded evidence packets — 3 legacy/extension migration rows](human-review-p2-evidence-packets.md)
- [Human review disposition log](human-review-disposition-log.md)
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
Start with the risk-first queue so the highest-consequence foundational, migration, risk/resilience, held-out, and legacy-extension rows are inspected before the full matrix. For all P0/P1/P2 rows, use the bounded evidence packets to inspect what repository evidence supports, what remains unproven, the exact author question, and the safe pre-review claim boundary. Record each real author/reviewer decision in the disposition log. Then review the remaining concepts one canonical domain at a time.

For each concept inspect: definition → OntoUML stereotype → V1 lineage → dataset/official-source evidence → literature/ontology support → held-out evidence → formal IRI.

Before assigning a disposition, use the provenance gap register to separate row-level evidence gaps (`G1`–`G9`) from genuine semantic defects. Record one of: APPROVE, APPROVE WITH WORDING CHANGE, REVISE SEMANTICS, SPLIT/MERGE, MOVE DOMAIN/MODULE, or DEFER.

The risk-first queue and evidence packets are prioritization/review aids only. Their rows are not pre-approved, and the other 68 concepts are not implicitly approved. The disposition log starts empty and must only contain decisions from actual review activity.

Any semantic change after Gate D should become a V2 design-decision issue before OWL/SHACL is changed.

## Boundary
This review package is V2-only. It does not modify CM-PharmE 1.x or the reviewer-facing `main` branch. The human-review method itself will be generalized into OGCM-RF only after this review cycle teaches us which steps and views are actually useful.
