# CM-PharmE: 17-domain OntoUML pattern review and 2.1 design candidate

Status: **review candidate, not a semantic release or conformance certificate** (04 October 2026). This expands W7-E3 rather than replacing its frozen result. The 2.0 Gate-D/W5 baseline, W7 scores, mappings and manuscript claims remain unchanged.

## Method and evidence boundary

- Sources: the 87-concept Gate-D registry, all six W5 Turtle modules, the W4 overview and corrected projection, W3 relation inventory, W4 design decisions, W7-E3, and the OntoUML [specification](https://ontouml.readthedocs.io/en/latest/), [four pattern catalogue entries](https://ontouml.readthedocs.io/en/latest/patterns/index.html) and [20 anti-pattern catalogue entries](https://ontouml.readthedocs.io/en/latest/anti-patterns/index.html).
- Reproduce [the machine-readable screen](pattern-audit-baseline.json) with `python tools/v2_ontology/pattern_audit.py`. It enumerates every one of the 17 W4 domains, 12 drawn Relators, their mediation endpoints, four RoleMixins, Mode/Quality characterization and cross-projection anomalies. A trigger means *inspect*, not that an anti-pattern is proved.
- W4 PlantUML lacks native OntoUML association-end multiplicities, read-only flags, generalization sets, formal/material classifications for every arrow and existential-dependence constraints. The project-native JSON is **not official OntoUML JSON**. Therefore neither an absence of a trigger nor the old 17-check PASS proves that all 20 catalogue anti-patterns are absent.

## Four documented pattern families

| Pattern | Current application | Review outcome |
|---|---|---|
| Relator | 12 Relator types; 10 principal Relators have at least two W5 outgoing object-property proxies. In W4 diagram, `ContextClass`, `RegulatoryOversight`, and `Partnership` have fewer than two drawn mediation edges; `IdAssignment` has two but one ends at a datatype. | W5 proxies alone cannot prove two **distinct mediated individuals** or their lower multiplicities. Candidate adds extension properties, a `2..*` partnership end, and fixes the value edge. Oversight and identifier participant typing remain open. |
| RoleMixin | `EcosystemParticipant` is abstract and spans Organization and Facility roles. `EvidenceItem`, `AssetAtRisk`, and `ClinicalParticipant` are abstract but have no concrete drawn role specializations. | The former has a defensible multiple-identity pattern. The latter three need concrete identity-bearing roles or an explicit deferred-module decision before activation. |
| RoleMixin alternative | Product's `AlternativeMedicinalProductRole` inherits `MedicinalProduct` identity in both projections, but W5 also assigns it to actor-oriented `EcosystemParticipant`, unlike W4 drawing. | Candidate removes the **actor RoleMixin** parent, retaining the Product Kind parent and the alternative-assignment Relator. Product is not silently cast as an actor. |
| Phase partition | No `Phase` stereotype or complete/disjoint intrinsic phase partition is asserted. | Appropriate restraint: source status values do not justify inventing a phase partition. |

Official constraints underlying the checks: Relators require mediation with minimum opposite-end cardinalities summing to at least two; mediation links a Relator to the individuals it connects; RoleMixins are abstract, anti-rigid and span identity principles; Modes require characterization by exactly one bearer. See the specification pages for [Relator](https://ontouml.readthedocs.io/en/latest/classes/sortals/relator/index.html), [Mediation](https://ontouml.readthedocs.io/en/latest/relationships/mediation/index.html), [RoleMixin](https://ontouml.readthedocs.io/en/latest/classes/nonsortals/rolemixin/index.html) and [Mode](https://ontouml.readthedocs.io/en/latest/classes/aspects/mode/index.html).

## Catalogue-wide anti-pattern screen

`No drawn trigger` is limited to the available representation. `Undetermined` is an open validation item, not a pass. The catalogue itself states that anti-patterns identify potentially unintended consequences and require interpretation.

| Anti-pattern | Static result | Evidence / action |
|---|---|---|
| BinOver | Undetermined | Association-end bounds and specialization/subsetting metadata absent. |
| DecInt | Undetermined | Decisive intensional/dependence constraints absent from W4 serialization. |
| DepPhase | No applicable Phase | No `Phase` in 87-element inventory. |
| FreeRole | No exact drawn trigger; dependence open | No Role→Role subtype chain is drawn; ten concrete roles still lack OWL existential grounding. |
| GSRig | Undetermined | No explicit generalization-set membership to test mixed rigidity. |
| HetColl | No typed `memberOf` pattern drawn | Do not infer absence of all mereological mistakes from this. |
| HomoFunc | No typed `componentOf` pattern drawn | Organization–Facility `componentOf` was explicitly rejected at Gate D. |
| ImpAbs | Undetermined | Needs association upper bounds and subtype-specific constraints. |
| MixIden | Undetermined for three abstract RoleMixins | No concrete specializations of EvidenceItem/AssetAtRisk/ClinicalParticipant; cannot establish multiple bearer identities. |
| MixRig | No rigid descendent of a RoleMixin found in W4 | Candidate also removes the incorrect Product-role actor inheritance in W5. |
| MultDep | Undetermined | Several entities participate in multiple Relators; their dependency conditions must be compared before calling this redundant. |
| PartOver | No typed part-whole pattern drawn | Requires mereology and multiplicities to decide. |
| RelComp | Undetermined | Completeness of Relator mediation and material derivation is not encoded in native metadata. |
| RelOver | Undetermined | Requires relation identity and overlapping ends. |
| **RelRig** | **12 rigid-end mediation triggers** | Examples: FacilityOperation→Organization/Facility, ClassAssignment→Product/ClassificationEntry, EvidenceSupport→Assertion. Some are legitimate optional participation in a Relator; decide role subtypes, read-only mediation or alternative relation per case. No blanket pass. |
| RelSpec | Undetermined | EvidenceSupport→EvidenceItem versus →SourceRecord may require a documented subsetting/role specialization; no relation-generalization metadata. |
| RepRel | Undetermined | Compare repeated participant relations and derived material edges individually; W5 properties alone are insufficient. |
| UndefFormal | Undetermined | Aboutness and other context arrows need derivation/quality basis or retyping; avoid generic formal links. |
| UndefPhase | No applicable Phase | No `Phase` stereotype in the registry. |
| WholeOver | No typed part-whole pattern drawn | Cannot evaluate unrepresented whole-overlap constraints. |

`RelRig` is a **trigger, not an automatic logical inconsistency**: its catalogue advises role-subtype refactoring when mediation is optional for a rigid Kind. The `FreeRole` and `UndefFormal` entries also require semantic evidence, not a count alone. The old W4 manual anti-pattern review's unqualified “no critical/high semantic defect” conclusion is consequently **too strong for this expanded catalogue-wide screen**; it remains a historical Gate-D decision, not a current all-clear.

## Domain-by-domain disposition

All 87 concepts in all 17 domains were included. `Review` means an explicit decision remains; it does not imply that every type in that domain is defective.

| Layer / domain | Concepts | Pattern or anti-pattern focus | Disposition |
|---|---:|---|---|
| Core — Ecosystem Organization | 8 | RoleMixin spans Organization and Facility, but concrete roles need relational dependence. | Review role grounding. |
| Core — Facility Operations | 4 | FacilityOperation mediates two rigid Kinds (RelRig triggers). | Review optional operator/facility roles and lower bounds. |
| Core — Regulatory Governance | 3 | Registration's Facility end is rigid; authorization participants are polymorphic. | Review role/mediation ends and jurisdictions. |
| Core — Pharmaceutical Product | 10 | Classification and listing mediate rigid Product/Entry/Presentation; Strength bearer is explicit. | Review RelRig cases; preserve three identities. |
| Core — Supply Operations | 4 | Capacity Mode has a bearer proxy, but polymorphic end and situation timing need rules. | Review bearer and temporal constraints. |
| Core — Ecosystem Observation | 3 | Subkinds of ObservationResult, separate from phenomenon. | Preserve distinction; qualify aboutness. |
| X-INFRA — Spatiotemporal Context | 7 | Four unattached datatypes in W4 are values, not orphan domain classes. | Map through values, not false mediations. |
| X-INFRA — Evidence Traceability | 13 | EvidenceItem lacks concrete Role subtypes; EvidenceSupport→SourceRecord exists in W5. | Review evidence bearers and Assertion RelRig. |
| X-INFRA — Entity Identity | 5 | IdentifierValue was incorrectly drawn as mediated; identifierEntity has no universal range. | Value edge corrected in candidate; bearer role open. |
| Extension — Regulatory Policy | 2 | Oversight has only one drawn mediation; W5 had no participant properties. | Candidate adds two properties; distinct participants/typing open. |
| Extension — Supply Resilience | 11 | Product RoleMixin mismatch in W5; ContextClass links absent from W4; dependency participants rigid. | Mismatch removed and contextual links drawn in candidate; review supply cases. |
| Extension — Market Access | 3 | Payer role dependence and isolated diagnosis reference. | Require source-backed context link. |
| Extension — Risk Management | 5 | AssetAtRisk has no concrete Role subtype; Vulnerability bearer missing in W5. | Candidate adds bearer property; bearer role remains open. |
| Extension — Pharmacovigilance | 3 | Reporting/Surveillance Events relate to requirements; event versus case boundary. | Retain module, review task data before new case type. |
| Extension — Business Architecture | 4 | Partnership mediations and Capability bearer incomplete; ServiceSpec isolated. | Candidate adds participant/bearer constraints; service identity open. |
| Extension — Digital Systems | 1 | DigitalComponent isolated. | Defer module activation or justify source-backed activity relation. |
| Extension — Clinical Care | 1 | ClinicalParticipant abstract RoleMixin with no bearer subtype or care activity. | Defer activation until an admitted care pattern exists. |

## Executed 2.1 design changes

The separate [2.1.0-alpha.0-review candidate](../../ontology/candidates/2.1.0-alpha.0-review/) contains **six full Turtle modules in a 2.1 namespace**, a project-native 87-element registry, a review diagram, and candidate SHACL plus positive/negative smoke data. Rebuild with `python tools/v2_ontology/build_21_candidate.py`. It is not an imported overlay of 2.0: OWL is monotonic, so merely adding an axiom could not remove the erroneous inheritance.

| Change | Why | Constraint / remaining limit |
|---|---|---|
| Remove `AlternativeMedicinalProductRole ⊑ EcosystemParticipant`; retain `⊑ MedicinalProduct` | Product's contextual alternative role has Product identity, not actor identity. | Review role dependence on AlternativeMedicineAssignment. |
| Add `vulnerabilityBearer` and `capabilityBearer` | Repair two W7-E3 W3 Mode-bearer gaps. | Candidate OWL exact-one bearer; `AssetAtRisk` concrete Role subtypes still undecided. |
| Add `oversightAuthorityRole`, `oversightGovernedEntity` | Expose the two participant positions defined in W4. | Governed end intentionally has no universal range; SHACL excludes the same value in both positions. |
| Add `partnershipParticipant` | Represent at least two distinct Organization participants. | OWL qualified min 2 and candidate SHACL min 2; verify agreement semantics with author. |
| Recast `IdentifierValue` diagram edge as a value relation | Datatype values are not individuals mediated by a Relator. | The polymorphic identified-bearer mediation remains a blocking conceptual decision. |
| Show both W5 contextual-classification links and existing source-record evidence mediation | Repair omissions in the W4 visualization. | No new dataset evidence or retrospective W7 result change. |

**Candidate quantity:** 87 conceptual elements (81 classes, six datatypes), **57** object properties versus 52 in 2.0; no concept added or removed yet. There are five new candidate properties, one removed subclass axiom, three new OWL cardinality restrictions and four focused SHACL node shapes. This is a provisional implementation, not a released improvement score.

## Verification performed and limits

- Baseline W7-E3 rerun: **17 checks, zero blocking failures, three warnings**, reproducing the frozen result. It is not reused as a candidate 2.1 certification because its role-grounding list hard-codes the product role as an EcosystemParticipant.
- Candidate six Turtle modules parsed; **81/81 classes and 6/6 datatypes** retain matching conceptual stereotype annotations; eight protected distinction pairs remain explicit. New candidate restrictions and properties were checked structurally. A local HermiT classification through Owlready2 found **zero unsatisfiable named classes**; this is not an OWL 2 DL profile report or multi-reasoner agreement.
- Candidate SHACL smoke: positive data **0 violations**; intentionally negative data **4 violations** (missing Mode bearer, excess Capability bearers, same Authority/Governed oversight value, one-party Partnership). These tests cover the *new* constraints, not the entire 2.0 mapping/KG.
- Native OntoUML JSON schema validation, official-tool anti-pattern detection, exhaustive Relation meta-properties, full 2.1 OWL/SHACL/CQ/mapping/E2–E13 regression, and a rendered diagram inspection are **not yet complete**. Therefore **zero OntoUML anti-patterns cannot presently be certified**.

## Human-review gates before a 2.1 release

1. **G1, semantics:** decide the 12 RelRig triggers one by one (legitimate rigid participation with read-only end versus new anti-rigid role), type and constrain the identified entity and oversight governed participant, and decide evidence/asset/clinical RoleMixin concrete bearers. Record source, definition, counterexample, cardinalities and rejection condition for each in #159/#173.
2. **G2, source and scope:** decide C03–C14 from the connectivity register and whether isolated Digital Systems, Clinical Care and Service Offering types stay as documented optional extensions. Discover new concepts only where an admitted source or competency question requires them; no expansion merely to connect the graph.
3. **G3, native model:** build official OntoUML JSON with relation stereotypes, meta-properties, multiplicities and generalization sets; run the official schema/validator and a tool-supported anti-pattern catalogue review. Resolve every finding with accepted refactoring or a documented justified exception.
4. **G4, formal/evidence regression:** run OWL 2 DL profile and two reasoners, all baseline and candidate SHACL/CQs, source mappings, held-out boundaries, figure/Wiki/manuscript traceability and the claim ledger. Record before/after separately; do not overwrite frozen W7 first-pass results.
5. **G5, author sign-off:** approve the concept/relation migration matrix and decide whether 87 elements and 57 properties are the accepted 2.1 inventory. Only then label `2.1.0-alpha.1` and make any no-unresolved-critical-antipattern claim within the validated scope.

### Negative acceptance conditions

Reject the candidate as a release if a datatype is mediated, a Relator lacks two distinct justified participants, a Mode lacks exactly one bearer, a RoleMixin is treated as a concrete bearer or imposes a false identity, an unbounded formal relation is used only to connect islands, a 2.0 protected distinction is collapsed, a held-out result is retroactively altered, or official validation is presented as having run when it has not.
