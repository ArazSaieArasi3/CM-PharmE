# Evaluation

CM-PharmE evaluation is organized as a layered evidence architecture. Reusable evaluation methodology is separated from version-specific evidence and results.

## Nine-layer evaluation framework

Reader-facing documentation uses descriptive names first; compact `E1`–`E9` codes are retained only as stable internal labels for traceability.

| Layer | Internal code | Current status |
|---|---|---|
| Syntax Validation | E1 | PASS |
| Logical Consistency | E2 | PASS for the current logical axiom set |
| Structural Integrity | E3 | PASS |
| Ontological Soundness | E4 | CONDITIONAL — targeted semantic findings remain open |
| Semantic & Expert Validation | E5 | PARTIAL — publication evidence exists; broader independent replication remains future work |
| Data & Mapping Validation | E6 | PASS within the bounded constructed scenario |
| Competency Questions | E7 | PASS within bounded expectations |
| Application Validation | E8 | PARTIAL / illustrative |
| Research Reproducibility | E9 | PASS for the completed repository-engineering scope |

These layers extend the five qualitative evaluation dimensions reported in the associated research: Syntactic and Structural Correctness, Semantic and Conceptual Accuracy, Conceptual Clarity, Adaptability and Modifiability, and Pragmatic Value.

## Evaluation records

- [CM-PharmE v1.0.0 — Structural Extraction Audit](v1.0.0-structural-audit.md)
- [Formal Ontology Audit (historical phase B3)](b3-formal-ontology-audit.md)
- [Paper-Grounded Evaluation Plan (historical phase B4)](b4-evaluation-plan.md)
- [Executed Evaluation Matrix](b4-evaluation-matrix.md)
- [Final Evaluation Report](b4-final-evaluation.md)
- [Reasoner and Semantic Finding Disposition](b4-10-semantic-finding-disposition.md)

The historical B-codes are retained in filenames and audit records so repository evolution remains traceable; readers do not need to understand those codes to navigate the current evaluation state.

## Executed evidence

Machine-readable evidence is maintained under [`../../evaluation/`](../../evaluation/). Current repository evidence includes:

- **28/28** structural and traceability checks passing;
- **8/8** competency queries executing to their bounded expected outcomes on the constructed vaccine sample;
- vaccine sample coverage of **32 core classes across all five domains**, with no scenario-specific classes and no explicit domain/range violations;
- re-evaluation of the eight OntoUML-informed anti-pattern categories;
- explicit manuscript-to-formal scenario traceability findings;
- normalized four-expert publication evidence;
- reproducible GitHub Actions ROBOT/HermiT validation with a pinned ROBOT SHA-256;
- machine-readable disposition of targeted semantic findings;
- deterministic build, graph-fingerprint, SHACL and serialization-equivalence checks.

For the OntoUML context behind the stereotype and anti-pattern terminology, see [Official OntoUML Ecosystem References](../references/ontouml-ecosystem.md).

## Validation boundary

OWL logical validation is **repository-executed and PASS for the current logical axiom set**. This does not establish universal domain completeness, empirical effectiveness, standards conformance, or correctness of every ontological modeling decision.

Ontological validation remains conditional because targeted role/mediation and part-whole findings require semantic refinement or additional domain evidence. Expert/semantic evidence remains partial because no new independent expert panel was conducted during repository execution.

No evaluation result should be generalized beyond the procedure and evidence that produced it.