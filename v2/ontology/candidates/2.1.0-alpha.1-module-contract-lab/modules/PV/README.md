# Pharmacovigilance — purposeful minimum viable ontology

پیوند شاهد ایمنی، سیگنال و نتیجهٔ ارزیابیِ قابل‌ردیابی

Status: retention direction accepted by user; detailed model remains a review proposal.

## Purpose and boundary

Input: A safety report or other documentary source, a product/substance or versioned source-defined group scope, and optionally an attributed assessment occurrence.

Output: Traceable signal content and assessment-result content; source statements separated from proposed mappings and actual events.

Workflow: source record → reported content → safety signal → assessment → result; a documentary scope points to versioned lexical entries.

## Owned concepts (working definitions)

| Concept | Working definition |
|---|---|
| AdverseEventReportingActivity | An occurrence reporting safety-related content through a record; it is not the record or a clinical adverse event. |
| PharmacovigilanceRequirement | An information object specifying a pharmacovigilance requirement in its applicability context. |
| PostMarketSurveillanceActivity | An occurrence conducting post-market surveillance under an identified requirement using identified sources. |
| SignalAssessmentActivity | An occurrence assessing a safety signal; distinct from reporting and assessment-result content. |

These are proposed working definitions. Imported interface classes are separately listed in contract.json and are not added to the owned count.

## Competency questions

- Which target and source are associated with a signal?
- How do successive assessment results differ, and who is attributed as assessor?
- Which jurisdiction/requirement supports surveillance?
- Which labels are listed in this exact source scope, and which qualifiers remain unknown?

## Excluded scope

- Patient event invention from a recommendation
- Signal implying established causality
- A complete ICSR/E2B implementation

## Independent execution

Copy this directory anywhere. With Java 17 installed, install requirements.txt and run `python runner.py`. The runner reads only this directory; it does not load sibling labs or fetch ontology imports. All selected dependencies are flattened into ontology.ttl.

Measured results: {'admission': [35, 35], 'queries': [9, 9], 'reasoner': [5, 5], 'source_scope_lookups': [15, 15]}. The source-group lookups in PV are documentary/proposed-mapping answers, not patient or legal advice.

## Limits and remaining work

Actual assessment/time evidence, an ICSR contract, canonical chemical identity mapping, legal applicability/version review and native representation of accepted information profiles.

Selected-signature projection, not a formally certified locality module. See omissions.json. Full and local admission behavior was compared only on the listed fixtures. SHACL opt-in required fields are not universal OWL cardinalities. Native OntoUML module exports and full semantic acceptance are not claimed.
