# G3-2a — native relation typing review overlay

Date: 2026-10-08 (Asia/Tehran). Source G3d commit: `336c3b7df02a93180970416a3ba1980cce5d2822`.

This is a **native OntoUML review overlay**, not a released 2.1 ontology, a full G3-2 disposition, or an all-domain anti-pattern certificate. The G3d OWL, SHACL, source mappings and frozen 2.0/W7 evidence remain the comparison baselines. PR #305 stays draft; issue #306 stays open. The G3d snapshot remains byte-preserved.

## Implemented delta

The 42 pre-existing records were enumerated from G3d: 41 had no native relation stereotype and `operates` already had `material` with `isDerived=true`. This overlay assigns `mediation` to precisely three of the 41:

| Relation | Grounded parent mediation | Endpoints |
|---|---|---|
| `contextClassificationEntry` | `classificationEntry` | ContextualMedicineClassificationAssignment (subkind of ProductClassificationAssignment) → AppliedClassificationEntryRole |
| `contextClassificationProduct` | `classificationEntity` | ContextualMedicineClassificationAssignment → ClassifiedMedicinalProductRole |
| `evidenceRecord` | `evidenceItem` | EvidenceSupport (Relator) → EvidenceSourceRecordRole |

In all three, **both association ends already subset the corresponding ends of the parent mediation**. The source has Relator identity (directly or through the specified subkind), and the target is a Role. The only changes inside the 520 native elements are those three stereotype values. The project ID/name identify this separate overlay.

The three multiplicity fields remain unspecified on these child associations. Their inherited relation context supports the stereotype decision; complete local cardinality, time-scoped dependence, concrete instances and semantic sign-off still need review. No OWL or SHACL rule has been silently added.

## Full triage of the 42 records

`relation-dispositions.json` records the name, typed endpoints, current end multiplicities, subsetting references, decision, rationale and required evidence for **each** record. The current categories are:

| Category | Count | Meaning |
|---|---:|---|
| `IMPLEMENTED_STEREOTYPE_ONLY` | 3 | Native mediation stereotype justified by existing parent subsetting; multiplicities remain to review |
| `PENDING_DOMAIN_SEMANTICS` | 20 | Need truthmaker, identity/dependence, direction and negative examples |
| `PENDING_RELRIG_DISPOSITION` | 3 | A Relator-to-rigid endpoint must not be converted to mediation without role or essential-dependence rationale |
| `PENDING_ENDPOINT_REFINEMENT` | 11 | A broad/untyped end prevents safe relation classification |
| `PENDING_PARENT_SEMANTICS` | 4 | Subsetting a parent with unresolved stereotype must be handled parent-first |
| `RETAIN_PRIOR_MATERIAL_PENDING_AUDIT` | 1 | Existing `operates` material derivation and scoped participant roles require checking |

Thus 42/42 records are inventoried, **3/42 have a stereotype-only change**, and **39/42 remain open for full disposition**. The current native inventory is 42 mediations, 38 untyped binary relations and one material relation; the 18 G3d new mediations are part of those 42 typed mediations. Concept and property counts, named-class connectivity (15 components, 14 isolates) and OWL semantics did not change.

## Checks performed and limits

- Parsed G3d native JSON and compared all 520 elements by ID and order.
- Verified exactly three element changes, each limited to `stereotype: null → mediation`.
- Checked all 520 IDs unique and all 81 binary associations refer to existing property IDs.
- For each edited association, verified both ends subset the existing mediation ends; the source Relator/subkind ancestry and anti-rigid target were checked.
- Counted the 42 prior records and the six disposition categories above.

These local structural checks do **not** rerun the official OntoUML JSON schema, semantic validator, anti-pattern engine, OWL reasoners, SHACL suite, relational mappings, or any real dataset. The existing G3d results apply to the unchanged G3d snapshot; they are not automatically new G3-2a test results. A null stereotype is not evidence that a relation is `formal`, and a Relator endpoint alone does not justify rigid-end mediation. See [official relationship stereotypes](https://ontouml.readthedocs.io/en/latest/relationships/index.html), [mediation](https://ontouml.readthedocs.io/en/latest/relationships/mediation/index.html), and [RelRig](https://ontouml.readthedocs.io/en/latest/anti-patterns/RelRig/index.html).

## Exact next step

**G3-2b:** start with the four child relations whose parents remain untyped, then the three Relator-to-rigid cases. Establish parent semantics, endpoint identity/roles, cardinalities and temporal/source evidence; write accepting and rejecting instances; apply only justified stereotype and constraint changes in a new native/OWL/SHACL candidate and run schema plus regression checks. Continue the remaining 32 records and maintain the separate queue of 14 isolates. Then G3-3 official semantic/anti-pattern tooling, G4 source and publication traceability, and G5 stable author review/diagram gate.
