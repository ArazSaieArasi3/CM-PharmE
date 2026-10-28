# Experimental 2.1.0-rc.1 contents and claim freeze

RC-01 scope **CMPE-RC-Scope/0.1.0**; issue #324. This is a complete source/claim
specification, not an archive, publication, tag or GA approval.

Payload source: `64edf150db8a78579928fd99b5a381f665c1afdf`, the verified
EvidenceRecord checkpoint. The [contract](scope-contract.json), [source manifest](payload-manifest.json),
[artifact roles](artifacts.json), [claim envelope](claims.json), [known limits](known-limits.json)
and [scope decisions](decision.md) were frozen before verifier implementation at
`c3f8f3ee4c4dbe3ee43827a9ae18d104bce57ff2`.

The exact payload contains **1,975 tracked files / 27,097,299 bytes** under
`source/`. Thirteen review groups select **155 files** for the artifact index;
all other files are archival source for reproducibility, not newly endorsed RC
assets. [artifact-index.csv](artifact-index.csv) names actual versions, roles,
primary paths and claim limits. File mode, Git blob identity, SHA-256 and byte
length are recorded for every source file. A clean separate checkout of the exact
payload revision is required; the checker never reads a moving working tree as
if it were the frozen source.

The latest native candidate is EvidenceRecord/0.1.0. ContextClass is a predecessor;
the source-policy dossiers, copied-W6 slices, ORSD 0.2.0 and GA register retain
their own versions and inputs. The newest native model is not certified as a
complete translation of experimental OWL or historical W6. The original witness
comparison remains 88/89; prospective admission is 89/89 under one declared
transition. Native inventories remain 76 unknown readOnly, 60 unknown cardinalities,
11 untyped and 14 specialized Properties; these are overlapping input inventories,
not detector findings. Source-policy scientific acceptance remains 0/4 and ORSD
author-accepted rows 0/83.

The historical source root citation says 1.0.0 and must not be reused as RC
citation metadata. No new blanket license grant is asserted; existing notices and
license availability must be retained and stated truthfully in RC-02 metadata.
The complete source snapshot preserves those historical files without silently
renaming or rewriting them.

```sh
python v2/release/2.1/rc.1/scope/verify_scope.py \
  --source-root /path/to/clean/64edf15-checkout
```

The checker validates every pinned source blob, group/index/version membership,
actual committed evidence and inventory, pending claims and source-CI provenance.
Nine controls reject missing/tampered assets, hidden unknowns/transition, unsupported
full-validation/scientific/native-OWL/GA claims and mislabeled root citation.
Local verification passed: all 1,975 source files and 13 review groups match;
all nine negative controls were refused. See [local-results.json](local-results.json).
Hosted verification also passed and exactly equals the local report: see
[hosted-results.json](hosted-results.json), [CI/artifact provenance](ci-evidence.json)
and [run 40684844072](https://github.com/ArazSaieArasi3/CM-PharmE/actions/runs/40684844072).
Freeze c3f8f3e precedes implementation 06c132f. All 24 distinct implementation
workflows passed within their individual declared scopes; their pinned runs are
in ci-evidence.json. RC-01 is complete in this scope.

RC-02 must still build the archive, generate current release metadata/checksums
and demonstrate a bounded clean replay. RC-03 must still confirm tag/asset/source
agreement and actual prerelease publication through a supported write route or
maintainer action. No merge of draft PR #305, tag or release occurs here. The
[finite route](../../0.2.0/README.md) and original GA gates stay in force.
