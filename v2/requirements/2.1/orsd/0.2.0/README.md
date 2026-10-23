# CM PharmE 2.1 ORSD 0.2.0

This version consolidates the existing requirements baseline and separates document readiness from ontology validation.

Run from a checkout containing the sibling 0.1.0 archive and pinned candidate packages:

```bash
python consolidate.py
python verify.py
python build_document.py
```

Dependencies: Python, python-docx, rdflib 7.6.0, pyshacl 0.30.1, owlready2 0.49 and Java 17. The document uses Vazirmatn. Render the DOCX through the documents skill renderer and retain its equivalent PDF after layout inspection.

The source data and old module artifacts remain unchanged. The corrected query in `verification/ba02-corrected.rq` supersedes the archived stale query as evidence for R-BA-02 in this document. Its scope is absence of a recorded logistics realization in the supplied graph. The separate OWL countermodel checks non-entailment for that relation under the pinned BA ontology.

`validation.json` reports executed checks. `closure.json` contains the finite remaining document action. Technical consolidation is complete; one author content review remains before a 1.0.0 specification freeze.
