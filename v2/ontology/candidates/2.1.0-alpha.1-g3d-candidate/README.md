# G3-1d — nine-role integrated review candidate

Date: 2026-10-07 (Asia/Tehran). Parent repository revision:
`168a26c3ac8c3309ef3a97d0b91213d831d1b694`.

**The nine recommended structural role definitions are now implemented together
in a separate candidate, with OWL, native OntoUML JSON and SHACL constraints.**
This is authorized continuation of candidate implementation after the displayed
nine-decision table. It is not recorded as explicit final scientific approval,
an independent expert review or authorization to publish a release. PR #305
remains draft and issue #306 remains open.

## Concrete delta

| Inventory | G3a baseline | G3d candidate |
|---|---:|---:|
| Named classes | 119 | 138 |
| Datatypes | 6 | 6 |
| Concepts (named classes + datatypes) | 125 | 144 |
| Object properties | 63 | 81 |
| Named-class connected components | 15 | 15 |
| Isolated named classes | 14 | 14 |
| Largest named-class component | 105 | 124 |

Added nine Relators, ten supporting Roles and eighteen mediation properties.
No existing logical axiom was removed; candidate version/status annotations were
updated. An anonymous OWL union is a logical expression, not a new named concept,
and is excluded from inventory counts. All added named concepts join the existing
main component. This step improves definition coverage, **not the old islands**.

The nine new Relators are ManufacturingResponsibility, ManufacturingSiteUse,
ImportResponsibility, WholesaleResponsibility, LogisticsServiceCommitment,
DistributionSiteUse, RegulatoryMandate, ProductLabelResponsibility, and
InstitutionalFundingCommitment. Exact participant types and properties are in
`contract.json` under `g3_profiles`; the native JSON contains their Role ends,
cardinalities and metadata. Each normalized assignment has exactly one holder
and one distinct counterpart. Each defining Role requires at least one such
context. Different independent contexts can have the same pair of participants.
The participant ends are read-only within an identified episode; bearer identity
persists independently of acquiring/losing a Role.

## Three integration choices preserved

1. **Operational roles express responsibility/site use.** Permission and actual
   occurrence remain separate. None of the new rules equates registration,
   generic authorization, generic facility operation or a source label with the
   six operational responsibility roles. Scoped permission/occurrence query
   distinctions remain documented in G3-1b; this integration does not introduce
   six additional permission classes or a new ImportActivity Event.
2. **Product responsibility has alternative grounds.** The existing listing
   subtype remains. ProductLabelCommitmentOrganizationRole is a second subtype.
   OWL represents the parent as their union; native OntoUML has a complete,
   overlapping generalization set; SHACL requires either route. A listed actor
   need not acquire a second fabricated commitment. Completeness is limited to
   these two admitted routes and remains a scientific scope choice for review.
3. **Funding is institutional-only in this candidate.** Funder and funded party
   are distinct Organizations. Direct-person reimbursement, individual entitlement
   and self-funding are outside this profile; no Person or patient individuals
   were fabricated. This bounded interpretation must remain visible in the paper
   and final author review. Aggregate NHIF results remain observations.

The authority definition uses a mandate with an evidenced distinct conferring
organization. The conferring organization is not recursively forced into the
same authority Role. Existing authorizing/registering/oversight subroles now
inherit the mandate requirement. This ordered dependence is intentional and
requires catalogue-wide review, not automatic removal to silence MultDep.

## Executed evidence

| Check | Actual result and scope |
|---|---|
| New SHACL integration cases | 72/72 expected outcomes: nine seven-case context suites, three product-route cases and six authority-migration cases |
| New OWL contradiction cases | Four deliberately inconsistent models correctly rejected by **both HermiT and Pellet** |
| Schema and positive/countermodel witnesses | Both engines consistent; no unsatisfiable named classes |
| OWL 2 DL profile | OWLAPI 3.4.3: zero violations on tested positive and negative inputs |
| Native JSON schema | 520 elements; zero schema errors; unique identifiers and references checked separately |
| Identity providers | All nine inherited roles retain their intended single Kind identity |
| Legacy G1 contract regression | 120/120 cases under the new ontology **with the old admission contract**; this preserves the previous gate, not new mandate completeness |
| G2 bridges | 24/24 cases under new ontology and current combined constraints |
| Existing synthetic NHIF projection | Still conforms to current SHACL; no real rows ingested and no new full SQL mapping evaluation |
| Twelve previous non-entailments | Explicit complement witnesses remain jointly consistent in both engines |
| Earlier G3b/G3c SQL suites | Historical 156 and 107 results retained; not rerun or counted as new integration tests |

