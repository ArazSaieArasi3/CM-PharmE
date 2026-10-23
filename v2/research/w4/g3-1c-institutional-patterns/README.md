# G3-1c — institutional roles and the consolidated nine-role decision package

Date: 2026-10-06. Parent revision: `d27461e4a62855528154ae880c1736ed09707dd7`.
**Status: bounded design/prototype complete; ready for author review. Not integrated.**

The remaining three inherited roles now have proposed defining contexts, identity,
cardinalities, temporal cessation, source boundaries and rejecting examples.
The SQLite prototype passes **107/107 new scenarios**: 61 admitted/query cases
(including correctly empty query results) and 46 expected input rejections.
The two design packages now cover nine of nine review-queue roles. This measures
design-package coverage, not ontology completeness, release readiness or quality.

The active G3a ontology is byte-preserved. It still has 125 concepts, 63 object
properties, 15 named-class components and 14 isolates. None of the proposed role
definitions or new types in G3-1b/G3-1c has been integrated or marked human-approved.
The previous G3a hierarchy repair is already active and is not counted again.

## D07 — RegulatoryAuthorityRole

Recommended meaning: an Organization bearing a documented effective regulatory
mandate, in a specific functional scope and jurisdiction. This does not require
that it has already issued a license, registered an establishment or inspected
a facility.

Proposed pattern: `RegulatoryMandate <<Relator>>` mediates exactly one
`RegulatoryAuthorityRole` and one distinct
`MandateConferringOrganizationRole <<Role>>`; each Role inherits Organization
identity. Each current role instance has at least one defining mandate, while
an Organization without this role is not forced to acquire one. Jurisdiction and
functional scope are references, not additional mandatory mediated agents.

The conferring body is an evidenced institution, such as the organization whose
constituting act establishes the mandate. Its competence is an evidence boundary
in this prototype: it is **not recursively required to be another instance of
RegulatoryAuthorityRole with the same mandate**. This avoids manufacturing an
infinite authority chain. A legal text is evidence, not the granting Organization
or the Relator itself. If a source provides no defensible distinct conferring
institution, quarantine that incomplete mapping or revise the pattern; never
invent an institution or split one Organization into two to satisfy cardinality.
This is a bounded two-party modeling proposal, not a universal legal theory.

Loss: a role ceases when its last effective mandate in the relevant scope ends.
Mandate acquisition and organizational identity are separate. Issuing an act
after mandate expiry does not revive authority. In the integrated candidate,
RegisteringAuthorityRole, AuthorizingAuthorityRole and OversightAuthorityRole
must inherit mandate dependence and retain their activity-specific contexts.
The legitimate ordered dependence must be reviewed against MultDep; do not erase
it merely to suppress a detector finding. A historical authority act requires a
mandate valid at the act's time, not necessarily at today's snapshot.

## D08 — ProductResponsibleLabelerRole

Keep the broader role and the G3a one-way subtype:
`ListingResponsibleOrganizationRole -> ProductResponsibleLabelerRole`.
Add a proposed alternative role, `ProductLabelCommitmentOrganizationRole`,
grounded in `ProductLabelResponsibility <<Relator>>`.

The new Relator mediates exactly one commitment-bearing Organization role and
one `ResponsibilitySubjectProductRole <<Role>>` with MedicinalProduct identity.
Each current role on this route has 1..* matching responsibility episodes.
The existing MarketListing route continues to mediate ListingResponsibleOrganizationRole
and ListedPresentationRole. A Product and a ProductPresentation remain different
identity providers; neither is silently substituted for the other.

For the bounded proposed scope, define the parent through the **inclusive union**
of the listing-responsible and commitment-responsible subroles. The proposed
covering generalization set is overlapping, not disjoint. Either route suffices;
both are allowed. Do not attach an additional universally mandatory commitment
mediation to the parent: that would require every listed organization to have a
second, potentially invented responsibility episode. Future responsibility routes
require an explicit revision of this scoped covering decision.

This is a native-model design obligation, not a claim that the SQL UNION-like
query already proves OntoUML conformance. The complete/overlapping set, derived
conditions and all dependencies still require serialization and formal checking.

