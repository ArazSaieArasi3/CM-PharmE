# Risk Management — purposeful minimum viable ontology

ارزیابی، برنامهٔ رسیدگی و بازبینی ریسک کیفیت و تداوم عرضهٔ دارو

Status: retention direction accepted by user; detailed model remains a review proposal.

## Purpose and boundary

Input: A scoped medicinal product, facility or supply dependency; a documentary source; assessment and optional review occurrences.

Output: Traceable assessment content, a treatment plan, separately evidenced treatment execution, and predecessor/successor review content.

Workflow: scenario → assessment → result/evidence → plan; execution references the plan; review connects prior/new results.

## Owned concepts (working definitions)

| Concept | Working definition |
|---|---|
| RiskAssessmentActivity | An occurrence assessing a scoped risk scenario; distinct from its result content. |
| RiskTreatmentActivity | An occurrence executing a risk treatment plan; the plan alone does not establish this occurrence. |
| RiskTreatmentPlan | An information artifact specifying a proposed treatment response to an assessment result. |
| RiskReviewActivity | An occurrence reviewing earlier assessment content and connecting it with new content. |

These are proposed working definitions. Imported interface classes are separately listed in contract.json and are not added to the owned count.

## Competency questions

- What product, facility or dependency is assessed, and which source supports the result?
- Which plans have no recorded execution in this dataset?
- Which review changed which result and conclusion?

## Excluded scope

- Patient-level clinical risk prediction
- All enterprise risk categories
- Plan existence implying execution or effectiveness

## Independent execution

Copy this directory anywhere. With Java 17 installed, install requirements.txt and run `python runner.py`. The runner reads only this directory; it does not load sibling labs or fetch ontology imports. All selected dependencies are flattened into ontology.ttl.

Measured results: {'admission': [14, 14], 'queries': [4, 4], 'reasoner': [3, 3], 'source_scope_lookups': [0, 0]}. The source-group lookups in PV are documentary/proposed-mapping answers, not patient or legal advice.

## Limits and remaining work

Real independent risk assessment/review evidence, treatment effectiveness, agreed temporal semantics and review of event/content boundaries.

Selected-signature projection, not a formally certified locality module. See omissions.json. Full and local admission behavior was compared only on the listed fixtures. SHACL opt-in required fields are not universal OWL cardinalities. Native OntoUML module exports and full semantic acceptance are not claimed.
