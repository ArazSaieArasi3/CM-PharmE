# Digital Systems — purposeful minimum viable ontology

توصیف جزء سامانه، استقرار و منشأ تولید یا تبدیل دادهٔ دارویی

Status: retention direction accepted by user; detailed model remains a review proposal.

## Purpose and boundary

Input: An identified digital component, versioned deployment and organization, a data activity and generated record, plus a supported pharmaceutical operation.

Output: A trace from a record to the digital activity, deployment/version, operator and separately attributed activity responsibility.

Workflow: record → data activity → deployment → component/version/operator; data activity → supported manufacturing/logistics.

## Owned concepts (working definitions)

| Concept | Working definition |
|---|---|
| DigitalInformationSystemComponent | An identifiable software/information-system component used in a deployment; distinct from a generated record. |
| SystemDeploymentActivity | An actual occurrence deploying an identified component version in an organizational context; distinct from transformation of data. |

These are proposed working definitions. Imported interface classes are separately listed in contract.json and are not added to the owned count.

## Competency questions

- Which component version and deployment produced this record?
- Which organization operated deployment, and which was responsible for processing?
- Which pharmaceutical manufacturing or logistics activity was supported?

## Excluded scope

- Full software architecture or cybersecurity ontology
- A record implying regulatory authorization
- Digital activity being identical to physical manufacturing/logistics

## Independent execution

Copy this directory anywhere. With Java 17 installed, install requirements.txt and run `python runner.py`. The runner reads only this directory; it does not load sibling labs or fetch ontology imports. All selected dependencies are flattened into ontology.ttl.

Measured results: {'admission': [17, 17], 'queries': [5, 5], 'reasoner': [3, 3], 'source_scope_lookups': [0, 0]}. The source-group lookups in PV are documentary/proposed-mapping answers, not patient or legal advice.

## Limits and remaining work

Independent real deployment/agent evidence, version identity, delegation and responsibility, and adjudication of the inherited PROV projection.

Selected-signature projection, not a formally certified locality module. See omissions.json. Full and local admission behavior was compared only on the listed fixtures. SHACL opt-in required fields are not universal OWL cardinalities. Native OntoUML module exports and full semantic acceptance are not claimed.
