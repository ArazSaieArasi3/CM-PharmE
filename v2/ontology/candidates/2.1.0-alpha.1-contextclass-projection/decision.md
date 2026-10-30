# ContextClass projection decision — issue #322

Profile **CMPE-ContextClassProjection/0.1.0**, delegated scoped candidate decision.
The two relationships are typed views over existing primitive mediations. This
adopts only the ContextClass portion of the earlier C proposal; evidenceRecord
and the earlier 88/89 contract-transition observation stay unchanged.

| ID | Decision | Rationale and limit |
|---|---|---|
| CC-D01 | Use derived unstereotyped native Associations, retaining their IDs and subsetting references. | They project eligible existing links, rather than introducing two new mandatory primitive mediations. The selected native schema supports this representation; scientific relation-category acceptance remains pending. |
| CC-D02 | Entry target 1; product target 0..1; both inverse bounds 0..*. | A contextual assignment has an applied entry but may classify a substance instead of a product. A generic classified entity/entry need not participate in a contextual assignment. These are explicit candidate design choices, not empirical cardinalities inferred from data. |
| CC-D03 | Primitive classificationEntity/classificationEntry target readOnly=true. | Candidate assignment identity includes the same classified individual and entry over observed time. A different established participant requires a different assignment identity; missing data, different IRIs or shared external codes alone do not establish replacement. This is a model identity policy, not a source record-ID rule. |
| CC-D04 | Derived target readOnly=true and inverse readOnly=false. | The projected participant is stable under the declared primitive identity policy; incoming assignments may vary. The four formerly null flags are deliberately specified rather than defaulted. |
| CC-D05 | Derive only from an existing primitive edge plus explicit eligible named types/subtypes. | No Product-to-Role inference, no fabricated primitive edge, no evidenceRecord derivation, no acceptance of a stale shortcut. OWL restrictions alone do not implement exact typed projection or temporal immutability. |
| CC-D06 | Produce a separate full native review candidate with exactly 14 permitted field changes. | Preserve every other field/element, modern nature, the four specialization references and all historical packages. Do not rewrite the pinned P3 or four-rule integration baseline. |
| CC-D07 | Complete only the bounded implementation acceptance contract. | Native schema, bounded subsetting, SHACL, HermiT and finite temporal checks are separate evidence. No independent scientific acceptance, complete modern validator/20-detector execution, production migration or final release. |

Basis: existing Contextual Medicine Classification Assignment passport C060;
ORSD 0.2.0 evidence anchors P5-R01/P6-R01/P6-R02; earlier A/B/C comparison and
its preserved product/substance counterexamples. The official mediation catalogue
(https://ontouml.readthedocs.io/en/latest/relationships/mediation/index.html)
describes existential dependence and distinct relata, but does not establish the
specific assignment-identity choice above. The earlier paper rationale at
https://www.inf.ufes.br/~gguizzardi/SLE2012-CR.pdf is retained as prior lineage;
fresh retrieval timed out in this run and no fresh paper inspection is claimed.

Completion contract: 12 independently frozen projection/SHACL cases, 89 historical
SHACL expectations before/after the two selected rules, 10 bounded identity traces,
4 OWL/HermiT cases, native schema/guarded serialization, four bounded subsetting
rows and six unauthorized-change refusals. Preserve the difference between closed-
world SHACL admission and open-world OWL consistency. Exact deltas and source
hashes are in contract.json; all expected outcomes precede implementation.
