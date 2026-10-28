# Verify and replay the prepared bundle

Use Python 3.12 with venv/pip, Node.js 24 with npm and Java 17, plus network access
to the pinned Python/npm dependencies. No installed runtime, database service or
Git history is included. Python direct and transitive versions are pinned in
requirements.lock; npm package versions/integrities are locked by the unchanged
EvidenceRecord runtime/package-lock.json in source/. Wheel hashes and an offline
runtime are not claimed.

The archive is an uncompressed POSIX tar to avoid compressor-version differences.
Its bytes are deterministic: sorted regular files, fixed modes, zero timestamps,
zero uid/gid and empty owner/group names. Two independent builds must agree.
The adjacent .sha256 is for the archive; CONTENTS.sha256 covers all files except
itself. Obtain the expected archive hash from the pinned build evidence, not an
unverified download's own claim.

After obtaining and safely extracting the archive, run from its top directory:

```sh
python verify_bundle.py --archive /path/cm-pharme-2.1.0-rc.1.tar   --sha256-file /path/cm-pharme-2.1.0-rc.1.tar.sha256 --output /tmp/bundle-check.json
python replay_bundle.py --archive /path/cm-pharme-2.1.0-rc.1.tar   --sha256-file /path/cm-pharme-2.1.0-rc.1.tar.sha256   --work-root /path/to/new-empty-replay-directory --output /tmp/replay-check.json
```

The verifier checks safe regular paths, exact file sets, frozen source/scope and
current metadata, provenance, hashes and ten refusal controls. Replay verifies
before extraction, creates a fresh isolated Python environment and npm install,
and invokes scripts only from extracted source. It writes outputs outside source
and verifies the source again afterwards. Native, SHACL, temporal and HermiT
outcomes must equal the entire pinned EvidenceRecord report; the policy dossier
integration must equal its pinned report. Runtime details go in environment.json.
No pre-existing dependency directory is accepted as a replay input.

This reruns 12 EvidenceRecord and 12 ContextClass SHACL rows, all 89 historical/
prospective rows, 10 identity cases, 6 HermiT cases and bounded native/refusal
checks. The four-policy integration is an evidence/provenance audit, not a fresh
execution of the four detector engines. Copied-W6 database results are retained
historical evidence, not replayed here. Full-model 20-family, scientific and GA
acceptance remain pending. Successful replay does not create a tag or release.

To rebuild, use build_bundle.py with the exact 64edf15 source files and a0a9a53
scope files (or their verified extracted source/ and scope/ directories):

```sh
python build_bundle.py --source-root /path/to/exact/source   --scope-root /path/to/exact/scope --output-dir /path/to/new-build-directory
```

Build evidence records the immutable source, scope, contract and builder code
hashes; artifact retention is finite, so the committed builder and hash-pinned
inputs are the durable reconstruction route. Actual release assets and tag/source
agreement must be verified independently in RC-03.
