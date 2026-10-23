# CM-PharmE — operational documentary witnesses

Eight primary documents, 49 extracted statements and 13 explicit mapping proposals test the practical boundaries of the retained four-domain design. The source evidence is historical, purposive and documentary; it is not a complete operational dataset or independent expert validation.

Read decision-report-fa.md, work-status-fa.md, core-evidence-matrix.json and decision-dossier.json. The 15-concept matrix deliberately includes unsupported and partially supported concepts. Do not call all 15 empirically covered.

Run from this directory with the preceding experiment packages present:

```sh
python run_lab.py
python run_risk_scope.py
python run_contract.py
python run_integration.py
python finalize.py
```

Python requirements: rdflib 7.6.0, pyshacl 0.30.1, owlready2 0.49; Java 17. These research runners use the full repository model. The previous four standalone exports remain unchanged; this new evidence adapter is not represented as a new standalone release.

New relation: scenarioScopeDescription, information-to-information; scientific approval and native representation pending. Existing complete profiles were not relaxed to make incomplete sources pass. Qualification modes distinguish plans, requirements, capabilities, reported occurrences, assessment content and authorization reports. Date precision and publication cutoffs do not establish current world truth.

The no-materialization countermodel establishes only scoped non-entailments. No full OWL2 DL, UFO/OntoUML conformance, detector-suite execution, semantic acceptance or release closure is claimed.
