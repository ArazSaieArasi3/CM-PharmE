# G3-1b: six operational role patterns and executable relational design lab

Date: 2026-10-06. Baseline: `2cf06dc21ef13f8b2c96e14621afa3ece74a99e6`.
Status: **six-role design package complete and tested as a proposal; active ontology integration and human semantic disposition remain open**.

## Result and scope

All six operational roles now have explicit permission, responsibility/site-use,
and occurrence boundaries. The executable SQLite lab passes **156/156 scenarios**:
96 successfully admitted/query cases and 60 deliberately rejected input cases.
This is a small relational prototype of the proposed patterns, not a relational
equivalent of the complete ontology or evidence from real organizations.

No active ontology axiom changed. SHA-256 checks preserve the G3a baseline files.
The inventory remains 125 concepts, 63 object properties, 15 named-class graph
components and 14 isolates. The six proposed responsibility types and counterpart
roles below are design candidates and are **not included in those counts**.
No new OWL reasoner or official OntoUML detector result is claimed in this step.

## Decision: choose a precise meaning for the six inherited roles

The previous G3a review suggested broad umbrella meanings. This design refines
that recommendation: define each inherited operational role by an effective
responsibility or assigned site use. Preserve permission in scoped specializations
of the already existing AuthorizedOrganizationRole/AuthorizedFacilityRole; preserve
actual occurrence as event participation. Neither permission alone nor a completed
event silently establishes the ongoing responsibility role.

This is a proposed **meaning refinement**, not merely a missing-edge correction.
It requires author disposition and source mapping migration before active import.
An actor evidenced only by a license can still be represented as an authorized
actor. An observed actor without commitment evidence remains an event participant;
the model does not assert that it lacks responsibility in the world.

At time t, proposed role membership is defined by at least one effective,
scope-matching responsibility/site-use episode. The model does not require all
three facets simultaneously and does not require an active license to represent
the existence of a responsibility or an activity. Legal compliance is a separate,
jurisdiction-specific question; this design is not a compliance assessment.

## Six responsibility patterns

Each proposed Relator instance mediates exactly one bearer and one distinct
counterpart in this normalized assignment profile. Each currently instantiated
Role end requires 1..* such contexts; non-role bearers have no mandatory context.
The 1:1 assignment profile is a modeling choice, **not a universal claim about
legal agreements**. Multiple responsible organizations, products or facilities
are represented by multiple independently justified assignment episodes and a
shared source instrument reference where appropriate.

| Inherited role / identity | Proposed defining Relator | Other mediated Role / identity | Definition and rejecting boundary |
|---|---|---|---|
| ManufacturerRole / Organization | ManufacturingResponsibility | ManufacturingResponsibilitySubjectRole / MedicinalProduct | An organization assigned a documented manufacturing responsibility for the product. Physical site operation is not mandatory. A manufacturing label, authorization or isolated event alone is insufficient for this responsibility claim. |
| ManufacturingSiteRole / Facility | ManufacturingSiteUse | AssigningManufacturingSiteUseOrganizationRole / Organization | A facility assigned manufacturing use by the responsible organization; it retains this role while idle if the assignment continues. Generic operation or registration does not establish the manufacturing use. |
| ImporterRole / Organization | ImportResponsibility | ImportResponsibilitySubjectRole / MedicinalProduct | Documented responsibility for importing the scoped product into the identified jurisdiction. Generic authorization does not establish import scope; permission does not establish an import occurrence. |
| WholesaleDistributorRole / Organization | WholesaleResponsibility | WholesaleResponsibilitySubjectRole / MedicinalProduct | Documented wholesale responsibility for a scoped product. Logistics activity alone does not establish wholesale responsibility; ownership transfers require separate evidence. |
| ThirdPartyLogisticsProviderRole / Organization | LogisticsServiceCommitment | CommissioningLogisticsClientRole / Organization | An evidenced logistics-service commitment to a distinct client. Product is an optional scope reference in this pattern. Ownership of product is not derived. This is not by itself a complete DSCSA classification rule. |
| DistributionSiteRole / Facility | DistributionSiteUse | AssigningDistributionSiteUseOrganizationRole / Organization | Assigned distribution/storage use with a responsible organization and a validity interval. An idle site can retain the role; an unrelated facility operation is insufficient. |

