# Comprehensive 2.2 prerequisites — full V2 reconciliation

Date: 2026-10-30, Asia/Tehran. Packet: [#343](https://github.com/ArazSaieArasi3/CM-PharmE/issues/343).

Araz explicitly defines 2.2 as the coherent, complete continuation of valid V2
content. The four authorized objectives are preservation/integration, justified
semantic connections, disposition of model/requirement/mapping/evaluation gaps,
and documentation/diagrams of that same complete model. The new
[release contract](release-contract.json) and [roadmap](../../../roadmap/0.13.0/README.md)
supersede the narrow future-capability objective in roadmap0.12.0. This is scope
authorization, not acceptance of every experimental semantic proposal.

## What the earlier connectivity result actually established

The author's recollection has a factual basis. A prior coherence experiment
really did reach one component and zero isolated named classes. Its own record
explicitly retained pending semantic acceptance and integration. It was not
promoted into the later native candidate or the released M1 profile.

This audit replays both native files with **the same metric**: an undirected
graph over named non-datatype classes, using explicit generalizations and binary
relations only when both endpoints name such classes. It excludes anonymous or
unknown targets, data values and inferred closures. It cannot certify semantic
coherence or domain completeness.

| Pinned artifact | Named classes | Components | Isolates | Actual scope |
|---|---:|---:|---:|---|
| Latest bounded EvidenceRecord/ContextClass native candidate | 138 | 14 | 13 | Later native decisions; full-model review still open |
| Earlier coherence experiment | 141 | 1 | 0 | Separate provisional additions; semantic acceptance pending |
| Released 2.1.0 M1 TBox | 4 CM-PharmE classes | Not compared | Not compared | 50 triples; scoped provenance support only |

The older G3-E report's 14 isolates used an earlier candidate before the typed
SupplyCapacity change. The 13-isolate latest result is freshly computed; it is
not an unexplained rewrite of that historical report. The initial W4 diagram's
8 isolates used an 81-class overview and is a different projection again.

## Reconciliation findings

- All **87 Gate-D concept IDs** are accounted for: 84 remain in the latest
  native file, while AssetAtRisk, Vulnerability and ClinicalCareParticipant have
  recorded S-04/S-05 deferrals and preserved declarations outside active import.
  Name retention does not prove preservation of meaning. Reassess these prior
  deferrals against the comprehensive 2.2 objective; do not silently treat them
  as either removed forever or automatically reinstated.
- The native candidate has 144 Class records including six datatypes. Its
  historical ownership inventory covers 17 domains, 16 with active concepts,
  with 60 provisional primary-domain allocations. Clinical Care has no active
  concept. These are ownership counts, not completeness scores.
- The experiment has **49 additional relations, three classes and 98 relation
  ends**. It also differs in **22 fields on shared non-package elements**.
  Replacing the later candidate with that old file would revert FacilityOperation,
  ContextClass and EvidenceRecord decisions. Each difference is enumerated in
  [branch-divergence.json](branch-divergence.json).
- Current native unknown inventories are 11 endpoint types, 60 cardinalities,
  76 readOnly values and 43 unclassified relation stereotypes. These overlapping
  counts are not a count of independent defects; nulls are not defaults.
- The baseline formal modules have 81 declared classes, 52 object properties
  and five datatype properties. All 52 object-property names exist in the native
  relation inventory. Three baseline class declarations are absent from the
  active formal base/native candidate under the recorded deferrals. Each of
  the **138 formal declarations** has its own name-presence crosswalk; names
  alone establish neither equivalent constraints nor successful migration.
- All **83 ORSD IDs** remain accounted for. Their historical ledger still marks
  semantic acceptance pending; 44 contracts are specified but not executed in
  that ledger, with other bounded/review states reported separately. Later
  scoped M1–M4 successes must be reconciled rather than ignored or counted as
  blanket ORSD acceptance.
- Existing mapping/evaluation inventories retain 36 ontology/RDB rows, 39 source
  field mappings across six source contracts, 97 E7 semantic rows (nine recorded
  as not represented, 14 partial), and 32 claim/evidence rows. This packet does
  not reexecute those historical evaluations on a comprehensive 2.2 assembly.

The public V2 reference still uses its pinned evolving V2 formal source; the
public 2.1.0 reference uses the exact released M1 TBox. Neither is documentation
of the separate provisional full native/coherence union. The captured
[source snapshot](source-snapshot.json) records that distinction, including the
last verified public baselines. No new public semantic documentation is
deployed by this audit.

## Evidence and reproduction

[report.json](report.json) contains fresh counts and limits.
[gate-d-preservation.csv](gate-d-preservation.csv),
[baseline-formal-terms.csv](baseline-formal-terms.csv),
[domain-inventory.csv](domain-inventory.csv) and
[requirement-inventory.csv](requirement-inventory.csv) expose individual rows.
[gap-register.csv](gap-register.csv) routes remaining work to existing owners.
[input-pins.json](input-pins.json) pins 52 source files by SHA-256 and Git blob
identity at candidate commit2ee5c8b86740349fc74427d29eb77f3e5951000c.
The captured public registry is independently checked against its main Git blob.

Install rdflib==7.5.0 and run from the repository root:

```bash
python v2/release/2.2/preparation/0.1.0/audit.py \
  --output build/comprehensive-22-preparation --check-committed
```

A passing audit proves reproducibility and accounting within its explicit
scope. `comprehensive_2_2_ready` remains **false**. Model files, old reports,
published releases, oracle history and actual scientific acceptance are
unchanged. [Hosted CI receipt](ci-evidence.json) records direct-push and PR-merge execution
identities. Both downloaded artifact ZIP digests verify and all six audit outputs
match local bytes exactly. [Local controls](local-verification.json) also verify
two Python hash seeds, refusal of changed input, and restoration of source bytes.

## Next bounded execution

[#344](https://github.com/ArazSaieArasi3/CM-PharmE/issues/344) defines one governed
assembly manifest and field/element reconciliation across the two lineages.
Keep the latest native decisions, retain all experimental proposals separately,
and identify each remaining semantic decision. Then execute one relation or
requirement packet at a time. #342 RelRig is a dependent validation subtask,
not the definition of the 2.2 release. No larger version number is needed merely
to pursue this integration goal; a genuinely incompatible change would require
its own documented version decision.
