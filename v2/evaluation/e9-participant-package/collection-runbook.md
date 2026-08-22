# W7-E9 Recruitment and Collection Runbook

## Purpose
Operationalize real expert recruitment and response collection without changing the frozen E9 protocol, instrument, eligibility rules, scoring, red-flag criteria, or analysis plan.

## Pre-launch gate
Before contacting participants:
1. confirm whether any university/institutional ethics, approval, waiver, or notification requirement applies;
2. retain that administrative evidence outside the public repository if it contains identifiable information;
3. use only the frozen instrument at `v2/evaluation/protocol/e9-expert-instrument.csv`;
4. use the controlled participant brief in this directory;
5. do not expose earlier evaluation scores/results to participants unless methodologically justified, because the E9 purpose is independent judgment of the model.

If institutional clearance is required and has not been obtained, recruitment pauses here.

## Recruitment target
Target 6–12 completed reviews, preferably with at least two eligible participants in each of the two strata:
- pharmaceutical-domain;
- ontology/conceptual-modeling.

A participant may qualify for both strata. Qualification basis must be recorded before response analysis.

## Pseudonymous participant IDs
Use IDs such as:
- `EX-DOM-01`
- `EX-ONT-01`
- `EX-BOTH-01`

Keep any identity↔ID key outside the public repository.

## Contact and screening sequence
1. Send the recruitment invitation privately.
2. Establish eligibility from the frozen protocol before accepting a completed response.
3. Provide the consent/data-governance notice.
4. Record explicit consent before substantive responses are accepted.
5. Provide the controlled review brief and frozen instrument.
6. Do not coach the participant toward agreement or disclose desired outcomes.
7. Invite critical findings and uncertainty explicitly.

## Data capture
Use the frozen templates:
- participant register: `v2/evaluation/templates/e9-participant-register-template.csv`
- item responses: `v2/evaluation/templates/e9-expert-response-template.csv`
- finding register: `v2/evaluation/templates/e9-finding-register-template.csv`
- deviation log: `v2/evaluation/templates/e9-deviation-log-template.csv`

Do not place names, email addresses, phone numbers, signed consent documents, or participant identity keys in the public repository.

## Minimum completion checks
Before marking a response complete:
- participant is eligible;
- consent is recorded;
- participant ID is pseudonymous and stable;
- required rating items for that participant's stratum are present;
- required confidence ratings are present;
- comments required by low ratings or a material/not-suitable disposition are present;
- instrument version/freeze anchor is recorded consistently.

No missing rating is imputed.

## Monitoring during collection
Track only operational counts until analysis:
- invitations sent privately;
- eligible participants;
- completed responses by stratum;
- withdrawals/exclusions with non-identifying reason;
- deviations, if any.

Do not compute or publicize provisional expert-result claims while recruitment is underway if doing so could influence further collection or interpretation.

## Collection stop rule
The planned target is 6–12 completed reviews. Recruitment may stop within that range when both strata are represented and at least two eligible participants are available in each stratum. If recruitment stops below target, document the reason and report the achieved sample transparently.

## Analysis handoff
After collection:
1. freeze the anonymized response dataset and participant register;
2. run the E9 validation/analysis tool;
3. inspect all red-flag outputs;
4. code qualitative comments under the frozen taxonomy;
5. adjudicate each material/critical finding traceably;
6. record any post-review ontology adaptation without altering the original expert evidence;
7. update E9 evidence status, manuscript evidence ledger, issue #98, W7 Epic #21, evidence register #103, and Gate F #104.

## Current boundary
This runbook makes E9 operationally launch-ready. It does **not** count E9 as completed. Completion requires real eligible expert responses and analysis under the frozen plan.