# Evaluation

CM-PharmE evaluation is organized as a layered evidence architecture. Reusable evaluation methodology is separated from version- or batch-specific evidence and results.

## Evaluation layers

The repository uses nine complementary layers: syntax validation, logical consistency, structural validation, ontological validation, semantic/expert validation, data and mapping validation, competency questions, application validation, and research reproducibility.

These layers extend the five qualitative evaluation dimensions reported in the associated research: Syntactic and Structural Correctness, Semantic and Conceptual Accuracy, Conceptual Clarity, Adaptability and Modifiability, and Pragmatic Value.

## Available evaluations

- [CM-PharmE v1.0.0 — Structural Extraction Audit](v1.0.0-structural-audit.md)
- [B3 — Formal Ontology Audit](b3-formal-ontology-audit.md)
- [B4 — Paper-Grounded Evaluation Plan](b4-evaluation-plan.md)
- [B4 — Executed Evaluation Matrix](b4-evaluation-matrix.md)
- [B4 — Final Evaluation Report](b4-final-evaluation.md)

## B4 executed evidence

Machine-readable evidence is maintained under [`../../evaluation/`](../../evaluation/). B4 currently records:

- **28/28** structural and traceability checks passing;
- **8/8** competency queries executing to their bounded expected outcomes on the constructed vaccine sample;
- vaccine sample coverage of **32 core classes across all five domains**, with no scenario-specific classes and no explicit domain/range violations;
- re-evaluation of the eight OntoUML-informed anti-pattern categories, including retained historical minor issues and new review candidates;
- explicit manuscript-to-formal scenario traceability findings;
- normalized four-expert publication evidence;
- an explicit reasoner-status record.

## Validation boundary

OWL DL reasoner validation remains **not verified** because the current execution runtime did not contain a reasoner and blocked external binary acquisition. Structural, SPARQL, scenario, or heuristic checks are not presented as a substitute for HermiT/ELK/ROBOT consistency evidence.

No evaluation result should be generalized beyond the procedure and evidence that produced it.