Reconciliation with G3-1b: its ManufacturingResponsibilitySubjectRole,
ImportResponsibilitySubjectRole and WholesaleResponsibilitySubjectRole are
**product-side roles**, while ProductResponsibleLabelerRole is an
**organization-side role**. A product is the object of responsibility, not the
responsible actor. Manufacturing responsibility also need not entail labeling
responsibility; no equivalence is proposed between their Relators or actor roles.

Evidence must support the specific responsibility. A free-text labeler name or
generic source row alone is not an admitted constituting context. An admitted
listing context supports listing responsibility, not manufacturing or regulatory
approval. When one responsibility route expires but another remains, the broader
role persists. With no admitted route, the lab returns no supported role; it does
not prove the real-world absence of responsibility.

## D09 — PayerFundingOrganizationRole

Recommended initial scope: institutional funding/reimbursement commitments.
`InstitutionalFundingCommitment <<Relator>>` mediates exactly one
`PayerFundingOrganizationRole` and one distinct
`InstitutionallyFundedOrganizationRole`; both have Organization identity.
Each current role requires 1..* effective commitments. A commitment has a stated
funding purpose/programme scope, jurisdiction and effective interval. Scope is
not a fabricated patient or payment individual.

This is a **proposed scope restriction requiring author disposition**, not full
coverage of every kind of payer. The present model has no admitted Person identity
for a patient-level funding pattern. Direct reimbursement to persons, individual
entitlement, a patient cohort's eligibility, self-funding within the same legal
organization and commitments with unspecified recipients are outside this lab
profile. Do not falsely require all real-world funders to fit it. If the author
requires those cases now, extend their identity/context patterns before importing
this definition or keep the broader parent unresolved with an explicit deferral.

A commitment can exist before any payment. An observed remitter may be an agent
and is not automatically the economically responsible funder. Publishing aggregate
reimbursement observations does not identify a commitment's parties or establish
an individual entitlement. No NHIF row was promoted to a funding commitment here.
No Patient, CoverageEntitlement, Payment or benefit programme individuals were
invented, and no financial-compliance claim is made.

## Shared temporal, identity and multiplicity policy

- Each new Relator has its own constituting institutional episode. The source
  document/row is evidence of the episode, not its identity principle.
- The exact-one pair is a normalized assignment profile, not a claim that all
  legal instruments have exactly two parties. Source instruments can support
  several assignments only when each assignment is independently justified.
- The same parties may have independent concurrent commitments. Duplicate
  episode keys are rejected; resolving source records to episodes is upstream.
- Half-open intervals [start,end) retain roles while at least one matching context
  persists. Null end means explicitly open-ended input, not unknown evidence.
  Suspension/resumption require separate effective episodes; raw status strings
  are not automatically OntoUML phases.
- Identity survives role loss. Counterparts are distinct within an episode;
  organizational roles are not globally disjoint across all episodes.
- The prototype uses integer days. Actual mapping must preserve source precision,
  jurisdiction and scope. Querying another jurisdiction or scope does not transfer
  authority, responsibility or funding.

## Executed tests and limitations

Twenty-three scenarios for each of four routes (mandate, label responsibility,
listing, funding) yield 92 cases. Fifteen additional scenarios examine overlapping
product routes, observations without commitments, three roles on one Organization,
expiry, and Product/Presentation non-interchangeability. Total: 107.

The tests assert expected error categories for rejected inputs, not merely that
some exception occurred. They cover role existence before exercise/payment,
start/end boundaries, jurisdiction and scope mismatches, renewal, overlapping
episodes, duplicate episode keys, missing/wrong counterpart identity, wrong
evidence classes, missing times and Product/Presentation confusion.

`observed_claim` is deliberately an evidence-record table. Its entries are not
formalized regulatory acts or payment Events and do not declare that an unsupported
act is legally valid. No trigger derives commitments from them. Conversely, the
prototype does not validate the complete ontology of regulatory acts or payments.

Pattern review addresses Role identity/dependence, two-relatum Mediation,
FreeRole definitions, alternative versus ordered dependencies under MultDep,
anti-rigid mediation ends under RelRig, and repeatable Relator identity under
RepRel. The exact RelOver trigger is not asserted for the binary 1+1 profiles;
context-local distinctness is still required. These are design dispositions, not
an official detector report. All three authority subroles and the product union
require native-model validation after integration.

