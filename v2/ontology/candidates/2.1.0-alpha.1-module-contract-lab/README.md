# CM-PharmE — purposeful standalone module contracts

User direction: retain Risk Management, Pharmacovigilance, Business Architecture and Digital Systems as purposeful small ontologies. Detailed scientific acceptance and release remain pending.

Read decision-report-fa.md and work-status-fa.md for the current decision, measured progress and complete work queue. Each modules/RM, PV, BA, DS directory is independently runnable and includes a purpose contract, owned versus imported vocabulary, flattened OWL, opt-in SHACL, fixed queries, fixtures and results.

Rebuild from the repository with the pinned Python requirements and Java 17:

```sh
python build_pv_group.py
python build_modules.py
python run_standalone.py
python run_integration.py
python finalize.py
```

Rebuild scripts read earlier immutable experiment packages. Exported module runners read only their own directory. Initial extraction failure (named property shapes omitted) and initial PV failure (scope/carrier identity not excluded) are retained with final passing results.

This is a bounded signature projection and fixture comparison, not formal locality extraction or complete logical equivalence. Native OntoUML remains unchanged; no gate or issue is closed. Do not sum overlapping PV checks as independent empirical evidence.
