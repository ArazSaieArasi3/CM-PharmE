# G3-1 inherited Role review and conservative repair

2026-10-06. Parent checkpoint: `a8500991dde903284e9c48fe13c74895cdacd234`.
This work completes the nine-role diagnosis and a justified hierarchy repair.
**It does not complete the nine roles' existential grounding. G3-1 remains open.**
The candidate is in draft PR #305, governed by issue #306; frozen 2.0/G1/G2
artifacts are unchanged. No final diagram, merge, tag or release was made.

## Concrete correction

Added the one-way generalization:

`ListingResponsibleOrganizationRole subClassOf ProductResponsibleLabelerRole`.

W4 `stereotype-decision-matrix.md` V2C-006 and `relator-material-patterns.md`
R6 explicitly place listing responsibility within the product-responsible role.
G1 introduced the narrower listing role but did not connect it to the inherited
broader role. The new axiom repairs that missing link in OWL, the conceptual
registry and native OntoUML JSON together.

This is **not equivalence**: broader product/label responsibility need not entail
a current market listing. Neither role entails ManufacturerRole. The existing
listing mediation grounds the narrower role; adding a subtype does not establish
existential dependence for every instance of its broader parent.

## Nine-role decision package

All nine Roles inherit exactly one intended identity provider. This passes the
identity check, not all Role constraints. The machine-readable register contains
exact W3/W4 anchors, recommendations, rejection examples and open decisions.

| Role | Identity | Recommended definition strategy | Reject this shortcut |
|---|---|---|---|
| ManufacturerRole | Organization | Separate authorization, manufacturing responsibility and participation in a particular occurrence; preserve a broader umbrella if contract production is included. | Every registered or licensed organization is an actual manufacturer in an observed event. |
| ManufacturingSiteRole | Facility | Distinguish assigned manufacturing function, authorization and event participation; allow an idle site to retain its function. | Facility operation or registration proves a manufacturing occurrence. |
| ImporterRole | Organization | Give import permission an explicit scope; model import responsibility separately. | Generic authorization proves import scope or an import transaction. |
| WholesaleDistributorRole | Organization | Explicit wholesale permission/responsibility; separate activity evidence. | Any establishment registration or logistics activity establishes wholesale distribution. |
| ThirdPartyLogisticsProviderRole | Organization | Ground the service responsibility separately from its permission and individual activities. | Logistics participation implies ownership of the product. |
| DistributionSiteRole | Facility | Explicit distribution/storage use context with validity, separate from operations and shipments. | Any operated facility is a distribution site. |
| RegulatoryAuthorityRole | Organization | Model the mandate separately from actual registration/authorization/oversight acts. | An authority exists as such only when it has already issued a license/registration. |
| ProductResponsibleLabelerRole | Organization | Keep broader responsibility; retain the corrected listing-responsible subtype; define any label-only context separately. | A labeler necessarily manufactures, or every responsibility necessarily has a market listing. |
| PayerFundingOrganizationRole | Organization | An explicit reimbursement/funding commitment, separate from observations and publication. | Publishing reimbursement counts proves the publisher is payer or establishes patient entitlement/payment. |

These recommendations are **not recorded as author/expert approval**. No new
mandatory license, operation, shipment, payment, mandate or event axiom was
silently imposed. In particular, no guessed relator was introduced merely to
make a graph check return zero unresolved roles.

## Evidence and why stronger automatic fixes were rejected

The official [Role specification](https://ontouml.readthedocs.io/en/latest/classes/sortals/role/index.html)
requires a unique identity provider and nonzero relational dependence. It also
warns about unintentionally requiring multiple dependencies. A drawn subtype or
a source label alone does not supply the missing role definition.

The official [FreeRole entry](https://ontouml.readthedocs.io/en/latest/anti-patterns/FreeRole/index.html)
describes a specific role-specialization pattern. The previous list of nine
unresolved inherited roles was a **grounding-review queue**, not nine confirmed
occurrences of that exact anti-pattern. A catalogue-wide official detector has
still not run.

[FDA eDRLS](https://www.fda.gov/drugs/guidance-compliance-regulatory-information/electronic-drug-registration-and-listing-system-edrls)
separates registration/listing from approval or verification of submitted
information. [DECRS](https://www.fda.gov/drugs/drug-approvals-and-databases/drug-establishments-current-registration-site-decrs)
has a particular establishment scope and does not include the separate wholesale
distributor/3PL reporting family. These source boundaries prevent a single
undifferentiated registration rule for all roles.

[openFDA NDC](https://open.fda.gov/apis/drug/ndc/) includes labelers whose
relationship to the product can involve private labeling. This supports preserving
the distinction between responsibility for a listing and performing manufacturing.
These official pages were checked on 2026-10-06; no live records were ingested.

Repository evidence at the parent revision:

- `v2/research/w4/stereotype-decision-matrix.md`
- `v2/research/w4/relator-material-patterns.md`
- `v2/research/w4/events-situations-observations.md`
- `v2/research/w3/candidate-relations-events.md`
- G2 `model-validation.json` and conceptual/native models.

## Executed validation

| Check | Result |
|---|---|
| Identity of inherited roles | 9/9 have the intended single Kind provider |
| G1 regression | 120/120 expected outcomes reproduced |
| G2 bridge regression | 24/24 expected outcomes reproduced |
| Existing synthetic NHIF projection | SHACL still passes; no new real-data claim |
| Unwanted-entailment countermodels | 12 explicit complements remain jointly consistent in both engines |
| New subtype rejection test | Both engines reject a listing-responsible individual explicitly outside the broader product-responsibility class |
| HermiT and Pellet | Schema and witness bundle consistent; no unsatisfiable named classes |
| OWLAPI 3.4.3 | Zero OWL 2 DL profile violations on the tested positive inputs |
| Official JSON schema | 435 elements checked; zero schema errors; references checked separately |
| Old logical axioms removed | Zero |

The twelve countermodels test specific **non-entailments**, not complete input
admission or complete role grounding. Open-world consistency of a partially
described individual is not evidence that its real-world role is established.
Likewise, the negative subtype example is deliberately inconsistent and expected
to fail; it is not a defect in the candidate.

Inventory remains **125 concepts (119 classes, six datatypes), 63 object
properties, 15 named-class components and 14 isolates**. Connectivity did not
change in this step. Nine complete grounding definitions and 42 native relation
records remain open. No numerical overall quality or completion score is claimed.

## Exact next step

**G3-1b: design the contextual patterns for the six operational roles**, starting
with ManufacturerRole and ManufacturingSiteRole. The concrete deliverable must
separate (1) scoped authorization, (2) a responsibility or site-use commitment,
and (3) an actual activity occurrence. For each, specify relata, identity,
cardinalities, temporal cessation, evidence boundary and a rejecting example.
Do not define broad roles as necessarily licensed or necessarily currently active.

Next handle the authority mandate, broader product responsibility and funding
commitment; then G3-2 resolves the 42 relation records and G3-3 performs the native
semantic/anti-pattern checks. G4 covers full source/held-out regression and
Wiki/Pages/article traceability. G5 remains author review and final diagram/release.

## Reproduce

Use the pinned G1 Python dependencies and Java 17+ with the compiler module:

```bash
python tools/v2_ontology/g3_role_review.py
```

See `role-decision-register.json`, `model-validation.json`, `results.json`,
`reasoner-results.json`, and the positive/counterexample/negative files under
`lab/`. The generated negative RDF is a test input and must not be imported into
the active ontology.
