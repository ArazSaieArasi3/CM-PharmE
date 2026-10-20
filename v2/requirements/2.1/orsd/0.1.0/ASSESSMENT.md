# ORSD 0.1.0 assessment against the 2.1 candidate

Date: 20 October 2026. Pinned model/evidence commit: `09d60136a990d6602438be4085a4d407c9bd5c68`.

## Result

The first independent ORSD has all seven sections of the 2009 methodological template. It is ready for author and domain review, not for declaring complete semantic coverage or release readiness.

| Result | Count | Meaning |
|---|---:|---|
| Tracked requirements | 83 | 71 functional rows and 12 quality requirements; semantic overlaps remain explicit |
| Native vocabulary contains all listed anchors | 49 | Identifier availability only; no claim of complete constraint or query coverage |
| Anchors found only in experimental signatures | 21 | Experimental support remains separate from accepted native implementation |
| Mapping requiring reconciliation | 1 | R-BA-02 and capabilityRealizedIn |
| Quality requirements requiring a separate assessment | 12 | Cannot be evaluated through class presence |
| Newly executed structural/metadata checks | 12/12 | IDs, metadata, source hashes, counting and retained inventories |
| Newly replayed module SELECT queries | 23/23 | Frozen historical fixtures; not new independent empirical data |
| New SHACL or HermiT execution in this work | 0 | Historical results are cited with their scope and date |
| Newly granted semantic approvals | 0 | User direction approval is preserved but not expanded |

## Concrete traceability finding

R-BA-02 cites `capabilityRealizedIn`. The native/portable-signature audit did not find that exact term. The BA package exports `capabilityRealizedInLogistics`, while an existing CQ uses the old term in `FILTER NOT EXISTS`. A passing answer on a fixture therefore does not establish the intended non-entailment for the revised realization path. This is a **mapping/oracle review finding**, not proof that the entire repository lacks capability semantics.

Resolve the governing realization relation, retain a capability with no execution as a countermodel, and add an executed-capability witness using the selected relation. Register the decision before closing this requirement.

## Prioritized improvements

1. **P0 — Establish the semantic denominator.** Review new general requirements against scoped R/B2 rows; mark parent, specialization, overlap, merge or deferral. Do not call 83 rows 83 independent domain needs.
2. **P0 — Reconcile native and experimental semantics.** Resolve identity, relation stereotypes, unknown ends/bounds, Event/Situation treatment, specialization and the detector/source disagreements under issues 306, 310 and 315.
3. **P0 — Correct R-BA-02 mapping and oracle.** Decide whether old and revised realization relations are aliases, subproperties or distinct relations. Test both presence and absence under the accepted semantics.
4. **P1 — Create independent CQ contracts for accepted Must requirements.** The 71 textual questions are review specifications. Existing executable CQs and their frozen fixtures remain separate; their success does not automatically validate the new requirements.
5. **P1 — Strengthen operational evidence.** Obtain supported treatment execution/effectiveness, actual work orders and commitment identity, deployment/component-version/operator evidence, and regulatory subject records. Preserve unknowns rather than generating factual-looking completions.
6. **P1 — Perform prospective expert review.** Record reviewer, scope, decision and rationale. Do not infer approval from query or reasoner success.
7. **P1 — Reassess held-out claims.** Keep the 97 discovery and 51 held-out source rows separate. Any later use of a former held-out source to redesign a version must be disclosed before claiming independence for that version.
8. **P2 — Synchronize publication artifacts.** After acceptance, refresh Word/PDF, the full diagram, Wiki and Pages; correct the earlier Information header to the recorded BioMedInformatics target.

## Exact next step

Review the purpose/scope and requirement dispositions in this document, beginning with overlaps and the R-BA-02 finding. Then prepare ORSD 0.2.0 with accepted priorities and a finite list of executable CQ contracts. The full ontology detector, CI and human review remain separate open gates.

## Method reference

M. C. Suarez-Figueroa, A. Gomez-Perez and B. Villazon-Terrazas, *How to Write and Use the Ontology Requirements Specification Document*, OTM 2009, LNCS 5871, pp. 966–982. DOI: 10.1007/978-3-642-05151-7_16. https://oa.upm.es/5474/
