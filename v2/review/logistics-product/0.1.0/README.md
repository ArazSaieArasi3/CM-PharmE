# Logistics product type association: delegated bounded decision

Issue #348. AUTH-22-01 permits this explicit bounded choice without a repeat
approval request. The primary European Commission GDP 2013 guideline is used
for the distinctions in chapters 4.2, 5.8 and 9.2. Its wording motivates
traceable records, product identification, batch and delivery distinctions;
it does not prescribe this ontology relation, a globally required product,
or a database design.

The decision keeps the existing provisional `logisticsProduct` association
from DistributionLogisticsActivity to MedicinalProduct, interpreted narrowly
as a **source-documented product type associated with one occurred logistics
activity**. The same product type may be associated with several events, and
one event may involve several product types. A broad product type does not
identify a batch, physical item, delivery note or consignment, and does not
establish successful delivery or legal compliance. No new global existential
or exactly-one axiom is introduced.

This has lower modeling cost than inventing item/consignment identity before
we have a required CQ and a source-specified identity criterion. Its limitation
is that batch-level provenance and route-level transport queries remain open.
An explicit consignment/batch participation object can be added later when
those queries and evidence justify its identity and temporal relations.

The [decision card](decision-card.json) records alternatives, temporal scope,
identity and native/OWL/SHACL effects. [Official-source locators](sources.json)
and [independent fixed boundary cases](fixed-oracles.json) precede implementation.
Only an opted-in source claim with an explicit event, named product type,
performed status and source record may project a candidate link. Candidate
triples remain source-qualified; they are not promoted to world truth.

The frozen packet changes no native/OWL artifact and does not close the
complete 2.2 release gate. A separate implementation/probe verifies these
boundaries and pins its own hosted evidence.

The [hosted receipt](ci-evidence.json) pins the frozen oracle commit, both
independent successful runs and byte-equal outputs. The bounded choice is
authorized under AUTH-22-01; full scientific model validation remains open.
