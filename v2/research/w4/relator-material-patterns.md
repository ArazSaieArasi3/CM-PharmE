# W4 Relator and Material-Relation Patterns

## Modeling rule
A relationship is reified as a `<<Relator>>` only when the domain requires an individual truth-maker with its own identity, validity, evidence, status or commitments. Simple reference, descriptive and spatial relations remain formal/reference relations. This avoids both under-modeling and gratuitous reification.

OntoUML requires Relators to be existentially dependent on and mediate at least two individuals; material relations can be derived from Relators and their mediation relations.

## Core relator patterns

### R1. Facility Operation
`Facility Operation <<Relator>>`
- mediates `Organization` (operator/responsible party)
- mediates `Facility`
- may have validity interval and evidence

Derived material relation: `operates(Organization, Facility)`.

Rationale: operation/responsibility can change while Organization and Facility retain identity. It must not be encoded as `Facility componentOf Organization` because a physical facility is not a mereological component of a social/legal organization.

### R2. Establishment Registration
`Establishment Registration <<Relator>>`
- mediates `Regulatory Authority Role`
- mediates `Facility` and/or `Organization` according to source scope
- refers to `Regulatory Jurisdiction`
- has identifier assignment / validity / status evidence

Derived material relation: `isRegisteredWith(regulatedEntity, authority)`.

Source registration records remain `Source Record` evidence; the record is not identical to the regulatory relation.

### R3. Regulatory Authorization
`Regulatory Authorization <<Relator>>`
- mediates `Regulatory Authority Role`
- mediates a regulated Organization/Facility role
- scopes permitted activity/role
- applies in `Regulatory Jurisdiction`
- has validity/evidence

Derived material relation: `isAuthorizedFor(regulatedParty, activityOrRole)`.

A license document/identifier is evidence or an identifier assignment associated with this relator, not its ontological identity principle.

### R4. Facility and Organization role mediation
`Ecosystem Participant <<RoleMixin>>` is an abstract anti-rigid pattern. Concrete roles must be grounded by relations/relators such as authorization, facility operation, market listing or domain activities. Role existence cannot be justified only by a label in a source row.

## Product and classification relators

### R5. Product Classification Assignment
`Product Classification Assignment <<Relator>>`
- mediates `Medicinal Product` or `Pharmaceutical Substance`
- references `Classification Entry`
- is governed by `Classification Scheme`
- may have source/version/jurisdiction/time context

Derived relation: `classifiedAs(product, classificationEntry)`.

This prevents an ATC code or other classification identifier from becoming Product identity.

### R6. Market Listing
`Market Listing <<Relator>>`
- mediates `Medicinal Product Presentation`
- mediates/relates `Product-Responsible / Labeler Role` when available
- applies in a source/jurisdiction/time context
- carries source-defined listing/marketing status value

Derived relation: `isListedIn(productPresentation, context)`.

Listing/marketed status is relational/contextual, so Product itself is not specialized into intrinsic `ListedProduct`/`UnlistedProduct` phases.

### R7. Contextual Medicine Classification Assignment
Generic relator for classifications whose truth depends on a list/context rather than intrinsic Product nature.

Subkinds:
- `Essential Medicine Classification`
- `Critical Medicine Classification`

Participants/context:
- Product/Substance
- list/version/source
- jurisdiction/policy context

This is the principal reason `Essential Medicine` and `Critical Medicine` are not rigid Product subkinds in V2.

### R8. Alternative Medicine Assignment
`Alternative Medicine Assignment <<Relator>>`
- mediates a reference/affected Product or Presentation
- mediates another Product bearing `Alternative Medicinal Product Role`
- is scoped by shortage/policy/list/therapeutic context

Derived material relation: `isAlternativeTo(productA, productB, context)`.

The Alternative role is anti-rigid: a product can be an alternative in one context and not another.

## Supply/resilience relators

### R9. Supply Dependency
`Supply Dependency <<Relator>>`
- mediates a dependent Product/Organization/Facility/Activity
- mediates a provider/source Product/Organization/Facility
- may reference geographic exposure and supporting evidence

Derived material relation: `dependsOnSupplyFrom(dependent, providerOrSource)`.

Boundary: W4 defines the pattern, but W6 may instantiate it only where source evidence justifies a dependency. It must not be used to imply a complete global supplier→buyer→shipment graph.

## Integration and evidence relators

### R10. Identifier Assignment
`Identifier Assignment <<Relator>>`
- mediates identified entity
- connects `Identifier Value`
- references `Identifier Scheme`
- may reference issuer/source and validity

Derived relation: `hasIdentifier(entity, valueUnderScheme)`.

This preserves source-scoped identifier semantics and prevents NDC, ATC, OMS, local facility codes or GeoNames IDs from being treated as universal identities.

### R11. Evidence Support
`Evidence Support <<Relator>>`
- mediates an information resource bearing `Evidence Item <<RoleMixin>>`
- mediates an `Assertion`, `Mapping Assertion`, `Entity Match Assertion` or model decision
- may carry support type/strength/provenance

Derived relation: `supports(evidenceItem, claim)`.

### R12. Mapping and Match Assertions
`Mapping Assertion` and `Entity Match Assertion` are modeled as propositions (`Assertion` subkinds), not Relators. They *state* correspondences; their truth/evidence is handled through Evidence Support and provenance. This avoids conflating a proposition with the domain relation it asserts.

## Extension relators

### R13. Regulatory Oversight
Extension-level `Regulatory Oversight <<Relator>>` mediates authority role and governed entity/activity where a persistent oversight relation is explicitly needed beyond authorization/registration.

### R14. Strategic Partnership Agreement
`Strategic Partnership Agreement <<Relator>>` mediates participating Organizations and commitment-bearing partnership relations. It remains BA/Partnership extension semantics.

## Non-relator decisions
The following are deliberately **not** Relators:
- `Strength` — Quality.
- `Supply Capacity` — Mode/disposition.
- `Medicine Shortage Situation` — Situation.
- `Observation Activity` — Event.
- `Observation Result` / Assertions — information objects.
- geographic containment/within relations — formal/spatial relations unless later evidence requires a richer truth-maker.

## W5 handoff
W5 should encode each approved Relator with explicit `<<Mediation>>` associations and may add derived `<<Material>>` relations for query convenience. Cardinalities must be justified from domain constraints rather than copied from source table foreign keys.
