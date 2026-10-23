# G1 — semantic decision package for the 2.1 review candidate

Status: **prepared for author review; G1 is not approved** (2026-10-04). This package applies only to the separate `2.1.0-alpha.0-review` candidate in draft PR #305. It neither amends Gate-D/2.0 nor certifies OntoUML conformance. A comprehensive OntoUML diagram is deliberately deferred.

## Scope and decision rule

The [machine-readable register](g1-relrig-decision-register.json) records **all 15** rigid-end mediation triggers in the candidate projection, with W3 relation IDs, W4 pattern numbers, the corresponding candidate OWL property, a provisional treatment, a counterexample and a specific author decision. `python tools/v2_ontology/check_g1_register.py` checks exact equality with the pattern audit's trigger set and resolves all project-internal references. A trigger is a review question, not a proved ontology error.

The [OntoUML RelRig catalogue](https://ontouml.readthedocs.io/en/latest/anti-patterns/RelRig/index.html) explicitly tests rigid types in mediation and the mediated end's `isReadOnly` condition; its refactorings include moving an optional mediation to an anti-rigid Role subtype. The [Relator](https://ontouml.readthedocs.io/en/latest/classes/sortals/relator/index.html) and [Mediation](https://ontouml.readthedocs.io/en/latest/relationships/mediation/index.html) specifications also require a relator to connect at least **two distinct individuals**, with the sum of appropriate minimum end multiplicities at least two. The W4 PlantUML and W5 OWL properties lack the native OntoUML `isReadOnly`, stereotype and end-bound declarations needed to prove or dismiss each trigger. Thus every proposal below is **unapproved**.

| ID | Current rigid end | W4 / W3 | Proposed semantic treatment for review | Decisive open question |
|---|---|---|---|---|
| RR-01 | FacilityOperation → Organization | R1 / 002 | Operator Organization Role | Can an Organization exist without this operation; how many current operators? |
| RR-02 | FacilityOperation → Facility | R1 / 002 | Operated Facility Role | Can a Facility exist between operations; how many facilities per operation? |
| RR-03 | Registration → Facility | R2 / 010 | Registered Facility Role, with Organization alternative | Which source registers a site versus an Organization, and what persists as the registration? |
| RR-04 | ClassAssignment → Product | R5 / 017 | Classified Entity Role; retain Product/Substance identities | Is the bearer a Product or Substance, and is classification contextual? |
| RR-05 | ClassAssignment → ClassEntry | R5 / 017 | **Reference candidate**, since W4 says “references” | If the Entry is only a reference, who is the second mediated individual? |
| RR-06 | MarketListing → Presentation | R6 / 018–019 | Listed Presentation Role | Is a labeler mandatory, and how do jurisdiction/time change participation? |
| RR-07 | EvidenceSupport → Assertion | R11 / 059, 062 | Supported Assertion Role or justified read-only rigid end | Which claim types are eligible, and can unsupported assertions exist? |
| RR-08 | IdAssignment → IdScheme | R10 / 066–067 | **Reference candidate**, since W4 says “references” | With IdentifierValue a literal, which two distinct individuals does assignment mediate? |
| RR-09 | AlternativeAssignment → Product | R8 / 023 | Reference/Affected Product Role | Which Product is the reference, and can Product/Presentation be interchanged? |
| RR-10 | SupplyDependency → Organization | R9 / 028 | Dependent/provider Role in source-bounded bearer family | Must a dependency contain an Organization at all? |
| RR-11 | SupplyDependency → Facility | R9 / 028 | Source Facility Role only when source supports it | Must a dependency contain a Facility at all? |
| RR-12 | Partnership → Organization | R14 / 078 | Partner Organization Role; two distinct participants provisionally | Does V1/W1 support a persistent agreement identity and two-party minimum? |
| RR-13 | EvidenceSupport → SourceRecord | R11 / 059, 062 | EvidenceItem bearer Role **or** provenance reference | Does the direct edge duplicate the EvidenceItem position? |
| RR-14 | ContextClass → Product | R7 / 021–022 | Contextually Classified Entity Role | W4 permits Product/Substance but candidate OWL ranges only to Product; which is intended? |
| RR-15 | ContextClass → ClassEntry | R7 / 021–022 | **Reference candidate** to a list/version entry | If only a reference, what are the two mediated individuals? |

**Cross-case decisions that block a safe automatic refactor:**

1. **RR-05/RR-08/RR-15:** W4's reference language conflicts with the projection's apparent mediation. Converting those arrows to reference without finding the relator's second distinct participant can create a worse Relator violation. ClassEntry/Scheme may instead play a grounded anti-rigid Role, or the assignment pattern may require remodeling; the author must decide the intended truth-maker.
2. **RR-10/RR-11:** The diagram's Organization–Facility pairing must not become a required pair. W4 R9 and V2R-028 allow Product/Organization/Facility/Activity dependent and Product/Organization/Facility source; C1 is conditional evidence, not a complete supplier network. The candidate `dependencyDependent` and `dependencyProvider` have no universal range.
3. **RR-07/RR-13:** `EvidenceSupport` has the information bearer (`EvidenceItem`), target assertion, and a direct SourceRecord property. The same record cannot be counted twice to satisfy the two-distinct-individual rule. Supporting evidence is provenance, not proof that a proposition is true.
4. **RR-12:** The candidate OWL/SHACL requires at least two distinct Organization values for Partnership. This is a review hypothesis for the Business Architecture extension, not a frozen domain fact; a Role subtype and agreement identity remain to be justified.

## Other G1 semantic blockers

| Item | Evidence in candidate | Required author decision |
|---|---|---|
| IdentifierAssignment | `identifierEntity` is untyped at the range; `identifierScheme` has a range; IdentifierValue is correctly a datatype value in the candidate drawing. | Scope polymorphic bearers, issuer and assignment identity; explicitly identify at least two *distinct* mediated individuals, not a value and not a duplicate end. |
| RegulatoryOversight | W5 candidate has `oversightAuthorityRole` and untyped `oversightGovernedEntity`; the drawing has only one typed mediation. | Decide governed Organization/Facility/Activity roles, exact persistent oversight commitment, two distinct participants and multiplicities. |
| EvidenceItem `RoleMixin` | Abstract, without concrete drawn Role subtypes. | Name source-supported, identity-bearing information-object Roles (for example SourceRecord only if its evidence participation is genuinely contingent) or defer the generalization. |
| AssetAtRisk `RoleMixin` | Abstract, without concrete drawn Role subtypes. | Determine whether Product, Organization, Facility or other identity bearers can acquire this relational risk role; avoid a generic bearer with no source or threat relation. |
| ClinicalParticipant `RoleMixin` | Abstract, without concrete drawn Role subtypes; V1-driven optional Clinical extension. | Admit independently supported clinical Roles or keep the extension inactive. Held-out pressure is not author approval. |
| BinOver / RelOver carry-over | Candidate marks `withinCountry` and `withinRegion` irreflexive; SHACL separates alternative/reference Products. | Verify these two property guards and whether the alternative positions can overlap in any intended context. Native OntoUML meta-properties remain untested. |

The [`RoleMixin` specification](https://ontouml.readthedocs.io/en/latest/classes/nonsortals/rolemixin/index.html) requires an abstract, anti-rigid type spanning identity principles. A bearer list alone does not establish a valid RoleMixin; concrete identity-bearing role generalizations and relational grounding need review.

## Quantitative outcome and release boundary

- **15/15** visible candidate RelRig pairs are in the register, covering **10 relator types** and their evidence/source/property links; **0/15** are author-approved or certified resolved.
- **3** additional abstract RoleMixins lack drawn concrete role specializations; IdentifierAssignment and RegulatoryOversight still lack a fully typed, justified two-participant conceptual pattern.
- The G1 work changes **no** ontology class, property, axiom, W7 measure, Wiki publication or comprehensive diagram. Candidate inventory remains 87 concepts and 57 object properties as reported in [the parent pattern review](pattern-review-2.1.md).
- G1 can close only after a named reviewer/author records **accept / revise / reject / defer** for each case, rationale and counterexample disposition, identity provider, relational dependence, two distinct relata, both association-end multiplicities and `isReadOnly`/Role choice where relevant. Any accepted structural change must then update the conceptual registry, native model and OWL/SHACL together, followed by validation. Mere completion of the 15-row checklist is not an all-anti-pattern certificate.

## Sequence after author disposition

**G2:** examine the ten proposed cross-domain connections and optional modules against admitted sources. **G3:** construct native OntoUML JSON with typed relations, multiplicities and meta-properties; run official validation and inspect all anti-pattern findings. **G4:** complete OWL 2 DL, two-reasoner, SHACL/CQ, mapping/held-out and manuscript/Wiki traceability regression. **G5:** author sign-off on remaining findings and prepare `2.1.0-alpha.1`. Only after these gates should a comprehensive OntoUML diagram be assembled and reviewed.
