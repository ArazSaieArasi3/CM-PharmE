# G3-2b — seven relation semantics review

Date: 2026-10-08 (Asia/Tehran). Based on G3-2a commit `fb281f2d605090da2779bb2021be7cb00de4de73`. This is a documented **design recommendation** for seven prior relations, not final author acceptance, a new ontology release, or an OntoUML anti-pattern pass.

## Results by dependency

| Relation(s) | Source-grounded recommendation | Why the stereotype remains open |
|---|---|---|
| `authorizationJurisdiction`, `listingJurisdiction`, `registrationJurisdiction` | Preserve legal-scope references to the `RegulatoryJurisdiction <<Kind>>`; do **not** mark them `mediation` solely because their source is a Relator | The three Relators already mediate two role-bearing participants each; direct mediation of the rigid jurisdiction would raise RelRig. A scope reference is not proof that the jurisdiction becomes relationally dependent on the authorization/listing/registration |
| `observationAboutProduct`, `observationAboutPresentation` | Preserve the two target identities and explicit information-aboutness; resolve `observationResultAbout` parent semantics before assigning a native stereotype | An information result is not the observation Event, a Product is not a Presentation, and a generic aboutness link does not automatically have a Relator truthmaker |
| `disruptionAffectsDependency` | Retain the bounded effect claim as an untyped child pending `disruptionAffects` semantics and causality evidence | Event → Relator is neither a mediation nor a demonstrated derived material relation; co-occurrence alone does not establish effect |
| `riskAssessmentConcernsDependency` | Retain an assessment-topic link pending `riskAssessmentConcerns` parent semantics | An assessment topic alone entails neither vulnerability, measured risk nor causal effect |

These proposals are in `decision-register.json` with exact endpoints, current multiplicities, source documents, a **synthetic explanatory positive example**, a rejecting counterexample and required evidence per relation. The examples are not ingested source rows or executed SHACL/SQL cases.

Historical W4 prose calls some jurisdiction links a "formal/context" relation. Under the [strict OntoUML Formal definition](https://ontouml.readthedocs.io/en/latest/relationships/formal/index.html), this does not itself establish a quality-comparison derivation. Hence this review does not automatically set `formal` either. The [Mediation definition](https://ontouml.readthedocs.io/en/latest/relationships/mediation/index.html), [RelRig catalogue](https://ontouml.readthedocs.io/en/latest/anti-patterns/RelRig/index.html) and [Material derivation](https://ontouml.readthedocs.io/en/latest/relationships/derivation/) motivate the bounded choices.

## Static checks actually executed

From the G3-2a native model and G3d OWL source: 7/7 native endpoint identities agree with corresponding OWL property domain/range; 4/4 child relations have the expected OWL `subPropertyOf` and native end-subsetting references; each of the three regulatory Relators already has two typed role-mediated participant relations. `static-checks.json` records the count. No model axiom or native stereotype changed in this step.

This is **static source comparison**, not a reasoner run, schema validation, official anti-pattern scan, SHACL run, mapping regression, causal test or empirical validation. The W4 evidence supports the distinctions and review questions; it does not supply complete cardinalities, all role lifecycles or real-source instances for these seven. Explicit human scientific disposition remains pending.

## Progress and exact next step

The G3-2a register inventories 42/42 old records. Three have a subtype-supported stereotype-only change; **seven more now have detailed semantic recommendations**, for 10/42 reviewed in depth. The other 32 have only first-pass triage. All 42 still require full disposition before G3 closes; 38 native relations remain untyped and the prior `operates` material derivation still needs audit. Fourteen named classes remain isolated under the defined metric.

**G3-2c:** resolve the eleven broad/untyped-end relations next. For each, fix exact endpoint identity and the source assertion that licenses it, or record a bounded deferral; then apply justified native/OWL/SHACL changes and rerun the affected cases. Subsequently handle the twenty domain-semantic relations and the one prior material relation. Revisit the seven recommendations here for author disposition and evidence-backed cardinalities; proceed to G3-3 official native semantic/anti-pattern tooling, G4 cross-source/publication traceability and G5 stable review/diagram gate. Keep PR #305 draft and issue #306 open.
