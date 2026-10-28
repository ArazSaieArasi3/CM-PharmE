# 2.1.0 GA readiness inventory — 0.1.0

**Disposition: HOLD pending the original GA gates.** Experimental
[2.1.0-rc.1 is published](https://github.com/ArazSaieArasi3/CM-PharmE/releases/tag/2.1.0-rc.1).
This source-backed audit completes only #327's inventory/decision-packet scope.
It does not record a new scientific acceptance, modify the published RC or close
an original GA issue. Source checkpoint: `c60e83166b1f15537572c03b0e36c37f780fedef`,
2026-10-28 Asia/Tehran.

There were **29 original open issues** at the start of this audit. The seven
operational groups below reorganize the existing [GA criteria](../../0.1.0/README.md).
Epics overlap; issue counts are not a release threshold. Each group can require
multiple small executions and real reviews. No fixed number of runs, date or
percentage of readiness is asserted. [gates.json](gates.json) pins source-file
hashes and metrics; [issue-map.csv](issue-map.csv) accounts for every original
open issue and distinguishes direct obligations, roll-ups and broader work.

| Gate | Current evidence / remaining gap | Exit before GA |
|---|---|---|
| GA-01 — source policies (#315) | Four bounded implementations and technical integration verified; scientific dispositions **0/4** | Explicit governing interpretation, applicability and author/scientific disposition for RelComp, WholeOver, RelRig and HomoFunc; preserve disagreements |
| GA-02 — native/full-candidate validation (#310/#306) | 536 elements/172 Properties; 76 unknown readOnly, 60 unknown cardinality, 11 untyped and 14 specialized Properties; no full-candidate 20-family run | Semantics-preserving inputs and ID crosswalk, supported/unsupported coverage per family, exact-candidate results and occurrence dispositions, affected regression |
| GA-03 — ORSD (#306) | 83 contracts specified; author acceptance **0/83**; 44 functional contracts still specified without execution and 12 quality protocols await their required evidence/review | Approved content and evidence/disposition for each in-scope contract; execution and author acceptance remain distinct |
| GA-04 — four domain modules (#311–#314) | RM/PV/BA/DS prototypes, scenarios and documentary evidence exist; detailed identity/relation/cardinality and integrated semantic acceptance pending | Each module meets its scoped requirements/CQs/scenarios and justified native/OWL/SHACL alignment, with recorded review |
| GA-05 — real source/mapping (#306) | M1–M4 copied-database slices verified; real operation/capacity source witnesses and wider mapping acceptance remain | Source-qualified identity/time/provenance, required mapping checks and scope-bound scientific acceptance; preserve synthetic/documentary/unknown distinctions |
| GA-06 — human, expert and task evidence (#98/#159/#173/#170) | Real author findings/E9 evidence still pending; historical review baseline is 87 concepts/52 object properties | Align target version, complete actual author review/findings, real eligible expert collection/analysis and representative demonstrator tasks |
| GA-07 — research/docs and final assembly (#171/#23 and related docs; PR #305) | RC packaging/replay is complete; final candidate diagrams, manuscript/claim mapping and reviewed GA commit remain | Reconcile actual final model/results/claims, versioned documentation and research artifacts; final tested archive/tag and publication after original gates close |

The native inventories overlap and are not detector findings. Optional source
metadata must not be filled by guesswork. #310 permits explicitly documented
per-pattern unsupported coverage; this report does not invent universal support
or a zero-defect requirement. Existing four-domain acceptance criteria remain in
force even though optional expansion was excluded from the experimental RC cut.

## What is already reusable

RC-01 scope, RC-02 deterministic archive/current citation/notices and clean bounded
replay, and RC-03 actual publication with downloaded-byte verification are complete.
The tag still identifies assembly `76c547f`; curated source `64edf15`, scope
`a0a9a53` and builder `f58a935` remain distinct. Stable-main merge and final GA
approval remain under their original criteria. Future model changes need their
own validation and eventual GA assembly; the published RC is retained unchanged.

ORSD ledger accounting is **3 fresh bounded + 1 earlier fresh query/countermodel +
23 bounded prior replays + 44 specified/not-executed + 12 quality protocols = 83**.
All 83 semantic-review statuses remain pending. These categories are evidence
provenance, not a pass percentage for the current candidate.

The human-review control center already has 87 concept passports and 52 relation
records. Its declared candidate is `RC-V2-HORP-01` / 2.0.0-alpha.1. The current
native has 138 non-datatype Class records plus six datatype Class records. Review
projection readiness for the older baseline is not transferred to the newer
candidate. The current E9 evidence register says collection is pending; public
participant/response templates have zero data rows. That template count makes no
claim about unknown private data. E9 targets 6–12 completed expert reviews across
pharmaceutical-domain and ontology/modeling strata under its governed protocol.
Before contact, check/record the institutional ethics requirement specified by
that protocol. This audit does not authorize recruitment or participant messages.

## Next bounded execution and useful parallel lanes

**This execution prepared the [RelComp scientific decision card](relcomp-review.md).**
It reconnects the existing runtime evidence to the actual source text and example,
with two concrete author judgments. Scientific acceptance remains pending. The
fresh catalogue bytes exactly match the original pinned HTML; the optional
BugTracker example/signature tension is now recorded explicitly. No original
oracle or engine result was changed, and no fresh detector run is claimed.

[The next-action table](next-steps.csv) separates:

- **Author/scientific lane:** one RelComp disposition, then one remaining policy
  at a time; ORSD/module decisions and actual findings remain separate.
- **Assistant lane:** one unresolved association audit/justified delta, one ORSD
  contract such as FR-04, or one source-qualified witness at a time. Independent
  audits can proceed while scientific decisions are pending; full claims wait
  for their actual dependencies.
- **Expert lane:** first reconcile target version and clearance status, then real
  authorized collection/analysis. Version alignment can be prepared now; no
  automated or synthetic response substitutes for the required real evidence.
- **Final assembly:** after verified original gate closure, reconcile final
  diagrams/docs/research claims, review integration and publish the tested GA.

Minimum truthful/versioned documentation and manuscript-to-evidence mapping
remain required. Broader full-Wiki redesign, scoring/excellence and cross-repo
profile extraction keep their original scope; this inventory does not turn every
open backlog issue into a new blanket GA prerequisite. No existing issue was
cancelled, waived or declared complete by this audit.

## Later incremental-release proposal

The [2026-10-28 incremental roadmap](../../../roadmap/0.1.0/README.md) responds
to Araz's subsequent request to make smaller stable releases through 2.2/3.0 and
retain unfinished research in later increments. It is a proposal awaiting an
explicit scope decision; it does not change this audit's seven original groups
or historical evidence. The first RelComp disposition remains #329, followed by
the exact supported-core inventory #330. Do not infer new scientific approval
from approval of the planning direction.
