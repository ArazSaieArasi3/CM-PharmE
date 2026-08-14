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
- [B4/B4.10 — Final Evaluation Report](b4-final-evaluation.md)
- [B4.10 — Reasoner and Semantic Finding Disposition](b4-10-semantic-finding-disposition.md)

## Executed evidence

Machine-readable evidence is maintained under [`../../evaluation/`](../../evaluation/). B4/B4.10 records:

- **28/28** structural and traceability checks passing;
- **8/8** competency queries executing to their bounded expected outcomes on the constructed vaccine sample;
- vaccine sample coverage of **32 core classes across all five domains**, with no scenario-specific classes and no explicit domain/range violations;
- re-evaluation of the eight OntoUML-informed anti-pattern categories;
- explicit manuscript-to-formal scenario traceability findings;
- normalized four-expert publication evidence;
- a reproducible GitHub Actions ROBOT/HermiT workflow with pinned ROBOT SHA-256;
- successful HermiT logical validation in GitHub Actions run `31796520297`;
- machine-readable disposition of the five targeted semantic findings;
- source-parity evidence showing annotation/provenance differences between the GitHub modular source and the B3 packaged canonical source, with **zero logical-predicate differences**.

## Validation boundary

OWL logical validation is now **repository-executed and PASS for the current logical axiom set**. This closes the former E2 gap but does not establish universal domain completeness, empirical effectiveness, standards conformance, or correctness of every ontological modeling decision.

E4 ontological validation remains conditional because targeted role/mediation and part-whole findings require semantic disposition or additional domain evidence. E5 expert/semantic evidence remains partial because no new independent expert panel was conducted in B4.

No evaluation result should be generalized beyond the procedure and evidence that produced it.