The product-side responsibility roles refer to the existing MedicinalProduct
identity, not a text code, batch, physical package or invented product instance.
If evidence identifies only a product class or vague scope, retain the source
assertion; do not manufacture a product relatum to satisfy the profile. Internal
manufacturing responsibility can use the organization-product pattern without
inventing an external contracting organization. A contract instrument may evidence
several assignments; that does not make the document identical to a Relator.

## Authorization and event patterns

Reuse RegulatoryAuthorization with its existing AuthorizingAuthorityRole and
AuthorizedParty mediation. For each of the six scopes, define the corresponding
authorized bearer by a matching authorization context, not simply a new label.
The six scoped authorized roles are proposed derived specializations; their
scope condition must be expressed in the native model/OCL or implementation
constraints before claiming FreeRole is resolved. Scope and jurisdiction are
references/values, not extra mediated persons.

ManufacturingActivity and DistributionLogisticsActivity are existing Event
types. ImportActivity is only a proposed event type: it is not silently added or
equated with a shipment. Participation relates the observed actor/site to a
specific occurrence with occurrence evidence. It is not a mediation. This lab
does not claim that event participation alone satisfies the OntoUML Role C2
constraint, nor does it create new event-dependent Role classes.

The lab assumes an explicitly identified authorization authority; its mandate
and the full RegulatoryAuthorityRole definition belong to G3-1c. The remaining
product-label responsibility role must also be reconciled with the proposed
product-side roles before integration, to avoid competing responsibility terms.

## Identity, time, cardinality and repetition

- Bearer identity is inherited from exactly one existing Kind; role acquisition
  or loss does not create or destroy the Organization/Facility.
- Relator identity follows its constituting responsibility episode. The same
  participants may enter multiple independent commitments; neither a pair-based
  uniqueness constraint nor a source-row identifier is its identity principle.
- The lab accepts intervals [start,end). Start is included; end is excluded.
  A null end is allowed only when the supplied episode is explicitly open-ended.
  Unknown starts or unknown occurrence ends are rejected by this strict lab
  admission profile, not declared ontologically impossible.
- Expiration, revocation, termination or replacement ends the relevant episode.
  A role is lost only after its last effective matching context ends. Suspension
  or resumption is represented by separate effective intervals; the prototype
  does not infer intervals from raw status strings.
- The occurrence tests use finite integer days for transparent boundary tests;
  production mappings must preserve real temporal precision and time zones.
- IDs supplied as `episode_key` identify already reconciled episodes. Duplicate
  keys are rejected, but resolving two source records to the same real episode
  remains an upstream identity task. The lab does not solve entity resolution.

## Pattern and anti-pattern assessment

This is a targeted design review, not an execution of the official catalogue
detector and not an all-domain absence certificate.

| Rule / catalogue entry | Design action | Evidence now | Remaining gate |
|---|---|---|---|
| Role identity and mandatory dependence | Exactly one Kind per bearer; one defining responsibility context with nonzero lower bounds | Register plus lab identity/required-counterpart tests | Encode and validate native model |
| Relator / Mediation pattern | Two distinct mediated Role bearers; episode identity; evidence is separate | Missing/self/wrong-kind counterparts rejected | OWL/SHACL/native serialization |
| FreeRole | Give responsibility roles explicit mediation; scoped authorized subroles have explicit scope derivation | Definition and scope-query tests | Encode derivation and run detector; no absence claim |
| MultDep | Do not conjoin permission, responsibility and occurrence as universally mandatory | Permission-only, idle-responsibility and occurrence-only cases for every role | Check the integrated hierarchy |
| RelRig | Mediate anti-rigid Role ends, leaving underlying Kinds unmediated by these new patterns | Proposed ends and identity table | Native readOnly/meta-property checks |
| RepRel | Allow independent commitments for the same parties; distinguish repeated evidence of one episode | Duplicate episode rejected; independent episodes and renewals accepted | Review source identity mapping and native finding disposition |
| RelOver | Distinct relata within an assignment; no global disjointness of organizational roles | Self-mediation rejection | Exact catalogue trigger is not asserted: binary 1+1 profile does not meet its >2 upper-bound condition; inspect integrated model |

The lab does not check every possible context graph. A structurally valid evidence
tag does not establish that its contents are true, that an authority has a valid
mandate, or that a service meets a jurisdiction's legal definition. Missing admitted
evidence yields no supported facet in this closed-world query; it is not an OWL
negative assertion about the world.

