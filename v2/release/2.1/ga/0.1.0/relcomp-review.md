# RelComp scientific decision card — prepared, not accepted

Parent #315; bounded packet #327. Named candidate profile:
**CMPE-RelComp-PositiveLowerBound/1.0.0**. Its implementation already passed
14 fixed cases, three historical replays and eight refusal controls. This packet
requests no new engine run and changes no frozen file. Scientific acceptance is
still **0/4** across the four-rule program.

## Two judgments to record

| ID | Concrete author/scientific judgment | Recommended bounded treatment |
|---|---|---|
| RC-A01 | Is a positive lower bound the governing condition for this explicitly named profile, with optional-plural source examples/engine matches retained as review items? | Retain the published textual condition as the named profile's policy; state the example tension and avoid universal/source-intent claims. |
| RC-A02 | Is the selected shared outer end explicitly assigned ATarget for an admitted declared frame, while retaining original end IDs/order and bounds? | Adopt only the explicit frame-role assignment. Original archive occurrence orientation/refactoring and full-model search remain outside this acceptance. |

The recorded response needs **ACCEPT / REVISE / DEFER**, reviewer identity/role,
rationale and evidence, plus any remaining limits. A generic instruction to
continue, CI success or this recommendation is not an author response. A revision
requires a new named profile and independent expectations; old results remain.

## Current primary-source check

[Official catalogue](https://ontouml.readthedocs.io/en/latest/anti-patterns/RelComp/index.html)
constraints describe a positive minimum and plural maximum at ATarget, while the
structural clauses mention both ATarget and ASource variants. The original
[decision](../../../../ontology/candidates/2.1.0-alpha.1-relcomp-policy/decision.md)
therefore explicitly labels role normalization as interpretation.

The [published examples image](https://ontouml.readthedocs.io/en/latest/_images/examples12.png)
shows the first BugTracker/Feature shared Feature end as **0..***, with an inner
Feature dependency; the University/Department example uses **1..*** at Department.
**Inference:** under the explicitly bound shared-end reading, the first example
falls outside the positive-lower profile. This visible example/signature tension
needs a disposition; it does not establish which diagram/text or historical
intention is wrong. It is not evidence of a recent documentation change: the
fresh HTML is byte-identical to the original pinned catalogue snapshot.

[relcomp-review.json](relcomp-review.json) records fresh HTML/image SHA-256 and
separates direct source readings from this inference. The thesis Table 44/page
reference is inherited from the unchanged original sources.json. The current PDF
web retrieval failed, so a fresh thesis/table re-review is not claimed. Neither
the PDF nor the source image is redistributed in this packet.

## Existing boundary evidence — unchanged

| Existing case | Shared bound | Raw archived count | Named profile match | Existing disposition |
|---|---|---:|---:|---|
| unlimited-zero | 0..* | 1 | 0 | ENGINE_ONLY_REVIEW_REQUIRED |
| unlimited-one | 1..* | 1 | 1 | Source-profile and archive channels both retained |
| finite-zero-2 | 0..2 | 1 | 0 | ENGINE_ONLY_REVIEW_REQUIRED |

These rows come from the existing [complete hosted report](../../../../ontology/candidates/2.1.0-alpha.1-relcomp-policy/hosted-results.json).
They are synthetic declared frames; the source diagram was not converted or run.
A profile non-match does not certify domain correctness. Explicit lower/upper
bounds, typed ends, acyclic ancestry and the documented supported frame scope
remain required; uncertain/unsupported input is refused. Scientific acceptance of
this bounded profile would not execute the current model, close #310/#306,
certify all 20 families or provide independent expert evidence.
