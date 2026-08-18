# CM-PharmE Validation Architecture

The repository uses layered validation so that syntax, logic, structure, semantics, application evidence, and reproducibility are not conflated.

## Automated gates

1. Build the modular Turtle source into the canonical graph.
2. Generate RDF/OWL distributions and SHACL shapes.
3. Generate compact JSON-LD, context, TriG, and N-Quads; verify graph equivalence.
4. Rebuild independently and require byte-identical generated RDF artifacts.
5. Run structural/fingerprint validation against the pinned CM-PharmE 1.0 reference graph.
6. Execute SHACL against the constructed vaccine sample and compare the result profile with registered expectations.
7. Execute eight positive competency-question SPARQL regressions.
8. Execute four negative competency regressions protecting against unsupported direct scenario relations.
9. Generate Manchester and OWL Functional Syntax with ROBOT and round-trip them back to RDF/OWL for graph comparison.
10. Run ROBOT ontology metrics and OWL 2 DL profile assessment.
11. Run HermiT logical reasoning through ROBOT.
12. Build the deterministic release bundle twice and require byte identity.

## SHACL interpretation

SHACL execution is intentionally evidence-preserving rather than cosmetic. The vaccine sample is not rewritten merely to make the complete generated shape set conform. The repository records a bounded expected finding profile and CI verifies that the findings do not drift silently. A passing SHACL CI step means that validation executed correctly and reproduced the registered result profile; it does not mean that the illustrative sample conforms to every generated constraint.

## Competency-question interpretation

Positive CQs test that intended structures can be retrieved from the formal model and sample. Negative CQs test that selected unsupported direct relations remain absent. Both are internal regression/evaluation artifacts, not substitutes for independent empirical validation.

## Logical reasoning interpretation

HermiT checks the current OWL axiom set for logical consistency and unsatisfiable named classes. A successful reasoner run strengthens bounded logical consistency. It does not establish domain completeness, ontological correctness of every modeling decision, or real-world effectiveness.

## OWL profile interpretation

ROBOT profile validation and metrics explicitly report whether the artifact conforms to OWL 2 DL. The profile result is recorded rather than silently normalized. If profile violations are present, they become an explicit future formalization item rather than being hidden during this engineering wave.