The four negative OWL cases exercise a ManufacturerRole explicitly constrained
to zero manufacturing responsibilities, a product-responsible actor explicitly
outside both permitted subroles, a mandate self-mediation, and an exact-one
funding assignment with two explicitly different counterparts. They are test
inputs under `lab/negative-*.rdf`, **not ontology imports**. Rejection is the
expected outcome, not a candidate inconsistency.

The twelve complement witnesses test those specific non-entailments. They are
not complete closed-world admission examples. Conversely, a missing required
triple can fail SHACL while OWL remains consistent under its open-world semantics.

## Migration finding: old authority examples need additional evidence

The old RegulatoryAuthorization, EstablishmentRegistration and RegulatoryOversight
complete-instance examples fail the new combined SHACL because their authorities
have no explicit mandate. The six migration tests demonstrate three failures and
three corrected **synthetic** examples with explicit mandate witnesses.

This is an intentional stricter completeness requirement, not a silently repaired
real dataset. The old 120-case suite is labeled separately so it cannot hide this
change. Source authority names or past acts must not be upgraded to mandates by
guessing a conferring body. Such rows remain incomplete source assertions until
evidence is available. No frozen baseline, held-out result or old mapping score
was overwritten.

## What is implemented, and what remains open

Implemented: named Role/Relator dependencies, local distinctness, cardinalities,
product alternatives, native serialization, identity checks and the tested
structural SHACL/OWL behavior. All nine targeted inherited-role definitions have
this structural implementation in G3d.

Still open: final scientific acceptance of meanings and scope; complete native
pattern/anti-pattern tooling; global relation typing; source-to-candidate migration;
full temporal/provenance admission for the new profiles; complete-instance
validation across real datasets and all domains. The earlier SQL laboratories
test interval/episode rules, but this step does not claim a full temporal OWL
semantics or a production SQL-to-RDF mapping for all new contexts. New positive
witnesses specifically test structural dependence; they are not fully evidenced
real-world commitments.

The 18 new mediation records are explicitly typed. The **42 previously unresolved
native relation records remain open**. No comprehensive diagram or release tag
was produced. The fourteen old isolates also remain; grounded Role definitions
do not automatically solve event/aboutness or optional-module connectivity.

The official OntoUML anti-pattern engine has **not run**. Schema validity,
reasoner consistency and scoped tests are not an all-domain conformance
certificate. Relevant intent/dispositions for FreeRole, RelRig, MultDep, RepRel
and RelOver are documented in the preceding G3b/G3c design reports and must be
rechecked on this integrated model.

## Reproduce

With the pinned G1 dependencies and Java 17+ with the compiler module:

```bash
python tools/v2_ontology/g3_integrate_roles.py
```

Inspect `model-validation.json`, `results.json`, `reasoner-results.json`,
`decisions.json`, `contract.json`, `lab/integration-tests.json`,
`lab/negative-reasoner-tests.json`, and `lab/authority-migration.json`.
The old contract replay is isolated under `lab/legacy-contract/`.

## Exact next step

**G3-2: resolve the 42 existing native relation records, starting with their
stereotypes, endpoint identity, multiplicities and any derivation/subsetting
conditions.** For each relation, record implement, justified exception or
evidence-bound deferral and test the affected cases. Include a separate queue for
the fourteen isolated concepts; do not add relations merely to decrease counts.

Then run supported native semantic/anti-pattern tooling (G3-3), finish source and
temporal/provenance migration plus Wiki/Pages/article traceability (G4), and prepare
the stable review/diagram gate (G5). Final scientific sign-off stays explicit;
it no longer blocks producing this concrete reviewable candidate.
