# Source-policy adjudication dossier

Status: **PROPOSED; AUTHOR/SOURCE ADJUDICATION REQUIRED**. Tracking issue: [#315](https://github.com/ArazSaieArasi3/CM-PharmE/issues/315).

The archived source is pinned to `nemo-ufes/ontouml-lightweight-editor@42b926f6c2859dc87e49a96b8482eae28d02e7d5`. All 20 detector classes are unchanged. The catalogue pages were retrieved on 2026-10-09. No expected value was changed to hide a documentation disagreement.

| Rule | Documentation source | Pinned implementation location | Reproduced boundary |
|---|---|---|---|
| RelComp | [Catalogue](https://ontouml.readthedocs.io/en/latest/anti-patterns/RelComp/index.html), constraints | `relcomp/RelCompAntipattern.java`, `identify()` | Lower bound zero still yields one occurrence; documentation specifies positive lower bound. |
| WholeOver | [Catalogue](https://ontouml.readthedocs.io/en/latest/anti-patterns/WholeOver/index.html), description and formula | `wholeover/WholeOverOccurrence.java`, constructor | Sum of upper bounds equal to two yields zero; constructor invokes minimum sum three. |
| RelRig | [Catalogue](https://ontouml.readthedocs.io/en/latest/anti-patterns/RelRig/index.html), formal constraint | `relrig/RelRigAntipattern.java`, `buildPropertyHash()` | Literal catalogue formula uses mediated-end readOnly=true; code skips when relator-end readOnly=true. |

The two single-boundary witnesses, four-cell readOnly matrix and two-cell HomoFunc lower-bound mutation have explicit before-execution engine oracles. Documentation oracles are separately recorded. Across all eight boundary states, five observed outputs differ from the literal published condition. This is evidence of a source/version interpretation problem, not a final judgment that the archived code or the catalogue is wrong.

Recommended interim decision: retain the archived engine unchanged as a reproducibility reference; flag these rules for manual/source review in any validation report. Do not claim universal specification conformance from passing basic sensitivity fixtures. If a correction is later accepted, publish a separately named and versioned policy overlay with both positive and negative boundary witnesses. Preserve the original observations.

Next source work: adjudicate the intended temporal/existential semantics and record which source version governs CM-PharmE; the primary dissertation has now also been inspected as recorded below. The author must accept that interpretation before it closes a scientific gate. Native Event/Situation, modern nature, unknown endpoint types/bounds and the 14 real specialized ends remain independent blockers.


## Primary-source cross-check completed

[Sales, *Ontology Validation for Managers*, 2014](https://nemo.inf.ufes.br/wp-content/papercite-data/pdf/ontology_validation_for_managers_2014.pdf), Tables 44, 46 and 51 (printed pages 166, 174 and 196–197), repeats the catalogue conditions for RelComp, RelRig and WholeOver. Thus the disagreements are not explained merely by later web transcription. RelRig's surrounding discussion still requires semantic adjudication.

Table 38 (page 144) specifies a HomoFunc lower bound of at least two. A targeted two-cell mutation now confirms that the engine detects lower=1 and lower=2 alike. This fourth source-policy disagreement is also retained in #315. Basic 20-family coverage remains limited.

Recommendation: retain separate observed-engine and proposed source-based oracles; do not choose one silently or patch the official archive. Source consultation is complete for these tables; author acceptance and governing policy remain open.
