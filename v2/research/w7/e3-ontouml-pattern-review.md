# W7-E3 — UFO/OntoUML Pattern and Anti-pattern Evaluation

## Status
**PASS WITH WARNING — no blocking anti-pattern found.**

Evaluation family: `W7-E3`  
Issue: #92  
Actions run: `32235300963`  
Evidence artifact: `9358720068` (`cm-pharme-v2-w7-e3-ontouml-evidence`)  
Frozen executable checklist: `v2/evaluation/protocol/e3-pattern-checks.json`

## Evaluation boundary
This is a **project-native executable semantic review** of the frozen Gate-D conceptual registry and the W5 OWL projection. It is not an official OntoUML-tool execution, official OntoUML JSON conformance test, or automated certification by the OntoUML catalogue tooling.

## Result summary
- conceptual elements checked: **87**
- executable checks: **17**
- blocking failures: **0**
- non-blocking warnings: **3**
- official OntoUML tool executed: **false**

## Mandatory checks — PASS
1. The conceptual registry explicitly remains project-native (`official_ontouml_json=false`).
2. All 87 conceptual elements use the frozen stereotype vocabulary.
3. Gate-D conceptual stereotypes and W5 formal stereotype annotations agree **87/87**.
4. Ten concrete Role types are grounded in the expected identity-providing Kind and the `EcosystemParticipant` RoleMixin.
5. All principal Relator patterns expose the predefined minimum participant-facing mediation properties:
   - FacilityOperation
   - EstablishmentRegistration
   - RegulatoryAuthorization
   - ProductClassificationAssignment
   - MarketListing
   - EvidenceSupport
   - IdentifierAssignment
   - ContextualMedicineClassificationAssignment
   - AlternativeMedicineAssignment
   - SupplyDependency
6. `operates` remains explicitly marked as a material relation derived from the `FacilityOperation` Relator pattern.
7. All eight protected Gate-D distinctions remain explicit:
   - Organization ≠ Facility
   - Facility ≠ GeographicFeature
   - GeographicFeature ≠ RegulatoryJurisdiction
   - MedicinalProduct ≠ PharmaceuticalSubstance
   - MedicinalProduct ≠ MedicinalProductPresentation
   - ObservationActivity ≠ ObservationResult
   - MedicineShortageSituation ≠ SourceRecord
   - SupplyCapacity ≠ SupplyCapacityObservationResult
8. Essential/Critical medicine semantics remain contextual assignment specializations rather than rigid MedicinalProduct subtypes.
9. Frozen Event/Situation distinctions are preserved.
10. Frozen Mode/Quality stereotypes are preserved.
11. Principal characterization signals for Strength, MatchConfidence and SupplyCapacity remain explicit.
12. Identifier Value, Scheme and Assignment remain separated; Identifier Assignment remains relational.
13. Observation Activity and Observation Result remain separated and explicitly connected.
14. Rejected generic `componentOf`/catch-all V1 relation names remain absent from the V2 formal vocabulary.

## Non-blocking warnings
### W1 — Extension-only Relator mediation is incomplete in the OWL projection
`RegulatoryOversight` and `StrategicPartnershipAgreement` are conceptually typed as Relators but currently expose no participant-facing OWL properties. These are extension-only patterns and do not affect the principal article demonstrators or Core identity decisions. They should be completed before any strong claim about those extensions.

### W2 — Role relational dependence is not fully enforced with OWL existential restrictions
The Gate-D conceptual registry and typed Relator patterns preserve Role semantics, but none of the ten Role classes currently carries a direct OWL existential restriction that fully enforces relational dependence. This is a formalization boundary: the OWL projection preserves the conceptual distinctions but does not encode every OntoUML meta-property as an OWL constraint.

### W3 — Two extension Modes lack explicit bearer/characterization properties
`Vulnerability` and `EnterpriseCapability` remain conceptually typed as Modes but currently expose no explicit bearer property in the W5 OWL projection. Both are extension-level concepts. `Vulnerability` should be revisited before a strong Risk/Resilience ontology-alignment claim; `EnterpriseCapability` belongs to the optional Business Architecture view.

## Interpretation
The frozen CM-PharmE 2.0 Core and cross-cutting infrastructure preserve the principal UFO/OntoUML distinctions required by Gate D, and no blocking anti-pattern defined by the prospective W7-E3 checklist was detected. The three warnings are bounded formalization gaps in extension semantics or in the degree to which OntoUML meta-properties are executable in OWL.

This result supports the claim that UFO/OntoUML commitments are **explicit and systematically preserved in the evaluated project artifacts**, but it does **not** support a claim of official OntoUML-tool conformance.

## Next
W7-E4 / V2-066 / #93 — freeze and execute positive and negative competency questions against the ontology/evaluation KG.
