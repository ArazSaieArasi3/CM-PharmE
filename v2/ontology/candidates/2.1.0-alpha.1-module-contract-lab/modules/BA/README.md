# Business Architecture — purposeful minimum viable ontology

توصیف قابلیت و خدمت دارویی و تعهدات همکاری در نمای تحلیلی

Status: retention direction accepted by user; detailed model remains a review proposal.

## Purpose and boundary

Input: Organizations, a pharmaceutical service specification, a borne capability, and documentary partnership commitments when actually supported.

Output: An analytical architecture view linking organizations, service specifications, capabilities and evidenced collaboration commitments.

Workflow: view → organization/service → capability → bearer; strategic agreement → participants/commitment/evidence.

## Owned concepts (working definitions)

| Concept | Working definition |
|---|---|
| BusinessArchitectureView | An information artifact representing selected organizational and service relationships for an analytical purpose. |
| ServiceOfferingSpecification | An information artifact specifying a service offering; distinct from execution of that service. |
| EnterpriseCapability | A capability borne by an organization; its presence does not imply an execution or a quantity of supply capacity. |
| PartnerOrganizationRole | A contextual organization role grounded in a strategic partnership agreement. |
| StrategicPartnershipAgreement | A proposed relator grounding participants and commitments; the agreement document is a separate source record. |

These are proposed working definitions. Imported interface classes are separately listed in contract.json and are not added to the owned count.

## Competency questions

- Who bears a capability, including a capability with no recorded exercise?
- Which medicinal product or facility gives the service a pharmaceutical scope?
- What commitments and documentary evidence support a strategic agreement?

## Excluded scope

- Complete enterprise architecture framework
- Every outsourcing agreement being a strategic partnership
- Capability implying exercised capacity

## Independent execution

Copy this directory anywhere. With Java 17 installed, install requirements.txt and run `python runner.py`. The runner reads only this directory; it does not load sibling labs or fetch ontology imports. All selected dependencies are flattened into ontology.ttl.

Measured results: {'admission': [17, 17], 'queries': [5, 5], 'reasoner': [3, 3], 'source_scope_lookups': [0, 0]}. The source-group lookups in PV are documentary/proposed-mapping answers, not patient or legal advice.

## Limits and remaining work

Independent real contract evidence and adjudication of agreement/commitment/document identity; not every outsourcing arrangement is a strategic partnership.

Selected-signature projection, not a formally certified locality module. See omissions.json. Full and local admission behavior was compared only on the listed fixtures. SHACL opt-in required fields are not universal OWL cardinalities. Native OntoUML module exports and full semantic acceptance are not claimed.
