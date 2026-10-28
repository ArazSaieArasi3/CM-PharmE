# Prepared experimental RC bundle — 0.1.0

Issue #325, after #324 scope freeze. Profile **CMPE-RC-Bundle/0.1.0**.
[Layout, replay and refusal contract](bundle-contract.json), [decisions](decision.md),
[release metadata](metadata/) and [Python version lock](requirements.lock) were
frozen at `56e5138a25866c9b23b3d966549ee9a41c1d4653` before implementation.
Contract SHA-256 `af43da6949e0db60438682d9ed362cd9a25dff327756e09663754bca96c36ff1`.

The prepared `cm-pharme-2.1.0-rc.1.tar` contains **2,001 regular files**: all
1,975 payload source files from 64edf150db8a78579928fd99b5a381f665c1afdf, 13 scope
files from a0a9a539c3891476847b52fed4c65d9ccae8d485, and 13 current metadata,
provenance, checksum and packaging files. There are no installed dependencies or
Git history in it. Thirteen review groups / 155 selected files keep their separate
versions. Historical citation 1.0.0 and the source's original 17-row GA register
remain unchanged; root citation identifies experimental 2.1.0-rc.1. Existing
notices are retained without inventing a root blanket license.

The builder verifies exact source/scope sets, creates two byte-identical tar
archives with fixed metadata, writes per-file and archive SHA-256, and reads the
archive back through the safe verifier. Uncompressed tar removes compressor
version differences. Ten frozen controls refuse missing/tampered or extra files,
unsafe paths, links, duplicates, historical citation promoted to RC, suppressed
witness transition, GA claim and a corrupt checksum inventory.

The replay uses a new extraction and newly installed isolated Python/npm
runtimes with Python 3.12, Node 24 and Java 17. It reruns the full bounded
EvidenceRecord script and requires **complete report equality**, including native
schema/guarded serialization, 12 new/12 ContextClass SHACL rows, 89 historical and
prospective rows, 10 identity cases, 6 HermiT rows and scoped native/refusal cases.
Original-after remains 88/89; prospective-after remains 89/89 under one transition.
It also reruns the four-policy **dossier integrity/integration audit**, requiring
complete report equality, and rechecks all extracted source/scope bytes. The four
policy detector engines and copied-W6 databases are not reexecuted. Their prior
scoped evidence remains indexed separately.

```sh
python v2/release/2.1/rc.1/bundle/build_bundle.py \
  --source-root /path/to/exact/64edf15-source \
  --scope-root v2/release/2.1/rc.1/scope --output-dir /path/to/new-build
python v2/release/2.1/rc.1/bundle/replay_bundle.py \
  --archive /path/to/new-build/cm-pharme-2.1.0-rc.1.tar \
  --sha256-file /path/to/new-build/cm-pharme-2.1.0-rc.1.tar.sha256 \
  --work-root /path/to/new-empty-work --output /path/to/replay-results.json
```

Local and hosted verification passed with **exactly equal complete portable
build and replay reports**: [build local](build-local-results.json),
[build hosted](build-hosted-results.json), [replay local](replay-local-results.json),
[replay hosted](replay-hosted-results.json), [CI/asset provenance](ci-evidence.json).
All **25 distinct implementation workflows** passed within their individual scopes.
The archive is **30,945,280 bytes**, SHA-256
`21f140abb6ccde5eebb9302cd87724ce8616a2f71a046b22bf3c3c5ea01b10ba`;
[committed sidecar](cm-pharme-2.1.0-rc.1.tar.sha256). A local rebuild using only
the extracted source/scope/packaging files produced the same archive bytes,
without Git history or an environment-variable bytecode workaround.

[Download the prepared bundle and evidence](https://github.com/ArazSaieArasi3/CM-PharmE/actions/runs/40690186882/artifacts/12816851256)
from [run 40690186882](https://github.com/ArazSaieArasi3/CM-PharmE/actions/runs/40690186882)
at implementation f58a935f5c8455cce7df1338d0d380cb6d7a0a3b. The workflow artifact
ZIP digest is distinct from the contained tar hash; both are recorded separately.
This completes RC-02 in its bounded scope; **RC-03 is next**. The hosted
workflow uploads the archive, sidecar hash, exact reports and logs with 90-day
retention; committed code and pinned input snapshots support reconstruction after
artifact expiry. Runtime versions are separate from portable deterministic
results. External dependency downloads are required; no offline runtime or
Python wheel-hash pinning is claimed.

No complete native-to-OWL translation, full-model 20-family execution, empirical
capacity validation, independent scientific/author/expert acceptance, production
migration, GA approval, tag or release is implied. #306/#310/#315 remain open;
#305 remains draft. RC-03 must verify exact tag/asset/source agreement and actual
experimental prerelease publication through an available route or maintainer.