Neither the semantic truth of supplied evidence nor completeness of all domain
cases follows from SQL admission. Empty closed-world query results are not OWL
negative assertions. No new OWL, HermiT/Pellet, SHACL or native OntoUML result is
claimed for this proposal. G3-1b's 156 tests remain a separate earlier suite; they
were not rerun or counted among these 107 new tests.

## Consolidated review and migration package

[`nine-role-decisions.json`](nine-role-decisions.json) contains all nine rows,
with recommendations, identity, definition, source package and explicit pending
author decisions. [`REVIEW-fa.md`](REVIEW-fa.md) is the concise Persian review table.
Each row must receive accept, amend or defer; execution is not author approval.

Before import, migrate raw legacy role labels into evidence-backed contexts or
quarantine them as source assertions. Do not silently drop source records or add
missing relata. In particular:

| Input | Candidate treatment |
|---|---|
| Generic manufacturer/importer/distributor label | Preserve source assertion; require the G3-1b context before responsibility-role admission |
| Scoped license evidence | Authorized role only; no fabricated occurrence or operational responsibility |
| Authority name in a record | Resolve organization; obtain mandate evidence or mark unresolved |
| G1-admitted listing responsibility | Preserve the existing subtype route; do not require an extra label commitment |
| Separate product-label commitment | New proposed commitment route; no invented listing |
| NHIF aggregate observation | Preserve observation mapping; no inferred funding commitment or patient entitlement |

All 42 pre-existing unresolved native relation records remain open. Integration
will add relation records, so 42 is a baseline count, not a fixed future total.

## Sources

Repository anchors: W4 stereotype matrix V2C-003/006/009; W4 R2/R3/R6/R13;
W3 V2R-072; G3a role review and listing subtype; G3-1b six operational patterns.
Official pages checked 2026-10-06:

- [OntoUML Role](https://ontouml.readthedocs.io/en/latest/classes/sortals/role/index.html),
  [FreeRole](https://ontouml.readthedocs.io/en/latest/anti-patterns/FreeRole/index.html),
  [MultDep](https://ontouml.readthedocs.io/en/latest/anti-patterns/MultDep/index.html):
  motivate explicit dependence and avoiding unintended simultaneous requirements.
- [WHO national regulatory system](https://www.who.int/publications/m/item/01-gbt-plus-rev-vi-plus-ver1-rs)
  and [clinical-trial oversight](https://www.who.int/publications/m/item/08gbt-plus-rev-vi-plus-ver1-ct):
  distinguish institutional regulatory functions; the latter explicitly describes
  a legal mandate for oversight. They motivate scoped mandate modeling but do not
  prescribe our two-party cardinalities or a universal granting-body pattern.
- [openFDA NDC](https://open.fda.gov/apis/drug/ndc/): distinguishes labeler responsibility
  and warns that listing information is not verified by inclusion. This supports
  separating label responsibility from performance of manufacturing.
- [WHO strategic purchasing](https://www.who.int/activities/promoting-strategic-purchasing):
  describes allocating pooled funds to providers for services. It motivates the
  institutional funding profile, not a claim that the profile covers all funders.

## Reproduce and next step

```bash
python tools/v2_ontology/g3_institutional_patterns.py
```

The script uses Python's standard library. `schema.sql`, `query.sql`, `example.sql`,
`cases.json` and `results.json` are reproducible outputs; results include SQLite
version and hashes of the unchanged active candidate artifacts.

**Exact next step: G3-1d — disposition of the nine-row decision package, then
implementation of the accepted definitions in a separate integration candidate.**
The concrete author choices are documented, particularly the responsibility-only
meaning of operational roles, the two-route product parent and the institutional
funding boundary. Apply accepted choices consistently to OWL, native OntoUML,
SHACL and mappings; run regression before claiming role grounding complete.
Following gates remain G3-2 relation typing, G3-3 official tooling, G4 full
data/traceability/Wiki/Pages/article alignment, and G5 stable review and diagram.
Issue #306 remains open and PR #305 remains draft.