## Test evidence and reproducibility

Run from the repository root with Python's standard library:

```bash
python tools/v2_ontology/g3_operational_patterns.py
```

- `role-pattern-register.json`: six machine-readable patterns, 18 facet definitions,
  exact cardinalities, temporal policy, source anchors and proposal status.
- `schema.sql`, `query.sql`: normalized entity/evidence/context lab and effective
  facet query. The `role` column selects a profile; it is not an asserted OWL type.
- `example.sql`: reproducible manufacturer and idle-site responsibility fixtures,
  with no authorization or occurrence invented.
- `cases.json`: all 156 input/expected/actual outcomes, including rejected inputs.
- `results.json`: run totals, SQLite version and baseline artifact hashes.

Twenty-six scenarios per role cover isolated facets, coexistence, insufficient
registration/operation, incorrect scope/jurisdiction, interval boundaries,
overlapping commitments, renewal, open-ended responsibility, duplicate episodes,
missing/wrong relata, wrong evidence and unbounded occurrence. The 96 admitted
cases include cases correctly returning no supported facet; they are not 96
positive role assertions. The 60 rejection cases are input-admission checks.

The previous 144 regression cases and dual-reasoner results remain evidence for
the unchanged G3a ontology; they were not rerun or counted as new tests here.

## Sources and claim boundaries

Repository anchors: W4 `stereotype-decision-matrix.md`, `relator-material-patterns.md`
R3/R4, `events-situations-observations.md`; W3 `candidate-relations-events.md`
V2R-003/004/008/024/025/026; G3a `role-decision-register.json`.

Official pages checked 2026-10-06:

- [Role](https://ontouml.readthedocs.io/en/latest/classes/sortals/role/index.html):
  unique identity and relational dependence motivate the explicit role definitions.
- [Mediation](https://ontouml.readthedocs.io/en/latest/relationships/mediation/index.html):
  the Relator must connect at least two distinct individuals.
- [FreeRole](https://ontouml.readthedocs.io/en/latest/anti-patterns/FreeRole/index.html),
  [MultDep](https://ontouml.readthedocs.io/en/latest/anti-patterns/MultDep/index.html),
  [RelRig](https://ontouml.readthedocs.io/en/latest/anti-patterns/RelRig/index.html),
  [RepRel](https://ontouml.readthedocs.io/en/latest/anti-patterns/RepRel/index.html),
  [RelOver](https://ontouml.readthedocs.io/en/latest/anti-patterns/RelOver/index.html):
  support the targeted design dispositions above, not blanket conformity.
- [FDA contract-manufacturing guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/contract-manufacturing-arrangements-drugs-quality-agreements-guidance-industry):
  distinguishes the documented manufacturing responsibilities of contracting
  parties. It motivates explicit responsibility evidence; it does not prescribe
  our exact Relator names, product counterpart or cardinalities.
- [FDA annual licensure reporting](https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/annual-licensure-reporting-wholesale-drug-distributors-and-third-party-logistics-providers):
  report entries alone are not proof of licensure or compliance. A generic record
  cannot simply be promoted to the lab's authorization-decision evidence.
- [DSCSA text hosted by FDA](https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/title-ii-drug-quality-and-security-act):
  its 3PL definition separates logistics services from product ownership. This
  informs the non-inference boundary; the six-role lab is not a DSCSA validator.

## Position and exact next step

G3-1b is complete **as a six-role design/prototype deliverable**. Six of nine role
definition packages are now designed at this level; zero of these six new
definitions has been imported into the active ontology or recorded as human
approved. G3-1 as a whole remains open.

**Next: G3-1c — design and test the three remaining contexts: authority mandate,
product/label responsibility, and funding/reimbursement commitment.** Start with
RegulatoryAuthorityRole: identify what confers its mandate, its jurisdiction,
effective interval and cessation, without requiring that it already issued a
license. Then reconcile all nine recommendations into one author-review decision
package and implement the agreed candidate definitions with OWL/native regression.

Following gates: G3-2 resolves the 42 native relation records (plus any introduced
by approved refinements); G3-3 executes supported native semantic/anti-pattern
checks; G4 handles full source/held-out/traceability checks and Wiki/Pages/article
updates; G5 is the stable human-review checkpoint and comprehensive diagram.
PR #305 stays draft and issue #306 stays open.
