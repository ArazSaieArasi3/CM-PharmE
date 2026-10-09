# G3-2c — broad endpoint review and scope guardrails

Date: 2026-10-08 (Asia/Tehran). Source revision: `d95b5640c14d2c43c1e88a9a76ef78067f058916`. This is a bounded 11-relation **design review**, not a new formal-model version, author sign-off or complete G3 validation.

## What was done

All eleven prior binary relations with one unspecified native end were compared with G3d OWL domain/range, W4 conceptual documentation, the historical human relation-review records, and relevant W6 mapping contracts. `endpoint-decisions.json` gives each relation's recommended policy, semantic reason, source link, positive **synthetic illustration**, negative acceptance condition, unresolved evidence and pending author disposition. `consolidated-relation-register.json` now presents all 42 old records in one list with review depth; original G3-2a/b snapshots remain intact.

| End policy | Relations | Result |
|---|---|---|
| Mapping-specific scope, generic ontology parent retained | `hasActiveSubstance`, `locatedIn` | W6 M016 binds `medicinal_product.primary_substance_id`; M031 binds `facility.geography_id`. These are **two registered mappings**, not proof that every use of the parent property has those source types. W4 also admits Product/Presentation active-substance semantics. |
| Directed Mode/bearer refactor required | `capacityBearer` | W4 says SupplyCapacity is a Mode of Organization or Facility. The current property points Mode→unspecified bearer; [OntoUML Characterization](https://ontouml.readthedocs.io/en/latest/relationships/characterization/index.html) is bearer→Mode with existential dependence. A direct stereotype on the current association would misstate the direction. |
| Common target semantics/identity unresolved | `baViewRepresents`, `disruptionAffects`, `observationResultAbout`, `riskAssessmentConcerns`, `riskTreatmentAddresses`, `usedSourceArtifact` | Target families span different identity/layer types. No invented common supertype or restrictive OWL range was added. |
| Paired match endpoint policy pending | `matchSubject`, `matchObject` | W6 uses two source-record references plus a separate canonical matched entity identifier; an ambiguous match does not create canonical identity equality. Both ends need one deliberate type policy. |

## Checks and counterexamples

- 11/11 declared native ends match G3d OWL domains/ranges; missing values remain explicitly unspecified.
- M016 and M031 match the two stated bounded W6 source fields.
- The OWL candidate explicitly places Organization, Facility, RegulatoryJurisdiction, MedicinalProduct, PharmaceuticalSubstance and MedicinalProductPresentation in an AllDisjointClasses set. Therefore imposing a global `MedicinalProduct` domain on `hasActiveSubstance` would make a future Presentation use infer incompatible Kind membership; likewise a global `Facility` domain on `locatedIn` would overcommit a legitimate non-Facility use. This is a **logical risk shown from the axioms**, not an executed reasoner countermodel.
- No ontology axiom, native stereotype or SHACL condition was changed in this step. Official schema, anti-pattern tool, reasoner, SHACL, SQL/RDF mapping regression and real data were **not run** for this packet.

The existing historical HORP relation records explicitly flagged these 11 unspecified ends for human review; this packet supplies sharper proposals and rejection conditions but does not silently close the human dispositions. It is unsafe to type all null associations as `formal`, or to label reversed `capacityBearer` as `characterization`, solely to decrease the unresolved count.

## Cumulative position and exact next step

G3-2a/b/c: **42/42 inventoried; 21/42 reviewed in depth** (three stereotype-only edits, seven relation-semantics proposals, eleven endpoint-policy proposals); 21/42 only first-pass triage. In the current native overlay, 38 binary associations are untyped and the previous `operates` material derivation remains to audit. All 42 still need a full final disposition, including multiplicity and scientific sign-off. G3-3 formal tool checking remains pending; 14 isolated named classes remain under the recorded connectivity metric.

**G3-2d:** work through the twenty remaining domain-semantic relations and `operates`, grouped by product structure, source/provenance, space, observations/shortage, and organization/capability. For each, identify truthmaker, allowed ends, cardinality, time and a rejection example; apply only justified native/OWL/SHACL deltas in a new candidate and run affected regressions. Then revisit the eighteen pending proposals with the author, run G3-3 official native semantic/anti-pattern tooling, perform G4 source/Wiki/Pages/article traceability, and assemble G5 stable human review and the comprehensive diagram. PR #305 stays draft, issue #306 open.
