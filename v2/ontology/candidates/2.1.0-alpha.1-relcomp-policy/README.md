# RelComp lower-bound source policy — P5e-1

Named profile: **CMPE-RelComp-PositiveLowerBound/1.0.0**. This is a separate
declared-frame predicate and comparison report. It is not the official archived
detector, an automatic refactoring tool or a full-model validator.

[decision.md](decision.md) records RC-D01–06. [sources.json](sources.json) pins the
governing thesis table, current catalogue snapshot, archived source and historical
inputs. The source interpretation and 14 independent boundary oracles were frozen
at commit `e3d0aa0949738c2c6f19431d56d75a564eb53a2b`, before implementation.

## Two result channels

The unchanged archived RelComp Java class runs on every accepted fixture. Its raw
occurrence count is preserved. An independent Python predicate checks the bound
composition frame against the separately named source profile. The report never
rewrites one result into the other.

For optional plural ends, the archived engine can report an occurrence while the
positive-lower-bound signature does not match. Such records remain
`ENGINE_ONLY_REVIEW_REQUIRED`. Neither a source-profile match nor a non-match
settles whether the domain model is correct.

The selected shared outer end is explicitly bound to ATarget for this profile;
this role normalization is documented as an interpretation in decision.md.
Reordering the serialized ends does not change their original IDs, types or
cardinalities. The runtime comparison concerns counts only; it does not validate
the archive's occurrence orientation or generated refactoring plans.

## Bounded verification

- Fourteen synthetic frames cover lower bounds 0/1/2, upper bounds 0/1/2/unlimited,
  an unrelated inner type, transitive ancestry, plurality at the nonshared end,
  and preserved role binding after end-list reordering.
- Every fixture's class/association/end/type/cardinality/generalization fields
  are independently compared with the actual official legacy parser output.
- The archived detector and independent profile must both match their own frozen
  expectations. Differences remain explicit review items.
- Three historical RelComp fixtures are replayed with identical file digests,
  parsed fields and original engine counts. Old results are not edited.
- Eight malformed/unsupported variants are refused before policy evaluation:
  missing bounds, negative lower, inverted interval, untyped end, duplicate ID,
  cyclic ancestry and unsupported subsetting.
- The archive commit, tracked source cleanliness, both RelComp Java digests,
  compiler digest, ordered dependency JAR digests and historical input hashes are
  checked or recorded. No archived Java file is patched.

## Reproduce

Use Python 3.12, Java 17, the archived repository at the exact commit in sources.json
and ECJ 3.39.0 with its recorded SHA-256.

```sh
python v2/ontology/candidates/2.1.0-alpha.1-relcomp-policy/run_policy.py \
  --archive /path/to/pinned/oled --ecj /path/to/ecj-3.39.0.jar
```

The checker verifies the compiler bytes before execution. The reproducible hosted
workflow is `.github/workflows/v2-21-relcomp-policy.yml`. Sources.json records the
reviewed PDF digest and exact table/page, but the full thesis, rendered page and
catalogue are not redistributed. Test replay is offline with respect to those
documents; it does not claim a fresh source download during every CI run.

## Applicability and remaining gates

Input scope is one explicitly bound frame in a two-association legacy witness
model, using Kind/SubKind classes, explicit endpoints/bounds and acyclic ancestry.
This narrow parser intentionally refuses unsupported constructs. No automatic
modern JSON conversion, Event/Situation coercion, nature/subsetting removal or
unknown cardinality filling occurs.

This slice addresses the positive-lower-bound source discrepancy only. It does not
settle every source-orientation interpretation, implement a whole-model search,
run the full CM-PharmE candidate, validate other detector families, or constitute
author/expert approval. WholeOver, RelRig, HomoFunc and the final applicability
integration remain open under #315; native adapter fidelity remains #310.
Scientific and release gates remain #306. PR #305 stays draft.

## Verified outcome

[Hosted run 40460902265](https://github.com/ArazSaieArasi3/CM-PharmE/actions/runs/40460902265) passes on implementation commit `9ecefa656651c5a5801ba42af5b227d6a6c17a9b`. [hosted-results.json](hosted-results.json) records all 14/14 independent cases, 3/3 historical replays and 8/8 refusal guards. [ci-evidence.json](ci-evidence.json) pins the successful run/artifact and all 18 successful distinct workflow families. [local-results.json](local-results.json) is the separate local runtime report.

Three new engine-only review states remain visible: finite-zero-2, unlimited-zero and reordered-zero. Old expected/actual counts and archive bytes are unchanged. [traceability.csv](traceability.csv) connects source, decision, predicate, fixtures, runtime and open gates. [applicability.json](applicability.json) identifies the exact P3/M1–M4 target snapshot and why it was not executed. Its 66 unknown-cardinality properties, 11 untyped properties and 14 specialized properties are overlapping source inventories, not RelComp findings.

[adjudication-register.csv](adjudication-register.csv) preserves the four-rule scope: the RelComp lower-bound slice is verified; WholeOver, RelRig and HomoFunc remain open, as does final integration. #315 remains open. The next finite task is P5e-2 WholeOver. No author/scientific or full-candidate approval follows from this technical completion.
